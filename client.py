import socket, time, getpass, os, pickle, hashlib
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
		print('Menu des mots de passe')
		print('1 - Ajouter un mot de passe')
		print('2 - Supprimer un mot de passe')
		print('3 - Quitter')
		print('')
		if len(psw_data) > 0:
			for row in psw_data:
				print("ID-" + str(row[2]) + " | " + str(row[3]) + "      " + str(row[4]))
		else:
			print('Aucun mot de passe sauvegardé !')
		print ('')
		asw = int(input('> '))
		if asw == 1:
			out_data[0] = 'psw_add'
			clear()
			out_data[3] = input('Mot de passe à sauvegarder > ')
			out_data[4] = input('À propos > ')
			send_data(client, out_data)
			time.sleep(1)
		elif asw == 2:
			out_data[0] = 'dlt'
			print('Choisissez l\'ID du mot de passe à supprimer')
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
			print('1 - Liste des mots de passe')
			print('2 - Supression du compte')
			print('3 - Quitter')
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
	psw = str.encode(getpass.getpass('Mot de passe > '))
	psw = hashlib.sha512(psw).hexdigest()
	out_data[0], out_data[1], out_data[2] = 'crt', usr, psw
	send_data(client, out_data)
	server_asw = receive_data(client)
	if server_asw[0] == 'log_fine':
		print('Succès de la création du compte !')
		time.sleep(2)
		clear()
		menu()
	elif server_asw[0] == 'log_shit':
		print('Èchec de la création du compte ! (L\'E-mail est peut-être déjà utilisée)')
		time.sleep(2)
		clear()
		menu()
	else:
		print('C\'est cassé...')
		time.sleep(2)
		clear()
		menu()

def ask_credentials_log_cpt():
	usr = input('Email > ')
	psw = str.encode(getpass.getpass('Mot de passe > '))
	psw = hashlib.sha512(psw).hexdigest()
	out_data[0], out_data[1], out_data[2] = 'log', usr, psw
	send_data(client, out_data)
	server_asw = receive_data(client)
	if server_asw[0] == 'log_fine':
		print('Identification réussie !')
		time.sleep(2)
		clear()
		logged_menu(out_data)
	elif server_asw[0] == 'log_shit':
		print('Èchec de l\'identification !')
		time.sleep(2)
		clear()
		menu()
	else:
		print('C\'est cassé...')
		time.sleep(2)
		clear()
		menu()

def menu():
	asw = 0
	while asw not in [1, 2]:
		print('Voulez-vous créer un compte ou vous identifier ?')
		print('1 - Créer')
		print('2 - Identification')
		asw = int(input('> '))
		clear()
	if asw == 1:
		ask_credentials_crt_cpt()
	else:
		ask_credentials_log_cpt()

clear()
menu()

client.close()