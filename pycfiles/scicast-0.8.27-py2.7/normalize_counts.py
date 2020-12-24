# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/scicast/normalize_counts.py
# Compiled at: 2016-10-27 15:17:15
from rpy2.robjects.packages import SignatureTranslatedAnonymousPackage
import rpy2.robjects as robjects
from rpy2.robjects.packages import importr
from rpy2 import rinterface as ri
from rpy2.rinterface import RRuntimeError
import os

def normalize(file_path, base_name, edgeR=True, DESeq2=True):
    try:
        rpack = importr('edgeR')
    except RRuntimeError:
        base = importr('base')
        base.source('http://www.bioconductor.org/biocLite.R')
        biocinstaller = importr('BiocInstaller')
        biocinstaller.biocLite('edgeR')

    try:
        rpack = importr('DESeq2')
    except RRuntimeError:
        base = importr('base')
        base.source('http://www.bioconductor.org/biocLite.R')
        biocinstaller = importr('BiocInstaller')
        biocinstaller.biocLite('DESeq2')

    funcs_string = '\n    run_deseq2 <- function(path_to_file, file_base_name, group1_terms, group1_name, group2_terms, group2_name){\n    library(DESeq2)\n    raw.data <- read.csv(file = path_to_file, header=TRUE, sep="\t", row.names=1)\n    counts <- raw.data[ , -c(1,ncol(raw.data)) ]\n    rownames(counts) <- row.names(raw.data)\n    group <- c()\n    for (x in colnames( counts )){if(grepl(group1_terms,x)){ group <- append(group, group1_name)} else if(grepl(group2_terms,x)){ group <- append(group,group2_name)} }\n    samples <- data.frame(row.names=colnames(counts), condition=as.factor(c(group)))\n    dds <- DESeqDataSetFromMatrix(countData = counts, colData=samples, design=~condition)\n    dds <- dds[ rowSums(counts(dds)) > 1, ]\n    dds <- DESeq(dds)\n    dds <- estimateSizeFactors(dds)\n    dds <- estimateDispersions(dds)\n    dds <- nbinomWaldTest(dds)\n    matrix <- counts(dds,normalized=TRUE)\n\n    write.table(matrix, file=paste(dirname(path_to_file),paste("DESeq2", file_base_name,"matrix_norm.txt",sep=\'_\'),sep=\'/\'), sep="\t", col.names=NA)\n    saveRDS(dds, paste(save_name,".rds"))\n    plotDispEsts(dds)\n    return(dds)}\n\n    run_edgeR <- function(path_to_file,file_base_name){\n    library(edgeR)\n    raw.data <- read.csv(file = file_path, header=TRUE, sep="\t", row.names=1)\n    counts <- raw.data[ , -c(1,ncol(raw.data)) ]\n    rownames( counts ) <- row.names(raw.data)\n    cds <- DGEList( counts , group = colnames(counts) )\n    cds <- cds[rowSums(1e+06 * cds$counts/expandAsMatrix(cds$samples$lib.size, dim(cds)) > 1) >= 3, ]\n    cds <- calcNormFactors(cds, method="TMM")\n    cps <- cpm(cds, normalized.lib.sizes=TRUE)\n    write.table(cps, file=paste(dirname(path_to_file),paste(file_base_name,"normalized_edgR_cpm.txt",sep=\'_\'),sep=\'/\'), sep="\t", col.names=NA)\n    }\n    '
    normalize = SignatureTranslatedAnonymousPackage(funcs_string, 'normalize')
    dirname = os.path.dirname(file_path)
    robjects.r.assign('dirname', dirname)
    robjects.r.assign('base_name', base_name)
    robjects.r.assign('file_path', file_path)
    robjects.globalenv['file_path'] = file_path
    robjects.globalenv['base_name'] = base_name
    group1_terms = ['ctrl1']
    group1_name = ['all']
    group2_terms = ['low']
    group2_name = ['low']
    if edgeR:
        normalize.run_edgeR(file_path, base_name)
    if DESeq2:
        dds = normalize.run_deseq2(file_path, base_name, robjects.vectors.StrVector(group1_terms), robjects.vectors.StrVector(group1_name), robjects.vectors.StrVector(group2_terms), robjects.vectors.StrVector(group2_name))


normalize('/Users/iandriver/Documents/count-picard_Pdgfra_ctrl/pdgfra_ctrl_only_count_table.txt', 'pdgfra_test1', DESeq2=False)