### Alex LENCE ###


from tkinter import *
from tkinter import ttk
import bibliotheque_read as br
import bibliotheque_plot as bp
import re, os, webbrowser

### Fenetre E-value ###
class Fenetre_blast:
	def __init__(self,dossier,test):

		self._test=test
		# Crée la fenêtre
		self._fenetre_blast = Tk()
		if self._test=="e_value":
			self._fenetre_blast.title("Paramètre E-value")
		elif self._test=="identite":
			self._fenetre_blast.title("Paramètre Identité")
		elif self._test=="recouvrement":
			self._fenetre_blast.title("Paramètre Recouvrement")
		self._fenetre_blast.geometry("1250x250")
	
		#Crée un bouton retour
		self._B_retour=Button(self._fenetre_blast,text="<--",width=1,command=self.f_retour)
		self._B_retour.place(x=1,y=1)

		#Crée une Combobox de choix de fichier
		self._nomdossier=dossier
		self._dico_fichier,liste_fichier=br.f_liste_fichier(self._nomdossier)#Récupération nom des organismes de chaque fichiers
		self._lcomboboxchoix=Label(self._fenetre_blast,text="Organismes")
		self._fichier=ttk.Combobox(self._fenetre_blast,values=(liste_fichier),width=60)
		self._fichier.current(0)
		self._lcomboboxchoix.pack(side=TOP)
		self._fichier.pack(side=TOP)

		


		#Crée les entrées pour modifier les paramètres
		if self._test=="e_value":
			self.Lparam=Label(self._fenetre_blast,text="Valeur e-value maximale (1e-50)")
		elif self._test=="identite":
			self.Lparam=Label(self._fenetre_blast,text="Pourcentage d'identité minimal")
		elif self._test=="recouvrement":
			self.Lparam=Label(self._fenetre_blast,text="Pourcentage de recouvrement minimal")
		self._param=Entry(self._fenetre_blast)

		self.distance_syn=Label(self._fenetre_blast,text="Distance max entre 2 gènes d'un même bloc de synténie")
		self._d_syn=Entry(self._fenetre_blast)

		self.taille_syn=Label(self._fenetre_blast,text="Taille minimale pour un bloc de synténie")
		self._t_syn=Entry(self._fenetre_blast)

		#Crée un checkbouton
		self._affichage=IntVar()
		self._save=IntVar()
		self._Check1=Checkbutton(self._fenetre_blast,text="Afficher les blocs de synthénie",variable=self._affichage)
		self._Check2=Checkbutton(self._fenetre_blast,text="Sauvegarder les blocs de synthénie",variable=self._save)
		if self._test=="recouvrement":
			self._varnuance=IntVar()
			self._Check3=Checkbutton(self._fenetre_blast,text="Nuance",variable=self._varnuance)
			self._Check3.place(x=950,y=210)
			
		

		
		#Place les Entrées dans les cadres
		self.Lparam.place(x=10,y=70)
		self._param.place(x=390,y=70)
		self.distance_syn.place(x=10,y=100)
		self._d_syn.place(x=390,y=100)
		self.taille_syn.place(x=10,y=130)
		self._t_syn.place(x=390,y=130)

		#Place les checkbuttons
		self._Check1.place(x=950,y=170)
		self._Check2.place(x=950,y=190)

	

		#Crée un bouton qui trace le dotplot
		self._Confirme=Button(self._fenetre_blast,text="Confirmer",command=self.trace)
		self._Confirme.pack(side=BOTTOM)

	#Fonction de tracage du dotplot	
	def trace(self):
		nomfichier=self._nomdossier+self._dico_fichier[self._fichier.get()]#Récupération du nom du fichier
		param=float(self._param.get())
		nespece=self._fichier.get()		
		espece=nespece.split("VS")
		nomx=espece[0]
		nomy=espece[1]
		
		if self._test=="e_value" or self._test=="identite":
			if self._test=="e_value":
				dico_match,dico_sp1,dico_sp2=br.read_blast_evalue(nomfichier,param)
				titre="Dotplot pour une e-value maximum de "+str(param)+" "+nespece
			elif self._test=="identite":
				dico_match,dico_sp1,dico_sp2=br.read_blast_id(nomfichier,param)
				titre="Dotplot pour un poucentage d'identité supérieur a "+str(param)+"% "+nespece
			bp.dotplot_blast(dico_match,dico_sp1,dico_sp2,int(self._t_syn.get()),int(self._d_syn.get()),titre,nomx,nomy,self._affichage.get(),self._save.get())
		elif self._test=="recouvrement":
			titre="Dotplot pour un poucentage de recouvrement supérieur a "+str(param)+"% "+nespece
			pos,nuance,maxi=br.read_blast_hit(nomfichier,param)
			bp.dotplot_hit(pos,nuance,int(self._varnuance.get()),int(self._t_syn.get()),int(self._d_syn.get()),maxi,titre,nomx,nomy,self._affichage.get(),self._save.get())
		

	def f_retour(self):
		self._fenetre_blast.destroy()
		lancement=Fenetre_une()
		lancement.main()
		
	
	def main(self):
		
		self._fenetre_blast.mainloop()

### Fenetre evalue pour un fichier cog ###
class Fenetre_cog:
	def __init__(self,dossier,test):

		self._test=test
		# Crée la fenêtre
		self._fenetre_cog = Tk()
		if self._test=="e_value":
			self._fenetre_cog.title("Paramètre E-value")
		elif self._test=="fonction":
			self._fenetre_cog.title("Paramètre Fonction")
		self._fenetre_cog.geometry("1250x250")


		#Crée un bouton retour
		self._B_retour=Button(self._fenetre_cog,text="<--",width=1,command=self.f_retour)
		self._B_retour.place(x=1,y=1)

		#Crée une spinbox de choix de fichier
		self._nomdossier=dossier
		self._dico_fichier,liste_fichier=br.f_liste_fichier_cog(self._nomdossier)#Récupération nom des organismes de chaque fichiers


		self._lcomboboxchoix1=Label(self._fenetre_cog,text="Organismes1")
		self._fichier1=ttk.Combobox(self._fenetre_cog,values=(liste_fichier),width=60)
		self._fichier1.current(0)

		self._lcomboboxchoix2=Label(self._fenetre_cog,text="Organismes2")
		self._fichier2=ttk.Combobox(self._fenetre_cog,values=(liste_fichier),width=60)
		self._fichier2.current(1)

		self._fichier1.pack(side=TOP)
		self._fichier2.pack(side=TOP)

		self._dico_COG=br.make_dico_cog("Fichier_Lecture/cognames2003-2014.tab.txt")
		self._dico_fonction,liste_fonction=br.make_dico_fonction("Fichier_Lecture/fun2003-2014.tab.txt")
		#Crée les entrées pour modifier les paramètres
		if self._test=="e_value":
			self.Lparam=Label(self._fenetre_cog,text="Valeur e-value maximale (1e-50)")
			self._param=Entry(self._fenetre_cog)
		elif self._test=="fonction":
			
			self._dico_couleur=br.make_dico_couleur("Fichier_Lecture/couleur.txt")
			
		

		self.distance_syn=Label(self._fenetre_cog,text="Distance max entre 2 gènes d'un même bloc de synténie")
		self._d_syn=Entry(self._fenetre_cog)

		self.taille_syn=Label(self._fenetre_cog,text="Taille minimale pour un bloc de synténie")
		self._t_syn=Entry(self._fenetre_cog)

		#Crée un checkbouton
		self._affichage=IntVar()
		self._save=IntVar()
		self._Check1=Checkbutton(self._fenetre_cog,text="Afficher les bloc de synthénie",variable=self._affichage)
		self._Check2=Checkbutton(self._fenetre_cog,text="Sauvegarder les blocs de synthénie",variable=self._save)

		
		#Place les Entrées dans les cadres
		if test=="e_value":
			self.Lparam.place(x=10,y=70)
			self._param.place(x=390,y=70)
		self.distance_syn.place(x=10,y=100)
		self._d_syn.place(x=390,y=100)
		self.taille_syn.place(x=10,y=130)
		self._t_syn.place(x=390,y=130)

		#Place les checkbuttons
		self._Check1.place(x=950,y=170)
		self._Check2.place(x=950,y=190)

	

		#Crée un bouton qui trace le dotplot
		self._Confirme=Button(self._fenetre_cog,text="Confirmer",command=self.trace)
		self._Confirme.pack(side=BOTTOM)

	#Fonction de tracage du dotplot	
	def trace(self):
		nomfichier1=self._nomdossier+self._dico_fichier[self._fichier1.get()]#Récupération du nom du fichier
		nomfichier2=self._nomdossier+self._dico_fichier[self._fichier2.get()]
		espece1=self._fichier1.get()
		espece2=self._fichier2.get()
		
		
		if self._test=="e_value":
			dico_pos_fon1=br.read_Cog_evalue(nomfichier1,self._param.get(),self._dico_COG)
			dico_pos_fon2=br.read_Cog_evalue(nomfichier2,self._param.get(),self._dico_COG)		
			titre="Dotplot pour une e-value inférieur a: "+str(self._param.get())+espece1+" VS "+espece2
			bp.dotplot_cog(dico_pos_fon1,dico_pos_fon2,self._dico_COG,self._dico_fonction,int(self._t_syn.get()),int(self._d_syn.get()),titre,espece1,espece2,self._affichage.get(),self._save.get())
		elif self._test=="fonction":
			dico_pos_fon1=br.read_Cog_fonction(nomfichier1,self._dico_COG)
			dico_pos_fon2=br.read_Cog_fonction(nomfichier2,self._dico_COG)
			titre="Dotplot fonctionnel "+espece1+" VS "+espece2
			bp.dotplot_fon(dico_pos_fon1,dico_pos_fon2,self._dico_COG,self._dico_couleur,self._dico_fonction,int(self._t_syn.get()),int(self._d_syn.get()),titre,espece1,espece2,self._affichage.get(),self._save.get())
		
		
		

	def f_retour(self):
		self._fenetre_cog.destroy()
		lancement=Fenetre_une()
		lancement.main()
	
	
	def main(self):
		self._fenetre_cog.mainloop()
	

### Fenetre Choix du Test ###
class Fenetre_une:
	def __init__(self):


		# Crée la fenêtre
		self._fenetre_choix = Tk()
		self._fenetre_choix.title("choix du test")
		self._fenetre_choix.geometry("450x200")

		
		#Cree le choix du dossier
		
		self.LabelDossier=Label(self._fenetre_choix,text="Choix du dossier")
		self._lDossier=ttk.Combobox(self._fenetre_choix,width=200)
		self._avance=Button(self._fenetre_choix,text="-->",command=self.avancer)
		self._recule=Button(self._fenetre_choix,text="<--",command=self.reculer)
		self.LabelDossier.pack(side=TOP)
		self._lDossier.pack(side=TOP)
		self._avance.place(x=250,y=42)
		self._recule.place(x=150,y=42)
		self.dossier_init()

		#Crée les boutons 
		self._B_evalue=Button(self._fenetre_choix,text="E-value",width=12,command=self.f_evalue)
		self._B_identite=Button(self._fenetre_choix,text="Identite",width=12,command=self.f_identite)
		self._B_recouvrement=Button(self._fenetre_choix,text="Recouvrement",width=12,command=self.f_recouvrement)
		self._B_fonctions=Button(self._fenetre_choix,text="Fonction",width=12,command=self.f_fonction)

		#Place les boutons
		self._B_evalue.place(x=70,y=100)
		self._B_identite.place(x=250,y=100)
		self._B_recouvrement.place(x=70,y=140)
		self._B_fonctions.place(x=250,y=140)

	#Fonction qui actualise la liste des dossiers
	def dossier_init(self):
		dossier_list = []
		dossier_actuel = sys.path[0]
		for element in os.listdir(dossier_actuel):
			dossier_l = dossier_actuel + "/" + element
			if os.path.isdir(dossier_l):
				dossier_list.append(dossier_l)
 
		if dossier_list != []:
			self._lDossier['values'] = dossier_list
		self._lDossier.set(dossier_list[0])

	def avancer(self):
		dossier_list = [] 
		dossier_actuel=self._lDossier.get()
		for element in os.listdir(dossier_actuel):
			dossier_l = dossier_actuel + "/" + element
			if os.path.isdir(dossier_l):
				dossier_list.append(dossier_l)
 
		if dossier_list != []:
			self._lDossier['values'] = dossier_list

	def reculer(self):
		dossier_list = []
		dossier_prece=""
		dossier_actuel=self._lDossier.get().split("/")
		
		for i in dossier_actuel[:-1]:
			dossier_prece+=i+"/"
		self._lDossier.set(dossier_prece[:-1])
	
	#Lance les fentres propres à chaque test
	def f_evalue(self):
		dossier=self._lDossier.get()+"/"
		verification=br.f_cog_blast(dossier)
		self._fenetre_choix.destroy()
		if verification=="blast":
			fen_evalue=Fenetre_blast(dossier,"e_value")
			fen_evalue.main()
		else:
			fen_evalue=Fenetre_cog(dossier,"e_value")
			fen_evalue.main()

	def f_identite(self):
		dossier=self._lDossier.get()+"/"
		self._fenetre_choix.destroy()
		fen_identite=Fenetre_blast(dossier,"identite")
		fen_identite.main()

	def f_recouvrement(self):
		dossier=self._lDossier.get()+"/"
		self._fenetre_choix.destroy()
		fen_recouvrement=Fenetre_blast(dossier,"recouvrement")
		fen_recouvrement.main()

	def f_fonction(self):
		dossier=self._lDossier.get()+"/"
		self._fenetre_choix.destroy()
		fen_fonction=Fenetre_cog(dossier,"fonction")
		fen_fonction.main()

	#Lance la boucle d'attente de ma fenetre
	def main(self):
		
		self._fenetre_choix.mainloop()

lancement=Fenetre_une()
lancement.main()

