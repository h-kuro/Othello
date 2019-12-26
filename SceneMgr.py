import tkinter

from Game import Game


class SceneMgr:
    __root = None
    __scene = None

    def __init__(self):
        self.__root = tkinter.Tk()
        self.__root.resizable(0, 0)
        self.__root.title("Othello")
        self.__root.geometry("1024x768")

        self.__scene = Game(self.__root)
        self.__scene.pack()

        self.__callback()

        self.__root.mainloop()

    def __callback(self):
        self.__scene.update()
        self.__root.after(int(1000 / 60), self.__callback)
