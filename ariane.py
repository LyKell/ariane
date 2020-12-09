from upemtk import *
from time import *
import os

# Voisins HDBG: laby[2*(i-1)+1][2*j+1]	laby[2*i+1][2*(j+1)+1]	laby[2*(i+1)+1][2*j+1]	laby[2*i+1][2*(j-1)+1]
# Mur HDBG: 	laby[2*i][2*j+1]		laby[2*i+1][2*j+2]		laby[2*i+2][2*j+1]		laby[2*i+1][2*j]

def ouvrirFichier(repertoire, fichier):
	"""
	Fonction permettant d'ouvrir un fichier, et de séparer les lignes
	pour pouvoir l'utiliser comme liste de liste plus tard.

	repertoire: str, Répertoire du labyrinthe
	fichier: str, Nom du fichier qui correspond au labyrinthe.
	"""
	if repertoire == "Classique":
		file = open("maps/" + fichier, "r").read().split('\n')
	else:
		file = open("maps/" + repertoire + "/" + fichier, "r").read().split('\n')

	return file


# def choixLabyrinthe():
# 	"""
# 	Fonction définissant la liste des labyrinthes du jeu et le choix du labyrinthe
# 	"""
# 	listeLaby = {1: "labyrinthe1.txt", 2: "labyrinthe2.txt", 3: "labyrinthe3.txt", 4: "labyrinthe4.txt",
# 					5: "labyrinthe5.txt", 6: "sandbox.txt", 7: "big1.txt", 8: "big2.txt",
# 					9: "small1.txt", 10: "small2.txt", 11: "small3.txt", 12: "small4.txt",
# 					13: "defi0.txt", 14: "defi1.txt", 15: "defi2.txt", 16: "defi3.txt"}

# 	print("Thésée est perdu dans l'un de ces labyrinthes conçus par Dédale pour enfermé le Minotaure !")
# 	print(listeLaby)
# 	choix = int(input("Lequel souhaitez vous explorer ?\n"))

# 	fichier = ouvrirFichier(listeLaby, choix)

# 	return fichier


# def choixDesign(design):
# 	"""
# 	Fonction permettant de choisir le thème du jeu
# 	"""
# 	theme = {1: "Original", 2: "Crypt of the NecroDancer"}
# 	print("Les univers sont nombreux et variés. Vous pouvez vous plonger dans l'un de ceux-là:", theme)
# 	choix = int(input("Dans quel univers souhaitez-vous vous plonger ?\n"))
# 	design = theme[choix]

# 	return design


def creerLabyrinthe(fichier):
	"""
	Fonction créant le labyrinthe en liste de liste

	fichier: nom du fichier qui correspond au labyrinthe. 
	"""
	laby = []
	i = 0

	for lines in fichier:
		laby.append([])
		for elem in lines:
			laby[i].append(elem)
		i += 1

	laby.pop(0)	# On retire la taille du labyrinthe
	laby.pop()	# On retire l'espace de fin de fichier
	return laby


def positionPersos(laby):
	"""
	Fonction renvoyant un dictionnaire qui contient la position de chaque personnage
	On utilise append au cas où il y a plusieurs même personnage, typiquement les minotaures

	laby: list, Contient le labyrinthe choisi par le joueur
	"""
	perso = {}
	for ligne in laby:
		for elem in ligne:
			if elem.isalpha():
				x = (laby.index(ligne)-1) // 2
				y = (ligne.index(elem)-1) // 2
				
				if elem in perso:	# La clé existe déjà dans le dictionnaire
					perso[elem].append((x, y))	# On rajoute les coordonnées du personnage

				else:				# La clé n'existe pas
					perso[elem] = [(x, y)]	# On ajoute les coordonnées du personnage
					
	return perso


def drawLaby(laby, taille_case, design, perso):
	"""
	Fonction dessinant le labyrinthe et renvoyant les coordonnées de la Porte qu'on utilisera dans le solveur
	Contrairement aux vidéos, dans notre programme, on ne se contente pas de simplement
	superposer les images d'Ariane et Thésée quand ils sont ensembles. On a crée une nouvelle image qui contient Ariane et Thésée
	pour pas que les personnages soient juste superposés, mais pour qu'ils soient côte à côte.	-> Sprite "ensemble.png"
	
	laby: list, Contient le labyrinthe choisi par le joueur
	taille_case: int, Taille des cases
	design: str, Dossier contenant les images nécessaires pour l'affichage du jeu
	perso: dict, Contient la position des entités
	"""
	for i in range(len(laby)):
		for j in range(len(laby)):
			if laby[i][j] == "-":
				ligne((j-1)*taille_case, i*taille_case, (j+1)*taille_case, i*taille_case, couleur="black", epaisseur=1, tag='')

			if laby[i][j] == "|":
				ligne(j*taille_case, (i-1)*taille_case, j*taille_case, (i+1)*taille_case, couleur="black", epaisseur=1, tag='')

			if laby[i][j] == "A":
				image(j*taille_case, i*taille_case, "media/"+design+"/ariane.png", ancrage="center")

			if laby[i][j] == "T":
				image(j*taille_case, i*taille_case, "media/"+design+"/thesee.png", ancrage="center")

			if laby[i][j] == "H":
				image(j*taille_case, i*taille_case, "media/"+design+"/minoH.png", ancrage="center")

			if laby[i][j] == "V":
				image(j*taille_case, i*taille_case, "media/"+design+"/minoV.png", ancrage="center")

			if laby[i][j] == "E":
				image(j*taille_case, i*taille_case, "media/"+design+"/ensemble.png", ancrage="center")

			if laby[i][j] == "P" and "E" not in perso:		# Porte verrouillée
				image(j*taille_case, i*taille_case, "media/"+design+"/porteL.png", ancrage="center")

			elif laby[i][j] == "P" and perso["E"] == perso["P"]:	# Ariane et Thésée sur la porte
				image(j*taille_case, i*taille_case, "media/"+design+"/victoire.png", ancrage="center")

			elif laby[i][j] == "P" and perso["E"] != perso["P"]:	# Porte déverouillée
				image(j*taille_case, i*taille_case, "media/"+design+"/porte.png", ancrage="center")


def moveQui(laby, perso, touche):
	"""
	Fonction permettant de déplacement soit Ariane, soit Ariane et Thésée, en fonction de la situation

	laby: list, Contient le labyrinthe choisi par le joueur
	perso: dict, Dictionnaire contenant les coordonnées de chaques personnages et de la porte
	touche: str, Touche sur laquelle le joueur a appuyé
	"""
	if "E" in perso:
		laby, perso = movePerso(laby, perso, touche, "E")
		perso["A"] = perso["E"]
		perso["T"] = perso["E"]
		# laby, perso = mino(laby, perso, "V")
		# laby, perso = mino(laby, perso, "H")
		

	elif "A" in perso:
		laby, perso = movePerso(laby, perso, touche, "A")
		# laby, perso = mino(laby, perso, "V")
		# laby, perso = mino(laby, perso, "H")

	return laby, dict(perso)


def movePerso(laby, perso, touche, char):
	"""
	Fonction permettant de bouger les personnages

	laby: list, Contient le labyrinthe choisi par le joueur
	perso: dict, Dictionnaire contenant les coordonnées de chaques personnages et de la porte
	touche: str, Touche sur laquelle le joueur a appuyé
	char: str: Personnage à déplacer - A: Ariane; E: Ariane et Thésée
	"""
	i = perso[char][0][0]
	j = perso[char][0][1]
	
	if touche == "Up":
		if laby[2*i][2*j+1] == " " and (laby[2*(i-1)+1][2*j+1] == " " or (laby[2*(i-1)+1][2*j+1] == "P" and (char == "A" or char == "E"))):				# On vérifie si le mur du haut et la case du haut sont vides
			perso[char] = [(i-1, j)]													# On change les coordonnées du perso
			laby[2*i+1][2*j+1], laby[2*(i-1)+1][2*j+1] = " ", laby[2*i+1][2*j+1]	# On déplace le perso en changeant modifiant les cases du labyrinthe

	elif touche == "Down":
		if laby[2*i+2][2*j+1] == " " and (laby[2*(i+1)+1][2*j+1] == " " or (laby[2*(i+1)+1][2*j+1] == "P" and (char == "A" or char == "E"))):				# On vérifie si le mur du bas et la case du bas sont vides
			perso[char] = [(i+1, j)]
			laby[2*i+1][2*j+1], laby[2*(i+1)+1][2*j+1] = " ", laby[2*i+1][2*j+1]

	elif touche == "Right":
		if laby[2*i+1][2*j+2] == " " and (laby[2*i+1][2*(j+1)+1] == " " or (laby[2*i+1][2*(j+1)+1] == "P" and (char == "A" or char == "E"))):				# On vérifie si le mur de droite et la case de droite sont vides
			perso[char] = [(i, j+1)]
			laby[2*i+1][2*j+1], laby[2*i+1][2*(j+1)+1] = " ", laby[2*i+1][2*j+1]

	elif touche == "Left":
		if laby[2*i+1][2*j] == " " and (laby[2*i+1][2*(j-1)+1] == " " or (laby[2*i+1][2*(j-1)+1] == "P" and (char == "A" or char == "E"))):				# On vérifie si le mur de gauche et la case de gauche sont vides
			perso[char] = [(i, j-1)]
			laby[2*i+1][2*j+1], laby[2*i+1][2*(j-1)+1] = " ", laby[2*i+1][2*j+1]

	return laby, dict(perso)


def mino(laby, perso, char):
	"""
	Fonction permettant de déplacer les minotaures

	laby: list, Contient le labyrinthe choisi par le joueur
	perso: dict, Dictionnaire contenant les coordonnées de chaques personnages et de la porte
	char: str: Personnage à déplacer - H: Minotaure Vertical; V: Minotaure Horizontal
	"""
	for coord in range(len(perso[char])):
		i = perso[char][coord-1][0]
		j = perso[char][coord-1][1]

	
		# Minotaures hoizontaux
		if char == "H":
			if laby[2*i][2*j+1] == " " and laby[2*(i-1)+1][2*j+1] in [" ", "A", "T", "E"] and perso["A"][0][1] == j and perso["A"][0][0] < i:	# On vérifie que le minotaure peut bouger
				while laby[2*i][2*j+1] == " " and laby[2*(i-1)+1][2*j+1]  in [" ", "A", "T", "E"] and perso["A"][0][0] < i:		# On déplace le minotaure
					perso[char][coord-1] = (i-1, j)
					laby[2*i+1][2*j+1], laby[2*(i-1)+1][2*j+1] = " ", laby[2*i+1][2*j+1]
					i -= 1

			elif laby[2*i+2][2*j+1] == " " and laby[2*(i+1)+1][2*j+1] in [" ", "A", "T", "E"] and perso["A"][0][1] == j and perso["A"][0][0] > i:
				while laby[2*i+2][2*j+1] == " " and laby[2*(i+1)+1][2*j+1] in [" ", "A", "T", "E"] and perso["A"][0][0] > i:
					perso[char][coord-1] = (i+1, j)
					laby[2*i+1][2*j+1], laby[2*(i+1)+1][2*j+1] = " ", laby[2*i+1][2*j+1]
					i += 1

			elif laby[2*i+1][2*j] == " " and laby[2*i+1][2*(j-1)+1] in [" ", "A", "T", "E"] and perso["A"][0][1] < j:
				while laby[2*i+1][2*j] == " " and laby[2*i+1][2*(j-1)+1] in [" ", "A", "T", "E"] and perso["A"][0][1] < j:
					perso[char][coord-1] = (i, j-1)
					laby[2*i+1][2*j+1], laby[2*i+1][2*(j-1)+1] = " ", laby[2*i+1][2*j+1]
					j -= 1
				
			elif laby[2*i+1][2*j+2] == " " and laby[2*i+1][2*(j+1)+1] in [" ", "A", "T", "E"] and perso["A"][0][1] > j :
				while laby[2*i+1][2*j+2] == " " and laby[2*i+1][2*(j+1)+1] in [" ", "A", "T", "E"] and perso["A"][0][1] > j:
					perso[char][coord-1] = (i, j+1)
					laby[2*i+1][2*j+1], laby[2*i+1][2*(j+1)+1] = " ", laby[2*i+1][2*j+1]
					j += 1

		# Minotaures verticaux
		elif char == "V":
			if laby[2*i+1][2*j] == " " and laby[2*i+1][2*(j-1)+1] in [" ", "A", "T", "E"] and perso["A"][0][0] == i and perso["A"][0][1] < j:
				while laby[2*i+1][2*j] == " " and laby[2*i+1][2*(j-1)+1] in [" ", "A", "T", "E"] and perso["A"][0][0] == i and perso["A"][0][1] < j:
					perso[char][coord-1] = (i, j-1)
					laby[2*i+1][2*j+1], laby[2*i+1][2*(j-1)+1] = " ", laby[2*i+1][2*j+1]
					j -= 1
				
			elif laby[2*i+1][2*j+2] == " " and laby[2*i+1][2*(j+1)+1] in [" ", "A", "T", "E"] and perso["A"][0][0] == i and perso["A"][0][1] > j:
				while laby[2*i+1][2*j+2] == " " and laby[2*i+1][2*(j+1)+1] in [" ", "A", "T", "E"] and perso["A"][0][0] == i and perso["A"][0][1] > j:
					perso[char][coord-1] = (i, j+1)
					laby[2*i+1][2*j+1], laby[2*i+1][2*(j+1)+1] = " ", laby[2*i+1][2*j+1]
					j += 1
			
			elif laby[2*i][2*j+1] == " " and laby[2*(i-1)+1][2*j+1] in [" ", "A", "T", "E"] and perso["A"][0][0] < i:
				while laby[2*i][2*j+1] == " " and laby[2*(i-1)+1][2*j+1] in [" ", "A", "T", "E"] and perso["A"][0][0] < i: 
					perso[char][coord-1] = (i-1, j)
					laby[2*i+1][2*j+1], laby[2*(i-1)+1][2*j+1] = " ", laby[2*i+1][2*j+1]
					i -= 1
				
			elif laby[2*i+2][2*j+1] == " " and laby[2*(i+1)+1][2*j+1] in [" ", "A", "T", "E"] and perso["A"][0][0] > i:
				while laby[2*i+2][2*j+1] == " " and laby[2*(i+1)+1][2*j+1] in [" ", "A", "T", "E"] and perso["A"][0][0] > i:
					perso[char][coord-1] = (i+1, j)
					laby[2*i+1][2*j+1], laby[2*(i+1)+1][2*j+1] = " ", laby[2*i+1][2*j+1]
					i += 1

	return laby, dict(perso)
			

def arianeEtThesee(laby, perso, taille):
	"""
	Fonction permettant de réunir Ariane et Thésée
	Dans le cas où on vérifie à droite et en bas, il faut faire attention à ce que la case de droite et du bas, respectivement,
	existent bien dans le tableau. Sinon on a un IndexError

	laby: list, Contient le labyrinthe choisi par le joueur
	perso: dict, Dictionnaire contenant les coordonnées de chaques personnages et de la porte
	taille: int, Taille du plateau. Ne pas confondre avec largeur_plateau et hauteur_plateau
	"""
	for ligne in laby:
		if "A" in ligne:			# On récupère les coordonnées d'Ariane
			i, j = perso["A"][0][0], perso["A"][0][1]

			if ((laby[2*(i-1)+1][2*j+1] == "T" and laby[2*i][2*j+1] == " ")		# On vérifie en haut
					or (2*i+1 in range(taille) and 2*(j+1)+1 in range(taille) and laby[2*i+1][2*(j+1)+1] == "T" and laby[2*i+1][2*j+2] == " ")	# On vérifie à droite
					or (2*(i+1)+1 in range(taille) and 2*j+1 in range(taille) and laby[2*(i+1)+1][2*j+1] == "T" and laby[2*i+2][2*j+1] == " ")	# On vérifie en bas
					or (laby[2*i+1][2*(j-1)+1] == "T" and laby[2*i+1][2*j] == " ")):	# On vérifie à gauche
				perso["E"], perso["T"] = perso["A"], perso["A"]

				for ligne in laby:
					if "T" in ligne:
						theseeX = laby.index(ligne)		# On récupère les coordonnées de Thésée pour pouvoir le déplacer sur Ariane
						theseeY = ligne.index("T")

				laby[2*i+1][2*j+1], laby[theseeX][theseeY] = "E", " "



	return laby, dict(perso)


def victoire(laby, perso, victory = None):
	"""
	Fonction vérifiant si la partie est gagnée ou perdue
	"""
	if perso["A"] == perso["T"] == perso["P"]:	# Ariane et Thésée sur la Porte
		victory = True

	elif perso["A"][0] in perso["H"] or perso["A"][0] in perso["V"] or perso["T"][0] in perso["H"] or perso["T"][0] in perso["V"]:	# Ariane et/ou Thésée tué
		victory = False

	return victory






# casesVoisines = [([2*(i-1)+1][2*j+1]), ([2*i+1][2*(j+1)+1]), ([2*(i+1)+1][2*j+1]), ([2*i+1][2*(j-1)+1])]
# mursVoisins = [([2*i][2*j+1]), ([2*i+1][2*j+2]), ([2*i+2][2*j+1]), ([2*i+1][2*j])]
# positionsVoisines = [(i-1, j), (i, j+1), (i+1, j), (i, j-1)]






# Les quatre fonctions suivantes ne servent qu'à la réalisation du solveur

def drawMur(laby, taille_case, perso):
	"""
	Fonction dessinant les murs et la porte
	Cette fonction est utilisée dans le solveur

	laby: list, Contient le labyrinthe
	"""
	for i in range(len(laby)):
		for j in range(len(laby)):
			if laby[i][j] == "-":
				ligne((j-1)*taille_case, i*taille_case, (j+1)*taille_case, i*taille_case, couleur="black", epaisseur=1, tag='')

			if laby[i][j] == "|":
				ligne(j*taille_case, (i-1)*taille_case, j*taille_case, (i+1)*taille_case, couleur="black", epaisseur=1, tag='')


def actualiserPerso(gameState, taille_case, perso):
	"""
	Fonction permettant d'afficher les personnages
	Cette fonction est utilisée dans le solveur

	gameState: dict, Contient la position des personnages uniquement
	"""
	i, j = gameState[0]
	image(j*taille_case, i*taille_case, "media/Original/ariane.png", ancrage="center")

	i, j = gameState[1]
	image((2*j+1)*taille_case, (2*i+1)*taille_case, "media/Original/thesee.png", ancrage="center")

	i, j = gameState[2]
	image((2*j+1)*taille_case, (2*i+1)*taille_case, "media/Original/minoH.png", ancrage="center")

	i, j = gameState[3]
	image((2*j+1)*taille_case, (2*i+1)*taille_case, "media/Original/minoV.png", ancrage="center")

	i, j = gameState[4]
	image(j*taille_case, i*taille_case, "media/Original/porte.png", ancrage="center")
	coordPorte = (i, j)

	if "E" in perso:
		coordE = ((perso["E"][0][0]-1)//2, (perso["E"][0][1]-1)//2)
		coord = tuple(gameState)
		gameState = coord + (coordE,)

	return coordPorte


def gameState(laby):
	"""
	Fonction qui renvoie une liste dans laquelle se trouve la position de chaque entité
	Cette liste est utilisée dans le solveur
	"""
	gameState = {}
	for i in range(len(laby)):
		for j in range(len(laby)):
			if laby[i][j] == "A":
				gameState[0] = (i, j)

			if laby[i][j] == "T":
				gameState[1] = (i, j)

			if laby[i][j] == "V":
				gameState[2] = (i, j)

			if laby[i][j] == "H":
				gameState[3] = (i, j)

			if laby[i][j] == "P":
				gameState[4] = (i, j)

			if laby[i][j] == "E":
				gameState[5] = (i, j)

	return gameState


def solveur(laby, C, perso, taille_case, config = set()):
	"""
	Solveur

	laby: lst, Contient l'intégralité du labyrinthe
	C: dict ou set, La configuration actuelle du jeu
	perso: dict, Contient les coordonnées des entités du jeu
	taille_case: int, Taille du labyrinthe
	config: set, Ensemble contenant toutes les configurations déjà visitées
	"""
	efface_tout()
	drawMur(laby, taille_case, perso)	# On dessine les murs
	coordPorte = actualiserPerso(C, taille_case, perso)		# On dessine toutes les entités tout en récupérant les coordonnées de la porte
	sleep(1/20)
	mise_a_jour()
	coordAriane = ((C[0][0]-1)//2, (C[0][1]-1)//2)		# On convertit les coordonnées d'Ariane, de Thésée et de la Porte
	coordThesee = ((C[3][0]-1)//2, (C[3][1]-1)//2)
	porte = ((coordPorte[0]-1)//2, (coordPorte[1]-1)//2)

	if coordAriane == C[1] == porte:	# Cas d'arrêt n°1: Si Ariane et Thésée sont sur la Porte
		return True

	elif coordAriane == C[3] or coordAriane == C[2] or C[1] == C[3] or C[1] == C[2]:	# Cas d'arrêt n°2: Si Ariane et/ou Thésée sont tués par les Minotaures
		return False

	else:
		config.add(tuple(C))	# On ajoute la configuration actuelle à l'ensemble des configurations déjà visitées
		(i, j) = C[0]	# Coordonnées d'Ariane par rapport à l'intégralité du labyrinthe

		casesVoisines = [(i-2, j), (i+2, j), (i, j-2), (i, j+2)]	# Liste des cases voisines
		mursVoisins = [(i-1, j), (i+1, j), (i, j-1), (i, j+1)]		# Liste des murs voisins
		toucheClavier = ["Up", "Down", "Left", "Right"]				# Liste des touches directionnelles

		for voisins, murs, touche in zip(casesVoisines, mursVoisins, toucheClavier):	# On vérifie pour chaque positions voisines et chaque murs voisins. Zip() permet, dans notre cas, de faire une boucle for
			if 0 <= voisins[0] <= len(laby) and 0 <= voisins[1] <= len(laby):		# On vérifie que les cases voisines sont bien dans le labyrinthe pour éviter un IndexError
				if laby[murs[0]][murs[1]] != " ":	# Coup non valide. Il suffit de regarder si le mur voisin est bien un mur, ou de regarder si la case voisine est occupée
					continue

				elif laby[voisins[0]][voisins[1]] in [" ", "P"] and laby[murs[0]][murs[1]] == " ":		# Coup valide
					ariane = dict(perso)	# On copie le dictionnaire perso, pour éviter de la modifier inintentionnellement
					laby, ariane = moveQui(laby, ariane, touche)	# On bouge Ariane
					laby, thesee = arianeEtThesee(laby, ariane, (len(laby)-1)//2)	# On bouge Thésée				
					laby, vertical = mino(laby, thesee, "V")	# On bouge les Minotaures Verticaux
					laby, horizontal = mino(laby, vertical, "H")	# On bouge les Minotaures Horizontaux
					
					Csuivant = (voisins, horizontal["T"][0], horizontal["V"][0], horizontal["H"][0], coordPorte)	# On crée la configuration actuelle

					if Csuivant not in config:	# On vérifie si la configuration actuelle existe déjà ou non
						if solveur(laby, Csuivant, horizontal, taille_case, config):	# L'appel récursif de la fonction
							return True

		return False



# Cette fonction est utilisée uniquement pour la partie graphique du programme

def menu():
	"""
	Fonction permettant de choisir graphiquement le labyrinthe
	"""
	clicX, clicY = -1, -1
	while not ((clicX in range(88,289) and clicY in range(311,365)) or (clicX in range(492,691) and clicY in range(311,363)) or (clicX in range(86,287) and clicY in range(478,532)) or (clicX in range(485,685) and clicY in range(479,531)) or (clicX in range(600,751) and clicY in range(722,761))):
		image(0, 0, "media/Menu/choixLaby.png", ancrage="nw")
		clicX, clicY, evt = attente_clic()

		# Labyrinthe classique
		if clicX in range(88,289) and clicY in range(311,365):
			repertoire = "Classique"
			image(0, 0, "media/Menu/choixLabyClassique.png", ancrage="nw")

			clicX, clicY = -1, -1
			while not ((clicX in range(50,249) and clicY in range(293,345)) or (clicX in range(292,491) and clicY in range(293,345)) or (clicX in range(593,735) and clicY in range(296,345)) or (clicX in range(50,249) and clicY in range(490,542)) or (clicX in range(292,492) and clicY in range(490,542)) or (clicX in range(536,735) and clicY in range(490,543)) or clicX in range(600,751) and clicY in range(722,761)):
				clicX, clicY, evt = attente_clic()

				if clicX in range(50,249) and clicY in range(293,345):
					fichier = "labyrinthe1.txt"
					return fichier, repertoire

				elif clicX in range(292,491) and clicY in range(293,345):
					fichier = "labyrinthe2.txt"
					return fichier, repertoire

				elif clicX in range(593,735) and clicY in range(296,345):
					fichier = "labyrinthe3.txt"
					return fichier, repertoire

				elif clicX in range(50,249) and clicY in range(490,542):
					fichier = "labyrinthe4.txt"
					return fichier, repertoire

				elif clicX in range(292,492) and clicY in range(490,542):
					fichier = "labyrinthe5.txt"
					return fichier, repertoire

				elif clicX in range(536,735) and clicY in range(490,543):
					fichier = "sandbox.txt"
					return fichier, repertoire

				elif clicX in range(600,751) and clicY in range(722,761):	# Bouton retour
					efface_tout()
					clicX, clicY = -1, -1
					fichier, repertoire = 0, 0
					break


		# Grand labyrinthe
		elif clicX in range(492,691) and clicY in range(311,363):
			repertoire = "big"
			image(0, 0, "media/Menu/choixLabyGrand.png", ancrage="nw")

			clicX, clicY = -1, -1
			while not ((clicX in range(99,299) and clicY in range(379,431)) or (clicX in range(474,674) and clicY in range(379,431)) or clicX in range(600,751) and clicY in range(722,761)):
				clicX, clicY, evt = attente_clic()

				if clicX in range(99,299) and clicY in range(379,431):
					fichier = "big1.txt"
					return fichier, repertoire

				elif clicX in range(474,674) and clicY in range(379,431):
					fichier = "big2.txt"
					return fichier, repertoire

				elif clicX in range(600,751) and clicY in range(722,761):	# Bouton retour
					efface_tout()
					clicX, clicY = -1, -1
					fichier, repertoire = 0, 0
					break


		# Petit labyrinthe
		elif clicX in range(86,287) and clicY in range(478,532):
			repertoire = "small"
			image(0, 0, "media/Menu/choixLabyPetit.png", ancrage="nw")

			clicX, clicY = -1, -1
			while not ((clicX in range(99,299) and clicY in range(324,377)) or (clicX in range(474,673) and clicY in range(324,377)) or (clicX in range(99,299) and clicY in range(503,556)) or (clicX in range(474,673) and clicY in range(503,556)) or clicX in range(600,751) and clicY in range(722,761)):
				clicX, clicY, evt = attente_clic()

				if clicX in range(99,299) and clicY in range(324,377):
					fichier = "small1.txt"
					return fichier, repertoire

				elif clicX in range(474,673) and clicY in range(324,377):
					fichier = "small2.txt"
					return fichier, repertoire

				elif clicX in range(99,299) and clicY in range(503,556):
					fichier = "small3.txt"
					return fichier, repertoire

				elif clicX in range(474,673) and clicY in range(503,556):
					fichier = "small4.txt"
					return fichier, repertoire

				elif clicX in range(600,751) and clicY in range(722,761):	# Bouton retour
					efface_tout()
					clicX, clicY = -1, -1
					fichier, repertoire = 0, 0
					break


		# Défi d'ariane
		elif clicX in range(485,685) and clicY in range(479,531):
			repertoire = "defi"
			image(0, 0, "media/Menu/choixLabyDefi.png", ancrage="nw")

			clicX, clicY = -1, -1
			while not ((clicX in range(99,299) and clicY in range(324,377)) or (clicX in range(474,673) and clicY in range(324,377)) or (clicX in range(99,299) and clicY in range(503,556)) or (clicX in range(474,673) and clicY in range(503,556)) or clicX in range(600,751) and clicY in range(722,761)):
				clicX, clicY, evt = attente_clic()

				if clicX in range(99,299) and clicY in range(324,377):
					fichier = "defi0.txt"
					return fichier, repertoire

				elif clicX in range(474,673) and clicY in range(324,377):
					fichier = "defi1.txt"
					return fichier, repertoire

				elif clicX in range(99,299) and clicY in range(503,556):
					fichier = "defi2.txt"
					return fichier, repertoire

				elif clicX in range(474,673) and clicY in range(503,556):
					fichier = "defi3.txt"
					return fichier, repertoire

				elif clicX in range(600,751) and clicY in range(722,761):	# Bouton retour
					efface_tout()
					clicX, clicY = -1, -1
					fichier, repertoire = 0, 0
					break

		# Bouton retour
		elif clicX in range(600,751) and clicY in range(722,761):
			efface_tout()
			fichier, repertoire = 0, 0
			return fichier, repertoire




if __name__ == "__main__":

	"""Création de la fenêtre"""
	taille_case = 40
	cree_fenetre(taille_case * 20,
				 taille_case * 20)

	
	clicX, clicY = -1, -1
	design = None
	repertoire = None
	fichier = None
	retour = None

	while not (193 <= clicX <= 593 and 296 <= clicY <= 400) or not (193 <= clicX <= 593 and 515 <= clicY <= 621):
		image(0, 0, "media/Menu/menu.png", ancrage="nw")
		if type(fichier) == str:
			break

		clicX, clicY, evt = attente_clic()
		if 193 <= clicX <= 593 and 296 <= clicY <= 400:		# On choisit de jouer
			jeu = "Jouer"
			
			clicX, clicY = -1, -1
			while not ((clicX in range(416,616) and clicY in range(504,557)) or (clicX in range(416,616) and clicY in range(335,388)) or (clicX in range(600,751) and clicY in range(722,761))):
				fichier, repertoire = None, None
				image(0, 0, "media/Menu/choixDesign.png", ancrage="nw")
				clicX, clicY, evt = attente_clic()
				
				if clicX in range(416,616) and clicY in range(335,388):
					design = "Original"

				elif clicX in range(416,616) and clicY in range(504,557):
					design = "Crypt of the NecroDancer"

				elif clicX in range(600,751) and clicY in range(722,761):	# Bouton retour
					efface_tout()
					break

				if design != None:
					while fichier == None and repertoire == None:
						fichier, repertoire = menu()
						if type(fichier) != str and type(repertoire) != str:	# Bouton retour
							efface_tout()
							clicX, clicY = -1, -1
							break


		# On choisit le solveur
		elif 193 <= clicX <= 593 and 515 <= clicY <= 621:
			jeu = "Solveur"
			fichier, repertoire = menu()
			if type(fichier) != str and type(repertoire) != str:	# Bouton retour
				efface_tout()
				clicX, clicY = -1, -1

		clicX, clicY = -1, -1

	ferme_fenetre()


	"""Initialisation du fichier du labyrinthe"""
	file = ouvrirFichier(repertoire, fichier)
	taille = file[0]
	continuer = True

	"""Initialisation de la taille de l'écran"""
	
	largeur_plateau = int(taille)*2
	hauteur_plateau = int(taille)*2

	"""Création de la variable stockant le labyrinthe en liste de liste et la variable stockant les positions des personnages"""
	laby = creerLabyrinthe(file)
	perso = positionPersos(laby)
	gameState = gameState(laby)

	"""Création de la fenêtre"""
	taille_case = 40
	cree_fenetre(taille_case * largeur_plateau,
				 taille_case * hauteur_plateau)


	if jeu == "Jouer":
		drawLaby(laby, taille_case, design, perso)

		while continuer:

			val, touche, evt = attente_clic_ou_touche()
			laby, perso = moveQui(laby, perso, touche)
			laby, perso = arianeEtThesee(laby, perso, largeur_plateau)
			victory = victoire(laby, perso)

			laby, perso = mino(laby, perso, "V")
			laby, perso = mino(laby, perso, "H")

			efface_tout()
			drawLaby(laby, taille_case, design, perso)

			if victory == True:
				texte((taille_case * largeur_plateau)/2, (taille_case * hauteur_plateau)/2, "Victory !", couleur='blue', ancrage="center", police="Purisa", taille=24, tag='')
				continuer = False

			elif victory == False:
				texte((taille_case * largeur_plateau)/2, (taille_case * hauteur_plateau)/2, "Defeat !", couleur='blue', ancrage="center", police="Purisa", taille=24, tag='')
				continuer = False
	

	elif jeu == "Solveur":
		res = solveur(laby, gameState, perso, taille_case)
		print(res)



attente_clic()
