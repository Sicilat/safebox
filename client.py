import socket, time, getpass, os, pickle, hashlib, re, string, random
SERVER = "127.0.0.1"
PORT = 8080
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((SERVER, PORT))
out_data = [0, 0, 0, 0, 0]

def clear():					#Fonction pour nettoyer le terminal
	os.system('clear||cls')

def receive_data(client):		#Reçoie les données du serveur
    data = client.recv(2048)
    return pickle.loads(data)

def send_data(client, tdata):	#Envoie les données au serveur
    data = pickle.dumps(tdata)
    client.sendall(data)

def menu():							#Gérer le menu de connexion et de création
	asw = 0
	while asw not in [1, 2]:
		print('Bienvenue sur Safebox')
		print('Voulez-vous créer un compte ou vous identifier ?')
		print('1 - Créer')
		print('2 - Identification')
		asw = int(input('> '))
		clear()
	if asw == 1:
		ask_credentials_crt_cpt()
	else:
		ask_credentials_log_cpt()

def ask_credentials_crt_cpt():			#Gérer la création de compte
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

def ask_credentials_log_cpt():			#Gérer la connexion au compte
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

def logged_menu(out_data):			#Gérer le menu principal
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

def password_menu(out_data):	#Gérer le menu des mots de passe
	while True:
		clear()
		out_data[0] = 'psw'
		send_data(client, out_data)
		time.sleep(1)
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
			Verif = False
			size = 0

			while not Verif:								#Boucle pour définir le mot de passe tant que le mot de passe est incorrect.
				print("Choisissez votre mode d'entrée de mot passe")
				choixGen="null"
			
				while choixGen != "r" and choixGen != "m":	#Choix du mode d'entrée.
					print("Aléatoire : r | Manuel : m")
					choixGen = str(input())
			
				if choixGen == "r":
					print("Choisissez la taille de votre mot de passe :")
					while size >= 21 or size <= 9:
						size = int(input())
						mdp = genMdp(size)					#Appel de la fonction de génération.
				elif choixGen == "m":
					print("Votre mot de passe doit contrenir au moins:")
					print("	>2 majucules")
					print("	>2 chiffres")
					print("	>1 caractère spécial")
					print("	>Une taille de" , size , "caractères.")
			
					print("Saisissez votre mot de passe :")
					mdp=str(input('Mot de passe à sauvegarder > '))						#Input du mot de passe en manuel.
			
				Verif = verifContraintes(mdp) 				#Vérification du mot de passe.
				
				if Verif:
					print("Mot de passe correct.")
				else:
					print("Mot de passe incorrect.")


			out_data[0] = 'psw_add'
			out_data[3] = mdp
			out_data[4] = input('À propos > ')
			clear()
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

def genMdp(size=10):	#Fonction de génération de mot de passe de taille "size"
	
	if size <= 20 and size >= 10:	#Le mot de passe généré doit contenir entre 10 et 20 charactères (contrainte arbitraire)
		sourceChar = string.ascii_letters + string.digits + string.punctuation	#Définition de sourceChar servant de ressource contenant des lettres
																				#minuscules, majuscules, des chiffres et des charactères spéciaux
		mdp = random.choice(string.ascii_lowercase)			#Création de la variable mdp et ajout d'une lettre minuscule aléatoire
		mdp = mdp + random.choice(string.ascii_lowercase)	#Ajout d'une deuxième lettre minuscule aléatoire
		mdp = mdp + random.choice(string.ascii_uppercase)		#Ajout de deux lettres majuscules
		mdp = mdp + random.choice(string.ascii_uppercase)		#aléatoires à mdp
		mdp = mdp + random.choice(string.digits)			#Ajout de deux chiffres
		mdp = mdp + random.choice(string.digits)			#aléatoires à mdp
		mdp = mdp + random.choice(string.punctuation)			#Ajout d'un caractère spécial
		for i in range(size-7):					#Remplissage des caractères restants depuis la
		    mdp += random.choice(sourceChar)	#ressource sourceChar (et de manière aléatoire)
		mdpList = list(mdp)							#
		random.SystemRandom().shuffle(mdpList)		#Mélange aléatoire du mot de passe
		mdp = ''.join(mdpList)						#
		return mdp		#Sortie de la variable mdp hors de la fonction
	else :
		print("Le mot de passe doit contenir entre 10 et 20 caractères.")	#Message d'erreur si la taille choisie ne resecte pas la condition

def verifContraintes(mdp):	#Fonction de vérification des contraintes du mot de passe 
		
	nbr_maj = 0						# Définition d'un compteur de majuscules dans le mot de passe.
	nbr_min = 0						# Définition d'un compteur de minuscules dans le mot de passe.
	compteurNombres = 0				# Définition d'un compteur de chiffres dans le mot de passe.									# Définition d'une variable mot de passe.


	# Analyse des conditions #

	specialChars = len(mdp) - len( re.findall('[\w]', mdp) )	# On détermine le nombre de caractères spéciaux dans mdp.
	if specialChars < 1:
		print("Le mot de passe doit contenir au moins un caractère spécial : # $ & ^ @!" )
		sp_char = False
	else:
		sp_char = True

	for c in mdp:									#
		if c.isdigit():								# } On initialise un compteur qui dénombre les chiffres dans le mot de de passe.
			compteurNombres = compteurNombres+1		#
	if compteurNombres <= 1:						#
		print(("Chiffres insuffisants!"))			# } Si il n'y a pas assez de nombres : "Nombres insuffisants".
		nb_chiffre = False
	else:
		nb_chiffre = True							


	for j in mdp:									#
		if j.lower() != j:							# } On initialise un compteur qui dénombre les majuscules dans le mot de de passe.
			nbr_maj += 1							#
	if nbr_maj < 2:									#
		print(("Majuscules insuffisantes!"))
		nb_maj = False
	else :		
		nb_maj = True								# } Si il n'y a pas assez de majuscules : "Majuscules inssuffisantes".
													#

	for j in mdp:									#
		if j.upper() != j:							# } On initialise un compteur qui dénombre les majuscules dans le mot de de passe.
			nbr_min += 1							#
	if nbr_min < 2:									#
		print(("Minuscules insuffisantes!"))
		nb_min = False
	else :		
		nb_min = True								# } Si il n'y a pas assez de majuscules : "Majuscules inssuffisantes".
													#


	if len(mdp)<=9:									#
		print("Mot de passe trop court!") 			# } On teste si le mot de passe est assez long.
		lenMdp = False
	elif len(mdp)>=21:								#
		print("Mot de passe trop long!")			# } On teste si le mot de passe est assez court.
		lenMdp = False								#
	else: 
		lenMdp = True



	# Validation du mot de passe après analyse des contraintes #
	if sp_char and nb_chiffre and nb_maj and nb_min and	lenMdp:							# Si le mot de passe est correct.

		Verif = True
	else:
		Verif = False
	return Verif		# Return si le mot de passe est correct ou non.


clear()
menu()

client.close()
