import customtkinter as ctk
from datetime import datetime

class SaisieDonnees:
    def __init__(self, main_frame, gestionnaire, patient_data):
        self.main_frame = main_frame
        self.gestionnaire = gestionnaire

        # Récupération des données du patient
        self.patient_id = patient_data.get('PatientID', 0)
        self.sexe = patient_data.get('Sexe', 'Homme')
        self.age = patient_data.get('Age', 0)

        
        self.fond = "#FFFFFF"          
        self.card_bg = "white"        
        self.accent = "#042C54"        
        self.texte = "#042C54"         
        self.btn_text_color = "white"  
        self.message_err = "#FB9488"   
        self.message_succes = "#00B386" 

    def ouvrir_saisie(self):
        # Nettoyer l'affichage
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        fond = self.fond
        accent = self.accent
        texte = self.texte

        # Titre principal
        titre = ctk.CTkLabel(
            self.main_frame,
            text="Saisie des données médicales",
            font=("Arial", 26, "bold"),
            text_color=texte,
            fg_color=fond
        )
        titre.pack(fill="x", pady=20)

        # Message d'erreur / info
        self.message_frame = ctk.CTkFrame(self.main_frame, fg_color=fond)
        self.message_frame.pack(fill='x', padx=20, pady=10)
        self.message_label = ctk.CTkLabel(
            self.message_frame,
            text="",
            font=("Arial", 14),
            text_color=self.message_err,
            fg_color=fond
        )
        self.message_label.pack()

        categories = {
            "Hématologie": ["Globules Rouges", "Hémoglobine", "Globules Blancs", "Plaquettes"],
            "Biochimie": ["Glycémie à jeun", "Créatinine", "Urée", "Fer", "Ferritine"],
            "Lipides": ["Cholestérol Total", "HDL", "LDL", "Triglycérides"],
            "Enzymes": ["ASAT", "ALAT", "Gamma GT"],
            "Ionogramme": ["Sodium", "Potassium", "Chlore"],
            "Autres": ["Bilirubine", "CRP", "TSH"],
        }

        self.entries = {}

        cartes_par_ligne = 3
        cat_items = list(categories.items())

        for i in range(0, len(cat_items), cartes_par_ligne):
            # Frame conteneur pour chaque ligne de cartes
            ligne = ctk.CTkFrame(self.main_frame, fg_color=fond)
            ligne.pack(anchor="center", pady=10)
            for titre_carte, champs in cat_items[i:i+cartes_par_ligne]:
                frame = self.creer_carte(ligne, titre_carte, champs)
                self.entries[titre_carte] = frame

        # Frame contenant la date
        date_frame = ctk.CTkFrame(self.main_frame, fg_color=fond)
        date_frame.pack(anchor="center", pady=10)

        date_label = ctk.CTkLabel(
            date_frame,
            text="Date du bilan",
            font=("Arial", 14),
            text_color=texte,
            fg_color=fond
        )
        date_label.pack(side="left", padx=(0, 10))

        date_defaut = datetime.now().strftime("%Y-%m-%d")

        self.date_entry = ctk.CTkEntry(
            date_frame,
            width=200,
            fg_color="white",
            text_color=accent,
            border_color=accent,
            border_width=1,
            corner_radius=6,
            placeholder_text="AAAA-MM-JJ"
        )
        self.date_entry.insert(0, date_defaut)
        self.date_entry.pack(side="left", padx=10)

        # Bouton enregistrer 
        btn_frame = ctk.CTkFrame(self.main_frame, fg_color=fond)
        btn_frame.pack(anchor="center", pady=20)

        btn_enregistrer = ctk.CTkButton(
            btn_frame,
            text="Enregistrer les données",
            fg_color=accent,
            hover_color="#034B70",  
            text_color=self.btn_text_color,
            corner_radius=15,
            font=("Arial", 16, "bold"),
            command=self.valider_et_enregistrer,
            width=250,
            height=45
        )
        btn_enregistrer.pack()

    def creer_carte(self, parent, titre_section, champs):
        # Cartes pour zone saisie
        card_bg = self.card_bg
        accent = self.accent
        texte = self.texte

        frame = ctk.CTkFrame(parent, fg_color=card_bg, corner_radius=15, border_width=1, border_color=accent)
        frame.pack(side="left", padx=20, pady=10)

        label_titre = ctk.CTkLabel(
            frame,
            text=titre_section,
            font=("Arial", 20, "bold"),
            text_color=texte,
            fg_color=card_bg
        )
        label_titre.pack(pady=15)

        entrees_carte = {}

        for champ in champs:
            
            ligne = ctk.CTkFrame(frame, fg_color=card_bg)
            ligne.pack(padx=15, pady=8, anchor="w")

            label = ctk.CTkLabel(
                ligne,
                text=champ,
                width=200,
                anchor="w",
                font=("Arial", 14),
                text_color=texte,
                fg_color=card_bg
            )
            label.pack(side="left")

            entry = ctk.CTkEntry(
                ligne,
                width=150,
                fg_color="white",
                text_color=accent,
                border_color=accent,
                border_width=1,
                corner_radius=6
            )
            entry.pack(side="left", padx=10)

            entrees_carte[champ] = entry

        return entrees_carte

    def valider_et_enregistrer(self):
        self.message_label.configure(text="", text_color=self.message_err)

        try:
            donnees_medicales = {
                'PatientID': self.patient_id,
                'Sexe': self.sexe,
                'Age': self.age,
                'Date': self.date_entry.get()
            }

            for section, champs in self.entries.items():
                for nom_champ, champ_entry in champs.items():
                    valeur = champ_entry.get().strip()
                    if not valeur:
                        self.message_label.configure(
                            text=f"Le champ '{nom_champ}' ne peut pas être vide.",
                            text_color=self.message_err
                        )
                        return
                    try:
                        valeur_float = float(valeur)
                        donnees_medicales[nom_champ] = valeur_float
                    except ValueError:
                        self.message_label.configure(
                            text=f"Valeur invalide pour '{nom_champ}': {valeur}",
                            text_color=self.message_err
                        )
                        return

            resultat = self.gestionnaire.ajouter_bilan(donnees_medicales)
            if resultat:
                self.message_label.configure(
                    text="✅ Données médicales enregistrées avec succès !",
                    text_color=self.message_succes
                )
                for champs in self.entries.values():
                    for entry in champs.values():
                        entry.delete(0, "end")
                self.date_entry.delete(0, "end")
                self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
            else:
                self.message_label.configure(
                    text="❌ Erreur lors de l'enregistrement des données.",
                    text_color=self.message_err
                )
        except ValueError as ve:
            self.message_label.configure(
                text=f"❌ {str(ve)}",
                text_color=self.message_err
            )
        except Exception as e:
            self.message_label.configure(
                text=f"❌ Une erreur est survenue : {str(e)}",
                text_color=self.message_err
            )