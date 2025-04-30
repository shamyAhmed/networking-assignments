from socket import *;
import time;

serverHostname = "localhost";
serverPort = 3000;

# although udp doesn't have a connection I would like to name the socket connection
connection = socket(AF_INET, SOCK_DGRAM);
connection.settimeout(1.0);

for i in range(10):
    startTime = time.time();
    connection.sendto("PING".encode(), (serverHostname, serverPort));
    # wait for a pong message from the server.
    delay = 0;
    try:
        # display the delay, how to measure the delay between two lines of execution?
        data, addr = connection.recvfrom(1024);
        if(addr[0] == serverHostname and addr[1] == serverPort and data.decode().lower() == "pong"):
            endTime = time.time();
            delay = (endTime - startTime) * 1000;
    except timeout:
        delay = None;

    print(f"Packet {i} is lost" if delay is None else f"Packet {i} RTT is {delay}");

connection.close();