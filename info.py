import customtkinter as ctk
from ArbreBinaire import ArbreBinaire

class ArbreVisualisateur:
    def __init__(self):
        self.rectangle_info = None  # Rectangle affichant l’info-bulle
        self.label_info = None      # Texte des définitions
        self.noeuds_affiches = set()  # Ensemble pour suivre les nœuds déjà affichés

        # Dictionnaire contenant toutes les définitions médicales associées aux termes
        self.definitions = {
            "Globules rouges": "Cellules du sang qui transportent l'oxygène dans tout le corps.",
            "Anémie": "Pas assez de globules rouges dans le sang, ce qui peut causer de la fatigue.",
            "Polyglobulie": "Trop de globules rouges, ce qui peut épaissir le sang.",
            "Globules blancs": "Cellules du sang qui combattent les infections.",
            "Infection": "Présence de bactéries, virus ou autres agents pathogènes dans le corps.",
            "Leucémie": "Cancer des globules blancs.",
            "Hypoglycémie": "Niveau de sucre trop bas dans le sang.",
            "Diabète": "Maladie caractérisée par un excès de sucre dans le sang.",
            "Cholestérol total": "Quantité totale de cholestérol dans le sang.",
            "LDL (mauvais)": "Mauvais cholestérol, peut s'accumuler dans les artères.",
            "HDL (bon)": "Bon cholestérol, aide à éliminer le mauvais cholestérol.",
            "Triglycérides": "Type de graisse dans le sang, source d'énergie.",
            "Hypertriglycéri-démie": "Trop de triglycérides, augmente le risque cardiovasculaire.",
            "ASAT / ALAT": "Enzymes hépatiques, indicateurs de santé du foie.",
            "Hépatite": "Inflammation du foie.",
            "Cirrhose": "Cicatrisation sévère du foie.",
            "Gamma-GT / Bilirubine": "Marqueurs de la fonction biliaire et hépatique.",
            "Alcoolisme": "Consommation excessive d'alcool, peut abîmer le foie.",
            "Obstruction biliaire": "Blocage dans les voies biliaires.",
            "Créatinine / Urée": "Marqueurs de la fonction rénale.",
            "Insuffisance rénale": "Fonction rénale diminuée.",
            "Ionogramme": "Mesure des électrolytes dans le sang.",
            "Déséquilibre électrolytique": "Trouble des sels minéraux comme le sodium, potassium.",
            "Infection aiguë": "Infection récente et rapide.",
            "Maladie inflammatoire chronique": "Inflammation prolongée dans le corps.",
            "Hypothyroïdie": "Fonction thyroïdienne ralentie.",
            "Hyperthyroïdie": "Fonction thyroïdienne excessive.",
            "Anémie ferriprive": "Manque de fer entraînant une anémie.",
            "Hémochromato-se": "Maladie où le corps stocke trop de fer, ce qui peut endommager les organes."
        }

        # Liste des arbres binaires représentant les bilans biologiques
        self.arbres = [
            ArbreBinaire("Numération Formule Sanguine",
                         ArbreBinaire("Globules rouges", ArbreBinaire("Anémie"), ArbreBinaire("Polyglobulie")),
                         ArbreBinaire("Globules blancs", ArbreBinaire("Infection"), ArbreBinaire("Leucémie"))),
            ArbreBinaire("Glycémie à jeun", ArbreBinaire("Hypoglycémie"), ArbreBinaire("Diabète")),
            ArbreBinaire("Bilan lipidique",
                         ArbreBinaire("Cholestérol total", ArbreBinaire("LDL (mauvais)"), ArbreBinaire("HDL (bon)")),
                         ArbreBinaire("Triglycérides", ArbreBinaire("Hypertriglycéri-démie"), None)),
            ArbreBinaire("Bilan hépatique",
                         ArbreBinaire("ASAT / ALAT", ArbreBinaire("Hépatite"), ArbreBinaire("Cirrhose")),
                         ArbreBinaire("Gamma-GT / Bilirubine", ArbreBinaire("Alcoolisme"), ArbreBinaire("Obstruction biliaire"))),
            ArbreBinaire("Bilan rénal",
                         ArbreBinaire("Créatinine / Urée", ArbreBinaire("Insuffisance rénale"), None),
                         ArbreBinaire("Ionogramme", ArbreBinaire("Déséquilibre électrolytique"), None)),
            ArbreBinaire("CRP (Inflammation)", ArbreBinaire("Infection aiguë"), ArbreBinaire("Maladie inflammatoire chronique")),
            ArbreBinaire("TSH (Thyroïdienne)", ArbreBinaire("Hypothyroïdie"), ArbreBinaire("Hyperthyroïdie")),
            ArbreBinaire("Fer / Ferritine", ArbreBinaire("Anémie ferriprive"), ArbreBinaire("Hémochromato-se"))
        ]

    def calculer_profondeur(self, arbre):
        # Calcule la profondeur maximale d’un arbre, permet de connaitre le nombre d'espace vertical pour eviter le chevauchement
        if arbre is None:
            return 0
        return 1 + max(self.calculer_profondeur(arbre.getFilsGauche()),
                       self.calculer_profondeur(arbre.getFilsDroit()))

    def dessiner_arbre(self, canvas, arbre, x, y, espace, niveau, profondeur_max):
        if arbre is not None:
            rayon = 65  # Rayon du cercle représentant un nœud
            couleurs = ["#27A8AF", "#3E5A6A", "#5494AC"]  # Couleurs par niveau
            couleur_noeud = couleurs[niveau % len(couleurs)]

            tag = f"noeud_{x}_{y}"  # Identifiant unique du nœud
            # Crée le cercle
            cercle = canvas.create_oval(x - rayon, y - rayon, x + rayon, y + rayon,
                                        outline="black", width=2, fill=couleur_noeud, tags=tag)
            # Ajoute le texte au centre
            texte = canvas.create_text(x, y, text=arbre.getElement(),
                                       font=("Arial", 12, "bold"), fill="#B8C8CE", width=120, tags=tag)

            def afficher_info(event, tag=tag, texte=arbre.getElement(), niveau=niveau, x=x, y=y):
                # Affiche ou masque la définition au clic pour les niveaux 1 et 2
                if niveau < 1 or niveau > 2:
                    return  # Ignore les autres niveaux

                if tag in self.noeuds_affiches:
                    # Si déjà affiché → retire l’info-bulle
                    if self.rectangle_info:
                        canvas.delete(self.rectangle_info)
                        self.rectangle_info = None
                    if self.label_info:
                        canvas.delete(self.label_info)
                        self.label_info = None
                    self.noeuds_affiches.remove(tag)
                else:
                    # Si pas affiché → affiche la définition
                    if self.rectangle_info:
                        canvas.delete(self.rectangle_info)
                    if self.label_info:
                        canvas.delete(self.label_info)

                    rect_x1 = x - 110
                    rect_x2 = x + 110
                    rect_y1 = y - 100
                    rect_y2 = y - 60

                    texte_info = self.definitions.get(texte, "Définition non disponible.")
                    self.rectangle_info = canvas.create_rectangle(rect_x1, rect_y1, rect_x2, rect_y2,
                                                                  fill="white", outline="black")
                    self.label_info = canvas.create_text((rect_x1 + rect_x2) // 2,
                                                         (rect_y1 + rect_y2) // 2,
                                                         text=texte_info, fill="black",
                                                         font=("Arial", 9), width=200)
                    self.noeuds_affiches.add(tag)

            # Connecte l’événement clic au nœud
            canvas.tag_bind(tag, "<Button-1>", afficher_info)

            if arbre.getFilsGauche():
                x_gauche = x - espace // 2
                y_fils = y + 150 #descend de 150 pixels pour dessiner la prochaien ligne
                canvas.create_line(x, y + rayon, x_gauche, y_fils - rayon,
                                   fill="black", width=2)
                self.dessiner_arbre(canvas, arbre.getFilsGauche(), x_gauche, y_fils,
                                    espace // 2, niveau + 1, profondeur_max)
            if arbre.getFilsDroit():
                x_droit = x + espace // 2
                y_fils = y + 150
                canvas.create_line(x, y + rayon, x_droit, y_fils - rayon,
                                   fill="black", width=2)
                self.dessiner_arbre(canvas, arbre.getFilsDroit(), x_droit, y_fils,
                                    espace // 2, niveau + 1, profondeur_max)

    def afficher_arbres(self, frame_principal):
        # Nettoie le frame principal
        for widget in frame_principal.winfo_children(): #nomée info_children car les définitions devaient etre compréhensibles par des enfants
            widget.destroy()

        # Crée le conteneur
        container_frame = ctk.CTkFrame(frame_principal, fg_color="#B8C8CE")
        container_frame.pack(fill="both", expand=True)

        # Calcule la hauteur nécessaire pour afficher tous les arbres
        hauteur_totale = 0
        espacement_vertical = 250 #nombres pixels par niveau
        marge_verticale = 100

        for arbre in self.arbres:
            profondeur = self.calculer_profondeur(arbre)
            hauteur_totale += (profondeur + 1) * espacement_vertical

        hauteur_totale += marge_verticale * 2

        # Crée le canvas
        self.canvas = ctk.CTkCanvas(
            container_frame,
            width=2000,
            height=hauteur_totale,
            bg="#FFFFFF",
            highlightthickness=0
        )
        self.canvas.pack(fill="both", expand=True)

        # Position de départ
        y_offset = marge_verticale
        x_center = 1000
        espacement_horizontal = 900

        # Dessine chaque arbre
        for arbre in self.arbres:
            profondeur_max = self.calculer_profondeur(arbre)
            self.dessiner_arbre(
                self.canvas,
                arbre,
                x_center,
                y_offset,
                espacement_horizontal,
                0,
                profondeur_max
            )
            y_offset += (profondeur_max + 1) * espacement_vertical

        # Ajuste la zone scrollable
        bbox = self.canvas.bbox("all")
        if bbox:
            margin = 100
            scroll_region = (
                bbox[0] - margin,
                bbox[1] - margin,
                bbox[2] + margin,
                bbox[3] + margin
            )
            self.canvas.configure(scrollregion=scroll_region)

        # Met à jour le canvas
        self.canvas.update_idletasks()