import socket
import pyautogui
import threading
import time
from threading import Timer

HEADER = 64
PORT = 888
# SERVER = ""
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

# try:
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)
print("ADDR:", ADDR)

# except socket.error as e:
#     print(e)
#     print('等待5秒之後繼續重試...')
#     server.send(f"等待5秒之後繼續重試...".encode(FORMAT))
#     time.sleep(5)

def handle_client(conn, addr):
    print(f"-----[NEW CONNECTION] {addr} connected.-----")
    conn.send(f"-----{addr}Connect success-----".encode(FORMAT))

    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg != DISCONNECT_MESSAGE:
                print(f"[{addr}] msg: [{msg}] \n")
                conn.send(f"Msg received.".encode(FORMAT))
            else:
                print(f"{msg} {addr} Stop \n")
                conn.send(f"StopMsg received.".encode(FORMAT))
                connected = False

    conn.close()


def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {PORT}")
    while True:
        conn, addr = server.accept()
        
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")


print("[STARTING] server is starting...")
start()