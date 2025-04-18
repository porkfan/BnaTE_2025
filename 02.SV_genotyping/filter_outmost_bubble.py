import pysam
import sys
import os

def split_vcf_by_lv(input_vcf, output_vcf):
    # # Construct output filename
    # file_name, file_ext = os.path.splitext(input_vcf)
    # output_vcf = f"{file_name}.outmost{file_ext}"

    # Open input VCF file
    vcf_in = pysam.VariantFile(input_vcf)
    # Create a dictionary to store IDs corresponding to different LV values
    LV_dict = {}  # {lv: {id: True,},}

    # Iterate through each record in the VCF file
    for record in vcf_in.fetch():
        # Get LV value
        lv_value = record.info.get('LV')
        id_ = record.id

        if lv_value not in LV_dict:
            LV_dict[lv_value] = {id_: "a"}
        else:
            LV_dict[lv_value][id_] = "a"

    # Open output VCF file
    with open(output_vcf, 'w') as f2:
        # Write header
        f2.write(str(vcf_in.header))

        # Initialize variables
        last_lv = None
        last_PS = None
        write = False

        # Iterate through each record in the VCF file and filter based on whether PS exists in the previous LV dictionary
        for record in vcf_in.fetch():
            # Get LV value
            lv_value = record.info.get('LV')
            PS = record.info.get('PS', 'NA')
            id_ = record.id

            # If lv=0, write directly and update current state
            if lv_value == 0:
                write = True
                last_lv = lv_value
                last_PS = id_
            elif last_lv == lv_value and last_PS == PS:
                pass
            else:
                back_lv = lv_value - 1
                write = False
                try:
                    if LV_dict[back_lv][PS] == "a":
                        pass
                except:
                    write = True
                last_lv = lv_value
                last_PS = PS

            if write:
                f2.write(str(record))

    print(f"Output file: {output_vcf}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <input_vcf> <output_vcf>")
        sys.exit(1)

    input_vcf = sys.argv[1]
    output_vcf = sys.argv[2]
    split_vcf_by_lv(input_vcf, output_vcf)

