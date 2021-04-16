import tkinter as tk
import random


##################
# Constantes

RANG_MIN = 1
RANG_MAX = 30

X_MIN = 1
X_COULOIR = 4
X_MAX = 7

OPT_HASARD = 0
OPT_PLUS = 1
OPT_MOINS = 2

BAGAGE_MIN = 0
BAGAGE_MAX = 2
BAGAGE_HASARD = -1
BAGAGE_MODULO_X = -2
BAGAGE_MODULO_Y = -3
BAGAGE_MODULO_Z = -4

CELL_LARGEUR = 30
CELL_HAUTEUR = 20

COUL_DEFAUT = "grey"
COUL_BORD = "white"
COUL_COULOIR_VIDE = "grey"
COUL_SIEGE_VIDE = "yellow"
COUL_PASSAGER_PLACE = "green"
COUL_PASSAGER_SANS_BAG = "cyan"
COUL_PASSAGER_AVEC_BAG = "blue"

BTN_START = "Demarrer"
BTN_STOP = "Arreter"
BTN_PAUSE_STOP = "Pause"
BTN_PAUSE_GO = "Relancer"
BTN_NEXT = "Etape suivante"

ACTION_ATTENDRE = 0
ACTION_AVANCE = 1
ACTION_BAGAGE = 2
ACTION_SIEGE = 3
ACTION_ECHANGE = 4

ERR_BAD_CELL = 0
ERR_PSG_COULOIR = 1
ERR_PSG_EXTERIEUR = 2
ERR_B = 3
ERR_C = 4


###################
# Classe Passager
class Passager:
    def __init__(self, x, y, nb_bagages):
        self.x = x
        self.y = y
        if ((nb_bagages >= BAGAGE_MIN) and (nb_bagages <= BAGAGE_MAX)):
            self.bagages = nb_bagages
        elif (nb_bagages == BAGAGE_MODULO_X):
            self.bagages = x % (BAGAGE_MAX-BAGAGE_MIN+1)
        elif (nb_bagages == BAGAGE_MODULO_Y):
            self.bagages = y % (BAGAGE_MAX-BAGAGE_MIN+1)
        elif (nb_bagages == BAGAGE_MODULO_Z):
            self.bagages = (x+y) % (BAGAGE_MAX-BAGAGE_MIN+1)
        else:
            # Au hasard
            self.bagages = random.randint(BAGAGE_MIN, BAGAGE_MAX)

    def id_str(self):
        return "Passager({0},{1},{2})".format(self.x, self.y, self.bagages)


###################
# Classe Statistiques
class Statistiques:
    def __init__(self, frame):
        self.etape_str = tk.StringVar()
        self.passagers_in_str = tk.StringVar()
        self.passagers_on_str = tk.StringVar()

        # Etape
        lbl = tk.Label(frame, text="Etape :",
                       anchor="w", font=("helvetica", "12"))
        lbl.grid(column=0, row=0, sticky="w")
        lbl = tk.Label(frame, textvariable=self.etape_str,
                       anchor="e", font=("helvetica", "12"))
        lbl.grid(column=1, row=0, sticky="e")

        # Nombre de passagers entre's dans l'avion
        lbl = tk.Label(frame, text="Passagers entrés :",
                       anchor="w", font=("helvetica", "12"))
        lbl.grid(column=0, row=1, sticky="w")
        lbl = tk.Label(frame, textvariable=self.passagers_in_str,
                       anchor="e", font=("helvetica", "12"))
        lbl.grid(column=1, row=1, sticky="e")

        # Nombre de passagers a leur place
        lbl = tk.Label(frame, text="Passagers placés :",
                       anchor="w", font=("helvetica", "12"))
        lbl.grid(column=0, row=2, sticky="w")
        lbl = tk.Label(frame, textvariable=self.passagers_on_str,
                       anchor="e", font=("helvetica", "12"))
        lbl.grid(column=1, row=2, sticky="e")

        self.reset()

    def reset(self):
        self.etape = 0
        self.passagers_in = 0
        self.passagers_on = 0
        self.actions = [0, 0, 0, 0, 0]
        self.errors = [0, 0, 0, 0, 0]

        self.affiche()

    def etape_suivante(self):
        self.etape += 1
        self.action_done = False

    def affiche(self):
        self.etape_str.set("  {0}".format(self.etape))
        self.passagers_in_str.set("  {0}".format(self.passagers_in))
        self.passagers_on_str.set("  {0}".format(self.passagers_on))

    def add_passager_in(self):
        self.passagers_in += 1
        self.action_done = True

    def add_passager_on(self):
        self.passagers_on += 1

    def del_passager_on(self):
        self.passagers_on -= 1

    def add_action(self, action_id):
        self.actions[action_id] += 1
        self.action_done = True

    def add_error(self, error_id):
        self.errors[error_id] += 1
        self.action_done = True

    def print_all(self, nb_rangs, nb_bagages):

        prevu_passagers = (X_MAX - X_MIN) * nb_rangs

        nb_avancer = 0
        for r in range(RANG_MIN, nb_rangs):
            nb_avancer += r
        prevu_avancer = (X_MAX - X_MIN) * nb_avancer

        nb_sieges = 0
        for s in range(X_MIN, X_COULOIR):
            nb_sieges += s
        prevu_sieges = 2 * nb_sieges * nb_rangs

        print("Etapes           : ", self.etape)
        print("Passagers entrés : ", self.passagers_in,
              "\t/ ", prevu_passagers)
        print("Passagers placés : ", self.passagers_on,
              "\t/ ", prevu_passagers)
        print("---- Actions ----")
        print("Attendre : ", self.actions[ACTION_ATTENDRE])
        print("Avancer  : ", self.actions[ACTION_AVANCE],
              "\t/ ", prevu_avancer)
        print("Bagage   : ", self.actions[ACTION_BAGAGE],
              "\t/ ", nb_bagages)
        print("Siège    : ", self.actions[ACTION_SIEGE],
              "\t/ ", prevu_sieges)
        print("Echanger : ", self.actions[ACTION_ECHANGE])
        print("---- Erreurs ----")
        print("Cellule non trouvée : ", self.errors[ERR_BAD_CELL])
        print("Passager couloir    : ", self.errors[ERR_PSG_COULOIR])
        print("Passager exterieur  : ", self.errors[ERR_PSG_EXTERIEUR])


###################
# Classe Cellule
class Cellule:
    def __init__(self, x, y, rang, canvas):
        # print("--> Creation Cellule(", x, ",", y, ")")
        self.__bien_place = False
        self.x = x
        self.y = y
        self.passager = None
        self.rang = rang
        self.canvas = canvas

        cx0 = (x-1) * (CELL_LARGEUR+2)
        cy0 = y * (CELL_HAUTEUR+2)
        cx1 = cx0 + CELL_LARGEUR
        cy1 = cy0 + CELL_HAUTEUR
        # print("   x0,y0 = ", cx0, ",", cy0, " | x1,y1 = ", cx1, ",", cy1)
        if (self.x == X_COULOIR):
            self.place = canvas.create_rectangle(cx0, cy0, cx1, cy1,
                                                 fill=COUL_DEFAUT, width=1,
                                                 outline=COUL_DEFAUT)
        else:
            self.place = canvas.create_oval(cx0, cy0, cx1, cy1,
                                            fill=COUL_DEFAUT, width=1,
                                            outline=COUL_DEFAUT)

    def id_str(self):
        return "Cellule({0},{1})".format(self.x, self.y)

    def est_vide(self):
        return (self.passager is None)

    def reset(self):
        self.__bien_place = False
        self.passager = None
        if (self.x == X_COULOIR):
            self.canvas.itemconfigure(self.place,
                                      fill=COUL_COULOIR_VIDE,
                                      outline=COUL_COULOIR_VIDE)
        else:
            self.canvas.itemconfigure(self.place,
                                      fill=COUL_SIEGE_VIDE,
                                      outline=COUL_BORD)

    def color_bad_passager(self):
        if (self.passager.bagages > 0):
            self.canvas.itemconfigure(self.place,
                                      fill=COUL_PASSAGER_AVEC_BAG)
        else:
            self.canvas.itemconfigure(self.place,
                                      fill=COUL_PASSAGER_SANS_BAG)

    def not_used(self):
        self.passager = None
        self.canvas.itemconfigure(self.place,
                                  fill=COUL_DEFAUT,
                                  outline=COUL_DEFAUT)

    def execute(self, stats_etape):
        # Il y a quelque chose à faire si il y a un passager dans la cellule
        if not self.est_vide():
            if (self.x == X_COULOIR):
                self.execute_couloir(stats_etape)
            else:
                self.execute_siege(stats_etape)

    def execute_couloir(self, stats_etape):
        # print("--> ", self.id_str(), ".execute_couloir()")
        if self.y == self.passager.y:
            # C'est le bon rang
            if (self.passager.bagages > 0):
                # On pose un bagage
                self.passager.bagages -= 1
                self.color_bad_passager()
                stats_etape.add_action(ACTION_BAGAGE)
            else:
                # Il faut insérer le passager dans le rang de sieges
                # du bon coté
                if self.passager.x == X_COULOIR:
                    print("    ", self.passager.id_str(), "dans couloir !")
                    self.remove_passager(stats_etape)
                    stats_etape.add_error(ERR_PSG_COULOIR)
                else:
                    self.move_passager(stats_etape)
        else:
            # Il faut passer le passager au couloir du rang suivant
            # si il est vide
            dest_cell = self.rang.get_cellule(self.x, self.y+1)
            if (dest_cell is None):
                print("    Cellule({0},{1})".format(self.x, self.y+1),
                      " pas trouvée pour ", self.passager.id_str())
                self.remove_passager(stats_etape)
                stats_etape.add_error(ERR_BAD_CELL)
            else:
                if dest_cell.est_vide():
                    dest_cell.set_passager(self.passager, stats_etape)
                    self.remove_passager(stats_etape)
                    stats_etape.add_action(ACTION_AVANCE)
                else:
                    stats_etape.add_action(ACTION_ATTENDRE)

    def execute_siege(self, stats_etape):
        # print("--> ", self.id_str(), ".execute_siege()")
        # Il y a quelque chose à faire si le passager n'est pas le bon
        if not self.__bien_place:
            if (self.x == X_MIN) or (self.x == X_MAX):
                print("    ", self.passager.id_str(), " trop exterieur !")
                self.remove_passager(stats_etape)
                stats_etape.add_error(ERR_PSG_EXTERIEUR)
            else:
                self.move_passager(stats_etape)

    def remove_passager(self, stats_etape):
        # On regarde si c'était le bon passager
        if self.__bien_place:
            self.__bien_place = False
            stats_etape.del_passager_on()

        self.reset()

    def set_passager(self, passager, stats_etape):
        if not self.est_vide():
            self.remove_passager(stats_etape)

        self.passager = passager
        if not (passager is None):
            if (self.x == X_COULOIR):
                self.color_bad_passager()
            else:
                # On regarde si c'est la bonne place pour le passager
                if (self.x == passager.x) and (self.y == passager.y):
                    self.__bien_place = True
                    self.canvas.itemconfigure(self.place,
                                              fill=COUL_PASSAGER_PLACE)
                    stats_etape.add_passager_on()
                else:
                    self.color_bad_passager()

    def move_passager(self, stats_etape):
        # print("--> ", self.id_str(), ".move_passager()")
        dest_x = 0
        if self.passager.x < X_COULOIR:
            dest_x = self.x - 1
        else:
            dest_x = self.x + 1

        dest_cell = self.rang.get_cellule(dest_x, self.y)
        if (dest_cell is None):
            print("    Cellule({0},{1})".format(dest_x, self.y),
                  " pas trouvée pour ", self.passager.id_str())
            self.remove_passager(stats_etape)
            stats_etape.add_error(ERR_BAD_CELL)
        else:
            if dest_cell.est_vide():
                dest_cell.set_passager(self.passager, stats_etape)
                self.remove_passager(stats_etape)
                stats_etape.add_action(ACTION_SIEGE)
            else:
                passager_tmp = self.passager
                self.set_passager(dest_cell.passager, stats_etape)
                dest_cell.set_passager(passager_tmp, stats_etape)
                stats_etape.add_action(ACTION_ECHANGE)


###################
# Classe Rang
class Rang:
    def __init__(self, y, canvas):
        # print("--> Creation Rang(", y, ")")
        self.y = y
        self.canvas = canvas

        # Cellule idx 0 not used
        self.cellules = [None]
        for i in range(X_MIN, X_MAX+1):
            self.cellules.append(Cellule(x=i, y=y, rang=self, canvas=canvas))

    def id_str(self):
        return "Rang({0})".format(self.y)

    def reset(self):
        for i in range(X_MIN, X_MAX+1):
            self.cellules[i].reset()

    def not_used(self):
        for i in range(X_MIN, X_MAX+1):
            self.cellules[i].not_used()

    def get_cellule(self, x, y):
        global liste_rangs
        result_cell = None
        if (x >= X_MIN and x <= X_MAX and y >= RANG_MIN and y <= RANG_MAX):
            if (self.y == y):
                result_cell = self.cellules[x]
            else:
                result_cell = liste_rangs[y].cellules[x]

        return result_cell

    def execute(self, stats_etape):
        # On exécute les cellules depuis l'extérieur vers le couloir
        for i in range(X_COULOIR-X_MIN, 0, -1):
            self.cellules[X_COULOIR-i].execute(stats_etape)
            self.cellules[X_COULOIR+i].execute(stats_etape)

        self.cellules[X_COULOIR].execute(stats_etape)


###################
# Classe Avion
class Avion:
    def __init__(self, nom, nb_rangs, delai):
        self.nom = nom
        if ((nb_rangs > RANG_MAX) or (nb_rangs < RANG_MIN)):
            self.__nb_rangs = RANG_MAX
        else:
            self.__nb_rangs = nb_rangs

        self.__etape = 0
        self.__complet = False
        self.__nb_bagages = 0
        # Delai entre les étapes en millisecondes
        self.delai = delai

    def complet(self):
        return self.__complet

    def reset(self):
        # Reinitialise les rangs et les cellules
        global stats
        global liste_rangs

        stats.reset()

        for r in range(RANG_MIN, self.__nb_rangs+1):
            liste_rangs[r].reset()

        if (self.__nb_rangs < RANG_MAX):
            for r in range(self.__nb_rangs+1, RANG_MAX+1):
                liste_rangs[r].not_used()

        self.__etape = 0
        self.__complet = False
        self.__nb_bagages = 0
        self.couloir_1 = liste_rangs[1].get_cellule(x=X_COULOIR, y=1)

    def etape_suivante(self):
        # Lance l'étape suivante
        global stats
        global liste_rangs

        self.__etape += 1
        stats.etape_suivante()

        # On execute les rangs depuis le dernier jusqu'au 1er
        for r in range(self.__nb_rangs, RANG_MIN-1, -1):
            liste_rangs[r].execute(stats_etape=stats)

        # Si il reste des passagers à faire entrer
        if len(self.passagers) > 0:
            # Si le couloir du premier rang est vide, on fait entrer
            # le passager suivant
            if self.couloir_1.est_vide():
                new_passager = self.passagers.pop(0)
                self.__nb_bagages += new_passager.bagages
                self.couloir_1.set_passager(passager=new_passager,
                                            stats_etape=stats)
                stats.add_passager_in()
            else:
                stats.add_action(ACTION_ATTENDRE)

        # Si il n'y a pas eu d'action à cette étape, l'avion est complet
        if (not stats.action_done):
            self.__complet = True
            # On retire cette dernière etape qui n'a rien fait du tout
            stats.etape -= 1
            print("\n*** Avion '" + self.nom + "' complet ! ***")
            stats.print_all(self.__nb_rangs, self.__nb_bagages)

        stats.affiche()

    def remplir(self, list_passagers):
        # Lance le remplissage avec la liste des passagers
        self.reset()
        self.passagers = list_passagers

        # self.etape_suivante() est appelé depuis remplissage()


###################
# Fonctions

def passagers_hasard(nb_rangs):
    liste_passagers = []
    for r in range(RANG_MIN, nb_rangs+1):
        for x in range(X_MIN, X_MAX+1):
            if (x != X_COULOIR):
                liste_passagers.append(Passager(x, r, BAGAGE_HASARD))
    random.shuffle(liste_passagers)
    return liste_passagers


# ----------
def decode_opt(code_opt):
    res_opt = OPT_HASARD
    if ((code_opt == "C") or (code_opt == "c") or
       (code_opt == "P") or (code_opt == "p")):
        res_opt = OPT_PLUS
    elif ((code_opt == "D") or (code_opt == "d") or
          (code_opt == "M") or (code_opt == "m")):
        res_opt = OPT_MOINS
    return res_opt


# ----------
def decode_bag(code_bag):
    res_bag = BAGAGE_HASARD
    descr_bag = "- nombre de bagages au hasard.\n"
    if (code_bag == "0"):
        res_bag = 0
        descr_bag = "- nombre de bagages à 0 pour tous les passagers.\n"
    elif (code_bag == "1"):
        res_bag = 1
        descr_bag = "- nombre de bagages à 1 pour tous les passagers.\n"
    elif (code_bag == "2"):
        res_bag = 2
        descr_bag = "- nombre de bagages à 2 pour tous les passagers.\n"
    elif (code_bag == "X") or (code_bag == "x"):
        res_bag = BAGAGE_MODULO_X
        descr_bag = "- le nombre de bagages d'un passager"
        descr_bag += " est un modulo de son x.\n"
    elif (code_bag == "Y") or (code_bag == "y"):
        res_bag = BAGAGE_MODULO_Y
        descr_bag = "- le nombre de bagages d'un passager"
        descr_bag += " est un modulo de son y.\n"
    elif (code_bag == "Z") or (code_bag == "z"):
        res_bag = BAGAGE_MODULO_Z
        descr_bag = "- le nombre de bagages d'un passager"
        descr_bag += " est un modulo de son x+y.\n"
    return res_bag, descr_bag


# ----------
def passagers_rangs(nom, nb_rangs):
    liste_passagers = []
    description = "- {0} rangs,\n".format(nb_rangs)
    descr_b = "- nombre de bagages au hasard.\n"
    opt_r = OPT_HASARD
    opt_x = OPT_HASARD
    opt_b = BAGAGE_HASARD
    found_x = False
    found_b = False

    len_nom = len(nom)
    if (len_nom >= 2):
        opt_r = decode_opt(nom[1])

    if (len_nom >= 4):
        nom3 = nom[3]
        if (nom3 == "B") or (nom3 == "b"):
            found_b = True
            if (len_nom >= 5):
                opt_b, descr_b = decode_bag(nom[4])
        elif (nom3 == "X") or (nom3 == "x") or (nom3 == "S") or (nom3 == "s"):
            found_x = True
            if (len_nom >= 5):
                opt_x = decode_opt(nom[4])

    if (len_nom >= 7):
        nom6 = nom[6]
        if (not found_b) and ((nom6 == "B") or (nom6 == "b")):
            found_b = True
            if (len_nom >= 8):
                opt_b, descr_b = decode_bag(nom[7])
        elif (not found_x) and ((nom6 == "X") or (nom6 == "x") or
                                (nom6 == "S") or (nom6 == "s")):
            found_x = True
            if (len_nom >= 8):
                opt_x = decode_opt(nom[7])

    liste_r = []
    liste_x = []
    if (opt_r == OPT_PLUS):
        description += "- pour chaque rang du"
        description += " 1er au {0}ème,\n".format(nb_rangs)
        for r in range(RANG_MIN, nb_rangs+1):
            liste_r.append(r)
    elif (opt_r == OPT_MOINS):
        description += "- pour chaque rang du"
        description += " {0}ème au 1er,\n".format(nb_rangs)
        for r in range(nb_rangs, RANG_MIN-1, -1):
            liste_r.append(r)
    else:
        # opt_r == OPT_HASARD
        description += "- pour chaque rang (ordonnés au hasard),\n"
        for r in range(RANG_MIN, nb_rangs+1):
            liste_r.append(r)
        random.shuffle(liste_r)

    if (opt_x == OPT_PLUS):
        description += "- les passagers sont ordonnés "
        description += "du couloir vers l'extérieur,\n"
        for i in range(X_MIN, X_COULOIR):
            liste_x.append(X_COULOIR-i)
            liste_x.append(X_COULOIR+i)
    elif (opt_x == OPT_MOINS):
        description += "- les passagers sont ordonnés "
        description += "de l'extérieur vers le couloir,\n"
        for i in range(X_COULOIR-X_MIN, 0, -1):
            liste_x.append(X_COULOIR-i)
            liste_x.append(X_COULOIR+i)
    else:
        # opt_x == OPT_HASARD
        description += "- les passagers sont ordonnés au hasard,\n"
        for x in range(X_MIN, X_MAX+1):
            if (x != X_COULOIR):
                liste_x.append(x)
        random.shuffle(liste_x)

    for r in liste_r:
        if (opt_x == OPT_HASARD):
            random.shuffle(liste_x)
        for x in liste_x:
            liste_passagers.append(Passager(x, r, opt_b))

    description += descr_b
    return liste_passagers, description


# ----------
def passagers_sieges(nom, nb_rangs):
    liste_passagers = []
    description = "- {0} rangs,\n".format(nb_rangs)
    descr_b = "- nombre de bagages au hasard.\n"
    opt_r = OPT_HASARD
    opt_x = OPT_HASARD
    opt_b = BAGAGE_HASARD
    found_r = False
    found_b = False
    pass

    len_nom = len(nom)
    if (len_nom >= 2):
        opt_x = decode_opt(nom[1])

    if (len_nom >= 4):
        nom3 = nom[3]
        if (nom3 == "B") or (nom3 == "b"):
            found_b = True
            if (len_nom >= 5):
                opt_b, descr_b = decode_bag(nom[4])
        elif ((nom3 == "Y") or (nom3 == "y") or
              (nom3 == "R") or (nom3 == "r")):
            found_r = True
            if (len_nom >= 5):
                opt_r = decode_opt(nom[4])

    if (len_nom >= 7):
        nom6 = nom[6]
        if (not found_b) and ((nom6 == "B") or (nom6 == "b")):
            found_b = True
            if (len_nom >= 8):
                opt_b, descr_b = decode_bag(nom[7])
        elif (not found_r) and ((nom6 == "Y") or (nom6 == "y") or
                                (nom6 == "R") or (nom6 == "r")):
            found_r = True
            if (len_nom >= 8):
                opt_r = decode_opt(nom[7])

    liste_x = []
    liste_r = []
    if (opt_x == OPT_PLUS):
        description += "- pour chaque x du couloir vers l'extérieur,\n"
        for i in range(X_MIN, X_COULOIR):
            liste_x.append(X_COULOIR-i)
            liste_x.append(X_COULOIR+i)
    elif (opt_x == OPT_MOINS):
        description += "- pour chaque x de l'extérieur vers le couloir,\n"
        for i in range(X_COULOIR-X_MIN, 0, -1):
            liste_x.append(X_COULOIR-i)
            liste_x.append(X_COULOIR+i)
    else:
        # opt_x == OPT_HASARD
        description += "- pour chaque x (ordonnés au hasard),\n"
        for x in range(X_MIN, X_MAX+1):
            if (x != X_COULOIR):
                liste_x.append(x)
        random.shuffle(liste_x)

    if (opt_r == OPT_PLUS):
        description += "- les passagers sont ordonnés selon leur rang"
        description += " du 1er au {0}ème,\n".format(nb_rangs)
        for r in range(RANG_MIN, nb_rangs+1):
            liste_r.append(r)
    elif (opt_r == OPT_MOINS):
        description += "- les passagers sont ordonnés selon leur rang"
        description += " du {0}ème au 1er,\n".format(nb_rangs)
        for r in range(nb_rangs, RANG_MIN-1, -1):
            liste_r.append(r)
    else:
        # opt_r == OPT_HASARD
        description += "- les passagers sont ordonnés au hasard,\n"
        for r in range(RANG_MIN, nb_rangs+1):
            liste_r.append(r)
        random.shuffle(liste_r)

    for x in liste_x:
        if (opt_r == OPT_HASARD):
            random.shuffle(liste_r)
        for r in liste_r:
            liste_passagers.append(Passager(x, r, opt_b))

    description += descr_b
    return liste_passagers, description


# ----------
def creer_avion():
    """Creer un avion a partir du nom dans le champ de saisie"""
    # Le nom est soit 'Hasard' soit un code composé comme suit
    # nom[0] : objet pour la boucle externe - obligatoire
    # nom[1] : option pour la boucle externe - hasard par defaut
    # nom[2] : separateur, caractère quelconque
    # nom[3] : objet pour la boucle interne ou bagage
    # nom[4] : option pour la boucle interne ou bagage - hasard par defaut
    # nom[5] : separateur, caractère quelconque
    # nom[6] : objet pour la boucle interne ou bagage
    # nom[7] : option pour la boucle interne ou bagage - hasard par defaut
    #
    # Les codes des objets pour les boucles ou bagage sont :
    #  Y|y|R|r pour le Y|rang
    #  X|x|S|s pour le X|siège (ou cellule)
    #  B|b pour bagage
    #
    # Les options sont
    #  H|h -> hasard
    #  C|c|P|p -> croissant|plus
    #               pour rang et siege (du couloir vers l'extéreur)
    #  D|d|M|m -> décroissant|moins
    #               pour rang et siege (de l'extérieur vers le couloir)
    #  0|1|2 pour bagage (le nb pour tous les passagers)
    #  X|x|Y|y|Z|z pour bagage (un modulo sur x ou y ou x+y du passager)

    # print("--> creer_avion()")
    global champ_avion_text
    global champ_rangs_text
    global champ_delai_text
    global label_descr_text

    # passagers = [Passager(1, 1, 1), Passager(2, 2, 2), Passager(7, 3, 0)]

    new_avion = None
    nom_avion = champ_avion_text.get()
    nom0 = ""
    if (len(nom_avion) >= 1):
        nom0 = nom_avion[0]

    rangs_avion = int(champ_rangs_text.get())
    if (rangs_avion < RANG_MIN) or (rangs_avion > RANG_MAX):
        rangs_avion = RANG_MAX

    delai_avion = int(champ_delai_text.get())
    if (delai_avion < 10):
        delai_avion = 100

    descr = "Avion '" + nom_avion + "' :\n"
    if nom_avion == "Hasard":
        descr += "- {0} rangs,\n".format(rangs_avion)
        descr += "- ordre des passagers au hasard,\n"
        descr += "- nombre de bagages au hasard.\n"
        psgs_avion = passagers_hasard(rangs_avion)
        new_avion = Avion(nom_avion, rangs_avion, delai_avion)
        new_avion.remplir(psgs_avion)
        pass
    elif (nom0 == "R") or (nom0 == "r") or (nom0 == "Y") or (nom0 == "y"):
        psgs_avion, details = passagers_rangs(nom_avion, rangs_avion)
        descr += details
        new_avion = Avion(nom_avion, rangs_avion, delai_avion)
        new_avion.remplir(psgs_avion)
        pass
    elif (nom0 == "S") or (nom0 == "s") or (nom0 == "X") or (nom0 == "x"):
        psgs_avion, details = passagers_sieges(nom_avion, rangs_avion)
        descr += details
        new_avion = Avion(nom_avion, rangs_avion, delai_avion)
        new_avion.remplir(psgs_avion)
        pass
    else:
        descr += "\nINCONNU !\n\nEssayez à nouveau."

    if not (new_avion is None):
        descr += "\nDélai entre les étapes : {0} ms".format(delai_avion)
    label_descr_text.set(descr)

    # print("<-- creer_avion()")
    return new_avion


# ----------
def remplissage():
    """Lance l'etape suivante de remplissage de l'avion"""
    # print("--> remplissage()")
    global avion
    global appel_remplissage
    global frame_avion

    avion.etape_suivante()
    if avion.complet():
        # Avion complet, on arrête le remplissage
        appel_remplissage = None

        # Et on fait comme si le bouton Stop avait été utilisé
        reset_boutons()
    else:
        # Sinon on lance une nouvelle étape
        appel_remplissage = frame_avion.after(avion.delai, remplissage)

    # print("<-- remplissage()")


# ----------
def stop_remplissage():
    """Arrete le remplissage de l'avion"""
    # print("--> stop_remplissage()")
    global appel_remplissage
    global frame_avion

    if not (appel_remplissage is None):
        frame_avion.after_cancel(appel_remplissage)

    # print("<-- stop_remplissage()")


# ----------
# Remettre les boutons dans l'état par défaut.
def reset_boutons():
    # Changer le texte du bouton start
    bouton_start_text.set(BTN_START)

    # Rendre invisible les boutons pause et next
    bouton_pause.grid_remove()
    bouton_next.grid_remove()


# ----------
# Action du bouton pour lancer/arreter le remplissage de l'avion
def onClickBtnStart():
    # print("--> onClickBtnStart()")
    global avion
    global bouton_start_text
    global bouton_pause
    global bouton_pause_text

    if bouton_start_text.get() == BTN_START:
        # Créer un nouvel avion
        avion = creer_avion()

        # Lancer le remplissage de l'avion
        if not (avion is None):
            remplissage()

            # Changer le texte du bouton
            bouton_start_text.set(BTN_STOP)

            # Rendre visible le bouton pause
            bouton_pause_text.set(BTN_PAUSE_STOP)
            bouton_pause.grid()
    else:
        reset_boutons()

        # Arreter le remplissage de l'avion
        stop_remplissage()

    # print("<-- onClickBtnStart()")


# ----------
# Action du bouton pour mettre en pause/relancer le remplissage de l'avion
def onClickBtnPause():
    # print("--> onClickBtnPause()")
    global bouton_pause
    global bouton_pause_text
    global bouton_next

    if bouton_pause_text.get() == BTN_PAUSE_STOP:
        # Changer le texte du bouton
        bouton_pause_text.set(BTN_PAUSE_GO)

        # Rendre visible le bouton next
        bouton_next.grid()

        # Suspendre le remplissage de l'avion
        stop_remplissage()
    else:
        # Changer le texte du bouton
        bouton_pause_text.set(BTN_PAUSE_STOP)

        # Rendre invisible le bouton next
        bouton_next.grid_remove()

        # Relancer le remplissage de l'avion
        remplissage()

    # print("<-- onClickBtnPause()")


# ----------
# Action du bouton pour lancer l'étape suivante du remplissage de l'avion
def onClickBtnNext():
    # print("--> onClickBtnNext()")
    global avion

    avion.etape_suivante()
    if avion.complet():
        # On fait comme si le bouton Stop avait été utilisé
        reset_boutons()

    # print("<-- onClickBtnNext()")


######################
# programme principal

racine = tk.Tk()
racine.title("Remplissage d'un avion")

# ----------
# La fenetre est organisée en 4 frames :
# 3 dans la colone de gauche : les commandes, la description, les stats
# 1 dans la colone de droite pour la représentation de l'avion

# ----------
# Frame 1,1 les commandes :
frame_cdes = tk.Frame(racine)
frame_cdes.grid(column=0, row=0, padx=5, pady=5)

# ---> Un champ de saisie pour préciser l'avion à remplir
champ_avion_frame = tk.LabelFrame(frame_cdes, text="Avion",
                                  font=("helvetica", "10"))
champ_avion_frame.grid(column=0, row=0, columnspan=2, padx=2, pady=2)

champ_avion_text = tk.StringVar()
champ_avion_text.set("Hasard")
champ_avion = tk.Entry(champ_avion_frame, textvariable=champ_avion_text,
                       font=("helvetica", "12"))
champ_avion.grid(column=0, row=0, padx=2, pady=2)

# ---> Un champ de saisie pour préciser le nombre de rangs
champ_rangs_frame = tk.LabelFrame(frame_cdes, text="Nombre de rangs",
                                  font=("helvetica", "10"))
champ_rangs_frame.grid(column=0, row=1, padx=2, pady=2)

champ_rangs_text = tk.StringVar()
champ_rangs_text.set("30")
champ_rangs = tk.Entry(champ_rangs_frame, textvariable=champ_rangs_text,
                       font=("helvetica", "12"))
champ_rangs.grid(column=0, row=0, padx=2, pady=2)

# ---> Un champ de saisie pour préciser le délai entre les étapes
champ_delai_frame = tk.LabelFrame(frame_cdes, text="Délai (10 ms mini)",
                                  font=("helvetica", "10"))
champ_delai_frame.grid(column=1, row=1, padx=2, pady=2)

champ_delai_text = tk.StringVar()
champ_delai_text.set("500")
champ_delai = tk.Entry(champ_delai_frame, textvariable=champ_delai_text,
                       font=("helvetica", "12"))
champ_delai.grid(column=0, row=0, padx=2, pady=2)

# ---> Un bouton pour lancer/arreter le remplissage de l'avion
bouton_start_text = tk.StringVar()
bouton_start_text.set(BTN_START)
bouton_start = tk.Button(frame_cdes, textvariable=bouton_start_text,
                         command=onClickBtnStart, font=("helvetica", "12"))
bouton_start.grid(column=0, row=2, columnspan=2, padx=2, pady=2)

# ---> Un bouton pour mettre en pause/relancer le remplissage de l'avion
bouton_pause_text = tk.StringVar()
bouton_pause_text.set(BTN_PAUSE_STOP)
bouton_pause = tk.Button(frame_cdes, textvariable=bouton_pause_text,
                         command=onClickBtnPause, font=("helvetica", "12"))
bouton_pause.grid(column=0, row=3, padx=2, pady=2)
bouton_pause.grid_remove()

# ---> Un bouton pour lancer l'étape suivante du remplissage de l'avion
bouton_next = tk.Button(frame_cdes, text=BTN_NEXT,
                        command=onClickBtnNext, font=("helvetica", "12"))
bouton_next.grid(column=1, row=3, padx=2, pady=2)
bouton_next.grid_remove()

# ----------
# Frame 1,2 la description :
frame_descr = tk.LabelFrame(racine, text="Descrition",
                            font=("helvetica", "10"))
frame_descr.grid(column=0, row=1, padx=5, pady=5)

# ---> Un label pour afficher la description du cas
label_descr_text = tk.StringVar()
label_descr_text.set("....................................\n\n\n\n...")
label_descr = tk.Label(frame_descr, textvariable=label_descr_text,
                       justify="left", font=("helvetica", "12"))
label_descr.grid(column=0, row=0)

# ----------
# Frame 1,3 les stats :
frame_stats = tk.LabelFrame(racine, text="Statistiques",
                            font=("helvetica", "10"))
frame_stats.grid(column=0, row=2, padx=5, pady=5)

# La classe qui crée les labels pour afficher les données statistiques
# du remplissage
stats = Statistiques(frame_stats)

# ----------
# Frame 2,0 : la représentation de l'avion :
frame_avion = tk.Frame(racine)
frame_avion.grid(column=1, row=0, rowspan=3, padx=5, pady=5)

avion_largeur = X_MAX * (CELL_LARGEUR+2)
avion_hauteur = (RANG_MAX+1) * (CELL_HAUTEUR+2)
arrow_x = X_COULOIR * (CELL_LARGEUR+2) - (CELL_LARGEUR // 2)
# ---> Une zone de dessin pour représenter l'avion
canvas_avion = tk.Canvas(frame_avion, bg=COUL_DEFAUT,
                         width=avion_largeur, height=avion_hauteur)
canvas_avion.grid(column=0, row=0)
arrow_in = canvas_avion.create_line(arrow_x, 0, arrow_x, CELL_HAUTEUR,
                                    arrow='last', fill=COUL_COULOIR_VIDE,
                                    width=2)

# ----------
# Création des rangs (Rang idx 0 nou used)
liste_rangs = [None]
for r in range(RANG_MIN, RANG_MAX+1):
    liste_rangs.append(Rang(y=r, canvas=canvas_avion))


# Variables globales utilisées
avion = None
appel_remplissage = None

racine.mainloop()
