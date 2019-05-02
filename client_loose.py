import socket, time, getpass, os
SERVER = "127.0.0.1"
PORT = 8080
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((SERVER, PORT))
out_data = [0, 0, 0]

def clear():
	os.system('clear||cls')

def ask_credentials_crt_cpt():
	client.sendall(bytes(out_data[0],'UTF-8'))
	time.sleep(0.1)
	client.sendall(bytes(out_data[1],'UTF-8'))

def ask_credentials_log_cpt():
	usr = input('Username > ')
	psw = getpass.getpass('Password > ')
	out_data[0], out_data[1], out_data[2] = 'log', usr, psw
	client.sendall(bytes(out_data[0],'UTF-8'))
	time.sleep(0.1)
	client.sendall(bytes(out_data[1],'UTF-8'))
	time.sleep(0.1)
	client.sendall(bytes(out_data[2],'UTF-8'))
	time.sleep(0.1)
	in_data =  client.recv(2048)
	server_asw = in_data.decode()
	if server_asw == 'log_fine':
		print('Login successful !')
		time.sleep(2)
		clear()
	elif server_asw == 'log_shit':
		print('Login unsuccessful !')
		time.sleep(2)
		clear()
	else:
		print('Seems broken...')
		time.sleep(2)
		clear()

def menu():
	asw = ''
	possibility = ['create', 'login']
	while asw.lower() not in possibility:
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