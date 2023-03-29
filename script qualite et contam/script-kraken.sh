#!/bin/bash

source ~/.bashrc
conda activate kraken
BD="/data/home/pnavarro/PROJET_AULNE/tool/virtual_env/kraken_env/minikraken_20171019_8GB"


for f in *.gz; do
	echo "$f:"
	kraken --db $BD --gzip-compressed --fastq-input $f > ../contam-report/report-$f.txt
	kraken-report --db $BD ../contam-report/report-$f.txt > ../contam-report/recap-$f.txt
done

