import random
import string
import re
import os


# PARTIE DEFINITION DES FONCTIONS

def genMdp(size=10): #Fonction de génération de mot de passe de taille "size".
	
	if size <= 20 and size >= 10:
		sourceChar = string.ascii_letters + string.digits + string.punctuation
		mdp = random.choice(string.ascii_lowercase)
		mdp = mdp + random.choice(string.ascii_uppercase)
		mdp = mdp + random.choice(string.digits)
		mdp = mdp + random.choice(string.digits)
		mdp = mdp + random.choice(string.punctuation)
		for i in range(size-5):
		    mdp += random.choice(sourceChar)
		mdpList = list(mdp)
		random.SystemRandom().shuffle(mdpList)
		mdp = ''.join(mdpList)
		return mdp
	else :
		print("Le mot de passe doit contenir entre 10 et 20 caractères.")

def verifContraintes(mdp): #Fonction de vérification des contraintes du mot de passe 
		
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


# PARTIE EXECUTION DU PROGRAMME #

size = 0
choixGen="null"
Verif = False

while not Verif:								#Boucle pour définir le mot de passe tant que le mot de passe est incorrect.
	print("Choisissez votre mode d'entrée de mot passe")

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
		mdp=str(input())						#Input du mot de passe en manuel.

	Verif = verifContraintes(mdp) 				#Vérification du mot de passe.
	
	if Verif:
		print("Mot de passe correct.")
	else:
		print("Mot de passe incorrect.")


print(mdp)