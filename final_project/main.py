import movie_info
from tkinter import *
from urllib


class MovieQuitous:
    def __init__(self):
        tk = Tk()

        tk.mainloop()





search_result = movie_info.SearchMovie("반지")

if search_result == None:
    print("검색 결과가 없습니다")
else:
    total_page = 10/search_result[0]
    movie_info.GetSearchResult(search_result[1],0)

