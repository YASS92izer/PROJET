import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns

class GestionnaireBilanSanguin:
    def __init__(self):
        # Initialisation du gestionnaire
        try:
            self.df = pd.read_csv('donnees.csv')
        except FileNotFoundError:
            self.df = pd.DataFrame(columns=['PatientID', 'Date', 'Sexe', 'Age', 
                                          'GlobulesRouges', 'Hemoglobine', 'GlobulesBlancs',
                                          'Plaquettes', 'GlycemieAJjeun', 'CholesterolTotal',
                                          'HDL', 'LDL', 'Triglycerides', 'ASAT', 'ALAT',
                                          'GammaGT', 'Bilirubine', 'Creatinine', 'Uree',
                                          'Sodium', 'Potassium', 'Chlore', 'CRP', 'TSH',
                                          'Fer', 'Ferritine'])

    def ajouter_bilan(self, donnees):
        """
        Ajoute un nouveau bilan à partir des données reçues de l'interface.
        Limite à 3 bilans par patient, supprime le plus ancien si nécessaire.
        """
        try:
            self.df = pd.read_csv('donnees.csv')
            if 'Date' not in self.df.columns:
                self.df['Date'] = datetime.now().strftime("%Y-%m-%d")
        except FileNotFoundError:
            self.df = pd.DataFrame(columns=['PatientID', 'Sexe', 'Age', 
                                          'GlobulesRouges', 'Hemoglobine', 'GlobulesBlancs',
                                          'Plaquettes', 'GlycemieAJjeun', 'CholesterolTotal',
                                          'HDL', 'LDL', 'Triglycerides', 'ASAT', 'ALAT',
                                          'GammaGT', 'Bilirubine', 'Creatinine', 'Uree',
                                          'Sodium', 'Potassium', 'Chlore', 'CRP', 'TSH',
                                          'Fer', 'Ferritine'])
            if 'Date' not in self.df.columns:
                self.df['Date'] = None

        # Ajouter la date au nouveau bilan si elle n'existe pas
        if 'Date' not in donnees:
            donnees['Date'] = datetime.now().strftime("%Y-%m-%d")

        # Vérifier le nombre de bilans existants pour ce patient
        bilan_p = self.df[self.df['PatientID'] == donnees['PatientID']]
        
        if len(bilan_p) >= 3:
            print(f"Le patient {donnees['PatientID']} a déjà 3 bilans.")
            print("Le bilan le plus ancien sera supprimé pour ajouter le nouveau.")
            
            # Trier les bilans par date et garder les 2 plus récents
            bilan_p = bilan_p.sort_values('Date')
            bilan_a_supprimer = bilan_p.iloc[0]
            
            # Supprimer le bilan le plus ancien
            self.df = self.df[~((self.df['PatientID'] == donnees['PatientID']) & 
                               (self.df['Date'] == bilan_a_supprimer['Date']))]
            
            

        # Vérifier si un bilan existe déjà pour cette date
        if 'Date' in self.df.columns:
            bilan_existant = self.df[
                (self.df['PatientID'] == donnees['PatientID']) & 
                (self.df['Date'] == donnees['Date'])
            ]
            
            if not bilan_existant.empty:
                print(f"Un bilan existe déjà pour le patient {donnees['PatientID']} à la date {donnees['Date']}")
                return None

        # Ajouter le nouveau bilan
        self.df = pd.concat([self.df, pd.DataFrame([donnees])], ignore_index=True)

        # Trier et réinitialiser l'index
        if 'Date' in self.df.columns:
            self.df = self.df.sort_values(['PatientID', 'Date'])
        else:
            self.df = self.df.sort_values('PatientID')
        
        self.df = self.df.reset_index(drop=True)

        # Sauvegarder
        self.sauvegarder()

        print(f"Nouveau bilan ajouté pour le patient {donnees['PatientID']}")
        return self.analyser_bilan(donnees)


    def sauvegarder(self):
        """Sauvegarde les données dans le fichier CSV"""
        self.df.to_csv('donnees.csv', index=False)

    def obtenir_bilan_p(self, patient_id):
        """Retourne tous les bilans d'un patient"""
        return self.df[self.df['PatientID'] == patient_id].sort_values('Date')

    def analyser_bilan(self, donnees):
        """Analyse un bilan et retourne les résultats"""
        resultats = {}
        for nom_test, valeur in donnees.items():
            if nom_test not in ['PatientID', 'Date', 'Sexe', 'Age']:
                resultats[nom_test] = self.evaluer_valeur(valeur, donnees['Sexe'], nom_test)
        return resultats

    def comparer_bilans(self, patient_id):
        """Compare les bilans d'un patient et retourne les variations"""
        bilans = self.obtenir_bilan_p(patient_id)
        if len(bilans) < 2:
            return None

        comparaisons = {}
        analyses = [col for col in self.df.columns if col not in ['PatientID', 'Date', 'Sexe', 'Age']]
        
        for analyse in analyses:
            valeurs = bilans[analyse].values
            dates = bilans['Date'].values
            
            variations = []
            for i in range(len(valeurs)-1):
                variation = ((valeurs[i+1] - valeurs[i]) / valeurs[i]) * 100
                variations.append({
                    'date_debut': dates[i],
                    'date_fin': dates[i+1],
                    'valeur_debut': valeurs[i],
                    'valeur_fin': valeurs[i+1],
                    'variation': variation
                })
            comparaisons[analyse] = variations
            
        return comparaisons

    def evaluer_valeur(self, valeur, sexe, nom_test):
        """Évalue une valeur par rapport aux références"""
        references = {
            'GlobulesRouges': {'Homme': (4.5, 5.5), 'Femme': (4.0, 5.0)},
            'Hemoglobine': {'Homme': (13, 17), 'Femme': (12, 16)},
            'GlobulesBlancs': {'tous': (4.0, 10.0)},
            'Plaquettes': {'tous': (150, 400)},
            'GlycemieAJjeun': {'tous': (70, 110)},
            'CholesterolTotal': {'tous': (0, 200)},
            'HDL': {'tous': (40, 100)},
            'LDL': {'tous': (0, 160)},
            'Triglycerides': {'tous': (0, 150)},
            'ASAT': {'tous': (0, 40)},
            'ALAT': {'tous': (0, 40)},
            'GammaGT': {'Homme': (0, 55), 'Femme': (0, 38)},
            'Bilirubine': {'tous': (0, 17)},
            'Creatinine': {'Homme': (62, 106), 'Femme': (44, 80)},
            'Uree': {'tous': (2.5, 7.5)},
            'Sodium': {'tous': (135, 145)},
            'Potassium': {'tous': (3.5, 5.0)},
            'Chlore': {'tous': (95, 105)},
            'CRP': {'tous': (0, 5)},
            'TSH': {'tous': (0.27, 4.2)},
            'Fer': {'Homme': (11, 27), 'Femme': (9, 21)},
            'Ferritine': {'Homme': (30, 300), 'Femme': (15, 150)}
        }

        if nom_test in references:
            if 'tous' in references[nom_test]:
                min_val, max_val = references[nom_test]['tous']
            else:
                min_val, max_val = references[nom_test][sexe]

            marge = (max_val - min_val) * 0.1
            
            return {
                'valeur': valeur,
                'min': min_val,
                'max': max_val,
                'statut': self._determiner_statut(valeur, min_val, max_val, marge)
            }
        
        return {'statut': "Référence non disponible"}

    def _determiner_statut(self, valeur, min_val, max_val, marge):
        """Détermine le statut d'une valeur"""
        if valeur < min_val:
            return "Trop basse"
        elif valeur > max_val:
            return "Trop élevée"
        elif (valeur - min_val) < marge or (max_val - valeur) < marge:
            return "Proche de la limite"
        else:
            return "Bonne"
    def references(self):
        """Retourne le dictionnaire des valeurs de référence"""
        return {
            'GlobulesRouges': {'Homme': (4.5, 5.5), 'Femme': (4.0, 5.0)},
            'Hemoglobine': {'Homme': (13, 17), 'Femme': (12, 16)},
            'GlobulesBlancs': {'tous': (4.0, 10.0)},
            'Plaquettes': {'tous': (150, 400)},
            'GlycemieAJjeun': {'tous': (70, 110)},
            'CholesterolTotal': {'tous': (0, 200)},
            'HDL': {'tous': (40, 100)},
            'LDL': {'tous': (0, 160)},
            'Triglycerides': {'tous': (0, 150)},
            'ASAT': {'tous': (0, 40)},
            'ALAT': {'tous': (0, 40)},
            'GammaGT': {'Homme': (0, 55), 'Femme': (0, 38)},
            'Bilirubine': {'tous': (0, 17)},
            'Creatinine': {'Homme': (62, 106), 'Femme': (44, 80)},
            'Uree': {'tous': (2.5, 7.5)},
            'Sodium': {'tous': (135, 145)},
            'Potassium': {'tous': (3.5, 5.0)},
            'Chlore': {'tous': (95, 105)},
            'CRP': {'tous': (0, 5)},
            'TSH': {'tous': (0.27, 4.2)},
            'Fer': {'Homme': (11, 27), 'Femme': (9, 21)},
            'Ferritine': {'Homme': (30, 300), 'Femme': (15, 150)}
        }
    def creer_graphique_comparaison(self, patient_id, categorie_choisie=None):
        """
        Crée un graphique comparatif des bilans d'un patient par catégorie avec un design amélioré
        """
        # Configuration du style seaborn
        sns.set_style("whitegrid")
        sns.set_context("notebook", font_scale=1.2)
        
        # Définition des couleurs
        colors = {
            'normal': '#2ecc71',     # Vert vif
            'haut': '#e74c3c',       # Rouge vif
            'bas': '#3498db',        # Bleu vif
            'reference': '#f39c12',   # Orange
            'text': '#2c3e50'        # Bleu foncé pour le texte
        }
        
        categories = {
            'hematologie': ['GlobulesRouges', 'Hemoglobine', 'GlobulesBlancs', 'Plaquettes'],
            'biochimie': ['GlycemieAJjeun', 'Creatinine', 'Uree', 'Fer', 'Ferritine'],
            'lipides': ['CholesterolTotal', 'HDL', 'LDL', 'Triglycerides'],
            'enzymes': ['ASAT', 'ALAT', 'GammaGT'],
            'ionogramme': ['Sodium', 'Potassium', 'Chlore'],
            'autres': ['Bilirubine', 'CRP', 'TSH']
        }

        bilans = self.obtenir_bilan_p(patient_id)
        
        if len(bilans) < 2:
            print("Pas assez de bilans pour faire une comparaison")
            return None

        if categorie_choisie is None:
            print("Catégories disponibles:")
            for cat in categories.keys():
                print(f"- {cat}")
            return None

        if categorie_choisie not in categories:
            print("Catégorie non valide")
            return None

        parametres = categories[categorie_choisie]
        n_parametres = len(parametres)
        n_cols = min(3, n_parametres)
        n_rows = (n_parametres + n_cols - 1) // n_cols

        # Création de la figure
        fig = plt.figure(figsize=(15, 4 * n_rows))
        sns.set_palette("husl")

        # Titre principal avec style seaborn
        fig.suptitle(f'Évolution des paramètres - {categorie_choisie.capitalize()}', 
                     fontsize=16, fontweight='bold', color=colors['text'], y=0.95)

        # Ajustement des espacements
        plt.subplots_adjust(hspace=0.5, wspace=0.3)

        for idx, parametre in enumerate(parametres, 1):
            ax = fig.add_subplot(n_rows, n_cols, idx)
            
            dates = bilans['Date'].values
            valeurs = bilans[parametre].values
            x = range(len(dates))
            
            # Création des barres avec style seaborn
            bars = sns.barplot(x=x, y=valeurs, ax=ax, alpha=0.8)
            
            # Ajout des valeurs sur les barres
            for i, v in enumerate(valeurs):
                ax.text(i, v, f'{v:.1f}', 
                       ha='center', va='bottom',
                       fontweight='bold', fontsize=10,
                       color=colors['text'])
            
            # Personnalisation des axes et titres
            ax.set_title(parametre, pad=20, fontsize=12, fontweight='bold', color=colors['text'])
            ax.set_xticks(x)
            ax.set_xticklabels(dates, rotation=45, ha='right')
            
            # Ajout des limites de référence
            references = self.references()
            if parametre in references:
                ref = references[parametre]
                if 'tous' in ref:
                    min_val, max_val = ref['tous']
                else:
                    sexe = bilans['Sexe'].iloc[0]
                    min_val, max_val = ref[sexe]
                
                # Lignes de référence
                ax.axhline(y=min_val, color=colors['reference'], linestyle='--', alpha=0.5, linewidth=2)
                ax.axhline(y=max_val, color=colors['reference'], linestyle='--', alpha=0.5, linewidth=2)
                
                # Zone normale en transparence
                ax.fill_between([-0.5, len(dates)-0.5], min_val, max_val, 
                              color=colors['normal'], alpha=0.1)
                
                # Coloration des barres selon les valeurs
                for i, (patch, valeur) in enumerate(zip(ax.patches, valeurs)):
                    if valeur < min_val:
                        patch.set_facecolor(colors['bas'])
                    elif valeur > max_val:
                        patch.set_facecolor(colors['haut'])
                    else:
                        patch.set_facecolor(colors['normal'])
                    patch.set_edgecolor('white')
                    patch.set_linewidth(1)

        # Création de la légende personnalisée
        legend_elements = [
            plt.Rectangle((0,0),1,1, facecolor=colors['normal'], label='Normal'),
            plt.Rectangle((0,0),1,1, facecolor=colors['bas'], label='Bas'),
            plt.Rectangle((0,0),1,1, facecolor=colors['haut'], label='Élevé')
        ]
        
        # Ajout de la légende avec style seaborn
        fig.legend(handles=legend_elements,
                  loc='center', 
                  bbox_to_anchor=(0.5, 0.02),
                  ncol=3,
                  frameon=True,
                  facecolor='white',
                  edgecolor='none',
                  fontsize=10)

        plt.tight_layout()
        return fig


"""def tester_fonctionnalites_classe():
    print("=== DÉBUT DES TESTS ===\n")
    
    # 1. Création de l'instance et affichage des données initiales
    print("1. Initialisation du gestionnaire")
    gestionnaire = GestionnaireBilanSanguin()
    print("Données initiales :")
    print(gestionnaire.df)
    print("\n" + "="*50 + "\n")

    # 2. Test d'ajout d'un nouveau bilan
    print("2. Test d'ajout d'un nouveau bilan")
    nouveau_bilan = {
        'PatientID': 1,
        'Sexe': 'Homme',
        'Age': 45,
        'GlobulesRouges': 4.8,
        'Hemoglobine': 14.5,
        'GlobulesBlancs': 6.0,
        'Plaquettes': 250,
        'GlycemieAJjeun': 92,
        'CholesterolTotal': 140,
        'HDL': 45,
        'LDL': 110,
        'Triglycerides': 140,
        'ASAT': 20,
        'ALAT': 15,
        'GammaGT': 30,
        'Bilirubine': 1.0,
        'Creatinine': 2.0,
        'Uree': 20,
        'Sodium': 110,
        'Potassium': 4.0,
        'Chlore': 100,
        'CRP': 5.0,
        'TSH': 2.0,
        'Fer': 70,
        'Ferritine': 150,
        'Date': "2025-04-03"
    }
    gestionnaire.ajouter_bilan(nouveau_bilan)
    print("\n" + "="*50 + "\n")

    # 3. Test d'ajout d'un deuxième bilan pour le même patient
    print("3. Test d'ajout d'un deuxième bilan pour le même patient")
    deuxieme_bilan = nouveau_bilan.copy()
    deuxieme_bilan.update({
        'GlobulesRouges': 5.0,
        'Hemoglobine': 15.0,
        'GlobulesBlancs': 6.5,
    })
    gestionnaire.ajouter_bilan(deuxieme_bilan)
    print("\n" + "="*50 + "\n")

    # 4. Test de la fonction obtenir_bilan_p
    print("4. Test de obtenir_bilan_p")
    bilan_p = gestionnaire.obtenir_bilan_p(6)
    print("Bilans du patient 6 :")
    print(bilan_p)
    print("\n" + "="*50 + "\n")

    # 5. Test de la fonction analyser_bilan
    print("5. Test de analyser_bilan")
    analyse = gestionnaire.analyser_bilan(nouveau_bilan)
    print("Analyse du bilan :")
    for test, resultat in analyse.items():
        print(f"{test}: {resultat}")
    print("\n" + "="*50 + "\n")

    # 6. Test de la fonction comparer_bilans
    print("6. Test de comparer_bilans")
    comparaisons = gestionnaire.comparer_bilans(1)
    if comparaisons:
        print("Comparaison des bilans :")
        for test, variations in comparaisons.items():
            for var in variations:
                print(f"\n{test}:")
                print(f"  Du {var['date_debut']} au {var['date_fin']}")
                print(f"  Valeur initiale: {var['valeur_debut']:.2f}")
                print(f"  Valeur finale: {var['valeur_fin']:.2f}")
                print(f"  Variation: {var['variation']:.1f}%")
    print("\n" + "="*50 + "\n")

    # 7. Test de la fonction evaluer_valeur
    print("7. Test de evaluer_valeur")
    evaluation = gestionnaire.evaluer_valeur(4.8, 'Homme', 'GlobulesRouges')
    print("Évaluation des globules rouges :")
    print(evaluation)
    print("\n" + "="*50 + "\n")

    # 8. Test de création du graphique
    print("8. Test de création du graphique")
    print("Création du graphique de comparaison...")
    fig = gestionnaire.creer_graphique_comparaison(1)
    if fig:
        print("Graphique créé avec succès")
        plt.show()
    print("\n" + "="*50 + "\n")

    # 9. Test d'ajout d'un bilan avec date existante (doit échouer)
    print("9. Test d'ajout d'un bilan avec date existante")
    bilan_meme_date = nouveau_bilan.copy()
    gestionnaire.ajouter_bilan(bilan_meme_date)
    print("\n" + "="*50 + "\n")

    # 10. Vérification finale des données
    print("10. Vérification finale des données")
    print("Contenu final du DataFrame :")
    print(gestionnaire.df)
    print("\nContenu du fichier CSV :")
    df_verification = pd.read_csv('donnees.csv')
    print(df_verification)
    print("\n=== FIN DES TESTS ===")

if __name__ == "__main__":
    tester_fonctionnalites_classe()"""
print("2. Test d'ajout d'un nouveau bilan")
gestionnaire = GestionnaireBilanSanguin()
nouveau_bilan = {
    'PatientID': 6,
    'Sexe': 'Homme',
    'Age': 45,
    'GlobulesRouges': 3.8,
    'Hemoglobine': 14.5,
    'GlobulesBlancs': 6.0,
    'Plaquettes': 550,
    'GlycemieAJjeun': 92,
    'CholesterolTotal': 140,
    'HDL': 45,
    'LDL': 110,
    'Triglycerides': 140,
    'ASAT': 20,
    'ALAT': 15,
    'GammaGT': 30,
    'Bilirubine': 1.0,
    'Creatinine': 2.0,
    'Uree': 20,
    'Sodium': 110,
    'Potassium': 4.0,
    'Chlore': 150,
    'CRP': 5.0,
    'TSH': 2.0,
    'Fer': 70,
    'Ferritine': 150,
    'Date': "2025-04-05"
}
gestionnaire.ajouter_bilan(nouveau_bilan)
    
def tester_graphiques():
    gestionnaire = GestionnaireBilanSanguin()
    
    # Test de chaque catégorie de graphiques
    categories = ['hematologie', 'biochimie', 'lipides', 'enzymes', 'ionogramme', 'autres']
    
    for categorie in categories:
        print(f"\nCréation du graphique pour la catégorie : {categorie}")
        fig = gestionnaire.creer_graphique_comparaison(6, categorie)
        if fig:
            plt.show()
            plt.close()  # Fermer la figure après affichage

if __name__ == "__main__":
    tester_graphiques()