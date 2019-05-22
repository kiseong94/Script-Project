import movie_info
import box_office
import tkinter as tk
import tkinter.font
import urllib.request
import io
from PIL import Image,ImageTk
import base64




def GetImageFromURL(url):
    u = urllib.request.urlopen(url)
    raw_data = u.read()
    im = Image.open(io.BytesIO(raw_data))
    image = ImageTk.PhotoImage(im)
    u.close()
    return image


class MovieQuitous:
    def __init__(self):
        self.window = tk.Tk()
        self.window.geometry("1400x800")
        self.bg=tk.PhotoImage(file="image/bg0.gif")
        self.page = 0

        menu = tk.Frame(self.window,width=1400,height=120,bg='red')
        menu.pack()
        tk.Button(menu, text="dddd",command = lambda : self.ChangeFrame(1) ).place(x=800, y=50)
        tk.Button(menu, text="dddd",command = lambda : self.ChangeFrame(2)).place(x=1000, y=50)
        tk.Button(menu, text="dddd",command = lambda : self.ChangeFrame(3)).place(x=1200, y=50)

        self.subframe =None
        self.ChangeFrame(2)
        self.subframe.pack()

        self.BoxOffice = box_office.GetBoxOfficeRankInfo()

        # image = GetImageFromURL("https://movie-phinf.pstatic.net/20170112_240/1484183668820LGsTJ_JPEG/movie_image.jpg?type=f67")
        # imageLabel = Label(image=image)
        # imageLabel.pack()

        images=[]
        # for page in BoxOffice:
        #
        #     for i in page:
        #         images.append(GetImageFromURL(i["img"]))
        #         imageLabel = tk.Label(frame,image=images[-1])
        #         imageLabel.place(x=x,y=y)
        #         x+=120
        #     x=0
        #     y+=200

        tk.mainloop()

    def GetFrame1(self):

        frame = tk.Frame(self.window,width = 1400, height = 680, bg="gray")
        tk.Label(frame,width=1400,height = 680, image = self.bg).place(x=-2,y=-2)

        SubFrame = tk.Frame(frame,width = 1000, height = 690, bg='black',highlightbackground="firebrick4", highlightthickness=3)
        SubFrame.place(x=200,y=-5)

        font = tk.font.Font(family="맑은 고딕",size=10)

        entries = []
        x,y=100,150
        idx = 0

        tk.Button(SubFrame, text="◀",command = lambda : self.Frame1_ChangePage(0)).place(x = 20 ,y=320)
        tk.Button(SubFrame, text="▶", command=lambda: self.Frame1_ChangePage(1)).place(x = 1000-55 ,y=320)

        for data in self.BoxOffice[self.page]:
            entry = tk.Frame(SubFrame,width=300,height=200,bg="black")
            entry.place(x=x,y=y)
            tk.Label(entry, image=data["img"]).pack()
            tk.Label(entry,width=20,text= str(data["rank"])+"위  "+data["name"],font = font,bg="black",fg="white",wraplength=180).pack()

            idx +=1

            if idx == 4:
                x=100
                y+=250
            else:
                x+=200
            entries.append(entry)



        return frame
    def Frame1_ChangePage(self,dir):
        if dir == 0:
            self.page -= 1
            self.page = max(self.page,0)
        else:
            self.page += 1
            self.page = min(self.page, 3)
        self.ChangeFrame(1)


    def GetFrame2(self):
        frame = tk.Frame(self.window,width=1400, height=680, bg='yellow')
        tk.Button(frame, text="fff").place(x=200,y=300)
        return frame

    def GetFrame3(self):
        frame = tk.Frame(self.window,width=1400, height=680, bg='white')
        tk.Button(frame, text="ggg").place(x=200,y=300)
        return frame

    def ChangeFrame(self,frame_num):
        if self.subframe:
            self.subframe.destroy()
        if frame_num == 1:
            self.subframe = self.GetFrame1()
        elif frame_num == 2:
            self.subframe = self.GetFrame2()
        elif frame_num == 3:
            self.subframe = self.GetFrame3()
        self.subframe.pack()




# search_result = movie_info.SearchMovie("반지")
#
# if search_result == None:
#     print("검색 결과가 없습니다")
# else:
#     total_page = 10/search_result[0]
#     movie_info.GetSearchResult(search_result[1],0)

movie = MovieQuitous()