------------------------------------------------------------------
DotPlot
------------------------------------------------------------------

Utilité:

DotPlot est un programme écrit sous Python3 qui permet de tracer des plots de match entre 2 organismes à l'aide de fichiers Blast ou de 
fichiers COG. En plus de tracer des graphes ce programme permet de sauvegarder dans un fichier la position des gènes appartenant à un bloc de synthénie.

------------------------------------------------------------------ 

Constitution du programme:

-fichier main.py qui sert à lancer le programme
-fichier bibliotheque_read.py qui comprend toutes les fonctions de lecture et d'écriture de fichier
-fichier bibliotheque_plot.py qui comprend toutes les fonctions de tracage de plot
-Un dossier Fichier_Lecture qui contient les fichiers:
	*couleur.txt qui permet d'associer chaque fonction à une couleur pour le dotplot fonction
	*prokaryotes_complete-genome.csv
	*cognames2003-2014.tab.txt
	*fun2003-2014.tab.txt

-----------------------------------------------------------------

Utilisation:

-Run sous python3
-Fichier COG enregistré dans un fichier qui leur est consacré
-Fichier Blast enregistré dans un fichier qui leur est consacré

-----------------------------------------------------------------

Comment utilisé le programme:

1/Choisir un dossier contenant les fichiers COG ou Blast (pour naviguer dans les répertoires utilisez la flèche de droite pour avancer dans l'arborescence et la flèche de gauche pour descendre)
2/Choisir le type de test pour filtrer les résultats:
	* E-value      (fonctionne pour des fichiers COG et Blast)
	* Identité     (fonctionne uniquement pour des fichiers Blast)
	* Recouvrement (fonctionne uniquement pour des fichiers Blast)
	* Fonction     (fonctionne uniquement pour des fichiers COG)
3/Sélectionner la ou les organisme(s) à faire matcher
4/Selon le type de test entrée les paramètres de filtrage (seuil d'e-value, pourcentage d'identité, pourcentage de recouvrement) ainsi que les paramètres pour les blocs de synthénie (taille minimale d'un bloc, distance maximale entre 2 gènes d'un bloc)
5/Séléctionner "Afficher les blocs de synthénie" pour les faire apparaitre sur le graphique
6/Séléctionner "Sauvegarder les blocs de synthénie" pour les sauvegarder dans un fichier text dans le répertoire du fichier "main.py"
7/Pour revenir au choix du test appuyer sur la flèche en haut à gauche
8/Pour quiter appuyer simplement sur la croix rouge en haut à droite

-----------------------------------------------------------------



