import subprocess
import os
import re


### Liste des sequences de PAM

dossier_pam = 'data/PAMs'
liste_pam = []
for fichier in os.listdir(dossier_pam):
    if fichier.endswith(".fa"):
        liste_pam.append(os.path.join(dossier_pam, fichier))


### Chemin vers le fichier des longreads

fichier_longreads = 'data/longreads/format_fasta/long_read.fasta'


### Creation de la base de donnees Magicblast

makeblastdb = f"makeblastdb -in {fichier_longreads} -dbtype nucl -out data/longreads/format_fasta/longreads_db"
subprocess.run(makeblastdb, shell=True, check=True)


### Boucle sur les séquences de PAM

for pam in liste_pam:
    # Alignement de la sequence de PAM sur les longreads avec Magicblast
    fichier_sortie = f"{pam}.sam"
    fichier_sortie = re.sub('/','_', fichier_sortie)
    # le nom des fichiers contient des "/", on les remplace par des "_" pour que la commande magicblast fonctionne bien en retrouvant les dossiers
    chemin_sortie = os.path.join('result/result_longV3', fichier_sortie)
    print(pam)
    print(chemin_sortie)
    commande_magicblast = f"magicblast -query {pam} -db data/longreads/format_fasta/longreads_db -splice T  -outfmt sam -score 80 -out {chemin_sortie}"
    subprocess.run(commande_magicblast, shell=True, check=True)
