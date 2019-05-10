from tkinter import *
from tkinter.font import Font
from time import sleep
import socket
import select
import threading

class MenuPrincipal(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.InitInterface()
        self.mainloop()
    def InitInterface(self):
        self.geometry("900x900")
        self.configure(bg="black")
        self.title("Demineur en cooperation")
        self.resizable(width=FALSE, height=FALSE)
        self.MainInterface()
    def MainInterface(self):
        self.interface=Canvas(self,width=900,height=900,bg='grey',bd=0)
        self.font=Font(family="Helvetica",size=14)
        self.interface.pack()
        solo=Button(self.interface, text="jouer en solo",bg='#999999',width=50,height=4, font=self.font)
        solo.place(x=170,y=350)
        multi=Button(self.interface, text="jouer en multi-joueurs",bg='#999999',width=50,height=4, font=self.font)
        multi.place(x=170,y=500)
        quitter=Button(self.interface, text="quitter",bg='#999999',width=4,height=2, font=self.font)
        quitter.place(x=850,y=850)

class Main(MenuPrincipal):
    def __init__(self):
        MenuPrincipal.__init__(self)


        

main=Main()
