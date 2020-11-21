### Alex LENCE ###

from os import listdir
from os.path import isfile, join


### Fonction de lecture des fichiers a traiter ###



#Entrée: nomfichier(nom du fichier a ouvrir), seuil (e-value maximal)
#Sortie: dico_match(gène_espèce1:[gène_espèce2_1,...,gène_espèce2_n]), dico_sp1,dico_sp2(dictionnaire du nom du gène associé à sa position)
def read_blast_evalue(nomfichier,seuil):
    dico_match={}
    dico_sp1={}
    dico_sp2={}
    fichier=open(nomfichier,"r")
    for ligne in fichier:
        if ligne[0]!="#":
            ligne=ligne.split("\n")[0]
            ligne=ligne.split("\t")
	    #On ne considère que les matchs dont la e-value est inférieur au seuil
            if float(ligne[10])<seuil:
                if ligne[0][4:] in dico_match:
                    dico_match[ligne[0][4:]].append(ligne[1])
                else:	
                    dico_match[ligne[0][4:]]=[ligne[1]]
                indice1=ligne[0].split("_")
                indice2=ligne[1].split("_")
		#Particularité d'écriture de certain gène
                if len(indice1)<4:
                        dico_sp1[ligne[0][4:]]=int(indice1[2])
                        
                else:
                    dico_sp1[ligne[0][4:]]=int(indice1[3])
                    
                if len(indice2)<4:
                    dico_sp2[ligne[1]]=int(indice2[2])
                else:
                    dico_sp2[ligne[1]]=int(indice2[3])
    fichier.close()	
    return(dico_match,dico_sp1,dico_sp2)



#Entrée: nomfichier(nom du fichier a ouvrir), seuil (e-value maximal), dico_COG(dictionnaire d'association entre un numéros COG et la fonction associé)
#Sortie: dico_pos_fon(position_du_gène:[fonction_1,...,fonction_n], on associe la position de chaque gène a sa/ses fonctions possible)
def read_Cog_evalue(nomfichier,seuil,dico_COG):
	dico_pos_fon={}
	fichier=open(nomfichier,"r")
	for ligne in fichier:
		if ligne[0:2]=="Q#":
			ligne=ligne[:-1]
			ligne=ligne.split("\t")
			#On ne considère que les gènes dont la e-value est inférieur pour une fonction donnée
			if ligne[5]<seuil:
				pos=ligne[0].split(" ")
				pos=pos[2].split("_")[-1]
				cog=ligne[7]
				if cog in dico_COG:
					if pos in dico_pos_fon:
						dico_pos_fon[pos].append(cog)
					else:
						dico_pos_fon[pos]=[cog]
	fichier.close()
	return(dico_pos_fon)


#Entrée: nomfichier(nom du fichier a ouvrir), seuil (valeur minimal d'identité)
#Sortie: dico_match(gène_espèce1:[gène_espèce2_1,...,gène_espèce2_n]), dico_sp1,dico_sp2(dictionnaire du nom du gène associé à sa position)
def read_blast_id(nomfichier,seuil):
	dico_match={}
	dico_sp1={}
	dico_sp2={}
	fichier=open(nomfichier,"r")
	for ligne in fichier:
		if ligne[0]!="#":
			ligne=ligne[:-1]
			ligne=ligne.split("\t")
			#On ne considère que des matchs pour lesquels l'identité est supérieur à la valeur seuil
			if float(ligne[2])>seuil:
				if ligne[0][4:] in dico_match:
					dico_match[ligne[0][4:]].append(ligne[1])
				else:
					dico_match[ligne[0][4:]]=[ligne[1]]
				indice1=ligne[0].split("_")
				indice2=ligne[1].split("_")
				if len(indice1)<4:#Particularité d'écriture de certain gène
					dico_sp1[ligne[0][4:]]=int(indice1[2])
				else:
					dico_sp1[ligne[0][4:]]=int(indice1[3])
				if len(indice2)<4:
					dico_sp2[ligne[1]]=int(indice2[2])
				else:
					dico_sp2[ligne[1]]=int(indice2[3])
	fichier.close()
	return(dico_match,dico_sp1,dico_sp2)



#Entrée: start,end(position du premier et du dernier aa du match), longueur(longueur du gène)
#Sortie: Couverture
def calcule_hit(start,end,longueur):
	couverture=(end-start)/longueur
	return(couverture)
#Entrée: nomfichier(nom du fichier à ouvrire), seuil(recouvrement minimal considéré)
#Sortie: pos(liste de liste des positions des gènes qui match), nuance(liste du recouvrement moyen pour le gène query et le gène s)
#	 maxi(minimum et maximum de recouvrement)
def read_blast_hit(nomfichier,seuil):
	pos=[]
	nuance=[]
	maxi=0
	fichier=open(nomfichier,"r")
	for ligne in fichier:
		if ligne[0]!="#":
			ligne=ligne[:-1]
			ligne=ligne.split("\t")
			qcouvertur=calcule_hit(int(ligne[6]),int(ligne[7]),int(ligne[3]))
			scouvertur=calcule_hit(int(ligne[8]),int(ligne[9]),int(ligne[3]))
			#Calcule du recouvrement moyen des 2 gènes si il est supérieur au seuil on le sauvegarde
			if (((qcouvertur+scouvertur)/2)*100)>seuil:
				pos.append([ligne[0][4:],ligne[1]])
				nuance.append(1-(qcouvertur+scouvertur)/2)#1-recouvrement permet ensuite d'afficher en noir les recouvrement
                                                                          #maximum (0:noire, 1:blanc sur un plot)
				#Sauvegarde de la nuance maximal pour la mise à l'echelle ensuite				
				if nuance[-1]>maxi:
					maxi=nuance[-1]
			
	fichier.close()
	return(pos,nuance,maxi)



#Entrée: nomfichier(nom du fichier à ouvrire), dico_COG(dictionnaire d'association entre un numéros COG et la fonction associé)
#Sortie: dico_pos_fon(dictionnaire d'association entre la position d'un gène et son numéros COG)
def read_Cog_fonction(nomfichier,dico_COG):
	dico_pos_fon={}
	fichier=open(nomfichier,"r")
	for ligne in fichier:
		if ligne[0:2]=="Q#":
			ligne=ligne[:-1]
			ligne=ligne.split("\t")
			pos=ligne[0].split(" ")
			pos=pos[2].split("_")[-1]
			cog=ligne[7]
			if cog in dico_COG:
				if pos in dico_pos_fon:
					dico_pos_fon[pos].append(cog)
				else:
					dico_pos_fon[pos]=[cog]
	fichier.close()
	return(dico_pos_fon)


##### Lecture de dossier et de fichier pour faciliter et compléter la lecture des fichiers principaux #####

#Entrée: nomfichier(nom du fichier à ouvrire)
#Sortie: dico_COG(dictionnaire d'association entre un numéros COG et la fonction associé)
def make_dico_cog(nomfichier):
	dico={}
	ligne=""
	with open(nomfichier, encoding="utf8", errors='ignore') as fichier: #Utilisation du a une erreur de lecture 
    		contenu = fichier.read()
	for c in contenu:
		ligne+=c
		if c=="\n":
			cle=ligne[:7]
			ligne=ligne[8:].split("\t")
			fonc=ligne[0]
			dico[cle]=fonc
			ligne=""
	fichier.close()
	return(dico)


#Entrée: nomfichier(nom du fichier à ouvrire)
#Sortie: dico_couleur(dictionnaire d'association d'une fonction à sa couleur pour le plot)
def make_dico_couleur(nomfichier):
	dico_couleur={}
	fichier=open(nomfichier,'r')
	for ligne in fichier:
		if ligne[0]!="#":
			rgb=[]#liste des couleurs R(intensité du rouge),G(intensité du vert) et B(intensité du bleu)
			cle=ligne[0]
			ligne=ligne[:-1].split("\t")
			for i in ligne[1:]:
				rgb.append(float(i))
			dico_couleur[cle]=rgb
	fichier.close()
	return(dico_couleur)

#Entrée: nomfichier(nom du fichier à ouvrire)
#Sortie: dico(dictionnaire d'association entre la fonction et sa lettre diminutive), liste_fonction(liste de l'ensemble des fonction)
def make_dico_fonction(nomfichier):
	dico={}
	liste_fonction=["ALL"]
	fichier=open(nomfichier,'r')
	for ligne in fichier:
		if ligne[0]!="#":
			cle=ligne[0]
			valeur=ligne[:-1].split("\t")[-1]
			dico[cle]=valeur
			liste_fonction.append(cle)
	fichier.close()
	return(dico,liste_fonction)

#Entrée: GCA(nom GCA des organisme)
#Sortie: Nom véritable de l'organisme
def read_nom_organisme(GCA):
	fichier=open("Fichier_Lecture/prokaryotes_complete-genomes.csv","r")
	for ligne in fichier:
		ligne=ligne.split(",")
		if ligne[5][1:-1]==GCA:
			return(ligne[0][1:-1])

#Entrée: nom_dossier(nom d'un dossier contenant les fichier d'un blast)
#Sortie: dico_fichier(dictionnaire d'association entre le nom veritéable du fichier et son nom GCA)
#        liste_fichier(liste du nom véritable dufichier)
#Particularité: Dans un dossier Blast deux organismes par fichier
def f_liste_fichier(nom_dossier):
	dossier = [f for f in listdir(nom_dossier) if isfile(join(nom_dossier,f))]
	dico_fichier={}
	liste_fichier=[]
	for f in range(len(dossier)):
			GCA1=dossier[f][6:21]
			t=dossier[f].split("GCA")[-1]
			GCA2="GCA_"+(t.split("_")[1])
			nomx=read_nom_organisme(GCA1)
			nomy=read_nom_organisme(GCA2)
			nomfichier=nomx+" VS "+nomy
			liste_fichier.append(nomfichier)
			dico_fichier[nomfichier]=dossier[f]
	return(dico_fichier,liste_fichier)

#Entrée: nom_dossier(nom d'un dossier contenant les fichier d'un blast)
#Sortie: dico_fichier(dictionnaire d'association entre le nom veritéable du fichier et son nom GCA)
#        liste_fichier(liste du nom véritable dufichier)
#Particularité: Dans un dossier COG un seul organisme par fichier
def f_liste_fichier_cog(nom_dossier):
	dossier = [f for f in listdir(nom_dossier) if isfile(join(nom_dossier,f))]
	dico_fichier={}
	liste_fichier=[]
	for f in range(len(dossier)):
		GCA1=dossier[f][6:21]
		nom=read_nom_organisme(GCA1)
		nomfichier=nom
		liste_fichier.append(nomfichier)
		dico_fichier[nomfichier]=dossier[f]
	return(dico_fichier,liste_fichier)


#Entrée: nom_dossier(nom du dossier)
#Sorite: Dit si le fichier ouvert est un COG ou un Blast permet de séléctionner les bonnes fonctions dans le cas d'une e-value
def f_cog_blast(nom_dossier):
	dossier = [f for f in listdir(nom_dossier) if isfile(join(nom_dossier,f))]
	verification=dossier[0].split("GCA")
	if len(verification)==3:
		return("blast")
	else:
		return("cog")

### Fichier d'écriture des gènes appartenant à des blocs de synthénie ###
#Entrée: titre(sert de nom de sauvegarde du fichier),nomx,nomy(nom des organismes)
#        liste_sp1,liste_sp2(liste de listes des blocs de synthénie en x et en y)
#Sortie: Fichier text dans le quel on retrouve les blocs de synthénie
def write_bloc_syn(titre,nomx,nomy,liste_sp1,liste_sp2):
    titre+=".txt"
    fichier=open(titre,'w')
    fichier.write("#nom_organisme	numeros_de_bloc		position_des_gènes")	
    nom_sp1=">"+nomx+"\t"
    nom_sp2=">"+nomy+"\t"
    fichier.write("\n\n")
    for i in range(len(liste_sp1)):
        blocx="bloc:"+str(i)+"\t"
        blocy="bloc:"+str(i)+"\t"
        fichier.write(nom_sp1)
        fichier.write(blocx)
        for j in range(len(liste_sp1[i])):
            fichier.write(str(liste_sp1[i][j]))
            fichier.write(" ")
        fichier.write("\n")
        fichier.write(nom_sp2)
        fichier.write(blocy)
        for j in range(len(liste_sp2[i])):
            fichier.write(str(liste_sp2[i][j]))
            fichier.write(" ")
        fichier.write("\n\n")
    fichier.close()



#Entrée: titre(sert de nom de sauvegarde du fichier),nomx,nomy(nom des organismes)
#        liste_sp1,liste_sp2(liste de listes des blocs de synthénie en x et en y)
#        dico1,dico2(dictionnaire d'association de la position d'un gène avec son numéros COG)
#        dico_fonction(dictionnaire d'association de la lettre à sa fonction)
#        dico_COG(dictionnaire d'association d'un numéros COG à une lettre abréviative d'une fonction)
#Sortie: Fichier text dans le quel on retrouve les blocs de synthénie ainsi que les fonctions possible de chaque gène
def write_bloc_syn_fonction(titre,nomx,nomy,liste_sp1,liste_sp2,dico1,dico2,dico_fonction,dico_COG):
    titre+=".txt"
    fichier=open(titre,"w")
    fichier.write("#nom_organisme	numeros_de_bloc		position_des_gènes:Fonction_des_gènes")	
    nom_sp1=">"+nomx+"\t"
    nom_sp2=">"+nomy+"\t"	
    fichier.write("\n\n")
    for i in range(len(liste_sp1)):
        blocx="bloc:"+str(i)+"\t"
        blocy="bloc:"+str(i)+"\t"
        fichier.write(nom_sp1)
        fichier.write(blocx)
        for j in range(len(liste_sp1[i])):
            pos=str(liste_sp1[i][j])
            fichier.write(pos)
            fichier.write(":")
            for k in dico1[pos]:
                for l in dico_COG[k]:
                    fichier.write(dico_fonction[l])
                    fichier.write(",")
            fichier.write(" ")
        fichier.write("\n")
        fichier.write(nom_sp2)
        fichier.write(blocy)
        for j in range(len(liste_sp2[i])):
            pos=str(liste_sp2[i][j])
            fichier.write(pos)
            fichier.write(":")
            for k in dico2[pos]:
                for l in dico_COG[k]:
                    fichier.write(dico_fonction[l])
                    fichier.write(",")
        fichier.write("\n\n")
    fichier.close()


