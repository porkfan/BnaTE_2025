import sys

def filter_rows(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            # Check if it's a title line (starts with a single '#')
            if line.startswith('#') and not line.startswith('##'):
                outfile.write(line)
                continue

            # Process other lines that are not comment lines
            if not line.startswith('##'):
                columns = line.strip().split('\t')
                if len(columns) > 7:  # Ensuring that there are enough columns
                    info = columns[7]
                    snp_info = info.split(';')[-1].split(',')

                    # Checking each part in the snp_info array
                    for item in snp_info:
                        last_part = item.split('-')[-1]  # Getting the last part after splitting by '-'
                        if last_part.isdigit() and int(last_part) >= 50:
                            outfile.write(line)
                            break  # Exit the loop after meeting the condition and writing the line

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python keep_sv_vcf.py <input_file> <output_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    filter_rows(input_file, output_file)

