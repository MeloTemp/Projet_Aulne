import subprocess
import os
import re


### Liste des sequences de PAM

dossier_pam = 'PAMs'
liste_pam = []
for fichier in os.listdir(dossier_pam):
    if fichier.endswith(".fa"):
        liste_pam.append(os.path.join(dossier_pam, fichier))


### Liste des long reads

dossier_long_reads= "longreads/run1"
liste_long_reads = []
for fichier in os.listdir(dossier_long_reads):
    if fichier.endswith(".gz"):
        liste_long_reads.append(os.path.join(dossier_long_reads, fichier))



# Boucle sur les long reads
for long_read in liste_long_reads:
    # Decompresse la sequence long read
    fichier_fq = 'zcat ' + long_read + ' > fichier.fq'
    subprocess.run(fichier_fq, shell=True, check=True)
    # Indexage de la sequence long read    
    indexx = 'bwa index fichier.fq'
    subprocess.run(indexx, shell=True, check=True)

    
    # Boucle sur les sequences de PAM
    for pam in liste_pam:
        # Aligner la sequence de PAM sur la sequence long read
        fichier_sortie = long_read + '_' + pam + '.sam'
        fichier_sortie = re.sub('/','_', fichier_sortie)
        # le nom des fichiers contient des "/", on les remplace par des "_" pour que la commande bwa fonctionne bien en retrouvant les dossiers
        chemin_sortie = os.path.join('result_long', fichier_sortie)
        alignement = 'bwa mem -t 4 -T 90 fichier.fq ' + pam + ' > ' + chemin_sortie
        # on ne conserve que les alignement avec un score d alignement superieur a 90 sur 100
        subprocess.run(alignement, shell=True, check=True)
        print(pam)