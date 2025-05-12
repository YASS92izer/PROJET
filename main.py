import customtkinter as ctk
from connexion import MedicalApp
from interface import App

class MainApplication(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("MediLabPro")
        self.geometry("1200x800")
        self.iconbitmap("logo.ico")
        
        # Frame principal qui contiendra toutes les interfaces
        self.main_container = ctk.CTkFrame(self)
        self.main_container.pack(fill="both", expand=True)
        
        # Commencer par l'interface de connexion
        self.show_login()

    def show_login(self):
        # Nettoyer le conteneur principal
        for widget in self.main_container.winfo_children():
            widget.destroy()
            
        # Créer et afficher l'interface de connexion
        self.login_frame = MedicalApp(self.main_container, self.on_login_success)
        self.login_frame.pack(fill="both", expand=True)

    def show_main_app(self, patient_data):
        # Nettoyer le conteneur principal
        for widget in self.main_container.winfo_children():
            widget.destroy()
            
        # Créer et afficher l'interface principale
        self.main_app = App(self.main_container, patient_data)
        self.main_app.pack(fill="both", expand=True)

    def on_login_success(self, patient_data):
        # Cette méthode sera appelée après une connexion réussie
        self.show_main_app(patient_data)

def main():
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")
    
    app = MainApplication()
    app.mainloop()

if __name__ == "__main__":
    main()