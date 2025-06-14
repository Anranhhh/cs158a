from socket import *

serverName = 'localhost' # ip address
serverPort = 12000 # port number

# TCP SOCKET_STREAM
clientSocket = socket(AF_INET, SOCK_STREAM)
# Connect to the server
clientSocket.connect((serverName, serverPort))

# Ask user for input
user_input = input('Input lowercase sentence: ')

# Send the input message to the server
clientSocket.send(user_input.encode())

# Receive the modified sentence from the server
modifiedSentence = clientSocket.recv(64) 

# Print the modified sentence
print('From Server: ', modifiedSentence.decode()) 

# Close the connection
clientSocket.close()
