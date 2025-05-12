#Arbre binaire d'entiers.

class ArbreBinaire :


    def __init__(self, element = None, filsGauche = None, filsDroit = None) :
        self.element = element
        self.filsGauche = filsGauche
        self.filsDroit = filsDroit

    def getElement(self) :
        return self.element

    def getFilsGauche(self) :
        return self.filsGauche

    def getFilsDroit(self) :
        return self.filsDroit

    def estVide(self) :
        return self.filsGauche==None and self.filsDroit==None

    def estFeuille(self) :
        return self.element != None and self.filsGauche==None and self.filsDroit==None

    def getTaille(self) :
        taille=0
        if self is None:
            return taille
        else:
            taille=1
            if self.getFilsGauche()!= None:
                #print("taille dans fils gauche avant", taille)
                taille=taille+self.getFilsGauche().getTaille()
                #print("taille dans fils gauche après", taille)
            if self.getFilsDroit()!= None:
                #print("taille dans fils droit avant", taille)
                taille=taille+self.getFilsDroit().getTaille()
                #print("taille dans fils droit après", taille)
        return taille
       
    def getHauteur(self):
        hauteur=1
        if self is None:
            return 0
        else:
            if self.getFilsGauche() != None:
                print("hauteur dans fils gauche avant", hauteur)
                hauteur = max(hauteur, 1 + self.getFilsGauche().getHauteur())
                print("hauteur dans fils gauche après", hauteur)
            if self.getFilsDroit() != None:
                print("hauteur dans fils droit avant", hauteur)
                hauteur = max(hauteur, 1 + self.getFilsDroit().getHauteur())
                print("hauteur dans fils droit après", hauteur)
        return hauteur


    def getNbFeuilles(self) :
        if self.estFeuille()==True:
            return 1
        else:
            return self.filsDroit.getNbFeuilles() + self.filsGauche.getNbFeuilles()
               
           
    def ajouterFilsGauche(self, element) :
        pass
   
    def ajouterFilsDroit(self, element) :
        pass

    def contient(self, element) :
        return False
   
    def __str__(self):
        if self.estFeuille()==True:
            return f"({self.getElement()},{None},{None})"
        else:
            chaineg=""
            if self.getFilsGauche()!=None:
                chaineg+=f"{self.getFilsGauche()}"
                print(chaineg)
            chained=""
            if self.getFilsDroit()!=None:
                chained+=f"{self.getFilsDroit()}"
                print(chained)
            return f"({self.getElement()},{chaineg},{chained})"
   
    racine_affichee=True        
    def afficherArbre(self) :
        resultat = ""
        if self.estFeuille()==True:
            return self.element
        if ArbreBinaire.racine_affichee:
           
            resultat += f"Racine: {self.element}"
           
            ArbreBinaire.racine_affichee = False
        else:
            resultat =self.element

        if self.filsGauche != None:
            resultat += "\n   Fils Gauche -> " + str(self.filsGauche.afficherArbre()).replace("\n", "\n   ")
        if self.filsDroit != None:
            resultat += "\n   Fils Droit -> " + str(self.filsDroit.afficherArbre()).replace("\n", "\n   ")
        return resultat

       
    def supprimerFeuille(self, element) :
        pass

    def supprimerNoeud(self, element) :
        pass

    def copierArbre(self) :
        if self.estFeuille():
            return ArbreBinaire(self.element, None, None)
        else:
            return ArbreBinaire(self.element, self.filsGauche.copierArbre(), self.filsDroit.copierArbre())

    def sontEgaux(self, autreArbre):
        if self.estFeuille() or autreArbre.estFeuille():
            if self.element != autreArbre.element:
                return False
            else:
                return True
        else:
            return self.filsGauche.sontEgaux(autreArbre.filsGauche) and self.filsDroit.sontEgaux(autreArbre.filsDroit)

    def getNbOccurences(semf, element) :
        pass