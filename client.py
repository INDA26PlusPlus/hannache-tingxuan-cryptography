
import socket, hashlib
from cryptography.fernet import Fernet


#Prep crypting
def init_crypt():
    key = Fernet.generate_key()
    #imagine this as a more complex cesar schiffer. I get this long text that can scramble my text. I can redo it it i have the key but very svårt without it.
    #   Like rsa i guess?
    helper_cipher = Fernet(key) #this is what i run my commands with. Its like a helper so cute.
    #helper_cipher.encrypt(...)
    #helper_cipher.decrypt(...) very strightforward. So nice
    return key, helper_cipher

def start_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #AF_INET -> IPv4. SOCK_STREAM -> TCP
    client.connect(("127.0.0.1", 1010)) #ansluter till servern
    print("connected to server")

    #client is how i make the connections from now on
    return client

def ask_for_input():#counter):
    a = input("What do you wanna do? (1 = Send, 2 = Read, 3 = Quit): ")
    msg = ""
    id = ""

    if a == "1":
        action = "send"
        msg = input("What data do you wanna send: ")
        while True:
            id = input("which_pos? (defult is next on counter enter enter): ")
            if id == "":
                break
            if id.isdigit():
                if int(id) < 8:
                    break
            print("please chose an id between and including 0 and 7")


        # if id == "":
        #     id = str(counter)
#            counter += 1 this is heykey useuess because its a local variable.
    elif a == "2":
        action = "read"
        while True:            
            id = input("Which id to read? ")
            if id == "":
                break
            if id.isdigit():
                if int(id) < 8 and int(id) >= 0:
                    break
            print("please chose an id between and including 0 and 7")

    else:
        action = "quit"
    return action, msg, id

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
    return buffer.decode("utf-8").strip() #Strip gets rid of \n


def verify_hash_tree(file_data, file_id, proof_hashes, leaves = 8):
    
    current_hash = hashlib.sha256(file_data.encode("utf-8")).digest()
    index = int(file_id) + leaves #top is 1, not top is the other half
    # [1v, 2h, 3v, 4h, 5v, 6h, 7v, 8h]

    for sibling in proof_hashes:
        #check if they are the right or left
        if index % 2 == 0: #vi är vänter
            combined = current_hash + sibling
        else:
            combined = sibling + current_hash

        #hash the combined = the parent
        current_hash = hashlib.sha256(combined).digest()
        index //= 2

    return current_hash

#good stuff to have
client = start_client()
key, helper_cipher = init_crypt()
counter = 0
expected_top_hash = bytes.fromhex(recieve_data(client)) #temporary the server is the one that send me the inital one. (honestly thats a vunerability but the task allows it so easy for me hahaha. Otherwise client could make the tree)

#this loops
while True:
    action, file_msg, file_id = ask_for_input()

    if file_id == "":
        file_id = counter
        counter += 1

    if action == "quit":
        client.sendall(b"QUIT\n") #tell server to close
        client.close()
        break

    elif action == "send":
        #update the local tree
        #crypt the message
        encrypted_msg = helper_cipher.encrypt(file_msg.encode("utf-8")).decode("utf-8")
        
        #sending
        client.sendall((f"SEND {encrypted_msg} {file_id}\n").encode("utf-8"))
        # "SEND myverycoolmessage 3\n"

        response = recieve_data(client).split()
        #get input as: [lst], new_top_hash 
        server_top_hash = bytes.fromhex(response.pop())
        components = [bytes.fromhex(x) for x in response]
        expected_top_hash = verify_hash_tree(encrypted_msg, file_id, components)

        if server_top_hash == expected_top_hash:
            #sucess
            print("Sucessfully sent")
        else:
            print("not sucessful sent")
            client.sendall(b"QUIT") #tell server to close
            client.close()
            break

    else:
        #action == read
        #match with the local tree top.

        client.sendall(f"READ {file_id}\n".encode("utf-8"))

        #this is the crypted data
        response = recieve_data(client).split()
        if response[0] == "EMPTY":
            print("there was nothing here")
            continue

        #split the response
        response.pop() #skip top hash. Trust our own more
        encrypted_msg = response.pop()
        components = [bytes.fromhex(x) for x in response]

        #check the tree
        if verify_hash_tree(encrypted_msg, file_id, components) == expected_top_hash:
            print("sucess")
            message = helper_cipher.decrypt(encrypted_msg.encode("utf-8")).decode("utf-8")
            print(f"The recieved message: {message}")

        else:
            print("its corrupted")
            #i'll just stop it here
            client.sendall(b"QUIT\n") #tell server to close
            client.close()
            break

        #now its the crypted version so decrypt it. but before that check the tree





    # #to test stuff we start by hardcoding a message
    # #sending message
    # file_msg = "secret msg hihi"
    # file_id = 1
    # client.sendall((file_msg + "|" + str(file_id) + "\n").encode("utf-8"))

    # #revience message
    # response_tcp = client.recv(2048)
    # response = response_tcp.decode("utf-8")
    # print(f"svar från server {response}")

    # client.close()