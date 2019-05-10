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
        self.server.bind((hote, port))
        self.server.listen(5)
        threading.Thread(target=self.AcceptClient).start()
    def AcceptClient(self):
        try:
            while serverOn:
                client, connectionInfos = self.server.accept()
                self.ClientList.append(client)
        except RuntimeError as e:
            print(e)
    def GetMessage(self, function):
        try:
            while serverOn:
                rlist, wlist, xlist = select.select(clients_connectes, [], [], 0.05)
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
    def StartEventHandler(self):
        self.GetMessages#Ici
    def GetEvent(evt):
        pass

class Main(Network, EventHandler):
    def __init__(self):
        Network.__init__(self)
        EventHandler.__init__(self)
        self.Start()
    def Start(self):
        pass


main=Main()
