import socket
import pyautogui
import time
from threading import Timer

HEADER = 64
PORT = 7414
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = ""
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)
print(client.recv(1024).decode(FORMAT))


def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)
    print(client.recv(1024).decode(FORMAT))


run = True
originTime = time.time()
while run:
    mx, my = pyautogui.position()
    localTime = time.time()
    runTime = localTime-originTime
    print("(x:",mx, ",y:", my, "),runTime:", round(runTime,3))
    send(f"(x:{mx}, y:{my}), runTime: {round(runTime,3)}")
    time.sleep(1) #隔0.1秒再傳
    if(localTime-originTime>=5):
        print(DISCONNECT_MESSAGE)
        send(DISCONNECT_MESSAGE)
        break

