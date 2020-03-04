import socket
import os

UDP_IP = '127.0.0.1'
UDP_PORT = 4000
BUFFER_SIZE = 1024
MESSAGE = "ping"
FILEPATH = os.getcwd()+os.path.sep+"upload.txt"
MAX_RETRY_COUNT = 5
#global sequence counter
SEQID = 1


def send():
    print("Connected to the server.")
    print("Starting a file (upload.txt) upload...")
    #retry_counter
    counter=0
    socket_timeout_counter=0
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(5)
        seq=SEQID
        with open(FILEPATH) as fp:
            for cnt, line in enumerate(fp):
                while True:
                    line_to_send=str(seq)+","+line
                    #send to server socket
                    s.sendto(line_to_send.encode(), (UDP_IP, UDP_PORT))
                    try:
                        #client recieve data from server
                        data, ip = s.recvfrom(BUFFER_SIZE)
                        recieved=data.decode()
                        if (int(recieved)==seq):
                            print(f"Received ack({recieved}) from the server.")
                            #Reset counters
                            counter=0
                            socket_timeout_counter=0
                            seq=seq+1
                            break
                        else:
                            if(counter==MAX_RETRY_COUNT):
                                print("Maximum tries attempted. Upload failed..")
                                exit()
                            print("Did not recieve acknowledgement from server. Trying again...")
                            counter=counter+1
                    except socket.timeout:
                            if(socket_timeout_counter==MAX_RETRY_COUNT):
                                print("Maximum tries attempted. Upload failed..")
                                exit()
                            print("Socket timedout. Trying again..")
                            socket_timeout_counter=socket_timeout_counter+1
                            continue
        fp.close()
        s.sendto("Completed upload".encode(), (UDP_IP, UDP_PORT))
        
    except socket.error:
        print("Error! {}".format(socket.error))
        exit()

send()
