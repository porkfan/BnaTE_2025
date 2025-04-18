cat genome_list.txt|while read sample;do
bsub -J ${sample}_RM -q normal -n 10 -R span[hosts=1] -o log/${sample}_RM.out -e log/${sample}_RM.err \
"RepeatMasker -e ncbi -pa 20 -q -div 40 -lib genome_list.txt.panEDTA.TElib.fa  -cutoff 225 -gff Brassica_napus.${sample}.genome.fa"
done