module load STAR/2.7.8a
module load SAMtools/1.9
sample=$1
mkdir -p star/${sample}
#Alignment
STAR --runThreadN 4 --genomeDir ref  --twopassMode Basic --readFilesCommand zcat --readFilesIn 01_trim/20DAF_seed/${sample}_1_val_1.fq.gz  01_trim/20DAF_seed/${sample}_2_val_2.fq.gz  --outFileNamePrefix star/${sample}/${sample} --outSAMtype BAM SortedByCoordinate --outBAMsortingThreadN 4 --quantMode  GeneCounts
samtools index star/${sample}/${sample}Aligned.sortedByCoord.out.bam