library(edgeR)
data=read.table("read_counts.txt", header = TRUE)
# Extract sample columns
gene_info <- data[, 1:6] # First six columns are gene information
counts_matrix <- data[, 7:ncol(data)]
# Create DGEList object
dge <- DGEList(counts = counts_matrix)
# Perform TMM normalization
dge <- calcNormFactors(dge)
# View normalized data
normalized_counts <- cpm(dge, log = TRUE)
# Merge gene information with normalized data
normalized_data <- cbind(gene_info, normalized_counts)
write.table(normalized_data, "result_TMM.txt", sep = "\t", row=F,col=T,quo=F)