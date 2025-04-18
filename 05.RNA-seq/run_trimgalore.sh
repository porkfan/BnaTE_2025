module load TrimGalore/0.6.6
sample=$1
trim_galore --paired --quality 20 -a AGATCGGAAGAGC -a2 AGATCGGAAGAGC --length 20 -o 01_trim/20DAF_seed/  raw_data/20DAF_seed/${sample}_1.fq.gz raw_data/20DAF_seed/${sample}_2.fq.gz