import sys
import tkinter
from tkinter import font, messagebox

from Disc import Disc
from DiscState import DiscState


class Game(tkinter.Frame):
    __main = None
    __sub = None
    __COLOR = ("WHITE", "BLACK")
    __placeList = dict()
    __discs = list()
    __discStates = list()
    __whiteCountLabel = None
    __blackCountLabel = None
    __turnLabel = None
    __restartButton = None
    __exitButton = None
    __font = None
    __turn = False
    __white = 0
    __black = 0
    __none = 0
    __resultDraw = False

    def __init__(self, master=None):
        tkinter.Frame.__init__(self, master)

        self.__sub = tkinter.Frame(self, width=256, height=768, bg="gray60")
        self.__sub.pack(side="left")
        self.__sub.propagate(False)

        self.__font = font.Font(self, family="MS Gothic", size=int(768 / 24))

        self.__blackCountLabel = tkinter.Label(self.__sub, width=11, bg="gray60", font=self.__font, fg="BLACK",
                                               anchor="w")
        self.__blackCountLabel.place(y=0)
        self.__whiteCountLabel = tkinter.Label(self.__sub, width=11, bg="gray60", font=self.__font, fg="WHITE",
                                               anchor="w")
        self.__whiteCountLabel.place(y=50)
        self.__turnLabel = tkinter.Label(self.__sub, width=11, bg="gray60", font=self.__font, border=1)
        self.__turnLabel.place(y=(768 / 2) - (50 / 2))

        self.__restartButton = tkinter.Button(self.__sub, width=12, bg="gray60", font=self.__font, text="NEXT",
                                              command=self.__restartClick)
        self.__restartButton.place(y=768 - 150)

        self.__exitButton = tkinter.Button(self.__sub, width=12, bg="gray60", font=self.__font, text="EXIT",
                                           command=self.__exitClick)
        self.__exitButton.place(y=768 - 75)

        self.__main = tkinter.Frame(self, width=768, height=768)
        self.__main.pack(side="left")
        self.__main.propagate(False)

        self.__gameInit()

    def __gameInit(self):
        if self.__discs is not None:
            self.__discs.clear()
        if self.__discStates is not None:
            self.__discStates.clear()

        for x in range(8):
            self.__discs.append(list())
            self.__discStates.append(list())
            for y in range(8):
                self.__discs[x].append(
                    Disc(self.__main, width=94, height=94, bg="Green4", highlightthickness=1,
                         highlightbackground="GRAY20"))
                self.__discs[x][y].grid(column=x, row=y)
                self.__discs[x][y].SetPoint(x, y)
                self.__discStates[x].append(
                    DiscState(self.__discs[x][y].getRelease(), self.__discs[x][y].getFill()))

        self.__turn = True

        # BLACK
        self.__systemPlacing(4, 3)
        self.__systemPlacing(3, 4)

        self.__nextTurn()

        # WHITE
        self.__systemPlacing(3, 3)
        self.__systemPlacing(4, 4)

        self.__nextTurn()

    def update(self):
        for x in range(8):
            for y in range(8):
                if (not self.__discStates[x][y].state) and self.__discs[x][y].getRelease():
                    if self.__placing(x, y):
                        self.__nextTurn()
                        if len(self.__placeList) == 0:
                            self.__nextTurn()
                self.__discs[x][y].setRelease(False)
                if self.__discs[x][y].getFill() == "SpringGreen3":
                    self.__discs[x][y].myConfig(fill=self.__discStates[x][y].color)
                if self.__discs[x][y].getFill() == "SeaGreen2":
                    self.__discs[x][y].myConfig(fill="Green4")

        for x in range(8):
            for y in range(8):
                if self.__discs[x][y].getCursor():
                    try:
                        for point in self.__placeList.get(self.__discs[x][y].getPoint()):
                            self.__discs[point[0]][point[1]].myConfig(fill="SpringGreen3")
                            self.__discs[point[0]][point[1]].setFill("SpringGreen3")
                    except TypeError:
                        continue
        for point in self.__placeList.keys():
            self.__discs[point[0]][point[1]].myConfig(fill="SeaGreen2")
            self.__discs[point[0]][point[1]].setFill("SeaGreen2")

    def __placing(self, x, y):
        if self.__placeList.get((x, y), False):
            self.__systemPlacing(x, y)
            for i in self.__placeList.get((x, y)):
                self.__systemPlacing(i[0], i[1])
            return True
        else:
            return False

    def __systemPlacing(self, x, y):
        self.__discs[x][y].placing(self.__COLOR[self.__turn])
        self.__discStates[x][y].color = self.__COLOR[self.__turn]

    def __createPlaceList(self, turn):
        self.__placeList.clear()
        # 探査
        for x in range(8):
            for y in range(8):
                if self.__discStates[x][y].color != "NONE":
                    continue
                for addX in range(-1, 2):
                    for addY in range(-1, 2):
                        # 自分自身をスキップ
                        if addX == addY == 0:
                            continue
                        moveX = addX
                        moveY = addY

                        temp = list()
                        try:
                            while self.__discStates[x + moveX][y + moveY].color == self.__COLOR[not turn]:
                                temp.append(((x + moveX), (y + moveY)))
                                moveX += addX
                                moveY += addY
                                if (x + moveX < 0) or (y + moveY < 0):
                                    break
                                if self.__discStates[x + moveX][y + moveY].color == self.__COLOR[turn]:
                                    if self.__placeList.get((x, y)) is None:
                                        self.__placeList[x, y] = list()
                                    self.__placeList[(x, y)].extend(temp)
                                if self.__discStates[x + moveX][y + moveY].color == "NONE":
                                    break
                        except IndexError:
                            break

    def __drawInfo(self):
        self.__black = 0
        self.__white = 0
        self.__none = 0
        for x in range(8):
            for y in range(8):
                if self.__discStates[x][y].color == "WHITE":
                    self.__white += 1
                if self.__discStates[x][y].color == "BLACK":
                    self.__black += 1
                if self.__discStates[x][y].color == "NONE":
                    self.__none += 1

        self.__blackCountLabel.configure(text="黒:" + str(self.__black) + "個")
        self.__whiteCountLabel.configure(text="白:" + str(self.__white) + "個")
        if self.__turn:
            self.__turnLabel.configure(text="黒のターン", fg="BLACK")
        else:
            self.__turnLabel.configure(text="白のターン", fg="WHITE")

    def __nextTurn(self):
        self.__turn = not self.__turn
        self.__drawInfo()
        self.__createPlaceList(self.__turn)
        if self.__none == 0 and (not self.__resultDraw):
            self.__resultDraw = True
            if self.__white == self.__black:
                messagebox.showinfo("結果", "黒:" + str(self.__black) + "\n白:" + str(self.__white) + "\n\n引き分け")
            elif self.__white < self.__black:
                messagebox.showinfo("結果", "黒:" + str(self.__black) + "\n白:" + str(self.__white) + "\n\n黒の勝利")
            else:
                messagebox.showinfo("結果", "黒:" + str(self.__black) + "\n白:" + str(self.__white) + "\n\n白の勝利")

    def __restartClick(self):
        if messagebox.askyesno("確認", "ゲームを再起動しますか？"):
            self.__gameInit()

    @staticmethod
    def __exitClick():
        if messagebox.askyesno("確認", "ウインドウを閉じますか？"):
            sys.exit()
