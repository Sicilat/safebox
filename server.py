import socket, threading, datetime, time, random, sqlite3

def get_time():
    return str(datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'))

class ClientThread(threading.Thread):
    def __init__(self,clientAddress,clientsocket):
        threading.Thread.__init__(self)
        self.csocket = clientsocket
        print(get_time() + " - New connection added: " + str(clientAddress))
    def run(self):
        msg = ['', '', '']
        usr_list = ['Alexandre', 'admin']
        pass_list = ['Test', 'admin']
        print(get_time() + " - Connection from : " + str(clientAddress))
       
        #data = self.csocket.recv(2048)
        #msg = data.decode()
        #print (datetime.datetime.now() , " - From " , clientAddress , " :", msg)
        data = self.csocket.recv(2048)
        msg[0] = data.decode()
        data = self.csocket.recv(2048)
        msg[1] = data.decode()
        data = self.csocket.recv(2048)
        msg[2] = data.decode()
        if msg[0] == 'log':
            usr = msg[1]
            psw = msg[2]
            if usr in usr_list and psw in pass_list:
                self.csocket.send(bytes('log_fine','UTF-8'))
                print(get_time() + " - Client at " +  str(clientAddress) + " logged in with username : " + str(usr))
            else:
                self.csocket.send(bytes('log_shit','UTF-8'))
                print(get_time() + " - Client at " + str(clientAddress) + " tried to log in with username : " + str(usr))
        print(get_time() + " - Client at " + str(clientAddress) + " disconnected...")
        
LOCALHOST = "127.0.0.1"
PORT = 8080
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((LOCALHOST, PORT))
print(get_time() + " - Server started")
print(get_time() + " - Waiting for client request..")

while True:
    server.listen(1)
    clientsock, clientAddress = server.accept()
    newthread = ClientThread(clientAddress, clientsock)
    newthread.start()