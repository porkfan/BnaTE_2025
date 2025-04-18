import pandas as pd
import argparse

def read_gff(file_path):
    """Reads a GFF file into a pandas DataFrame"""
    columns = ['seqid', 'source', 'type', 'start', 'end', 'score', 'strand', 'phase', 'attributes']
    gff_df = pd.read_csv(file_path, sep='\t', comment='#', names=columns)
    return gff_df

def read_te_info(file_path):
    """Reads the TE information file into a pandas DataFrame"""
    columns = ['TE_split_ID', 'TE_type', 'chr', 'TE_start', 'TE_end', 'TE_strand', 'TE_family', 'TE_genotype_ID']
    te_df = pd.read_csv(file_path, sep='\t', header=None, names=columns)
    return te_df

def parse_attributes(attributes):
    """Parses the attributes column in the GFF file into a dictionary"""
    return dict(item.split('=') for item in attributes.split(';'))

def find_nearest_te(gene_df, te_df):
    """Finds the nearest TE for each gene"""
    results = []

    for _, gene in gene_df[gene_df['type'] == 'gene'].iterrows():
        gene_start = gene['start']
        gene_end = gene['end']
        gene_strand = gene['strand']
        gene_seqid = gene['seqid']

        gene_id = parse_attributes(gene['attributes']).get('ID')
        
        if not gene_id:
            print(f"Failed to parse gene ID from attributes: {gene['attributes']}")
            continue
        
        # Replacing T with G in gene_id for matching with exon's Parent attribute
        parent_id = gene_id.replace("G", "T")
        exons = gene_df[(gene_df['type'] == 'exon') & (gene_df['attributes'].str.contains(f"Parent={parent_id}"))]
        
        # Print gene ID and exon regions for debugging
        #print(f"Gene ID: {gene_id}")
        #print(f"Exon regions for gene {gene_id}:")
        for _, exon in exons.iterrows():
            print(f"Exon start: {exon['start']}, Exon end: {exon['end']}")

            te_candidates = te_df[(te_df['chr'] == gene_seqid) & (te_df['TE_strand'] == gene_strand)].copy()
        if te_candidates.empty:
            continue

        te_candidates.loc[:, 'distance'] = te_candidates.apply(
            lambda te: min(abs(te['TE_start'] - gene_end), abs(te['TE_end'] - gene_start)), axis=1)

        nearest_te = te_candidates.loc[te_candidates['distance'].idxmin()]

        overlap_type = "exon"
        for _, exon in exons.iterrows():
            if not (nearest_te['TE_end'] < exon['start'] or nearest_te['TE_start'] > exon['end']):
                overlap_type = "exon"
                break
        else:
            overlap_type = "intron"

        if nearest_te['TE_start'] <= gene_end and nearest_te['TE_end'] >= gene_start:
            distance = 0
        else:
            overlap_type = "upstream"
            distance = nearest_te['distance']

        results.append({
            'gene_id': gene_id,
            'nearest_te_id': nearest_te['TE_split_ID'],
            'overlap_type': overlap_type,
            'distance': distance
        })

    return pd.DataFrame(results)

def main():
    parser = argparse.ArgumentParser(description='Find nearest TE for each gene.')
    parser.add_argument('--gene_gff', type=str, required=True, help='Path to the gene GFF file')
    parser.add_argument('--te_info', type=str, required=True, help='Path to the TE info file')
    parser.add_argument('--output', type=str, required=True, help='Path to the output CSV file')

    args = parser.parse_args()

    gene_df = read_gff(args.gene_gff)
    te_df = read_te_info(args.te_info)

    nearest_te_df = find_nearest_te(gene_df, te_df)

    nearest_te_df.to_csv(args.output, index=False)
    print(f"Results saved to {args.output}")

if __name__ == "__main__":
    main()

