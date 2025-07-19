import json
import os
import socket
import sys
import threading
import time
import uuid

class Message:
    def __init__(self, uuid, flag: int):
        self.uuid = str(uuid)
        self.flag = int(flag)

    # Encode to json format
    def encode(self) -> bytes:
        return (json.dumps({"uuid": self.uuid, "flag": self.flag}) + "\n").encode()

    # Decode the json format to object
    @staticmethod
    def decode(raw: bytes):
        obj = json.loads(raw.decode())
        return Message(obj["uuid"], obj["flag"])

# Write log.txt file
def log(line: str):
    with open("log.txt", "a", encoding="utf-8") as f:
        f.write(line + "\n")

# Read config.txt
def read_config():
    with open("config.txt", encoding="utf-8") as f:
        lines = [ln.strip() for ln in f if ln.strip()]
    if len(lines) != 2:
        sys.exit("config.txt must have exactly two non-blank lines")
    my_ip, my_port = [x.strip() for x in lines[0].split(",")]
    nb_ip, nb_port = [x.strip() for x in lines[1].split(",")]
    return (my_ip, int(my_port)), (nb_ip, int(nb_port))

def send_message(uuid, flag):
    # Block until client socket is connected, then send msg ≤ BUF chunks
    client_ready.wait()
    data = Message(uuid, flag).encode()
    for i in range(0, len(data), BUF):
        client_sock.sendall(data[i:i+BUF])
    log(f"Sent: uuid={uuid}, flag={flag}")
    print(f"Sent: uuid={uuid}, flag={flag}", flush=True)

# Mehthod to read and process the message
def server_recv(sock):
    buf = bytearray()
    while True:
        chunk = sock.recv(BUF)
        if not chunk:
            return None 
        buf.extend(chunk)
        if b"\n" in chunk:
            line, _, _ = buf.partition(b"\n")
            return Message.decode(line)

def server_thread():
    global state, leader_id
    conn, addr = server_sock.accept()
    print(f"Accepted from {addr}", flush=True)

    while True:
        msg = server_recv(conn)
        if msg is None: 
            break

        msg_uuid = uuid.UUID(msg.uuid)
        cmp = "greater" if msg_uuid > node_id else "less" if msg_uuid < node_id else "equal"
        log(f"Received: uuid={msg.uuid}, flag={msg.flag}, {cmp}, {state}, "
            f"{leader_id if state else 'N/A'}")

        # Election in progress
        if msg.flag == 0:
            if msg_uuid > node_id:
                send_message(msg.uuid, 0)
            elif msg_uuid < node_id:
                log(f"Ignored message from uuid={msg.uuid}, flag=0")
            else: # msg_uuid == node_id here
                leader_id = msg.uuid
                state = 1
                log(f"Leader is decided to {leader_id}.")
                send_message(msg_uuid, 1)
        
        # Leader is decided, and msg.flag == 1
        else: 
            if state == 0:
                leader_id = msg.uuid
                state = 1
                log(f"Leader is decided to {leader_id}.")
                send_message(msg.uuid, 1)
            elif msg.uuid == leader_id:    # Finished a full circle
                print(f"I AM THE LEADER ({leader_id}).", flush=True)
                break
    conn.close()


BUF = 1024

MY_ADDR, NB_ADDR = read_config() # Read from config.txt
node_id = uuid.uuid4() # Generate UUID for this process
state = 0 # 0 = election in progress, 1 = leader decided
leader_id  = None
print(f"My UUID is: {node_id}")

if os.path.exists("log.txt"):
    os.remove("log.txt")

# TCP Socket
server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_sock.bind(MY_ADDR)
server_sock.listen(1)
print(f"Server listening on {MY_ADDR}", flush=True)

# In the threads
threading.Thread(target=server_thread, daemon=True).start()

# Client side
client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

# Connect with retry
client_ready = threading.Event()

while True:
    try:
        # print(f"Trying to connect to {NB_ADDR}", flush=True)
        client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        client_sock.connect(NB_ADDR)
        # print(f"Connected to neighbor at {NB_ADDR}", flush=True)
        client_ready.set()
        break
    except ConnectionRefusedError:
        # print(f"Waiting for neighbor at {NB_ADDR}...", flush=True)
        client_sock.close()
        time.sleep(1)

# Initiate election
send_message(node_id, 0)

# Wait until leader known
while state == 0:
    time.sleep(0.2)

print(f"Leader is {leader_id}", flush=True)
log(f"Leader is {leader_id}")
