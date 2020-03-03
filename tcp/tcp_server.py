import socket
import _thread

TCP_IP = '127.0.0.1'
TCP_PORT = 5000
BUFFER_SIZE = 1024

#every thread works on this function
def on_new_client(clientsocket,addr):
    #recieve data from client
    data = clientsocket.recv(BUFFER_SIZE)
    if not data: 
        print('No data received.')
    #client id eg "A" is the first part of the data
    client_id=data.decode().split(":")[0]
    #message(ping) is the second part of the data
    message=data.decode().split(":")[1]

    #first message contains Connected Client, if yes, then recieve the second message (ping)
    if(message.startswith("Connected Client")):
        print("Connected Client:"+client_id)
        #send acknowledgment for connected client
        clientsocket.send("Syn".encode())
        #second part of the message
        data = clientsocket.recv(BUFFER_SIZE)
        message=data.decode().split(":")[1]

    print("received data:"+client_id+":"+message)
    clientsocket.send("pong".encode())
    clientsocket.close()


def listen_forever():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((TCP_IP, TCP_PORT))
    print('Server started at port 5000')
    s.listen(5)

    while True:
        conn, addr = s.accept()     # Establish connection with client.        
        _thread.start_new_thread(on_new_client,(conn,addr)) 

listen_forever()
