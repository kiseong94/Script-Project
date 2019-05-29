import movie_info
import box_office
import theater_info
from functools import partial
import tkinter as tk
import tkinter.ttk
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

        # 데이터
        self.BoxOffice = box_office.GetBoxOfficeRankInfo()
        self.MovieSearchResult = None
        self.MovieInfo = None
        self.MovieSearchEntry = None
        self.MovieDetailInfo = None
        self.TheaterList = None
        self.TheaterInfo = None
        self.canvas = None
        self.scrollbar = None
        self.LocationComboBox =None
        self.LoadImage()
        self.frame1_page = 0
        self.frame2_page = 0
        self.IsMovieSearched = False
        self.ShowDetail = False

        menu = tk.Frame(self.window,width=1400,height=120,bg='red')
        menu.pack()
        tk.Label(menu,image = self.TitleImage,bg='red').place(x=30,y=0)
        tk.Button(menu,relief='flat',bg='red', image = self.MenuButtonImages[0],command = lambda : self.ChangeFrame(1) ).place(x=750, y=60)
        tk.Button(menu,relief='flat',bg='red', image = self.MenuButtonImages[1],command = lambda : self.ChangeFrame(2)).place(x=960, y=60)
        tk.Button(menu,relief='flat',bg='red', image = self.MenuButtonImages[2],command = lambda : self.ChangeFrame(3)).place(x=1170, y=60)

        self.subframe =None
        self.ChangeFrame(1)
        self.subframe.pack()




        tk.mainloop()

    def GetFrame1(self):

        frame = tk.Frame(self.window,width = 1400, height = 680, bg="gray")
        tk.Label(frame,width=1400,height = 680, image = self.bg).place(x=-2,y=-2)

        SubFrame = tk.Frame(frame,width = 1000, height = 690, bg='black',highlightbackground="firebrick4", highlightthickness=3)
        SubFrame.place(x=200,y=-5)

        font = tk.font.Font(family="맑은 고딕",size=10)


        x,y=100,150
        idx = 0

        tk.Button(SubFrame, text="◀",command = lambda : self.Frame1_ChangePage(0)).place(x = 20 ,y=320)
        tk.Button(SubFrame, text="▶", command=lambda: self.Frame1_ChangePage(1)).place(x = 1000-55 ,y=320)

        for data in self.BoxOffice[self.frame1_page]:
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
        return frame

    def GetFrame2(self):
        font = tk.font.Font(family="맑은 고딕", size=10)
        frame = tk.Frame(self.window,width=1400, height=680, bg='white')
        tk.Label(frame,image=self.Frame2LabelImage[0],bg='white').place(x=5,y=-2)
        self.MovieSearchEntry = tk.Entry(frame,width=50,bg='gray90')
        self.MovieSearchEntry.place(x=125,y=3)
        tk.Button(frame,relief='flat', bg='white', image = self.SearchButtonImage[0] ,command = self.Frame2_SearchMovie).place(x=530, y=-3)

        SubFrame = tk.Frame(frame,width=1406,height=656,bg='wheat1',highlightbackground="wheat4", highlightthickness=3)
        SubFrame.place(y=30,x=-3)



        x, y = 50, 100
        idx = 0
        if self.MovieInfo:
            tk.Label(SubFrame, text="총 "+str(self.MovieSearchResult[0])+" 개의 검색 결과가 있습니다",bg='wheat1').place(x=20,y=20)
            tk.Label(SubFrame, text= str(self.frame2_page+1)+" / "+str( self.MovieSearchResult[0]//10+1), bg='wheat1').place(x=380,y=70)
            tk.Button(SubFrame, text="◀", command=lambda:self.Frame2_ChangePage(0)).place(x=10, y=300)
            tk.Button(SubFrame, text="▶", command=lambda:self.Frame2_ChangePage(1)).place(x=770, y=300)
            for data in self.MovieInfo:
                entry = tk.Frame(SubFrame,width=80,height=200,bg="wheat2")
                entry.place(x=x,y=y)
                tk.Button(entry,relief='flat',image=data["img"],command = partial(self.Frame2_GetMovieDetailInfo, data)).pack()
                tk.Label(entry,width=12,text= str(data["name"]),bg="wheat1",fg="black",wraplength=120).pack()
                idx +=1
                if idx == 5:
                    x=50
                    y+=250
                else:
                    x+=150
        else:
            if self.IsMovieSearched:
                tk.Label(SubFrame, text="검색 결과가 없습니다",bg='wheat1').place(x=20, y=20)

        if self.ShowDetail:
            f = tk.Frame(SubFrame,width=600, height=656)
            f.place(y=0,x=800)
            self.scrollbar = tk.Scrollbar(f, orient="vertical")
            self.canvas = tk.Canvas(f, bg='bisque',width=580,height=656,highlightthickness=0, yscrollcommand=self.scrollbar.set)

            self.scrollbar.config(command=self.canvas.yview)
            self.scrollbar.pack(side="right", fill="y")
            self.canvas.pack(fill="both", expand=True)

            self.canvas.yview_moveto(0)

            self.DetailFrame = tk.Frame(self.canvas,width=600,height=656, bg='bisque')
            self.canvas.create_window(0, 0, window=self.DetailFrame,anchor='nw')

            self.DetailFrame.bind('<Configure>', self.FrameConfigure)

            tk.Label(self.DetailFrame, bg='bisque', text=self.MovieDetailInfo["name"],font=font,wraplength=550).grid(row=0, column=0)
            tk.Label(self.DetailFrame, width=500, bg='bisque', image=self.MovieDetailInfo["big_img"]).grid(row=1,column=0)
            if 'director' in self.MovieDetailInfo.keys():
                tk.Label(self.DetailFrame, bg='bisque', text=self.MovieDetailInfo["director"],wraplength=500).grid(row=2,column=0)
            if 'actors' in self.MovieDetailInfo.keys():
                tk.Label(self.DetailFrame, bg='bisque', text=self.MovieDetailInfo["actors"], wraplength=500).grid(row=3,column=0)
            if 'story' in self.MovieDetailInfo.keys():
                tk.Label(self.DetailFrame, bg='bisque', text=self.MovieDetailInfo["story"],wraplength=500).grid(row=4,column=0)

        return frame

    def GetFrame3(self):
        frame = tk.Frame(self.window,width=1400, bg='LightBlue1', height=680)
        tk.Label(frame, image=self.Frame3LabelImage[0], bg='LightBlue1').place(x=5, y=-2)
        tk.Label(frame, image=self.Frame3LabelImage[1], bg='LightBlue1').place(x=280, y=-2)
        if self.LocationComboBox==None:
            self.LocationComboBox = tkinter.ttk.Combobox(frame,state="readonly", width=15, height=10, values=theater_info.location_table)
        else:
            self.LocationComboBox = tkinter.ttk.Combobox(frame,textvariable="서울특별시", width=15, state="readonly", height=10,values=theater_info.location_table)
        self.LocationComboBox.place(x=120,y=2)
        self.LocationComboBox.bind("<<ComboboxSelected>>", self.ComboBoxCallBack)

        self.SubLocationComboBox = tkinter.ttk.Combobox(frame, state="readonly", width=25, height=10, values=theater_info.sub_location_table[self.LocationComboBox.get()])
        self.SubLocationComboBox.place(x=395, y=2)
        tk.Button(frame, relief='flat', bg='LightBlue1', image=self.SearchButtonImage[1],command = self.Frame3_GetTheaterList).place(x=623, y=-3)

        SubFrame = tk.Frame(frame,width=1406,height=656,bg='snow3',highlightbackground="grey50", highlightthickness=3)
        TheaterListFrame = tk.Frame(SubFrame,width=275,height=656,highlightbackground="grey50", highlightthickness=3)

        TheaterListSubFrame = tk.Frame(TheaterListFrame, width=300, height=656)
        tk.Label(TheaterListSubFrame,text='영 화 관',width=24,bd=3, relief='raised',
                        bg='lavender', fg='black',font=('HY견고딕', 10,'italic')).place(x=0,y=0)
        if self.TheaterList != None:
            f = tk.Frame(TheaterListSubFrame, width=270, height=626)
            f.place(x=0,y=26)
            self.scrollbar = tk.Scrollbar(f, orient="vertical")
            self.canvas = tk.Canvas(f, width=250, height=626, highlightthickness=0,
                                    yscrollcommand=self.scrollbar.set)

            self.scrollbar.config(command=self.canvas.yview)
            self.scrollbar.pack(side="right", fill="y")
            self.canvas.pack(fill="both", expand=True)

            self.DetailFrame = tk.Frame(self.canvas, width=250, height=626)
            self.canvas.create_window(0, 0, window=self.DetailFrame, anchor='nw')

            self.DetailFrame.bind('<Configure>', self.FrameConfigure)
            idx=0
            for theater in self.TheaterList:
                tk.Button( self.DetailFrame,width=23,text=theater["name"],cursor='hand2',bd=6, relief='raised',
                          bg='black', fg='white',font=('helvetica', 10, 'italic'),command = partial(self.GetTheaterInfo,theater)).grid(row=idx,column=0)
                idx+=1

        TheaterInfoFrame = tk.Frame(SubFrame,width=1200,height=656,highlightbackground="grey50", highlightthickness=3)

        if self.TheaterInfo != None:
            tk.Label(TheaterInfoFrame, text=self.TheaterInfo['name'], font=('맑은 고딕', 18, 'bold')).place(x=10, y=10)
#===================================== 상영 정보 스크롤링 ==========================

            TheaterInfoSubFrame = tk.Frame(TheaterInfoFrame, width=550, height=460)
            TheaterInfoSubFrame.place(x=0, y=26)
            self.scrollbar2 = tk.Scrollbar(TheaterInfoSubFrame, orient="vertical")
            self.canvas2 = tk.Canvas(TheaterInfoSubFrame, width=550, height=460, highlightthickness=0,
                                    yscrollcommand=self.scrollbar2.set)

            self.scrollbar2.config(command=self.canvas2.yview)
            self.scrollbar2.pack(side="right", fill="y")
            self.canvas2.pack(fill="both", expand=True)

            self.canvas2.yview_moveto(0)

            self.DetailFrame2 = tk.Frame(self.canvas2, width=550, height=460)
            self.canvas2.create_window(0, 0, window=self.DetailFrame2, anchor='nw')

            self.DetailFrame2.bind('<Configure>', self.FrameConfigure2)

            idx = 0
            for info in self.TheaterInfo['info']:
                tk.Label(self.DetailFrame2,text=info['movie'],font=('맑은 고딕', 10, 'bold')).grid(row=idx,sticky='w')
                idx+=1
                TimeFrame = tk.Frame(self.DetailFrame2)
                row,column = 0,0
                for time in info['time']:
                    if column == 10:
                        tk.Label(TimeFrame, text=time,relief = 'groove').grid(row=row,column=column)
                        row += 1
                        column = 0
                    else:
                        tk.Label(TimeFrame, text=time, relief='groove').grid(row=row,column=column)
                        column += 1

                TimeFrame.grid(row=idx,sticky='w')
                idx += 1

            TheaterInfoSubFrame.place(x=50, y=100)

        TheaterInfoFrame.place(x=300,y=-3)
        TheaterListSubFrame.place(x=0,y=0)
        TheaterListFrame.place(x=-3,y=-3)
        SubFrame.place(x=-3,y=30)

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

    def Frame1_ChangePage(self, dir):
        if dir == 0:
            self.frame1_page -= 1
            self.frame1_page = max(self.frame1_page, 0)
        else:
            self.frame1_page += 1
            self.frame1_page = min(self.frame1_page, 3)
        self.ChangeFrame(1)

    def Frame2_ChangePage(self, dir):
        prev = self.frame2_page
        if dir == 0:
            self.frame2_page -= 1
            self.frame2_page = max(self.frame2_page, 0)
        else:
            self.frame2_page += 1
            self.frame2_page = min(self.frame2_page, self.MovieSearchResult[0]//10)
        if self.frame2_page != prev:
            self.Frame2_GetMovieInfo()
            self.ChangeFrame(2)

    def Frame2_SearchMovie(self):
        self.MovieSearchResult = movie_info.SearchMovie(self.MovieSearchEntry.get())
        self.IsMovieSearched = True
        self.ShowDetail = False
        if self.MovieSearchResult != None:
            self.frame2_page = 0
            self.Frame2_GetMovieInfo()
        else:
            self.MovieInfo = None
            self.ChangeFrame(2)

    def Frame2_GetMovieInfo(self):
        self.MovieInfo = movie_info.GetSearchResult(self.MovieSearchResult[1],self.frame2_page)
        self.ChangeFrame(2)

    def Frame2_GetMovieDetailInfo(self, data):
        self.ShowDetail = True
        self.MovieDetailInfo = movie_info.GetDetailInfo(data['detailURL'])
        self.MovieDetailInfo = {**self.MovieDetailInfo,**data}
        self.ChangeFrame(2)

    def Frame3_GetTheaterList(self):
        if self.LocationComboBox.get() != "":

            self.TheaterInfo = None
            self.TheaterList = theater_info.getTheaterInfo(self.LocationComboBox.get(),self.SubLocationComboBox.get())
            self.ChangeFrame(3)

    def GetTheaterInfo(self,theater):
        self.TheaterInfo = theater_info.GetMovieInfo(theater)
        self.TheaterInfo['name'] = theater['name']
        self.ChangeFrame(3)

    def FrameConfigure(self,event):
        self.canvas.configure(scrollregion = self.canvas.bbox("all"))

    def FrameConfigure2(self,event):
        self.canvas2.configure(scrollregion = self.canvas2.bbox("all"))

    def ComboBoxCallBack(self,event):
        self.ChangeFrame(3)

    def LoadImage(self):
        self.bg = tk.PhotoImage(file="image/bg0.gif")
        self.TitleImage = tk.PhotoImage(file="image/title.png")
        self.MenuButtonImages = [tk.PhotoImage(file="image/button1.png"),tk.PhotoImage(file="image/button2.png"),tk.PhotoImage(file="image/button3.png")]
        self.SearchButtonImage = [tk.PhotoImage(file="image/search_button.png"),tk.PhotoImage(file="image/search_button2.png")]
        self.Frame2LabelImage = [tk.PhotoImage(file="image/f2_label1.png")]
        self.Frame3LabelImage = [tk.PhotoImage(file="image/f3_label1.png"),tk.PhotoImage(file="image/f3_label2.png")]




# search_result = movie_info.SearchMovie("반지")
#
# if search_result == None:
#     print("검색 결과가 없습니다")
# else:
#     total_page = 10/search_result[0]
#     movie_info.GetSearchResult(search_result[1],0)

movie = MovieQuitous()