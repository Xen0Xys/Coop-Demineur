from tkinter import *
from tkinter.font import Font
from time import sleep
import socket
import select
import threading

class ClientMessage():
    def __init__(self, message, server):
        self.message=message
        self.server=server

class Network():
    def __init__(self):
        pass
    def StartClient(self):
        threading.Thread(target=self.__StartClient).start()
    def __StartClient(self):
        try:
            self.clientOn=True
            self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server.connect(("localhost", 1001))
            self.SendMessage("Client connect", self.server)
        except RuntimeError as e:
            print(e)
        except ConnectionRefusedError as e:
            print(e)
    def GetMessages(self, function):
        try:
            while self.clientOn:
                if len(self.ClientList)>0:
                    rlist, wlist, xlist = select.select([self.server], [], [], 0.05)
                    for server in rlist:
                        message = server.recv(1024).decode()
                        evt = ClientMessage(message, server)
                        function(evt)
        except RuntimeError as e:
            print(e)
    def SendMessage(self, message, server):
        threading.Thread(target=self.__SendMessage, args=(message, server,)).start()
    def __SendMessage(self, message, server):
        server.send(message.encode())

class EventHandler():
    def __init__(self):
        pass
    def StartEventHandler(self):
        self.GetMessages(self.GetEvent)
    def GetEvent(self, evt):
        print(evt.message)

        
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


        

if __name__=="__main__":
    main=Main()
