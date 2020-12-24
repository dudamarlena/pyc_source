# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/deeparg/deepARG-old.py
# Compiled at: 2020-04-23 22:10:14
import predict.bin.deepARG as clf, sys, os
iden = 50
evalue = 1e-10
minCoverage = 0.8
numAlignmentsPerEntry = 1000
pipeline = 'reads'
version = 'v2'
opts, args = getopt.getopt(sys.argv[1:], 'hi:o:', ['predict', 'align', 'genes', 'reads',
 'v1', 'type=', 'input=', 'output=', 'iden=', 'prob=', 'evalue=', 'coverage=', 'nk='])
options = {}
for opt, arg in opts:
    if opt == '-h' or opt == '--help':
        print '\n                DeepARG:\n                    https://bitbucket.org/gusphdproj/deeparg-ss\n\n                    A deep learning based approach for predicting Antibiotic Resistance Genes and annotation.\n                    You can use --predict if you already have a blast-like tabular output (outfmt6) from any\n                    other program (blast, userarch, vsearch, diamond, etc.). Here you can use the --reads options\n                    that will predict NGS reads or --genes that will take longer gene-like sequences (NOT ASSEMBLED CONTIGS).\n                    If you use the --align flag, the system will first perform blast over the input you provide\n                    (genes or reads) and continue with the predict stage. There are additional parameter such as idenity (60% default)\n                    or prediction probability to retrieve the most significant predictions (default --prob 0.8).\n\n                USAGE:  python deepARG.py --predict --reads --input /Volumes/data/dev/deepARG/test/test.tsv --output /Volumes/data/dev/deepARG/test/test.out\n                        python deepARG.py --align --genes --type prot --input /Volumes/data/dev/deepARG/test/test.fasta --output /Volumes/data/dev/deepARG/test/test.out\n\n                General options:\n                    --type          (nucl/prot) Molecule type of input data\n                    --iden          (50% default) minimum percentaje of identity to consider\n                    --prob          (0.8 default) Significance of the prediction, default 0.8\n                    --evalue        (1e-10 default) evalue of alignments (default 1e-10)\n                    --coverage      (0.8 default) minimum coverage of the alignment (alignment_length/reference_gene_length)\n                    --reads         short sequences version\n                    --genes         long sequences version\n                    --v1            Use this flag to activate deepARG version v1 [default: v2]\n\n                Optional:\n                    --nk            (1000 default) maximum number of alignments reported for each query (diamond alignment)\n\n\n                PREDICT ARG-like sequences using blast output file as input:\n                    deepARG --predict --input <inputfile> --output <outputfile>\n                        --input         blast tab delimited file.\n                        --output        output of annotated reads.\n\n                ALIGN sequences to DEEP_ARGDB and PREDICT ARGs using fasta files as input:\n                    deepARG --align  --input <inputfile> --output <outputfile>\n                        --input         fasta file containing reads.\n                        --output        blast tab delimited alignment file.\n\n                Thanks for using DeepARG\n                '
        sys.exit()
    else:
        options[opt.replace('--', '')] = arg

if 'genes' in options:
    mdl = '_LS'
    iden = 30
    evalue = 1e-10
    prob = 0.8
    minCoverage = 0.8
    pipeline = 'genes'
if 'reads' in options:
    mdl = '_SS'
    iden = 60
    evalue = 1e-05
    prob = 0.8
    minlen = 0.8
    minCoverage = 30
    pipeline = 'reads'
if 'v1' in options:
    print 'Using deepARG models Version 2'
    version = 'v1'
try:
    iden = float(options['iden'])
except:
    pass

try:
    evalue = float(options['evalue'])
except:
    pass

try:
    prob = float(options['prob'])
except:
    pass

try:
    minCoverage = float(options['coverage'])
except:
    pass

try:
    numAlignmentsPerEntry = int(options['nk'])
except:
    pass

if 'type' in options:
    if options['type'] == 'prot':
        aligner = 'blastp'
    if options['type'] == 'nucl':
        aligner = 'blastx'
if 'predict' in options:
    clf.process(options['input'], options['output'], iden, mdl, evalue, prob, minCoverage, pipeline, version)
if 'align' in options:
    print 'DIAMOND ' + aligner + ' alignment'
    os.system((' ').join([gopt.path + '/bin/diamond ', aligner,
     '-q', options['input'],
     '-d', gopt.path + '/database/' + version + '/features',
     '-k', str(numAlignmentsPerEntry),
     '--id', str(iden),
     '--sensitive',
     '-e', str(evalue),
     '-a', options['output'] + '.align']))
    print 'parsing output file'
    os.system((' ').join([
     gopt.path + '/bin/diamond view',
     '-a', options['output'] + '.align.daa',
     '-o', options['output'] + '.align.daa.tsv']))
    clf.process(options['output'] + '.align.daa.tsv', options['output'] + '.mapping', iden, mdl, evalue, prob, minCoverage, pipeline, version)