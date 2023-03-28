[![hackmd-github-sync-badge](https://hackmd.io/FOS4WC4KSFCWq94aDoD-kw/badge)](https://hackmd.io/FOS4WC4KSFCWq94aDoD-kw)

# **Assemblage du génome d’Alnus glutinosa et recherche de séquences codantes des peptides antimicrobiens**

## I/ Contrôle qualité séquençage

### 1. Contrôle qualité 
**A) Short-Read** 

**a. Données utilisées**
- Données de séquençage Illumina de l'aulne glutineux [(accessible ici)](https://www.ebi.ac.uk/ena/browser/view/PRJNA374770)


**b. Outils et commandes utilisées**

Outil : [Fastqc](https://github.com/s-andrews/FastQC)

Commandes:

Un script lançant fastqc sur chacune de nos 8 paires de fichier a été réalisé. La syntaxe de base de la commande utilisée dans ce script est la suivante:
```
fastqc data/SRR5279623_1.fastq data/SRR5279623_2.fastq -o output/SRR5279623
```
**c. Analyse**

Fastqc présente en sortie un résumé global de la qualité des données et détaille ses analyses à l'aide de texte, tableau ou graphique.

| Résumé Global | Détail de la partie "Sequence Duplication Levels" |
| -------- | -------- |
| ![](https://i.imgur.com/QWEL0iL.png) | ![](https://i.imgur.com/Xx2tlXu.png)  |

Dans cet exemple, on peur remarque un **Warning** sur la partie *Per Tile Sequence Quality* et une **Erreur** sur la partie *Sequence Duplication Level*.

Le résultat de l'éxecution de fastqc sur l'entièreté des données de séquençage short-read est très satisfaisante, en effet, tout les fichiers présente une qualité nous permettant de les utiliser sans soucis. Les seuls Warning et Error que présentent nos données sont de type *Per Tile Sequence Quality*, *Sequence Duplication Level* et *Overrepresented Sequence*. Or après analyse, on constate que ces difficultés ne sont pas handicapantent pour notre utilisation des données.

**B) Long-Read** 

**a. Données utilisées**
- Données de séquençage Minion Nanopore de l'aulne glutineux [accessible ici](https://i.imgur.com/w13p5Pi.png) (mauvaise l'adresse)


**b. Outils et commandes utilisées**

Outil : [LongQC](https://github.com/yfukasawa/LongQC)

Commandes:

Après l'installation d'un environnement conda adapté à l'utilisation de LongCQ, la commande suivante à été utilisée:
```
python longQC.py sampleqc -x ont-ligation -o output/long-read data/long-reads.fq
```
L'option "*-x ont-ligation*" indique à longQC qu'il a affaire à des données *Oxford Nanopore Technologies*.

**c. Analyse**

LongQC présente en sortie 8 analyses sous la forme de tableau ou de graphique, à l'inverse de fastqc, il n'indique pas directement si telle partie est synonyme de bonne qualité ou pas mais il laisse à son utilisateur des guides d'analyse pour chaque partie comme ci-dessous.


| Analyse de la QValue des reads | ![](https://i.imgur.com/t8eHT7s.png) |
| ----- | -------- |
| Guide d'analyse | ![](https://i.imgur.com/tVzRb0B.png)  |

Pour ce graphique, on constate que tout les reads sont en effet de qualité supérieure à 10 et que leur distribution est bien semblable, on peut donc en conclure que nos reads ont bien une QValue de qualité suffisante.

Après analyse de toute les parties du compte-rendu de LongQC, il apparait que nos données Minion sont elles aussi de bonne qualité.

### 2. Contrôle des Contamination

## II/ Assemblage 

### 1. Assemblage de novo 

**A) DBG2OLC**

Ce pipeline assemble dans un premier temps les short reads puis en s'aidant d'un module consensus (sparc/pbdagcon de blasr) aligne les long reads pour produire un assemblage final.

En raison du grand nombre de blocages rencontrés dans les scripts blasr, les recherches n'ont pas été poursuivies pour ce pipeline. En effet, blasr semble être un ancien outil d'alignment de long reads qui semble avoir été dépassé il y a quelques années par minimap2.

Minimap2 n'a pas non plus pu remplacé blasr étant donné que DBG2OLC traite spécifiquement les données de sortie de blasr.

**B) CulebrONT**

in progress!!


### 2. Amélioration assemblage short-read

*Données utilisées : assemblage short-read incomplet ; long-reads nanopore*

**A) Outils de Gap-filling : MaSuRCA** 

**a. Installation et lancement**
- Installation de MaSuRCA qui inclut l'outils de Gap-filling SAMBA ([Github MaSuRCA](https://github.com/alekseyzimin/masurca))
- Lancement de la commande 
```
./samba.sh -r <assemblage-short-read.fasta> -q <long-read.fasta/.fastq> -m 10000
```
Choix paramètre -m (minimum matching length):  
D'après la documentation de SAMBA, *"10000 est la meilleure valeur pour les grands génomes de plantes hautement répétitifs"* 

**b. Contrôle qualité de l'assemblage obtenue : QUAST**

- Installation de QUAST ([GitHub](https://))
- Lancement de la commande
```
./quast.py <assemblage.fasta> -o <fichier_sortie>
```
- Analyse et comparaison de la sortie de QUAST ([Documentation sortie QUAST](https://quast.sourceforge.net/docs/manual.html#sec3))  


| Assemblage short-readsde réference | Assemblage sortie de gap-filling |
| --------                           | -------- |
| ![](https://i.imgur.com/K68Tu9j.png) |  ![](https://i.imgur.com/Nt5qyfN.png)
   |

- Discussion  

Après analyse de la qualité de l'assemblage, on remarque que l'assemblage obtenue avec SAMBA est assez similaire à l'assemblage de référence short-reads.
Selon les critères étudiés ([N50, L50](https://en.wikipedia.org/wiki/N50,_L50,_and_related_statistics#N50), N's per 100 kbp etc.), on voit que le nouvelle assemblage n'est pas vraiment meilleur voir moins bon sur certains critères notamment le N50 et le L50. On remarque entre autres que "N's per 100 kbp" ne diminue que d'une vingtaine de bases.On voit cependant que le nombre de contigs à diminue.  
Ces observations nous ont amené à remettre en question le bon fonctionnement de SAMBA. Nous nous sommes entre autres penché sur le paramètre '-m' vu précédement et avons testé une valeur inférieur (-5000). 

- Comparaison des sorties de contrôles qualités QUAST selon le paramètre -m  


| Assemblage -m 10000 | Assemblage -m 5000 |
| --------            |           -------- |
|![](https://i.imgur.com/yp19F2l.png)| ![](https://i.imgur.com/cB9IjNh.png)

  
 -Discussion  
 
La modifcation du paramètre '-m' permet d'obtenir un assemblage légèrement meilleur. En effet, on retrouve un N50 plus haut, un L50 plus bas et une "N's per 100 kbp" diminué d'une centaine de bases. De plus on remaruqe une plus forte diminution du nombre de contigs. Le paramètre '-m' semble donc donner un assemblage de meilleure qualité avec une valeur de 5000.  
Néanmoins, ce second assemblage reste similaire à l'assemblage de référence short-read.  
Ce première outils de Gap-filling semble ordonner les contigs entre eux diminuant ainsi le nombre de contigs mais ne permet pas de net amélioration du point de vu des Mismatches.
Ces observations nous ont amené a tester un second outil de gap-filling. 


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
| ![](https://i.imgur.com/K68Tu9j.png) |  ![](https://i.imgur.com/KRyEnhq.png)

- Discussion  

L'assemblage obtenue semble un peu meilleur du point de vu du N50 et L50 mais on remarque une net diminution des Mismatches "N's". En effet, on passe de 10 mille bases pour "N's per 100 kbp" a moins de 500 bases.Mais on remarque aussi que cette outils de gap-filling n'a pas eu d'impact sur le nombre de contigs  
Cette observation montre que ce second outils de Gap-filling à mieux fonctionné que le premier du point des vu des Mismatches (N's) et nous rend un assemblage plus complet. Néanmoins, il n'a pas permit d'ordonner les reads entre eux et ainsi ne diminue pas le nombre de contigs.  

**C) LR_Gapcloser et SAMBA**

Les observations faites précedement lors de l'utilisation des deux outils de Gap-filling, nous on amener à utiliser l'assemblage de sortie de LR_Gapcloser comme entrée de SAMBA. En effet, le première outils 'corrige' les Mismatches tandis que le second semble ordonner les contigs.  

- Lancement de la commande
```
./samba.sh -r <gapclosed.fasta> -q <long-read-sequencing.fastq> -m 5000
```



## III/ Recherche des séquences de PAMs

### 1. Données nanopore (long-reads)

### 2. Assemblages 

### 3. Analyse
