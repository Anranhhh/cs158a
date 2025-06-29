from socket import *
import threading
import sys

serverName = '127.0.0.1' # Server IP address
serverPort = 12345 # Server port number
bufSize = 1024

# Receives messages
def recv_loop(sock):
    while True:
        try:
            msg = sock.recv(bufSize).decode()
        except OSError:
            break
        if not msg:
            break
        print(f"\n{msg}")

# Sends messages
def send_loop(sock):
    while True:
        try:
            text = input()
        except EOFError:
            text = "exit"
        if text.lower() == "exit":
            try:
                sock.sendall(b"exit")
            except OSError:
                pass
            break

        msg = text.encode()
        for i in range(0, len(msg), bufSize):
            sock.sendall(msg[i:i + bufSize])

    # "exit" was entered to exit the chat and disconnected to the server      
    sock.close()
    print("Disconnected from server")
    sys.exit(0)

# TCP SOCKET_STREAM
clientSocket = socket(AF_INET, SOCK_STREAM)
# Connect to the server
clientSocket.connect((serverName, serverPort))

print("Connected to chat server. Type 'exit' to leave.")

t = threading.Thread(target=recv_loop, args=(clientSocket,), daemon=True)
t.start()
send_loop(clientSocket)