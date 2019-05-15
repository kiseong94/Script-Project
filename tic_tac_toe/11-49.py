from tkinter import *
import random

class hh:
    def again(self):
        for i in range(9):
            self.labelList[i].configure(image=self.imageList[random.randint(0, 1)])

    def __init__(self):
        window = Tk()
        self.imageList = []
        self.labelList = []
        self.imageList.append(PhotoImage(file='image/o.gif'))
        self.imageList.append(PhotoImage(file='image/x.gif'))
        frame = Frame(window)
        frame.pack()
        for i in range(9):
            self.labelList.append(Label(frame, image=self.imageList[random.randint(0, 1)]))
            self.labelList[i].grid(row=i//3, column=i%3)
        frame2 = Frame(window)
        frame2.pack()
        Button(frame2, text="다시생성", command=self.again).pack()

        window.mainloop()

hh()