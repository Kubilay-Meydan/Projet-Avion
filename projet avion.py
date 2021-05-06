#########################################
# groupe DLBI 1
# Kubilay MEYDAN
# Julie CIESLA
# Alix FRAGNER
# Margaux DUBOIS GUENRO
# Elise REBER
# https://github.com/uvsq22004090/Projet-Avion.git
#########################################


import tkinter as tk
import random as rd
from random import choice
import copy


racine = tk.Tk()
racine.title("simulation d'avion")

#########################################
# CONSTANTES

CANVAS_HEIGHT = 600
CANVAS_WIDTH = 140
COTE = 20
COULEUR_COULOIR = 'grey'
COULEUR_PASSAGER_0_BAGAGE = 'cyan'
COULEUR_PASSAGER_1_BAGAGE = 'mediumorchid1'
COULEUR_PASSAGER_2_BAGAGES = 'red'
COULEUR_SIEGE_VIDE = 'blue'
COULEUR_SIEGE_OCCUPE = 'yellow'
COULEUR_SIEGE_REMPLI = 'green'
NB_RANG = 30
NB_COLONNE = 7
NB_PASSAGERS_MAX = 180
X_COULOIR = 4 
TPS_ETAPES = 50  # temps entre chaque étape

#########################################
# VARIABLES

mat_passagers = [] # Liste de tous les passages
mat_2 = []
liste_passagers_in=[] # Liste des passagers actuellement dans l'avion.
l_passagers_in_bis = []
interdit_x = [4]
interdit_y = []
count_x = []
count_y = []
compteur_passager = -1
compteur_passager_assis = 0

#########################################
# FONCTIONS


def passagers(mat):
    '''Créer un passager [[destination], bagage, couleur] dans une matrice'''

    global mat_2, interdit_x, interdit_y

    x = choice([i for i in range(1, 8) if i not in interdit_x])
    y = choice([i for i in range(1, 31) if i not in interdit_y])

    if [x, y] in mat_2:
        while [x, y] in mat_2:
            x = choice([i for i in range(1, 8) if i not in interdit_x])
            y = choice([i for i in range(1, 31) if i not in interdit_y])
    mat_2.append([x, y])
    mat.append([[x, y]])

    interdit(x, y)

    # bagages + couleur
    mat[-1].append(rd.randint(0, 2))

    if mat[-1][1] == 0:
        mat[-1].append(COULEUR_PASSAGER_0_BAGAGE)
    elif mat[-1][1] == 1:
        mat[-1].append(COULEUR_PASSAGER_1_BAGAGE)
    else:
        mat[-1].append(COULEUR_PASSAGER_2_BAGAGES)


def interdit(x, y):
    '''Compte combien de fois x, y sont apparus.
    Si x est apparu 30 fois ou y est apparu 7 fois, il est enlevé des
    possibilités de choix pour les places'''

    global interdit_x, interdit_y, count_x, count_y

    count_x.append(x)
    count_y.append(y)

    if count_x.count(x) >= 30:
        interdit_x.append(x)
    if count_y.count(y) >= 6:
        interdit_y.append(y)


def convertit_siege_identifiant(x, y):  # colonne, rang
    """Cette fonction prend en argument x et y qui sont les coordonnées d'où se
    trouve un passager (ou bien où il doit aller).
    Convertit ces coordonnées en identifiant de canvas.
    Returne l'identifiant du canevas"""

    global NB_COLONNE, NB_RANG

    identifiant = 0
    for i in range(1, NB_RANG+1):
        for j in range(1, NB_COLONNE+1):
            identifiant += 1
            if x == j and y == i:
                return identifiant


def entree_passager():
    """ Prend en argument la liste d'un passager qui n'est pas dans l'avion.
    Test si un nouveau passager peut entrer dans l'avion.
    Si oui il rentre et on ajoute ses coordonnées actuelles à la liste la
    représentant. Sinon rien ne se passe."""

    global compteur_passager, liste_passagers_in, mat_passagers

    if (avion.itemcget((convertit_siege_identifiant(4, 1)), "fill")) == COULEUR_SIEGE_VIDE:
        compteur_passager += 1  # Prend le passager suivant dans la liste de tous les passagers
        if compteur_passager < NB_PASSAGERS_MAX:  # Si tous les passagers ne sont pas encore dans l'avion
            avion.itemconfigure(convertit_siege_identifiant(4, 1), fill=mat_passagers[compteur_passager][2])
            liste_passagers_in.append(mat_passagers[compteur_passager])
            liste_passagers_in[compteur_passager].extend([[4, 1]])


def deplace_passagers_in():
    """Déplace tous les passages qui sont actuellement dans l'avion.
    Fait entrer un passager si possible. 
    La fonction est répétée tous les TPS_ETAPES."""

    global liste_passagers_in

    if liste_passagers_in != []:
        for i in range(len(liste_passagers_in)):
            deplace_1_passager(liste_passagers_in, i)

        entree_passager()

    avion.after(TPS_ETAPES, lambda: deplace_passagers_in())


def convertisseur_couleur_case(x, y, couleur):
    """Prend en entrée les coordonnées x et y d'une case et une couleur.
    Puis associe cette couleur à la case."""

    avion.itemconfig((convertit_siege_identifiant(x, y)), fill=couleur)


def swipe_place(liste, n1, x_prime, y_prime):
    """Permet de faire échanger deux places à des passagers, si l'un bloque
    l'autre dans une rangée.
    Prend en arguments:
    liste --> la liste de tous les passagers acutellement dans l'avion.
    n1 --> l'indice auquel se trouve le passager qui est bloqué dans la liste.
    x_prime --> la coordonnée x où veut aller le passager n1
    y_prime --> la coordonnée y où veut aller le passager n1"""

    # print("liste après", liste, "\n")
    if [[x_prime, y_prime], 0, COULEUR_SIEGE_REMPLI, [x_prime, y_prime]] in liste:
        n2 = liste.index([[x_prime, y_prime], 0, COULEUR_SIEGE_REMPLI, [x_prime, y_prime]])  # Cherche le passager avec qui n1 doit échanger sa place.
        # print(n1, n2)
        # print((liste[n1]), liste[n2])
        liste[n2][3][0], liste[n1][3][0] = liste[n1][3][0], liste[n2][3][0]  
        liste[n2][2] = COULEUR_PASSAGER_0_BAGAGE
        convertisseur_couleur_case(liste[n2][3][0], liste[n2][3][1], liste[n2][2])
        convertisseur_couleur_case(liste[n1][3][0], liste[n1][3][1], liste[n1][2])
    # liste.extend([liste[n2]])
    # del liste[n2]

    return liste


def deplace_1_passager(liste, n):  # [[x, y], bagage, couleur, [x', y']]
    """Prend en entrée la liste des passagers actuellement dans l'avion ainsi
    et l'indice auquel correspond le passager dans cette liste (l'indice est noté n)
    
    Puis déplace ou non le passager en fonction d'où il se trouve dans l'avion.
    Permet aussi de faire déposer les bagages de passagers."""
    global compteur_passager_assis

    if liste[n][0] == liste[n][3]:  # si passager à sa place
        pass
    elif (liste[n][0][1]) != (liste[n][3][1]):  # si passager pas dans sa rangée.
        liste[n][3][1] += 1  # Va dans la rangée suivante.
        if (avion.itemcget((convertit_siege_identifiant(liste[n][3][0], liste[n][3][1])), "fill")) != COULEUR_SIEGE_VIDE:  #S i case suivante occupé
            liste[n][3][1] -= 1
        else:
            convertisseur_couleur_case(liste[n][3][0], (liste[n][3][1]-1), COULEUR_SIEGE_VIDE)
            convertisseur_couleur_case(liste[n][3][0], liste[n][3][1], liste[n][2])

    elif (liste[n][0][1]) == (liste[n][3][1]):  # Si dans sa rangée
        if liste[n][1] == 0:  # si pas de bagages
            if liste[n][0][0] < X_COULOIR:  # Va dans le rang de gauche (par rapport à l'interface graphique)
                if (avion.itemcget((convertit_siege_identifiant(liste[n][3][0]-1, liste[n][3][1])), "fill")) == COULEUR_SIEGE_VIDE:  # Si pas de passager qui gene.
                    convertisseur_couleur_case(liste[n][3][0], liste[n][3][1], COULEUR_SIEGE_VIDE)  # La case redevient vide
                    liste[n][3][0] -= 1 
                elif (avion.itemcget((convertit_siege_identifiant(liste[n][3][0]-1, liste[n][3][1])), "fill")) == COULEUR_SIEGE_REMPLI:  # Si passager assis gène le passage.
                    # print("liste avant", liste, "\n")
                    swipe_place(liste, n, liste[n][3][0] - 1, liste[n][3][1])

            else:  # Va dans le rang de droite (par rapport à l'interface graphique)
                if (avion.itemcget((convertit_siege_identifiant(liste[n][3][0]+1, liste[n][3][1])), "fill")) == COULEUR_SIEGE_VIDE:  # Si pas de passager qui gene.
                    convertisseur_couleur_case(liste[n][3][0], liste[n][3][1], COULEUR_SIEGE_VIDE)  # La case redevient vide
                    liste[n][3][0] += 1
                elif (avion.itemcget((convertit_siege_identifiant(liste[n][3][0]-1, liste[n][3][1])), "fill")) == COULEUR_SIEGE_REMPLI:  # Si passager assis gène le passage.
                    # print("liste avant", liste, "\n")
                    swipe_place(liste, n, liste[n][3][0] + 1, liste[n][3][1])

            if liste[n][0] == liste[n][3]:  # si passager à atteint son siège.
                liste[n][2] = COULEUR_SIEGE_REMPLI
                compteur_passager_assis += 1
            convertisseur_couleur_case(liste[n][3][0], liste[n][3][1], liste[n][2])  # La case suivante prend la couleur du passager

        else:  # si a des bagages
            liste[n][1] -= 1
            if liste[n][1] == 0:
                liste[n][2] = COULEUR_PASSAGER_0_BAGAGE
            elif liste[n][1] == 1:
                liste[n][2] = COULEUR_PASSAGER_1_BAGAGE
            convertisseur_couleur_case(liste[n][3][0], liste[n][3][1], liste[n][2])



def demarrer():
    # fonction démarrant la simulation
    pass


def arreter():
    # fonction arrêtant la simulation
    pass


def pause():
    # fonction mettant la simulation en pause
    pass


def relancer():
    # fonction relançant la simulation après l'avoir mis en pause
    pass


def etape_1():
    # fonction permettant d'avancer la simulation d'une étape
    pass


def etape_par_etape():
    # fonction permmettant de
    pass


def recommencer():
    # fonction permettant de recommencer la simulation du début
    pass


def quadrillage():
    i = 0
    j = 0
    while j <= CANVAS_HEIGHT:
        while i < CANVAS_WIDTH:
            avion.create_rectangle(i, j, i+COTE, j+COTE, fill="blue")
            i += COTE
        j += COTE
        i = 0


#########################################
# WIDGETS


avion = tk.Canvas(racine, height=CANVAS_HEIGHT, width=CANVAS_WIDTH)
bouton_demarrer = tk.Button(racine, text='démarrer', command=demarrer)
bouton_arreter = tk.Button(racine, text='arrêter', command=arreter)
bouton_pause = tk.Button(racine, text='pause', command=pause)
bouton_relancer = tk.Button(racine, text='relancer', command=relancer)
bouton_etape_1 = tk.Button(racine, text='étape +1', command=etape_1)
bouton_etape_par_etape = tk.Button(racine, text='étape par étape',
                                   command=etape_par_etape)
bouton_recommencer = tk.Button(racine, text='recommencer', command=recommencer)


#########################################
# POSITIONNEMENT

avion.grid(row=0, column=1, rowspan=7)
bouton_demarrer.grid(row=0, column=0)
bouton_arreter.grid(row=1, column=0)
bouton_pause.grid(row=2, column=0)
bouton_relancer.grid(row=3, column=0)
bouton_etape_1.grid(row=4, column=0)
bouton_etape_par_etape.grid(row=5, column=0)
bouton_recommencer.grid(row=6, column=0)


avion.bind(quadrillage())


#########################################
for i in range(180):
    passagers(mat_passagers)

#print(mat_passagers, "\n")

entree_passager()

deplace_passagers_in()

racine.mainloop()