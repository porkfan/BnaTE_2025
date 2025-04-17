# 7. TE-eQTL

## 7.1 TE-cis-eQTL

```bash
QTLtools cis --vcf arabidopsis.impute.maf0.05.mis0.5.recode.vcf.gz --bed Bna_TMM.bed.gz --cov PCA_top_10.pca.gz --nominal 1 --window 1000000 --std-err --out 02.nominal/cis.nominal
```

## 7.2 TE-trans-eQTL

```bash
QTLtools trans --vcf arabidopsis_impute_maf0.05.het0.5.recode.vcf.gz --bed Bna_TMM.bed.gz --cov PCA_10.pca.gz --nominal --threshold ${threshold} --window 1000000  --out 02.result/trans.nominal
```
