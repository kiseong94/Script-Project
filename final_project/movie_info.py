import urllib.request
import urllib.parse
import requests
import http.client
from bs4 import BeautifulSoup
import json
import re


def SearchMovie(name):

    BaseURL = "https://movie.naver.com/movie/search/result.nhn?section=movie&query="
    URL = BaseURL+urllib.parse.quote(name.encode("euc-kr"))
    #req = urllib.request.Request(URL)
    #data = urllib.request.urlopen(req).read()
    req = requests.get(URL)
    req.encoding = 'euc-kr'
    bs = BeautifulSoup(req.text, 'html.parser')

    l = bs.find_all("span",{"class":"num"})

    if len(l) == 0:
        return None
    else:
        r = re.search(' (\d+)건',str(l))
        result_num = eval(r.group(1))

        return (result_num, URL+"&page=")


def GetSearchResult(url, page):
    PageMovieInfoList = []
    url = url+str(page+1)
    print(url)
    req = requests.get(url)
    req.encoding = 'euc-kr'
    bs = BeautifulSoup(req.text, 'html.parser')

    l = bs.find("ul",{"class":"search_list_1"}).find_all("li")

    for e in l:
        info = dict()
#영화 제목
        name_data = e.find("dt")
        name_data = str(name_data).replace("<strong>","")
        name_data = name_data.replace("</strong>", "")
        name = re.search('">(.+?)</',name_data)
        info["name"] = name.group(1)

        url = re.search('href="(.+?)">', name_data)
        info["detailURL"] = "https://movie.naver.com"+url.group(1)


#이미지 링크
        image_data = e.find("img")
        image = re.search('src="(.*?)"',str(image_data))
        info["imgURL"] = image.group(1)
#기타
        genre = []
        nation = []
        etc_data = e.find_all("dd",{"class":"etc"})
        for d in etc_data[0].find_all("a"):
            if "genre" in str(d):
                data = re.search('\>(.+?)\<', str(d))
                if data:
                    genre.append(data.group(1))
            elif "nation" in str(d):
                data = re.search('\>(.+?)\<', str(d))
                if data:
                    nation.append(data.group(1))
            elif "year" in str(d):
                data = re.search('\>(.+?)\<', str(d))
                if data:
                    info["year"] = data.group(1)
        info["genre"] = genre
        info["nation"] = nation

# 감독 배우
        actors = []
        first=True
        for d in etc_data[1].find_all("a"):
            data = re.search('\>(.+?)\<', str(d))
            if data:
                if first:
                    info["director"] = data.group(1)
                    first = False
                else:
                    actors.append(data.group(1))
        info["actors"] = actors

        PageMovieInfoList.append(info)


    for i in PageMovieInfoList:
        print(i)


# def SearchMovie(name):
#
#     MovieList=[]
#
#     conn = http.client.HTTPConnection("www.kobis.or.kr")
#     URL = "/kobisopenapi/webservice/rest/movie/searchMovieList.json?key=430156241533f1d058c603178cc3ca0e&itemPerPage=50&movieNm="+urllib.parse.quote(name)
#     conn.request("GET", URL)  # 서버에 GET 요청
#     req = conn.getresponse()  # openAPI 서버에서 보내온 요청을 받아옴
#     data = json.loads(req.read().decode("UTF-8"))
#
#     for i in data["movieListResult"]["movieList"]:
#         MovieList.append(i["movieNm"])
#         print(i["movieNm"])
#         GetMovieInfo(i["movieNm"])
#
#     return MovieList

#GetMovieInfo("영화 반지")
SearchMovie("해리포터")