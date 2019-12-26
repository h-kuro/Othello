import tkinter


class Disc(tkinter.Canvas):
    __id = None
    __fill = None
    __x = None
    __y = None
    __eventRelease = None
    __eventCursor = None

    def __init__(self, master=None, cnf={}, **kw):
        tkinter.Canvas.__init__(self, master, cnf, **kw)
        tkinter.Canvas(self, width=12, height=12)
        self.bind("<ButtonRelease-1>", self.__release)
        self.bind("<Enter>", self.__enter)
        self.bind("<Leave>", self.__leave)
        self.__id = self.create_oval(5, 5, 89, 89)
        self.myConfig(fill="GREEN4", outline="GREEN4")
        self.__event = False
        self.__fill = "NONE"

    def myConfig(self, **kw):
        self.itemconfig(self.__id, kw)

    def SetPoint(self, x, y):
        self.__x = x
        self.__y = y

    def getPoint(self):
        return self.__x, self.__y

    def __release(self, event):
        self.__eventRelease = True

    def __enter(self, event):
        self.__eventCursor = True

    def __leave(self, event):
        self.__eventCursor = False

    def placing(self, color):
        self.myConfig(fill=color)
        self.__fill = color

    def getRelease(self):
        return self.__eventRelease

    def setRelease(self, event):
        self.__eventRelease = event

    def getCursor(self):
        return self.__eventCursor

    def getFill(self):
        return self.__fill

    def setFill(self, fill):
        self.__fill = fill
