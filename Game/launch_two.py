from server import Main as Server
from tkinter.font import Font
from random import randint
from tkinter import *
import threading
import socket
import select
from client import Main as client
from time import sleep

def StartClient1():
    main1 = client()

def StartClient2():
    main2 = client()

threading.Thread(target=StartClient1).start()
StartClient2()
