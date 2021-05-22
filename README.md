# Projet-Avion
Bonjour,

Nous sommes heureux de vous présenter, en tant que groupe, notre simulation d'embarquement aérien.
Tout d'abord, voici les personnes ayant contribué au projet ainsi que nos tâches respectives:

-Julie CIESLA 22003761: Les fonctions de déplacement des passagers (de convertit_siege_identifiant à déplace_1_passager), ainsi que la fenêtre d'information.

-Kubilay MEYDAN 22004090: Responsable Git, fonctionnement des boutons de commande, écriture du README 
 (PS, j’ai fait mes commits de 2 ordinateurs donc soit “Kubilay Meydan”, soit “uvsq22004090”).
 
-Elise REBER 21929616: Gestion de l’interface graphique.

-Alix FRAGNER 22006323: Génération de la liste des passagers avec leur destination. 

-Margaux DUBOIS 21803447: Responsable flake8, mise en place du compteur d'étapes et contribution aux fonctions 'Swipe' et 'déplace_1_passager'. (J'ai tenté de modifier les variables avec des indices de liste très longs, mais certaines variables faisaient bugger le code une fois ramplacées.)

Code couleur:

La simulation présente une rangée du milieu où les passagers circulent, pour s'installer dans les 3 rangées de droite, ou les 3 de gauche.
La couleur grise correspond à un siège vacant, ou au couloir.
Un carré vert correspond à une place occupée, autrement dit à un passager installé.
Un passager rose est un passager sans bagage. 
Un passager violet clair est un passager avec 1 bagage, un passager violet foncé est un passager avec 2 bagages.

Prise en main:

L’interface présente 4 boutons en position haute (Démarrer, Recommencer, Arrêt, et Information). 
L’appui sur ‘Démarrer’ lance la simulation à une vitesse moyenne. Le bouton 'Recommencer' permet de recommencer, comme son nom l’indique, la simulation à zéro, en régénérant les informations des passagers de manière aléatoire. Le bouton arrêt permet d'arrêter la simulation en cours, peu importe son avancement. Et finalement, le bouton ‘information’ est une simple fenêtre d’information permettant de rappeler le code couleur de la simulation.

Passons maintenant aux boutons à gauche de l’avion, les boutons ‘Pause’, ‘Relancer’, ‘Étape +1’, ‘étape par étape'.
Le bouton Pause, si pressé, met la simulation en pause jusqu'à ce qu’on appuie sur ‘Relancer’, qui remet la simulation en marche à un rythme moyen. La fonction ‘Etape+1’ permet de montrer l'étape de la simulation à l'étape suivante, et le bouton étape par étape sert à visionner chaque étape de la simulation avec un rythme idéal pour voir les changements. 
Petit Bonus, il y a un Slider pour gérer le temps qu’il y a entre les étapes, plus de temps entre les étapes = une simulation plus lente, moins de temps = une simulation plus rapide.

