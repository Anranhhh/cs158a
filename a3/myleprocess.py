from socket import *
import uuid
import os
import json
import threading
import time

class Message:
    def __init__(self, uuid, flag):
        self.uuid = str(uuid)
        self.flag = flag

    def to_json(self):
        return json.dumps(self.__dict__).encode()

    @staticmethod
    def from_json(data):
        obj = json.loads(data.decode())
        return Message(obj['uuid'], obj['flag'])

def log(msg):
    with open(log_file, "a") as f:
        f.write(msg + "\n")

def send_message(uuid, flag):
    msg = Message(uuid, flag)
    clientSocket.sendall(msg.to_json())
    log(f"Sent: uuid={uuid}, flag={flag}")
    print(f"Sent: uuid={uuid}, flag={flag}", flush=True)

def server_thread():
    while True:
        try:
            conn, addr = serverSocket.accept()
            print(f"Accepted connection from {addr}", flush=True)
            handle_server_connection(conn)
            break  # Stop after one connection
        except Exception as e:
            print(f"Server accept error: {e}", flush=True)
            time.sleep(1)

def handle_server_connection(connection):
    global leader_id, state
    print("Server thread started", flush=True)
    while True:
        try:
            data = connection.recv(1024)
            if not data:
                break
            msg = Message.from_json(data)
           
            msg_uuid = uuid.UUID(msg.uuid)
            log(f"Received: uuid={msg.uuid}, flag={msg.flag}, "
                f"{'greater' if msg_uuid > node_id else 'less' if msg_uuid < node_id else 'same'}, {state}, "
                f"leader_id={leader_id if state == 1 else 'N/A'}")
            
            # Election in progress
            if msg.flag == 0:
                if msg_uuid > node_id:
                    send_message(msg_uuid, 0)
                elif msg_uuid < node_id:
                    pass  # ignore
                    log(f"Ignored message from uuid={msg.uuid}, flag=0")
                elif msg_uuid == node_id:
                    # I am the leader
                    leader_id = msg.uuid
                    state = 1
                    log(f"Leader is decided to {leader_id}.")
                    send_message(msg_uuid, 1)

            # Leader decided
            elif msg.flag == 1: 
                if state == 0: # At the node that is not the leader
                    state = 1
                    leader_id = msg.uuid
                    log(f"Leader is decided to {leader_id}.")
                    send_message(msg_uuid, 1)
                elif msg.uuid == leader_id: # Election complete since goes back to the leader 
                    break  

        except Exception as e:
            log(f"Error in server thread: {e}")
            break
    connection.close()

# Method to read from config.txt
def read_config():
    with open("config.txt", "r") as f:
        lines = f.read().strip().split("\n")
        my_ip, my_port = lines[0].split(',')
        neighbor_ip, neighbor_port = lines[1].split(',')
    return (my_ip.strip(), int(my_port.strip())), (neighbor_ip.strip(), int(neighbor_port.strip()))

# Generate UUID for this process
node_id = uuid.uuid4()
state = 0 # 0 -> election in progress, 1 -> election ends & leader decided
leader_id = None

log_file = f"log_{str(node_id)[-6:]}.txt"
if os.path.exists(log_file): os.remove(log_file)

# Call method to read itself and neighbor's IP address and port # from config.txt
my_addr, neighbor_addr = read_config()

serverSocket = socket(AF_INET, SOCK_STREAM)  # Create a TCP socket
serverSocket.bind(('', my_addr[1])) # Bind the socket to the port
serverSocket.listen(1)
print(f"Server listening on {my_addr[0]}:{my_addr[1]}", flush=True)

# Create threads
t = threading.Thread(target=server_thread, daemon=True)
t.start()

time.sleep(2) # Wait for a server node to be up

clientSocket = socket(AF_INET, SOCK_STREAM)

while True:
    try:
        clientSocket.connect((neighbor_addr[0], neighbor_addr[1]))
        break
    except ConnectionRefusedError:
        time.sleep(1)

# Send initial message to start the election
send_message(node_id, 0)

# Wait until election terminates
while state == 0:
    time.sleep(1)

print(f"Leader is {leader_id}")
log(f"Leader is {leader_id}")
