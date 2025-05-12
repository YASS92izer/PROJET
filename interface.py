import customtkinter as ctk
from gestionnaire import GestionnaireBilanSanguin
from info import ArbreVisualisateur
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from saisie_donnees import SaisieDonnees
from mail import EmailEnvoi
from rapport_pdf import RapportPDF
from tkinter import messagebox, filedialog
from datetime import datetime
from PIL import Image, ImageTk


class ScrollableFrame(ctk.CTkScrollableFrame):
    def __init__(self, container, **kwargs):
        super().__init__(container, **kwargs)
        self.grid_columnconfigure(0, weight=1)

class App(ctk.CTkFrame):
    def __init__(self, parent, patient_data=None):
        super().__init__(parent)
        
        
        self.COLORS = {
            'primary': "#042C54",     
            'secondary': "#E3F2FD",   
            'accent': "#2CBEC3",      
            'hover': "#3E5A6A",      
            'background': "#FFFFFF",  
            'text': "#2B2B2B",       
        }

        self.gestionnaire = GestionnaireBilanSanguin()
        self.patient_connecte = patient_data
        
        if patient_data:
            self.patient_id = patient_data['PatientID']
        else:
            self.patient_id = None
            
        self.arbre_visualisateur = ArbreVisualisateur()

        
        self.menu_window = None

        # Création des catégories
        self.categories = {
            'hematologie': 'Hématologie',
            'biochimie': 'Biochimie',
            'lipides': 'Lipides',
            'enzymes': 'Enzymes',
            'ionogramme': 'Ionogramme',
            'autres': 'Autres'
        }

        # Frame principal conteneur
        self.main_container = ctk.CTkFrame(self, fg_color=self.COLORS['background'])
        self.main_container.pack(fill="both", expand=True)

        # En-tête avec informations utilisateur
        self.create_header()

        # Menu principal
        self.create_menu()

        # Frame principal pour le contenu
        self.main_frame = ScrollableFrame(
            self.main_container,
            fg_color=self.COLORS['background'],
            corner_radius=0
        )
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Label initial
        self.label_instructions = ctk.CTkLabel(
            self.main_frame,
            text="Sélectionnez une option dans le menu",
            font=("Arial", 14)
        )
        self.label_instructions.pack(pady=20)

    def create_header(self):
        # Frame d'en-tête
        header_frame = ctk.CTkFrame(
            self.main_container,
            fg_color=self.COLORS['primary'],
            height=60,
            corner_radius=0
        )
        header_frame.pack(fill="x", pady=0)
        header_frame.pack_propagate(False)

        
        ctk.CTkLabel(
            header_frame,
            text="MediLabPro",
            font=("Helvetica", 24, "bold"),
            text_color="white"
        ).pack(side="left", padx=20)

        
        user_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        user_frame.pack(side="right", padx=20)

        if self.patient_connecte:
            username = self.patient_connecte.get('Username', 'Utilisateur')
            ctk.CTkLabel(
                user_frame,
                text=f"👤 {username}",
                font=("Helvetica", 14),
                text_color="white"
            ).pack(side="right", padx=10)

    def create_menu(self):
        # Frame du menu
        menu_frame = ctk.CTkFrame(
            self.main_container,
            fg_color="white",
            height=75
        )
        menu_frame.pack(fill="x", pady=0)
        menu_frame.pack_propagate(False)

        # Container pour centrer les boutons
        button_container = ctk.CTkFrame(menu_frame, fg_color="transparent")
        button_container.pack(expand=True, pady=15)

        
        self.resultats_btn = self.create_menu_button(button_container, {
            'text': "📊 Derniers Résultats",
            'command': self.afficher_tous_etats,
            'icon': "📊"
        })

        self.arbre_btn = self.create_menu_button(button_container, {
            'text': "🔍 Liens Maladies",
            'command': self.afficher_arbre_maladies,
            'icon': "🔍"
        })

        self.compare_btn = self.create_menu_button(button_container, {
            'text': "📈 Comparer Analyses",
            'command': lambda: self.show_graph_menu(None),
            'icon': "📈"
        })

        self.saisie_btn = self.create_menu_button(button_container, {
            'text': "➕ Nouveau Bilan",
            'command': self.ouvrir_saisie_donnees,
            'icon': "➕"
        })

        self.email_btn = self.create_menu_button(button_container, {
            'text': "📧 Envoyer Email",
            'command': self.ouvrir_email_frame,
            'icon': "📧"
        })

        self.rapport_btn = self.create_menu_button(button_container, {
            'text': "📑 Générer PDF",
            'command': self.generer_rapport_pdf,
            'icon': "📑"
        })

    def create_menu_button(self, parent, config):
        button_frame = ctk.CTkFrame(parent, fg_color="transparent")
        button_frame.pack(side="left", padx=10)

        btn = ctk.CTkButton(
            button_frame,
            text=config['text'],
            command=config['command'],
            font=("Helvetica", 13),
            fg_color=self.COLORS['primary'],
            hover_color=self.COLORS['hover'],
            corner_radius=10,
            height=40,
            width=160,
            border_width=2,
            border_color=self.COLORS['accent']
        )
        btn.pack()

        
        def on_enter(e):
            btn.configure(fg_color=self.COLORS['hover'])

        def on_leave(e):
            btn.configure(fg_color=self.COLORS['primary'])

        btn.bind('<Enter>', on_enter)
        btn.bind('<Leave>', on_leave)
        
        return btn  
        
    def show_graph_menu(self, e):
        # Fermer le menu précédent s'il existe
        if self.menu_window is not None:
            self.menu_window.destroy()
            self.menu_window = None
            return

        # Créer une nouvelle fenêtre pour le menu
        self.menu_window = ctk.CTkToplevel(self)
        self.menu_window.overrideredirect(True)
        self.menu_window.attributes('-topmost', True)
        
        
        self.menu_window.configure(fg_color=self.COLORS['primary'])
        
        
        menu_frame = ctk.CTkFrame(
            self.menu_window,
            fg_color=self.COLORS['primary'],
            corner_radius=15,
        )
        menu_frame.pack(expand=True, fill="both", padx=2, pady=2)

        # Titre du menu déroulant
        ctk.CTkLabel(
            menu_frame,
            text="Choisir une catégorie",
            font=("Helvetica", 14, "bold"),
            text_color="white"
        ).pack(pady=(10, 5))

        
        for cat_key, cat_name in self.categories.items():
            btn = ctk.CTkButton(
                menu_frame,
                text=cat_name,
                font=("Helvetica", 13),
                fg_color="transparent",
                hover_color=self.COLORS['hover'],
                corner_radius=8,
                height=35,
                width=140,
                border_width=1,
                border_color=self.COLORS['accent'],
                command=lambda c=cat_key: self.menu_button_click(c)
            )
            btn.pack(padx=10, pady=4)

        # Positionnement du menu
        button_pos = self.compare_btn.winfo_rootx(), self.compare_btn.winfo_rooty()
        menu_x = button_pos[0]
        menu_y = button_pos[1] + self.compare_btn.winfo_height() + 5
        self.menu_window.geometry(f"+{menu_x}+{menu_y}")

        # Gestion de la fermeture
        self.menu_window.bind('<FocusOut>', lambda e: self.close_menu())
        self.menu_window.focus_set()

    def close_menu(self):
        if self.menu_window:
            self.menu_window.destroy()
            self.menu_window = None

    def menu_button_click(self, category):
        if self.menu_window:
            self.menu_window.destroy()
            self.menu_window = None
        self.afficher_graphique(category)

    def on_closing(self):
        if self.menu_window:
            self.menu_window.destroy()
        self.destroy()

    def get_status_color(self, statut):
        colors = {
            "Trop basse": self.COLORS['accent'],
            "Trop élevée": "#FB9488",   
            "Proche de la limite": "#FF9F43",  
            "Bonne": "#00B386"               
        }
        return colors.get(statut, "white")

    def afficher_message(self, message, is_error=False):
        # Nettoyer l'affichage actuel
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        message_frame = ctk.CTkFrame(
            self.main_frame,
            fg_color=self.COLORS['background']
        )
        message_frame.pack(expand=True)

        icon = "❌" if is_error else "ℹ️"
        color = "#FB9488" if is_error else self.COLORS['primary']

        ctk.CTkLabel(
            message_frame,
            text=f"{icon} {message}",
            font=("Helvetica", 14),
            text_color=color
        ).pack(pady=20)
        
    def afficher_tous_etats(self):
        # Nettoyer l'affichage actuel
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        # Récupérer le dernier bilan
        bilans = self.gestionnaire.obtenir_bilan_p(self.patient_id)
        if bilans.empty:
            self.afficher_message("Aucun bilan disponible", True)
            return

        dernier_bilan = bilans.iloc[-1]
        descriptions = self.get_descriptions()

        
        header_frame = ctk.CTkFrame(
            self.main_frame,
            fg_color=self.COLORS['primary'],
            corner_radius=15
        )
        header_frame.pack(fill="x", pady=(0, 20))

        ctk.CTkLabel(
            header_frame,
            text=f"Résultats du bilan sanguin du {dernier_bilan['Date']}",
            font=("Helvetica", 16, "bold"),
            text_color="white"
        ).pack(pady=15)

        
        grid_container = ctk.CTkFrame(
            self.main_frame,
            fg_color=self.COLORS['background']
        )
        grid_container.pack(fill="both", expand=True, padx=5, pady=5)

        
        for i in range(3):
            grid_container.grid_columnconfigure(i, weight=1)

        # Paramètres pour chaque catégorie
        parametres = {
            'hematologie': ['Globules Rouges', 'Hémoglobine', 'Globules Blancs', 'Plaquettes'],
            'biochimie': ['Glycémie à jeun', 'Créatinine', 'Urée', 'Fer', 'Ferritine'],
            'lipides': ['Cholestérol Total', 'HDL', 'LDL', 'Triglycérides'],
            'enzymes': ['ASAT', 'ALAT', 'Gamma GT'],
            'ionogramme': ['Sodium', 'Potassium', 'Chlore'],
            'autres': ['Bilirubine', 'CRP', 'TSH']
        }

        # Créer les tableaux dans une grille 2x3
        for idx, (cat_key, cat_name) in enumerate(self.categories.items()):
            # Calculer la position dans la grille (2 lignes, 3 colonnes)
            row = idx // 3  # 0 pour les 3 premiers, 1 pour les 3 derniers
            col = idx % 3   # 0, 1, 2 pour chaque ligne

            
            cat_frame = ctk.CTkFrame(
                grid_container,
                fg_color="white",
                corner_radius=15,
                border_width=2,
                border_color=self.COLORS['accent']
            )
            cat_frame.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")

            
            cat_header = ctk.CTkFrame(
                cat_frame,
                fg_color=self.COLORS['primary'],
                corner_radius=12
            )
            cat_header.pack(fill="x", padx=2, pady=2)

            ctk.CTkLabel(
                cat_header,
                text=cat_name,
                font=("Helvetica", 14, "bold"),
                text_color="white"
            ).pack(pady=8)

            
            table_frame = ctk.CTkFrame(cat_frame, fg_color="white")
            table_frame.pack(fill="both", expand=True, padx=10, pady=10)

            
            headers = ["Paramètre", "Valeur", "Réf.", "Statut", "Info"]
            for col_idx, header in enumerate(headers):
                ctk.CTkLabel(
                    table_frame,
                    text=header,
                    font=("Helvetica", 12, "bold"),
                    text_color=self.COLORS['primary']
                ).grid(row=0, column=col_idx, padx=5, pady=5, sticky="w")

            
            for row_idx, param in enumerate(parametres[cat_key], 1):
                
                ctk.CTkLabel(
                    table_frame,
                    text=param,
                    font=("Helvetica", 12),
                    text_color=self.COLORS['text']
                ).grid(row=row_idx, column=0, padx=5, pady=3, sticky="w")

                # Valeur
                valeur = dernier_bilan[param]
                ctk.CTkLabel(
                    table_frame,
                    text=f"{valeur:.1f}",
                    font=("Helvetica", 12)
                ).grid(row=row_idx, column=1, padx=5, pady=3)

                # Évaluation
                resultat = self.gestionnaire.evaluer_valeur(valeur, dernier_bilan['Sexe'], param)
                
                # Références
                ref_text = f"{resultat['min']}-{resultat['max']}"
                ctk.CTkLabel(
                    table_frame,
                    text=ref_text,
                    font=("Helvetica", 12)
                ).grid(row=row_idx, column=2, padx=5, pady=3)

                # Statut
                status_label = ctk.CTkLabel(
                    table_frame,
                    text=resultat['statut'],
                    text_color=self.get_status_color(resultat['statut']),
                    font=("Helvetica", 12, "bold")
                )
                status_label.grid(row=row_idx, column=3, padx=5, pady=3)

                # Bouton Info
                info_button = ctk.CTkButton(
                    table_frame,
                    text="ℹ",
                    width=30,
                    height=25,
                    fg_color=self.COLORS['primary'],
                    hover_color=self.COLORS['hover'],
                    corner_radius=8,
                    command=lambda p=param, d=descriptions.get(param, ""): 
                        self.afficher_description_popup(p, d)
                )
                info_button.grid(row=row_idx, column=4, padx=5, pady=3)

            
            for i in range(5):
                table_frame.grid_columnconfigure(i, weight=1)

    def afficher_description_popup(self, param, description):
        # Créer une nouvelle fenêtre popup
        popup = ctk.CTkToplevel(self)
        popup.title(f"Information sur {param}")
        popup.geometry("400x200")
        
        
        popup.transient(self)
        popup.grab_set()
        
        
        popup.configure(fg_color="#ffffff")  
        
        
        label = ctk.CTkLabel(
            popup,
            text=description,
            wraplength=350,
            font=("Arial", 12),
            justify="left",
            text_color="#042C54"
        )
        label.pack(padx=20, pady=20, expand=True, fill="both")
        
        
        btn = ctk.CTkButton(
            popup,
            text="Fermer",
            command=popup.destroy,
            fg_color="#042C54",
            hover_color="#3E5A6A",
            border_color="#2CBEC3",
            border_width=1,
            corner_radius=8
        )
        btn.pack(pady=10)

    

    def ouvrir_saisie_donnees(self):
        saisie = SaisieDonnees(self.main_frame, self.gestionnaire, self.patient_connecte)
        saisie.ouvrir_saisie()

    def ouvrir_email_frame(self):
        email_frame = EmailEnvoi(self.main_frame, self.gestionnaire, self.patient_connecte)
        email_frame.ouvrir_email()

    def generer_rapport_pdf(self):
        try:
            bilans = self.gestionnaire.obtenir_bilan_p(self.patient_id)
            if bilans.empty:
                self.afficher_message("Aucun bilan disponible", True)
                return

            filename = filedialog.asksaveasfilename(
                defaultextension=".pdf",
                initialfile=f"rapport_medical_{self.patient_connecte['Username']}_{datetime.now().strftime('%Y%m%d')}.pdf",
                title="Enregistrer le rapport PDF",
                filetypes=[("PDF files", "*.pdf")]
            )
            
            if filename:
                
                progress_frame = ctk.CTkFrame(
                    self.main_frame,
                    fg_color=self.COLORS['background']
                )
                progress_frame.pack(expand=True)

                progress = ctk.CTkProgressBar(
                    progress_frame,
                    mode='indeterminate',
                    progress_color=self.COLORS['accent']
                )
                progress.pack(pady=20)
                progress.start()
                
                status_label = ctk.CTkLabel(
                    progress_frame,
                    text="📊 Génération du rapport en cours...",
                    font=("Helvetica", 14),
                    text_color=self.COLORS['primary']
                )
                status_label.pack(pady=10)
                
                self.update()

                generateur_pdf = RapportPDF(self.gestionnaire)
                dernier_bilan = bilans.iloc[-1].to_dict()
                generateur_pdf.generer_rapport(self.patient_connecte, dernier_bilan, filename)

                progress.stop()
                progress_frame.destroy()

                if messagebox.askyesno(
                    "Rapport généré",
                    "Le rapport a été généré avec succès. Voulez-vous l'ouvrir maintenant ?"
                ):
                    import os
                    os.startfile(filename)

        except Exception as e:
            self.afficher_message(f"Erreur lors de la génération du rapport : {str(e)}", True)
            
    
        
    def get_descriptions(self):
        return {
            'Globules Rouges': "Transportent l'oxygène dans le sang. Un taux trop bas (anémie) peut causer fatigue, essoufflement et pâleur. Un taux trop élevé peut indiquer une maladie du sang ou augmenter le risque de caillots sanguins.",
            'Hémoglobine': "Protéine dans les globules rouges qui transporte l'oxygène. Un taux bas indique une anémie (fatigue, essoufflement, vertiges). Un taux élevé peut être lié à un manque d'oxygène (altitude, tabac) ou à une maladie du sang.",
            'Globules Blancs': "Cellules de défense du corps. Un taux élevé peut signaler une infection, une inflammation ou une leucémie. Un taux trop bas peut indiquer une faiblesse du système immunitaire ou un problème de moelle osseuse.",
            'Plaquettes': "Aident à la coagulation du sang. Un taux bas peut provoquer des saignements. Un taux élevé augmente le risque de formation de caillots pouvant entraîner des AVC ou des thromboses.",
            'Glycémie à jeun': "Mesure le sucre dans le sang après plusieurs heures sans manger. Un taux élevé peut signaler un diabète ou un prédiabète. Un taux trop bas (hypoglycémie) peut causer vertiges, sueurs et perte de connaissance.",
            'Cholestérol Total': "Graisse dans le sang. Un taux élevé augmente le risque de maladies cardiovasculaires. Un taux trop bas est rare mais peut être lié à certaines maladies ou carences.",
            'HDL': "Bon cholestérol. Protège le cœur en éliminant le mauvais cholestérol. Un taux bas augmente le risque cardiovasculaire. Un taux élevé est bénéfique.",
            'LDL': "Mauvais cholestérol. Un taux trop élevé favorise les dépôts dans les artères (plaques) et augmente les risques d'infarctus ou AVC. Un taux bas est préférable.",
            'Triglycérides': "Type de graisses. Un taux élevé peut indiquer un risque cardiovasculaire accru, souvent lié à une mauvaise alimentation. Un taux très bas peut être observé en cas de malnutrition.",
            'ASAT': "Enzyme présente dans le foie, le cœur et les muscles. Un taux élevé peut signaler des atteintes hépatiques, musculaires ou cardiaques. Un taux normal est rassurant.",
            'ALAT': "Enzyme surtout produite par le foie. Un taux élevé est un signe spécifique de souffrance hépatique (hépatite, médicaments, alcool).",
            'Gamma GT': "Enzyme du foie. Un taux élevé peut être dû à l'alcool, à certains médicaments ou à un problème des voies biliaires.",
            'Bilirubine': "Pigment issu de la dégradation des globules rouges. Un taux élevé peut causer un jaunissement de la peau (jaunisse) et signaler un problème hépatique ou une destruction excessive des globules rouges.",
            'Créatinine': "Déchet filtré par les reins. Un taux élevé indique un mauvais fonctionnement rénal. Un taux trop bas est rare et généralement sans gravité.",
            'Urée': "Résidu du métabolisme des protéines, éliminé par les reins. Un taux élevé peut indiquer une insuffisance rénale ou une déshydratation. Un taux bas peut refléter une alimentation pauvre en protéines.",
            'Sodium': "Électrolyte essentiel à l'hydratation et à la transmission nerveuse. Un taux trop bas (hyponatrémie) peut provoquer fatigue, nausées, confusion. Un taux trop élevé (hypernatrémie) peut indiquer une déshydratation.",
            'Potassium': "Électrolyte vital pour le cœur et les muscles. Un taux trop bas (hypokaliémie) peut causer fatigue, crampes, troubles du rythme cardiaque. Un taux trop élevé (hyperkaliémie) peut provoquer une faiblesse musculaire.",
            'Chlore': "Électrolyte qui aide à équilibrer les liquides et l'acidité du corps. Un taux trop bas ou trop élevé peut entraîner des déséquilibres acido-basiques, avec fatigue, confusion ou troubles respiratoires.",
            'CRP': "Protéine produite lors d'une inflammation. Un taux élevé signale une infection, une inflammation chronique ou une maladie auto-immune. Un taux bas est normal.",
            'TSH': "Hormone qui contrôle la thyroïde. Un taux élevé indique souvent une hypothyroïdie (ralentissement du métabolisme). Un taux bas peut signaler une hyperthyroïdie (accélération du métabolisme).",
            'Fer': "Minéral indispensable pour fabriquer l'hémoglobine. Un taux faible peut entraîner une anémie. Un taux trop élevé peut signaler une surcharge en fer (hémochromatose).",
            'Ferritine': "Protéine qui stocke le fer. Un taux bas reflète des réserves faibles (carence). Un taux élevé peut indiquer une inflammation, une surcharge en fer ou une maladie chronique."
        }

    

    def afficher_arbre_maladies(self):
        # Nettoyer l'affichage actuel
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        
        # Afficher l'arbre dans le main_frame
        self.arbre_visualisateur.afficher_arbres(self.main_frame)
        
    def afficher_graphique(self, categorie):
        # Nettoyer l'affichage actuel
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        
        title_frame = ctk.CTkFrame(
            self.main_frame,
            fg_color=self.COLORS['primary'],
            corner_radius=15
        )
        title_frame.pack(fill="x", pady=(0, 20))

        ctk.CTkLabel(
            title_frame,
            text=f"Évolution des paramètres - {self.categories[categorie]}",
            font=("Helvetica", 16, "bold"),
            text_color="white"
        ).pack(pady=15)

        # Frame conteneur pour le graphique
        graph_container = ctk.CTkFrame(
            self.main_frame,
            fg_color="white",
            corner_radius=15,
            border_width=2,
            border_color=self.COLORS['accent']
        )
        graph_container.pack(fill="both", expand=True, padx=5, pady=5)

        fig = self.gestionnaire.creer_graphique_comparaison(self.patient_id, categorie)
        
        if fig:
            
            fig.set_size_inches(16, 10)  
            
            
            fig.tight_layout(pad=3.0)
            
            
            canvas = FigureCanvasTkAgg(fig, master=graph_container)
            canvas.draw()
            
            # Configurer le widget canvas pour qu'il prenne tout l'espace disponible
            canvas_widget = canvas.get_tk_widget()
            canvas_widget.pack(fill="both", expand=True, padx=20, pady=20)
            
            # Mettre à jour l'affichage
            self.update_idletasks()
        else:
            self.afficher_message(
                "Il faut au minimum 2 analyses pour effectuer une comparaison",
                True
            )

    def toggle_user_menu(self):
        """Affiche ou cache le menu utilisateur"""
        if self.user_menu is not None:
            self.user_menu.destroy()
            self.user_menu = None
            return
        
        # Créer le menu déroulant
        self.user_menu = ctk.CTkToplevel(self)
        self.user_menu.overrideredirect(True)
        self.user_menu.attributes('-topmost', True)
        
        # Configuration du style
        self.user_menu.configure(fg_color=self.COLORS['primary'])
        
        # Frame principale du menu avec coins arrondis
        menu_frame = ctk.CTkFrame(
            self.user_menu,
            fg_color=self.COLORS['primary'],
            corner_radius=15,
        )
        menu_frame.pack(expand=True, fill="both", padx=2, pady=2)
        
        # Options du menu
        profile_btn = ctk.CTkButton(
            menu_frame,
            text="👤 Profil",
            font=("Helvetica", 13),
            fg_color="transparent",
            hover_color=self.COLORS['hover'],
            corner_radius=8,
            height=35,
            width=130,
            border_width=1,
            border_color=self.COLORS['accent'],
            command=self.show_profile
        )
        profile_btn.pack(padx=10, pady=4)
        
        logout_btn = ctk.CTkButton(
            menu_frame,
            text="🚪 Déconnexion",
            font=("Helvetica", 13),
            fg_color="transparent",
            hover_color=self.COLORS['hover'],
            corner_radius=8,
            height=35,
            width=130,
            border_width=1,
            border_color=self.COLORS['accent'],
            command=self.logout
        )
        logout_btn.pack(padx=10, pady=4)
        
        # Positionnement du menu
        button_pos = self.user_button.winfo_rootx(), self.user_button.winfo_rooty()
        menu_x = button_pos[0]
        menu_y = button_pos[1] + self.user_button.winfo_height() + 5
        self.user_menu.geometry(f"+{menu_x}+{menu_y}")
        
        # Gestion de la fermeture
        self.user_menu.bind('<FocusOut>', lambda e: self.close_user_menu())
        self.user_menu.focus_set()

    def close_user_menu(self):
        """Ferme le menu utilisateur"""
        if self.user_menu:
            self.user_menu.destroy()
            self.user_menu = None

    def show_profile(self):
        """Affiche et permet de modifier le profil utilisateur"""
        self.close_user_menu()
        
        # Nettoyer l'affichage actuel
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        
        
        title_frame = ctk.CTkFrame(
            self.main_frame,
            fg_color=self.COLORS['primary'],
            corner_radius=15
        )
        title_frame.pack(fill="x", pady=(0, 20))
        
        ctk.CTkLabel(
            title_frame,
            text="Mon Profil",
            font=("Helvetica", 16, "bold"),
            text_color="white"
        ).pack(pady=15)
        
        # Frame pour le formulaire de profil
        profile_frame = ctk.CTkFrame(
            self.main_frame,
            fg_color="white",
            corner_radius=15,
            border_width=2,
            border_color=self.COLORS['accent']
        )
        profile_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        
        content_frame = ctk.CTkFrame(profile_frame, fg_color="transparent")
        content_frame.pack(expand=True, pady=30)
        
        
        ctk.CTkLabel(
            content_frame,
            text="Nom d'utilisateur:",
            font=("Helvetica", 14, "bold"),
            text_color=self.COLORS['primary']
        ).grid(row=0, column=0, padx=20, pady=10, sticky="e")
        
        ctk.CTkLabel(
            content_frame,
            text=self.patient_connecte.get('Username', ''),
            font=("Helvetica", 14),
            text_color=self.COLORS['text']
        ).grid(row=0, column=1, padx=20, pady=10, sticky="w")
        
        
        ctk.CTkLabel(
            content_frame,
            text="ID Patient:",
            font=("Helvetica", 14, "bold"),
            text_color=self.COLORS['primary']
        ).grid(row=1, column=0, padx=20, pady=10, sticky="e")
        
        ctk.CTkLabel(
            content_frame,
            text=str(self.patient_connecte.get('PatientID', '')),
            font=("Helvetica", 14),
            text_color=self.COLORS['text']
        ).grid(row=1, column=1, padx=20, pady=10, sticky="w")
        
        
        ctk.CTkLabel(
            content_frame,
            text="Âge:",
            font=("Helvetica", 14, "bold"),
            text_color=self.COLORS['primary']
        ).grid(row=2, column=0, padx=20, pady=10, sticky="e")
        
        self.age_entry = ctk.CTkEntry(
            content_frame,
            font=("Helvetica", 14),
            width=100,
            height=35,
            border_color=self.COLORS['primary'],
            corner_radius=8
        )
        self.age_entry.insert(0, str(self.patient_connecte.get('Age', '')))
        self.age_entry.grid(row=2, column=1, padx=20, pady=10, sticky="w")
        
        
        ctk.CTkLabel(
            content_frame,
            text="Sexe:",
            font=("Helvetica", 14, "bold"),
            text_color=self.COLORS['primary']
        ).grid(row=3, column=0, padx=20, pady=10, sticky="e")
        
        self.sexe_menu = ctk.CTkOptionMenu(
            content_frame,
            values=["Homme", "Femme"],
            font=("Helvetica", 14),
            width=150,
            height=35,
            fg_color=self.COLORS['primary'],
            button_hover_color=self.COLORS['hover'],
            corner_radius=8
        )
        self.sexe_menu.set(self.patient_connecte.get('Sexe', 'Homme'))
        self.sexe_menu.grid(row=3, column=1, padx=20, pady=10, sticky="w")
        
        
        self.profile_info = ctk.CTkLabel(
            content_frame,
            text="",
            font=("Helvetica", 12),
            text_color="#e74c3c"
        )
        self.profile_info.grid(row=4, column=0, columnspan=2, pady=10)
        
        
        save_btn = ctk.CTkButton(
            content_frame,
            text="Enregistrer les modifications",
            font=("Helvetica", 14, "bold"),
            fg_color=self.COLORS['primary'],
            hover_color=self.COLORS['hover'],
            corner_radius=10,
            height=40,
            width=250,
            command=self.save_profile
        )
        save_btn.grid(row=5, column=0, columnspan=2, pady=20)

    def save_profile(self):
        """Sauvegarde les modifications du profil"""
        try:
            # Valider l'âge
            age_text = self.age_entry.get().strip()
            if not age_text.isdigit() or int(age_text) <= 0:
                self.profile_info.configure(text="⚠️ L'âge doit être un nombre entier positif.")
                return
            
            # Mise à jour des données en mémoire
            self.patient_connecte['Age'] = int(age_text)
            self.patient_connecte['Sexe'] = self.sexe_menu.get()
            
            # Mise à jour du fichier CSV
            import csv
            import os
            
            temp_file = "temp_comptes.csv"
            found = False
            
            with open("comptes.csv", 'r', newline='', encoding='latin-1') as infile, \
                 open(temp_file, 'w', newline='', encoding='latin-1') as outfile:
                
                reader = csv.DictReader(infile)
                fieldnames = reader.fieldnames
                
                writer = csv.DictWriter(outfile, fieldnames=fieldnames)
                writer.writeheader()
                
                for row in reader:
                    if int(row['PatientID']) == self.patient_connecte['PatientID']:
                        row['Age'] = str(self.patient_connecte['Age'])
                        row['Sexe'] = self.patient_connecte['Sexe']
                        found = True
                    writer.writerow(row)
            
            # Remplacer l'ancien fichier par le nouveau
            os.replace(temp_file, "comptes.csv")
            
            if found:
                self.profile_info.configure(text="✅ Profil mis à jour avec succès!", text_color="#2ecc71")
            else:
                self.profile_info.configure(text="⚠️ Utilisateur non trouvé dans la base de données.")
                
        except Exception as e:
            self.profile_info.configure(text=f"⚠️ Erreur: {str(e)}")

    def logout(self):
        """Déconnecte l'utilisateur et retourne à l'écran de connexion"""
        self.close_user_menu()
        
        # On retourne à l'écran de connexion
        # On accède au parent de niveau supérieur (MainApplication)
        parent_app = self.winfo_toplevel()
        parent_app.show_login()

    def on_closing(self):
        if self.menu_window:
            self.menu_window.destroy()
        if hasattr(self, 'user_menu') and self.user_menu:
            self.user_menu.destroy()
        self.destroy()
        
    def create_header(self):
        
        header_frame = ctk.CTkFrame(
            self.main_container,
            fg_color=self.COLORS['primary'],
            height=60,
            corner_radius=0
        )
        header_frame.pack(fill="x", pady=0)
        header_frame.pack_propagate(False)

        
        logo_title_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        logo_title_frame.pack(side="left", padx=20)
        
        try:
            # Chargement du logo pour l'en-tête 
            logo_path = "logo1.png"  
            header_logo = ctk.CTkImage(
                light_image=Image.open(logo_path),
                dark_image=Image.open(logo_path),
                size=(40, 40)  
            )
            
            # Création d'un label pour le logo
            logo_label = ctk.CTkLabel(
                logo_title_frame,
                image=header_logo,
                text=""
            )
            logo_label.pack(side="left", padx=(0, 10))
        
        except Exception as e:
            print(f"Erreur lors du chargement du logo d'en-tête: {e}")
        
        # Nom de l'application à côté du logo
        ctk.CTkLabel(
            logo_title_frame,
            text="MediLabPro",
            font=("Helvetica", 24, "bold"),
            text_color="white"
        ).pack(side="left")

        # Informations utilisateur
        user_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        user_frame.pack(side="right", padx=20)

        if self.patient_connecte:
            username = self.patient_connecte.get('Username', 'Utilisateur')
            
            
            self.user_button = ctk.CTkButton(
                user_frame,
                text=f"👤 {username}",
                font=("Helvetica", 14),
                text_color="white",
                fg_color="transparent",
                hover_color=self.COLORS['hover'],
                corner_radius=8,
                command=self.toggle_user_menu
            )
            self.user_button.pack(side="right")
            
            # Variable pour tracker le sous-menu utilisateur
            self.user_menu = None
