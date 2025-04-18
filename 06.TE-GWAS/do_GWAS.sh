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