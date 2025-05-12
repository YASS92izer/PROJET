import customtkinter as ctk
from email_module import send_email  
from tkinter import messagebox

class EmailEnvoi:
    def __init__(self, main_frame, gestionnaire, patient_data):
        # Initialise l’interface et les données du patient
        self.main_frame = main_frame
        self.gestionnaire = gestionnaire
        self.patient_connecte = patient_data
        self.patient_id = patient_data.get('PatientID', 0)

        # Définition des couleurs utilisées dans l’interface
        self.fond = "#FFFFFF"
        self.accent = "#042C54"
        self.texte = "#042C54"
        self.btn_text_color = "white"
        self.message_err = "#FB9488"
        self.message_succes = "#00B386"

    def ouvrir_email(self):
        # Nettoie le cadre principal en retirant les widgets existants
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        fond = self.fond
        accent = self.accent
        texte = self.texte

        titre = ctk.CTkLabel(
            self.main_frame,
            text="Envoyer bilan sanguin par email",
            font=("Arial", 24, "bold"),
            text_color=texte,
            fg_color=fond
        )
        titre.pack(fill="x", pady=20)

        # Label pour afficher les messages d’erreur ou de succès
        self.message_label = ctk.CTkLabel(
            self.main_frame,
            text="",
            font=("Arial", 14),
            text_color=self.message_err,
            fg_color=fond
        )
        self.message_label.pack(fill="x", padx=20, pady=(0, 15))

        # Label pour demander l’adresse email
        label_email = ctk.CTkLabel(
            self.main_frame,
            text="Adresse email destinataire :",
            font=("Arial", 16),
            text_color=texte,
            fg_color=fond
        )
        label_email.pack(pady=(10, 7))

        # Champ de saisie de l’adresse email
        self.email_entry = ctk.CTkEntry(
            self.main_frame,
            width=350,
            fg_color="white",
            text_color=accent,
            border_color=accent,
            border_width=1,
            corner_radius=6,
            placeholder_text="exemple@mail.com"
        )
        self.email_entry.pack(pady=(0, 20))

        # Bouton pour envoyer l’email
        btn_envoyer = ctk.CTkButton(
            self.main_frame,
            text="Envoyer le bilan",
            fg_color=accent,
            hover_color="#034B70",
            text_color=self.btn_text_color,
            corner_radius=15,
            font=("Arial", 16, "bold"),
            command=self.envoyer_bilan_email,
            width=250,
            height=45
        )
        btn_envoyer.pack()

    def envoyer_bilan_email(self):
        # Récupère l’adresse saisie
        adresse = self.email_entry.get().strip()
        if not adresse:
            # Si vide, affiche un message d’erreur
            self.message_label.configure(text="Veuillez saisir une adresse email valide.", text_color=self.message_err)
            return

        # Récupère les bilans du patient
        bilans = self.gestionnaire.obtenir_bilan_p(self.patient_id)
        if bilans.empty:
            # Si aucun bilan, affiche un message d’erreur
            self.message_label.configure(text="Aucun bilan disponible pour envoi.", text_color=self.message_err)
            return

        # Prend le dernier bilan disponible
        dernier_bilan = bilans.iloc[-1].to_dict()
        resultats = {}
        for nom_test, valeur in dernier_bilan.items():
            if nom_test not in ['PatientID', 'Date', 'Sexe', 'Age']:
                # Définie les valeurs et statuts
                resultats[nom_test] = self.gestionnaire.evaluer_valeur(
                    valeur,
                    dernier_bilan.get('Sexe', 'Homme'),
                    nom_test
                )

        # Génère le contenu HTML de l’email
        content = self.creer_contenu_html(resultats)

        try:
            # Tente d’envoyer l’email
            send_email(adresse, "Bilan sanguin et évaluation", content)
            # Affiche un message de succès
            self.message_label.configure(text=f"Bilan envoyé à {adresse} !", text_color=self.message_succes)
            self.email_entry.delete(0, 'end')  # Vide le champ email
        except Exception as e:
            # En cas d’erreur, affiche le message d’erreur
            self.message_label.configure(text=f"Erreur d'envoi : {e}", text_color=self.message_err)

    def creer_contenu_html(self, resultats):
        # Crée le contenu HTML à envoyer par email
        content = """
        <!DOCTYPE html><html lang="fr"><head><meta charset="UTF-8"><style>
        body { font-family: Arial; background:#f4f4f4; padding:20px;}
        .container { background:#fff; padding:20px; border-radius:8px;}
        table { width:100%; border-collapse:collapse;}
        th, td { padding:10px; border-bottom:1px solid #ddd;}
        th { background:#f2f2f2;}
        .statut { font-weight: bold; }
        .bonne { color: #00B386; }
        .trop-eleve { color: #FB9488; }
        .proche-limite { color: #FF9F43; }
        .trop-basse { color: #2CBEC3; }
        </style></head><body><div class="container">
        <h1>Bilan sanguin</h1><table><tr><th>Test</th><th>Valeur</th><th>Référence</th><th>Statut</th></tr>
        """

        # Ajoute une ligne HTML par test avec valeur, référence et statut
        for test, resultat in resultats.items():
            valeur = resultat.get('valeur', '-')
            min_val = resultat.get('min', '-')
            max_val = resultat.get('max', '-')
            statut = resultat.get('statut', '-')
            statut_class = ''
            # Associe une classe CSS selon le statut
            if statut == 'Bonne': statut_class = 'bonne'
            elif statut == 'Trop élevée': statut_class = 'trop-eleve'
            elif statut == 'Proche de la limite': statut_class = 'proche-limite'
            elif statut == 'Trop basse': statut_class = 'trop-basse'

            # Ajoute une ligne au tableau
            content += f"""
            <tr>
                <td>{test}</td>
                <td>{valeur}</td>
                <td>{min_val} - {max_val}</td>
                <td class="statut {statut_class}">{statut}</td>
            </tr>"""

        # Termine le HTML
        content += "</table></div></body></html>"
        return content