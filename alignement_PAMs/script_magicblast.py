import subprocess
import os
import re


### Liste des sequences de PAM

dossier_pam = 'data/PAMs'
liste_pam = []
for fichier in os.listdir(dossier_pam):
    if fichier.endswith(".fa"):
        liste_pam.append(os.path.join(dossier_pam, fichier))


# Chemin vers le fichier ou on aligne (genome)
fichier_entre = 'data/ref/genome_db_V2.fa'


### Creation de la base de donnees Magicblast

makeblastdb = f"makeblastdb -in {fichier_entre} -dbtype nucl -out data/ref/genome_db_V2"
subprocess.run(makeblastdb, shell=True, check=True)

# Boucle sur les sequences de PAM
for pam in liste_pam:
    # Alignement de la sequence de PAM sur le genome avec Magicblast
    fichier_sortie = f"{pam}.sam"
    fichier_sortie = re.sub('/','_', fichier_sortie)
    # le nom des fichiers contient des "/", on les remplace par des "_" pour que la commande magicblast fonctionne bien en retrouvant les dossiers
    chemin_sortie = os.path.join('result/result_magicblast', fichier_sortie)
    print(pam)
    print(chemin_sortie)
    commande_magicblast = f"magicblast -query {pam} -db data/ref/genome_db_V2 -splice T -outfmt sam -out {chemin_sortie}"
    subprocess.run(commande_magicblast, shell=True, check=True)
