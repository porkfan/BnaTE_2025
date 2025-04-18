def filter_and_process_alt(input_file_path, output_file_path):
    with open(input_file_path, 'r') as file:
        lines = file.readlines()

    processed_lines = []

    for line in lines:
        if not line.startswith('#'):  # Skip header lines
            columns = line.strip().split('\t')
            ref = columns[3]
            alt = columns[4]

            # Skip lines with any 'N' in either REF or ALT columns
            if 'N' in ref or 'N' in alt:
                continue
            else:
                # Include lines without 'N's in both REF and ALT columns
                processed_lines.append('\t'.join(columns))
        else:
            # Include header lines without modification
            processed_lines.append(line.strip())

    # Write the processed lines to the output file
    with open(output_file_path, 'w') as file:
        for line in processed_lines:
            file.write(line + '\n')

input_vcf_path = 'Brassica_napus14-pg.raw_r100kb_fil_0.5missing_phased.vcf'  # Replace with the path to your input VCF file
output_vcf_path = 'Brassica_napus14-pg.raw_r100kb_fil_0.5missing_phased_deleteN.vcf'  # Replace with the desired path for your output VCF file

filter_and_process_alt(input_vcf_path, output_vcf_path)

