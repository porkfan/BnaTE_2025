# 7. TE-eQTL

## 7.1 Genotype file preprocess

After a series of processing steps to obtain the genotype input file required by QTLtools

```bash
vcftools --vcf ${genotype_file}  --keep ${id_f} --maf 0.05 --min-alleles 2 --max-alleles 2 --recode --recode-INFO-all --out ${work_dir}/${genotype_prefix}\_maf0.05

python het_filter.py -i ${work_dir}/${genotype_prefix}\_maf0.05.sorted.vcf -m 0.05 -c 0.5 -o ${work_dir}/${genotype_prefix}\_maf0.05_het0.5

bgzip -d ${work_dir}/${genotype_prefix}\_maf0.05_het0.5.vcf.gz

bgzip ${work_dir}/${genotype_prefix}\_maf0.05_het0.5.vcf && tabix -p vcf ${work_dir}/${genotype_prefix}\_maf0.05_het0.5.vcf.gz

plink --vcf ${work_dir}/${genotype_prefix}\_maf0.05_het0.5.vcf.gz --threads 4 --allow-extra-chr --make-bed --out ${work_dir}/${genotype_prefix}
```

## 7.2 Gene express file preprocess

After a series of processing steps to obtain the expression input file required by QTLtools

```bash
bgzip ${work_dir}/${express_file} && tabix -p bed ${work_dir}/${express_file}.gz

QTLtools pca --bed ${work_dir}/${express_file}.gz --out ${work_dir}/${genotype_prefix}

cat ${work_dir}/${genotype_prefix}.pca |head -n 11 > ${work_dir}/${genotype_prefix}_top10.pca

bgzip ${work_dir}/${genotype_prefix}_top10.pca

```

## 7.3 TE-cis-eQTL

Perform cis-eQTL analysis using the cis parameter in QTLtools

```bash
QTLtools cis --vcf ${work_dir}/${genotype_prefix}\_maf0.05_het0.5.vcf.gz --bed Bna_TMM.bed.gz --cov ${work_dir}/${genotype_prefix}_top10.pca --nominal 1 --window 1000000 --std-err --out 01.cis/cis.nominal
```

## 7.4 TE-trans-eQTL

Perform trans-eQTL analysis using the trans parameter in QTLtools

```bash
QTLtools trans --vcf ${work_dir}/${genotype_prefix}\_maf0.05_het0.5.vcf.gz --bed Bna_TMM.bed.gz --cov ${work_dir}/${genotype_prefix}_top10.pca --nominal --threshold ${threshold} --window 1000000  --out 02.trans/trans.nominal
```

## 7.5 lead-eQTL analysis

plink clump

```bash
plink --bfile {f} --clump {gwas_f} --clump-snp-field var_id --clump-field nom_pval --clump-kb 100000 --clump-p1 ${threshold} --clump-r2 0.8 --out {clump_pre}
```
