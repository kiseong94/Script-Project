import urllib.request
from bs4 import BeautifulSoup
import re
import json

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


