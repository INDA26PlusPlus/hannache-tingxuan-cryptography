import socket


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
    tcp_data = connection.recv(2048) #läser upp till 2048 bytes??
    message = tcp_data.decode("utf-8") #means turns from 8 bit to not 8 bit...
    print(f"Message recieved: {message}")

def send_data(connection, message=None):
    if message == None:
        message = "Message received\n"
    connection.sendall(message.encode("utf-8"))

def closing(server, connection):
    connection.close()
    server.close()

server, connection, adress = start_server()
recieve_data(connection)
send_data(connection)
closing(server, connection)


