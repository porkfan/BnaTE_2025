# 5. TE-GWAS

```bash
module load cta/1.94.1
gcta --bfile ${phenotype} --autosome --make-grm --out ${phenotype}
gcta --grm ${phenotype} --pca 10 --out ${phenotype}_pca10
awk '{print "1\t"$3"\t"$4"\t"$5}' ${phenotype}_pca10.eigenvec > ${phenotype}_pca3_cov.txt
cut -f2 ${phenotype}_pca3_cov.txt > tmp.txt
gemma -bfile ${phenotype} -gk 2 -o ${phenotype} -p tmp.txt

```

```bash
module load gcta/1.94.1
i=$1
cpu=4
f=${phenotype}
grm=${phenotype}
q=${phenotype}_pca10.eigenvec

gcta --mlma --bfile $f --grm $grm --pheno ${i}.txt --qcovar $q --out GCTA_out_2017/${i}_gcta --thread-num $cpu
```
