# MediLabPro

## Présentation du projet

MediLabPro est une application desktop pour la gestion et l'analyse des bilans sanguins. Elle permet aux patients de :

- Stocker et visualiser leurs résultats d'analyses sanguines
- Comparer les évolutions des différents paramètres dans le temps
- Comprendre les liens entre paramètres sanguins et maladies potentielles
- Générer des rapports PDF de leurs bilans
- Envoyer leurs résultats par email à leur médecin traitant

Cette application a été conçue pour aider les patients à mieux suivre et comprendre leurs analyses médicales avec une interface intuitive et des visualisations claires.

## Fonctionnalités principales

- Système d'authentification : Connexion et inscription sécurisées pour protéger les données médicales
- Saisie de bilans sanguins : Interface simple pour entrer de nouveaux résultats d'analyses
- Visualisation des données : Affichage clair des résultats avec indications de normalité
- Graphiques d'évolution : Comparaison dans le temps des différents paramètres par catégorie
- Arbre de décision médical : Visualisation des liens entre paramètres anormaux et pathologies possibles
- Génération de rapports PDF : Export des résultats dans un format professionnel
- Envoi d'emails : Partage facile des résultats avec les professionnels de santé
- Gestion de profil : Modification des informations personnelles comme l'âge et le sexe

## Installation

### Prérequis

- Python 3.8 ou supérieur
- Pip (gestionnaire de paquets Python)
- Git (optionnel, pour cloner le dépôt)

### Étapes d'installation

1. Cloner le dépôt (ou télécharger le code source)

git clone https://github.com/YASS92izer/PROJET
cd medilabpro

2. Créer et activer un environnement virtuel

Sur Windows :
python -m venv env
env\Scripts\activate

Sur macOS/Linux :
python -m venv env
source env/bin/activate

3. Installer les dépendances

pip install -r requirements.txt

4. Configuration pour l'envoi d'emails

Le fichier .env contenant les identifiants pour l'envoi d'emails est déjà configuré dans le dossier du projet.

## Lancement de l'application

Une fois l'environnement configuré, lancez l'application avec la commande :

python main.py

## Première utilisation

1. Lors du premier lancement, utilisez l'option "Inscription" pour créer un compte
2. Renseignez vos informations (nom d'utilisateur, mot de passe, âge, sexe)
3. Connectez-vous avec vos identifiants
4. Utilisez l'option "Nouveau Bilan" pour saisir vos premières données

## Structure du projet

- main.py : Point d'entrée de l'application
- connexion.py : Gestion de l'authentification
- interface.py : Interface principale de l'application
- gestionnaire.py : Logique métier pour la gestion des bilans sanguins
- saisie_donnees.py : Interface de saisie des bilans
- info.py : Visualisation des arbres de décision
- mail.py : Interface pour l'envoi d'emails
- email_module.py : Module pour la gestion technique de l'envoi d'emails
- rapport_pdf.py : Génération de rapports PDF
- ArbreBinaire.py : Structure de données pour l'arbre de décision

## Gestion des données

L'application stocke les données dans deux fichiers CSV :
- comptes.csv : Informations des utilisateurs (identifiants, âge, sexe)
- donnees.csv : Résultats des bilans sanguins

Ces fichiers sont créés automatiquement lors de la première utilisation.

Remarque : L'application est conçue pour stocker et gérer jusqu'à 3 bilans par patient simultanément. Cette limitation est intentionnelle pour garantir des performances optimales et faciliter la comparaison des données récentes.

## Note

Cette application est fournie avec toutes les configurations nécessaires pour un fonctionnement immédiat, y compris les identifiants d'email pour tester la fonctionnalité d'envoi.
