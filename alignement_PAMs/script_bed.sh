#!/bin/bash

# Les fichiers de sorties au format .sam de nos allignements PAM sur assemblage ont ensuite été convertis au format .bam, puis triés et indexés avec les commandes samtools view, samtools sort et samtools index


# Conversion des fichiers SAM en fichier BAM pour les resultats d'allignement sur le genome gapfilling
for file in result/result_gapf/*.sam; do # result
  samtools view -Sb $file > ${file%.sam}.bam
done

# Tri et indexation des fichiers BAM
for file in result/result_gapf/*.bam; do # result
  samtools sort $file -o ${file%.bam}_sorted.bam
  samtools index ${file%.bam}_sorted.bam
done

# Conversion des fichiers SAM en fichier BAM pour les resultats d'allignement magicblast sur le genome de ref
for file in result/result_magicblast/*.sam; do # result
  samtools view -Sb $file > ${file%.sam}.bam
done

# Tri et indexation des fichiers BAM
for file in result/result_magicblast/*.bam; do # result
  samtools sort $file -o ${file%.bam}_sorted.bam
  samtools index ${file%.bam}_sorted.bam
done