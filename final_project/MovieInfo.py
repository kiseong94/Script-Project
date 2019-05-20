import urllib.request
from bs4 import BeautifulSoup
import re

#import http.client
#conn = http.client.HTTPSConnection("movie.naver.com")
#conn.request("GET", "/movie/bi/ti/running.nhn?code=92")
#req = conn.getresponse() 			#openAPI 서버에서 보내온 요청을 받아옴
#print(req.status, req.reason)

#print(req.read().decode("euc-kr"))

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


def getMovieInfoFromCGV():
    pass


