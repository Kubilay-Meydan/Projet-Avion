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
COULEUR_PASSAGER_1_BAGAGE = 'blue'
COULEUR_PASSAGER_2_BAGAGE = 'blue'
COULEUR_SIEGE_VIDE = 'blue'
COULEUR_SIEGE_OCCUPE = 'green'
COULEUR_SIEGE_REMPLI = 'yellow'
NB_RANG = 30
NB_COLONNE = 7


#########################################
# VARIABLES

mat_passagers = []
mat_2 = []
interdit_x = [4]
interdit_y = []
count_x = []
count_y = []


#########################################
# FONCTIONS

def passagers(mat):
    '''Créer un passager [[destination], bagage, couleur] dans une matrice'''

    global mat_2, interdit_x, interdit_y

    x = choice([i for i in range(1, 8) if i not in interdit_x])
    y = choice([i for i in range(1, 31) if i not in interdit_y])
    mat.append([[x, y]])

    while mat[-1] in mat_2:
        del mat[-1]
        x = choice([i for i in range(1, 8) if i not in interdit_x])
        y = choice([i for i in range(1, 31) if i not in interdit_y])
        mat.append([x, y])
    mat_2 = mat.copy()

    interdit(x, y)

    # bagages + couleur
    mat[-1].append(rd.randint(0, 2))

    if mat[-1][1] == 0:
        mat[-1].append(COULEUR_PASSAGER_0_BAGAGE)
    elif mat[-1][1] == 1:
        mat[-1].append(COULEUR_PASSAGER_1_BAGAGE)
    else:
        mat[-1].append(COULEUR_PASSAGER_2_BAGAGE)


def interdit(x, y):
    '''Compte combien de fois x, y sont apparus.
    Si x est apparu 30 fois ou y est apparu 7 fois, il est enlevé des
    possibilités de choix pour les places'''

    global interdit_x, interdit_y, count_x, count_y

    count_x.append(x)
    count_y.append(y)

    if count_x.count(x) >= NB_COLONNE:
        interdit_x.append(x)
    if count_y.count(y) >= NB_RANG:
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


def entree_passager(liste):
    """ Prend en argument la liste d'un passager qui n'est pas dans l'avion.
    Test si un nouveau passager peut entrer dans l'avion.
    Si oui il rentre et on ajoute ses coordonnées actuelles à la liste la
    représentant. Sinon rien ne se passe."""

    if (avion.itemcget((convertit_siege_identifiant(4, 1)), "fill")) == COULEUR_SIEGE_VIDE:
        avion.itemconfigure(convertit_siege_identifiant(4, 1), fill=liste[3])  # Liste à changer selon liste Alix.
        liste.extend([4, 1])

        # Faire une liste qui regroupe tous les passagers actuellement dans l'avion ?


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


racine.mainloop()
