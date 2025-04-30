from socket import *;

serverHostname = "localhost";
serverPort = 3000;

listeningSocket = socket(AF_INET, SOCK_DGRAM);
listeningSocket.bind((serverHostname, serverPort));

count = 1;

print("Server is running....")
while True:
    count += 1;
    data, clientAddress = listeningSocket.recvfrom(1024)
    # I will ignore the fifth packet to test the case where a packet is lost.
    if(data.decode().lower() != "ping" or count == 5):
        # ignore any messages that aren't a ping message as the server is only to handle ping messages.
        continue;
    print(f"a message was received from client {clientAddress[0]}:{clientAddress[1]}")
    listeningSocket.sendto("PONG".encode(), clientAddress);