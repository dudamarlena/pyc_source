# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/traits_finder/scripts/HGT_finder_sum.py
# Compiled at: 2020-01-23 22:37:30
# Size of source mod 2**32: 46619 bytes
import os
from Bio import SeqIO
import argparse, glob
from datetime import datetime
parser = argparse.ArgumentParser(formatter_class=(argparse.RawDescriptionHelpFormatter))
parser.add_argument('-t', help='trait name',
  type=str,
  default='ARG',
  metavar='trait name')
parser.add_argument('-m', help='mapping file of traits to function',
  type=str,
  default='Butyrate.pro.mapping.txt',
  metavar='Butyrate.pro.mapping.txt')
parser.add_argument('-db', help='file name of your input database',
  type=str,
  default='Butyrate.pro.aa',
  metavar='database.aa')
parser.add_argument('-dbf', help="sequence format of your input database                    (1: nucleotide; 2: protein),                     (default '1' for nucleotide)",
  metavar='1 or 2',
  choices=[
 1, 2],
  action='store',
  default=1,
  type=int)
parser.add_argument('--r', help='input directory or folder of your previous results by Traits_WGD.py',
  type=str,
  default='Result',
  metavar='Result')
parser.add_argument('--s', help='input directory or folder of your previous results by traits summary',
  type=str,
  default='None',
  metavar='summary')
parser.add_argument('--g', help='Optional: gene-level HGT finding; --g T (default: function-level; --g F)',
  metavar=[
 'T', 'F'],
  action='store',
  default='F',
  type=str)
parser.add_argument('--th', help='Optional: set the thread number assigned for running XXX (default 1)',
  metavar='1 or more',
  action='store',
  default=1,
  type=int)
parser.add_argument('--u', '--usearch', help="Optional: use two-step method for blast search, 'None' for using one step, 'usearch' for using two-step                              (complete path to usearch if not in PATH), (default: 'None')",
  metavar='None or usearch',
  action='store',
  default='None',
  type=str)
parser.add_argument('--dm', '--diamond', help="Optional: use two-step method for blast search, 'None' for using one step, 'diamond' for using two-step                            (complete path to diamond if not in PATH), (default: 'None')",
  metavar='None or diamond',
  action='store',
  default='None',
  type=str)
parser.add_argument('--hs', help="Optional: use two-step method for blast search, 'None' for using one step, 'hs-blastn' for using two-step                            (complete path to hs-blastn if not in PATH), (default: 'None')",
  metavar='None or hs-blastn',
  action='store',
  default='None',
  type=str)
parser.add_argument('--bp', help='Optional: complete path to blastp or blastn if not in PATH,',
  metavar='/usr/local/bin/blast',
  action='store',
  default='blast',
  type=str)
parser.add_argument('--mf', '--mafft', help='Optional: complete path to mafft if not in PATH,',
  metavar='/usr/local/bin/mafft',
  action='store',
  default='None',
  type=str)
parser.add_argument('--ft', '--fasttree', help='Optional: complete path to fasttree if not in PATH,',
  metavar='/usr/local/bin/fasttree',
  action='store',
  default='None',
  type=str)
args = parser.parse_args()
Cutoff_16S = 0.97
Cutoff_HGT = 0.99
Cutoff_aa = 0.8
Cutoff_extended = 0.8
Cutoff_extended2 = 0.99
Hit_length = 0.9
script_i = 0
script_i_max = int(args.th)
if args.s == 'None':
    input_dir = os.path.join(args.r, 'summary')
    result_dir = os.path.join(args.r, 'HGT')
else:
    input_dir = args.s
    result_dir = os.path.join(args.s, '../HGT')
try:
    os.mkdir(result_dir)
except OSError:
    pass

try:
    os.mkdir(result_dir + '/sub_fun_summary')
except OSError:
    pass

try:
    os.mkdir(result_dir + '/sub_fun')
except OSError:
    pass

workingdir = os.path.abspath(os.path.dirname(__file__))
try:
    os.system('rm -rf HGT_subscripts')
    os.mkdir('HGT_subscripts')
except OSError:
    pass

__metaclass__ = type

class HGT_function:
    __doc__ = 'a class to store HGT_function'

    def init(self, function, type, cutoff, range16S_same, outputfile):
        self.function = function
        self.type = type
        self.cutoff = cutoff
        self.range16S_same = range16S_same
        self.Diff_16S_min = Cutoff_16S
        self.mge_to_genome = 0
        self.mge_to_mge = 0
        self.sameCluster_16S_Set = set()
        self.diffCluster_16S_Set = set()
        self.outputfile = outputfile
        self.outputfile_list = []
        output_file = open(outputfile, 'w')
        output_file.write('function\ttype_cutoff\tgenome_pair\tid_gene\tid_16S\n')
        output_file.close()
        self.Same_genome_set = set()
        self.Diff_genome_set = set()

    def addsame16Scluster(self, cluster):
        self.sameCluster_16S_Set.add(cluster)

    def adddiff16Scluster(self, cluster):
        self.diffCluster_16S_Set.add(cluster)

    def adddiffgenome_set(self, genome_pair):
        self.Diff_genome_set.add(genome_pair)

    def addsamegenome_set(self, genome_pair):
        self.Same_genome_set.add(genome_pair)

    def setDiff_16S_min(self, newlow):
        self.Diff_16S_min = min(self.Diff_16S_min, newlow)

    def addmge_to_genome(self):
        self.mge_to_genome += 1

    def addmge_to_mge(self):
        self.mge_to_mge += 1

    def addoutput(self, lines):
        self.outputfile_list.append(lines)

    def writeoutput(self):
        output_file = open(self.outputfile, 'a')
        output_file.write(''.join(self.outputfile_list))
        self.outputfile_list = []
        output_file.close()


def Calculate_length(file_name):
    DB_length = set()
    try:
        for lines in open(file_name + '.length', 'r'):
            DB_length.add(float(str(lines.split('\t')[(-1)]).replace('\n', '')))

    except IOError:
        Fasta_name = open(file_name, 'r')
        f = open(file_name + '.length', 'w')
        for record in SeqIO.parse(Fasta_name, 'fasta'):
            f.write(str(record.id) + '\t' + str(len(record.seq)) + '\n')
            DB_length.add(len(str(record.seq)))

        f.close()

    DB_length_min = min(DB_length)
    if args.dbf == 1:
        DB_length_out = [
         DB_length_min, DB_length_min / 3.0]
    else:
        DB_length_out = [
         DB_length_min * 3.0, DB_length_min]
    return DB_length_out


def split_string_last(input_string, substring):
    last_loci = input_string.rfind(substring)
    if last_loci > -1:
        return input_string[0:last_loci]
    else:
        return input_string


def checkfile(filename, i):
    try:
        f1 = open(filename, 'r')
        if os.path.getsize(filename) > 0:
            for lines in f1:
                try:
                    lines.split('\t', maxsplit=(i + 1))[i]
                    return 'not empty'
                except IndexError:
                    return 'wrong content by spliting %s \\t' % str(i)

                break

        else:
            return 'empty'
    except IOError:
        return 'non-existed'


def genome_com(genome1, genome2):
    if genome1 == genome2:
        return 'same'
    else:
        if genome1 < genome2:
            return '%s-%s' % (genome1, genome2)
        return 'skip'


def usearch_16S_load(input_file):
    Checkoutput = checkfile(input_file, 2)
    if Checkoutput == 'not empty':
        for lines in open(input_file, 'r'):
            line_set = lines.split('\t', maxsplit=4)
            genome_16S = genome_com(line_set[0], line_set[1])
            if genome_16S not in ('same', 'skip'):
                ID_16S.setdefault(genome_16S, float(line_set[2]) / 100.0)

    else:
        print('file %s is %s' % (input_file, Checkoutput))


def self_clustering--- This code section failed: ---

 L. 235         0  LOAD_GLOBAL              open
                2  LOAD_FAST                'output_uc'
                4  LOAD_STR                 'w'
                6  CALL_FUNCTION_2       2  '2 positional arguments'
                8  STORE_FAST               'output_uc'

 L. 236        10  LOAD_GLOBAL              dict
               12  CALL_FUNCTION_0       0  '0 positional arguments'
               14  STORE_FAST               'clusters'

 L. 237        16  LOAD_CONST               0
               18  STORE_FAST               'cluster_num'

 L. 238        20  LOAD_GLOBAL              checkfile
               22  LOAD_FAST                'input_usearch'
               24  LOAD_CONST               2
               26  CALL_FUNCTION_2       2  '2 positional arguments'
               28  STORE_FAST               'Checkoutput'

 L. 239        30  LOAD_FAST                'Checkoutput'
               32  LOAD_STR                 'not empty'
               34  COMPARE_OP               ==
               36  POP_JUMP_IF_FALSE   522  'to 522'

 L. 240        40  SETUP_LOOP          538  'to 538'
               44  LOAD_GLOBAL              open
               46  LOAD_FAST                'input_usearch'
               48  CALL_FUNCTION_1       1  '1 positional argument'
               50  GET_ITER         
               52  FOR_ITER            518  'to 518'
               56  STORE_FAST               'lines'

 L. 241        58  LOAD_FAST                'lines'
               60  LOAD_ATTR                split
               62  LOAD_STR                 '\t'
               64  LOAD_CONST               4
               66  LOAD_CONST               ('maxsplit',)
               68  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               70  STORE_FAST               'line_set'

 L. 242        72  LOAD_FAST                'line_set'
               74  LOAD_CONST               0
               76  BINARY_SUBSCR    
               78  STORE_FAST               'Gene1'

 L. 243        80  LOAD_FAST                'line_set'
               82  LOAD_CONST               1
               84  BINARY_SUBSCR    
               86  STORE_FAST               'Gene2'

 L. 244        88  LOAD_GLOBAL              float
               90  LOAD_FAST                'line_set'
               92  LOAD_CONST               2
               94  BINARY_SUBSCR    
               96  CALL_FUNCTION_1       1  '1 positional argument'
               98  LOAD_CONST               100.0
              100  BINARY_TRUE_DIVIDE
              102  STORE_FAST               'ID'

 L. 245       104  LOAD_GLOBAL              genome_com
              106  LOAD_FAST                'Gene1'
              108  LOAD_FAST                'Gene2'
              110  CALL_FUNCTION_2       2  '2 positional arguments'
              112  STORE_FAST               'genome_16S'

 L. 246       114  LOAD_FAST                'genome_16S'
              116  LOAD_CONST               ('same', 'skip')
              118  COMPARE_OP               not-in
              120  POP_JUMP_IF_FALSE   140  'to 140'

 L. 247       122  LOAD_GLOBAL              ID_16S
              124  LOAD_ATTR                setdefault
              126  LOAD_GLOBAL              function_com
              128  LOAD_FAST                'Gene1'
              130  LOAD_FAST                'Gene2'
              132  CALL_FUNCTION_2       2  '2 positional arguments'
              134  LOAD_FAST                'ID'
              136  CALL_FUNCTION_2       2  '2 positional arguments'
              138  POP_TOP          
            140_0  COME_FROM           120  '120'

 L. 248       140  LOAD_FAST                'Gene1'
              142  LOAD_FAST                'clusters'
              144  COMPARE_OP               not-in
              146  JUMP_IF_FALSE_OR_POP   154  'to 154'
              148  LOAD_FAST                'Gene2'
              150  LOAD_FAST                'clusters'
              152  COMPARE_OP               not-in
            154_0  COME_FROM           146  '146'
              154  POP_JUMP_IF_FALSE   306  'to 306'

 L. 249       158  LOAD_FAST                'cluster_num'
              160  LOAD_CONST               1
              162  INPLACE_ADD      
              164  STORE_FAST               'cluster_num'

 L. 250       166  LOAD_FAST                'ID'
              168  LOAD_GLOBAL              Cutoff_16S
              170  COMPARE_OP               <
              172  POP_JUMP_IF_FALSE   244  'to 244'

 L. 252       174  LOAD_FAST                'clusters'
              176  LOAD_ATTR                setdefault
              178  LOAD_FAST                'Gene1'
              180  LOAD_FAST                'cluster_num'
              182  CALL_FUNCTION_2       2  '2 positional arguments'
              184  POP_TOP          

 L. 253       186  LOAD_FAST                'output_uc'
              188  LOAD_ATTR                write
              190  LOAD_STR                 '*\t%s\t*\t*\t*\t*\t*\t*\t%s\t*\n'
              192  LOAD_FAST                'cluster_num'
              194  LOAD_FAST                'Gene1'
              196  BUILD_TUPLE_2         2 
              198  BINARY_MODULO    
              200  CALL_FUNCTION_1       1  '1 positional argument'
              202  POP_TOP          

 L. 254       204  LOAD_FAST                'cluster_num'
              206  LOAD_CONST               1
              208  INPLACE_ADD      
              210  STORE_FAST               'cluster_num'

 L. 255       212  LOAD_FAST                'clusters'
              214  LOAD_ATTR                setdefault
              216  LOAD_FAST                'Gene2'
              218  LOAD_FAST                'cluster_num'
              220  CALL_FUNCTION_2       2  '2 positional arguments'
              222  POP_TOP          

 L. 256       224  LOAD_FAST                'output_uc'
              226  LOAD_ATTR                write
              228  LOAD_STR                 '*\t%s\t*\t*\t*\t*\t*\t*\t%s\t*\n'
              230  LOAD_FAST                'cluster_num'
              232  LOAD_FAST                'Gene2'
              234  BUILD_TUPLE_2         2 
              236  BINARY_MODULO    
              238  CALL_FUNCTION_1       1  '1 positional argument'
              240  POP_TOP          
              242  JUMP_FORWARD        304  'to 304'
              244  ELSE                     '304'

 L. 259       244  LOAD_FAST                'clusters'
              246  LOAD_ATTR                setdefault
              248  LOAD_FAST                'Gene1'
              250  LOAD_FAST                'cluster_num'
              252  CALL_FUNCTION_2       2  '2 positional arguments'
              254  POP_TOP          

 L. 260       256  LOAD_FAST                'output_uc'
              258  LOAD_ATTR                write
              260  LOAD_STR                 '*\t%s\t*\t*\t*\t*\t*\t*\t%s\t*\n'
              262  LOAD_FAST                'cluster_num'
              264  LOAD_FAST                'Gene1'
              266  BUILD_TUPLE_2         2 
              268  BINARY_MODULO    
              270  CALL_FUNCTION_1       1  '1 positional argument'
              272  POP_TOP          

 L. 261       274  LOAD_FAST                'clusters'
              276  LOAD_ATTR                setdefault
              278  LOAD_FAST                'Gene2'
              280  LOAD_FAST                'cluster_num'
              282  CALL_FUNCTION_2       2  '2 positional arguments'
              284  POP_TOP          

 L. 262       286  LOAD_FAST                'output_uc'
              288  LOAD_ATTR                write
              290  LOAD_STR                 '*\t%s\t*\t*\t*\t*\t*\t*\t%s\t*\n'
              292  LOAD_FAST                'cluster_num'
              294  LOAD_FAST                'Gene2'
              296  BUILD_TUPLE_2         2 
              298  BINARY_MODULO    
              300  CALL_FUNCTION_1       1  '1 positional argument'
              302  POP_TOP          
            304_0  COME_FROM           242  '242'
              304  JUMP_BACK            52  'to 52'
              306  ELSE                     '516'

 L. 264       306  LOAD_FAST                'ID'
              308  LOAD_GLOBAL              Cutoff_16S
              310  COMPARE_OP               <
              312  POP_JUMP_IF_FALSE   418  'to 418'

 L. 266       316  LOAD_FAST                'Gene1'
              318  LOAD_FAST                'clusters'
              320  COMPARE_OP               not-in
              322  POP_JUMP_IF_FALSE   366  'to 366'

 L. 267       326  LOAD_FAST                'cluster_num'
              328  LOAD_CONST               1
              330  INPLACE_ADD      
              332  STORE_FAST               'cluster_num'

 L. 268       334  LOAD_FAST                'clusters'
              336  LOAD_ATTR                setdefault
              338  LOAD_FAST                'Gene1'
              340  LOAD_FAST                'cluster_num'
              342  CALL_FUNCTION_2       2  '2 positional arguments'
              344  POP_TOP          

 L. 269       346  LOAD_FAST                'output_uc'
              348  LOAD_ATTR                write
              350  LOAD_STR                 '*\t%s\t*\t*\t*\t*\t*\t*\t%s\t*\n'
              352  LOAD_FAST                'cluster_num'
              354  LOAD_FAST                'Gene1'
              356  BUILD_TUPLE_2         2 
              358  BINARY_MODULO    
              360  CALL_FUNCTION_1       1  '1 positional argument'
              362  POP_TOP          
              364  JUMP_FORWARD        416  'to 416'
              366  ELSE                     '416'

 L. 270       366  LOAD_FAST                'Gene2'
              368  LOAD_FAST                'clusters'
              370  COMPARE_OP               not-in
              372  POP_JUMP_IF_FALSE   516  'to 516'

 L. 271       376  LOAD_FAST                'cluster_num'
              378  LOAD_CONST               1
              380  INPLACE_ADD      
              382  STORE_FAST               'cluster_num'

 L. 272       384  LOAD_FAST                'clusters'
              386  LOAD_ATTR                setdefault
              388  LOAD_FAST                'Gene2'
              390  LOAD_FAST                'cluster_num'
              392  CALL_FUNCTION_2       2  '2 positional arguments'
              394  POP_TOP          

 L. 273       396  LOAD_FAST                'output_uc'
              398  LOAD_ATTR                write
              400  LOAD_STR                 '*\t%s\t*\t*\t*\t*\t*\t*\t%s\t*\n'
              402  LOAD_FAST                'cluster_num'
              404  LOAD_FAST                'Gene2'
              406  BUILD_TUPLE_2         2 
              408  BINARY_MODULO    
              410  CALL_FUNCTION_1       1  '1 positional argument'
              412  POP_TOP          
              414  JUMP_FORWARD        416  'to 416'
            416_0  COME_FROM           414  '414'
            416_1  COME_FROM           364  '364'

 L. 276       416  CONTINUE             52  'to 52'

 L. 279       418  LOAD_FAST                'Gene1'
              420  LOAD_FAST                'clusters'
              422  COMPARE_OP               not-in
              424  POP_JUMP_IF_FALSE   468  'to 468'

 L. 280       428  LOAD_FAST                'clusters'
              430  LOAD_FAST                'Gene2'
              432  BINARY_SUBSCR    
              434  STORE_FAST               'Gene2_cluster'

 L. 281       436  LOAD_FAST                'clusters'
              438  LOAD_ATTR                setdefault
              440  LOAD_FAST                'Gene1'
              442  LOAD_FAST                'Gene2_cluster'
              444  CALL_FUNCTION_2       2  '2 positional arguments'
              446  POP_TOP          

 L. 282       448  LOAD_FAST                'output_uc'
              450  LOAD_ATTR                write
              452  LOAD_STR                 '*\t%s\t*\t*\t*\t*\t*\t*\t%s\t*\n'
              454  LOAD_FAST                'Gene2_cluster'
              456  LOAD_FAST                'Gene1'
              458  BUILD_TUPLE_2         2 
              460  BINARY_MODULO    
              462  CALL_FUNCTION_1       1  '1 positional argument'
              464  POP_TOP          
              466  JUMP_BACK            52  'to 52'
              468  ELSE                     '516'

 L. 283       468  LOAD_FAST                'Gene2'
              470  LOAD_FAST                'clusters'
              472  COMPARE_OP               not-in
              474  POP_JUMP_IF_FALSE    52  'to 52'

 L. 284       476  LOAD_FAST                'clusters'
              478  LOAD_FAST                'Gene1'
              480  BINARY_SUBSCR    
              482  STORE_FAST               'Gene1_cluster'

 L. 285       484  LOAD_FAST                'clusters'
              486  LOAD_ATTR                setdefault
              488  LOAD_FAST                'Gene2'
              490  LOAD_FAST                'Gene1_cluster'
              492  CALL_FUNCTION_2       2  '2 positional arguments'
              494  POP_TOP          

 L. 286       496  LOAD_FAST                'output_uc'
              498  LOAD_ATTR                write
              500  LOAD_STR                 '*\t%s\t*\t*\t*\t*\t*\t*\t%s\t*\n'
              502  LOAD_FAST                'Gene1_cluster'
              504  LOAD_FAST                'Gene2'
              506  BUILD_TUPLE_2         2 
              508  BINARY_MODULO    
              510  CALL_FUNCTION_1       1  '1 positional argument'
              512  POP_TOP          
              514  CONTINUE             52  'to 52'

 L. 289       516  JUMP_BACK            52  'to 52'
              518  POP_BLOCK        
            520_0  COME_FROM_LOOP       40  '40'
              520  JUMP_FORWARD        538  'to 538'
              522  ELSE                     '538'

 L. 291       522  LOAD_GLOBAL              print
              524  LOAD_STR                 'file %s is %s'
              526  LOAD_FAST                'input_usearch'
              528  LOAD_FAST                'Checkoutput'
              530  BUILD_TUPLE_2         2 
              532  BINARY_MODULO    
              534  CALL_FUNCTION_1       1  '1 positional argument'
              536  POP_TOP          
            538_0  COME_FROM           520  '520'

 L. 292       538  LOAD_FAST                'output_uc'
              540  LOAD_ATTR                close
              542  CALL_FUNCTION_0       0  '0 positional arguments'
              544  POP_TOP          

Parse error at or near `POP_BLOCK' instruction at offset 518


def loci_seq(record_name):
    loci_last = record_name.rfind('_')
    return [int(record_name[record_name.rfind('_', 0, loci_last) + 1:loci_last]),
     int(record_name[loci_last + 1:])]


def function_load(input_file, type_fasta):
    Function_Set = dict()
    Checkoutput = checkfile(input_file, 8)
    if Checkoutput == 'not empty':
        for lines in open(input_file, 'r'):
            line_set = lines.split('\t', maxsplit=3)
            gene = line_set[1]
            if args.g == 'F':
                function = line_set[0].replace('(', '').replace(')', '').replace('.', '_').replace(' ', '_').replace('-', '_')
            else:
                function = line_set[2]
            if type_fasta == 'dna':
                loci_new = loci_seq(gene)
                gene = gene[0:gene.rfind('_', 0, gene.rfind('_') - 1)]
                Function_Set.setdefault(gene, [[], []])
                loci_set = [int(loci_new[0]), int(loci_new[1])]
                if loci_set not in Function_Set[gene][(-1)]:
                    Function_Set[gene][(-1)].append(loci_set)
                    Function_Set[gene][0].append([function, loci_set])
            else:
                Function_Set.setdefault(gene, function)

    else:
        print('file %s is %s' % (input_file, Checkoutput))
    return Function_Set


def compare_loci(loci_new, loci_ref):
    if min(loci_new[0], loci_new[1]) <= min(loci_ref[0], loci_ref[1]):
        if max(loci_new[0], loci_new[1]) >= max(loci_ref[0], loci_ref[1]):
            return True
    return False


def function_find(Function_Set, Genome, type_fasta):
    if not Genome.startswith('reference'):
        if type_fasta == 'aa':
            return Function_Set.get(Genome)
        else:
            loci_last_2 = Genome.rfind('_', 0, Genome.rfind('_') - 1)
            loci_last_3 = Genome.rfind('_', 0, loci_last_2)
            loci_last_4 = Genome.rfind('_', 0, loci_last_3)
            loci_new = [int(Genome[loci_last_4 + 1:loci_last_3]),
             int(Genome[loci_last_3 + 1:loci_last_2])]
            Genome_name = Genome[0:loci_last_4]
            for functions in Function_Set.get(Genome_name)[0]:
                if type_fasta == 'dna':
                    if loci_new == functions[(-1)]:
                        return functions[0]
                else:
                    loci_ref = functions[(-1)]
                    if compare_loci(loci_new, loci_ref):
                        return functions[0]

            return 'reference'
    else:
        return 'reference'


def deduplicate(input_fasta, Function_Set, type_fasta):
    unique_set = dict()
    record_list = dict()
    i = 0
    for record in SeqIO.parse(input_fasta, 'fasta'):
        record_id = str(record.id)
        record_seq = str(record.seq)
        if record_seq not in unique_set:
            function = function_find(Function_Set, record_id, type_fasta)
            new_name = '%s-%s' % (function, i)
            unique_set.setdefault(record_seq, [new_name, len(record_seq)])
            i += 1
            record_list.setdefault(new_name, [record_id])
        else:
            new_name = unique_set[record_seq][0]
            if new_name.startswith('reference'):
                function = function_find(Function_Set, record_id, type_fasta)
                new_new_name = new_name.replace('reference', function)
                unique_set[record_seq][0] = new_new_name
                record_list[new_new_name] = record_list.pop(new_name)
                new_name = new_new_name
            record_list[new_name].append(str(record.id))

    fout1 = open(input_fasta + '.unique', 'w')
    fout1_list = []
    fout2 = open(input_fasta + '.unique_list', 'w')
    fout2_list = []
    fout3 = open(input_fasta + '.unique_length', 'w')
    fout3_list = []
    for record_seq in unique_set:
        record_id = unique_set[record_seq][0]
        record_len = unique_set[record_seq][1]
        if not record_id.startswith('reference'):
            fout1_list.append('>%s\n%s\n' % (record_id, record_seq))
            fout3_list.append('%s\t%s\t\n' % (record_id, record_len))

    fout1.write(''.join(fout1_list))
    fout3.write(''.join(fout3_list))
    for newrecord in record_list:
        if not newrecord.startswith('reference'):
            for oldrecord in record_list[newrecord]:
                fout2_list.append('%s\t%s\t\n' % (newrecord, oldrecord))

    fout2.write(''.join(fout2_list))
    fout1.close()
    fout2.close()
    fout3.close()


def function_com(function1, function2):
    if function1 < function2:
        return function1 + '-' + function2
    else:
        if function1 == function2:
            return function1
        return function2 + '-' + function1


def run_compare(input_fasta, Function_Set, cutoff1, cutoff2, type_fasta, clustering='F'):
    if clustering != 'T':
        try:
            f1 = open('%s.unique_length' % input_fasta, 'r')
        except IOError:
            print('%s deduplicate %s' % (datetime.now(), input_fasta))
            deduplicate(input_fasta, Function_Set, type_fasta)

        input_fasta = input_fasta + '.unique'
    else:
        filesize = int(os.path.getsize(input_fasta))
        if filesize <= 1000000000.0:
            if args.u != 'None':
                try:
                    f1 = open('%s.sorted' % input_fasta, 'r')
                except IOError:
                    os.system('%s -sortbylength %s -fastaout %s.sorted' % (args.u, input_fasta, input_fasta))

                input_fasta = input_fasta + '.sorted'
        try:
            f1 = open('%s.%s.usearch.txt' % (input_fasta, cutoff2), 'r')
        except IOError:
            print('%s Running usearch for %s' % (datetime.now(), input_fasta))
            if filesize <= 30000000.0:
                if args.u != 'None':
                    try:
                        f1 = open('%s.udb' % input_fasta, 'r')
                    except IOError:
                        os.system('%s -makeudb_usearch %s -output %s.udb\n' % (
                         args.u, input_fasta, input_fasta))

                    if type_fasta == 'aa':
                        os.system('%s  -usearch_global %s -db %s.udb  -id %s -maxaccepts 0 -maxrejects 0 -blast6out %s.%s.usearch.txt  -threads %s\n' % (
                         args.u, input_fasta, input_fasta, cutoff2, input_fasta, cutoff2, str(args.th)))
                    else:
                        os.system('%s  -usearch_global %s -db %s.udb  -strand both -id %s -maxaccepts 0 -maxrejects 0 -blast6out %s.%s.usearch.txt  -threads %s\n' % (
                         args.u, input_fasta, input_fasta, cutoff2, input_fasta, cutoff2, str(args.th)))
            if type_fasta == 'dna':
                if args.hs != 'None':
                    print('%s Using hs-blastn instead of usearch because the input file is larger than 2GB\n' % datetime.now())
                    try:
                        f1 = open('%s.counts.obinary' % input_fasta, 'r')
                    except IOError:
                        os.system('%s -in %s -input_type fasta -dbtype nucl' % (
                         os.path.join(os.path.split(args.bp)[0], 'makeblastdb'), input_fasta))
                        os.system('windowmasker -in %s -infmt blastdb -mk_counts -out %s.counts' % (
                         input_fasta, input_fasta))
                        os.system('windowmasker -in %s.counts -sformat obinary -out %s.counts.obinary -convert' % (
                         input_fasta, input_fasta))
                        os.system('%s index %s' % (args.hs, input_fasta))

                    os.system('%s align -db %s -window_masker_db %s.counts.obinary -query %s -out %s.%s.usearch.txt -outfmt 6 -evalue 1 -perc_identity %s -num_threads %s\n' % (
                     args.hs, input_fasta,
                     input_fasta, input_fasta, input_fasta, cutoff2,
                     cutoff2, str(min(int(args.th), 40))))
            if args.dm != 'None':
                if type_fasta == 'aa':
                    print('%s Using diamond instead of usearch because the input file is larger than 2GB\n' % datetime.now())
                    try:
                        f1 = open('%s.dmnd' % input_fasta, 'r')
                    except IOError:
                        os.system('%sdiamond makedb --in %s -d %s.dmnd' % (
                         split_string_last(args.dm, 'diamond'), input_fasta, input_fasta))

                    os.system('%sdiamond blastp  --query  %s  --db  %s.dmnd --out %s.%s.usearch.txt --outfmt 6 --id %s --evalue 1 --max-target-seqs 0 --threads %s\n' % (
                     split_string_last(args.dm, 'diamond'), input_fasta,
                     input_fasta, input_fasta, cutoff2,
                     cutoff2, str(min(int(args.th), 40))))
            if type_fasta == 'aa':
                print('Input file %s is %sMb, too large for usearch\nPlease provide diamond using --dm' % (
                 input_fasta, filesize / 10000000.0))
            else:
                print('Input file %s is %sMb, too large for usearch\nPlease provide hs-blastn using --hs' % (
                 input_fasta, filesize / 10000000.0))

        if clustering == 'T':
            try:
                f1 = open('%s.uc' % input_fasta, 'r')
            except IOError:
                print('%s Running usearch cluster for %s' % (datetime.now(), input_fasta))
                if int(os.path.getsize(input_fasta)) <= 1000000000.0:
                    if args.u != 'None':
                        os.system('%s -sort length -cluster_fast %s -id %s -centroids %s.cluster.aa -uc %s.uc -threads %s' % (
                         args.u, input_fasta, cutoff1, input_fasta, input_fasta, args.th))
                else:
                    print('%s We roughly clustered the 16S by 97% identity\n' % datetime.now())
                    self_clustering('%s.%s.usearch.txt' % (input_fasta, cutoff2), input_fasta + '.uc')

            if ID_16S == dict():
                usearch_16S_load('%s.%s.usearch.txt' % (input_fasta, cutoff2))
            print('%s finish running usearch cluster for %s' % (datetime.now(), input_fasta))
            Clusters = dict()
            Clusters_seqs = dict()
            Checkoutput = checkfile(input_fasta + '.uc', -2)
            Max_ID_len = 0
            Min_ID_len = 0
            if Checkoutput == 'not empty':
                for lines in open(input_fasta + '.uc', 'r'):
                    line_set = lines.split('\t')
                    cluster = line_set[1]
                    record_name = line_set[(-2)].split(' ', maxsplit=2)[0]
                    Clusters.setdefault(cluster, [])
                    Clusters[cluster].append(record_name)
                    length = len(record_name)
                    Max_ID_len = max(Max_ID_len, length)
                    if Min_ID_len == 0:
                        Min_ID_len = length
                    Min_ID_len = min(Min_ID_len, length)

            else:
                print('file %s is %s' % (input_fasta + '.uc', Checkoutput))
            for cluster in Clusters:
                for record_name in Clusters[cluster]:
                    Clusters_seqs.setdefault(record_name, str(cluster))

            return [
             Clusters_seqs, Clusters, Max_ID_len, Min_ID_len]


def compare_16S(Genome1, Genome2, cutoff):
    if Genome1 == 'mge' or Genome2 == 'mge':
        return [
         'mge']
    else:
        Genome_set = genome_com(Genome1, Genome2)
        if Genome_set not in ('same', 'skip'):
            if Genome_set in ID_16S:
                if ID_16S[Genome_set] < cutoff:
                    return [True, Genome_set]
                else:
                    return [
                     False, Genome_set]
            else:
                return [
                 '16S missing']
        else:
            return [
             '16S missing']


def function_pair(Genome1, Genome2):
    function1 = split_string_last(Genome1, '-')
    function2 = split_string_last(Genome2, '-')
    return function_com(function1, function2)


def extract_dna(dna_file, gene_list, output_fasta, type_fasta, script_i):
    output_file = open(output_fasta, 'a')
    for record in SeqIO.parse(open(dna_file, 'r'), 'fasta'):
        record_id = str(record.id)
        if record_id in gene_list:
            output_file.write('>%s\n%s\n' % (record_id, str(record.seq)))

    output_file.close()
    if args.mf != 'None':
        try:
            f1 = open('%s.align.nwk' % output_fasta, 'r')
        except IOError:
            f1 = open('%s.align.nwk' % output_fasta, 'w')
            output_script_file = open('HGT_subscripts/HGTalign.%s.sh' % int(script_i % script_i_max), 'a')
            script_i += 1
            output_script_file.write('#!/bin/bash\n')
            output_script_file.write('python %s/remove.duplicated.seq.py -i %s \n' % (workingdir, output_fasta))
            if 'dna' in type_fasta:
                output_script_file.write('%s --nuc --adjustdirection --quiet --nofft --maxiterate 0 --retree 1 --thread %s %s.dereplicated.id.fasta > %s.align\n' % (
                 args.mf, str(args.th), output_fasta, output_fasta))
                if args.ft != 'None':
                    output_script_file.write('%s -nt -quiet -fastest -nosupport %s.align > %s.align.nwk\n' % (
                     args.ft, output_fasta, output_fasta))
            else:
                output_script_file.write('%s --amino --quiet --retree 1 --maxiterate 0 --nofft --thread %s %s.dereplicated.id.fasta > %s.align\n' % (
                 args.mf, str(args.th), output_fasta, output_fasta))
            if args.ft != 'None':
                output_script_file.write('%s -quiet -fastest -nosupport %s.align > %s.align.nwk\n' % (
                 args.ft, output_fasta, output_fasta))
            output_script_file.close()

    return script_i


def add_gene_and_function(Diff_gene_set, Function, Gene):
    Diff_gene_set.setdefault(Function, set())
    Diff_gene_set[Function].add(Gene)


def find_genome(Genome1):
    if Genome1 in mapping:
        return mapping[Genome1]
    else:
        if Genome1.startswith('mge'):
            mapping.setdefault(Genome1, 'mge')
            return 'mge'
        for i in range(cluster_16S[(-1)], len(Genome1)):
            if Genome1[i] in ('.', '_'):
                Candidate = Genome1[0:i]
                if Candidate in cluster_16S[0]:
                    mapping.setdefault(Genome1, Candidate)
                    return Candidate
                if i > cluster_16S[(-2)]:
                    mapping.setdefault(Genome1, 'None')
                    return 'None'

        if Genome1 in cluster_16S[0]:
            mapping.setdefault(Genome1, Genome1)
            return Genome1
        mapping.setdefault(Genome1, 'None')
        return 'None'


def unique_list_load(input_fasta):
    unique_list = dict()
    unique_length = dict()
    for lines in open(input_fasta + '.unique_list', 'r'):
        loci_last = lines.rfind('\t')
        loci_last_2 = lines.rfind('\t', 0, loci_last - 1)
        new_name = lines[0:loci_last_2]
        new_genome = lines[loci_last_2 + 1:loci_last]
        new_genome2 = find_genome(new_genome)
        if new_genome2 != 'None':
            unique_list.setdefault(new_name, [])
            unique_list[new_name].append([new_genome, new_genome2])

    for lines in open(input_fasta + '.unique_length', 'r'):
        loci_last = lines.rfind('\t')
        loci_last_2 = lines.rfind('\t', 0, loci_last - 1)
        new_name = lines[0:loci_last_2]
        gene_length = int(lines[loci_last_2 + 1:loci_last])
        unique_length.setdefault(new_name, gene_length)

    return [
     unique_list, unique_length]


def HGT_finder_sum(type_fasta, input_folder, input_prefix, cutoff, cutoff_hit_length, script_i, output_file1, input_fasta, DB_length_min):
    Function_list = dict()
    unique_list_all = unique_list_load(input_fasta)
    unique_list = unique_list_all[0]
    unique_length = unique_list_all[1]
    all_usearch = glob.glob(os.path.join(input_folder, input_prefix))
    line_num = 1
    for files in all_usearch:
        Checkoutput = checkfile(files, 2)
        if Checkoutput == 'not empty':
            Outputfiles = dict()
            Diff_gene_set = dict()
            for lines in open(files, 'r'):
                try:
                    line_set = lines.split('\t', maxsplit=4)
                    ID = float(line_set[2]) / 100.0
                    if ID >= cutoff:
                        newGene1 = line_set[0]
                        newGene2 = line_set[1]
                        min_gene_length = float(min(unique_length[newGene1], unique_length[newGene2]))
                        if min_gene_length >= DB_length_min:
                            hit_length = float(line_set[3]) / min_gene_length
                            if hit_length >= cutoff_hit_length:
                                Function = function_pair(newGene1, newGene2)
                                if Function not in Function_list:
                                    HGT_function_temp = HGT_function()
                                    HGT_function_temp.init(Function, type_fasta, cutoff, '%.3f-1.000' % Cutoff_16S, os.path.join(result_dir, 'sub_fun_summary/%s.%s.%.2f.identity.summary.txt' % (
                                     Function, type_fasta, cutoff)))
                                    Function_list.setdefault(Function, HGT_function_temp)
                                HGT_function_temp = Function_list[Function]
                                for Gene1_set in unique_list.get(newGene1, []):
                                    for Gene2_Set in unique_list.get(newGene2, []):
                                        Gene1 = Gene1_set[0]
                                        Gene2 = Gene2_Set[0]
                                        Genome1 = Gene1_set[1]
                                        Genome2 = Gene2_Set[1]
                                        Gene_pair = genome_com(Gene1, Gene2)
                                        if Gene_pair not in ('same', 'skip'):
                                            if line_num % 100000 == 0:
                                                for Outputfilename in Outputfiles:
                                                    fout = open(Outputfilename, 'a')
                                                    fout.write(''.join(Outputfiles[Outputfilename]))
                                                    fout.close()

                                                Outputfiles = dict()
                                                HGT_function_temp.writeoutput()
                                                print('%s HGT_finder processing %s lines' % (datetime.now(), line_num))
                                            compare_result = compare_16S(Genome1, Genome2, Cutoff_16S)
                                            if compare_result[0] != '16S missing':
                                                line_num += 1
                                                if compare_result[0] != 'mge':
                                                    try:
                                                        if Genome1 != Genome2:
                                                            Genome_pair = compare_result[1]
                                                            cluster1 = cluster_16S[0][Genome1]
                                                            cluster2 = cluster_16S[0][Genome2]
                                                            if compare_result[0]:
                                                                output_file_name = os.path.join(result_dir + '/sub_fun', '%s.%s.%s.diff.cluster' % (
                                                                 Function, args.t, type_fasta))
                                                                Outputfiles.setdefault(output_file_name, [])
                                                                Outputfiles[output_file_name].append('%s\t%s\t%s\t%s' % (Function, Gene1, Gene2, lines))
                                                                if args.mf != 'None':
                                                                    add_gene_and_function(Diff_gene_set, Function, newGene1)
                                                                    add_gene_and_function(Diff_gene_set, Function, newGene2)
                                                                ID = float(line_set[2]) / 100.0
                                                                HGT_function_temp.adddiffgenome_set(Genome_pair)
                                                                HGT_function_temp.adddiff16Scluster(cluster1)
                                                                HGT_function_temp.adddiff16Scluster(cluster2)
                                                                lowest_id = Cutoff_16S
                                                                if Genome_pair in ID_16S:
                                                                    lowest_id = ID_16S[Genome_pair]
                                                                HGT_function_temp.setDiff_16S_min(lowest_id)
                                                                HGT_function_temp.addoutput('%s\t%s_%s\t%s\t%.3f\t%.3f\n' % (
                                                                 Function, type_fasta, cutoff,
                                                                 Genome_pair, ID, lowest_id))
                                                            else:
                                                                output_file_name = os.path.join(result_dir + '/sub_fun', '%s.%s.%s.same.cluster' % (
                                                                 Function, args.t, type_fasta))
                                                                Outputfiles.setdefault(output_file_name, [])
                                                                Outputfiles[output_file_name].append('%s\t%s\t%s\t%s' % (Function, Gene1, Gene2, lines))
                                                                HGT_function_temp.addsamegenome_set(Genome_pair)
                                                                HGT_function_temp.addsame16Scluster(cluster1)
                                                                HGT_function_temp.addsame16Scluster(cluster2)
                                                    except KeyError:
                                                        pass

                                                else:
                                                    output_file_name = os.path.join(result_dir + '/sub_fun', '%s.%s.%s.mge.cluster' % (
                                                     Function, args.t, type_fasta))
                                                    Outputfiles.setdefault(output_file_name, [])
                                                    Outputfiles[output_file_name].append('%s\t%s\t%s\t%s' % (Function, Gene1, Gene2, lines))
                                                    if Genome1 == 'mge':
                                                        if Genome2 == 'mge':
                                                            HGT_function_temp.addmge_to_mge()
                                                    else:
                                                        HGT_function_temp.addmge_to_genome()

                except IndexError:
                    print('file %s is %s' % (files, 'wrong content by spliting %s \\t' % '2'))
                    print(lines)

    for Outputfilename in Outputfiles:
        fout = open(Outputfilename, 'a')
        fout.write(''.join(Outputfiles[Outputfilename]))
        fout.close()

    print('%s HGT_finder processing %s lines' % (datetime.now(), line_num))
    print('%s output HGT results' % datetime.now())
    for Function in Function_list:
        HGT_function_temp = Function_list[Function]
        total_combination = []
        for clusters in HGT_function_temp.diffCluster_16S_Set:
            total_16S = len(cluster_16S[1][clusters])
            total_combination.append(total_16S)

        total_combination_sum = sum(total_combination)
        total_pair_diff = total_combination_sum * (total_combination_sum - 1) / 2.0
        for total_16S in total_combination:
            total_pair_diff -= total_16S * (total_16S - 1) / 2.0

        range16S_diff = '%.3f-%.3f' % (HGT_function_temp.Diff_16S_min, Cutoff_16S)
        hit_pair_diff = len(HGT_function_temp.Diff_genome_set)
        try:
            percentage_diff_pair = float(hit_pair_diff / total_pair_diff)
        except ZeroDivisionError:
            percentage_diff_pair = 0

        total_combination = []
        total_pair_same = 0
        for clusters in HGT_function_temp.sameCluster_16S_Set:
            total_16S = len(cluster_16S[1][clusters])
            total_combination.append(total_16S)

        for total_16S in total_combination:
            total_pair_same += total_16S * (total_16S - 1) / 2.0

        hit_pair_same = len(HGT_function_temp.Same_genome_set)
        try:
            percentage_same_pair = float(hit_pair_same / total_pair_same)
        except ZeroDivisionError:
            percentage_same_pair = 0

        try:
            diff_same_ratio = '%.3f' % (percentage_diff_pair / percentage_same_pair)
        except ZeroDivisionError:
            diff_same_ratio = 0

        Result = [Function, type_fasta, '%.2f' % cutoff,
         range16S_diff, '%.1f' % hit_pair_diff, total_pair_diff, '%.3f' % percentage_diff_pair, HGT_function_temp.range16S_same,
         '%.1f' % hit_pair_same, total_pair_same, '%.3f' % percentage_same_pair, diff_same_ratio,
         HGT_function_temp.mge_to_genome, HGT_function_temp.mge_to_mge]
        for i in range(0, len(Result)):
            Result[i] = str(Result[i])

        output_file1.write('\t'.join(Result) + '\n')
        HGT_function_temp.writeoutput()

    os.system('cat %s > %s' % (
     os.path.join(result_dir, 'sub_fun_summary/*.identity.summary.txt'),
     os.path.join(result_dir, 'all.identity.summary.txt')))
    if args.mf != 'None':
        if Diff_gene_set != dict():
            print('%s extract sequences' % datetime.now())
            for Function in Diff_gene_set:
                if Diff_gene_set[Function] != []:
                    script_i = extract_dna(input_fasta + '.unique', Diff_gene_set[Function], os.path.join(result_dir + '/sub_fun', '%s.%s.%s.diff.cluster.fasta' % (
                     Function, args.t, type_fasta)), type_fasta, script_i)

    return script_i


f16s = os.path.join(args.s, args.t + '.all.16S.fasta')
faa = os.path.join(args.s, args.t + '.all.traits.aa.fasta')
fdna = os.path.join(args.s, args.t + '.all.traits.dna.fasta')
fdna_500 = glob.glob(os.path.join(args.s, args.t + '.all.traits.dna.extra*.fasta'))[0]
ID_16S = dict()
Function_Set_dna = function_load(os.path.join(args.s, args.t + '.all.traits.dna.txt'), 'dna')
Function_Set_aa = function_load(os.path.join(args.s, args.t + '.all.traits.aa.txt'), 'aa')
DB_length = Calculate_length(args.db)
print('%s comparing and clustering 16S' % datetime.now())
cluster_16S = run_compare(f16s, Function_Set_dna, Cutoff_16S, 0.6, 'dna', 'T')
print('the range of length of 16S ID is %s to %s' % (cluster_16S[(-1)], cluster_16S[(-2)]))
print('%s comparing and clustering DNA' % datetime.now())
run_compare(fdna, Function_Set_dna, Cutoff_HGT, Cutoff_HGT, 'dna', 'F')
print('%s comparing and clustering DNA extended' % datetime.now())
run_compare(faa, Function_Set_aa, Cutoff_aa, Cutoff_aa, 'aa', 'F')
print('%s comparing and clustering AA' % datetime.now())
run_compare(fdna_500, Function_Set_dna, Cutoff_extended, Cutoff_extended, 'dna', 'F')
print('%s loading pre-mapping file' % datetime.now())
mapping = dict()
mapping_file = os.path.join(result_dir, 'mapping.genome.16S.txt')
mapping_file_output = 0
try:
    for lines in open(mapping_file, 'r'):
        lines_set = lines.split('\t', maxsplit=3)
        mapping.setdefault(lines_set[0], lines_set[1])

except IOError:
    mapping_file_output = 1

all_output_file = os.path.join(result_dir, 'HGT.summary.dna.%s.aa.%s.16S.%s.txt' % (
 Cutoff_HGT, Cutoff_aa, Cutoff_16S))
all_output = open(all_output_file, 'w')
all_output.write('function_name\ttype\tcutoff\trange16S_diff\thit_pair_diff\ttotal_pair_diff\tpercentage_diff_pair\trange16S_same\thit_pair_same\ttotal_pair_same\tpercentage_same_pair\tdiff_same_ratio\tmge_to_genome\tmge_to_mge\n')
all_output.close()
if glob.glob(os.path.join(result_dir + '/sub_fun', '*.%s.%s.*.cluster' % (
 args.t, 'dna'))) == []:
    print('%s summarize potential HGT of %s trait with cutoff of %s' % (datetime.now(), 'dna', Cutoff_HGT))
    all_output = open(all_output_file, 'a')
    script_i = HGT_finder_sum('dna', args.s, os.path.split(fdna)[(-1)] + '*.unique*.usearch.txt', Cutoff_HGT, Hit_length, script_i, all_output, fdna, DB_length[0])
    all_output.close()
if glob.glob(os.path.join(result_dir + '/sub_fun', '*.%s.%s.*.cluster' % (
 args.t, 'aa'))) == []:
    print('%s summarize potential HGT of %s trait with cutoff of %s' % (datetime.now(), 'aa', Cutoff_aa))
    all_output = open(all_output_file, 'a')
    script_i = HGT_finder_sum('aa', args.s, os.path.split(faa)[(-1)] + '*.unique*.usearch.txt', Cutoff_aa, Hit_length, script_i, all_output, faa, DB_length[1])
    all_output.close()
if glob.glob(os.path.join(result_dir + '/sub_fun', '*.%s.%s.*.cluster' % (
 args.t, 'dna_extended'))) == []:
    print('%s summarize potential HGT of %s trait with cutoff of %s' % (datetime.now(), 'extended dna', Cutoff_extended))
    all_output = open(all_output_file, 'a')
    script_i = HGT_finder_sum('dna_extended', args.s, os.path.split(fdna_500)[(-1)] + '*.unique*.usearch.txt', Cutoff_extended, Hit_length, script_i, all_output, fdna_500, DB_length[0])
    all_output.close()
    print('%s summarize potential HGT of %s trait with cutoff of %s' % (datetime.now(), 'extended dna', Cutoff_HGT))
    all_output = open(all_output_file, 'a')
    script_i = HGT_finder_sum('dna_extended', args.s, os.path.split(fdna_500)[(-1)] + '*.unique*.usearch.txt', Cutoff_extended2, Hit_length, script_i, all_output, fdna_500, DB_length[0])
    all_output.close()
list_of_files = glob.glob('HGT_subscripts/HGTalign.*.sh')
f1 = open('HGTalign.sh', 'w')
f1.write('#!/bin/bash\nsource ~/.bashrc\n')
for file_name in list_of_files:
    f1.write('jobmit %s HGTalign\n' % file_name)

f1.close()
if mapping_file_output == 1:
    fout = open(mapping_file, 'w')
    fout_set = []
    for genome in mapping:
        fout_set.append(genome + '\t' + mapping[genome] + '\t\n')

    fout.write(''.join(fout_set))
    fout.close()