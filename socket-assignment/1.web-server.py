from socket import *
import os;

serverPort = 3000;
serverHost = "localhost";
baseDirPath = os.path.join(os.path.dirname(os.path.abspath(__file__)), "baseDir");

serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind((serverHost, serverPort));
serverSocket.listen();
print("listening on port 3000")

connectionSocket, clientAddress = serverSocket.accept();
print("connection established with client " + str(clientAddress));
requestString = "";
while True:
    data = connectionSocket.recv(1024);
    dataStr = data.decode();

    requestString += dataStr;
    if "\r\n\r\n" in dataStr:
        break;

def parseStartLine(line):
    return line.split(" ");

def parseHeaders(headersArr):
    headers = [];
    for header in headersArr:
        splitted = header.split(": ");
        if(len(splitted) != 2):
            break;
        headers.append((splitted[0], splitted[1]));
    return headers;

def parseRequest(requestMessage):
    requestLines = requestMessage.splitlines();
    startingLine, headers = requestLines[0], requestLines[1:];
    method, path, version = parseStartLine(startingLine);
    if(method != "GET"):
        raise Exception("Not supported");
    headersArr = parseHeaders(headers);
    dictionary = {
        "method": method,
        "path": path,
        "version": version,
        "headers": headersArr
    }
    return dictionary;

def getFile(path):
    path = path.lstrip('\\/');
    filePath = os.path.join(baseDirPath, path);
    return open(filePath, "rb");

def response(status):
    statusPhrases = {
        "200": "Ok",
        "404": "Not Found"
    }
    return f"HTTP/1.1 {str(status)} {statusPhrases[str(status)]}\r\n"

def header(response, header):
    return f"{response}{header[0]}: {header[1]}\r\n"

parsedRequest = parseRequest(requestString);
try:
    file = getFile(parsedRequest["path"]);
    responseMessage = response(200);
except FileNotFoundError as e:
    responseMessage = response(404);
    file = getFile("404.html");

file_size = os.fstat(file.fileno()).st_size;
responseMessage = header(responseMessage, ("Content-Type", "text/html"))
responseMessage = header(responseMessage, ("Content-Length", str(file_size)))

connectionSocket.send(responseMessage.encode());
connectionSocket.send("\r\n".encode());

while True:
    data = file.read(1024);
    if(not data):
        break;
    connectionSocket.send(data);
file.close();
connectionSocket.close();