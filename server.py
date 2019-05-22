import socket, threading, datetime, time, sqlite3, pickle

def receive_data(self):             #Recevoir les données des clients
    data = self.csocket.recv(2048)
    return pickle.loads(data)

def send_data(self, tdata):         #Envoyer les données aux clients
    data = pickle.dumps(tdata)
    self.csocket.send(data)

def create_tables():                #Créer les tables de la base de données si elles n existe pas
    db_connection = sqlite3.connect('database.db')
    cursor = db_connection.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS users(datestamp TEXT, email TEXT, password TEXT)')
    cursor.execute('CREATE TABLE IF NOT EXISTS storage(datestamp TEXT, email TEXT, id REAL, password TEXT, about TEXT)')
    cursor.close()
    db_connection.close()

def get_time():                     #Récupérer l heure et la date actuelle
    return str(datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'))

def del_account(self, data):        #upprimer un compte utilisateur
    db_connection = sqlite3.connect('database.db')
    cursor = db_connection.cursor()
    sql = "DELETE FROM users WHERE email='" + data[1] + "'"
    cursor.execute(sql)
    db_connection.commit()
    print(get_time() + " - Client depuis " +  str(clientAddress) + " a supprimméle compte : " + str(data[1]))
    cursor.close()
    db_connection.close()

def psw_menu(self, data):           #Gérer les données utilisateur en provenance du menu des mot de passe
    db_connection = sqlite3.connect('database.db')
    cursor = db_connection.cursor()
    while True:
        results = cursor.fetchall()
        sql = "SELECT * FROM storage WHERE email='" + data[1] + "'"
        cursor.execute(sql)
        results = cursor.fetchall()
        send_data(self, results)
        data = receive_data(self)
        if data[0] == 'psw_add':
            sql = "SELECT MAX(id) FROM storage WHERE email='" + data[1] + "'"
            cursor.execute(sql)
            id_psw = cursor.fetchone()[0]
            if type(id_psw) == 'NoneType':
                id_psw = int(id_psw) + 1
            else:
                id_psw = 0
            date = get_time()
            cursor.execute("INSERT INTO storage (datestamp, email, id, password, about) VALUES (?, ?, ?, ?, ?)", (date, data[1], id_psw, data[3], data[4]))
            db_connection.commit()
            print(get_time() + " - Client depuis " +  str(clientAddress) + " a rajouté un mot de passe avec l'E-mail : " + str(data[1]))
        if data[0] == 'dlt':
            sql = "DELETE FROM storage WHERE id='" + str(data[3]) + "'"
            cursor.execute(sql)
            db_connection.commit()
            print(get_time() + " - Client depuis " +  str(clientAddress) + " a supprimmé un mot de passe avec l'E-mail : " + str(data[1]))
    cursor.close()
    db_connection.close()

def logged_menu(self, data):        #Gérer les données utilisateur en provenance du menu principale
    data = receive_data(self)
    if data[0] == 'spr':
        del_account(self, data)
    if data[0] == 'psw':
        psw_menu(self, data)

def log_in(self, data):             #Gérer les connexions utilisateurs
    db_connection = sqlite3.connect('database.db')
    cursor = db_connection.cursor()
    sql = "SELECT * FROM users WHERE email='" + str(data[1]) + "' AND password='" + str(data[2]) + "'"
    cursor.execute(sql)
    result = len(cursor.fetchall())
    if result == 1:
        send_data(self, ['log_fine'])
        print(get_time() + " - Client depuis " +  str(clientAddress) + " c'est identifié avec l'E-mail : " + str(data[1]))
        cursor.close()
        db_connection.close()
        logged_menu(self, data)
        return 1
    else:
        send_data(self, ['log_shit'])
        print(get_time() + " - Client depuis " + str(clientAddress) + " a essayé de s'identifier avec l'E-mail : " + str(data[1]))
        cursor.close()
        db_connection.close()
        return 1

def create_account(self, data):     #Créer les comptes utilisateurs
    db_connection = sqlite3.connect('database.db')
    cursor = db_connection.cursor()
    sql = "SELECT * FROM users WHERE email='" + str(data[1]) + "'"
    cursor.execute(sql)
    result = len(cursor.fetchall())
    if result == 0:
        date = get_time()
        cursor.execute("INSERT INTO users (datestamp, email, password) VALUES (?, ?, ?)", (date, data[1], data[2]))
        db_connection.commit()
        print(get_time() + " - Client depuis " +  str(clientAddress) + " a créé un compte avec l'E-mail : " + str(data[1]))
        send_data(self, ['log_fine'])
    else:
        send_data(self, ['log_shit'])
        print(get_time() + " - Client depuis " + str(clientAddress) + " a essayé de créer un compte avec l'E-mail : " + str(data[1]))
    cursor.close()
    db_connection.close()
    return 0


class ClientThread(threading.Thread):       #Permet le multi tâche du serveur
    def __init__(self,clientAddress, clientsocket):
        threading.Thread.__init__(self)
        self.csocket = clientsocket
        print(get_time() + " - Nouvelle connection ajoutée: " + str(clientAddress))
    def run(self):
        msg = ['', '', '']
        print(get_time() + " - Connection depuis : " + str(clientAddress))
        exit_var = 0
        while exit_var == 0:
            msg = receive_data(self)
            if msg[0] == 'log':
                exit_var = log_in(self, msg)
            elif msg[0] == 'crt':
                exit_var = create_account(self, msg)

        print(get_time() + " - Client depuis " + str(clientAddress) + " c\'est déconnecté...")

create_tables()
LOCALHOST = "127.0.0.1"
PORT = 8080
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((LOCALHOST, PORT))
print(get_time() + " - Serveur lancé")
print(get_time() + " - En attente des requêtes clientes")

while True:                 #Boucle principale
    server.listen(1)
    clientsock, clientAddress = server.accept()
    newthread = ClientThread(clientAddress, clientsock)
    newthread.start()