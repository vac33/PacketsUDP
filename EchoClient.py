import socket
import time
import struct


serverName = 'localhost' 
serverPort = 12000
lastPing = 10
sequence = 0

ottList = []
rttList = []
numRecieved = 0

clientSocket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
clientSocket.settimeout(1)
print ("Pinging", serverName , "," , serverPort ,": " )

while sequence < lastPing:
    #Create pack for squence #
    packedSequence = struct.pack("i", sequence)
    
    sequence +=1
    startTime = time.time()
    clientSocket.sendto(packedSequence, (serverName, serverPort))

    try:
        #Recvfrom Server and Unpack timestamp from server 
        packedRecieveTime, serverAddress = clientSocket.recvfrom(2048)
        unpackedRecieveTime = struct.unpack("d", packedRecieveTime)

        #Recvfrom Server sequence
        packedSequence, serverAddress = clientSocket.recvfrom(2048)


        recieveTime = unpackedRecieveTime[0]
        OTT = recieveTime - startTime
        ottList.append(float(OTT))
        RTT = ((time.time()) - startTime)
        rttList.append(float(RTT))
        print ("Ping message number {} RTT (OTT): {} ({}) secs".format(sequence, RTT, OTT))
        numRecieved += 1


    except socket.timeout:
        print("Ping message number {} timed out".format(sequence))

lostPercent = numRecieved/sequence
lostPercent = (1- lostPercent) * 100
max_RTT = max(rttList)
min_RTT = min(rttList)
avg_RTT = sum(rttList)/len(rttList)

max_OTT = max(ottList)
min_OTT = min(ottList)
avg_OTT = sum(ottList)/len(ottList)

#-Number of packets sent, received, lost (% loss rate)
#-Min, Max, Average RTT and OTT for all acknowledged ping packets
print("\n\nNumber of packets Sent: {}. Received: {}. Lost: {} %".format(sequence, numRecieved, round(lostPercent,0)))
print("RTT MIN:{}. MAX: {}. AVG:{}.".format(min_RTT, max_RTT, avg_RTT))
print("OTT MIN:{}. MAX: {}. AVG:{}.".format(min_OTT, max_OTT, avg_OTT))

clientSocket.close()
    
