import sys

# Check if enough command line arguments are provided
if len(sys.argv) < 3:
    print("Usage: python script.py <input_vcf> <output_vcf> <max_missing_count>")
    sys.exit(1)

# Read input filename, output filename and maximum missing count from command line arguments
input_vcf = sys.argv[1]
output_vcf = sys.argv[2]
max_missing_count = int(sys.argv[3])  # Convert the provided maximum missing count parameter to integer

# Read input file
with open(input_vcf, 'r') as file:
    lines = file.readlines()

# Keep all lines starting with #
filtered_lines = [line for line in lines if line.startswith('#')]

# Process each line that doesn't start with #
for line in lines:
    if not line.startswith('#'):
        # Count the number of "." in columns from the 10th column onwards
        if line.split('\t')[9:].count('.') < max_missing_count:  # Use the provided maximum missing count parameter
            filtered_lines.append(line)

# Write filtered lines to new file
with open(output_vcf, 'w') as file:
    for line in filtered_lines:
        file.write(line)

