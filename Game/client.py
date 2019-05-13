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
    def StartHost(self):
        threading.Thread(target=self.__StartHost).start()
    def __StartHost(self):
        pass
    def StartJoin(self):
        threading.Thread(target=self.__StartJoin).start()
    def __StartJoin(self):
        pass
    def ResetInterface(self):
        for item in self.winfo_children():
            item.destroy()
    def InitInterface(self):
        self.geometry("800x800")
        self.configure(bg="black")
        self.title("Demineur en cooperation")
        self.resizable(width=FALSE, height=FALSE)
        self.MainInterface()
    def MainInterface(self):
        self.interface=Canvas(self,width=900,height=900,bg='grey',bd=0)
        self.font=Font(family="Helvetica",size=14)
        self.font_bts_quitter=Font(family="Helvetica",size=10)
        self.font2=Font(family="Helvetica",size=8)
        self.interface.pack()
        solo=Button(self.interface, text="Jouer en solo",bg='#999999',width=50,height=4, font=self.font, command=self.SoloInterface)
        solo.place(x=130,y=250)
        multi=Button(self.interface, text="Jouer en multi-joueurs",bg='#999999',width=50,height=4, font=self.font, command=self.MultiInterface)
        multi.place(x=130,y=400)
        quitter=Button(self.interface, text="Quitter",bg='#999999',width=4,height=2, font=self.font_bts_quitter, command=self.destroy)
        quitter.place(x=750,y=750)
        nomLabel=Label(self.interface,font=self.font,text="Demineur en cooperation", bg="grey")
        nomLabel.place(x=310,y=20)
        createurLabel=Label(self.interface,font=self.font2,text="Jeu cree par Czekaj Tom et Duchene Guillaume", bg="grey")
        createurLabel.place(x=10,y=760)
    def SoloInterface(self):
        self.ResetInterface()
        self.interface=Canvas(self,width=900,height=900,bg='grey',bd=0)
        self.font=Font(family="Helvetica",size=14)
        self.font_bts_quitter=Font(family="Helvetica",size=10)
        self.font2=Font(family="Helvetica",size=8)
        self.interface.pack()
        self.nbrDeCaseParCoter= IntVar()
        self.nbrDeCaseParCoter.set(10)
        self.nbrDeBombe= IntVar()
        self.nbrDeBombe.set(10)
        quitter=Button(self.interface, text="Quitter",bg='#999999',width=4,height=2, font=self.font_bts_quitter, command=self.destroy)
        quitter.place(x=750,y=750)
        nomLabel=Label(self.interface,font=self.font,text="Demineur en cooperation", bg="grey")
        nomLabel.place(x=310,y=20)
        nbrDeCaseParCoterLabel=Label(self.interface,font=self.font,text="Nombre de case par coter:", bg="grey")
        nbrDeCaseParCoterLabel.place(x=20,y=170)
        nbrDeCaseParCoterScale=Scale(self.interface, orient='horizontal', from_=10, to=25,resolution=1, tickinterval=5, length=350,bg="grey",highlightthickness=0, variable=self.nbrDeCaseParCoter )
        nbrDeCaseParCoterScale.place(x=300,y=160)
        nbrDeBombeLabel=Label(self.interface,font=self.font,text="Nombre de case par coter:", bg="grey")
        nbrDeBombeLabel.place(x=20,y=270)
        nbrDeBombeScale=Scale(self.interface, orient='horizontal', from_=10, to=99,resolution=1, tickinterval=10, length=350,bg="grey",highlightthickness=0, variable=self.nbrDeBombe)
        nbrDeBombeScale.place(x=300,y=260)
        play=Button(self.interface, text="Commencer a jouer",bg='#999999',width=50,height=4, font=self.font)
        play.place(x=120,y=680)
    def MultiInterface(self):
        self.ResetInterface()
        self.interface=Canvas(self,width=900,height=900,bg='grey',bd=0)
        self.font=Font(family="Helvetica",size=14)
        self.font_bts_quitter=Font(family="Helvetica",size=10)
        self.font2=Font(family="Helvetica",size=8)
        self.interface.pack()
        self.nbrDeCaseParCoter= IntVar()
        self.nbrDeCaseParCoter.set(10)
        self.nbrDeBombe= IntVar()
        self.nbrDeBombe.set(10)
        quitter=Button(self.interface, text="Quitter",bg='#999999',width=4,height=2, font=self.font_bts_quitter, command=self.destroy)
        quitter.place(x=750,y=750)
        nomLabel=Label(self.interface,font=self.font,text="Demineur en cooperation", bg="grey")
        nomLabel.place(x=310,y=20)
        nbrDeCaseParCoterLabel=Label(self.interface,font=self.font,text="Nombre de case par coter:", bg="grey")
        nbrDeCaseParCoterLabel.place(x=20,y=170)
        nbrDeCaseParCoterScale=Scale(self.interface, orient='horizontal', from_=10, to=25,resolution=1, tickinterval=5, length=350,bg="grey",highlightthickness=0, variable=self.nbrDeCaseParCoter )
        nbrDeCaseParCoterScale.place(x=300,y=160)
        nbrDeBombeLabel=Label(self.interface,font=self.font,text="Nombre de case par coter:", bg="grey")
        nbrDeBombeLabel.place(x=20,y=270)
        nbrDeBombeScale=Scale(self.interface, orient='horizontal', from_=10, to=99,resolution=1, tickinterval=10, length=350,bg="grey",highlightthickness=0, variable=self.nbrDeBombe)
        nbrDeBombeScale.place(x=300,y=260)
        play=Button(self.interface, text="Commencer a jouer",bg='#999999',width=50,height=4, font=self.font)
        play.place(x=120,y=680)


class Main(MenuPrincipal):
    def __init__(self):
        MenuPrincipal.__init__(self)


        

if __name__=="__main__":
    main=Main()
