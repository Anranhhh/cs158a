from socket import *
import threading

serverName = '127.0.0.1' # Server IP address
serverPort = 12345 # Server port number
bufSize = 1024

clientThreads = []
lock = threading.Lock()

serverSocket = socket(AF_INET, SOCK_STREAM) # Create a TCP socket
serverSocket.bind(('', serverPort)) # Bind the socket to the port
serverSocket.listen(1)
print(f"Server listening on {serverName}: {serverPort}")

# Removes "exited" client from the current client list
def remove_client(sock):
    with lock:
        for c in clientThreads:
            if c[0] is sock:
                clientThreads.remove(c)
                break
    try:
        sock.close()
    except OSError:
        pass

# Broadcasts client's message to all current other clients 
def broadcast(sender_sock, msg: bytes):
    for sock, _ in list(clientThreads):
        if sock is sender_sock:
            continue # Do not broadcast message again to the sender of the message 
        try:
            for i in range(0, len(msg), bufSize):
                sock.sendall(msg[i:i + bufSize])
        except OSError:             # peer disconnected while sending
            remove_client(sock)


def handle_client(sock, addr):
    port = addr[1] # addr[0] is client IP address, addr[1] is port number
    
    # In a while loop, keep broadcasting message to all current clients until 'exit' entered
    while True:
        try:
            message = sock.recv(bufSize)
        except OSError:
            break 
        if not message:
            break

        message = message.decode().rstrip('\n')
        print(f"{port}: {message}")

        # User entered exit to disconnect
        if message.lower() == "exit":
            break
        
        broadcast(sock, f"{port}: {message}".encode())
    
    # When exit the while loop, exit the chat grouop
    remove_client(sock)
    print(f"{addr} disconnected")

# In while loop, keep waiting and accepting new client's connection request
while True:
    try: 
        cnSocket, addr = serverSocket.accept() # Accepts connection requests 
    except KeyboardInterrupt:
        print("\nServer shutting down…")
        break
    
    print(f"New connection from {addr}")
    with lock:
        clientThreads.append((cnSocket, addr))
        
    # Handle multiple clients in using multiple threads
    t = threading.Thread(target=handle_client, args=(cnSocket, addr), daemon=True)
    t.start()

cnSocket.close()