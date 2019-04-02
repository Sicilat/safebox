import socket, threading, datetime
class ClientThread(threading.Thread):
    def __init__(self,clientAddress,clientsocket):
        threading.Thread.__init__(self)
        self.csocket = clientsocket
        print (datetime.datetime.now(), " - New connection added: " , clientAddress)
    def run(self):
        print (datetime.datetime.now() , " - Connection from : " , clientAddress)
        msg = ['', '']
        data = self.csocket.recv(2048)
        msg = data.decode()
        print (datetime.datetime.now() , " - From " , clientAddress , " :", msg)
        data = self.csocket.recv(2048)
        msg = data.decode()
        print (datetime.datetime.now() , " - From " , clientAddress , " :" , msg)
        print (datetime.datetime.now() , " - Client at ",  clientAddress , " disconnected...")





LOCALHOST = "127.0.0.1"
PORT = 8080
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((LOCALHOST, PORT))
print(datetime.datetime.now() , " - Server started")
print(datetime.datetime.now() , " - Waiting for client request..")
while True:
    server.listen(1)
    clientsock, clientAddress = server.accept()
    newthread = ClientThread(clientAddress, clientsock)
    newthread.start()