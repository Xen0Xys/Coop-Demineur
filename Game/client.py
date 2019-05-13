from server import Main as StartServer
from tkinter.font import Font
from tkinter import *
from time import sleep
import threading
import socket
import select

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
            return False
        return True
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

class Game():
    def __init__(self):
        pass
    def StartGame(self):
        self.geometry("800x800+10+10")
        self.configure(bg="black")
        self.title("Demineur en cooperation")
        self.resizable(width=FALSE, height=FALSE)
        self.mat=[]
        for i in range(self.nbrDeCaselongueur.get()):
            temp=[]
            for j in range(self.nbrDeCaseHauteur.get()):
                temp.append(0)
            self.mat.append(temp)
        print(self.mat)
        for k in range(self.nbrDeBombe.get()):
            r=randint(0, self.nbrDeCaselongueur.get())
            s=randint(0, self.nbrDeCaseHauteur.get())
            if self.mat[r][s]==1:
                self.nbrDeBombe.set(self.nbrDeBombe+1)
            self.mat[r][s]=1

class MenuPrincipal(Tk, Game):
    def __init__(self):
        Tk.__init__(self)
        Game.__init__(self)
        self.InitInterface()
        self.mainloop()
    def StartHost(self):
        threading.Thread(target=self.__StartHost).start()
    def __StartHost(self):
        pass
    def StartJoin(self):
        threading.Thread(target=self.__StartJoin).start()
    def __StartJoin(self):
        self.loadingText.set("Connection au client en cours...")
        status = self._Network__StartClient()
        if status==True:
            self.loadingText.set("Connecte au client, en attente du lancement...")
        else:
            self.FailedJoinMenu()
    def ResetInterface(self):
        for item in self.winfo_children():
            item.destroy()
    def InitInterface(self):
        self.geometry("800x800+10+10")
        self.configure(bg="black")
        self.title("Demineur en cooperation")
        self.resizable(width=FALSE, height=FALSE)
        self.MainInterface()
    def MainInterface(self):
        self.ResetInterface()
        self.interface=Canvas(self,width=900,height=900,bg='grey',bd=0)
        self.font=Font(family="Helvetica",size=14)
        self.font_bts_quitter=Font(family="Helvetica",size=10)
        self.font2=Font(family="Helvetica",size=8)
        self.interface.pack()
        solo=Button(self.interface, text="Jouer en solo",bg='#999999',width=50,height=4, font=self.font, command=self.SoloInterface)
        solo.place(x=130,y=250)
        multi=Button(self.interface, text="Jouer en multi-joueurs",bg='#999999',width=50,height=4, font=self.font, command=self.MultiPlayerChoice)
        multi.place(x=130,y=400)
        quitter=Button(self.interface, text="Quitter",bg='#999999',width=4,height=2, font=self.font_bts_quitter, command=self.destroy)
        quitter.place(x=750,y=750)
        nomLabel=Label(self.interface,font=self.font,text="Demineur en cooperation", bg="grey")
        nomLabel.place(x=310,y=20)
        createurLabel=Label(self.interface,font=self.font2,text="Jeu cree par Czekaj Tom et Duchene Guillaume", bg="grey")
        createurLabel.place(x=10,y=760)
    def SoloInterface(self):
        def SoloInterface(self):
        self.ResetInterface()
        self.interface=Canvas(self,width=900,height=900,bg='grey',bd=0)
        self.font=Font(family="Helvetica",size=14)
        self.font_bts_quitter=Font(family="Helvetica",size=10)
        self.font2=Font(family="Helvetica",size=8)
        self.interface.pack()
        self.nbrDeCaseHauteur= IntVar()
        self.nbrDeCaseHauteur.set(10)
        self.nbrDeCaselongueur= IntVar()
        self.nbrDeCaselongueur.set(10)
        self.nbrDeBombe= IntVar()
        self.nbrDeBombe.set(10)
        nomLabel=Label(self.interface,font=self.font,text="Demineur en cooperation", bg="grey")
        nomLabel.place(x=310,y=20)
        nbrDeCaseHauteurLabel=Label(self.interface,font=self.font,text="Nombre de case en hauteur:", bg="grey")
        nbrDeCaseHauteurLabel.place(x=20,y=170)
        nbrDeCaseHauteurScale=Scale(self.interface, orient='horizontal', from_=10, to=25,resolution=1, tickinterval=5, length=350,bg="grey",highlightthickness=0, variable=self.nbrDeCaseHauteur )
        nbrDeCaseHauteurScale.place(x=300,y=160)
        nbrDeBombeLabel=Label(self.interface,font=self.font,text="Nombre de bombes:", bg="grey")
        nbrDeBombeLabel.place(x=20,y=370)
        nbrDeBombeScale=Scale(self.interface, orient='horizontal', from_=10, to=99,resolution=1, tickinterval=10, length=350,bg="grey",highlightthickness=0, variable=self.nbrDeBombe)
        nbrDeBombeScale.place(x=300,y=360)
        nbrDeCaseLongueurLabel=Label(self.interface,font=self.font,text="Nombre de case en longueur:", bg="grey")
        nbrDeCaseLongueurLabel.place(x=20,y=270)
        nbrDeCaseLongueurScale=Scale(self.interface, orient='horizontal', from_=10, to=25,resolution=1, tickinterval=5, length=350,bg="grey",highlightthickness=0, variable=self.nbrDeCaselongueur )
        nbrDeCaseLongueurScale.place(x=300,y=260)
        play=Button(self.interface, text="Commencer a jouer",bg='#999999',width=50,height=4, font=self.font, command= self.StartGame)#, command=self.LoadingMenuInterface
        play.place(x=120,y=680)
        retour=Button(self.interface, text="retour",bg='#999999',width=4,height=2, font=self.font2, command=self.MainInterface)
        retour.place(x=750,y=750)
    def MultiPlayerChoice(self):
        self.ResetInterface()
        self.interface=Canvas(self,width=900,height=900,bg='grey',bd=0)
        self.font=Font(family="Helvetica",size=14)
        self.font_bts_quitter=Font(family="Helvetica",size=10)
        self.font2=Font(family="Helvetica",size=8)
        self.interface.pack()
        retour=Button(self.interface, text="retour",bg='#999999',width=4,height=2, font=self.font2, command=self.MainInterface)
        retour.place(x=750,y=750)
        creeUnePartie=Button(self.interface, text="Cree une partie",bg='#999999',width=50,height=4, font=self.font, command=self.MultiInterface)
        creeUnePartie.place(x=120,y=250)
        rejoindreUnePartie=Button(self.interface, text="Rejondre une partie",bg='#999999',width=50,height=4, font=self.font, command=self.LoadingMenuInterface)
        rejoindreUnePartie.place(x=120,y=400)
        nomLabel=Label(self.interface,font=self.font,text="Demineur en cooperation", bg="grey")
        nomLabel.place(x=310,y=20)
    def MultiInterface(self):
        self.ResetInterface()
        self.interface=Canvas(self,width=900,height=900,bg='grey',bd=0)
        self.font=Font(family="Helvetica",size=14)
        self.font_bts_quitter=Font(family="Helvetica",size=10)
        self.font2=Font(family="Helvetica",size=8)
        self.interface.pack()
        self.nbrDeCaseHauteur= IntVar()
        self.nbrDeCaseHauteur.set(10)
        self.nbrDeCaselongueur= IntVar()
        self.nbrDeCaselongueur.set(10)
        self.nbrDeBombe= IntVar()
        self.nbrDeBombe.set(10)
        nomLabel=Label(self.interface,font=self.font,text="Demineur en cooperation", bg="grey")
        nomLabel.place(x=310,y=20)
        nbrDeCaseHauteurLabel=Label(self.interface,font=self.font,text="Nombre de case en hauteur:", bg="grey")
        nbrDeCaseHauteurLabel.place(x=20,y=170)
        nbrDeCaseHauteurScale=Scale(self.interface, orient='horizontal', from_=10, to=25,resolution=1, tickinterval=5, length=350,bg="grey",highlightthickness=0, variable=self.nbrDeCaseHauteur )
        nbrDeCaseHauteurScale.place(x=300,y=160)
        nbrDeBombeLabel=Label(self.interface,font=self.font,text="Nombre de bombes:", bg="grey")
        nbrDeBombeLabel.place(x=20,y=370)
        nbrDeBombeScale=Scale(self.interface, orient='horizontal', from_=10, to=99,resolution=1, tickinterval=10, length=350,bg="grey",highlightthickness=0, variable=self.nbrDeBombe)
        nbrDeBombeScale.place(x=300,y=360)
        nbrDeCaseLongueurLabel=Label(self.interface,font=self.font,text="Nombre de case en longueur:", bg="grey")
        nbrDeCaseLongueurLabel.place(x=20,y=270)
        nbrDeCaseLongueurScale=Scale(self.interface, orient='horizontal', from_=10, to=25,resolution=1, tickinterval=5, length=350,bg="grey",highlightthickness=0, variable=self.nbrDeCaselongueur )
        nbrDeCaseLongueurScale.place(x=300,y=260)
        play=Button(self.interface, text="Commencer a jouer",bg='#999999',width=50,height=4, font=self.font, command=self.LoadingMenuInterface)
        play.place(x=120,y=680)
        retour=Button(self.interface, text="retour",bg='#999999',width=4,height=2, font=self.font2, command=self.MainInterface)
        retour.place(x=750,y=750)
    def LoadingMenuInterface(self, message=""):
        self.ResetInterface()
        self.interface=Canvas(self,width=900,height=900,bg='grey',bd=0)
        self.font=Font(family="Helvetica",size=14)
        self.font_bts_quitter=Font(family="Helvetica",size=10)
        self.font2=Font(family="Helvetica",size=8)
        self.interface.pack()
        self.loadingText= StringVar()
        self.loadingText.set(message)
        loadingTextLabel=Label(self.interface,font=self.font,textvariable=self.loadingText, bg="grey")
        loadingTextLabel.place(x=280,y=400)
        self.StartJoin()
    def FailedJoinMenu(self):
        self.ResetInterface()
        self.interface=Canvas(self,width=900,height=900,bg='grey',bd=0)
        self.font=Font(family="Helvetica",size=14)
        self.font_bts_quitter=Font(family="Helvetica",size=10)
        self.font2=Font(family="Helvetica",size=8)
        self.interface.pack()
        retour=Button(self.interface, text="retour",bg='#999999',width=4,height=2, font=self.font2, command=self.MainInterface)
        retour.place(x=750,y=750)
        creeUnePartie=Button(self.interface, text="Reesayer",bg='#999999',width=50,height=4, font=self.font, command=self.LoadingMenuInterface)
        creeUnePartie.place(x=120,y=550)
        loadingTextLabel=Label(self.interface,font=self.font,text="La connection a echoue", bg="grey")
        loadingTextLabel.place(x=280,y=400)



class Main(MenuPrincipal, Network):
    def __init__(self):
        MenuPrincipal.__init__(self)




if __name__=="__main__":
    main=Main()
