import customtkinter as ctk
from tkinter import messagebox
import csv
import os
from PIL import Image, ImageTk

# Configuration de l'application
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

BG_COLOR = "#FFFFFF"
BTN_COLOR = "#4C89A4"
TEXT_COLOR = "#1C2A3A"
FRAME_BG = "#D3D3D3"
LOGO_PATH = "logo.png"
FICHIER_DONNEES = "donnees.csv"

CHAMPS_PATIENT = [
    "PatientID", "utilisateur", "mdp", "Sexe", "Age",
    "GlobulesRouges", "Hemoglobine", "GlobulesBlancs", "Plaquettes",
    "GlycemieAJjeun", "CholesterolTotal", "HDL", "LDL", "Triglycerides",
    "ASAT", "ALAT", "GammaGT", "Bilirubine", "Creatinine", "Uree",
    "Sodium", "Potassium", "Chlore", "CRP", "TSH", "Fer", "Ferritine"
]

CHAMPS_PAGES = [
    [
        {"titre": "Numération Sanguine", "elements": {
            "GlobulesRouges": ("M/µL"), "Hemoglobine": ("g/dL"),
            "GlobulesBlancs": ("K/µL"), "Plaquettes": ("K/µL")}},
        {"titre": "Glycémie & Lipides", "elements": {
            "GlycemieAJjeun": ("mg/dL"), "CholesterolTotal": ("mg/dL"),
            "HDL": ("mg/dL"), "LDL": ("mg/dL"), "Triglycerides": ("mg/dL")}}
    ],
    [
        {"titre": "Fonction Hépatique & Rénale", "elements": {
            "ASAT": ("U/L"), "ALAT": ("U/L"), "GammaGT": ("U/L"), "Bilirubine": ("mg/dL"),
            "Creatinine": ("mg/dL"), "Uree": ("mg/dL"), "Sodium": ("mmol/L"),
            "Potassium": ("mmol/L"), "Chlore": ("mmol/L")}},
        {"titre": "Inflammation, Thyroïde et Fer", "elements": {
            "CRP": ("mg/L"), "TSH": ("mIU/L"), "Fer": ("µg/dL"), "Ferritine": ("ng/mL")}}
    ]
]

mode_inscription = False
donnees_patient = {}

app = ctk.CTk()
app.title("Interface Médicale")
app.geometry("1200x700")
app.state("zoomed")
app.configure(bg=BG_COLOR)

valeurs_donnees = {}

frame_connexion = ctk.CTkFrame(app, fg_color=BG_COLOR)
frame_connexion.pack(fill="both", expand=True)

# Ajout du logo
try:
    logo_img = Image.open(LOGO_PATH)
    logo_img = logo_img.resize((150, 150))
    logo_photo = ImageTk.PhotoImage(logo_img)
    logo_label = ctk.CTkLabel(frame_connexion, image=logo_photo, text="")
    logo_label.image = logo_photo
    logo_label.pack(pady=20)
except Exception as e:
    print("Erreur de chargement du logo:", e)

ctk.CTkLabel(frame_connexion, text="Utilisateur").pack(pady=5)
entry_utilisateur = ctk.CTkEntry(frame_connexion)
entry_utilisateur.pack(pady=5)

ctk.CTkLabel(frame_connexion, text="Mot de passe").pack(pady=5)
entry_mot_de_passe = ctk.CTkEntry(frame_connexion, show="*")
entry_mot_de_passe.pack(pady=5)

entry_sexe = ctk.CTkEntry(frame_connexion, placeholder_text="Sexe")
entry_age = ctk.CTkEntry(frame_connexion, placeholder_text="Âge")

btn_login = ctk.CTkButton(frame_connexion, text="Connexion", fg_color=BTN_COLOR, command=lambda: verifier_identification())
btn_login.pack(pady=5)

btn_register = ctk.CTkButton(frame_connexion, text="S'inscrire", fg_color=BTN_COLOR, command=lambda: activer_inscription())
btn_register.pack(pady=5)

frame_saisie_1 = ctk.CTkFrame(app, fg_color=BG_COLOR)
frame_saisie_2 = ctk.CTkFrame(app, fg_color=BG_COLOR)

def activer_inscription():
    global mode_inscription
    mode_inscription = True
    entry_sexe.pack(pady=5)
    entry_age.pack(pady=5)
    btn_valider = ctk.CTkButton(frame_connexion, text="Valider l'inscription", fg_color=BTN_COLOR, command=valider_inscription)
    btn_valider.pack(pady=5)

def valider_inscription():
    nom = entry_utilisateur.get()
    mdp = entry_mot_de_passe.get()
    sexe = entry_sexe.get()
    age = entry_age.get()
    if not nom or not mdp or not sexe or not age:
        messagebox.showerror("Erreur", "Veuillez remplir tous les champs")
        return
    donnees = lire_donnees()
    for ligne in donnees:
        if ligne['utilisateur'] == nom:
            messagebox.showerror("Erreur", "Utilisateur déjà existant")
            return
    with open(FICHIER_DONNEES, 'a', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=CHAMPS_PATIENT)
        if os.stat(FICHIER_DONNEES).st_size == 0:
            writer.writeheader()
        writer.writerow({"PatientID": len(donnees)+1, "utilisateur": nom, "mdp": mdp, "Sexe": sexe, "Age": age})
    messagebox.showinfo("Succès", "Inscription réussie")
    frame_connexion.pack_forget()
    frame_saisie_1.pack(fill="both", expand=True)

def lire_donnees():
    if not os.path.exists(FICHIER_DONNEES):
        return []
    with open(FICHIER_DONNEES, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        return list(reader)

def verifier_identification():
    nom = entry_utilisateur.get()
    mdp = entry_mot_de_passe.get()
    donnees = lire_donnees()
    for ligne in donnees:
        if ligne['utilisateur'] == nom and ligne['mdp'] == mdp:
            donnees_patient.update(ligne)
            frame_connexion.pack_forget()
            frame_saisie_1.pack(fill="both", expand=True)
            return
    messagebox.showerror("Erreur", "Identifiants incorrects")

def afficher_saisie_2():
    frame_saisie_1.pack_forget()
    frame_saisie_2.pack(fill="both", expand=True)

def enregistrer_donnees():
    for key in valeurs_donnees:
        val = valeurs_donnees[key].get()
        if val == "":
            messagebox.showerror("Erreur", f"Champ vide: {key}")
            return
        donnees_patient[key] = float(val)
    messagebox.showinfo("Succès", "Données enregistrées dans le dictionnaire")
    frame_saisie_2.pack_forget()

def creer_interface_saisie():
    global valeurs_donnees
    for page_index, page in enumerate(CHAMPS_PAGES):
        frame = frame_saisie_1 if page_index == 0 else frame_saisie_2
        for section in page:
            frame_section = ctk.CTkFrame(frame, fg_color=FRAME_BG)
            frame_section.pack(padx=10, pady=10, fill="x")
            ctk.CTkLabel(frame_section, text=section["titre"], font=("Arial", 16, "bold")).pack(pady=5)
            for champ, unite in section["elements"].items():
                line = ctk.CTkFrame(frame_section, fg_color=FRAME_BG)
                line.pack(fill="x", padx=10, pady=2)
                ctk.CTkLabel(line, text=f"{champ} ({unite})").pack(side="left")
                entry = ctk.CTkEntry(line, width=120)
                entry.pack(side="right")
                valeurs_donnees[champ] = entry

    ctk.CTkButton(frame_saisie_1, text="Suivant", fg_color=BTN_COLOR, command=afficher_saisie_2).pack(pady=10)
    ctk.CTkButton(frame_saisie_2, text="Valider", fg_color=BTN_COLOR, command=enregistrer_donnees).pack(pady=10)

creer_interface_saisie()
app.mainloop()
