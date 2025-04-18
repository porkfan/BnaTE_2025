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