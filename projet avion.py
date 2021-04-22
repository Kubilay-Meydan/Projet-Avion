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


# # # CONSTANTES

CANVAS_HEIGHT = 600
CANVAS_WIDTH = 140
COTE = 20

# # # FONCTIONS


def demarrer():
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
        print(i)


# # # WIDGETS

avion = tk.Canvas(racine, height=CANVAS_HEIGHT, width=CANVAS_WIDTH, bg='blue')
bouton_demarrer = tk.Button(racine, text='démarrer', command=demarrer)
# Statistiques =
# informations_avion


# # # POSITIONNEMENT

avion.grid(row=0, column=1)
bouton_demarrer.grid(row=0, column=0)

avion.bind(quadrillage())

racine.mainloop()
