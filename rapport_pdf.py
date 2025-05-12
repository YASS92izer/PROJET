from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.units import inch
import matplotlib.pyplot as plt
import io
from datetime import datetime

class RapportPDF:
    def __init__(self, gestionnaire):
        self.gestionnaire = gestionnaire
        self.styles = getSampleStyleSheet()
        
        
        self.styles.add(ParagraphStyle(
            name='CustomBody',
            parent=self.styles['Normal'],
            fontSize=11,
            spaceAfter=12
        ))
        
        
        self.styles.add(ParagraphStyle(
            name='SectionTitle',
            parent=self.styles['Heading1'],
            fontSize=14,
            textColor=colors.HexColor("#042C54"),
            spaceAfter=16
        ))

    def generer_rapport(self, patient_data, bilan_data, filename):
        doc = SimpleDocTemplate(
            filename,
            pagesize=A4,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=72
        )

        elements = []

        # En-tête
        self.ajouter_entete(elements, patient_data)
        
        # Résumé des résultats
        self.ajouter_resume_resultats(elements, bilan_data)
        
        # Graphiques de tendance
        self.ajouter_graphiques(elements, patient_data['PatientID'])
        
        # Recommandations personnalisées
        self.ajouter_recommandations(elements, bilan_data)
        
        # Glossaire
        self.ajouter_glossaire(elements)

        # Générer le PDF
        doc.build(elements)

    def ajouter_entete(self, elements, patient_data):
        
        elements.append(Paragraph(
            "MediLabPro - Rapport d'Analyses",
            self.styles['Title']
        ))
        elements.append(Spacer(1, 20))
        
        # Date et informations patient
        date = datetime.now().strftime("%d/%m/%Y")
        info_patient = f"""
        <para align=left>
        <b>Date du rapport:</b> {date}<br/>
        <b>Patient:</b> {patient_data['Username']}<br/>
        <b>Âge:</b> {patient_data['Age']} ans<br/>
        <b>Sexe:</b> {patient_data['Sexe']}
        </para>
        """
        elements.append(Paragraph(info_patient, self.styles['CustomBody']))
        elements.append(Spacer(1, 20))

    def ajouter_resume_resultats(self, elements, bilan_data):
        elements.append(Paragraph("Résumé des Analyses", self.styles['SectionTitle']))
        
        
        data = [['Paramètre', 'Valeur', 'Référence', 'Statut']]
        
        for param, valeur in bilan_data.items():
            if param not in ['PatientID', 'Date', 'Sexe', 'Age']:
                try:
                    valeur_float = float(valeur)
                    resultat = self.gestionnaire.evaluer_valeur(valeur_float, bilan_data['Sexe'], param)
                    
                    if isinstance(resultat, dict) and 'min' in resultat and 'max' in resultat:
                        reference = f"{resultat['min']}-{resultat['max']}"
                        statut = resultat['statut']
                        
                        
                        if statut == "Trop basse":
                            statut_color = colors.blue
                        elif statut == "Trop élevée":
                            statut_color = colors.red
                        elif statut == "Proche de la limite":
                            statut_color = colors.orange
                        else:
                            statut_color = colors.green
                        
                        data.append([
                            param,
                            f"{valeur_float:.1f}",
                            reference,
                            statut
                        ])
                except (ValueError, TypeError):
                    continue

        table = Table(data, colWidths=[120, 80, 100, 100])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#042C54")),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
        ]))
        
        elements.append(table)
        elements.append(Spacer(1, 20))

    def ajouter_graphiques(self, elements, patient_id):
        elements.append(Paragraph("Évolution des Paramètres", self.styles['SectionTitle']))
        
        categories = ['hematologie', 'biochimie', 'lipides']
        for cat in categories:
            fig = self.gestionnaire.creer_graphique_comparaison(patient_id, cat)
            if fig:
                img_data = io.BytesIO()
                fig.savefig(img_data, format='png', bbox_inches='tight')
                img_data.seek(0)
                img = Image(img_data, width=400, height=300)
                elements.append(img)
                elements.append(Spacer(1, 20))
                plt.close(fig)

    def ajouter_recommandations(self, elements, bilan_data):
        elements.append(Paragraph("Recommandations Personnalisées", self.styles['SectionTitle']))
        
        recommandations = []
        for param, valeur in bilan_data.items():
            if param not in ['PatientID', 'Date', 'Sexe', 'Age']:
                try:
                    valeur_float = float(valeur)
                    resultat = self.gestionnaire.evaluer_valeur(valeur_float, bilan_data['Sexe'], param)
                    
                    if resultat['statut'] == "Trop basse":
                        if param == "Fer":
                            recommandations.append(
                                "• Augmentez votre consommation d'aliments riches en fer : "
                                "viande rouge, légumes verts, légumineuses"
                            )
                        elif param == "Hémoglobine":
                            recommandations.append(
                                "• Consultez votre médecin pour une possible supplémentation en fer"
                            )
                    elif resultat['statut'] == "Trop élevée":
                        if "Cholestérol" in param:
                            recommandations.append(
                                "• Réduisez votre consommation de graisses saturées et privilégiez "
                                "les graisses végétales (huile d'olive, avocat)"
                            )
                except (ValueError, TypeError):
                    continue
        
        # Éliminer les doublons
        recommandations = list(set(recommandations))
        
        for rec in recommandations:
            elements.append(Paragraph(rec, self.styles['CustomBody']))
        
        if not recommandations:
            elements.append(Paragraph(
                "• Vos résultats sont globalement satisfaisants. "
                "Continuez à maintenir une bonne hygiène de vie.",
                self.styles['CustomBody']
            ))
        
        elements.append(Spacer(1, 20))

    def ajouter_glossaire(self, elements):
        elements.append(Paragraph("Glossaire Médical", self.styles['SectionTitle']))
        
        glossaire = {
            "Hémoglobine": "Protéine des globules rouges qui transporte l'oxygène dans le sang",
            "Fer": "Minéral essentiel pour la production d'hémoglobine",
            "Cholestérol": "Lipide important pour la production d'hormones et la structure cellulaire",
            "Glycémie": "Taux de sucre dans le sang",
            "Créatinine": "Marqueur de la fonction rénale",
            "CRP": "Protéine qui augmente en cas d'inflammation",
            "TSH": "Hormone qui contrôle la thyroïde"
        }
        
        for terme, definition in glossaire.items():
            elements.append(Paragraph(
                f"<b>{terme}:</b> {definition}",
                self.styles['CustomBody']
            ))