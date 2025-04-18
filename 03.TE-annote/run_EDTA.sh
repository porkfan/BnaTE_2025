cat genome_list.txt|while read sample;do
EDTA.pl --genome Brassica_napus.${genome}.genome.fa --species others --anno 1 --sensitive 1  --step all --t 40 --cds Brassica_napus.${genome}.cds.fa
done