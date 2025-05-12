import os
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv

# Charge les variables d’environnement depuis le fichier .env
load_dotenv()

# Récupère les informations d’identification email et serveur depuis .env
EMAIL_USER = os.getenv('EMAIL_USER')      # Adresse email de l’expéditeur
EMAIL_PASS = os.getenv('EMAIL_PASS')      # Mot de passe mais ici utilisation du code de la double authentification
SMTP_SERVER = os.getenv('SMTP_SERVER')    # Adresse du serveur SMTP (ex: smtp.gmail.com)
SMTP_PORT = int(os.getenv('SMTP_PORT')) if os.getenv('SMTP_PORT') else 587  # Port SMTP, par défaut 587

def send_email(to_email, subject, content):
    """
    Envoie un email au format HTML.
   
    :to_email= adresse email du destinataire
    :subject= sujet de l’email
    :content= contenu HTML de l’email
    """
    # Crée un objet EmailMessage
    msg = EmailMessage()
    msg['Subject'] = subject               # Définit le sujet de l’email
    msg['From'] = EMAIL_USER              # Définit l’expéditeur
    msg['To'] = to_email                  # Définit le destinataire
    msg.set_content("Votre bilan sanguin est disponible en HTML.")  # Contenu texte
    msg.add_alternative(content, subtype='html')                   # Contenu HTML

    try:
        # Initialise la connexion SMTP
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()                # Démarre le mode sécurisé TLS
            server.login(EMAIL_USER, EMAIL_PASS)  # Authentifie l’utilisateur
            server.send_message(msg)        # Envoie le message
            print(f"Email envoyé à {to_email}")
    except Exception as e:
        # Si une erreur survient, l’affiche et la relance pour être capturée en interface
        print(f"Erreur d'envoi : {e}")
        raise e