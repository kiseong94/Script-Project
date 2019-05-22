import urllib.request
from bs4 import BeautifulSoup
from PIL import Image,ImageTk
import io
import re

# dict 형식 = {"rank" : 랭킹, "name": 제목 ,"img" : 이미지 URL}

def GetImageFromURL(url):
    u = urllib.request.urlopen(url)
    raw_data = u.read()
    im = Image.open(io.BytesIO(raw_data))
    image = ImageTk.PhotoImage(im)
    u.close()
    return image



def GetBoxOfficeRankInfo():

    BoxOfficeRankInfo = []

    URL =  "https://search.naver.com/search.naver?sm=top_hty&fbm=0&ie=utf8&query=%EB%B0%95%EC%8A%A4%EC%98%A4%ED%94%BC%EC%8A%A4"
    req = urllib.request.Request(URL)
    data = urllib.request.urlopen(req).read()

    bs = BeautifulSoup(data, 'html.parser')

    pages = bs.find_all("div", {"class": "_content"})

    rank = 1
    for page in pages:
        page_list = []
        l1 = page.find_all("strong")
        l2 = page.find_all("img")
        for i in range(len(l1)):
            name = re.search('\>(.*?)\<', str(l1[i]))
            img_url = re.search('src="(.*?)"', str(l2[i]))

            info = dict( rank = rank ,name = name.group(1), img = GetImageFromURL(img_url.group(1)))
            page_list.append(info)
            rank+=1
        BoxOfficeRankInfo.append(page_list)
    # for i in BoxOfficeRankInfo:
    #     print(i)
    return BoxOfficeRankInfo

