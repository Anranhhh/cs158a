# CS158A Assignment 2
This assignment implements TCP-based client and server programs in which the server supports multiple clients joining to exchange messages.

## Files Included
- `mychatclient.py`: a client program
- `mychatserver.py`: a server program
- `README.md`: instructions and execution examples/test cases

## Run the Program

### Step 1. Start the server
In one terminal:

Execute command: `python mychatserver.py` -> server starts waiting for the clients' connection requests

### Step 2. Run the client
Open multiple terminal windows:

Execute command: `python mychatclient.py`

### Step 3. Build the connections
Make sure that all clients are connected to the server, which means they are in the same chat now

Server's side:

<img width="426" alt="Screenshot 2025-06-29 at 4 42 24 PM" src="https://github.com/user-attachments/assets/899501d7-2e06-4cab-b4de-c3bc384255c8" />

Client's side:

<img width="426" alt="Screenshot 2025-06-29 at 4 43 50 PM" src="https://github.com/user-attachments/assets/249362cc-8463-4f02-99f4-b93a49485a2d" />

## Execution Example & Output
### From the server's side
- Shows a message every time when a new client joins the chat, including the client's IP address and port number
- Receives messages from all current clients and shows the messages
- Disconnected from every client that exited and shows a message

<img width="426" alt="Screenshot 2025-06-29 at 4 45 29 PM" src="https://github.com/user-attachments/assets/80fb7a19-1b18-4bd3-a2fe-8036ee58bf8b" />


### From the client's side
- Sends raw text input to the server, and messages will be broadcasted/relayed to all other current clients
- Enters "exit" to disconnect from the server and exit the chat
  - Shows a message on its own side, and other clients do not know that

Client 1:

<img width="426" alt="Screenshot 2025-06-29 at 4 46 26 PM" src="https://github.com/user-attachments/assets/d9108633-648b-4177-86a7-3aa7e85ec5bc" />

Client 2:

<img width="426" alt="Screenshot 2025-06-29 at 4 47 19 PM" src="https://github.com/user-attachments/assets/bb2db571-4ff2-4b13-a7f9-f5fdb007bf57" />

Client 3:

<img width="426" alt="Screenshot 2025-06-29 at 4 47 46 PM" src="https://github.com/user-attachments/assets/5f0ad73c-77f2-4d38-8ffe-99fa02375312" />
