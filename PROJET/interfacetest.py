import tkinter as tk
from tkinter import messagebox

# Données de connexion fictives
UTILISATEUR_ATTENDU = "admin"
MOT_DE_PASSE_ATTENDU = "1234"

# Fonction pour vérifier l'identification
def verifier_identification():
    utilisateur = entry_utilisateur.get()
    mot_de_passe = entry_mot_de_passe.get()
    if utilisateur == UTILISATEUR_ATTENDU and mot_de_passe == MOT_DE_PASSE_ATTENDU:
        afficher_saisie()
    else:
        messagebox.showerror("Erreur", "Nom d'utilisateur ou mot de passe incorrect.")

# Fonction pour enregistrer les données
def enregistrer_donnees():
    nom_patient = entry_nom_patient.get()
    hemoglobine = entry_hemoglobine.get()
    glucose = entry_glucose.get()
    cholesterol = entry_cholesterol.get()

    if not (nom_patient and hemoglobine and glucose and cholesterol):
        messagebox.showerror("Erreur", "Veuillez remplir tous les champs.")
        return

    try:
        with open("resultats.txt", "a") as fichier:
            fichier.write(f"Patient : {nom_patient}\n")
            fichier.write(f"Hémoglobine : {hemoglobine} g/dL\n")
            fichier.write(f"Glucose : {glucose} g/L\n")
            fichier.write(f"Cholestérol : {cholesterol} g/L\n")
            fichier.write("-" * 30 + "\n")
        messagebox.showinfo("Succès", "Données enregistrées avec succès !")
    except Exception as e:
        messagebox.showerror("Erreur", f"Impossible d'enregistrer les données : {e}")
    finally:
        entry_nom_patient.delete(0, tk.END)
        entry_hemoglobine.delete(0, tk.END)
        entry_glucose.delete(0, tk.END)
        entry_cholesterol.delete(0, tk.END)

# Changer de frame
def afficher_connexion():
    frame_saisie.pack_forget()
    frame_connexion.pack(pady=20, padx=20, fill="both", expand=True)

def afficher_saisie():
    frame_connexion.pack_forget()
    frame_saisie.pack(pady=20, padx=20, fill="both", expand=True)

# Fenêtre principale
app = tk.Tk()
app.title("Application Médicale")
app.geometry("600x500")

# Frame de connexion
frame_connexion = tk.Frame(app)
frame_connexion.pack(pady=20, padx=20, fill="both", expand=True)

tk.Label(frame_connexion, text="Nom d'utilisateur :").pack(pady=5)
entry_utilisateur = tk.Entry(frame_connexion)
entry_utilisateur.pack(pady=5)

tk.Label(frame_connexion, text="Mot de passe :").pack(pady=5)
entry_mot_de_passe = tk.Entry(frame_connexion, show="*")
entry_mot_de_passe.pack(pady=5)

btn_connexion = tk.Button(frame_connexion, text="Se connecter", command=verifier_identification)
btn_connexion.pack(pady=10)

# Frame de saisie
frame_saisie = tk.Frame(app)

tk.Label(frame_saisie, text="Nom du Patient :").pack(pady=5)
entry_nom_patient = tk.Entry(frame_saisie)
entry_nom_patient.pack(pady=5)

tk.Label(frame_saisie, text="Hémoglobine (g/dL) :").pack(pady=5)
entry_hemoglobine = tk.Entry(frame_saisie)
entry_hemoglobine.pack(pady=5)

tk.Label(frame_saisie, text="Glucose (g/L) :").pack(pady=5)
entry_glucose = tk.Entry(frame_saisie)
entry_glucose.pack(pady=5)

tk.Label(frame_saisie, text="Cholestérol (g/L) :").pack(pady=5)
entry_cholesterol = tk.Entry(frame_saisie)
entry_cholesterol.pack(pady=5)

btn_enregistrer = tk.Button(frame_saisie, text="Enregistrer", command=enregistrer_donnees)
btn_enregistrer.pack(pady=10)

btn_retour = tk.Button(frame_saisie, text="Déconnexion", command=afficher_connexion)
btn_retour.pack(pady=10)

# Afficher le frame de connexion par défaut
afficher_connexion()

# Lancer l'application
app.mainloop()
