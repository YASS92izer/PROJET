import tkinter as tk
from tkinter import messagebox

# Données de connexion fictives
UTILISATEUR_ATTENDU = "admin"
MOT_DE_PASSE_ATTENDU = "1234"

def verifier_identification():
    """Vérifie si l'utilisateur et le mot de passe sont corrects."""
    utilisateur = entry_utilisateur.get()
    mot_de_passe = entry_mot_de_passe.get()
    
    if utilisateur == UTILISATEUR_ATTENDU and mot_de_passe == MOT_DE_PASSE_ATTENDU:
        messagebox.showinfo("Succès", "Connexion réussie !")
    else:
        messagebox.showerror("Erreur", "Nom d'utilisateur ou mot de passe incorrect.")

# Création de la fenêtre principale
fenetre = tk.Tk()
fenetre.title("Connexion")
fenetre.geometry("300x200")

# Label et champ de saisie pour le nom d'utilisateur
tk.Label(fenetre, text="Nom d'utilisateur :").pack(pady=5)
entry_utilisateur = tk.Entry(fenetre)
entry_utilisateur.pack(pady=5)

# Label et champ de saisie pour le mot de passe
tk.Label(fenetre, text="Mot de passe :").pack(pady=5)
entry_mot_de_passe = tk.Entry(fenetre, show="*")
entry_mot_de_passe.pack(pady=5)

# Bouton de connexion
btn_connexion = tk.Button(fenetre, text="Se connecter", command=verifier_identification)
btn_connexion.pack(pady=10)

# Lancement de l'interface
fenetre.mainloop()
