import customtkinter as ctk
from tkinter import messagebox
import csv
import os
from PIL import Image, ImageTk


ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

COMPTES_FILE = "comptes.csv"

class MedicalApp(ctk.CTkFrame):
    def __init__(self, parent, callback):
        super().__init__(parent)
        
        
        self.COLORS = {
            'primary': "#042C54",     
            'secondary': "#FFFFFF",   
            'background': "#FFFFFF", 
            'text': "#FFFFFF",       
            'error': "#FF5252",      
            'success': "#4CAF50"     
        }
        
        self.callback = callback
        self.configure(fg_color=self.COLORS['background'])
        self.patient_connecte = None
        self.mode = "Connexion"
        
        # Création du layout principal
        self.create_layout()

    def create_layout(self):
        # Nettoyer les widgets existants
        for widget in self.winfo_children():
            widget.destroy()

        # Container principal avec deux colonnes
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        
        self.left_panel = ctk.CTkFrame(
            self,
            fg_color="white",
            corner_radius=0
        )
        self.left_panel.grid(row=0, column=0, sticky="nsew")
        self.left_panel.grid_rowconfigure(0, weight=1)
        self.left_panel.grid_columnconfigure(0, weight=1)

        # Titre de l'application
        ctk.CTkLabel(
            self.left_panel,
            text="MediLabPro",
            font=("Helvetica", 40, "bold"),
            text_color="#042C54"
        ).grid(row=0, column=0, pady=(50, 20))

        try:
            
            logo_path = "logo1.png" 
            
            self.logo_image = ctk.CTkImage(
                light_image=Image.open(logo_path),
                dark_image=Image.open(logo_path),
                size=(400, 400)  
            )
            
            
            logo_label = ctk.CTkLabel(
                self.left_panel,
                image=self.logo_image,
                text="",  
            )
            logo_label.grid(row=1, column=0, pady=(20, 20))

        except Exception as e:
            print(f"Erreur lors du chargement du logo: {e}")

        
        ctk.CTkLabel(
            self.left_panel,
            text="Votre plateforme d'analyse\nmédicale intelligente",
            font=("Helvetica", 20),
            text_color="#042C54"
        ).grid(row=2, column=0, pady=20)

        
        self.right_panel = ctk.CTkFrame(
            self,
            fg_color=self.COLORS['background'],
            corner_radius=0
        )
        self.right_panel.grid(row=0, column=1, sticky="nsew")

        
        ctk.CTkLabel(
            self.right_panel,
            text="Bienvenue !",
            font=("Helvetica", 32, "bold"),
            text_color=self.COLORS['text']
        ).pack(pady=(50, 20))

        # Toggle Connexion/Inscription
        self.toggle = ctk.CTkSegmentedButton(
            self.right_panel,
            values=["Connexion", "Inscription"],
            command=self.on_toggle,
            fg_color=self.COLORS['secondary'],
            selected_color=self.COLORS['primary'],
            text_color=self.COLORS['text'],
            font=("Helvetica", 14),
            width=300,
            height=40
        )
        self.toggle.set(self.mode)
        self.toggle.pack(pady=20)

        
        self.form = ctk.CTkFrame(
            self.right_panel,
            fg_color=self.COLORS['background']
        )
        self.form.pack(pady=20, padx=50)

        
        self.user_entry = self.create_entry("👤 Nom d'utilisateur")
        self.pwd_entry = self.create_entry("🔒 Mot de passe", show="●")
        self.age_entry = self.create_entry("📅 Âge")
        
        
        self.sexe_menu = ctk.CTkOptionMenu(
            self.form,
            values=["Homme", "Femme"],
            fg_color=self.COLORS['primary'],
            button_color=self.COLORS['primary'],
            button_hover_color="#1565C0",
            text_color="white",
            font=("Helvetica", 14),
            width=300,
            corner_radius=10
        )

        
        self.validate_btn = ctk.CTkButton(
            self.form,
            text="Valider",
            fg_color=self.COLORS['primary'],
            hover_color="#1565C0",
            text_color="white",
            font=("Helvetica", 16, "bold"),
            width=300,
            height=50,
            corner_radius=25,
            command=self.on_validate
        )
        self.validate_btn.pack(pady=20)

        
        self.info_label = ctk.CTkLabel(
            self.form,
            text="",
            font=("Helvetica", 12),
            text_color=self.COLORS['error']
        )
        self.info_label.pack(pady=10)

        self.update_form_fields()

    def create_entry(self, placeholder, show=None):
        entry = ctk.CTkEntry(
            self.form,
            placeholder_text=placeholder,
            width=300,
            height=45,
            font=("Helvetica", 14),
            fg_color="white",
            text_color=self.COLORS['primary'],
            border_color=self.COLORS['primary'],
            border_width=2,
            corner_radius=10,
            show=show
        )
        entry.pack(pady=10)
        return entry

    def update_form_fields(self):
        if self.mode == "Inscription":
            self.age_entry.pack(pady=10)
            self.sexe_menu.pack(pady=10)
            self.validate_btn.configure(text="S'inscrire")
        else:
            self.age_entry.pack_forget()
            self.sexe_menu.pack_forget()
            self.validate_btn.configure(text="Se connecter")

    def on_toggle(self, value):
        self.mode = value
        self.update_form_fields()
        self.info_label.configure(text="")

    def show_message(self, message, is_error=True):
        self.info_label.configure(
            text=message,
            text_color=self.COLORS['error'] if is_error else self.COLORS['success']
        )

    def on_validate(self):
        username = self.user_entry.get().strip()
        password = self.pwd_entry.get().strip()

        if not username or not password:
            self.show_message("⚠️ Veuillez remplir tous les champs obligatoires.")
            return

        if self.mode == "Inscription":
            age_text = self.age_entry.get().strip()
            if not age_text.isdigit() or int(age_text) <= 0:
                self.show_message("⚠️ L'âge doit être un nombre entier positif.")
                return
            patient_sexe = self.sexe_menu.get()
            patient_age = int(age_text)

            if self.user_exists(username):
                self.show_message("⚠️ Ce nom d'utilisateur existe déjà.")
                return

            patient_id = self.get_next_patient_id()
            self.save_account_to_csv(patient_id, username, password, patient_sexe, patient_age)

            self.patient_connecte = {
                "PatientID": patient_id,
                "Sexe": patient_sexe,
                "Age": patient_age,
                "Username": username
            }
            
            self.callback(self.patient_connecte)

        else:
            if not self.verify_account(username, password):
                self.show_message("⚠️ Nom d'utilisateur ou mot de passe incorrect.")
                return

            user_data = self.get_user_data(username)
            if user_data is None:
                self.show_message("⚠️ Erreur lecture données utilisateur.")
                return

            self.patient_connecte = {
                "PatientID": int(user_data.get("PatientID", 0)),
                "Sexe": user_data.get("Sexe"),
                "Age": int(user_data.get("Age", 0)),
                "Username": username
            }

            self.show_message("✅ Connexion réussie !", False)
            self.callback(self.patient_connecte)

    
    def save_account_to_csv(self, patient_id, username, password, sexe, age):
        
        headers = ["PatientID", "Username", "Password", "Sexe", "Age"]

        if not os.path.isfile(COMPTES_FILE):
            with open(COMPTES_FILE, 'w', newline='', encoding='latin-1') as f:
                writer = csv.writer(f)
                writer.writerow(headers)

        with open(COMPTES_FILE, 'a', newline='', encoding='latin-1') as f:
            writer = csv.writer(f)
            writer.writerow([patient_id, username, password, sexe, age])

    def verify_account(self, username, password):
        
        if not os.path.isfile(COMPTES_FILE):
            return False
        with open(COMPTES_FILE, 'r', encoding='latin-1') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row["Username"] == username and row["Password"] == password:
                    return True
        return False

    def user_exists(self, username):
        
        if not os.path.isfile(COMPTES_FILE):
            return False
        with open(COMPTES_FILE, 'r', encoding='latin-1') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row["Username"] == username:
                    return True
        return False

    def get_user_data(self, username):
        
        if not os.path.isfile(COMPTES_FILE):
            return None
        with open(COMPTES_FILE, 'r', encoding='latin-1') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['Username'] == username:
                    return row
        return None

    def get_next_patient_id(self):
        
        if os.path.isfile(COMPTES_FILE):
            with open(COMPTES_FILE, 'r', newline='', encoding='latin-1') as f:
                reader = csv.DictReader(f)
                ids = [int(row["PatientID"]) for row in reader if row["PatientID"].isdigit()]
                return max(ids) + 1 if ids else 1
        return 1