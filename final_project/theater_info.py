from bs4 import BeautifulSoup
import urllib.request
import urllib.parse
import json
import re


CGVTheaterTable = None
with open('CGVtheaterCode.json') as file:
    CGVTheaterTable = json.load(file)
#    print(CGVTheaterTable)
#     for i in CGVTheaterTable:
#         for j in i["AreaTheaterDetailList"]:
#             name = j["TheaterName"]
#             name = name.replace(" ","",4)
#             if name == 'CINEdeCHEF센텀':
#                 name = '씨네드쉐프센텀시티'
#             name = name.replace('CINEdeCHEF','씨네드쉐프')
#             t = (j["TheaterCode"],j["RegionCode"])
#             theater_list[name] = t
#
# with open('CGVtheaterCode.json', 'w', encoding="utf-8") as make_file:
#     json.dump(theater_list, make_file)



location_table = ["서울특별시", "인천광역시", "경기도", "세종특별자치시","대전광역시","충청도","강원도","광주광역시","전라도","대구광역시","울산광역시","부산광역시","경상도","제주특별자치도"]
sub_location_table = {
    "서울특별시": ["","도봉구.강북구.성북구.노원구","은평구.서대문구","종로구","마포구","중구.용산구","동대문구.중랑구.성동구.광진구","강서구.양천구.영등포구.구로구","동작구.관악구.금천구","강남구.서초구","강동구.송파구"],
    "인천광역시": ["","강화군","서구.계양구.부평구","중구.동구.미추홀구","남동구.연수구.웅진군"],
    "경기도": ["","파주시","고양시","양주시.의정부시","남양주시.구리시.가평군","김포시","부천시.광명시","시흥시.안산시","안양시.군포시.의왕시.과천시","수원시","성남시.하남시","용인시","화성시.오산시.평택시","이천시.안성시","광주시.양평군.여주시","연천군.포천시.동두천시"],
    "세종특별자치시": [""],
    "대전광역시": [""],
    "충청도": ["","청주시","천안시","당진시","보령시"],
    "강원도": ["","원주시"],
    "광주광역시": [""],
    "전라도" : ["","전주시","목포시","순천시","여수시"],
    "대구광역시" : ["","동구.수성구","중구","북구.서구.달서구"],
    "울산광역시" : [""],
    "부산광역시" : ["","해운대구","부산진구","중구.남구","금정구.북구.동래구.연제구"],
    "경상도" : ["","구미시","포항시","안동시","창원시","진주시","김해시","거제시.통영시"],
    "제주특별자치도" : [""]
}


def GetURL(location,sub_loaction):
    URL = "https://m.search.naver.com/p/csearch/content/apirender.nhn?_callback=window.__jindo2_callback&where=nexearch&pkid=38&key=TheaterListApi&q=%EC%98%81%ED%99%94%EA%B4%80&start=1&display=100&q_f1=location&q_f2=sub&q_f3=&q_f4="
    URL = URL.replace("location",urllib.parse.quote(location))
    URL = URL.replace("sub", urllib.parse.quote(sub_loaction))
    return URL

def getTheaterInfo(location, sub_location):
    baseURL = "http://movie.naver.com/movie/bi/ti/running.nhn?code="
    #URL = baseURL + str(theatercode)
    req = urllib.request.Request(GetURL(location_table[location],sub_location_table[location_table[location]][sub_location]))
    data = urllib.request.urlopen(req).read()

    data = data.decode("UTF-8")
    data = data[data.find("data"):]

    #print(data)

    m = re.search('\[(.*?)\]', str(data))
    if m:
        #print(m.group(1))
        data = m.group(1)
    data = "["+data+"]"
    #print(data)
    json_data = json.loads(data)

    theater_inform = []

    for item in json_data:
        code = re.search('\d+',item["endpage"])
        d = dict(name = item["name"],code = code.group(0), longitude = item["longitude"], latitude = item["latitude"])
        theater_inform.append(d)
    return theater_inform

def getMovieInfoFromNaver(theatercode):
    movie_inform_list = []

    baseURL = "http://movie.naver.com/movie/bi/ti/running.nhn?code="
    URL =  baseURL + str(theatercode)
    req = urllib.request.Request(URL)
    data = urllib.request.urlopen(req).read()

    bs = BeautifulSoup(data, 'html.parser')
    #print(bs)
    l1 = bs.find_all('th')
    l2 = bs.find_all('td')

    movie_name_list = []
    time_list = []

    for i in l1:
        e = i.find('a')
        name = re.search('\>(.*?)\<', str(e))

        if name:
            movie_name_list.append(name.group(1))

    for i in l2:
        time = re.findall('\d\d\:\d\d', str(i))
        if time:
            time_list.append(time)

    for i in range(len(movie_name_list)):
        movie_inform_list.append((movie_name_list[i],time_list[i]))

    return movie_inform_list


def getMovieInfoFromCGV(theater):
    global CGVTheaterTable

    movie_inform_list = []

    theater_name = theater.replace(" ","")
    baseURL = "http://www.cgv.co.kr/common/showtimes/iframeTheater.aspx?areacode=key1&theatercode=key0&date="
    URL = baseURL.replace('key0', CGVTheaterTable[theater_name][0])
    URL = URL.replace('key1', CGVTheaterTable[theater_name][1])

    req = urllib.request.Request(URL)
    data = urllib.request.urlopen(req).read()

    bs = BeautifulSoup(data, 'html.parser')

    #print(bs)

    movie_name_list = []

    l1 = bs.find("div", {"class" :"sect-showtimes"}).find_all("strong")
    l2 = bs.find("div", {"class": "sect-showtimes"}).find_all("div",{"class": "col-times"})
    time_list = []
    for i in l2:
        l = i.find_all("em")
        time = re.findall('\d\d\:\d\d', str(l))
        time_list.append(time)

    for i in l1:
        name = re.search('\s+(.*)\<', str(i))
        if name:
            movie_name_list.append(name.group(1))

    for i in range(len(movie_name_list)):
        movie_inform_list.append((movie_name_list[i],time_list[i]))

    return movie_inform_list






for t in getTheaterInfo(0,0):
    print(t['name'])

    if "씨네드쉐프" in t['name'] or "CGV" in t['name']:
        print(getMovieInfoFromCGV(t['name']))
    else:
        print(getMovieInfoFromNaver(t['code']))