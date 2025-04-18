# 6. TE-GWAS

Generate kinship matrix and PCA results

```bash
module load gcta/1.94.1
module load gemma/0.98.5

f=${phenotype}
gcta --bfile $f --autosome --make-grm --out $f
gcta --grm $f --pca 10 --out $f_pca10
awk '{print "1\t"$3"\t"$4"\t"$5}' ${f}_pca10.eigenvec > ${f}_pca3_cov.txt
cut -f2 ${f}_pca3_cov.txt > tmp.txt
gemma -bfile ${f} -gk 2 -o ${f} -p tmp.txt
```

Perform GWAS using GEMMA

```bash
module load gemma/0.98.5
i=$1
cpu=4
f=${phenotype}
grm=${phenotype}
q=${phenotype}_pca10.eigenvec

mkdir -p gemma_output/${i}

cd gemma_output/${i}
awk -F '\t' '{print $3}' /${i}.txt > ${i}.phe.tmp
gemma -bfile $f -gk 2 -p ${i}.phe.tmp -o ${i}
gemma -bfile $f -k output/${i}.sXX.txt -p ${i}.phe.tmp -lmm 1 -c $q -o ${i}_gemma

```
