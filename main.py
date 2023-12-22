import tkinter as tk
from tkinter import messagebox
import os

# Création de la fenêtre
fenetre_principal = tk.Tk()
fenetre_principal.minsize(600, 600)
fenetre_principal.config(bg="#09404c")
fenetre_principal.title("Tic Tac Toe")

cadre_tableau = None

# fonction pour définir les options du menu*
def option(option_index):


    if option_index == 0:  # Rejouer
        rejouer()
        choisir_symbole()
    elif option_index == 1:
       jouer_ia()
        
    elif option_index == 2:  # Quitter
        quitter()

# fonction pour afficher le menu
def afficher_menu():
    global menu_options
    global fenetre_principal

    # Création du menu principal avec les options définies dans le tableau menu_options 
    menu = tk.Menu(fenetre_principal) 

    # Boucle pour ajouter les options du menu   
    for i in range(len(menu_options)): 
        menu.add_command(label=menu_options[i], command=lambda option_index=i: option(option_index))
        
    # Affichage du menu dans la fenêtre
    fenetre_principal.config(menu=menu)
    

# fonction choisir symbole 
def choisir_symbole():
    global joueur
    global label_joueur

    # Boîte de dialogue pour choisir le symbole
    choix_symbole = messagebox.askquestion("Choix du Symbole", "Voulez-vous jouer avec X ?")

    # Si le joueur choisit X, il commence à jouer
    if choix_symbole == "yes":
        joueur = "X"
    # Sinon, c'est O
    else:
        joueur = "O"

    label_joueur.config(text=f"Joueur {joueur}")

# fonction pour rejouer 
def rejouer():
    global tableau
    global partie_en_cours
    global label_joueur

    # Réinitialisation du tableau et de la partie 
    tableau = [" "] * 9 
    partie_en_cours = True # la partie est en cours tant qu'il y a des cases vides dans le tableau 
    afficher_tableau(tableau)
    
    # Réinitialisation du label du joueur permettant d'afficher le joueur qui doit jouer
    label_joueur.config(text=f"Joueur {joueur}")
    for bouton in cadre_tableau.winfo_children(): # boucle pour parcourir les boutons du tableau et les activer. winfo_children() permet de récupérer les widgets enfants du cadre
        bouton.config(state="normal") # config permet de modifier les paramètres d'un widget (ici, on modifie l'état des boutons)


# fonction pour quitter le jeu 
def quitter():
    fenetre_principal.destroy()

# Définir les options du menu
menu_options = ["REJOUER","JOUER VS ORDI", "QUITTER"]

# Afficher les options du menu principal
afficher_menu()

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
                    cadre_tableau.boutons[lignes][colonnes].config(text=symbole, fg="black", bd= 5)
                # Si le symbole est O, on affiche le texte en bleu 
                elif symbole == "O":
                    cadre_tableau.boutons[lignes][colonnes].config(text=symbole, fg="white", bd= 5)
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

            # boucle pour créer les boutons du tableau
            for colonnes in range(3):
                bouton = tk.Button(cadre_tableau, text=tableau[lignes * 3 + colonnes], font=("arial", 50),width=3, height=1, command=lambda position=lignes * 3 + colonnes: jouer(position))
                bouton.grid(row=lignes, column=colonnes)
                bouton.config(bg="#f2b615", border=5, relief="raised")
                ligne_boutons.append(bouton)

            # Ajout de la ligne de boutons dans le tableau
            cadre_tableau.boutons.append(ligne_boutons)

        # Ajout du tableau dans la fenêtre
        cadre_tableau.grid(row=0, column=0, padx=100, pady=50)

    # Configuration du cadre du tableau pour qu'il s'adapte à la fenêtre
        for i in range(3):
            fenetre_principal.grid_rowconfigure(i, weight=1) # weight permet de définir la priorité d'extension de la ligne ou de la colonne
            fenetre_principal.grid_columnconfigure(i, weight=1) # ici, on définit la priorité à 1 pour que le tableau s'adapte à la fenêtre

    return cadre_tableau

# fonction pour jouer 
def jouer(position):
    global joueur 
    global tableau
    global label_joueur

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
        


# fonction pour désactiver les boutons du tableau
def desactiver_boutons(cadre):
    for bouton in cadre.winfo_children():
        bouton.config(state="disabled")

# fonction pour jouer contre l'ordinateur
def jouer_ia():
    os.system("python ia.py") # permet d'exécuter le fichier ia.py

# fonction pour vérifier si un joueur a gagné  
def verifier_victoire():

    # verifier la victoire sur les lignes
    for i in range(3):
        if tableau[i * 3] == tableau[i * 3 + 1] == tableau[i * 3 + 2] != " ":
            return tableau[i * 3]

    # verifier la victoire sur les colonnes
    for i in range(3):
        if tableau[i] == tableau[i + 3] == tableau[i + 6] != " ": 
            return tableau[i]

    # verifier la victoire sur les diagonales
    if tableau[0] == tableau[4] == tableau[8] != " ":
        return tableau[0]

    # verifier la victoire sur les diagonales
    if tableau[2] == tableau[4] == tableau[6] != " ":
        return tableau[2]

    return None

# Création d'un tableau vide
tableau = [" "] * 9

# Initialisation des variables joueur et partie_en_cours
joueur = "X"
partie_en_cours = True

# Création du label pour afficher le joueur qui doit jouer
label_joueur = tk.Label(fenetre_principal, text="Joueur " + joueur, font=('Arial', 30), bg="#09404c", fg="white")
label_joueur.grid(row=2, column=0, padx=120, pady=30, sticky="nsew")


# Affichage du tableau dans la fenêtre
afficher_tableau(tableau)
if messagebox.askyesno("Choix du Joueur", "Voulez-vous choisir votre joueur ? "):
    choisir_symbole()


# Affichage de la fenêtre Tkinter
fenetre_principal.mainloop()