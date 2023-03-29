[![hackmd-github-sync-badge](https://hackmd.io/FOS4WC4KSFCWq94aDoD-kw/badge)](https://hackmd.io/FOS4WC4KSFCWq94aDoD-kw)

# **Assemblage du génome de l'Aulne glutineux et recherche de séquences codant des peptides antimicrobiens**

*Pierre-Antoine Navarro - Gauri Roussin - Cornélius Venturini - Mélody Temperville*

## I/ Contrôle qualité des données de séquençage

### 1. Qualité des reads
**A) Short-Read** 

**a. Données utilisées**
- Données de séquençage Illumina de l'aulne glutineux [(accessible ici)](https://www.ebi.ac.uk/ena/browser/view/PRJNA374770)


**b. Outils et commandes utilisées**

Outil : [Fastqc](https://github.com/s-andrews/FastQC)

Commandes:

Un script lançant fastqc sur chacune de nos 8 paires de fichier a été réalisé.  
La syntaxe de base de la commande utilisée dans ce script est la suivante :
```
fastqc <sequencage-short-read_1.fasta> <sequencage-short-read_2.fasta> -o <fichier_sortie>
```
**c. Analyse**

Fastqc présente en sortie un résumé global de la qualité des données et détaille ses analyses à l'aide de texte, tableau ou graphique.

| Résumé Global | Détail de la partie "Sequence Duplication Levels" |
| -------- | -------- |
| ![](https://i.imgur.com/QWEL0iL.png) | ![](https://i.imgur.com/Xx2tlXu.png)  |

Dans cet exemple, on peut remarquer un **Warning** sur la partie *Per Tile Sequence Quality* et une **Erreur** sur la partie *Sequence Duplication Level*.  

Les résultats de fastqc sur l'ensemble des short-reads montrent que nos données sont de bonnes qualités.  
En effet, les seuls Warning et Error que présentent nos données short-read sont de type *Per Tile Sequence Quality*, *Sequence Duplication Level* et *Overrepresented Sequence*.  
Or après analyse du rapport, on constate que ces *warning/erreur* ne représentent pas un problème pour notre utilisation des données.

**B) Long-Read** 

**a. Données utilisées**
- Données de séquençage Minion Nanopore de l'aulne glutineux (privées)


**b. Outils et commandes utilisées**

Outil : [LongQC](https://github.com/yfukasawa/LongQC)

Commandes:

Après l'installation d'un environnement conda adapté à l'utilisation de LongQC, la commande suivante a été utilisée :
```
python longQC.py sampleqc -x ont-ligation -o <fichier_sortie>
```
L'option "*-x ont-ligation*" indique à longQC qu'il a affaire à des données *Oxford Nanopore Technologies*.

**c. Analyse**

LongQC présente en sortie 8 analyses sous la forme de tableau ou de graphique.  
L'analyse se fait à l'aide d'un guide utilisateur fournis par LongQC.


| Analyse de la QValue des reads | ![](https://i.imgur.com/t8eHT7s.png) |
| ----- | -------- |
| **Guide d'analyse** | ![](https://i.imgur.com/tVzRb0B.png)  |

Par exemple, on remarque ici que les reads sont de QValue supérieure à 10 avec des distributions semblable. On peut donc conclure selon le guide d'analyse que nos reads sont de bonne qualité.

Après analyse de toute les parties du compte-rendu de LongQC, il apparait que nos données Minion sont elles aussi de bonne qualité.

### 2. Recherche de contaminants

**A) Short-Read** 

**a. Données utilisées**
- Données de séquençage Illumina de l'Aulne glutineux [(accessible ici)](https://www.ebi.ac.uk/ena/browser/view/PRJNA374770)


**b. Outils et commandes utilisées**

Outil : [Kraken](https://github.com/DerrickWood/kraken)

Commandes:

Kraken est un outil qui permet d'assigner à de courtes séquences d'ADN un label taxonomique. Nous nous en servons donc pour repérer si les données de séquençage contiennent des éléments non propre au génome de l'Aulne glutineux.  
Un script bash a été réalisé pour lancer kraken sur chacun des 16 fichier short-read. La syntaxe de base des commandes utilisées dans ce script sont les suivante:
```
kraken --db <database> --gzip-compressed --fastq-input <sequencage-short-read.fasta> > <report-short-read>
kraken-report --db <database> <report-short-read> > <output-short-read>
```
On peut remarquer que kraken prend en paramètre une base de données. Dans le cadre de ce projet, la base de données [minikraken-8GB](http://ccb.jhu.edu/software/kraken/dl/minikraken_20171019_4GB.tgz) a été utilisée. Plusieurs version sont disponible, dont la meilleure pesant 500GB, mais par soucis de place, nous nous sommes restreint à celle de 8GB.

**c. Analyse**

| kraken | ![](https://i.imgur.com/JO3wEId.png) |
| ----- | -------- |
| **kraken-report** | ![](https://i.imgur.com/pmSMPRA.png)  |

Pour chacun de nos 16 fichiers fasta, la commande `kraken` renvoie un fichier tsv. La première colonne indique si le read concerné est "C-Classified/U-Unclassified"
Ensuite, la commande `kraken-report` permet de synthétiser le résultat de `kraken` sur l'entièreté du fichier.  
Un read "Classified" peut être un read contaminant, dans la partie `kraken-report`, on peut voir 0.67% de "Bacteria". Un read "Unclassified" est considéré comme appartenant à l'hôte.   

Dans le cas présenté ici, on trouve 99.26% de séquences "Unclassified", on a choisi un seuil de contamination maximum de 10% donc quoi que contiennent les données "Classified", on considère cet échantillon à la hauteur de nos critères de qualité.  
Pour les données short-read, la quantité mimimum de séquence "Classified" est de 97.47%, cet échantillon présente donc plus de 2% de génome bactérien dans ses reads. Étant donné que cela ne dépasse pas le seuil fixé on les considèrent de bonne qualité.


**B) Long-Read** 

**a. Données utilisées**
- Données de séquençage Minion Nanopore de l'Aulne glutineux (privées)


**b. Outils et commandes utilisées**

Outil : [Kraken](https://github.com/DerrickWood/kraken)

Commandes:

```
kraken --db minikraken_20171019_8GB --gzip-compressed --fastq-input data/long-read-seq.fq > output/report-long-read.txt
kraken-report --db minikraken_20171019_8GB output/report-long-read.txt > output/recap-long-read.txt
```

**c. Analyse**

Comme vu précédemment, `kraken` nous renvoie d'abord un rapport qu'on analyse ensuite avec `kraken-report`.  
On récupère toutes les lignes dont le pourcentage est supérieur à 1 grâce à un script `awk` ce qui nous permet de savoir d'où vienne les contaminations.


| **kraken-report** | ![](https://i.imgur.com/YTXhFX7.png)
| -------- | -------- |
| **awk** |![](https://i.imgur.com/GqZh4kY.png)
 | 

Finalement, on a plus de 90% de "Unclassified", on considère donc nos données comme respectant notre seuil de qualité.

## II/ Assemblage 

### 1. Amélioration assemblage short-read

*Données utilisées : assemblage short-read de 2018 ; long-reads nanopore*

**A) Outils de Gap-filling : SAMBA** 

**a. Installation et lancement**
- Installation de MaSuRCA qui inclut l'outil de Gap-filling SAMBA ([Github MaSuRCA](https://github.com/alekseyzimin/masurca))
- Lancement de la commande 
```
./samba.sh -r <assemblage-short-read.fasta> -q <long-read.fasta/.fastq> -m 10000
```
Choix paramètre -m (minimum matching length):  
D'après la documentation de SAMBA, *"10000 est la meilleure valeur pour les grands génomes de plantes hautement répétitifs"* 

**b. Contrôle qualité de l'assemblage obtenu : QUAST**

- Installation de QUAST ([GitHub](https://))
- Lancement de la commande
```
./quast.py <assemblage.fasta> -o <fichier_sortie>
```
- Analyse et comparaison de la sortie de QUAST ([Documentation sortie QUAST](https://quast.sourceforge.net/docs/manual.html#sec3))  


| Assemblage short-reads de réference | Assemblage sortie de gap-filling |
| --------                           | -------- |
| ![](https://i.imgur.com/K68Tu9j.png) |  ![](https://i.imgur.com/Nt5qyfN.png)
   |

- Discussion  

Après analyse de la qualité, on remarque que l'assemblage obtenu avec SAMBA est assez similaire à l'assemblage de référence short-reads.
Selon les critères étudiés ([N50, L50](https://en.wikipedia.org/wiki/N50,_L50,_and_related_statistics#N50), N's per 100 kbp etc.), on voit que le nouvel assemblage n'est pas meilleur voire moins bon sur certains critères notamment le N50 et le L50. On remarque entre autres que "N's per 100 kbp" ne diminue que d'une vingtaine de bases. Cependant le nombre de contigs a diminué car certains ont été regroupés.  
Ces observations nous ont amenés à remettre en question le bon fonctionnement de SAMBA. Nous nous sommes entre autres penchés sur le paramètre '-m' vu précédemment et avons testé une valeur inférieure (-5000). 

- Comparaison des sorties de contrôles qualités QUAST selon le paramètre -m  


| Assemblage -m 10000 | Assemblage -m 5000 |
| --------            |           -------- |
|![](https://i.imgur.com/yp19F2l.png)| ![](https://i.imgur.com/cB9IjNh.png)

  
- Discussion  

La modification du paramètre '-m' permet d'obtenir un assemblage légèrement meilleur. En effet, on retrouve un N50 plus grand, un L50 plus faible et une "N's per 100 kbp" diminué d'une centaine de bases. De plus, on remarque une plus forte diminution du nombre de contigs. Le paramètre '-m' semble donc donner un assemblage de meilleure qualité avec une valeur de 5000.  
Néanmoins, la modification de ce paramètre le rend moins optimal pour les grands génomes de plantes et risque de créer de faux scaffolds.  
Ce second assemblage reste similaire à celui de référence.  
Ce premier outil de gap-filling semble regrouper des contigs entre eux diminuant ainsi le nombre de contigs mais, ne permet pas de nettes améliorations du point de vue des mismatchs.
Ces observations nous ont amené à tester un second outil de gap-filling. 


**B) Outils de Gap-Filling : LR_Gapcloser**


**a. Installation et lancement**

- Installation de LR_Gapcloser ([Github LR_Gapcloser](https://github.com/CAFS-bioinformatics/LR_Gapcloser))
- Lancement de la commande 
```
 ./LR_Gapcloser.sh -i <short-read-assembly.fasta> -l <long_read.fasta> -s n -o <fichier_sortie>
```
*Paramètre "-s n" car nous travaillons avec des long-reads nanopores.*


**b. Contrôle qualité de l'assemblage obtenue : QUAST**

- Installation de QUAST ([GitHub](https://))
- Lancement de la commande
```
./quast.py <assemblage.fasta> -o <fichier_sortie>
```
- Analyse et comparaison de la sortie de QUAST ([Documentation sortie QUAST](https://quast.sourceforge.net/docs/manual.html#sec3))  


| Assemblage short-readsde réference | Assemblage sortie de gap-filling |
| --------                           | -------- |
| ![](https://i.imgur.com/K68Tu9j.png) |  ![](https://i.imgur.com/FmpJn8s.png)



- Discussion  

L'assemblage obtenu semble un peu meilleur du point de vu du N50 et L50. De plus, on remarque une nette diminution des mismatchs "N's". En effet, on passe de 10 mille bases pour "N's per 100 kbp" à moins de 500 bases. 
On remarque que le 'Largest contig' a augmenté mais que le nombre de contigs est le même que celui du génome de référence.  
Cette observation montre que ce second outil de Gap-filling a mieux fonctionné que le premier du point de vu des mismatchs (N's) et nous rend un assemblage plus complet. Néanmoins, il n'a pas permis d'ordonner et de regrouper les contigs entre eux et ainsi ne diminue pas leur nombre.  

**C) LR_Gapcloser et SAMBA**

**a. Discussion et lancement**

Les observations faites précedement lors de l'utilisation des deux outils de Gap-filling, nous on amener à utiliser l'assemblage de sortie de LR_Gapcloser comme entrée de SAMBA. En effet, le première outils 'corrige' les Mismatches tandis que le second semble ordonner et regrouper les contigs.  

- Lancement de la commande
```
./samba.sh -r <gapclosed.fasta> -q <long-read-sequencing.fastq> -m 5000
```

**b. Contrôle qualité de l'assemblage obtenue : QUAST**

- Installation de QUAST ([GitHub](https://))
- Lancement de la commande
```
./quast.py <assemblage.fasta> -o <fichier_sortie>
```
- Analyse et comparaison de la sortie de QUAST ([Documentation sortie QUAST](https://quast.sourceforge.net/docs/manual.html#sec3))

| Assemblage short-readsde réference | Assemblage sortie de gap-filling |
| --------                           | -------- |
| ![](https://i.imgur.com/K68Tu9j.png) |  ![](https://i.imgur.com/Smvx0XC.png)


- Discussion  
Ce dernier assemblage semble une fois de plus meilleur que le précédent selon les critères N50, L50, nombre de contigs et N's. Néanmoins, le nombre total de contigs reste très grand et notre assemblage reste incomplet.  
Nos outils de gap-filling, nous ont permis d'améliorer l'assemblage short-reads notamment du point de vue des Mismatches.  
Néanmoins, l'utilisation des long-reads en vue de compléter cet assemblage n'est pas entièrement exploré. En effet, il serait intéressant d'utiliser des outils d'avantage centré sur le rangement et le regroupement des contigs afin d'obtenir un nombre final de contigs réduit et des contigs plus longs.  
Nous nous sommes intéressé dans ce but à l'outil LongStitch ([GitHub](https://github.com/bcgsc/longstitch)) que nous n'avons pas pu faire fonctionner dans les délais de fin de projet, mais qui pourrait être intéressant de tester.

### 2. Assemblage hybride, non concluant  

**A) DBG2OLC ([GitHub](https://github.com/yechengxi/DBG2OLC))**

Ce pipeline assemble dans un premier temps les short-reads puis en s'aidant d'un module consensus (sparc/pbdagcon de blasr) aligne les long-reads pour produire un assemblage final.

Aucun assemblage hybride n'a pu être obtenu avec ce pipeline en raison de la désuétude de l'outil suivant l'assemblage des short-reads (blasr).



**B) CulebrONT ([GitHub](https://github.com/SouthGreenPlatform/culebrONT))**

Culebront est un outil d’assemblage hybride pour génomes eucaryotes et procaryotes. Il regroupe de nombreux outils: pour l’assemblage de lectures longues (Canu, Flye, Smartdenovo,…), le polissage (Racon), de contrôle qualité (Quast, Assemblytics, Flagstats,…) et de correction (Pilon, Nanopolish). 
Les outils peuvent être choisis en fonction des choix de paramètres proposés.

Étant donné les délais de fin de projet et les soucis rencontrés lors du lancement du pipeline nous n'avons pas pu obtenir un assemblage hybride. Néanmoins, il serait pertinant de réalisé cet assemblage afin de le comparer au génome de référence short-reads obtenu en 2018 ainsi que ceux obtenus à l'aide du Gap-Filling. 


## III/ Recherche des séquences de PAMs

### 1. Recherche sur les données nanopore (long-reads)

Cette étape réalisée en début de projet permet de savoir si les données de séquençage sont exploitables. En effet, si on ne retrouve pas les séquences codant pour nos peptides antimicrobien (PAMs), il faudrait produire de nouvelles données. Les séquences PAMs ont été obtenues grâce à la rétrotranscription de l'ARNm. Elles peuvent donc être différentes de leurs gênes dû à l'absence d'introns.

**a. Utilisation de BLAST et BWA**

En raison du taux d'erreur du séquençage nanopore et du potentiel épissage que subissent les transcrits de nos PAMs, les outils adaptés à l'épissage ont du mal à faire un alignement qualitatif sur les long-read. BWA et BLASTn ont donc été utilisés pour essayer d'aligner les séquences PAMs sur les exons présents sur les reads. Ces derniers peuvent faire un bon alignement local en s'adaptant aux erreurs. 

Des scripts python ont été créés pour automatiser les étapes suivantes : 
- Préparation des données long-reads : 
```
### indexage des séquences long-reads pour bwa
bwa index reads.fq

### création d'une base de donnée pour blast
makeblastdb -in longreads.fa -dbtype nucl -out longreads_db
```
- Alignement : 
```
# BLAST
blastn -query pam.fa -db longreads_db -outfmt '17 SQ' -out alignement.sam
```
L'option -outfmt formate le fichier de sorti pour conserver des informations sur tout les reads qui s'alignent.
```
# BWA
bwa mem -T 90 reads.fq pam.fa > alignement.sam
```
L'option-T 90 permet de ne conserver que les alignement avec un score d'identité supérieur à 90 sur 100.

**b. Résultats**

On retrouve bien des alignements de PAMs sur certaines séquences de long-reads (entre 30 et 200 reads). On peut donc supposer qu'on retrouvera nos séquences d'intérêts sur l'assemblage final.


### 2. Alignement sur le génome avec Magicblast

Pour rechercher la présence des peptides anti-microbien dans le jeu de donnée à disposition, Magicblast a été utilisé. Ce dernier est un outil d'alignement pouvant traiter une grande quantité de données avec précision, il a l'avantage de prendre en compte l'épissage.

**a. Installation**

La dernière version de magicblast (1.7.1) est disponible sur le site :

https://ftp.ncbi.nlm.nih.gov/blast/executables/magicblast/LATEST/

**b. Utilisation**

Des scripts python ont été créés pour automatiser les étapes suivantes :

- Création d'une base de donnée à partir du génome : 
```
makeblastdb -in <genome.fa> -dbtype nucl -out <genome_db>
```
*nucl pour nucléotide indique le type de la séquence.*

- Lancement de l'alignement 
```
magicblast -query <Pam.fa> -db <genome_db> -splice T -outfmt sam -out <fichier_sortie.sam>
```
*splice T pour faire un alignement avec épissage*

**c. Résultats**

 Avec samtools, les fichiers de sortie sont traités pour être visualisés sur IGV. Le pourcentage d'identité et le Query Cover sont calculés pour juger la qualité de l'alignement, et déterminer si on localise bien le gène PAM sur le génome.

| Observation IGV des gènes codant ag9 et ag15|
| -------- |
|
! ![](https://i.imgur.com/j4ZTO7F.png)|

Après observation de nos 11 PAMs retrouvés, on suppose que 7 d'entre eux subissent un épissage. On peut aussi observer des cas d'épissage alternatif comme avec ag9 et ag15. 

 *Table des PAMs alignés sur le génome :*
![](https://i.imgur.com/6XIeZ2J.png)

Au vu des scores trouvés, on retrouve 11 des 12 PAMs connus dans le génome. Seul l'ag4 n'a pas donnée de résultat pertinent, soit il est localisé dans une région non assemblée du génome, soit les outils d'alignement n'ont pas permis de le retrouver.

