import socket
import random
import time
import struct



serverName = 'localhost'
serverPort = 12000
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


print ('The server is ready to receive on port:' , serverPort)

serverSocket.bind((serverName, serverPort))

while True:
    #Generate randome #
    RandNum = random.randint(0,10)
    
    #Unpack the sequence # from Client
    packedSequence , clientAddress = serverSocket.recvfrom(2048)
    unpacked = struct.unpack("i", packedSequence)

    #Pack timestamp of receiving time
    receiveTime = time.time()
    packedRecieveTime = struct.pack("d", receiveTime)

    if RandNum < 4:
        print("Message with sequence number ", unpacked, "dropped")
        continue
    else:
        print("Responding to ping request with sequence number", unpacked, "received at" , receiveTime)
        serverSocket.sendto(packedRecieveTime,clientAddress)
        serverSocket.sendto(packedSequence,clientAddress)

    





