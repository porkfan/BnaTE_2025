import pandas as pd
import subprocess
import os
import sys

def run_cis_trans_plink_clump(f, gi):
    gwas_f = f"02.tmp_cis_trans_depth/{gi}_cis_trans_significant.nominal.txt"
    clump_pre = f"02.tmp_cis_trans_depth/{gi}"
    clumped_file = f"{clump_pre}.clumped"

    cmd = f"plink --bfile {f} --clump {gwas_f} --clump-snp-field var_id --clump-field nom_pval --clump-kb 100000 --clump-p1 6.34e-6 --clump-r2 0.8 --out {clump_pre}"
    subprocess.call(cmd, shell=True)


# 主程序开始
infile1 = sys.argv[1]
infile2 = sys.argv[2]
f = sys.argv[3]
chri = sys.argv[4]


# 读取数据文件
dat1 = pd.read_csv(infile1, sep='\t')
dat2 = pd.read_csv(infile2, sep='\t')
genes1 = set(dat1.loc[dat1['phe_chr'] == int(chri), 'phe_id'].drop_duplicates())
genes2 = set(dat2.loc[dat2['phe_chr'] == int(chri), 'phe_id'].drop_duplicates())

all_genes = genes1.union(genes2)

# 循环处理每个唯一基因
for gi in all_genes:
    run_cis_trans_plink_clump(f, gi)
