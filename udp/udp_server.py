import socket
import time
import os


UDP_IP = '127.0.0.1'
UDP_PORT = 4000
BUFFER_SIZE = 1024
FILEPATH = os.getcwd()+os.path.sep+"server_upload.txt"

def listen_forever():
    lines=[]
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(("", UDP_PORT))
    print(f"Server started at port {UDP_PORT}")
    print("Accepting a file upload...")

    while True:
        # get the data sent from client
        data, ip = s.recvfrom(BUFFER_SIZE)
        line=data.decode(encoding="utf-8").strip()
        #if last line
        if(line=="Completed upload"):
            with open(FILEPATH,'w') as fp:
                fp.writelines(lines)
            print("Upload successfully completed.")
        else:
            #to simulate socket timeout, uncomment this sleep
            #time.sleep(6)
            #every line in the file sent by client is of the format <id>:<text>
            message_id=line.split(',')[0]
            message=line.split(',')[1]
            #if index already exist in list, update that index else append to the list
            try:
                lines[int(message_id)]=message+"\n"
            except:
                lines.append(message+"\n")
            s.sendto(message_id.encode(), ip)

listen_forever()
