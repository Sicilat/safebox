import socket, threading, datetime
from Crypto.Cipher import AES

def get_time():
    return str(datetime.datetime.now())

def log_pass():
    global log_file
    log_file.write('\n')

class ClientThread(threading.Thread):
    def __init__(self,clientAddress,clientsocket):
        global log_file
        threading.Thread.__init__(self)
        self.csocket = clientsocket
        print_msg = get_time() , " - New connection added: " , clientAddress
        print(str(print_msg))
        log_file.write(str(print_msg))
        log_pass()
    def run(self):
        global log_file
        msg = ['', '', '']
        usr_list = ['Alexandre', 'admin']
        pass_list = ['Test', 'admin']
        print_msg = get_time() , " - Connection from : " , clientAddress
        print(str(print_msg))
        log_file.write(str(print_msg))
        log_pass()
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
                print_msg = get_time() , " - Client at ",  clientAddress , " logged in with username : " , usr
                print(str(print_msg))
                log_file.write(str(print_msg))
                log_pass()
            else:
                self.csocket.send(bytes('log_shit','UTF-8'))
                print_msg = get_time() , " - Client at ",  clientAddress , " tried to log in with username : " , usr
                print(str(print_msg))
                log_file.write(str(print_msg))
                log_pass()

        print_msg = get_time() , " - Client at ",  clientAddress , " disconnected..."
        print(str(print_msg))
        log_file.write(str(print_msg))
        log_pass()




log_file = open('./log.txt', 'a', encoding = 'UTF-8')
LOCALHOST = "127.0.0.1"
PORT = 8080
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((LOCALHOST, PORT))
print_msg = get_time() , " - Server started"
print(str(print_msg))
log_file.write(str(print_msg))
log_pass()
print_msg = get_time() , " - Waiting for client request.."
print(str(print_msg))
log_file.write(str(print_msg))
log_pass()
while True:
    server.listen(1)
    clientsock, clientAddress = server.accept()
    newthread = ClientThread(clientAddress, clientsock)
    newthread.start()