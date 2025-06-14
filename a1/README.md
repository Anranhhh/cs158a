# CS158A Assignment 1
This assignment implements TCP-based client and server programs that can handle an arbitrary length of messages.

## Files Included
- `myvlclient.py`: a client program
- `myvlserver.py`: a server program
- `README.md`: instructions and usage example

## Run the Program

### Step 1. Start the server
In one terminal:

Execute command: `python myvlserver.py` -> server starts waiting for client's connection request

Example:

<img width="525" alt="Screenshot 2025-06-14 at 2 28 11 PM" src="https://github.com/user-attachments/assets/8ab89120-0149-47c1-88f1-b0904d4e7b34" />



### Step 2. Run the client
Open another terminal:

Execute command: `python myvlclient.py`

Test the input with "10helloworld"

Example:

<img width="519" alt="Screenshot 2025-06-14 at 2 29 18 PM" src="https://github.com/user-attachments/assets/f25940f8-5b6b-4ab7-b552-0166574d6915" />

## Execution Example & Output
### From the server's side
- shows the client's IP address and port number when connected successfully
- shows the message's length and the message itself
- shows the length of the message that was sent to the client
- notifies the connection was closed

<img width="520" alt="Screenshot 2025-06-14 at 2 37 39 PM" src="https://github.com/user-attachments/assets/d603d630-099f-433f-9d09-b443deab59be" />

### From the client's side
- prints the received modified message from the server

<img width="519" alt="Screenshot 2025-06-14 at 2 36 53 PM" src="https://github.com/user-attachments/assets/74260c99-126f-47f9-9e13-d06abf8ab8e2" />
