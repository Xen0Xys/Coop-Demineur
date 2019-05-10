from client import Main as client
from server import Main as server
import threading

threading.Thread(target=server).start()
client()
