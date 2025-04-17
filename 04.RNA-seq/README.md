# 5. RNA-seq

## 5.1 Quality Control

```bash
# 01_TrimGalore.sh
module load TrimGalore/0.6.6
sample=$1
trim_galore --paired --quality 20 -a AGATCGGAAGAGC -a2 AGATCGGAAGAGC --length 20 -o 01_trim/40DAF_seed/  raw_data/40DAF_seed/${sample}_1.fq.gz raw_data/40DAF_seed/${sample}_2.fq.gz
```

## 5.2 Alignment

```bash
#02_star.sh
module load STAR/2.7.8a
module load SAMtools/1.9
sample=$1
mkdir -p star/${sample}
#Alignment
STAR --runThreadN 4 --genomeDir GL_ref  --twopassMode Basic --readFilesCommand zcat --readFilesIn 01_trim/20DAF_seed/${sample}_1_val_1.fq.gz  01_trim/20DAF_seed/${sample}_2_val_2.fq.gz  --outFileNamePrefix star/${sample}/${sample} --outSAMtype BAM SortedByCoordinate --outBAMsortingThreadN 4 --quantMode  GeneCounts
samtools index star/${sample}/${sample}Aligned.sortedByCoord.out.bam
```

## 5.3 TMM Normalization

```R
library(edgeR)
data=read.table("read_counts_filter.txt", header = TRUE)
# Extract sample columns
gene_info <- data[, 1:6] # First six columns are gene information
counts_matrix <- data[, 7:ncol(data)]
# Create DGEList object
dge <- DGEList(counts = counts_matrix)
# Perform TMM normalization
dge <- calcNormFactors(dge)
# View normalized data
normalized_counts <- cpm(dge, log = TRUE)
# Merge gene information with normalized data
normalized_data <- cbind(gene_info, normalized_counts)
write.table(normalized_data, "result_TMM.txt", sep = "\t", row=F,col=T,quo=F)
```
