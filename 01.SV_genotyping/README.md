# 2. Determination of the structural variant (SV) set in the graph-pangenome and genotyping SV in 2311 accessions

## 2.1 Determination of the structural variant (SV) set in the graph-pangenome

Remove bubbles larger than 100kb from raw.vcf using vcfbub

```bash
vcfbub -r 100000 Brassica_napus14-pg.raw.vcf > Brassica_napus14-pg.raw_r100kb.vcf
```

Keep only non-overlapping bubbles with minimum LV using script

```bash
python filter_outmost_bubble.py Brassica_napus14-pg.raw_r100kb.vcf Brassica_napus14-pg.raw_r100kb_fil.vcf
```

After a series of filtering steps to obtain the graph-genome SV set for PanGenie index construction

```bash
### Filter variants with too many missing values
python filter_missing.py Brassica_napus14-pg.raw_r100kb_fil.vcf Brassica_napus14-pg.raw_r100kb_fil_0.5missing.vcf 4
### Convert all genotypes to homozygous format (1->1|1, .->.|., 0->0|0, N->N|N)
python phase.py
### Remove sequences containing N in variants
python delete_N.py
### Remove alternative alleles not covered by any haplotype
bcftools view --trim-alt-alleles Epi_Brassica_napus14-pg.raw_r100kb_fil_0.5missing_phased_deleteN > Epi_Brassica_napus14-pg.raw_r100kb_fil_0.5missing_phased_deleteN_trim.vcf
### Decompose and annotate bubbles using annotate_vcf.py
python annotate_vcf.py -vcf Brassica_napus14-pg.raw_r100kb_fil_0.5missing_phased_deleteN_trim.vcf -gfa Brassica_napus14-pg.gfa  -o Epi_Brassica_napus14-pg.raw_r100kb_fil_0.5missing_phased_deleteN_trim_id
### Filter rows where alt column is '.' using filter_vcf.py
python filter_vcf.py
Brassica_napus14-pg.raw_r100kb_fil_0.5missing_phased_deleteN_id_trim.vcf -> Brassica_napus14-pg.raw_r100kb_fil_0.5missing_phased_deleteN_trim_id_filter.vcf
### Extract variants >50bp (includes some <50bp variants in multi-allelic cases with SVs)
python keep_sv_vcf.py  Brassica_napus14-pg.raw_r100kb_fil_0.5missing_phased_deleteN_trim_id_filter.vcf  Epi_Brassica_napus14-pg.raw_r100kb_fil_0.5missing_phased_deleteN_trim_id_filter_SV.vcf
```

## 2.2 Build the graph-genome index by PanGenie

```bash
module load Singularity/3.7.3
singularity exec pangenie.sif  PanGenie-index -v  Brassica_napus14-pg.raw_r100kb_fil_0.5missing_phased_deleteN_trim_id_filter_SV.vcf  -r Brassica_napus.ZS11.v0.genome.fa  -t 20 -o PanGenie
```

## 2.3 SV genotyping in 2311 accessions

```bash
cat sample_2311.txt|while read sample;do
bsub -J PanGenie_${sample} -q normal -n 4 -R span[hosts=1] -o genotype_log/${sample}.out -e genotype_log/${sample}.err "sh PanGenie.sh ${sample}"
done

tmp_dir="tmp" # Temporary directory
output_dir="2311pop_pangenie" # Output directory

# Create temporary directory
mkdir -p ${tmp_dir}
mkdir -p ${output_dir}

# Merge paired-end data and decompress to fq file
zcat ${input_dir}/${sample}_1_clean.fq.gz  ${input_dir}/${sample}_2_clean.fq.gz > ${tmp_dir}/${sample}.fq

# Execute PanGenie
PanGenie -f PanGenie -i ${tmp_dir}/${sample}.fq -o ${output_dir}/${sample} -s ${sample} -j 4 -t 4

# Remove temporary fq file after completion
rm ${tmp_dir}/${sample}.fq
```

## 2.4 convert-to-biallelic

convert-to-biallelic.py

```bash
cat 2311pop_pangenie/${sample}_genotyping.vcf |python3 convert-to-biallelic.py  Brassica_napus14-pg.raw_r100kb_fil_0.5missing_phased_deleteN_trim_id_biallelic.vcf  > 2311pop_pangenie/${sample}_genotyping_biallelic.vcf
```
