from tkinter import *
from time import sleep
import socket
import select
import threading

class ClientMessage():
    def __init__(self, message, client):
        self.message=message
        self.client=client

class Network():
    def __init__(self):
        self.serverOn=True
        self.ClientList=[]
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    def StartServer(self):
        self.server.bind(("localhost", 1001))
        self.server.listen(5)
        threading.Thread(target=self.AcceptClient).start()
    def CloseServer(self):
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
                rlist, wlist, xlist = select.select([self.server], [], [], 0.05)
                for connection in rlist:
                    client, connectionInfos = connection.accept()
                    self.ClientList.append(client)
                    self.SendMessage("instruct;client_account_changed*{}".format(len(self.ClientList)), self.ClientList[0])
        except RuntimeError as e:
            print(e)
    def GetMessages(self, function):
        try:
            while self.serverOn:
                if len(self.ClientList)>0:
                    rlist, wlist, xlist = select.select(self.ClientList, [], [], 0.05)
                    for client in rlist:
                        message = client.recv(1024).decode()
                        evt = ClientMessage(message, client)
                        function(evt)
        except RuntimeError as e:
            print(e)
    def SendMessage(self, message, client):
        threading.Thread(target=self.__SendMessage, args=(message, client,)).start()
    def __SendMessage(self, message, client):
        client.send(message.encode())

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
        message = self.Deserializer(evt.message)
        if evt.message=="":
            self.CloseClient(evt.client)
        if message["message_type"]=="instruct":
            if message["message_body"]["name"] == "close_connection":
                self.CloseClient(evt.client)
        elif message["message_type"]=="message":
            if message["message_body"]["name"] == "dev_message":
                print("[Server] : " + message["message_body"]["args"][0])

class Main(Network, EventHandler):
    def __init__(self):
        Network.__init__(self)
        EventHandler.__init__(self)
        #self.Start()
    def Start(self):
        self.StartServer()
        self.StartEventHandler()


if __name__=="__main__":
    main=Main()
