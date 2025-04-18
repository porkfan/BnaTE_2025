# 5. Obtain TE genotypes for the graph pangenome and 2311 populations using SV genotypes from 2311 populations and TE annotations from each genome in the graph

## 5.1 Use halLiftover to perform coordinate conversion based on the graph pangenome's hal file

```bash
singularity exec cactus_v2.6.8.sif halLiftover Brassica_napus14-pg.full.hal ${genome_1} ${bed_1} ${genome_2} ${bed_2}
```

## 5.2 Convert SV genotypes to corresponding TE genotypes based on the overlap between population SV and TE annotation information

```bash
python TE_SV_overlap.py
```
