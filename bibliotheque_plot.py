### Alex Lence ###

import matplotlib.pyplot as plt
import bibliotheque_read as br

###Fonction de tracage de Bloc de Synthenie###

#Entrée 2 listes de points de match entre une espèce1 et une espèce2
#Sortie 2 dico pour les bloc dico_c:"croissant" et dico_d:"décroissant"
def bloc_syn(liste_sp1,liste_sp2):
	dico_c={}#Dictionnaire de bloc "croissant"
	dico_d={}#Dictionnaire de bloc "décroissant"
	for i in range(len(liste_sp1)):
		cle_c=liste_sp1[i]-liste_sp2[i]#Un bloc aligné "croissant" est un bloc pour le quel x-y=cst
		cle_d=liste_sp2[i]+liste_sp1[i]#Un bloc aligné "croissant" est un bloc pour le quel y+x=cst
		if cle_c in dico_c:
			if not (liste_sp1[i],liste_sp2[i]) in dico_c[cle_c]:#On ne compte pas en double les couples de valeurs
				dico_c[cle_c].append((liste_sp1[i],liste_sp2[i]))
		else:
			dico_c[cle_c]=[(liste_sp1[i],liste_sp2[i])]
		if cle_d in dico_d:
			if not (liste_sp1[i],liste_sp2[i]) in dico_d[cle_d]:#On ne compte pas en double les couples de valeurs
				dico_d[cle_d].append((liste_sp1[i],liste_sp2[i]))
		else:
			dico_d[cle_d]=[(liste_sp1[i],liste_sp2[i])]
	return(dico_c,dico_d)

#Entrée dictionnaire de bloc de synthénie, et la taille minimum pour que ce bloc soit considéré
#Sortie une liste de bloc de synthénie avec une taille supérieur au seuil fixé par l'utilisateur
def verif_taille_min_syn(dico,taille_min_syn):
	liste_bloc=[]	
	for i in dico:
		if len(dico[i])>taille_min_syn:#Si la taille du bloc est supérieur au seuil alors on le garde
			liste_bloc.append(dico[i])
	return (liste_bloc)

#Entrée une liste de bloc avec une taille convenable, le seuil de taille du bloc et la distance max entre 2 gènes au sein d'un bloc
#Sortie la liste des bloc finaux a considérer
def verification_bloc(liste_bloc_syn,taille_min_syn,seuil):
	liste_bloc=[]#Liste final des blocs à considérer
	for l in liste_bloc_syn:#Pour tous les blocs on va vérifié la distance entre chaque gène
		liste=[]
		prece=l[0][0]
		for i in l:#Pour chaque gène dans un bloc on va vérifié sa distance avec le gène précédent
			if not i[0]>(prece+seuil):#Si la distance entre deux gènes n'est pas supérieur au seuil
                                                  #alors on incrémente la liste de ce bloc				
				liste.append(i)
			else:                     #Si la distance est supérieure alors on crée un nouveau bloc
                                                  #Et on remplit la liste des blocs
				liste_bloc.append(liste)
				liste=[i]
			prece=i[0]
		liste_bloc.append(liste)
	
	i=0
	#On verifie que chaque bloc dans la liste des blocs a bien une taille convenable sinon on suprime le bloc
	while i!=len(liste_bloc):
		if len(liste_bloc[i])<taille_min_syn:
			del liste_bloc[i]
		else:
			i+=1
	return(liste_bloc)




			
#Entrée: titre du graphique(qui sert de titre au fichier de sauvegarde),nomx,nomy,liste_sp1,liste_sp2(point qui match entre les 2 espèces)
#	 taille_min_syn(taille minimal d'un bloc de synthénie pour être considéré),seuil(distance max entre deux gènes d'un même bloc)	#	 affichage(option d'affichage des blocs de synthénie),save(option de sauvegarde des blocs de synthénie)
#Sortie: Affichage sur le graphique des blocs de synthnie
def synthenie(titre,nomx,nomy,liste_sp1,liste_sp2,taille_min_syn,seuil,affichage,save):	

	dico_c,dico_d=bloc_syn(liste_sp1,liste_sp2)
	liste_bloc_syn_c=verif_taille_min_syn(dico_c,taille_min_syn)
	liste_bloc_syn_d=verif_taille_min_syn(dico_d,taille_min_syn)

	liste_bloc_c=verification_bloc(liste_bloc_syn_c,taille_min_syn,seuil)
	liste_bloc_d=verification_bloc(liste_bloc_syn_d,taille_min_syn,seuil)
	
	listex=[]
	listey=[]

	listex1=[]
	listex2=[]
	listey1=[]
	listey2=[]	
	#on récupère tous les x et les y de chaque bloc qu'on stock dans une liste de liste
	for l in liste_bloc_c:
		listexi=[]
		listeyi=[]
		for i in l:
			listexi.append(i[0])
			listeyi.append(i[1])
		listex.append(listexi)
		listey.append(listeyi)

	for l in liste_bloc_d:
		listexi=[]
		listeyi=[]
		for i in l:
			listexi.append(i[0])
			listeyi.append(i[1])
		listex.append(listexi)
		listey.append(listeyi)
	
	#Option de sauvegarde si la case est coché alors save=1 et la fonction sauvegarde tous les blocs
	if save==1:
		br.write_bloc_syn(titre,nomx,nomy,listex,listey)

	#On crée la liste des premier x,y et des dernier x,y de chaque bloc pour les plot ensuite
	for i in range(len(listex)):
		listex1.append(listex[i][0])
		listex2.append(listex[i][-1])
		listey1.append(listey[i][0])
		listey2.append(listey[i][-1])
	
	#On affiche ou pas les blocs de synthénie obtenue
	if affichage==1:
		plt.plot([listex1,listex2],[listey1,listey2],color="red",lw=2)#[x1,x2],[y1,y2]

#Entrée: titre du graphique(qui sert de titre au fichier de sauvegarde),nomx,nomy,liste_sp1,liste_sp2(point qui match entre les 2 espèces)
#	 taille_min_syn(taille minimal d'un bloc de synthénie pour être considéré),seuil(distance max entre deux gènes d'un même bloc)	#	 affichage(option d'affichage des blocs de synthénie),save(option de sauvegarde des blocs de synthénie)
#Sortie: Affichage sur le graphique des blocs de synthnie
def synthenie_fonction(titre,nomx,nomy,liste_sp1,liste_sp2,taille_min_syn,seuil,affichage,save,dico1,dico2,dico_fonction,dico_COG):	

	dico_c,dico_d=bloc_syn(liste_sp1,liste_sp2)
	liste_bloc_syn_c=verif_taille_min_syn(dico_c,taille_min_syn)
	liste_bloc_syn_d=verif_taille_min_syn(dico_d,taille_min_syn)

	liste_bloc_c=verification_bloc(liste_bloc_syn_c,taille_min_syn,seuil)
	liste_bloc_d=verification_bloc(liste_bloc_syn_d,taille_min_syn,seuil)
	
	listex=[]
	listey=[]

	listex1=[]
	listex2=[]
	listey1=[]
	listey2=[]	
	#on récupère tous les x et les y de chaque bloc qu'on stock dans une liste de liste
	for l in liste_bloc_c:
		listexi=[]
		listeyi=[]
		for i in l:
			listexi.append(i[0])
			listeyi.append(i[1])
		listex.append(listexi)
		listey.append(listeyi)

	for l in liste_bloc_d:
		listexi=[]
		listeyi=[]
		for i in l:
			listexi.append(i[0])
			listeyi.append(i[1])
		listex.append(listexi)
		listey.append(listeyi)
	
	#Option de sauvegarde si la case est coché alors save=1 et la fonction sauvegarde tous les blocs
	if save==1:
		br.write_bloc_syn_fonction(titre,nomx,nomy,listex,listey,dico1,dico2,dico_fonction,dico_COG)

	#On crée la liste des premier x,y et des dernier x,y de chaque bloc pour les plot ensuite
	for i in range(len(listex)):
		listex1.append(listex[i][0])
		listex2.append(listex[i][-1])
		listey1.append(listey[i][0])
		listey2.append(listey[i][-1])
	
	#On affiche ou pas les blocs de synthénie obtenue
	if affichage==1:
		plt.plot([listex1,listex2],[listey1,listey2],color="red",lw=2)#[x1,x2],[y1,y2]




##### Fonction De Plot #####


#Entrée: dico_match(quel gène de l'espèce1 match avec quel gène de l'espèce2), dico1,dico2 (la position de chaque gène)
#        taille_min_syn(taille minimal d'un bloc de synthénie),seuil(distance maximal entre 2 gènes d'un même bloc de synthénie)
#        titre(titre du graphique et du fichier de sauvegarde),nomx,nomy(noms des organismes)
#        affichage(option d'affichage),save(option de sauvegarde du plot)
#Sortie: Affichage du plot en fonction des paramètres définies
def dotplot_blast(dico_match,dico1,dico2,taille_min_syn,seuil,titre,nomx,nomy,affichage,save):
    liste_sp1=[]#Liste des coordonnées x des points de match
    liste_sp2=[]#Liste des coordonnées y des points de match
    for i in dico_match:
        for j in dico_match[i]:
            liste_sp1.append(dico1[i])
            liste_sp2.append(dico2[j])

    #Definition de la figure
    plt.figure()
    plt.scatter(liste_sp1,liste_sp2,c="black",s=3)#(listex,listey,couleur,taille des point)
    if affichage!=0 or save!=0:#Si on ne veut ni afficher ni sauvegarder les blocs de synthénie pas besoin de lancer la fonction
    	synthenie(titre,nomx,nomy,liste_sp1,liste_sp2,taille_min_syn,seuil,affichage,save)
    plt.title(titre)
    plt.xlabel(nomx)
    plt.ylabel(nomy)
    plt.show()#Affichage du plot avec ou non les blocs de synthénie tracer dans la fonction synthenie



#Entrée: dico1,dico2(dictionnaire de chaque espèce pour la/les fonction(s) de chaque gènes
#        taille_min_syn(taille minimal d'un bloc de synthénie),seuil(distance maximal entre 2 gènes d'un même bloc de synthénie)
#        titre(titre du graphique et du fichier de sauvegarde),nomx,nomy(noms des organismes)
#        affichage(option d'affichage),save(option de sauvegarde du plot)
#Sortie: Affichage du plot en fonction des paramètres définies
def dotplot_cog(dico1,dico2,dico_COG,dico_fonction,taille_min_syn,seuil,titre,nomx,nomy,affichage,save):
	listex=[]
	listey=[]
	#On parcourt chaque gène de l'espèce1	
	for pos1 in dico1:
		#On parcourt chaque fonction de chaque gène de l'espèce1
		for fonc1 in dico1[pos1]:
			#On parcourt chaque gène de l'espèce2
			for pos2 in dico2:
				#On parcourt chaque fonction de chaque gène de l'espèce2
				for fonc2 in dico2[pos2]:
					#Si au moins une fonction est similaire alors on considère que les 2 gènes match
					if fonc1==fonc2:
					#if fonc1==fonc_voulu and fonc2==fonc_voulu (Dans Le cas de la visualisation d'une certaine fonction) 
						listex.append(int(pos1))
						listey.append(int(pos2))
	plt.figure()
	plt.scatter(listex,listey,c="black",s=3)
	if affichage!=0 or save!=0:
		synthenie_fonction(titre,nomx,nomy,listex,listey,taille_min_syn,seuil,affichage,save,dico1,dico2,dico_fonction,dico_COG)
	plt.title(titre)
	plt.xlabel(nomx)
	plt.ylabel(nomy)
	plt.show()


#Ajoute la legende au graphique fonction
def legend_fonction(dico_couleur):
	Y=0
	liste_lettre=[]
	liste_symbole=[]
	for lettre in dico_couleur:
		liste_symbole.append(plt.scatter(0,0+Y,color=dico_couleur[lettre],marker='o',s=2))
		liste_lettre.append(lettre)
		Y+=0.5
	plt.legend(liste_symbole,liste_lettre,markerscale=1,frameon=True,fontsize=6)
	


#Entrée: dico1,dico2(dictionnaire de chaque espèce pour la/les fonction(s) de chaque gènes
#        dico_COG(dictionnaire de correspondance entre le COG et le code des fonctions) dico_couleur(dictionnaire des code de fonction et des
#        couleur associé)
#        taille_min_syn(taille minimal d'un bloc de synthénie),seuil(distance maximal entre 2 gènes d'un même bloc de synthénie)
#        titre(titre du graphique et du fichier de sauvegarde),nomx,nomy(noms des organismes)
#        affichage(option d'affichage),save(option de sauvegarde du plot)
#Sortie: Affichage du plot en fonction des paramètres définies
def dotplot_fon(dico1,dico2,dico_COG,dico_couleur,dico_fonction,taille_min_syn,seuil,titre,nomx,nomy,affichage,save):
	listex=[]
	listey=[]
	listec=[]
	#On parcourt chaque gène de l'espèce1	
	for pos1 in dico1:
		#On parcourt chaque fonction de chaque gène de l'espèce1
		for fonc1 in dico1[pos1]:
			#On parcourt chaque gène de l'espèce2
			for pos2 in dico2:
				#On parcourt chaque fonction de chaque gène de l'espèce2
				for fonc2 in dico2[pos2]:
					#Si au moins une fonction est similaire alors on considère que les 2 gènes match
					if fonc1==fonc2:
					#if fonc1==fonc_voulu and fonc2==fonc_voulu (Dans Le cas de la visualisation d'une certaine fonction) 
						listex.append(int(pos1))
						listey.append(int(pos2))
						#Dans le cas ou il peut y avoir plusieurs fonctions on fait la moyenne des couleursdesfonctions
						if len(dico_COG[fonc1])>1:
							r,g,b=0,0,0
							for lettre in dico_COG[fonc1]:
								r+=dico_couleur[lettre][0]
								g+=dico_couleur[lettre][1]
								b+=dico_couleur[lettre][2]
							r=r/len(dico_COG[fonc1])
							g=g/len(dico_COG[fonc1])
							b=b/len(dico_COG[fonc1])
							listec.append([r,g,b])
						else:
							listec.append(dico_couleur[dico_COG[fonc1]])
	plt.figure()
	plt.scatter(listex,listey,c=listec,s=3)
	if affichage!=0 or save!=0:
		synthenie_fonction(titre,nomx,nomy,listex,listey,taille_min_syn,seuil,affichage,save,dico1,dico2,dico_fonction,dico_COG)

	#Permet de placer la légend sur le dotplot
	legend_fonction(dico_couleur)
	
	plt.title(titre)
	plt.xlabel(nomx)
	plt.ylabel(nomy)
	plt.show()

#Entrée: pos(liste des gènes qui match entre eux),nuance(degré de noir pour chaque couple),varnuance(option d'affichage de nuance)
#        taille_min_syn(taille minimal d'un bloc de synthénie),seuil(distance maximal entre 2 gènes d'un même bloc de synthénie)
#        maxi(nuance maximal)
#        titre(titre du graphique et du fichier de sauvegarde),nomx,nomy(noms des organismes)
#        affichage(option d'affichage),save(option de sauvegarde du plot)
#Sortie: Affichage du plot en fonction des paramètres définies
def dotplot_hit(pos,nuance,varnuance,taille_min_syn,seuil,maxi,titre,nomx,nomy,affichage,save):

	#facteur de mise à l'echelle (le max/max=1 et tout autre chose sera inférieur a 1 donc moins noire sur le graphe)
	FaNo=1/maxi

	liste_sp1=[]#liste des coordonées en x des gènes de l'espèce1
	liste_sp2=[]#liste des coordonées en y des gènes de l'espèce2

	norma_nuance=[]#Liste des nuances mise à l'échelle

	for i in pos:
		sp1=i[0].split("_")#Récupération de la position du gène de l'espèce1
		sp2=i[1].split("_")#Récupération de la position du gène de l'espèce2
		if len(sp1)<4:#Dépend de la facon dont est noté le gène
			liste_sp1.append(int(sp1[2]))
		else:
			liste_sp1.append(int(sp1[3]))
		if len(sp2)<4:
			liste_sp2.append(int(sp2[2]))
		else:
			liste_sp2.append(int(sp2[3]))
	#Mise à l'echelle de la nuance	
	for i in nuance:
		norma_nuance.append(str(i*FaNo))
	
	plt.figure()
	#Affichage des nuances de noire en fonction du recouvrement
	if varnuance==1:
		plt.scatter(liste_sp1,liste_sp2,color=norma_nuance,s=3)
	else:
		plt.scatter(liste_sp1,liste_sp2,color="black",s=3)
	#Affichage et ou sauvegarde des blocs de synthénies
	if affichage!=0 or save!=0:
    		synthenie(titre,nomx,nomy,liste_sp1,liste_sp2,taille_min_syn,seuil,affichage,save)
	plt.title(titre)
	plt.xlabel(nomx)
	plt.ylabel(nomy)
	plt.show()
		
