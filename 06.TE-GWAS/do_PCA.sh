module load gcta/1.94.1
module load gemma/0.98.5

f=${phenotype}
gcta --bfile $f --autosome --make-grm --out $f
gcta --grm $f --pca 10 --out $f_pca10
awk '{print "1\t"$3"\t"$4"\t"$5}' ${f}_pca10.eigenvec > ${f}_pca3_cov.txt
cut -f2 ${f}_pca3_cov.txt > tmp.txt
gemma -bfile ${f} -gk 2 -o ${f} -p tmp.txt