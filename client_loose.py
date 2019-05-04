import socket, time, getpass, os, pickle
SERVER = "127.0.0.1"
PORT = 8080
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((SERVER, PORT))
out_data = [0, 0, 0]

def clear():
	os.system('clear||cls')

def receive_data(client):
    data = client.recv(2048)
    return pickle.loads(data)

def send_data(client, tdata):
    data = pickle.dumps(tdata)
    client.sendall(data)

def ask_credentials_crt_cpt():
	usr = input('Email > ')
	psw = getpass.getpass('Password > ')
	out_data[0], out_data[1], out_data[2] = 'crt', usr, psw
	send_data(client, out_data)
	server_asw = receive_data(client)
	if server_asw[0] == 'log_fine':
		print('Account creation successful !')
		time.sleep(2)
		clear()
	elif server_asw[0] == 'log_shit':
		print('Account creation unsuccessful ! (E-mail maybe already in use)')
		time.sleep(2)
		clear()
	else:
		print('Seems broken...')
		time.sleep(2)
		clear()

def ask_credentials_log_cpt():
	usr = input('Email > ')
	psw = getpass.getpass('Password > ')
	out_data[0], out_data[1], out_data[2] = 'log', usr, psw
	send_data(client, out_data)
	server_asw = receive_data(client)
	if server_asw[0] == 'log_fine':
		print('Login successful !')
		time.sleep(2)
		clear()
	elif server_asw[0] == 'log_shit':
		print('Login unsuccessful !')
		time.sleep(2)
		clear()
	else:
		print('Seems broken...')
		time.sleep(2)
		clear()

def menu():
	asw = ''
	possibilitys = ['create', 'login']
	while asw.lower() not in possibilitys:
		print('Would you like to create an account or login ?')
		print('create/login')
		asw = input('> ')
		clear()
	if asw == 'create':
		ask_credentials_crt_cpt()
	else:
		ask_credentials_log_cpt()

clear()
menu()

client.close()