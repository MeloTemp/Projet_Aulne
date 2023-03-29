import subprocess
import os
import re


### Liste des sequences de PAM

dossier_pam = 'data/PAMs'
liste_pam = []
for fichier in os.listdir(dossier_pam):
    if fichier.endswith(".fa"):
        liste_pam.append(os.path.join(dossier_pam, fichier))


### Chemin vers le dossier contenant les long reads

dossier_long_reads = 'data/longreads/run1'  # dossier perso
dossier_long_reads = 'data/longreads/format_fasta/'


### Creation de la base de donnees Blast

makeblastdb = f"makeblastdb -in {dossier_long_reads}/*.fasta -dbtype nucl -out data/longreads_db"
# Cette commande s execute grace a la commande subprocess.run
subprocess.run(makeblastdb, shell=True, check=True)


#### Boucle sur les sequences de PAM

for pam in liste_pam:
    # Aligner la sequence de PAM sur la base de donnees Blast
    fichier_sortie = f"{pam}.sam"
    fichier_sortie = re.sub('/','_', fichier_sortie)
    # le nom des fichiers contient des "/", on les remplace par des "_" pour que la commande blast fonctionne bien en retrouvant les dossiers
    chemin_sortie = os.path.join('result/result_longV2', fichier_sortie)
    blastn = f"blastn -query {pam} -db data/longreads_db -outfmt '17 SQ' -out {chemin_sortie}"
    subprocess.run(blastn, shell=True, check=True)