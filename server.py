import socket, hashlib


def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #AF_INET -> IPv4. SOCK_STREAM -> TCP
    server.bind(("127.0.0.1", 1010)) #ansluter till servern
    server.listen(1) #1 means only 1 queue spot. (one to one connection)
    print("Waiting for client")

    connection, adress = server.accept() #accept the queue
    print(f"connected to {adress}")

    return server, connection, adress


def recieve_data(connection):
    buffer = bytearray()

    while True:
        in_data = connection.recv(2048) #läser upp till 2048 bytes??
        if not in_data:
            break
            #they disconnected. no longer getting input
        buffer.extend(in_data)
        if b"\n" in buffer:
            break
    return buffer.decode("utf-8").strip() #Strip 

def send_data(connection, message=None):
    if message == None:
        message = "Message received\n"
    connection.sendall(message.encode("utf-8"))

def closing(server, connection):
    connection.close()
    server.close()

def upload(tree, id, hash):
    tree[id+8] = hash  # change the id:th leaf and update all hash upstream
    n = (id+8)//2
    while n>=1:
        tree[n] = hashlib.sha256(tree[2*n]+tree[2*n+1]).digest()
        n //= 2
    return tree 

def get_components(tree, file_id, leaves = 8):
    index = file_id + leaves
    component_lst = []
    n = index
    while n > 1:
        sibling_index = n + 1 if n % 2 == 0 else n - 1
        component_lst.append(tree[sibling_index])
        n //= 2
    return component_lst

server, connection, adress = start_server()

#send the top hash back to client directly
# a tree with 8 leaves, total 15 nodes
tree = [b"\x00" * 32 for i in range(16)]
#this makes the tree. sum of the two child nodes. initial
for i in range(7,0,-1):
    tree[i] = hashlib.sha256(tree[2*i]+tree[2*i+1]).digest()
connection.sendall((tree[1].hex() + "\n").encode("utf-8"))

all_data = [None for i in range(8)]

while True:
    chunks = recieve_data(connection)
    message = chunks.split()

    if not message or message[0] == "QUIT":
        closing(server, connection)
        break

    elif message[0] == "SEND":
        # client.sendall((f"SEND {file_msg} {file_id}\n").encode("utf-8"))
        encrypted_msg = message[1]
        file_id = int(message[2])

        all_data[int(file_id)] = encrypted_msg
        #the index points towards the message.

        upload(tree, file_id, hashlib.sha256(encrypted_msg.encode("utf-8")).digest())

        response = " ".join(c.hex() for c in get_components(tree, file_id)) + " " + tree[1].hex() + "\n"
        #list + top-hash
        connection.sendall(response.encode("utf-8"))
    else: 
        #read
        file_id = int(message[1])
        if all_data[file_id] == None:
            connection.sendall(b"EMPTY\n")
            break

        top_hash = tree[1].hex()
        components = get_components(tree, file_id)
        response = " ".join(c.hex() for c in components) + " " + all_data[file_id] + " " + tree[1].hex() + "\n"
        connection.sendall(response.encode("utf-8"))

    # send_data(connection)


