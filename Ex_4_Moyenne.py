fic_in = open("notes_IN200", "r")
fic_out = open("moyenne", "w")

for ligne in fic_in:
    print(ligne)

fic_out.close()
fic_in.close()
