import tkinter as tk
from tkinter import messagebox
import random

# Création de la fenêtre
fenetre_principal = tk.Tk()
fenetre_principal.minsize(600, 600)
fenetre_principal.config(bg="#09404c")
fenetre_principal.title("Tic Tac Toe")


# fonction pour jouer contre l'IA
def jouer_ia():
    global joueur
    global tableau
    global label_joueur
    global partie_en_cours

    # verifier si la partie est en cours et si c'est au tour de l'IA
    if partie_en_cours and joueur == "O": #si c'est au tour de l'IA représenter par O
        position_dispo = [i for i in range(9) if tableau[i] == " "] #liste des positions disponibles dans le tableau de jeu 
        
        # verifier si la liste des positions disponibles n'est pas vide et si c'est le cas, on choisit une position au hasard
        if position_dispo:
            position_ia = random.choice(position_dispo)
            
            # appel de la fonction jouer pour jouer avec un délai de 800 millisecondes
            fenetre_principal.after(800, lambda: jouer(position_ia))


# fonction pour jouer
def jouer(position):
    global joueur
    global tableau
    global label_joueur
    global partie_en_cours

    # Si la partie est en cours et que la case est vide, on joue
    if partie_en_cours and tableau[position] == " ":
        tableau[position] = joueur
        afficher_tableau(tableau)

    gagnant = verifier_victoire()

    # Si un joueur a gagné, on affiche un message et on désactive les boutons
    if gagnant:
        messagebox.showinfo("Fin de la partie", f"Le joueur {gagnant} a gagné !")
        desactiver_boutons(cadre_tableau)
        label_joueur.config(text=f"Le joueur {gagnant} a gagné !")
    elif " " not in tableau:
        messagebox.showinfo("Fin de la partie", "Match nul !")
        desactiver_boutons(cadre_tableau)
        label_joueur.config(text="Match nul !")
    else:
        joueur = "O" if joueur == "X" else "X"
        label_joueur.config(text="Joueur " + joueur)
        jouer_ia()

# fonction pour rejouer
def rejouer():
    global tableau
    global partie_en_cours
    global label_joueur
    global joueur

    # Réinitialisation du tableau et de la partie
    tableau = [" "] * 9
    partie_en_cours = True  # la partie est en cours tant qu'il y a des cases vides dans le tableau
    afficher_tableau(tableau)

    # Réinitialisation du label du joueur permettant d'afficher le joueur qui doit jouer
    label_joueur.config(text=f"Joueur {joueur}")
    for bouton in cadre_tableau.winfo_children():  # boucle pour parcourir les boutons du tableau et les activer. winfo_children() permet de récupérer les widgets enfants du cadre
        bouton.config(state="normal")  # config permet de modifier les paramètres d'un widget (ici, on modifie l'état des boutons)

# fonction pour quitter le jeu
def quitter():
    fenetre_principal.destroy()

# fonction pour désactiver les boutons du tableau
def desactiver_boutons(cadre):
    for bouton in cadre.winfo_children():
        bouton.config(state="disabled")

# fonction pour vérifier si un joueur a gagné
def verifier_victoire():

    # boucle pour verifier les lignes 
    for i in range(3):
        if tableau[i * 3] == tableau[i * 3 + 1] == tableau[i * 3 + 2] != " ":
            return tableau[i * 3]
    
    # boucle pour vérifier les colonnes
    for i in range(3):
        if tableau[i] == tableau[i + 3] == tableau[i + 6] != " ":
            return tableau[i]

    # vérifier les diagonales 
    if tableau[0] == tableau[4] == tableau[8] != " ":
        return tableau[0]

    # vérifier les diagonales inversées
    if tableau[2] == tableau[4] == tableau[6] != " ":
        return tableau[2]

    return None

cadre_tableau = None
# fonction pour afficher le tableau de jeu dans la fenêtre
def afficher_tableau(tableau):
    global cadre_tableau
    # Si le tableau existe déjà, on le met à jour
    if cadre_tableau:
        # boucle pour parcourir les lignes et les colonnes du tableau
        for lignes in range(3):
            for colonnes in range(3):
                symbole = tableau[lignes * 3 + colonnes]

                # Si le symbole est X, on affiche le texte en rouge
                if symbole == "X":
                    cadre_tableau.boutons[lignes][colonnes].config(text=symbole, fg="black", bd=5)
                # Si le symbole est O, on affiche le texte en bleu
                elif symbole == "O":
                    cadre_tableau.boutons[lignes][colonnes].config(text=symbole, fg="white", bd=5)
                # Sinon, on affiche le texte en noir
                else:
                    cadre_tableau.boutons[lignes][colonnes].config(text=symbole, fg="black")

    # autrement, on crée le tableau
    else:
        cadre_tableau = tk.Frame(fenetre_principal)
        cadre_tableau.boutons = []

        # boucle pour parcourir les lignes et les colonnes du tableau
        for lignes in range(3):
            ligne_boutons = []
            for colonnes in range(3):
                bouton = tk.Button(cadre_tableau, text=tableau[lignes * 3 + colonnes], font=("arial", 50), width=3,
                                   height=1, command=lambda position=lignes * 3 + colonnes: jouer(position))
                bouton.grid(row=lignes, column=colonnes)
                bouton.config(bg="#f2b615", border=5, relief="raised")
                ligne_boutons.append(bouton)

            cadre_tableau.boutons.append(ligne_boutons)

        cadre_tableau.grid(row=1, column=0, padx=150, pady=50, sticky="nsew")

        # Configuration du cadre du tableau pour qu'il s'adapte à la fenêtre
        for i in range(3):
            fenetre_principal.grid_rowconfigure(i, weight=10)
            fenetre_principal.grid_columnconfigure(i, weight=10)

    return cadre_tableau

# Création d'un tableau vide
tableau = [" "] * 9

# Création du label pour afficher le joueur qui doit jouer
joueur = "X"
partie_en_cours = True

label_joueur = tk.Label(fenetre_principal, text="Joueur " + joueur, font=('Arial', 30), bg="#09404c", fg="white")
label_joueur.grid(row=2, column=0, padx=120, pady=30, sticky="nsew")

# Affichage du tableau dans la fenêtre
afficher_tableau(tableau)
jouer_ia()


# Affichage de la fenêtre Tkinter
fenetre_principal.mainloop()
