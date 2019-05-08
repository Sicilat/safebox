import socket, time, getpass, os, pickle
SERVER = "127.0.0.1"
PORT = 8080
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((SERVER, PORT))
out_data = [0, 0, 0, 0, 0]

def clear():
	os.system('clear||cls')

def receive_data(client):
    data = client.recv(2048)
    return pickle.loads(data)

def send_data(client, tdata):
    data = pickle.dumps(tdata)
    client.sendall(data)

def password_menu(out_data):
	while True:
		clear()
		out_data[0] = 'psw'
		send_data(client, out_data)
		psw_data = receive_data(client)
		print('Password menu')
		print('1 - Add a password')
		print('2 - Delete a password')
		print('3 - Quit')
		print('')
		if len(psw_data) > 0:
			for row in psw_data:
				print("ID-" + str(row[2]) + " | " + str(row[3]) + "      " + str(row[4]))
		else:
			print('No password is saved !')
		print ('')
		asw = int(input('> '))
		if asw == 1:
			out_data[0] = 'psw_add'
			clear()
			out_data[3] = input('Password to save > ')
			out_data[4] = input('About this > ')
			send_data(client, out_data)
			time.sleep(1)
		elif asw == 2:
			out_data[0] = 'dlt'
			print('Choose the ID of the password to delete')
			out_data[3] = int(input('> '))
			send_data(client, out_data)
			time.sleep(1)
		elif asw == 3:
			clear()
			client.close()
			exit()

def logged_menu(out_data):
	while True:
		print('Compte : ' + out_data[1])
		print('1 - Liste des mots de passe')
		print('2 - Supression du compte')
		print('3 - Quitter')
		asw = int(input('> '))
		while asw not in [1, 2, 3]:
			clear()
			print('Compte : ' + out_data[1])
			print('1 - Supression du compte')
			print('2 - Quitter')
			asw = int(input('> '))
		clear()
		if asw == 2:
			out_data[0] = 'spr'
			send_data(client, out_data)
			print('Compte supprimé !')
			client.close()
			time.sleep(2)
			clear()
			exit()
		elif asw == 1:
			clear()
			password_menu(out_data)
		else:
			break

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
		menu()
	elif server_asw[0] == 'log_shit':
		print('Account creation unsuccessful ! (E-mail maybe already in use)')
		time.sleep(2)
		clear()
		menu()
	else:
		print('Seems broken...')
		time.sleep(2)
		clear()
		menu()

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
		logged_menu(out_data)
	elif server_asw[0] == 'log_shit':
		print('Login unsuccessful !')
		time.sleep(2)
		clear()
		menu()
	else:
		print('Seems broken...')
		time.sleep(2)
		clear()
		menu()

def menu():
	asw = 0
	while asw not in [1, 2]:
		print('Would you like to create an account or login ?')
		print('1 - Create')
		print('2 - Login')
		asw = int(input('> '))
		clear()
	if asw == 1:
		ask_credentials_crt_cpt()
	else:
		ask_credentials_log_cpt()

clear()
menu()

client.close()