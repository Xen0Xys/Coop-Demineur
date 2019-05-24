from server import Main as Server
from tkinter.font import Font
from random import randint
from tkinter import *
from time import sleep
import threading
import socket
import select

class EventObject():
    def __init__(self, x, y):
        self.x=x
        self.y=y

class ClientMessage():
    def __init__(self, message, server):
        self.message=message
        self.server=server

class Network():
    def __init__(self):
        pass
    def StartClient(self, ip):
        threading.Thread(target=self.__StartClient, args=(ip, )).start()
    def StopClient(self):
        self.clientOn=False
    def __StartClient(self, ip):
        try:
            self.clientOn=True
            self.onSync=False
            self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server.connect((ip, 1001))
            self.SendMessage("message;dev_message*Client connecte")
        except RuntimeError as e:
            #print(e)
            pass
        except ConnectionRefusedError as e:
            #print(e)
            return False
        except OSError as e:
            #print(e)
            return False
        return True
    def GetMessages(self, function):
        try:
            while self.clientOn:
                try:
                    rlist, wlist, xlist = select.select([self.server], [], [], 0.001)
                    for server in rlist:
                        message = server.recv(4096).decode()
                        evt = ClientMessage(message, server)
                        function(evt)
                except OSError as e:
                    #print(e)
                    pass
                except ValueError as e:
                    #print(e)
                    self.StopClient()
                    self.FailedJoinMenu()
        except RuntimeError as e:
            #print(e)
            pass
    def SendMessage(self, message):
        #threading.Thread(target=self.__SendMessage, args=(message,)).start()
        self.__SendMessage(message + "/")
    def __SendMessage(self, message):
        try:
            self.server.send(message.encode())
        except OSError as e:
            #print(e)
            pass

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
        try:
            reste=message.split("/")[1]
            message=message.split("/")[0]
            if reste!="":
                evt = ClientMessage(reste + "/", self.server)
                self.GetEvent(evt)
        except IndexError as e:
            #print(e)
            pass
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
        """Recepton des messages"""
        #print(evt.message)
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
                    if self.onSync==True:
                        self.SendMessage("instruct;sync*received")
                    self.StartGame()
                elif message["message_body"]["name"] == "left_click":
                    x = int(message["message_body"]["args"][0])
                    y = int(message["message_body"]["args"][1])
                    event=EventObject(x, y)
                    if self.onSync==True:
                        self.SendMessage("instruct;sync*received")
                    self.OnLeftClick(event)
                elif message["message_body"]["name"] == "right_click":
                    x = int(message["message_body"]["args"][0])
                    y = int(message["message_body"]["args"][1])
                    event=EventObject(x, y)
                    if self.onSync==True:
                        self.SendMessage("instruct;sync*received")
                    self.OnRightClick(event)
                elif message["message_body"]["name"] == "change_mode":
                    if message["message_body"]["args"][0]=="enable":
                        self.onSync=True
                    elif message["message_body"]["args"][0]=="disable":
                        self.onSync=False
                    if self.onSync==True:
                        print("Sending")
                        self.SendMessage("instruct;sync*received")
            elif message["message_type"]=="game_info":
                if message["message_body"]["name"] == "time":
                    time = message["message_body"]["args"][0]
                    ##self.Function(time)
                    pass

class Game():
    def __init__(self):
        pass
    def StartGame(self):
        self.ResetInterface()
        self.clickAuto=True
        self.geometry("1000x800")
        self.configure(bg="black")
        self.interface=Canvas(self,width=1000,height=800,bg='grey',bd=0)
        self.interface.pack()
        self.nombreDeDrapeau=self.nbrDeBombe.get()
        self.GameWin()
        self.WinCoteGrille()
    def GameWin(self):
        self.bind("<Button-1>",self.OnLeftClickServer)
        self.bind("<Button-3>",self.OnRightClickServer)
        self.matClickDroit=[]
        for i in range(self.nbrDeCaselongueur.get()):
            temp=[]
            for j in range(self.nbrDeCaseHauteur.get()):
                temp.append(0)
            self.matClickDroit.append(temp)
        self.image_case_pleine = PhotoImage(file ='ressources/case_pleine.png')
        self.image_case_vide = PhotoImage(file ='ressources/case_vide.png')
        self.image_case_1 = PhotoImage(file ='ressources/case_1.png')
        self.image_case_2 = PhotoImage(file ='ressources/case_2.png')
        self.image_case_3 = PhotoImage(file ='ressources/case_3.png')
        self.image_case_4 = PhotoImage(file ='ressources/case_4.png')
        self.image_case_5 = PhotoImage(file ='ressources/case_5.png')
        self.image_case_6 = PhotoImage(file ='ressources/case_6.png')
        self.image_case_7 = PhotoImage(file ='ressources/case_7.png')
        self.image_case_8 = PhotoImage(file ='ressources/case_8.png')
        self.image_drapeau = PhotoImage(file ='ressources/drapeau.png')
        self.image_explosion = PhotoImage(file ='ressources/explosion.png')
        self.image_mine = PhotoImage(file ='ressources/mine.png')
        self.image_point_interro = PhotoImage(file ='ressources/point_interro.png')
        for i in range(self.nbrDeCaseHauteur.get()):
            for j in range(self.nbrDeCaselongueur.get()):
                self.interface.create_image(j*25,i*25, image=self.image_case_pleine, anchor=NW)
    def OnLeftClickServer(self, evt):
        self.SendMessage("instruct;left_click*{}*{}".format(evt.x, evt.y))
    def OnRightClickServer(self, evt):
        self.SendMessage("instruct;right_click*{}*{}".format(evt.x, evt.y))
    def OnRightClick(self, event):
        if self.clickAuto==True:
            self.coordX=event.x//25
            self.coordY=event.y//25
            if 0<= (self.coordX)<=self.nbrDeCaselongueur.get()-1 and 0<= (self.coordY)<=self.nbrDeCaseHauteur.get()-1:
                if self.matClickDroit[self.coordX][self.coordY]==0 and self.mat[self.coordX][self.coordY] not in [0, 3]:
                    self.matClickDroit[self.coordX][self.coordY]=1
                    self.interface.create_image(self.coordX*25,self.coordY*25, image=self.image_drapeau, anchor=NW)
                    self.nombreDeDrapeau=self.nombreDeDrapeau-1
                    self.ActualiseNbreDrapeauVar()
                elif self.matClickDroit[self.coordX][self.coordY]==1 and self.mat[self.coordX][self.coordY] not in [0, 3]:
                    self.matClickDroit[self.coordX][self.coordY]=2
                    self.interface.create_image(self.coordX*25,self.coordY*25, image=self.image_point_interro, anchor=NW)
                    self.nombreDeDrapeau=self.nombreDeDrapeau+1
                    self.ActualiseNbreDrapeauVar()
                elif self.matClickDroit[self.coordX][self.coordY]==2 and self.mat[self.coordX][self.coordY] not in [0, 3]:
                    self.matClickDroit[self.coordX][self.coordY]=0
                    self.interface.create_image(self.coordX*25,self.coordY*25, image=self.image_case_pleine, anchor=NW)
            print(self.matClickDroit)

    def OnLeftClick(self,event):
        if self.clickAuto==True:
            self.coordX=event.x//25
            self.coordY=event.y//25
            if 0<= (self.coordX)<=self.nbrDeCaselongueur.get()-1 and 0<= (self.coordY)<=self.nbrDeCaseHauteur.get()-1:
                if self.mat[self.coordX][self.coordY]==2 and self.matClickDroit[self.coordX][self.coordY]!=1:
                    self.interface.create_image((self.coordX)*25,(self.coordY)*25, image=self.image_explosion, anchor=NW)
                    self.clickAuto=False
                    self.mat[self.coordX][self.coordY]=3
                if self.mat[self.coordX][self.coordY]==0:
                    pass
                if self.mat[self.coordX][self.coordY]==1 and self.matClickDroit[self.coordX][self.coordY]!=1:
                    self.CalculBombeACote()
    def CalculBombeACote(self):
        self.nbrDeBombeACoter=0
        a=1
        for i in range(3):
            b=1
            for j in range(3):
                try:
                    if (self.mat[self.coordX+a][self.coordY+b]==2 or self.mat[self.coordX+a][self.coordY+b]==3) and self.nbrDeCaselongueur.get()-1>=self.coordX+a>=0 and self.nbrDeCaseHauteur.get()-1>=self.coordY+b>=0:
                        self.nbrDeBombeACoter=self.nbrDeBombeACoter+1
                except IndexError:
                    pass
                b=b-1
            a=a-1
        print(self.nbrDeBombeACoter)
        if self.nbrDeBombeACoter==0:
            self.interface.create_image(self.coordX*25,self.coordY*25, image=self.image_case_vide, anchor=NW)
            self.ActualisationCaseVide(self.coordX,self.coordY)
        elif self.nbrDeBombeACoter==1:
            self.interface.create_image(self.coordX*25,self.coordY*25, image=self.image_case_1, anchor=NW)
            self.mat[self.coordX][self.coordY]=0
        elif self.nbrDeBombeACoter==2:
            self.mat[self.coordX][self.coordY]=0
            self.interface.create_image(self.coordX*25,self.coordY*25, image=self.image_case_2, anchor=NW)
        elif self.nbrDeBombeACoter==3:
            self.mat[self.coordX][self.coordY]=0
            self.interface.create_image(self.coordX*25,self.coordY*25, image=self.image_case_3, anchor=NW)
        elif self.nbrDeBombeACoter==4:
            self.mat[self.coordX][self.coordY]=0
            self.interface.create_image(self.coordX*25,self.coordY*25, image=self.image_case_4, anchor=NW)
        elif self.nbrDeBombeACoter==5:
            self.mat[self.coordX][self.coordY]=0
            self.interface.create_image(self.coordX*25,self.coordY*25, image=self.image_case_5, anchor=NW)
        elif self.nbrDeBombeACoter==6:
            self.mat[self.coordX][self.coordY]=0
            self.interface.create_image(self.coordX*25,self.coordY*25, image=self.image_case_6, anchor=NW)
        elif self.nbrDeBombeACoter==7:
            self.mat[self.coordX][self.coordY]=0
            self.interface.create_image(self.coordX*25,self.coordY*25, image=self.image_case_7, anchor=NW)
        elif self.nbrDeBombeACoter==8:
            self.mat[self.coordX][self.coordY]=0
            self.interface.create_image(self.coordX*25,self.coordY*25, image=self.image_case_8, anchor=NW)
        else:
            pass
        self.CheckVictory()
    def ActualisationCaseVide(self,x,y):
        self.nbrDeBombeACoter=0
        a=1
        b=1
        try:
            if self.mat[x][y]==1:
                if self.nbrDeCaselongueur.get()>=x>=0 and self.nbrDeCaseHauteur.get()>=y>=0:
                    for i in range(3):
                        b=1
                        for j in range(3):
                            try:
                                if (self.mat[x+a][y+b]==2 or self.mat[x+a][y+b]==3) and self.nbrDeCaselongueur.get()>=x+a>=0 and self.nbrDeCaseHauteur.get()>=y+b>=0:
                                    self.nbrDeBombeACoter=self.nbrDeBombeACoter+1
                            except IndexError:
                                pass
                            b=b-1
                        a=a-1
                else:
                    self.nbrDeBombeACoter=9
            else:
                self.nbrDeBombeACoter=9
        except IndexError:
            self.nbrDeBombeACoter=9
        if self.nbrDeBombeACoter==0:
            self.mat[x][y]=0
            self.interface.create_image(x*25,y*25, image=self.image_case_vide, anchor=NW)
            self.ActualisationCaseVide(x+1,y)
            self.ActualisationCaseVide(x-1,y)
            self.ActualisationCaseVide(x,y-1)
            self.ActualisationCaseVide(x,y+1)
            self.ActualisationCaseVide(x+1,y+1)
            self.ActualisationCaseVide(x-1,y-1)
            self.ActualisationCaseVide(x-1,y+1)
            self.ActualisationCaseVide(x+1,y-1)
            self.CheckVictory()
        elif self.nbrDeBombeACoter==1:
            self.mat[x][y]=0
            self.interface.create_image(x*25,y*25, image=self.image_case_1, anchor=NW)
        elif self.nbrDeBombeACoter==2:
            self.mat[x][y]=0
            self.interface.create_image(x*25,y*25, image=self.image_case_2, anchor=NW)
        elif self.nbrDeBombeACoter==3:
            self.mat[x][y]=0
            self.interface.create_image(x*25,y*25, image=self.image_case_3, anchor=NW)
        elif self.nbrDeBombeACoter==4:
            self.mat[x][y]=0
            self.interface.create_image(x*25,y*25, image=self.image_case_4, anchor=NW)
        elif self.nbrDeBombeACoter==5:
            self.mat[x][y]=0
            self.interface.create_image(x*25,y*25, image=self.image_case_5, anchor=NW)
        elif self.nbrDeBombeACoter==6:
            self.mat[x][y]=0
            self.interface.create_image(x*25,y*25, image=self.image_case_6, anchor=NW)
        elif self.nbrDeBombeACoter==7:
            self.mat[x][y]=0
            self.interface.create_image(x*25,y*25, image=self.image_case_7, anchor=NW)
        elif self.nbrDeBombeACoter==8:
            self.mat[x][y]=0
            self.interface.create_image(x*25,y*25, image=self.image_case_8, anchor=NW)
        elif self.nbrDeBombeACoter==9:
            pass
        
    def WinCoteGrille(self):
        self.time=StringVar()
        self.time.set("0")
        timeLabel=Label(self.interface,font=self.font,text="temps:", bg="grey")
        timeLabel.place(x=820,y=170)
        timeNbrLabel=Label(self.interface,font=self.font,textvariable=self.time, bg="grey")
        timeNbrLabel.place(x=890,y=170)
        self.nbrDrapeau=StringVar()
        self.nbrDrapeau.set(str(self.nombreDeDrapeau))
        nbrdrapeauLabel=Label(self.interface,font=self.font,textvariable=self.nbrDrapeau, bg="grey")
        nbrdrapeauLabel.place(x=890,y=70)
        self.interface.create_image(860,70, image=self.image_drapeau, anchor=NW)
        recommencer=Button(self.interface, text="Recommencer",bg='#999999',width=15,height=2, font=self.font)
        recommencer.place(x=820,y=270)
        quitter=Button(self.interface, text="Quitter",bg='#999999',width=15,height=2, font=self.font)
        quitter.place(x=820,y=370)
    def ActualiseNbreDrapeauVar(self):
        self.nbrDrapeau.set(str(self.nombreDeDrapeau))

    def CheckVictory(self):
        self.nbrDeCaseNnDecouverte=0
        for i in range(self.nbrDeCaselongueur.get()):
            for j in range(self.nbrDeCaseHauteur.get()):
                if self.mat[i][j]==1:
                    self.nbrDeCaseNnDecouverte=self.nbrDeCaseNnDecouverte+1
        if self.nbrDeCaseNnDecouverte==0:
            self.clickAuto=False
            self.PlaceBombeAfterVictoryOrDefeat()

    """def PlaceBombeAfterVictoryOrDefeat():
        for i in range(self.nbrDeCaselongueur.get()):
            for j in range(self.nbrDeCaseHauteur.get()):
                if self.mat[i][j]==2:
                    self.interface.create_image(self.coordX*25,self.coordY*25, image=self.image_case_5, anchor=NW)"""




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
        if self.Ip.get()!="":
            threading.Thread(target=self.__StartHost).start()
            self.StartJoin()
        else:
            self.FailedJoinMenu()
    def __StartHost(self):
        self.localServer=Server()
        self.localServer.Start(self.Ip.get())
    def __StartGame(self):
        self.SendMessage("instruct;start*{}*{}*{}".format(self.nbrDeCaseHauteur.get(), self.nbrDeCaselongueur.get(), self.nbrDeBombe.get()))
    def __StopServer(self):
        self.localServer.CloseServer()
    def StartJoin(self):
        threading.Thread(target=self.__StartJoin).start()
    def __StartJoin(self):
        self.loadingText.set("Connection au client en cours...")
        try:
            status = self._Network__StartClient(self.Ip.get())
            if status==True:
                threading.Thread(target=self.StartEventHandler).start()
        except ValueError:
            status=False
        if status==True:
            self.loadingText.set("Connecte au client, en attente du lancement...")
        else:
            self.FailedJoinMenu()
    def ResetInterface(self):
        for item in self.winfo_children():
            try:
                item.destroy()
            except TclError as e:
                #print(e)
                pass
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
        rejoindreUnePartie=Button(self.interface, text="Rejondre une partie",bg='#999999',width=50,height=4, font=self.font, command=self.ChoiceIpHost)
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
        nbrDeCaseHauteurScale=Scale(self.interface, orient='horizontal', from_=10, to=32,resolution=1, tickinterval=5, length=350,bg="grey",highlightthickness=0, variable=self.nbrDeCaseHauteur, command=self.onHeightScaleChange)
        nbrDeCaseHauteurScale.place(x=300,y=160)
        nbrDeBombeLabel=Label(self.interface,font=self.font,text="Nombre de bombes:", bg="grey")
        nbrDeBombeLabel.place(x=20,y=370)
        self.nbrDeBombeScale=Scale(self.interface, orient='horizontal', from_=10, to=150,resolution=1, tickinterval=10, length=350,bg="grey",highlightthickness=0, variable=self.nbrDeBombe)
        self.nbrDeBombeScale.place(x=300,y=360)
        nbrDeCaseLongueurLabel=Label(self.interface,font=self.font,text="Nombre de case en longueur:", bg="grey")
        nbrDeCaseLongueurLabel.place(x=20,y=270)
        nbrDeCaseLongueurScale=Scale(self.interface, orient='horizontal', from_=10, to=32,resolution=1, tickinterval=5, length=350,bg="grey",highlightthickness=0, variable=self.nbrDeCaselongueur, command=self.onWidthScaleChange)
        nbrDeCaseLongueurScale.place(x=300,y=260)
        #
        self.Ip=StringVar()
        self.Ip.set("localhost")
        Label(self, text="Ip:", font=self.font, bg='grey').place(x=20, y=450)
        Entry(self, font=self.font, textvariable=self.Ip, bg="#999999").place(x=250, y=450)
        #
        play=Button(self.interface, text="Commencer a jouer",bg='#999999',width=50,height=4, font=self.font, command=self.WaitClientMenu)
        play.place(x=120,y=680)
        retour=Button(self.interface, text="Retour",bg='#999999',width=4,height=2, font=self.font2, command=self.MultiPlayerChoice)
        retour.place(x=750,y=750)
    def onHeightScaleChange(self, evt):
        self.nbrDeBombeScale["to"]=int(evt)*self.nbrDeCaselongueur.get()-1
        self.nbrDeBombeScale["tickinterval"]=int(int(evt)*self.nbrDeCaselongueur.get()/12)
    def onWidthScaleChange(self, evt):
        self.nbrDeBombeScale["to"]=int(evt)*self.nbrDeCaseHauteur.get()-1
        self.nbrDeBombeScale["tickinterval"]=int(int(evt)*self.nbrDeCaseHauteur.get()/12)
    def ChoiceIpHost(self):
        self.ResetInterface()
        self.interface=Canvas(self,width=900,height=900,bg='grey',bd=0)
        self.font=Font(family="Helvetica",size=14)
        self.font_bts_quitter=Font(family="Helvetica",size=10)
        self.font2=Font(family="Helvetica",size=8)
        self.interface.pack()
        self.Ip=StringVar()
        self.Ip.set("localhost")
        Label(self, text="Ip:", font=self.font, bg='grey').place(x=250, y=150)
        Entry(self, font=self.font, textvariable=self.Ip, bg="#999999").place(x=250, y=175)
        retour=Button(self.interface, text="Retour",bg='#999999',width=4,height=2, font=self.font2, command=self.MultiPlayerChoice)
        retour.place(x=750,y=750)
        creeUnePartie=Button(self.interface, text="Connection",bg='#999999',width=50,height=4, font=self.font, command=self.LoadingMenuInterface)
        creeUnePartie.place(x=120,y=550)
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
        retour=Button(self.interface, text="Retour",bg='#999999',width=4,height=2, font=self.font2, command=self.ChoiceIpHost)
        retour.place(x=750,y=750)
        creeUnePartie=Button(self.interface, text="Reesayer",bg='#999999',width=50,height=4, font=self.font, command=self.ChoiceIpHost)
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

