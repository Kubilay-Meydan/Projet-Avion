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

racine = tk.Tk()
racine.title("simulation d'avion")


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


# MATRICE PASSAGERS

list_pass = [[coord], nb_bagages, couleur_entrée]

mat_pass = []
for i in range(180):
    



# FONCTIONS

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
    while i <= CANVAS_WIDTH:
        while j <= CANVAS_HEIGHT:
            avion.create_rectangle(i, j, i+COTE, j+COTE)
            j += COTE
        i += COTE
        j = 0


# WIDGETS

avion = tk.Canvas(racine, height=CANVAS_HEIGHT, width=CANVAS_WIDTH, bg='blue')
bouton_demarrer = tk.Button(racine, text='démarrer', command=demarrer)
bouton_arreter = tk.Button(racine, text='arrêter', command=arreter)
bouton_pause = tk.Button(racine, text='pause', command=pause)
bouton_relancer = tk.Button(racine, text='relancer', command=relancer)
bouton_etape_1 = tk.Button(racine, text='étape +1', command=etape_1)
bouton_etape_par_etape = tk.Button(racine, text='étape par étape',
                                   command=etape_par_etape)
bouton_recommencer = tk.Button(racine, text='recommencer', command=recommencer)


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

racine.mainloop()
