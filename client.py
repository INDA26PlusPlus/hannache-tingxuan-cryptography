
import socket



def start_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #AF_INET -> IPv4. SOCK_STREAM -> TCP
    client.connect(("127.0.0.1", 1010)) #ansluter till servern
    print("connected to server")

    #client is how i make the connections from now on
    return client

client = start_client()

#to test stuff we start by hardcoding a message
#sending message
file_msg = "secret msg hihi"
file_id = 1
client.sendall((file_msg + "|" + str(file_id)).encode("utf-8"))

#revience message
responde_tcp = client.recv(2048)
responde = responde_tcp.decode("utf-8")
print(f"svar från server {responde}")

client.close()