from server import Main as Server
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
    def StopClient(self):
        self.clientOn=False
    def __StartClient(self):
        try:
            self.clientOn=True
            self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server.connect(("localhost", 1001))
            self.SendMessage("message;dev_message*Client connecte")
        except RuntimeError as e:
            print(e)
        except ConnectionRefusedError as e:
            print(e)
            return False
        return True
    def GetMessages(self, function):
        try:
            while self.clientOn:
                try:
                    rlist, wlist, xlist = select.select([self.server], [], [], 0.05)
                    for server in rlist:
                        message = server.recv(2048).decode()
                        evt = ClientMessage(message, server)
                        function(evt)
                except OSError as e:
                    print(e)
                except ValueError as e:
                    print(e)
        except RuntimeError as e:
            print(e)
    def SendMessage(self, message):
        threading.Thread(target=self.__SendMessage, args=(message,)).start()
    def __SendMessage(self, message):
        self.server.send(message.encode())

class EventHandler():
    def __init__(self):
        pass
    def DeserializeMatrice(self, args):
        height=int(args[0])
        self.nbrDeCaseHauteur=IntVar()
        self.nbrDeCaseHauteur.set(height)
        del args[0]
        width=int(args[0])
        self.nbrDeCaselongueur=IntVar()
        self.nbrDeCaselongueur.set(width)
        del args[0]
        Matrice=[]
        for i in range(width):
            temp=[]
            for j in range(height):
                temp.append(int(args[i*height+j]))
            Matrice.append(temp)
        return Matrice
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
        print(evt.message)
        if evt.message=="":
            self.server.close()
        else:
            message = self.Deserializer(evt.message)
            if message["message_type"]=="instruct":
                if message["message_body"]["name"] == "client_account_changed":
                    print(message["message_body"]["args"][0])
                    self.clientCount.set("Clients connectes: {}".format(int(message["message_body"]["args"][0])))
                elif message["message_body"]["name"] == "start":
                    self.mat=self.DeserializeMatrice(message["message_body"]["args"])
                    self.StartGame()

class Game():
    def __init__(self):
        pass
    def StartGame(self):
        self.ResetInterface()
        self.interface=Canvas(self,width=900,height=900,bg='grey',bd=0)
        self.interface.pack()
        self.GameWin()
    def GameWin(self):
        self.bind("<Button-1>",self.OnLeftClick)
        self.bind("<Button-2>",self.OnRightClick)
        self.image_case_pleine = PhotoImage(file ='ressources/case_pleine.PNG')
        self.image_case_vide = PhotoImage(file ='ressources/case_vide.PNG')
        self.image_case_1 = PhotoImage(file ='ressources/case_1.PNG')
        self.image_case_2 = PhotoImage(file ='ressources/case_2.PNG')
        self.image_case_3 = PhotoImage(file ='ressources/case_3.PNG')
        self.image_case_4 = PhotoImage(file ='ressources/case_4.PNG')
        self.image_case_5 = PhotoImage(file ='ressources/case_5.PNG')
        self.image_case_6 = PhotoImage(file ='ressources/case_6.PNG')
        self.image_case_7 = PhotoImage(file ='ressources/case_7.PNG')
        self.image_case_8 = PhotoImage(file ='ressources/case_8.PNG')
        self.image_drapeau = PhotoImage(file ='ressources/drapeau.PNG')
        self.image_explosion = PhotoImage(file ='ressources/explosion.PNG')
        self.image_mine = PhotoImage(file ='ressources/mine.PNG')
        self.image_point_interro = PhotoImage(file ='ressources/point_interro.PNG')
        for i in range(self.nbrDeCaseHauteur.get()):
            for j in range(self.nbrDeCaselongueur.get()):
                self.interface.create_image(j*25,i*25, image=self.image_case_pleine, anchor=NW)
    def OnRightClick(self):
        pass
    def OnLeftClick(self,event):
        self.coordX=event.x//25
        self.coordY=event.y//25
        if 0<= (self.coordX)<=self.nbrDeCaselongueur.get()-1 and 0<= (self.coordY)<=self.nbrDeCaseHauteur.get()-1:
            if self.mat[self.coordX][self.coordY]==2:
                self.interface.create_image((self.coordX)*25,(self.coordY)*25, image=self.image_explosion, anchor=NW)
            if self.mat[self.coordX][self.coordY]==0:
                pass
            if self.mat[self.coordX][self.coordY]==1:
                self.CalculBombeACote()
    def CalculBombeACote(self):
        self.nbrDeBombeACoter=0
        self.mat[self.coordX][self.coordY]=0
        a=1
        for i in range(3):
            b=1
            for j in range(3):
                try:
                    if self.mat[self.coordX+a][self.coordY+b]==2 and self.nbrDeCaselongueur.get()-1>=self.coordX+a>=0 and self.nbrDeCaseHauteur.get()-1>=self.coordY+b>=0:
                        self.nbrDeBombeACoter=self.nbrDeBombeACoter+1
                except IndexError:
                    pass
                b=b-1
            a=a-1
        print(self.nbrDeBombeACoter)
        if self.nbrDeBombeACoter==0:
            #on change la case pleine en case vide
            self.interface.create_image(self.coordX*25,self.coordY*25, image=self.image_case_vide, anchor=NW)
            self.coordX=self.coordX+1
            self.CalculBombeACote()
        elif self.nbrDeBombeACoter==1:
            self.interface.create_image(self.coordX*25,self.coordY*25, image=self.image_case_1, anchor=NW)
        elif self.nbrDeBombeACoter==2:
            self.interface.create_image(self.coordX*25,self.coordY*25, image=self.image_case_2, anchor=NW)
        elif self.nbrDeBombeACoter==3:
            self.interface.create_image(self.coordX*25,self.coordY*25, image=self.image_case_3, anchor=NW)
        elif self.nbrDeBombeACoter==4:
            self.interface.create_image(self.coordX*25,self.coordY*25, image=self.image_case_4, anchor=NW)
        elif self.nbrDeBombeACoter==5:
            self.interface.create_image(self.coordX*25,self.coordY*25, image=self.image_case_5, anchor=NW)
        elif self.nbrDeBombeACoter==6:
            self.interface.create_image(self.coordX*25,self.coordY*25, image=self.image_case_6, anchor=NW)
        elif self.nbrDeBombeACoter==7:
            self.interface.create_image(self.coordX*25,self.coordY*25, image=self.image_case_7, anchor=NW)
        elif self.nbrDeBombeACoter==8:
            self.interface.create_image(self.coordX*25,self.coordY*25, image=self.image_case_8, anchor=NW)
        else:
            pass



class MenuPrincipal(Tk, Game):
    def __init__(self):
        Tk.__init__(self)
        Game.__init__(self)
        self.InitInterface()
        self.protocol("WM_DELETE_WINDOW", self.onWindowClosed)
        self.mainloop()
    def onWindowClosed(self):
        self.StopClient()
        try:
            self.localServer.CloseServer()
        except AttributeError:
            pass
        self.destroy()
    def StartHost(self):
        threading.Thread(target=self.__StartHost).start()
        self.StartJoin()
    def __StartHost(self):
        self.localServer=Server()
        self.localServer.Start()
    def __StartGame(self):
        self.SendMessage("instruct;start*{}*{}*{}".format(self.nbrDeCaseHauteur.get(), self.nbrDeCaselongueur.get(), self.nbrDeBombe.get()))
    def __StopServer(self):
        self.localServer.CloseServer()
    def StartJoin(self):
        threading.Thread(target=self.__StartJoin).start()
    def __StartJoin(self):
        self.loadingText.set("Connection au client en cours...")
        status = self._Network__StartClient()
        threading.Thread(target=self.StartEventHandler).start()
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
        creeUnePartie=Button(self.interface, text="Commencer la partie",bg='#999999',width=50,height=4, font=self.font, command=self.__StartGame)
        creeUnePartie.place(x=120,y=550)
        loadingTextLabel=Label(self.interface,font=self.font,text="En attente de la connection de clients", bg="grey")
        loadingTextLabel.place(x=280,y=400)
        self.StartHost()
    def ReturnToMainMenu(self):
        self.__StopServer()
        self.StopClient()
        self.MultiPlayerChoice()




class Main(MenuPrincipal, Network, EventHandler):
    def __init__(self):
        MenuPrincipal.__init__(self)




if __name__=="__main__":
    main=Main()

