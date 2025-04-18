# Function to process the 10th and onward columns in the VCF file
def process_columns(line):
    columns = line.strip().split('\t')
    # Process from the 10th column onwards
    for i in range(9, len(columns)):
        if columns[i] == '.':
            columns[i] = '.|.'
        elif columns[i].isdigit():
            columns[i] = f"{columns[i]}|{columns[i]}"
    return '\t'.join(columns)

# Read the VCF file and apply the processing
def modify_vcf_file(input_file_path, output_file_path):
    with open(input_file_path, 'r') as file:
        lines = file.readlines()
    
    with open(output_file_path, 'w') as file:
        for line in lines:
            if line.startswith('#'):
                # Write header lines to the new file as is
                file.write(line)
            else:
                # Write processed lines to the new file
                file.write(process_columns(line) + '\n')

# Specify the input and output file paths
input_vcf_path = 'Brassica_napus14-pg.raw_r100kb_fil_0.5missing.vcf'  # Replace with your file's path
output_vcf_path = 'Brassica_napus14-pg.raw_r100kb_fil_0.5missing_phased.vcf'  # Replace with your desired output path

# Call the function to modify the VCF file
modify_vcf_file(input_vcf_path, output_vcf_path)

