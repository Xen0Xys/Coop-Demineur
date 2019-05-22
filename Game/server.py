from tkinter import *
from time import sleep
import socket
import select
import threading
from random import randint

class ClientMessage():
    def __init__(self, message, client):
        self.message=message
        self.client=client

class Network():
    def __init__(self):
        self.serverOn=True
        self.canAcceptClient=True
        self.ClientList=[]
        self.EventList=[]
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    def StartServer(self, ip):
        self.server.bind((ip, 1001))
        self.server.listen(5)
        threading.Thread(target=self.AcceptClient).start()
    def CloseServer(self):
        self.serverOn=False
        for client in self.ClientList:
            client.close()
        self.server.close()
        print("Server closed")
    def CloseClient(self, client):
        client.close()
        for i in range(len(self.ClientList)):
            if client==self.ClientList[i]:
                del self.ClientList[i]
                break
    def AcceptClient(self):
        try:
            while self.serverOn:
                try:
                    rlist, wlist, xlist = select.select([self.server], [], [], 0.05)
                    for connection in rlist:
                        if self.canAcceptClient==True:
                            client, connectionInfos = connection.accept()
                            self.ClientList.append(client)
                            self.SendMessage("instruct;client_account_changed*{}".format(len(self.ClientList)), self.ClientList[0])
                        else:
                            client, connectionInfos = connection.accept()
                            self.ClientList.append(client)
                            self.OnNewClientJoin(client)
                except OSError as e:
                    print(e)
                except ValueError as e:
                    print(e)
        except RuntimeError as e:
            print(e)
    def OnNewClientJoin(self, client):
        self.SendMessage(self.formateMatrice, client)
        for item in self.EventList:
            client.send("instruct;{}*{}*{}".format(item[0], item[1]*25, item[2]*25))
    def GetMessages(self, function):
        try:
            while self.serverOn:
                if len(self.ClientList)>0:
                    try:
                        rlist, wlist, xlist = select.select(self.ClientList, [], [], 0.05)
                        for client in rlist:
                            message = client.recv(2048).decode()
                            evt = ClientMessage(message, client)
                            function(evt)
                    except OSError as e:
                        print(e)
                    except ValueError as e:
                        print(e)
        except RuntimeError as e:
            print(e)
    def SendMessage(self, message, client):
        threading.Thread(target=self.__SendMessage, args=(message, client,)).start()
    def __SendMessage(self, message, client):
        client.send(message.encode())

class EventHandler():
    def __init__(self):
        pass
    def GenerateMatrice(self, height, width, bombeNbre):
        #Matrice
        Matrice=[]
        for i in range(width):
            temp=[]
            for j in range(height):
                temp.append(1)
            Matrice.append(temp)
        #Bombes
        k=0
        while k<bombeNbre:
            k=k+1
            r=randint(0, width-1)
            s=randint(0, height-1)
            if Matrice[r][s]==2:
                k=k-1
            else:
                Matrice[r][s]=2
        print(Matrice)
        return self.SerializeMatrice(Matrice, height, width)
    def SerializeMatrice(self, Matrice, height, width):
        final="instruct;start*{}*{}".format(height, width)
        for i in range(len(Matrice)):
            for j in range(len(Matrice)):
                print(i*height+j)
                final+="*" + str(Matrice[i][j])
        return final
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
        """Reception des messages"""
        message = self.Deserializer(evt.message)
        if evt.message=="":
            self.CloseClient(evt.client)
        if message["message_type"]=="instruct":
            if message["message_body"]["name"] == "close_connection":
                self.CloseClient(evt.client)
            elif message["message_body"]["name"] == "start":
                self.EventList=[]
                self.canAcceptClient=False
                height = int(message["message_body"]["args"][0])
                width = int(message["message_body"]["args"][1])
                bombNbre = int(message["message_body"]["args"][2])
                msg=self.GenerateMatrice(height, width, bombNbre)
                self.formateMatrice=msg
                for client in self.ClientList:
                    self.SendMessage(msg, client)
            elif message["message_body"]["name"] == "left_click":
                x=int(message["message_body"]["args"][0])
                y=int(message["message_body"]["args"][1])
                #EventList
                exist=False
                for item in self.EventList:
                    if item[0]=="left_click":
                        if item[1]==x//25:
                            if item[2]==y//25:
                                exist=True
                if exist==False:
                    self.EventList.append(("left_click", x//25, y//25))
                #//EventList
                for client in self.ClientList:
                    self.SendMessage("instruct;left_click*{}*{}".format(x, y), client)
            elif message["message_body"]["name"] == "right_click":
                x=int(message["message_body"]["args"][0])
                y=int(message["message_body"]["args"][1])
                #EventList
                exist=False
                for item in self.EventList:
                    if item[0]=="right_click":
                        if item[1]==x//25:
                            if item[2]==y//25:
                                exist=True
                if exist==False:
                    self.EventList.append(("right_click", x//25, y//25))
                #//EventList
                self.EventList.append(("right_click", x//25, y//25))
                for client in self.ClientList:
                    self.SendMessage("instruct;right_click*{}*{}".format(x, y), client)
        elif message["message_type"]=="message":
            if message["message_body"]["name"] == "dev_message":
                print("[Server] : " + message["message_body"]["args"][0])
        print(message)

class Main(Network, EventHandler):
    def __init__(self):
        Network.__init__(self)
        EventHandler.__init__(self)
        #self.Start()
    def Start(self, ip):
        self.StartServer(ip)
        self.StartEventHandler()


if __name__=="__main__":
    main=Main()
