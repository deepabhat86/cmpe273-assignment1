import socket
import sys
import time

TCP_IP = '127.0.0.1'
TCP_PORT = 5000
BUFFER_SIZE = 1024
MESSAGE = "ping"

#send to server
def send(id=0):
    #argv[3] is the number of requests to send
    for i in range(1,int(sys.argv[3])+1):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((TCP_IP, TCP_PORT))
        #if its the first message, send "<client_id>:Connected Client" so that server will print this
        if(i==1):
            str_to_send=id+":Connected Client"
            s.send(str_to_send.encode())
            data=s.recv(BUFFER_SIZE)

        print("Sending data:ping")
        s.send(f"{id}:{MESSAGE}".encode())
        #recieving from server
        data = s.recv(BUFFER_SIZE)
        s.close()
        print("received data:", data.decode())

        #sleep for the amount of time specified in second command line argument
        time.sleep(int(sys.argv[2]))


def get_client_id():
    #read command line argument: 1st argument is client id
    id = sys.argv[1]
    return id


send(get_client_id())
