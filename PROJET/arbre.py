import customtkinter as ctk
from ArbreBinaire import ArbreBinaire

rectangle_info = None
label_info = None
noeuds_affiches = set()

definitions = {
    "Globules rouges": "Cellules du sang qui transportent l'oxygène dans tout le corps.",
    "Anémie": "Pas assez de globules rouges dans le sang, ce qui peut causer de la fatigue.",
    "Polyglobulie": "Trop de globules rouges, ce qui rend le sang plus épais.",
    "Globules blancs": "Cellules du sang qui aident à combattre les infections et les maladies.",
    "Infection": "Des microbes envahissent le corps et causent des maladies.",
    "Leucémie": "Un cancer du sang qui affecte les globules blancs et leur production.",
    "Hypoglycémie": "Niveau de sucre dans le sang trop bas, ce qui peut causer des vertiges ou de la faiblesse.",
    "Diabète": "Maladie où le corps ne contrôle pas bien le sucre dans le sang, souvent trop élevé.",
    "Cholestérol total": "Mesure de toute la quantité de cholestérol dans le sang. Il peut être 'bon' ou 'mauvais'.",
    "Triglycérides": "Un type de graisse dans le sang. Trop peut être mauvais pour la santé.",
    "LDL (mauvais)": "Cholestérol qui peut se coller aux parois des artères et les boucher.",
    "HDL (bon)": "Cholestérol qui aide à éliminer le mauvais cholestérol et protège les artères.",
    "Hypertriglycéri-démie": "Un taux trop élevé de triglycérides dans le sang.",
    "ASAT / ALAT": "Enzymes du foie. Un taux élevé peut signaler un problème au foie.",
    "Hépatite": "Inflammation du foie souvent causée par un virus, de l'alcool ou des médicaments.",
    "Cirrhose": "Maladie du foie où le tissu devient dur et cicatrisé, cause :infection ou consommation excessive d'alcool.",
    "Gamma-GT / Bilirubine": "Substances mesurées pour évaluer la fonction du foie et des voies biliaires.",
    "Alcoolisme": "Dépendance à l’alcool, qui peut causer des problèmes de santé graves, notamment au foie.",
    "Obstruction biliaire": "Problème où la bile ne peut pas circuler correctement, ce qui peut affecter la digestion.",
    "Créatinine / Urée": "Produits chimiques filtrés par les reins. Leur taux indique si les reins fonctionnent bien.",
    "Insuffisance rénale": "Quand les reins ne sont pas capables de filtrer correctement le sang.",
    "Ionogramme": "Mesure de certains sels et minéraux dans le sang. Un déséquilibre peut être dangereux.",
    "Déséquilibre électrolytique": "Trop ou trop peu de sels dans le corps, ce qui peut perturber la santé.",
    "CRP (Inflammation)": "Protéine présente dans le sang. Un taux élevé peut signaler une infection ou une inflammation.",
    "Infection aiguë": "Une infection soudaine et rapide, souvent accompagnée de symptômes comme la fièvre.",
    "Maladie inflammatoire chronique": "Maladie où le corps est en inflammation continue.",
    "TSH (Thyroïdienne)": "Hormone produite par la glande thyroïdienne, qui contrôle le métabolisme. Un déséquilibre peut affecter l'énergie et le poids.",
    "Hypothyroïdie": "Glande thyroïdienne trop lente, causant fatigue, prise de poids et dépression.",
    "Hyperthyroïdie": "Glande thyroïdienne trop active, causant nervosité, perte de poids et palpitations.",
    "Fer / Ferritine": "Le fer est essentiel pour produire des globules rouges. La ferritine est une protéine qui stocke le fer.",
    "Anémie ferriprive": "Anémie causée par un manque de fer, ce qui rend une personne fatiguée et pâle.",
    "Hémochromato-se": "Une maladie où le corps stocke trop de fer, ce qui peut endommager les organes."
}

def calculer_profondeur(arbre):
    if arbre is None:
        return 0
    return 1 + max(calculer_profondeur(arbre.getFilsGauche()), calculer_profondeur(arbre.getFilsDroit()))

def dessiner_arbre(canvas, arbre, x, y, espace, niveau, profondeur_max):
    if arbre is not None:
        rayon = 65
        couleurs = ["#27A8AF", "#3E5A6A", "#5494AC"]
        couleur_noeud = couleurs[niveau % len(couleurs)]

        tag = f"noeud_{x}_{y}"
        cercle = canvas.create_oval(x - rayon, y - rayon, x + rayon, y + rayon, outline="black", width=2, fill=couleur_noeud, tags=tag)
        canvas.create_text(x, y, text=arbre.getElement(), font=("Arial", 12, "bold"), fill="#B8C8CE", width=120)

        def afficher_info(event, tag=tag, texte=arbre.getElement(), niveau=niveau, x=x, y=y):
            global rectangle_info, label_info

            if niveau < 1 or niveau > 2:
                return

            if tag in noeuds_affiches:
                if rectangle_info:
                    canvas.delete(rectangle_info)
                    rectangle_info = None
                if label_info:
                    canvas.delete(label_info)
                    label_info = None
                noeuds_affiches.remove(tag)
            else:
                if rectangle_info:
                    canvas.delete(rectangle_info)
                if label_info:
                    canvas.delete(label_info)

                rect_x1 = x - 110
                rect_x2 = x + 110
                rect_y1 = y - 100
                rect_y2 = y - 60

                texte_info = definitions.get(texte, "Définition non disponible.")
                rectangle_info = canvas.create_rectangle(rect_x1, rect_y1, rect_x2, rect_y2, fill="white", outline="black")
                label_info = canvas.create_text((rect_x1 + rect_x2) // 2, (rect_y1 + rect_y2) // 2, text=texte_info, fill="black", font=("Arial", 9), width=200)

                noeuds_affiches.add(tag)

        canvas.tag_bind(cercle, "<Button-1>", afficher_info)

        if arbre.getFilsGauche():
            x_gauche = x - espace // 2
            y_fils = y + 150
            canvas.create_line(x, y + rayon, x_gauche, y_fils - rayon, fill="black", width=2)
            dessiner_arbre(canvas, arbre.getFilsGauche(), x_gauche, y_fils, espace // 2, niveau + 1, profondeur_max)
        if arbre.getFilsDroit():
            x_droit = x + espace // 2
            y_fils = y + 150
            canvas.create_line(x, y + rayon, x_droit, y_fils - rayon, fill="black", width=2)
            dessiner_arbre(canvas, arbre.getFilsDroit(), x_droit, y_fils, espace // 2, niveau + 1, profondeur_max)

def lors_du_scroll_souris(event):
    canvas.yview_scroll(-1 * (event.delta // 120), "units")

def afficher_arbres(arbres):
    global canvas
    ctk.set_appearance_mode("dark")
    fenetre = ctk.CTk()
    fenetre.title("Lien entre les mesures et les maladies")
    fenetre.geometry("1200x700")
    fenetre.configure(bg="#B8C8CE")

    frame_principale = ctk.CTkFrame(fenetre, fg_color="#B8C8CE")
    frame_principale.pack(fill=ctk.BOTH, expand=True, padx=10, pady=10)

    canvas = ctk.CTkCanvas(frame_principale, width=1200, height=600, bg="#B8C8CE")
    scrollbar = ctk.CTkScrollbar(frame_principale, orientation="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side=ctk.RIGHT, fill=ctk.Y)
    canvas.pack(side=ctk.LEFT, fill=ctk.BOTH, expand=True)

    frame_canvas = ctk.CTkFrame(canvas, fg_color="#B8C8CE")
    canvas.create_window((0, 0), window=frame_canvas, anchor="nw")

    y_offset = 70
    for arbre in arbres:
        profondeur_max = calculer_profondeur(arbre)
        dessiner_arbre(canvas, arbre, 700, y_offset, 600, 0, profondeur_max)
        y_offset += (profondeur_max + 1) * 150

    frame_canvas.update_idletasks()
    canvas.config(scrollregion=(0, 0, 1200, y_offset))
    canvas.bind_all("<MouseWheel>", lors_du_scroll_souris)
    fenetre.mainloop()

arbres = [
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

afficher_arbres(arbres)
