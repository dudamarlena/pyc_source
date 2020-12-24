# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/zga/zga.py
# Compiled at: 2020-05-10 08:51:47
# Size of source mod 2**32: 23856 bytes
import argparse, os.path, logging, shutil, subprocess, re
from Bio import SeqIO
import hashlib

def parse_args():
    parser = argparse.ArgumentParser(description='ZGA genome assembly and annotation pipeline')
    general_args = parser.add_argument_group(title='General options', description='')
    general_args.add_argument('-s', '--first-step', help='First step of the pipeline', default='qc', choices=[
     'qc', 'processing', 'assembling', 'check_genome', 'annotation'])
    general_args.add_argument('-l', '--last-step', help='Last step of the pipeline', default='annotation', choices=[
     'qc', 'processing', 'assembling', 'check_genome', 'annotation'])
    general_args.add_argument('-o', '--output-dir', required=True, help='Output directory')
    general_args.add_argument('--force', action='store_true', help='Overwrite output directory if exists')
    general_args.add_argument('-t', '--threads', type=int, default=1, help='Number of CPU threads to use (where possible)')
    general_args.add_argument('-m', '--memory-limit', type=int, help='Memory limit in GB for SPAdes')
    general_args.add_argument('--genus', default='Unknown', help='Provide genus if known')
    general_args.add_argument('--species', default='sp.', help='Provide species if known')
    general_args.add_argument('--strain', help='Provide strain if known')
    general_args.add_argument('--transparent', action='store_true', help='Show output from tools inside the pipeline')
    general_args.add_argument('--domain', default='bacteria', choices=['archaea', 'bacteria'], help='Provide prokaryotic domain: bacteria or archaea')
    input_args = parser.add_argument_group(title='Input files and options', description='')
    input_args.add_argument('-1', '--pe-1', help='FASTQ file with first (left) paired-end reads')
    input_args.add_argument('-2', '--pe-2', help='FASTQ file with second (right) paired-end reads')
    input_args.add_argument('--pe-merged', help='FASTQ file  with merged overlapped paired-end reads')
    input_args.add_argument('-S', '--single-end', help='FASTQ file with unpaired or single-end reads')
    input_args.add_argument('--mp-1', help='Mate pair forward reads. SPAdes only')
    input_args.add_argument('--mp-2', help='Mate pair forward reads. SPAdes only')
    input_args.add_argument('--pacbio', help='PacBio reads')
    input_args.add_argument('--nanopore', help='Nanopore reads')
    reads_args = parser.add_argument_group(title='Setting for processing of reads')
    reads_args.add_argument('-q', '--quality-cutoff', type=int, default=25, help='Base quality cutoff for short reads')
    reads_args.add_argument('--adapters', help='Adapter sequences for trimming from short reads')
    reads_args.add_argument('--merge-with', default='bbmerge', choices=['bbmerge', 'seqprep'], help='Tool for merging overlapping paired-end reads: bbmerge (default) or seqprep')
    reads_args.add_argument('--filter-by-tile', action='store_true', help='Filter reads based on positional quality over a flowcell.')
    reads_args.add_argument('--use-unknown-mp', action='store_true', help='Include reads that are probably mate pairs (default: only known MP used)')
    asly_args = parser.add_argument_group(title='Assembly settings')
    asly_args.add_argument('-a', '--assembler', default='unicycler', choices=['spades', 'unicycler'], help='Assembler: unicycler (default, better quality, may use only long reads,) or spades (faster, may use mate-pair reads).')
    asly_args.add_argument('--no-correction', action='store_true', help='Disable read correction')
    asly_args.add_argument('--use-scaffolds', action='store_true', help='SPAdes: Use assembled scaffolds.')
    asly_args.add_argument('--spades-k-list', help="List of kmers for Spades, even comma-separated numbers e.g. '21,33,55,77'")
    asly_args.add_argument('--unicycler-mode', default='normal', choices=['conservative', 'normal', 'bold'], help='Mode of unicycler assembler: conservative, normal (default) or bold.')
    asly_args.add_argument('--linear-seqs', default=0, help='Expected number of linear sequences')
    asly_args.add_argument('--extract-replicons', action='store_true', help='Extract replicons (e.g. plasmids) from Unicycler assembly to separate files')
    check_args = parser.add_argument_group(title='Genome check settings')
    check_args.add_argument('--check-phix', action='store_true', help='Check genome for presence of PhiX control sequence.')
    check_args.add_argument('--checkm-mode', default='taxonomy_wf', choices=['taxonomy_wf', 'lineage_wf'], help='Select CheckM working mode. Default is checking for domain-specific marker-set.')
    check_args.add_argument('--checkm-rank', help="Rank of taxon for CheckM. Run 'checkm taxon_list' for details.")
    check_args.add_argument('--checkm-taxon', help="Taxon for CheckM. Run 'checkm taxon_list' for details.")
    check_args.add_argument('--checkm-full-tree', action='store_true', help='Use full tree for inference of marker set, requires LOTS of memory.')
    anno_args = parser.add_argument_group(title='Annotation settings')
    anno_args.add_argument('-g', '--genome', help='Genome assembly (when starting from annotation).')
    anno_args.add_argument('--gcode', default=11, type=int, help='Genetic code.')
    anno_args.add_argument('--locus-tag', help='Locus tag prefix. If not provided prefix will be generated from MD5 checksum.')
    anno_args.add_argument('--locus-tag-inc', default=10, type=int, help='Locus tag increment, default = 10')
    anno_args.add_argument('--center-name', help='Genome center name.')
    anno_args.add_argument('--minimum-length', help='Minimum sequence length in genome assembly.')
    return parser.parse_args()


def check_reads(args):
    reads = {}
    read_list = [
     args.pe_1, args.pe_2, args.single_end, args.pe_merged,
     args.mp_1, args.mp_2, args.pacbio, args.nanopore]
    logger.info('Checking input files.')
    for f in read_list:
        if f:
            os.path.isfile(f) or logger.error("File %s doesn't exist" % f)
            raise FileNotFoundError("File %s doesn't exist" % f)

    if args.pe_1 and args.pe_2:
        reads['pe_1'] = os.path.abspath(args.pe_1)
        reads['pe_2'] = os.path.abspath(args.pe_2)
    else:
        if not args.pe_1:
            if args.pe_2:
                logger.error('Single end reads provided as paired. Please use "--single-end" option')
                exit(1)
        elif args.mp_1 and args.mp_2:
            reads['mp_1'] = os.path.abspath(args.mp_1)
            reads['mp_2'] = os.path.abspath(args.mp_2)
        if args.pe_merged:
            reads['merged'] = os.path.abspath(args.pe_merged)
        if args.single_end:
            reads['single'] = os.path.abspath(args.single_end)
        if args.pacbio:
            reads['pacbio'] = os.path.abspath(args.pacbio)
        if args.nanopore:
            reads['nanopore'] = os.path.abspath(args.nanopore)
        return reads


def create_subdir(parent, child):
    path = os.path.join(parent, child)
    try:
        os.mkdir(path)
    except Exception as e:
        try:
            raise e(f"Impossible to create directory: {path}")
        finally:
            e = None
            del e

    return path


def run_external(args, cmd):
    logger.debug('Running: ' + ' '.join(cmd))
    if args.transparent:
        rc = subprocess.run(cmd).returncode
    else:
        rc = subprocess.run(cmd, stderr=(subprocess.PIPE), stdout=(subprocess.PIPE)).returncode
    if rc != 0:
        logger.error(f"""Non-zero return code of "{' '.join(cmd)}"""")
    return rc


def read_QC(args, reads):
    logger.info('Read quality control started')
    qcoutdir = create_subdir(args.output_dir, 'QC')
    cmd = ['fastqc', '-q', '-t', str(args.threads), '-o', qcoutdir] + list(reads.values())
    return run_external(args, cmd)


def filter_by_tile(args, reads, readdir):
    filtered_pe_r1 = os.path.join(readdir, 'filtered_pe_r1.fq.gz')
    filtered_pe_r2 = os.path.join(readdir, 'filtered_pe_r2.fq.gz')
    cmd = [
     'filterbytile.sh', f"in={reads[pe_1]}", f"in2={reads[pe_2]}",
     f"out={filtered_pe_r1}", f"out2={filtered_pe_r2}"]
    rc = run_external(args, cmd)
    if rc == 0:
        reads['pe_1'] = filtered_pe_r1
        reads['pe_2'] = filtered_pe_r2
    return reads


def merge_seqprep(args, reads, readdir):
    notmerged_r1 = os.path.join(readdir, 'nm.pe_1.fq.gz')
    notmerged_r2 = os.path.join(readdir, 'nm.pe_2.fq.gz')
    merged = os.path.join(readdir, 'merged.fq.gz')
    cmd = ['seqprep', '-f', reads['pe_1'], '-r', reads['pe_2'], '-1', notmerged_r1,
     '-2', notmerged_r2, '-s', merged]
    logger.info('Merging paired-end reads.')
    rc = run_external(args, cmd)
    if rc == 0:
        reads['merged'] = merged
        reads['pe_1'] = notmerged_r1
        reads['pe_2'] = notmerged_r2
    return reads


def merge_bb(args, reads, readdir):
    bb_trim = True
    bb_trimq = '10'
    notmerged_r1 = os.path.join(readdir, 'nm.pe_1.fq.gz')
    notmerged_r2 = os.path.join(readdir, 'nm.pe_2.fq.gz')
    merged = os.path.join(readdir, 'merged.fq.gz')
    cmd = ['bbmerge.sh', f"in1={reads['pe_1']}", f"in2={reads['pe_2']}",
     f"outu1={notmerged_r1}", f"outu2={notmerged_r2}", f"out={merged}"]
    if bb_trim:
        cmd += ['qtrim2=t', f"trimq={bb_trimq}"]
    logger.info('Merging paired-end reads.')
    rc = run_external(args, cmd)
    if rc == 0:
        reads['merged'] = merged
        reads['pe_1'] = notmerged_r1
        reads['pe_2'] = notmerged_r2
    return reads


def trim_and_filter_pe(args, reads, readdir):
    MINLEN = 55
    WINDOW = 3
    if 'pe_1' in reads.keys():
        if 'pe_2' in reads.keys():
            logger.info('Trimming and filtering paired end reads')
            out_pe1 = os.path.join(readdir, 'pe_1.fq')
            out_pe2 = os.path.join(readdir, 'pe_2.fq')
            cmd = ['fastq-mcf', '-H', '-X', '-q', str(args.quality_cutoff), '-l', str(MINLEN),
             '-w', str(WINDOW), '-o', out_pe1, '-o', out_pe2, args.adapters, reads['pe_1'], reads['pe_2']]
            rc = run_external(args, cmd)
            if rc == 0:
                reads['pe_1'] = out_pe1
                reads['pe_2'] = out_pe2
    if 'single' in reads.keys():
        logger.info('Trimming and filtering single end reads')
        out_single = os.path.join(readdir, 'single.fq')
        cmd = ['fastq-mcf', '-H', '-X', '-q', str(args.quality_cutoff), '-l', str(MINLEN),
         '-w', str(WINDOW), '-o', out_single, 'n/a', reads['single']]
        rc = run_external(args, cmd)
        if rc == 0:
            reads['single'] = out_single
    if 'merged' in reads.keys():
        logger.info('Trimming and filtering merged paired-end reads')
        out = os.path.join(readdir, 'merged.fq')
        cmd = ['fastq-mcf', '-H', '-X', '-q', str(args.quality_cutoff), '-l', str(MINLEN),
         '-w', str(WINDOW), '-o', out, 'n/a', reads['merged']]
        rc = run_external(args, cmd)
        if rc == 0:
            reads['merged'] = out
    return reads


def read_processing(args, reads):
    logger.info('Reads processing started')
    readdir = create_subdir(args.output_dir, 'reads')
    illumina_adapters = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data/illumina.adapters.fasta')
    if args.adapters and os.path.isfile(args.adapters):
        args.adapters = os.path.abspath(args.adapters)
    else:
        args.adapters = illumina_adapters
    if args.filter_by_tile:
        if 'pe_1' in reads.keys():
            if 'pe_2' in reads.keys():
                reads = filter_by_tile(args, reads, readdir)
    else:
        reads = trim_and_filter_pe(args, reads, readdir)
        if 'merged' not in reads.keys():
            if 'pe_1' in reads.keys():
                if 'pe_2' in reads.keys():
                    if args.merge_with == 'bbmerge':
                        reads = merge_bb(args, reads, readdir)
                    else:
                        reads = merge_seqprep(args, reads, readdir)
    if 'mp_1' in reads.keys():
        reads = mp_read_processing(args, reads, readdir)
    logger.info('Read processing finished')
    return reads


def mp_read_processing(args, reads, readdir):
    prefix = os.path.join(readdir, 'nxtrim')
    MINLENGTH = 31
    cmd = [
     'nxtrim', '-1', reads['mp_1'], '-2', reads['mp_2'], '--separate']
    cmd += ['--justmp', '-O', prefix, '-l', str(MINLENGTH)]
    rc = run_external(args, cmd)
    if args.use_unknown_mp:
        with open(f"{prefix}_R1.all.fastq.gz", 'wb') as (dest):
            with open(f"{prefix}_R1.mp.fastq.gz", 'rb') as (src):
                shutil.copyfileobj(src, dest)
            with open(f"{prefix}_R1.unknown.fastq.gz", 'rb') as (src):
                shutil.copyfileobj(src, dest)
        with open(f"{prefix}_R2.all.fastq.gz", 'wb') as (dest):
            with open(f"{prefix}_R2.mp.fastq.gz", 'rb') as (src):
                shutil.copyfileobj(src, dest)
            with open(f"{prefix}_R2.unknown.fastq.gz", 'rb') as (src):
                shutil.copyfileobj(src, dest)
        reads['mp_1'] = f"{prefix}_R1.all.fastq.gz"
        reads['mp_2'] = f"{prefix}_R2.all.fastq.gz"
    else:
        reads['mp_1'] = f"{prefix}_R1.mp.fastq.gz"
        reads['mp_2'] = f"{prefix}_R2.mp.fastq.gz"
    return reads


def assemble--- This code section failed: ---

 L. 327         0  LOAD_GLOBAL              logger
                2  LOAD_METHOD              info
                4  LOAD_STR                 'Assembling started'
                6  CALL_METHOD_1         1  '1 positional argument'
                8  POP_TOP          

 L. 328        10  LOAD_GLOBAL              os
               12  LOAD_ATTR                path
               14  LOAD_METHOD              join
               16  LOAD_FAST                'args'
               18  LOAD_ATTR                output_dir
               20  LOAD_STR                 'assembly'
               22  CALL_METHOD_2         2  '2 positional arguments'
               24  STORE_FAST               'aslydir'

 L. 330        26  LOAD_FAST                'args'
               28  LOAD_ATTR                assembler
               30  LOAD_STR                 'spades'
               32  COMPARE_OP               ==
            34_36  POP_JUMP_IF_FALSE   578  'to 578'

 L. 332        38  LOAD_STR                 'spades.py'
               40  LOAD_STR                 '-o'
               42  LOAD_FAST                'aslydir'
               44  LOAD_STR                 '--careful'
               46  LOAD_STR                 '-t'
               48  LOAD_GLOBAL              str
               50  LOAD_FAST                'args'
               52  LOAD_ATTR                threads
               54  CALL_FUNCTION_1       1  '1 positional argument'

 L. 333        56  LOAD_STR                 '--cov-cutoff'
               58  LOAD_STR                 'auto'
               60  BUILD_LIST_8          8 
               62  STORE_FAST               'cmd'

 L. 337        64  SETUP_EXCEPT        102  'to 102'

 L. 338        66  LOAD_GLOBAL              str
               68  LOAD_GLOBAL              subprocess
               70  LOAD_ATTR                run
               72  LOAD_STR                 'spades.py'
               74  LOAD_STR                 '-v'
               76  BUILD_LIST_2          2 
               78  LOAD_GLOBAL              subprocess
               80  LOAD_ATTR                PIPE

 L. 339        82  LOAD_GLOBAL              subprocess
               84  LOAD_ATTR                PIPE
               86  LOAD_CONST               True
               88  LOAD_CONST               ('stdout', 'stderr', 'universal_newlines')
               90  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
               92  LOAD_ATTR                stdout
               94  CALL_FUNCTION_1       1  '1 positional argument'
               96  STORE_FAST               'spades_version'
               98  POP_BLOCK        
              100  JUMP_FORWARD        150  'to 150'
            102_0  COME_FROM_EXCEPT     64  '64'

 L. 340       102  DUP_TOP          
              104  LOAD_GLOBAL              Exception
              106  COMPARE_OP               exception-match
              108  POP_JUMP_IF_FALSE   148  'to 148'
              110  POP_TOP          
              112  STORE_FAST               'e'
              114  POP_TOP          
              116  SETUP_FINALLY       136  'to 136'

 L. 341       118  LOAD_GLOBAL              logger
              120  LOAD_METHOD              error
              122  LOAD_STR                 'Failed to run "spades"'
              124  CALL_METHOD_1         1  '1 positional argument'
              126  POP_TOP          

 L. 342       128  LOAD_FAST                'e'
              130  RAISE_VARARGS_1       1  'exception instance'
              132  POP_BLOCK        
              134  LOAD_CONST               None
            136_0  COME_FROM_FINALLY   116  '116'
              136  LOAD_CONST               None
              138  STORE_FAST               'e'
              140  DELETE_FAST              'e'
              142  END_FINALLY      
              144  POP_EXCEPT       
              146  JUMP_FORWARD        150  'to 150'
            148_0  COME_FROM           108  '108'
              148  END_FINALLY      
            150_0  COME_FROM           146  '146'
            150_1  COME_FROM           100  '100'

 L. 344       150  LOAD_GLOBAL              re
              152  LOAD_METHOD              search
              154  LOAD_STR                 '[\\d\\.]+'
              156  LOAD_FAST                'spades_version'
              158  CALL_METHOD_2         2  '2 positional arguments'
              160  LOAD_CONST               0
              162  BINARY_SUBSCR    
              164  STORE_FAST               'version'

 L. 345       166  LOAD_GLOBAL              logger
              168  LOAD_METHOD              debug
              170  LOAD_STR                 'Spades version %s detected'
              172  LOAD_FAST                'version'
              174  BINARY_MODULO    
              176  CALL_METHOD_1         1  '1 positional argument'
              178  POP_TOP          

 L. 358       180  LOAD_FAST                'args'
              182  LOAD_ATTR                memory_limit
              184  POP_JUMP_IF_FALSE   204  'to 204'

 L. 359       186  LOAD_FAST                'cmd'
              188  LOAD_STR                 '-m'
              190  LOAD_GLOBAL              str
              192  LOAD_FAST                'args'
              194  LOAD_ATTR                memory_limit
              196  CALL_FUNCTION_1       1  '1 positional argument'
              198  BUILD_LIST_2          2 
              200  INPLACE_ADD      
              202  STORE_FAST               'cmd'
            204_0  COME_FROM           184  '184'

 L. 360       204  LOAD_STR                 'pe_1'
              206  LOAD_FAST                'reads'
              208  LOAD_METHOD              keys
              210  CALL_METHOD_0         0  '0 positional arguments'
              212  COMPARE_OP               in
              214  POP_JUMP_IF_FALSE   252  'to 252'
              216  LOAD_STR                 'pe_2'
              218  LOAD_FAST                'reads'
              220  LOAD_METHOD              keys
              222  CALL_METHOD_0         0  '0 positional arguments'
              224  COMPARE_OP               in
              226  POP_JUMP_IF_FALSE   252  'to 252'

 L. 361       228  LOAD_FAST                'cmd'
              230  LOAD_STR                 '-1'
              232  LOAD_FAST                'reads'
              234  LOAD_STR                 'pe_1'
              236  BINARY_SUBSCR    
              238  LOAD_STR                 '-2'
              240  LOAD_FAST                'reads'
              242  LOAD_STR                 'pe_2'
              244  BINARY_SUBSCR    
              246  BUILD_LIST_4          4 
              248  INPLACE_ADD      
              250  STORE_FAST               'cmd'
            252_0  COME_FROM           226  '226'
            252_1  COME_FROM           214  '214'

 L. 362       252  LOAD_STR                 'merged'
              254  LOAD_FAST                'reads'
              256  LOAD_METHOD              keys
              258  CALL_METHOD_0         0  '0 positional arguments'
              260  COMPARE_OP               in
          262_264  POP_JUMP_IF_FALSE   282  'to 282'

 L. 363       266  LOAD_FAST                'cmd'
              268  LOAD_STR                 '--merged'
              270  LOAD_FAST                'reads'
              272  LOAD_STR                 'merged'
              274  BINARY_SUBSCR    
              276  BUILD_LIST_2          2 
              278  INPLACE_ADD      
              280  STORE_FAST               'cmd'
            282_0  COME_FROM           262  '262'

 L. 364       282  LOAD_STR                 'single'
              284  LOAD_FAST                'reads'
              286  LOAD_METHOD              keys
              288  CALL_METHOD_0         0  '0 positional arguments'
              290  COMPARE_OP               in
          292_294  POP_JUMP_IF_FALSE   312  'to 312'

 L. 365       296  LOAD_FAST                'cmd'
              298  LOAD_STR                 '-s'
              300  LOAD_FAST                'reads'
              302  LOAD_STR                 'single'
              304  BINARY_SUBSCR    
              306  BUILD_LIST_2          2 
              308  INPLACE_ADD      
              310  STORE_FAST               'cmd'
            312_0  COME_FROM           292  '292'

 L. 366       312  LOAD_STR                 'mp_1'
              314  LOAD_FAST                'reads'
              316  LOAD_METHOD              keys
              318  CALL_METHOD_0         0  '0 positional arguments'
              320  COMPARE_OP               in
          322_324  POP_JUMP_IF_FALSE   364  'to 364'
              326  LOAD_STR                 'mp_2'
              328  LOAD_FAST                'reads'
              330  LOAD_METHOD              keys
              332  CALL_METHOD_0         0  '0 positional arguments'
              334  COMPARE_OP               in
          336_338  POP_JUMP_IF_FALSE   364  'to 364'

 L. 367       340  LOAD_FAST                'cmd'
              342  LOAD_STR                 '--mp1-1'
              344  LOAD_FAST                'reads'
              346  LOAD_STR                 'mp_1'
              348  BINARY_SUBSCR    
              350  LOAD_STR                 '--mp1-2'
              352  LOAD_FAST                'reads'
              354  LOAD_STR                 'mp_2'
              356  BINARY_SUBSCR    
              358  BUILD_LIST_4          4 
              360  INPLACE_ADD      
              362  STORE_FAST               'cmd'
            364_0  COME_FROM           336  '336'
            364_1  COME_FROM           322  '322'

 L. 368       364  LOAD_STR                 'nanopore'
              366  LOAD_FAST                'reads'
              368  LOAD_METHOD              keys
              370  CALL_METHOD_0         0  '0 positional arguments'
              372  COMPARE_OP               in
          374_376  POP_JUMP_IF_FALSE   394  'to 394'

 L. 369       378  LOAD_FAST                'cmd'
              380  LOAD_STR                 '--nanopore'
              382  LOAD_FAST                'reads'
              384  LOAD_STR                 'nanopore'
              386  BINARY_SUBSCR    
              388  BUILD_LIST_2          2 
              390  INPLACE_ADD      
              392  STORE_FAST               'cmd'
            394_0  COME_FROM           374  '374'

 L. 370       394  LOAD_STR                 'pacbio'
              396  LOAD_FAST                'reads'
              398  LOAD_METHOD              keys
              400  CALL_METHOD_0         0  '0 positional arguments'
              402  COMPARE_OP               in
          404_406  POP_JUMP_IF_FALSE   424  'to 424'

 L. 371       408  LOAD_FAST                'cmd'
              410  LOAD_STR                 '--pacbio'
              412  LOAD_FAST                'reads'
              414  LOAD_STR                 'pacbio'
              416  BINARY_SUBSCR    
              418  BUILD_LIST_2          2 
              420  INPLACE_ADD      
              422  STORE_FAST               'cmd'
            424_0  COME_FROM           404  '404'

 L. 372       424  LOAD_FAST                'args'
              426  LOAD_ATTR                no_correction
          428_430  POP_JUMP_IF_FALSE   442  'to 442'

 L. 373       432  LOAD_FAST                'cmd'
              434  LOAD_STR                 '--only-assembler'
              436  BUILD_LIST_1          1 
              438  INPLACE_ADD      
              440  STORE_FAST               'cmd'
            442_0  COME_FROM           428  '428'

 L. 374       442  LOAD_FAST                'args'
              444  LOAD_ATTR                spades_k_list
          446_448  POP_JUMP_IF_FALSE   464  'to 464'

 L. 375       450  LOAD_FAST                'cmd'
              452  LOAD_STR                 '-k'
              454  LOAD_FAST                'args'
              456  LOAD_ATTR                spades_k_list
              458  BUILD_LIST_2          2 
              460  INPLACE_ADD      
              462  STORE_FAST               'cmd'
            464_0  COME_FROM           446  '446'

 L. 377       464  LOAD_GLOBAL              run_external
              466  LOAD_FAST                'args'
              468  LOAD_FAST                'cmd'
              470  CALL_FUNCTION_2       2  '2 positional arguments'
              472  STORE_FAST               'rc'

 L. 379       474  LOAD_FAST                'rc'
              476  LOAD_CONST               0
              478  COMPARE_OP               !=
          480_482  POP_JUMP_IF_FALSE   528  'to 528'

 L. 380       484  LOAD_GLOBAL              logger
              486  LOAD_METHOD              error
              488  LOAD_STR                 'Genome assembly finished with errors.'
              490  CALL_METHOD_1         1  '1 positional argument'
              492  POP_TOP          

 L. 381       494  LOAD_GLOBAL              logger
              496  LOAD_METHOD              error
              498  LOAD_STR                 'Plese check %s for more information.'
              500  LOAD_GLOBAL              os
              502  LOAD_ATTR                path
              504  LOAD_METHOD              join
              506  LOAD_FAST                'aslydir'
              508  LOAD_STR                 'spades.log'
              510  CALL_METHOD_2         2  '2 positional arguments'
              512  BINARY_MODULO    
              514  CALL_METHOD_1         1  '1 positional argument'
              516  POP_TOP          

 L. 382       518  LOAD_GLOBAL              Exception
              520  LOAD_STR                 'Extermal software error'
              522  CALL_FUNCTION_1       1  '1 positional argument'
              524  RAISE_VARARGS_1       1  'exception instance'
              526  JUMP_FORWARD       1010  'to 1010'
            528_0  COME_FROM           480  '480'

 L. 384       528  LOAD_GLOBAL              logger
              530  LOAD_METHOD              debug
              532  LOAD_STR                 'Assembling finished'
              534  CALL_METHOD_1         1  '1 positional argument'
              536  POP_TOP          

 L. 385       538  LOAD_FAST                'args'
              540  LOAD_ATTR                use_scaffolds
          542_544  POP_JUMP_IF_FALSE   560  'to 560'

 L. 386       546  LOAD_GLOBAL              os
              548  LOAD_ATTR                path
              550  LOAD_METHOD              join
              552  LOAD_FAST                'aslydir'
              554  LOAD_STR                 'scaffolds.fasta'
              556  CALL_METHOD_2         2  '2 positional arguments'
              558  RETURN_VALUE     
            560_0  COME_FROM           542  '542'

 L. 388       560  LOAD_GLOBAL              os
              562  LOAD_ATTR                path
              564  LOAD_METHOD              join
              566  LOAD_FAST                'aslydir'
              568  LOAD_STR                 'contigs.fasta'
              570  CALL_METHOD_2         2  '2 positional arguments'
              572  RETURN_VALUE     
          574_576  JUMP_FORWARD       1010  'to 1010'
            578_0  COME_FROM            34  '34'

 L. 390       578  LOAD_FAST                'args'
              580  LOAD_ATTR                assembler
              582  LOAD_STR                 'unicycler'
              584  COMPARE_OP               ==
          586_588  POP_JUMP_IF_FALSE   996  'to 996'

 L. 392       590  SETUP_EXCEPT        622  'to 622'

 L. 393       592  LOAD_GLOBAL              subprocess
              594  LOAD_ATTR                run
              596  LOAD_STR                 'unicycler'
              598  LOAD_STR                 '--version'
              600  BUILD_LIST_2          2 

 L. 394       602  LOAD_GLOBAL              subprocess
              604  LOAD_ATTR                PIPE
              606  LOAD_GLOBAL              subprocess
              608  LOAD_ATTR                PIPE
              610  LOAD_CONST               ('stderr', 'stdout')
              612  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              614  LOAD_ATTR                stdout
              616  STORE_FAST               'version'
              618  POP_BLOCK        
              620  JUMP_FORWARD        672  'to 672'
            622_0  COME_FROM_EXCEPT    590  '590'

 L. 395       622  DUP_TOP          
              624  LOAD_GLOBAL              Exception
              626  COMPARE_OP               exception-match
          628_630  POP_JUMP_IF_FALSE   670  'to 670'
              632  POP_TOP          
              634  STORE_FAST               'e'
              636  POP_TOP          
              638  SETUP_FINALLY       658  'to 658'

 L. 396       640  LOAD_GLOBAL              logger
              642  LOAD_METHOD              critical
              644  LOAD_STR                 "Failed to run 'Unicycler'."
              646  CALL_METHOD_1         1  '1 positional argument'
              648  POP_TOP          

 L. 397       650  LOAD_FAST                'e'
              652  RAISE_VARARGS_1       1  'exception instance'
              654  POP_BLOCK        
              656  LOAD_CONST               None
            658_0  COME_FROM_FINALLY   638  '638'
              658  LOAD_CONST               None
              660  STORE_FAST               'e'
              662  DELETE_FAST              'e'
              664  END_FINALLY      
              666  POP_EXCEPT       
              668  JUMP_FORWARD        672  'to 672'
            670_0  COME_FROM           628  '628'
              670  END_FINALLY      
            672_0  COME_FROM           668  '668'
            672_1  COME_FROM           620  '620'

 L. 399       672  LOAD_STR                 'unicycler'
              674  LOAD_STR                 '-o'
              676  LOAD_FAST                'aslydir'
              678  LOAD_STR                 '-t'
              680  LOAD_GLOBAL              str
              682  LOAD_FAST                'args'
              684  LOAD_ATTR                threads
              686  CALL_FUNCTION_1       1  '1 positional argument'
              688  BUILD_LIST_5          5 
              690  STORE_FAST               'cmd'

 L. 400       692  LOAD_STR                 'pe_1'
              694  LOAD_FAST                'reads'
              696  LOAD_METHOD              keys
              698  CALL_METHOD_0         0  '0 positional arguments'
              700  COMPARE_OP               in
          702_704  POP_JUMP_IF_FALSE   744  'to 744'
              706  LOAD_STR                 'pe_2'
              708  LOAD_FAST                'reads'
              710  LOAD_METHOD              keys
              712  CALL_METHOD_0         0  '0 positional arguments'
              714  COMPARE_OP               in
          716_718  POP_JUMP_IF_FALSE   744  'to 744'

 L. 401       720  LOAD_FAST                'cmd'
              722  LOAD_STR                 '-1'
              724  LOAD_FAST                'reads'
              726  LOAD_STR                 'pe_1'
              728  BINARY_SUBSCR    
              730  LOAD_STR                 '-2'
              732  LOAD_FAST                'reads'
              734  LOAD_STR                 'pe_2'
              736  BINARY_SUBSCR    
              738  BUILD_LIST_4          4 
              740  INPLACE_ADD      
              742  STORE_FAST               'cmd'
            744_0  COME_FROM           716  '716'
            744_1  COME_FROM           702  '702'

 L. 402       744  LOAD_FAST                'args'
              746  LOAD_ATTR                no_correction
          748_750  POP_JUMP_IF_FALSE   762  'to 762'

 L. 403       752  LOAD_FAST                'cmd'
              754  LOAD_STR                 '--no_correct'
              756  BUILD_LIST_1          1 
              758  INPLACE_ADD      
              760  STORE_FAST               'cmd'
            762_0  COME_FROM           748  '748'

 L. 404       762  LOAD_STR                 'merged'
              764  LOAD_FAST                'reads'
              766  LOAD_METHOD              keys
              768  CALL_METHOD_0         0  '0 positional arguments'
              770  COMPARE_OP               in
          772_774  POP_JUMP_IF_FALSE   794  'to 794'

 L. 405       776  LOAD_FAST                'cmd'
              778  LOAD_STR                 '-s'
              780  LOAD_FAST                'reads'
              782  LOAD_STR                 'merged'
              784  BINARY_SUBSCR    
              786  BUILD_LIST_2          2 
              788  INPLACE_ADD      
              790  STORE_FAST               'cmd'
              792  JUMP_FORWARD        824  'to 824'
            794_0  COME_FROM           772  '772'

 L. 406       794  LOAD_STR                 'single'
              796  LOAD_FAST                'reads'
              798  LOAD_METHOD              keys
              800  CALL_METHOD_0         0  '0 positional arguments'
              802  COMPARE_OP               in
          804_806  POP_JUMP_IF_FALSE   824  'to 824'

 L. 407       808  LOAD_FAST                'cmd'
              810  LOAD_STR                 '-s'
              812  LOAD_FAST                'reads'
              814  LOAD_STR                 'single'
              816  BINARY_SUBSCR    
              818  BUILD_LIST_2          2 
              820  INPLACE_ADD      
              822  STORE_FAST               'cmd'
            824_0  COME_FROM           804  '804'
            824_1  COME_FROM           792  '792'

 L. 408       824  LOAD_STR                 'nanopore'
              826  LOAD_FAST                'reads'
              828  LOAD_METHOD              keys
              830  CALL_METHOD_0         0  '0 positional arguments'
              832  COMPARE_OP               in
          834_836  POP_JUMP_IF_FALSE   854  'to 854'

 L. 409       838  LOAD_FAST                'cmd'
              840  LOAD_STR                 '-l'
              842  LOAD_FAST                'reads'
              844  LOAD_STR                 'nanopore'
              846  BINARY_SUBSCR    
              848  BUILD_LIST_2          2 
              850  INPLACE_ADD      
              852  STORE_FAST               'cmd'
            854_0  COME_FROM           834  '834'

 L. 410       854  LOAD_STR                 'pacbio'
              856  LOAD_FAST                'reads'
              858  LOAD_METHOD              keys
              860  CALL_METHOD_0         0  '0 positional arguments'
              862  COMPARE_OP               in
          864_866  POP_JUMP_IF_FALSE   884  'to 884'

 L. 411       868  LOAD_FAST                'cmd'
              870  LOAD_STR                 '-l'
              872  LOAD_FAST                'reads'
              874  LOAD_STR                 'pacbio'
              876  BINARY_SUBSCR    
              878  BUILD_LIST_2          2 
              880  INPLACE_ADD      
              882  STORE_FAST               'cmd'
            884_0  COME_FROM           864  '864'

 L. 413       884  LOAD_GLOBAL              run_external
              886  LOAD_FAST                'args'
              888  LOAD_FAST                'cmd'
              890  CALL_FUNCTION_2       2  '2 positional arguments'
              892  STORE_FAST               'rc'

 L. 415       894  LOAD_FAST                'rc'
              896  LOAD_CONST               0
              898  COMPARE_OP               !=
          900_902  POP_JUMP_IF_FALSE   948  'to 948'

 L. 416       904  LOAD_GLOBAL              logger
              906  LOAD_METHOD              error
              908  LOAD_STR                 'Genome assembly finished with errors.'
              910  CALL_METHOD_1         1  '1 positional argument'
              912  POP_TOP          

 L. 417       914  LOAD_GLOBAL              logger
              916  LOAD_METHOD              error
              918  LOAD_STR                 'Plese check %s for more information.'
              920  LOAD_GLOBAL              os
              922  LOAD_ATTR                path
              924  LOAD_METHOD              join
              926  LOAD_FAST                'aslydir'
              928  LOAD_STR                 'unicycler.log'
              930  CALL_METHOD_2         2  '2 positional arguments'
              932  BINARY_MODULO    
              934  CALL_METHOD_1         1  '1 positional argument'
              936  POP_TOP          

 L. 418       938  LOAD_GLOBAL              Exception
              940  LOAD_STR                 'Extermal software error'
              942  CALL_FUNCTION_1       1  '1 positional argument'
              944  RAISE_VARARGS_1       1  'exception instance'
              946  JUMP_FORWARD        994  'to 994'
            948_0  COME_FROM           900  '900'

 L. 420       948  LOAD_GLOBAL              logger
              950  LOAD_METHOD              debug
              952  LOAD_STR                 'Assembling finished'
              954  CALL_METHOD_1         1  '1 positional argument'
              956  POP_TOP          

 L. 421       958  LOAD_GLOBAL              os
            960_0  COME_FROM           526  '526'
              960  LOAD_ATTR                path
              962  LOAD_METHOD              join
              964  LOAD_FAST                'aslydir'
              966  LOAD_STR                 'assembly.fasta'
              968  CALL_METHOD_2         2  '2 positional arguments'
              970  STORE_FAST               'assembly'

 L. 422       972  LOAD_FAST                'args'
              974  LOAD_ATTR                extract_replicons
          976_978  POP_JUMP_IF_FALSE   990  'to 990'

 L. 423       980  LOAD_GLOBAL              extract_replicons
              982  LOAD_FAST                'args'
              984  LOAD_FAST                'aslydir'
              986  CALL_FUNCTION_2       2  '2 positional arguments'
              988  POP_TOP          
            990_0  COME_FROM           976  '976'

 L. 424       990  LOAD_FAST                'assembly'
              992  RETURN_VALUE     
            994_0  COME_FROM           946  '946'
              994  JUMP_FORWARD       1010  'to 1010'
            996_0  COME_FROM           586  '586'

 L. 427       996  LOAD_GLOBAL              logger
              998  LOAD_METHOD              critical
             1000  LOAD_STR                 'Not yet implemented'
             1002  CALL_METHOD_1         1  '1 positional argument'
             1004  POP_TOP          

 L. 428      1006  LOAD_CONST               None
             1008  RETURN_VALUE     
           1010_0  COME_FROM           994  '994'
           1010_1  COME_FROM           574  '574'

Parse error at or near `COME_FROM' instruction at offset 960_0


def extract_replicons(args, aslydir):
    logfile = os.path.join(aslydir, 'unicycler.log')
    assemblyfile = os.path.join(aslydir, 'assembly.fasta')
    with open(logfile, 'r') as (log):
        regexp = re.compile('\\s?\\d+.+\\scomplete')
        repl_lengths = []
        for l in log.readlines():
            if regexp.search(l):
                component, segments, links, length, _, _, status = l.split()
                if int(segments) == 1:
                    repl_lengths.append(int(length.replace(',', '')))

        logger.debug('Extracting ' + str(len(repl_lengths)) + ' replicon(s).')
        with open(assemblyfile, 'r') as (assembly):
            replicons = [x for x in SeqIO.parse(assembly, 'fasta') if len(x) in repl_lengths]
            for x in range(len(replicons)):
                try:
                    F = open(os.path.join(aslydir, f"replicon.{x + 1}.fasta"), 'w')
                    SeqIO.write(replicons[x], F, 'fasta')
                    F.close()
                except Exception as e:
                    try:
                        raise e
                    finally:
                        e = None
                        del e


def locus_tag_gen(genome):
    logger.info('No locus tag provided. Generating it as MD5 hash of genome')
    with open(genome, 'rb') as (genomefile):
        locus_tag = ''.join([chr(ord(x) + 17).upper() for x in hashlib.md5(genomefile.read()).hexdigest()[0:6]])
        logger.info('Locus tag generated: %s' % locus_tag)
        return locus_tag


def annotate(args):
    logger.info('Genome annotation started')
    try:
        version = subprocess.run(['dfast', '--version'], stderr=(subprocess.PIPE), stdout=(subprocess.PIPE)).stdout
    except Exception as e:
        try:
            logger.critical('Failed to run DFAST')
            raise e
        finally:
            e = None
            del e

    annodir = os.path.join(args.output_dir, 'annotation')
    cmd = [
     'dfast', '-g', args.genome, '-o', annodir, '--organism', ' '.join([args.genus, args.species]),
     '--cpu', str(args.threads)]
    if args.strain:
        cmd += ['--strain', args.strain]
    if args.center_name:
        cmd += ['--center_name', args.center_name]
    if not args.locus_tag:
        args.locus_tag = locus_tag_gen(args.genome)
    if args.locus_tag:
        cmd += ['--locus_tag_prefix', args.locus_tag]
    if args.locus_tag_inc:
        cmd += ['--step', str(args.locus_tag_inc)]
    if args.minimum_length:
        cmd += ['--minimum_length', args.minimum_length]
    rc = run_external(args, cmd)
    return os.path.join(annodir, 'genome.fna')


def check_phix(args):
    logger.info('Checking assembly for presence of Illumina phiX control')
    phix_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data/phiX174.fasta')
    blast_format = '6 sseqid pident slen length'
    cmd = ['blastn', '-query', phix_path, '-subject', args.genome, '-outfmt', blast_format, '-evalue', '1e-6']
    logger.debug('Running: ' + ' '.join(cmd))
    try:
        blast_out = str(subprocess.run(cmd, universal_newlines=True, stderr=(subprocess.PIPE), stdout=(subprocess.PIPE)).stdout).rstrip()
    except Exception as e:
        try:
            raise e
        finally:
            e = None
            del e

    phix_contigs = []
    if bool(blast_out):
        for l in blast_out.split('\n'):
            i, p, s, l = l.split('\t')
            if float(p) > 95.0 and int(s) / int(l) > 0.5:
                phix_contigs.append(i)

        phix_contigs = list(set(phix_contigs))
        if len(phix_contigs) > 0:
            logger.info(f"PhiX was found in: {', '.join(phix_contigs)}")
            newgenome = os.path.join(args.output_dir, 'assembly.nophix.fasta')
            records = [x for x in SeqIO.parse(args.genome, 'fasta') if x.id not in phix_contigs]
            with open(newgenome, 'w') as (handle):
                SeqIO.write(records, handle, 'fasta')
                args.genome = newgenome
    return args.genome


def run_checkm(args):
    checkm_indir = create_subdir(args.output_dir, 'checkm_tmp_in')
    try:
        shutil.copy(args.genome, checkm_indir)
    except Exception as e:
        try:
            raise e
        finally:
            e = None
            del e

    checkm_outdir = os.path.join(args.output_dir, 'checkm')
    checkm_outfile = os.path.join(args.output_dir, 'CheckM.txt')
    checkm_ext = os.path.splitext(args.genome)[1]
    if args.checkm_mode == 'taxonomy_wf':
        cmd = ['checkm', 'taxonomy_wf', '-f', checkm_outfile, '-x', checkm_ext, '-t', str(args.threads)]
        try:
            checkm_taxon_list = str(subprocess.run(['checkm', 'taxon_list'], universal_newlines=True,
              stderr=(subprocess.PIPE),
              stdout=(subprocess.PIPE)).stdout)
        except Exception as e:
            try:
                raise e
            finally:
                e = None
                del e

        if args.checkm_taxon:
            if args.checkm_rank:
                found = False
                for l in checkm_taxon_list.split('\n'):
                    if args.checkm_taxon in l and args.checkm_rank in l:
                        found = True
                        break

                if not found:
                    logger.error(f"Taxon {args.checkm_taxon} of rank {args.checkm_rank} not available for CheckM")
                    args.checkm_taxon = None
                    args.checkm_rank = None
        if not (args.checkm_taxon and args.checkm_rank):
            args.checkm_taxon = 'Archaea' if args.domain == 'archaea' else 'Bacteria'
            args.checkm_rank = 'domain'
        logger.info(f"{args.checkm_taxon} marker set will be used for CheckM")
        cmd += [args.checkm_rank, args.checkm_taxon, checkm_indir, checkm_outdir]
    else:
        cmd = ['checkm', 'lineage_wf', '-f', checkm_outfile, '-t', str(args.threads), '-x', checkm_ext]
        if not args.checkm_full_tree:
            cmd += ['--reduced_tree']
        cmd += ['--pplacer_threads', str(args.threads), checkm_indir, checkm_outdir]
    rc = run_external(args, cmd)
    shutil.rmtree(checkm_indir)
    return rc


def check_last_step(args, step):
    if args.last_step == step:
        logger.info('Workflow finished!')
        exit(0)


def main():
    global logger
    args = parse_args()
    args.output_dir = os.path.abspath(args.output_dir)
    if os.path.isdir(args.output_dir):
        if args.force:
            shutil.rmtree(args.output_dir)
        else:
            raise FileExistsError('\nOutput directory "%s" already exists.\n' % args.output_dir + 'Use --force to overwrite or provide another path')
    try:
        os.mkdir(args.output_dir)
    except Exception as e:
        try:
            raise e('Imposible to create directory "%s"' % args.output_dir + 'Check provided path and permisions')
        finally:
            e = None
            del e

    logger = logging.getLogger('main')
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    fh = logging.FileHandler(os.path.join(args.output_dir, 'zga.log'))
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    logger.info('Pipeline started')
    steps = {'qc':1, 
     'processing':2,  'assembling':3,  'annotation':5,  'check_genome':4}
    start_step_int = steps[args.first_step]
    args.last_step = steps[args.last_step]
    if start_step_int <= 3:
        reads = check_reads(args)
        logger.debug('Reads: ' + str(reads))
        if len(list(reads)) == 0:
            logger.error('No reads provided for genome assembly')
            raise Exception('No reads provided for genome assembly')
    if start_step_int > 3:
        args.genome and os.path.isfile(args.genome) or logger.error('Genome assembly is not provided')
        raise FileNotFoundError()
    if start_step_int == 1:
        return_code = read_QC(args, reads)
        check_last_step(args, 1)
    if start_step_int <= 2:
        reads = read_processing(args, reads)
        logger.debug('Processed reads: ' + str(reads))
        check_last_step(args, 2)
    if start_step_int <= 3:
        args.genome = assemble(args, reads)
        check_last_step(args, 3)
    if start_step_int <= 4:
        logger.info('Checking genome quality')
        if args.check_phix:
            args.genome = check_phix(args)
        return_code = run_checkm(args)
        check_last_step(args, 4)
    if start_step_int <= 5:
        if not (args.genome and os.path.isfile(args.genome)):
            logger.error('Genome assembly is not provided')
            raise FileNotFoundError()
        args.genome = annotate(args)
        check_last_step(args, 5)


if __name__ == '__main__':
    main()