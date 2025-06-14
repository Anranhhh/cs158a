from socket import *

serverPort = 12000 # port number

serverSocket = socket(AF_INET, SOCK_STREAM) # Create a TCP socket

# This empty string means the server will listen on all available interfaces
serverSocket.bind(('', serverPort)) # Bind the socket to the port

serverSocket.listen(1) # Listen for incoming connections

# Accept the connection request from a client
cnSocket, addr = serverSocket.accept()
print(f"Connection from {addr}")

# Receive the message
whole_msg = cnSocket.recv(64).decode()
msg_length = int(whole_msg[:2])
message = whole_msg[2:]
print(f"msg_len: {msg_length}")
print(f"processed: {message}")

# Process the message
capSentence = message.upper() # convert to uppercase

# Send back the modified message
cnSocket.send(capSentence.encode()) 
print(f"msg_len_sent: {len(capSentence)}")

# Close the connection
print("Connection closed\n")
cnSocket.close()
