from tkinter import *
import tkinter.messagebox

class Samok:
    def __init__(self):
        self.window = Tk()
        self.frame = Frame(self.window)
        self.frame.pack()
        self.frame2 = Frame(self.window)
        self.frame2.pack()
        self.imageList = []
        self.winImageList = []
        self.imageList.append(PhotoImage(file='image/x.gif'))
        self.imageList.append(PhotoImage(file='image/o.gif'))
        self.imageList.append(PhotoImage(file='image/empty.gif'))
        self.winImageList.append(PhotoImage(file='image/win_x.gif'))
        self.winImageList.append(PhotoImage(file='image/win_o.gif'))
        self.buttonList = []
        self.positList = []
        self.colList = [0] * 7
        self.count = 0
        self.TheGame = True
        self.turn = True

        for i in range(42):
            self.buttonList.append(Button(self.frame, text=' ', image=self.imageList[2],
                                          command=lambda col=i % 7: self.fill(col)))
            # text를 사용할 필요는 없지만 text를 이용하여 button의 정보를 가지고 올 수 있기 때문에
            # 사용해도 좋다.
            self.buttonList[i].grid(row=i // 7, column=i % 7)

        self.resetButton = Button(self.frame2, text='새로시작', command=self.Reset)
        self.resetButton.pack()

        self.window.mainloop()

    def fill(self, col):
        if self.colList[col] < 6 and self.TheGame:
            self.buttonList[(5 - self.colList[col]) * 7 + col].configure(image=self.imageList[self.turn])
            if self.turn:
                self.buttonList[(5 - self.colList[col]) * 7 + col].configure(text='o')
            else:
                self.buttonList[(5 - self.colList[col]) * 7 + col].configure(text='x')
            self.colList[col] += 1
            self.turn = not self.turn
            self.count += 1
            endgame = self.Endgame(6-self.colList[col], col, self.turn)   # 결과를 확인하기 위해 사용

            if endgame == 1 or endgame == 2:
                self.TheGame = False
                self.AnimateWin(endgame-1)

            if endgame == 1:
                tkinter.messagebox.showinfo('승리', 'o가 승리하였습니다')
            elif endgame == 2:
                tkinter.messagebox.showinfo('승리', 'x가 승리하였습니다')
            elif endgame == 3:
                tkinter.messagebox.showinfo('비김', '비겼습니다')


    def AnimateWin(self, who):
        self.color = 0
        for i in range(40):
            self.frame.after(100)
            self.color= not self.color
            for j in range(4):
                if self.color:
                    self.buttonList[(self.positList[j][0])*7+self.positList[j][1]]['image'] \
                        = self.winImageList[not who]
                else:
                    self.buttonList[(self.positList[j][0]) * 7 + self.positList[j][1]]['image'] \
                        = self.imageList[not who]
            self.frame.update()

    def DisableAllButton(self):
        for i in range(42):
            self.buttonList[i]['state'] = 'disable'

    def Endgame(self, row, col, turn):
        directionTuple = ((1, 0), (0, 1), (1, 1), (1, -1))
        value = 0
        for i in range(4):
            self.positList.clear()
            value = self.confirm(row, col, directionTuple[i])
            if value == 1:
                break

        if value == 1:
            return turn + 1
        if self.count == 42:
            return 3
        return 0

    def Reset(self):
        self.positList.clear()
        self.colList = [0] * 7
        self.count = 0
        self.turn = True
        self.TheGame = True

        for i in range(42):
            self.buttonList[i]['text'] = ' '
            self.buttonList[i]['image'] = self.imageList[2]
            self.buttonList[i]['state'] = 'normal'

    def confirm(self, row, col, tup):
        fill = 0
        dx, dy = 0, 0
        while (row + dx) != 6 and (row + dx) != -1 and (col + dy) != 7 and (col + dy) != -1:
            if self.buttonList[(row+dx) * 7 + (col+dy)]['text'] == self.buttonList[row * 7 + col]['text']:
                self.positList.append((row + dx, col + dy))
                fill += 1
                dx += tup[0]
                dy += tup[1]
            else:
                break

        dx, dy = tup[0], tup[1]
        while (row - dx) != 6 and (row - dx) != -1 and (col - dy) != 7 and (col - dy) != -1:
            if self.buttonList[(row-dx) * 7 + (col-dy)]['text'] == self.buttonList[row * 7 + col]['text']:
                self.positList.append((row - dx, col - dy))
                fill += 1
                dx += tup[0]
                dy += tup[1]
            else:
                break

        if fill >= 4:
            return True
        else:
            return False

Samok()