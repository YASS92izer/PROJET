import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns

class GestionnaireBilanSanguin:
    def __init__(self):
        try:
            # Essayer de lire avec UTF-8
            try:
                self.df = pd.read_csv('donnees.csv', encoding='utf-8')
            except UnicodeDecodeError:
                # Si problème, lire avec latin-1
                self.df = pd.read_csv('donnees.csv', encoding='latin-1')
        
        except FileNotFoundError:
            # Créer un DataFrame vide avec les colonnes attendues
            self.df = pd.DataFrame(columns=[
                'PatientID', 'Date', 'Sexe', 'Age', 
                'Globules Rouges', 'Hémoglobine', 'Globules Blancs',
                'Plaquettes', 'Glycémie à jeun', 'Cholestérol Total',
                'HDL', 'LDL', 'Triglycérides', 'ASAT', 'ALAT',
                'Gamma GT', 'Bilirubine', 'Créatinine', 'Urée',
                'Sodium', 'Potassium', 'Chlore', 'CRP', 'TSH',
                'Fer', 'Ferritine'
            ])
        except Exception as e:
            print(f"Erreur lors du chargement du fichier : {e}")
            # Créer un DataFrame vide
            self.df = pd.DataFrame(columns=[
                'PatientID', 'Date', 'Sexe', 'Age', 
                'Globules Rouges', 'Hémoglobine', 'Globules Blancs',
                'Plaquettes', 'Glycémie à jeun', 'Cholestérol Total',
                'HDL', 'LDL', 'Triglycérides', 'ASAT', 'ALAT',
                'Gamma GT', 'Bilirubine', 'Créatinine', 'Urée',
                'Sodium', 'Potassium', 'Chlore', 'CRP', 'TSH',
                'Fer', 'Ferritine'
            ])

    def ajouter_bilan(self, donnees):
        """
        Ajoute un nouveau bilan à partir des données reçues de l'interface.
        Limite à 3 bilans par patient, supprime le plus ancien si nécessaire.
        """
        # Valider le format de la date
        try:
            # Vérifier le format de la date (AAAA-MM-JJ)
            date_saisie = donnees.get('Date', '')
            
            # Vérifier si la date est vide
            if not date_saisie:
                raise ValueError("La date ne peut pas être vide")
            
            # Essayer de parser la date avec le format spécifique
            datetime.strptime(date_saisie, '%Y-%m-%d')
        
        except ValueError:
            # Lever une exception avec un message détaillé
            raise ValueError("Format de date incorrect. Utilisez le format AAAA-MM-JJ (ex: 2023-06-15)")

        try:
            # Utiliser UTF-8 avec une solution de secours
            try:
                self.df = pd.read_csv('donnees.csv', encoding='utf-8')
            except UnicodeDecodeError:
                self.df = pd.read_csv('donnees.csv', encoding='latin-1')
            
            # Ajouter la colonne Date si manquante
            if 'Date' not in self.df.columns:
                self.df['Date'] = datetime.now().strftime("%Y-%m-%d")
        
        except FileNotFoundError:
            # Créer un DataFrame avec toutes les colonnes nécessaires
            self.df = pd.DataFrame(columns=[
                'PatientID', 'Date', 'Sexe', 'Age', 
                'Globules Rouges', 'Hémoglobine', 'Globules Blancs',
                'Plaquettes', 'Glycémie à jeun', 'Cholestérol Total',
                'HDL', 'LDL', 'Triglycérides', 'ASAT', 'ALAT',
                'Gamma GT', 'Bilirubine', 'Créatinine', 'Urée',
                'Sodium', 'Potassium', 'Chlore', 'CRP', 'TSH',
                'Fer', 'Ferritine'
            ])

        # Vérifier le nombre de bilans existants pour ce patient
        bilan_p = self.df[self.df['PatientID'] == donnees['PatientID']]
        
        # Limiter à 3 bilans
        if len(bilan_p) >= 3:
            # Trier les bilans par date et supprimer le plus ancien
            bilan_p_tries = bilan_p.sort_values('Date')
            self.df = self.df[~(
                (self.df['PatientID'] == donnees['PatientID']) & 
                (self.df['Date'] == bilan_p_tries.iloc[0]['Date'])
            )]

        # Vérifier si un bilan existe déjà pour cette date
        bilan_existant = self.df[
            (self.df['PatientID'] == donnees['PatientID']) & 
            (self.df['Date'] == donnees['Date'])
        ]
        
        if not bilan_existant.empty:
            print(f"Un bilan existe déjà pour le patient {donnees['PatientID']} à la date {donnees['Date']}")
            return None

        # Créer un DataFrame avec les données
        nouveau_bilan = pd.DataFrame([donnees])

        # Ajouter le nouveau bilan
        self.df = pd.concat([self.df, nouveau_bilan], ignore_index=True)

        # Trier par PatientID et Date
        self.df = self.df.sort_values(['PatientID', 'Date']).reset_index(drop=True)

        
        self.sauvegarder()

        print(f"Nouveau bilan ajouté pour le patient {donnees['PatientID']}")
        return self.analyser_bilan(donnees)

    def sauvegarder(self):
        """Sauvegarde les données dans le fichier CSV"""
        try:
            # Sauvegarder avec latin-1 et forcer l'encodage correct des colonnes
            self.df.to_csv('donnees.csv', index=False, encoding='latin-1')
        except Exception as e:
            print(f"Erreur lors de la sauvegarde : {e}")

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
            'Globules Rouges': {'Homme': (4.5, 5.5), 'Femme': (4.0, 5.0)},
            'Hémoglobine': {'Homme': (13, 17), 'Femme': (12, 16)},
            'Globules Blancs': {'tous': (4.0, 10.0)},
            'Plaquettes': {'tous': (150, 400)},
            'Glycémie à jeun': {'tous': (70, 110)},
            'Cholestérol Total': {'tous': (0, 200)},
            'HDL': {'tous': (40, 100)},
            'LDL': {'tous': (0, 160)},
            'Triglycérides': {'tous': (0, 150)},
            'ASAT': {'tous': (0, 40)},
            'ALAT': {'tous': (0, 40)},
            'Gamma GT': {'Homme': (0, 55), 'Femme': (0, 38)},
            'Bilirubine': {'tous': (0, 17)},
            'Créatinine': {'Homme': (62, 106), 'Femme': (44, 80)},
            'Urée': {'tous': (2.5, 7.5)},
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
            'Globules Rouges': {'Homme': (4.5, 5.5), 'Femme': (4.0, 5.0)},
            'Hémoglobine': {'Homme': (13, 17), 'Femme': (12, 16)},
            'Globules Blancs': {'tous': (4.0, 10.0)},
            'Plaquettes': {'tous': (150, 400)},
            'Glycémie à jeun': {'tous': (70, 110)},
            'Cholestérol Total': {'tous': (0, 200)},
            'HDL': {'tous': (40, 100)},
            'LDL': {'tous': (0, 160)},
            'Triglycérides': {'tous': (0, 150)},
            'ASAT': {'tous': (0, 40)},
            'ALAT': {'tous': (0, 40)},
            'Gamma GT': {'Homme': (0, 55), 'Femme': (0, 38)},
            'Bilirubine': {'tous': (0, 17)},
            'Créatinine': {'Homme': (62, 106), 'Femme': (44, 80)},
            'Urée': {'tous': (2.5, 7.5)},
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
        
        sns.set_style("whitegrid")
        sns.set_context("notebook", font_scale=1.2)
        
        
        colors = {
            'normal': '#2ecc71',     
            'haut': '#e74c3c',       
            'bas': '#023E8A',        
            'reference': '#f39c12',   
            'text': '#2c3e50'        
        }
        
        categories = {
            'hematologie': ['Globules Rouges', 'Hémoglobine', 'Globules Blancs', 'Plaquettes'],
            'biochimie': ['Glycémie à jeun', 'Créatinine', 'Urée', 'Fer', 'Ferritine'],
            'lipides': ['Cholestérol Total', 'HDL', 'LDL', 'Triglycérides'],
            'enzymes': ['ASAT', 'ALAT', 'Gamma GT'],
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

        
        plt.subplots_adjust(hspace=0.5, wspace=0.3)

        for idx, parametre in enumerate(parametres, 1):
            
            ax = fig.add_subplot(n_rows, n_cols, idx)
            
            dates = bilans['Date'].values
            valeurs = bilans[parametre].values
            x = range(len(dates))
            
            
            bars = sns.barplot(x=x, y=valeurs, ax=ax, alpha=0.8)
            
            # Ajout des valeurs sur les barres
            for i, v in enumerate(valeurs):
                ax.text(i, v, f'{v:.1f}', 
                       ha='center', va='bottom',
                       fontweight='bold', fontsize=10,
                       color=colors['text'])
            
            
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

        # Création de la légende 
        legend_elements = [
            plt.Rectangle((0,0),1,1, facecolor=colors['normal'], label='Normal'),
            plt.Rectangle((0,0),1,1, facecolor=colors['bas'], label='Bas'),
            plt.Rectangle((0,0),1,1, facecolor=colors['haut'], label='Élevé')
        ]
        
        
        fig.legend(handles=legend_elements,
                  loc='center', 
                  bbox_to_anchor=(0.5, 0.02),
                  ncol=3,
                  frameon=True,
                  facecolor='white',
                  edgecolor='none',
                  fontsize=18)

        plt.tight_layout()
        return fig





