# 3. TE-annote

## 3.1 TE annote in 14 genomes by EDTA

```bash
EDTA.pl --genome Brassica_napus.${genome}.genome.fa --species others --anno 1 --sensitive 1  --step all --t 40 --cds Brassica_napus.${genome}.cds.fa
```

## 3.2 panEDTA pipeline build a panTElib in 14 genomes

```bash
sh panEDTA.sh -g genome_list.txt  -c Brassica_napus.ZS11.v0.cds.fa  -t 40
```

## 3.3 repeatmasker 14genomes by panTElib

```bash
cat genome_list|while read sample;do
bsub -J ${sample}_RM -q normal -n 10 -R span[hosts=1] -o log/${sample}_RM.out -e log/${sample}_RM.err \
"RepeatMasker -e ncbi -pa 20 -q -div 40 -lib genome_list.txt.panEDTA.TElib.fa  -cutoff 225 -gff Brassica_napus.${sample}.genome.fa"
done
```
