from tkinter import *
import tkinter.messagebox

class hh:
    def again(self):
        for i in range(9):
            self.buttonList[i].configure(image=self.imageList[2])
            self.buttonList[i]['text'] = ''
            self.fillList[i] = False
        self.turn = True
        self.count = 0

    def EndGame(self, row, col, turn):
        if self.buttonList[row*3]['text'] == self.buttonList[row*3+1]['text'] == self.buttonList[row*3+2]['text']:
            return turn+1
        if self.buttonList[0*3+col]['text'] == self.buttonList[1*3+col]['text'] == self.buttonList[2*3+col]['text']:
            return turn+1
        if (col + row) % 2 == 0:
            if not(row == 0 and col == 2) and not(row == 2 and col == 0): 
                if self.buttonList[row*3+col]['text'] == self.buttonList[((row+1) % 3)*3+((col+1) % 3)]['text'] == \
                        self.buttonList[((row+2) % 3)*3+((col+2) % 3)]['text']:
                    return turn + 1
            if not(row == 0 and col == 0) and not(row == 2 and col == 2): 
                if self.buttonList[row*3+col]['text'] == self.buttonList[((row+1) % 3)*3+((col+2) % 3)]['text'] == \
                        self.buttonList[((row+2) % 3)*3+((col+1) % 3)]['text']:
                    return turn + 1
        if self.count == 9:
            return 3
        return 0

    def pressed(self, row, col):
        if self.fillList[row*3 + col] == False:
            self.count += 1
            if self.turn:
                self.buttonList[row*3 + col].configure(image=self.imageList[0])
                self.buttonList[row * 3 + col]['text'] = 'o'
            else:
                self.buttonList[row * 3 + col]['image'] = self.imageList[1]
                self.buttonList[row * 3 + col]['text'] = 'x'
            self.fillList[row*3 + col] = True
            self.turn = not self.turn
            endgame = self.EndGame(row, col, self.turn)

            if endgame == 1:
                tkinter.messagebox.showinfo('승리', 'o가 승리하였습니다')
                self.again()
            elif endgame == 2:
                tkinter.messagebox.showinfo('승리', 'x가 승리하였습니다')
                self.again()
            elif endgame == 3:
                tkinter.messagebox.showinfo('비김', '비겼습니다')
                self.again()

    def __init__(self):
        window = Tk()
        self.turn = True
        self.imageList = []
        self.imageList.append(PhotoImage(file='image/o.gif'))
        self.imageList.append(PhotoImage(file='image/x.gif'))
        self.imageList.append(PhotoImage(file='image/empty.gif'))
        frame = Frame(window)
        frame.pack()
        self.count = 0;
        self.buttonList = []
        self.fillList = [False] * 9
        for i in range(9):
            self.buttonList.append(
                Button(frame, image=self.imageList[2], text='',
                       command=lambda row=i // 3, col=i % 3: self.pressed(row, col)))
            self.buttonList[i].grid(row=i//3, column=i%3)
        frame2 = Frame(window)
        frame2.pack()
        Button(frame2, text="다시생성", command=self.again).pack()

        window.mainloop()

hh()
