from server import Main as StartServer
from tkinter.font import Font
from random import randint
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
            self.SendMessage("message;dev_message*Client connecte", self.server)
        except RuntimeError as e:
            print(e)
        except ConnectionRefusedError as e:
            print(e)
            return False
        return True
    def GetMessages(self, function):
        try:
            while self.clientOn:
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
    def Deserializer(self, message):
        dico={}
        dico["message_type"] = message.split(";")[0]
        dico2={}
        dico2["name"] = message.split(";")[1].split("*")[0]
        dico2["args"] = message.split(";")[1].split("*")
        del dico2["args"][0]
        dico["message_body"] = dico2
        return dico
    def StartEventHandler(self):
        self.GetMessages(self.GetEvent)
    def GetEvent(self, evt):
        if evt.message=="":
            self.server.close()
        else:
            message = self.Deserializer(evt.message)
            if message["message_type"]=="instruct":
                if message["message_body"]["name"] == "client_account_changed":
                    print(message["message_body"]["args"][0])
                    self.clientCount.set("Clients connectes: {}".format(int(message["message_body"]["args"][0])))
        print(evt.message)

class Game():
    def __init__(self):
        pass
    def StartGame(self):
        self.geometry("800x800+10+10")
        self.configure(bg="black")
        self.title("Demineur en cooperation")
        self.resizable(width=FALSE, height=FALSE)
        self.CreateMatrice()
    def CreateMatrice(self):
        self.mat=[]
        for i in range(self.nbrDeCaselongueur.get()):
            temp=[]
            for j in range(self.nbrDeCaseHauteur.get()):
                temp.append(0)
            self.mat.append(temp)
        self.PlaceBombe()
    def PlaceBombe(self):
        self.nombreDeBombeMalPlacer=0
        for k in range(self.nbrDeBombe.get()):
            r=randint(0, self.nbrDeCaselongueur.get()-1)
            s=randint(0, self.nbrDeCaseHauteur.get()-1)
            if self.mat[r][s]==1:
                self.nombreDeBombeMalPlacer=self.nombreDeBombeMalPlacer+1
            else:
                self.mat[r][s]=1
        if self.nombreDeBombeMalPlacer>0:
            self.nbrDeBombe.set(self.nombreDeBombeMalPlacer)
            self.PlaceBombe()
        else:
            print(self.mat)
            print(self.nbrDeBombe.get())

class MenuPrincipal(Tk, Game):
    def __init__(self):
        Tk.__init__(self)
        Game.__init__(self)
        self.InitInterface()
        self.mainloop()
    def StartHost(self):
        threading.Thread(target=self.__StartHost).start()
        self.StartJoin()
    def __StartHost(self):
        self.localServer=Server()
        print(self.localServer)
        self.localServer.Start()
    def __StartGame(self):
        self.localServer.send()
    def __StopServer(self):
        self.localServer.CloseServer()
    def StartJoin(self):
        threading.Thread(target=self.__StartJoin).start()
    def __StartJoin(self):
        self.loadingText.set("Connection au client en cours...")
        status = self._Network__StartClient()
        threading.Thread(target=self.StartEventHandler()).start()
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
        self.MultiPlayerChoice()
    def MultiPlayerChoice(self):
        self.ResetInterface()
        self.interface=Canvas(self,width=900,height=900,bg='grey',bd=0)
        self.font=Font(family="Helvetica",size=14)
        self.font_bts_quitter=Font(family="Helvetica",size=10)
        self.font2=Font(family="Helvetica",size=8)
        self.interface.pack()
        retour=Button(self.interface, text="Quitter",bg='#999999',width=4,height=2, font=self.font2, command=self.destroy)
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
        play=Button(self.interface, text="Commencer a jouer",bg='#999999',width=50,height=4, font=self.font, command=self.WaitClientMenu)
        play.place(x=120,y=680)
        retour=Button(self.interface, text="retour",bg='#999999',width=4,height=2, font=self.font2, command=self.destroy)
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
        retour=Button(self.interface, text="retour",bg='#999999',width=4,height=2, font=self.font2, command=self.MultiPlayerChoice)
        retour.place(x=750,y=750)
        creeUnePartie=Button(self.interface, text="Reesayer",bg='#999999',width=50,height=4, font=self.font, command=self.LoadingMenuInterface)
        creeUnePartie.place(x=120,y=550)
        loadingTextLabel=Label(self.interface,font=self.font,text="La connection a echoue", bg="grey")
        loadingTextLabel.place(x=280,y=400)
    def WaitClientMenu(self):
        self.ResetInterface()
        self.interface=Canvas(self,width=900,height=900,bg='grey',bd=0)
        self.font=Font(family="Helvetica",size=14)
        self.font_bts_quitter=Font(family="Helvetica",size=10)
        self.font2=Font(family="Helvetica",size=8)
        self.interface.pack()
        self.clientCount=StringVar()
        self.clientCount.set("Clients connectes: 0")
        self.loadingText=StringVar()
        Label(self, textvariable=self.clientCount, font=self.font,bg="#999999").place(x=280, y=300)
        retour=Button(self.interface, text="retour",bg='#999999',width=4,height=2, font=self.font2, command=self.ReturnToMainMenu)
        retour.place(x=750,y=750)
        creeUnePartie=Button(self.interface, text="Commencer la partie",bg='#999999',width=50,height=4, font=self.font, command=self.LoadingMenuInterface)
        creeUnePartie.place(x=120,y=550)
        loadingTextLabel=Label(self.interface,font=self.font,text="En attente de la connection de clients", bg="grey")
        loadingTextLabel.place(x=280,y=400)
        self.StartHost()
    def ReturnToMainMenu(self):
        self.__StopServer()
        self.MultiPlayerChoice()



class Main(MenuPrincipal, Network):
    def __init__(self):
        MenuPrincipal.__init__(self)




if __name__=="__main__":
    main=Main()
