import urllib.request
import urllib.parse
from bs4 import BeautifulSoup
import json
import re

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


search_key1=""
search_key2=""
baseURL = "http://movie.naver.com/movie/bi/ti/running.nhn?code="
#URL = baseURL + str(theatercode)
req = urllib.request.Request(GetURL(location_table[2],sub_location_table[location_table[2]][1]))
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

theater_list = []

for item in json_data:
    print(item)


