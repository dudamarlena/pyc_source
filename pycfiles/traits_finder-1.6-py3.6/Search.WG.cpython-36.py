# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/traits_finder/scripts/Search.WG.py
# Compiled at: 2020-01-24 00:53:52
# Size of source mod 2**32: 27051 bytes
import os
from Bio import SeqIO
import argparse, glob
parser = argparse.ArgumentParser(formatter_class=(argparse.RawDescriptionHelpFormatter))
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
parser.add_argument('-i', help='input dir of WGD',
  type=str,
  default='.',
  metavar='current dir (.)')
parser.add_argument('-s', help="set the method to search the your database                     (1: blast; 2: hmm; 3: alignment),                     (default '1' for blast search)",
  metavar='1 or 2',
  choices=[
 1, 2, 3],
  action='store',
  default=1,
  type=int)
parser.add_argument('--fa', help='input format of genome sequence',
  type=str,
  default='.fna.add',
  metavar='.fasta, .fna or .fa')
parser.add_argument('--orf', help='input format of genome orfs',
  type=str,
  default='.faa',
  metavar='.faa')
parser.add_argument('--r', help='output directory or folder of your results',
  type=str,
  default='Result',
  metavar='Result')
parser.add_argument('--r16', help='output directory or folder of your 16S sequences',
  type=str,
  default='Result',
  metavar='Result')
parser.add_argument('--t', help='Optional: set the thread number assigned for running (default 1)',
  metavar='1 or more',
  action='store',
  default=1,
  type=int)
parser.add_argument('--id', default=50.0,
  action='store',
  type=float,
  metavar='80.0',
  help='Optional: set the amno acid based identity cutoff for blast (default is 80.0)\nLeave it alone if hmm is used')
parser.add_argument('--ht', default=50.0,
  action='store',
  type=float,
  metavar='80.0',
  help='Optional: set the amno acid based hit-length cutoff for blast (default is 80.0)\nLeave it alone if hmm is used')
parser.add_argument('--e', default=1e-05,
  action='store',
  type=float,
  metavar='1e-5',
  help='Optional: set the evalue cutoff for blast or hmm (default is 1e-5)')
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
parser.add_argument('--hmm', help='Optional: complete path to hmmscan if not in PATH,',
  metavar='/usr/local/bin/hmmscan',
  action='store',
  default='hmmscan',
  type=str)
parser.add_argument('--bp', help='Optional: complete path to blast if not in PATH,',
  metavar='/usr/local/bin/blast',
  action='store',
  default='blast',
  type=str)
parser.add_argument('--bwa', help='Optional: complete path to bwa if not in PATH,',
  metavar='/usr/local/bin/bwa',
  action='store',
  default='None',
  type=str)
parser.add_argument('--mf', '--mafft', help='Optional: complete path to mafft if not in PATH,',
  metavar='/usr/local/bin/mafft',
  action='store',
  default='None',
  type=str)
parser.add_argument('--pro', '--prodigal', help='Optional: complete path to prodigal if not in PATH,',
  metavar='/usr/local/bin/prodigal',
  action='store',
  default='None',
  type=str)
args = parser.parse_args()
fasta_format = args.fa
orfs_format = args.orf
try:
    os.mkdir(args.r)
except OSError:
    pass

workingdir = os.path.abspath(os.path.dirname(__file__))

def addname(file_name):
    Fasta_name = open(file_name, 'r')
    f = open(file_name + '.add', 'w')
    in_dir, input_file = os.path.split(file_name)
    for record in SeqIO.parse(Fasta_name, 'fasta'):
        if len(str(record.seq).replace(' ', '')) > 0:
            f.write('>' + str(input_file) + '_' + str(record.id) + '\t' + str(record.description).replace('\t', ' ') + '\n' + str(str(record.seq)) + '\n')

    f.close()


def split_string_last(input_string, substring):
    last_loci = input_string.rfind(substring)
    if last_loci > -1:
        return input_string[0:last_loci]
    else:
        return input_string


def search--- This code section failed: ---

 L. 131         0  LOAD_STR                 ''
                2  STORE_FAST               'cmds'

 L. 132         4  LOAD_FAST                'cmds'
                6  LOAD_STR                 '#!/bin/bash \nmodule add c3ddb/blast+/2.7.1 \n'
                8  INPLACE_ADD      
               10  STORE_FAST               'cmds'

 L. 133        12  LOAD_GLOBAL              os
               14  LOAD_ATTR                path
               16  LOAD_ATTR                join
               18  LOAD_FAST                'roottemp'
               20  LOAD_FAST                'genome_output'
               22  CALL_FUNCTION_2       2  '2 positional arguments'
               24  STORE_FAST               'genome_file'

 L. 134        26  LOAD_GLOBAL              os
               28  LOAD_ATTR                path
               30  LOAD_ATTR                join
               32  LOAD_FAST                'roottemp'
               34  LOAD_FAST                'orf_output'
               36  CALL_FUNCTION_2       2  '2 positional arguments'
               38  STORE_FAST               'orf_file'

 L. 136        40  LOAD_GLOBAL              args
               42  LOAD_ATTR                s
               44  LOAD_CONST               1
               46  COMPARE_OP               ==
               48  POP_JUMP_IF_FALSE  2680  'to 2680'

 L. 137        52  LOAD_GLOBAL              args
               54  LOAD_ATTR                u
               56  LOAD_STR                 'None'
               58  COMPARE_OP               !=
               60  POP_JUMP_IF_TRUE     84  'to 84'
               62  LOAD_GLOBAL              args
               64  LOAD_ATTR                hs
               66  LOAD_STR                 'None'
               68  COMPARE_OP               !=
               70  POP_JUMP_IF_TRUE     84  'to 84'
               72  LOAD_GLOBAL              args
               74  LOAD_ATTR                dm
               76  LOAD_STR                 'None'
               78  COMPARE_OP               !=
             80_0  COME_FROM            70  '70'
             80_1  COME_FROM            60  '60'
               80  POP_JUMP_IF_FALSE  1178  'to 1178'

 L. 139        84  LOAD_CONST               0
               86  STORE_FAST               'Usearch'

 L. 140        88  SETUP_LOOP          226  'to 226'
               90  LOAD_GLOBAL              os
               92  LOAD_ATTR                walk
               94  LOAD_GLOBAL              args
               96  LOAD_ATTR                r
               98  LOAD_STR                 '/usearch'
              100  BINARY_ADD       
              102  CALL_FUNCTION_1       1  '1 positional argument'
              104  GET_ITER         
              106  FOR_ITER            224  'to 224'
              108  UNPACK_SEQUENCE_3     3 
              110  STORE_FAST               'root'
              112  STORE_FAST               'dirs'
              114  STORE_FAST               'files'

 L. 141       116  SETUP_EXCEPT        202  'to 202'

 L. 142       118  LOAD_GLOBAL              open
              120  LOAD_GLOBAL              os
              122  LOAD_ATTR                path
              124  LOAD_ATTR                join
              126  LOAD_FAST                'root'
              128  LOAD_FAST                'genome_output'
              130  LOAD_STR                 '.usearch.txt.aa'
              132  BINARY_ADD       
              134  CALL_FUNCTION_2       2  '2 positional arguments'
              136  LOAD_STR                 'r'
              138  CALL_FUNCTION_2       2  '2 positional arguments'
              140  STORE_FAST               'ftry'

 L. 143       142  LOAD_GLOBAL              os
              144  LOAD_ATTR                path
              146  LOAD_ATTR                join
              148  LOAD_FAST                'root'
              150  LOAD_FAST                'genome_output'
              152  LOAD_STR                 '.usearch.txt.aa'
              154  BINARY_ADD       
              156  CALL_FUNCTION_2       2  '2 positional arguments'
              158  STORE_FAST               'searchfile_genome'

 L. 144       160  LOAD_GLOBAL              os
              162  LOAD_ATTR                path
              164  LOAD_ATTR                join
              166  LOAD_GLOBAL              args
              168  LOAD_ATTR                r
              170  LOAD_STR                 '/usearch/'
              172  BINARY_ADD       
              174  LOAD_GLOBAL              str
              176  LOAD_GLOBAL              folder_id
              178  CALL_FUNCTION_1       1  '1 positional argument'
              180  BINARY_ADD       

 L. 145       182  LOAD_FAST                'orf_output'
              184  LOAD_STR                 '.usearch.txt.aa'
              186  BINARY_ADD       
              188  CALL_FUNCTION_2       2  '2 positional arguments'
              190  STORE_FAST               'searchfile_orf'

 L. 146       192  LOAD_CONST               1
              194  STORE_FAST               'Usearch'

 L. 147       196  BREAK_LOOP       
              198  POP_BLOCK        
              200  JUMP_BACK           106  'to 106'
            202_0  COME_FROM_EXCEPT    116  '116'

 L. 148       202  DUP_TOP          
              204  LOAD_GLOBAL              IOError
              206  COMPARE_OP               exception-match
              208  POP_JUMP_IF_FALSE   220  'to 220'
              210  POP_TOP          
              212  POP_TOP          
              214  POP_TOP          

 L. 149       216  POP_EXCEPT       
              218  JUMP_BACK           106  'to 106'
              220  END_FINALLY      
              222  JUMP_BACK           106  'to 106'
              224  POP_BLOCK        
            226_0  COME_FROM_LOOP       88  '88'

 L. 150       226  LOAD_FAST                'Usearch'
              228  LOAD_CONST               0
              230  COMPARE_OP               ==
              232  POP_JUMP_IF_FALSE  1186  'to 1186'

 L. 151       236  LOAD_GLOBAL              os
              238  LOAD_ATTR                path
              240  LOAD_ATTR                join
              242  LOAD_GLOBAL              args
              244  LOAD_ATTR                r
              246  LOAD_STR                 '/usearch/'
              248  BINARY_ADD       
              250  LOAD_GLOBAL              str
              252  LOAD_GLOBAL              folder_id
              254  CALL_FUNCTION_1       1  '1 positional argument'
              256  BINARY_ADD       

 L. 152       258  LOAD_FAST                'orf_output'
              260  LOAD_STR                 '.usearch.txt.aa'
              262  BINARY_ADD       
              264  CALL_FUNCTION_2       2  '2 positional arguments'
              266  STORE_FAST               'searchfile_orf'

 L. 153       268  LOAD_GLOBAL              os
              270  LOAD_ATTR                path
              272  LOAD_ATTR                join
              274  LOAD_GLOBAL              args
              276  LOAD_ATTR                r
              278  LOAD_STR                 '/usearch/'
              280  BINARY_ADD       
              282  LOAD_GLOBAL              str
              284  LOAD_GLOBAL              folder_id
              286  CALL_FUNCTION_1       1  '1 positional argument'
              288  BINARY_ADD       

 L. 154       290  LOAD_FAST                'genome_output'
              292  LOAD_STR                 '.usearch.txt.aa'
              294  BINARY_ADD       
              296  CALL_FUNCTION_2       2  '2 positional arguments'
              298  STORE_FAST               'searchfile_genome'

 L. 155       300  LOAD_GLOBAL              args
              302  LOAD_ATTR                dm
              304  LOAD_STR                 'None'
              306  COMPARE_OP               !=
              308  POP_JUMP_IF_FALSE   656  'to 656'
              312  LOAD_GLOBAL              args
              314  LOAD_ATTR                dbf
              316  LOAD_CONST               2
              318  COMPARE_OP               ==
              320  POP_JUMP_IF_FALSE   656  'to 656'

 L. 158       324  LOAD_FAST                'cmds'

 L. 163       326  LOAD_GLOBAL              split_string_last
              328  LOAD_GLOBAL              args
              330  LOAD_ATTR                dm
              332  LOAD_STR                 'diamond'
              334  CALL_FUNCTION_2       2  '2 positional arguments'
              336  LOAD_STR                 'diamond blastp --query '
              338  BINARY_ADD       
              340  LOAD_FAST                'orf_file'
              342  BINARY_ADD       
              344  LOAD_STR                 ' --db '
              346  BINARY_ADD       
              348  LOAD_GLOBAL              split_string_last
              350  LOAD_GLOBAL              args
              352  LOAD_ATTR                db
              354  LOAD_STR                 '.dmnd'
              356  CALL_FUNCTION_2       2  '2 positional arguments'
              358  BINARY_ADD       
              360  LOAD_STR                 '.dmnd --out '
              362  BINARY_ADD       
              364  LOAD_GLOBAL              os
              366  LOAD_ATTR                path
              368  LOAD_ATTR                join
              370  LOAD_GLOBAL              args
              372  LOAD_ATTR                r
              374  LOAD_STR                 '/usearch/'
              376  BINARY_ADD       
              378  LOAD_GLOBAL              str
              380  LOAD_GLOBAL              folder_id
              382  CALL_FUNCTION_1       1  '1 positional argument'
              384  BINARY_ADD       
              386  LOAD_FAST                'orf_output'
              388  LOAD_STR                 '.usearch.txt'
              390  BINARY_ADD       
              392  CALL_FUNCTION_2       2  '2 positional arguments'
              394  BINARY_ADD       
              396  LOAD_STR                 ' --outfmt 6 --max-target-seqs 1 --evalue '
              398  BINARY_ADD       
              400  LOAD_GLOBAL              str
              402  LOAD_GLOBAL              args
              404  LOAD_ATTR                e
              406  CALL_FUNCTION_1       1  '1 positional argument'
              408  BINARY_ADD       
              410  LOAD_STR                 ' --threads '
              412  BINARY_ADD       
              414  LOAD_GLOBAL              str
              416  LOAD_GLOBAL              int
              418  LOAD_GLOBAL              i_max
              420  CALL_FUNCTION_1       1  '1 positional argument'
              422  CALL_FUNCTION_1       1  '1 positional argument'
              424  BINARY_ADD       
              426  LOAD_STR                 ' \n'
              428  BINARY_ADD       
              430  INPLACE_ADD      
              432  STORE_FAST               'cmds'

 L. 165       434  LOAD_FAST                'cmds'

 L. 170       436  LOAD_GLOBAL              split_string_last
              438  LOAD_GLOBAL              args
              440  LOAD_ATTR                dm
              442  LOAD_STR                 'diamond'
              444  CALL_FUNCTION_2       2  '2 positional arguments'
              446  LOAD_STR                 'diamond blastx --query '
              448  BINARY_ADD       
              450  LOAD_FAST                'genome_file'
              452  BINARY_ADD       
              454  LOAD_STR                 ' --db '
              456  BINARY_ADD       
              458  LOAD_GLOBAL              split_string_last
              460  LOAD_GLOBAL              args
              462  LOAD_ATTR                db
              464  LOAD_STR                 '.dmnd'
              466  CALL_FUNCTION_2       2  '2 positional arguments'
              468  BINARY_ADD       
              470  LOAD_STR                 '.dmnd --out '
              472  BINARY_ADD       
              474  LOAD_GLOBAL              os
              476  LOAD_ATTR                path
              478  LOAD_ATTR                join
              480  LOAD_GLOBAL              args
              482  LOAD_ATTR                r
              484  LOAD_STR                 '/usearch/'
              486  BINARY_ADD       
              488  LOAD_GLOBAL              str
              490  LOAD_GLOBAL              folder_id
              492  CALL_FUNCTION_1       1  '1 positional argument'
              494  BINARY_ADD       
              496  LOAD_FAST                'genome_output'
              498  LOAD_STR                 '.usearch.txt'
              500  BINARY_ADD       
              502  CALL_FUNCTION_2       2  '2 positional arguments'
              504  BINARY_ADD       
              506  LOAD_STR                 ' --outfmt 6 --max-target-seqs 1 --evalue '
              508  BINARY_ADD       
              510  LOAD_GLOBAL              str
              512  LOAD_GLOBAL              args
              514  LOAD_ATTR                e
              516  CALL_FUNCTION_1       1  '1 positional argument'
              518  BINARY_ADD       
              520  LOAD_STR                 ' --threads '
              522  BINARY_ADD       
              524  LOAD_GLOBAL              str
              526  LOAD_GLOBAL              int
              528  LOAD_GLOBAL              i_max
              530  CALL_FUNCTION_1       1  '1 positional argument'
              532  CALL_FUNCTION_1       1  '1 positional argument'
              534  BINARY_ADD       
              536  LOAD_STR                 ' \n'
              538  BINARY_ADD       
              540  INPLACE_ADD      
              542  STORE_FAST               'cmds'

 L. 172       544  LOAD_FAST                'cmds'

 L. 174       546  LOAD_STR                 'python '
              548  LOAD_GLOBAL              workingdir
              550  BINARY_ADD       
              552  LOAD_STR                 '/Extract.WG.py -i '
              554  BINARY_ADD       
              556  LOAD_FAST                'roottemp'
              558  BINARY_ADD       
              560  LOAD_STR                 ' -f '
              562  BINARY_ADD       
              564  LOAD_FAST                'orf_output'
              566  BINARY_ADD       
              568  LOAD_STR                 ' -n .usearch.txt -r '
              570  BINARY_ADD       
              572  LOAD_GLOBAL              args
              574  LOAD_ATTR                r
              576  BINARY_ADD       
              578  LOAD_STR                 '/usearch/'
              580  BINARY_ADD       
              582  LOAD_GLOBAL              str
              584  LOAD_GLOBAL              folder_id
              586  CALL_FUNCTION_1       1  '1 positional argument'
              588  BINARY_ADD       
              590  LOAD_STR                 ' \n'
              592  BINARY_ADD       
              594  INPLACE_ADD      
              596  STORE_FAST               'cmds'

 L. 176       598  LOAD_FAST                'cmds'

 L. 178       600  LOAD_STR                 'python '
              602  LOAD_GLOBAL              workingdir
              604  BINARY_ADD       
              606  LOAD_STR                 '/Extract.MG.py  -p 1 -i '
              608  BINARY_ADD       
              610  LOAD_FAST                'roottemp'
              612  BINARY_ADD       
              614  LOAD_STR                 ' -f '
              616  BINARY_ADD       
              618  LOAD_FAST                'genome_output'
              620  BINARY_ADD       
              622  LOAD_STR                 ' -n .usearch.txt -r '
              624  BINARY_ADD       
              626  LOAD_GLOBAL              args
              628  LOAD_ATTR                r
              630  BINARY_ADD       
              632  LOAD_STR                 '/usearch/'
              634  BINARY_ADD       
              636  LOAD_GLOBAL              str
              638  LOAD_GLOBAL              folder_id
              640  CALL_FUNCTION_1       1  '1 positional argument'
              642  BINARY_ADD       
              644  LOAD_STR                 ' \n'
              646  BINARY_ADD       
              648  INPLACE_ADD      
              650  STORE_FAST               'cmds'
              652  JUMP_ABSOLUTE      1186  'to 1186'
            656_0  COME_FROM           308  '308'

 L. 179       656  LOAD_GLOBAL              args
              658  LOAD_ATTR                hs
              660  LOAD_STR                 'None'
              662  COMPARE_OP               !=
              664  POP_JUMP_IF_FALSE   834  'to 834'
              668  LOAD_GLOBAL              args
              670  LOAD_ATTR                dbf
              672  LOAD_CONST               1
              674  COMPARE_OP               ==
              676  POP_JUMP_IF_FALSE   834  'to 834'

 L. 181       680  LOAD_GLOBAL              args
              682  LOAD_ATTR                dbf
              684  LOAD_CONST               1
              686  COMPARE_OP               ==
              688  POP_JUMP_IF_FALSE  1176  'to 1176'

 L. 183       692  LOAD_FAST                'cmds'
              694  LOAD_STR                 '%s align -db %s -window_masker_db %s.counts.obinary -query %s -out %s -outfmt 6 -evalue %s -num_threads %s\n'

 L. 184       696  LOAD_GLOBAL              args
              698  LOAD_ATTR                hs
              700  LOAD_GLOBAL              args
              702  LOAD_ATTR                db
              704  LOAD_GLOBAL              args
              706  LOAD_ATTR                db
              708  LOAD_FAST                'genome_file'
              710  LOAD_GLOBAL              os
              712  LOAD_ATTR                path
              714  LOAD_ATTR                join

 L. 185       716  LOAD_GLOBAL              args
              718  LOAD_ATTR                r
              720  LOAD_STR                 '/usearch/'
              722  BINARY_ADD       
              724  LOAD_GLOBAL              str
              726  LOAD_GLOBAL              folder_id
              728  CALL_FUNCTION_1       1  '1 positional argument'
              730  BINARY_ADD       

 L. 186       732  LOAD_FAST                'genome_output'
              734  LOAD_STR                 '.usearch.txt'
              736  BINARY_ADD       
              738  CALL_FUNCTION_2       2  '2 positional arguments'

 L. 187       740  LOAD_GLOBAL              str
              742  LOAD_GLOBAL              args
              744  LOAD_ATTR                e
              746  CALL_FUNCTION_1       1  '1 positional argument'
              748  LOAD_GLOBAL              str
              750  LOAD_GLOBAL              min
              752  LOAD_GLOBAL              int
              754  LOAD_GLOBAL              i_max
              756  CALL_FUNCTION_1       1  '1 positional argument'
              758  LOAD_CONST               40
              760  CALL_FUNCTION_2       2  '2 positional arguments'
              762  CALL_FUNCTION_1       1  '1 positional argument'
              764  BUILD_TUPLE_7         7 
              766  BINARY_MODULO    
              768  INPLACE_ADD      
              770  STORE_FAST               'cmds'

 L. 188       772  LOAD_FAST                'cmds'

 L. 189       774  LOAD_STR                 'python '
              776  LOAD_GLOBAL              workingdir
              778  BINARY_ADD       
              780  LOAD_STR                 '/Extract.MG.py -p 1 -i '
              782  BINARY_ADD       
              784  LOAD_FAST                'roottemp'
              786  BINARY_ADD       
              788  LOAD_STR                 ' -f '
              790  BINARY_ADD       
              792  LOAD_FAST                'genome_output'
              794  BINARY_ADD       
              796  LOAD_STR                 ' -n .usearch.txt -r '
              798  BINARY_ADD       
              800  LOAD_GLOBAL              args
              802  LOAD_ATTR                r
              804  BINARY_ADD       
              806  LOAD_STR                 '/usearch/'
              808  BINARY_ADD       
              810  LOAD_GLOBAL              str
              812  LOAD_GLOBAL              folder_id
              814  CALL_FUNCTION_1       1  '1 positional argument'
              816  BINARY_ADD       
              818  LOAD_STR                 ' \n'
              820  BINARY_ADD       
              822  INPLACE_ADD      
              824  STORE_FAST               'cmds'

 L. 190       826  LOAD_FAST                'orf_file'
              828  STORE_FAST               'searchfile_orf'
              830  JUMP_ABSOLUTE      1186  'to 1186'
            834_0  COME_FROM           664  '664'

 L. 191       834  LOAD_GLOBAL              args
              836  LOAD_ATTR                u
              838  LOAD_STR                 'None'
              840  COMPARE_OP               !=
              842  POP_JUMP_IF_FALSE  1160  'to 1160'

 L. 193       846  LOAD_STR                 '.udb  -evalue 1e-2 -accel 0.5 -blast6out '
              848  STORE_FAST               'usearch_cmd'

 L. 194       850  LOAD_GLOBAL              args
              852  LOAD_ATTR                dbf
              854  LOAD_CONST               1
              856  COMPARE_OP               ==
              858  POP_JUMP_IF_FALSE   870  'to 870'

 L. 195       862  LOAD_FAST                'usearch_cmd'
              864  LOAD_STR                 ' -strand both '
              866  INPLACE_ADD      
              868  STORE_FAST               'usearch_cmd'
            870_0  COME_FROM           858  '858'

 L. 197       870  LOAD_FAST                'cmds'

 L. 201       872  LOAD_GLOBAL              args
              874  LOAD_ATTR                u
              876  LOAD_STR                 ' -ublast '
              878  BINARY_ADD       
              880  LOAD_FAST                'genome_file'
              882  BINARY_ADD       
              884  LOAD_STR                 ' -db '
              886  BINARY_ADD       
              888  LOAD_GLOBAL              split_string_last
              890  LOAD_GLOBAL              args
              892  LOAD_ATTR                db
              894  LOAD_STR                 '.udb'
              896  CALL_FUNCTION_2       2  '2 positional arguments'
              898  BINARY_ADD       
              900  LOAD_FAST                'usearch_cmd'
              902  BINARY_ADD       
              904  LOAD_GLOBAL              os
              906  LOAD_ATTR                path
              908  LOAD_ATTR                join
              910  LOAD_GLOBAL              args
              912  LOAD_ATTR                r
              914  LOAD_STR                 '/usearch/'
              916  BINARY_ADD       
              918  LOAD_GLOBAL              str
              920  LOAD_GLOBAL              folder_id
              922  CALL_FUNCTION_1       1  '1 positional argument'
              924  BINARY_ADD       
              926  LOAD_FAST                'genome_output'
              928  LOAD_STR                 '.usearch.txt'
              930  BINARY_ADD       
              932  CALL_FUNCTION_2       2  '2 positional arguments'
              934  BINARY_ADD       
              936  LOAD_STR                 ' -threads '
              938  BINARY_ADD       
              940  LOAD_GLOBAL              str
              942  LOAD_GLOBAL              int
              944  LOAD_GLOBAL              i_max
              946  CALL_FUNCTION_1       1  '1 positional argument'
              948  CALL_FUNCTION_1       1  '1 positional argument'
              950  BINARY_ADD       
              952  LOAD_STR                 ' \n'
              954  BINARY_ADD       
              956  INPLACE_ADD      
              958  STORE_FAST               'cmds'

 L. 203       960  LOAD_FAST                'cmds'

 L. 206       962  LOAD_GLOBAL              args
              964  LOAD_ATTR                u
              966  LOAD_STR                 ' -ublast '
              968  BINARY_ADD       
              970  LOAD_FAST                'orf_file'
              972  BINARY_ADD       
              974  LOAD_STR                 ' -db '
              976  BINARY_ADD       
              978  LOAD_GLOBAL              split_string_last
              980  LOAD_GLOBAL              args
              982  LOAD_ATTR                db
              984  LOAD_STR                 '.udb'
              986  CALL_FUNCTION_2       2  '2 positional arguments'
              988  BINARY_ADD       
              990  LOAD_FAST                'usearch_cmd'
              992  BINARY_ADD       
              994  LOAD_GLOBAL              os
              996  LOAD_ATTR                path
              998  LOAD_ATTR                join
             1000  LOAD_GLOBAL              args
             1002  LOAD_ATTR                r
             1004  LOAD_STR                 '/usearch/'
             1006  BINARY_ADD       
             1008  LOAD_GLOBAL              str
             1010  LOAD_GLOBAL              folder_id
             1012  CALL_FUNCTION_1       1  '1 positional argument'
             1014  BINARY_ADD       
             1016  LOAD_FAST                'orf_output'
             1018  LOAD_STR                 '.usearch.txt'
             1020  BINARY_ADD       
             1022  CALL_FUNCTION_2       2  '2 positional arguments'
             1024  BINARY_ADD       
             1026  LOAD_STR                 ' -threads '
             1028  BINARY_ADD       
             1030  LOAD_GLOBAL              str
             1032  LOAD_GLOBAL              int
             1034  LOAD_GLOBAL              i_max
             1036  CALL_FUNCTION_1       1  '1 positional argument'
             1038  CALL_FUNCTION_1       1  '1 positional argument'
             1040  BINARY_ADD       
             1042  LOAD_STR                 ' \n'
             1044  BINARY_ADD       
             1046  INPLACE_ADD      
             1048  STORE_FAST               'cmds'

 L. 208      1050  LOAD_FAST                'cmds'

 L. 209      1052  LOAD_STR                 'python '
             1054  LOAD_GLOBAL              workingdir
             1056  BINARY_ADD       
             1058  LOAD_STR                 '/Extract.WG.py -i '
             1060  BINARY_ADD       
             1062  LOAD_FAST                'roottemp'
             1064  BINARY_ADD       
             1066  LOAD_STR                 ' -f '
             1068  BINARY_ADD       
             1070  LOAD_FAST                'orf_output'
             1072  BINARY_ADD       
             1074  LOAD_STR                 ' -n .usearch.txt -r '
             1076  BINARY_ADD       
             1078  LOAD_GLOBAL              args
             1080  LOAD_ATTR                r
             1082  BINARY_ADD       
             1084  LOAD_STR                 '/usearch/'
             1086  BINARY_ADD       
             1088  LOAD_GLOBAL              str
             1090  LOAD_GLOBAL              folder_id
             1092  CALL_FUNCTION_1       1  '1 positional argument'
             1094  BINARY_ADD       
             1096  LOAD_STR                 ' \n'
             1098  BINARY_ADD       
             1100  INPLACE_ADD      
             1102  STORE_FAST               'cmds'

 L. 211      1104  LOAD_FAST                'cmds'

 L. 213      1106  LOAD_STR                 'python '
             1108  LOAD_GLOBAL              workingdir
             1110  BINARY_ADD       
             1112  LOAD_STR                 '/Extract.MG.py  -p 1 -i '
             1114  BINARY_ADD       
             1116  LOAD_FAST                'roottemp'
             1118  BINARY_ADD       
             1120  LOAD_STR                 ' -f '
             1122  BINARY_ADD       
             1124  LOAD_FAST                'genome_output'
             1126  BINARY_ADD       
             1128  LOAD_STR                 ' -n .usearch.txt -r '
             1130  BINARY_ADD       
             1132  LOAD_GLOBAL              args
             1134  LOAD_ATTR                r
             1136  BINARY_ADD       
             1138  LOAD_STR                 '/usearch/'
             1140  BINARY_ADD       
             1142  LOAD_GLOBAL              str
             1144  LOAD_GLOBAL              folder_id
             1146  CALL_FUNCTION_1       1  '1 positional argument'
             1148  BINARY_ADD       
             1150  LOAD_STR                 ' \n'
             1152  BINARY_ADD       
             1154  INPLACE_ADD      
             1156  STORE_FAST               'cmds'
             1158  JUMP_FORWARD       1176  'to 1176'
             1160  ELSE                     '1176'

 L. 215      1160  LOAD_GLOBAL              print
             1162  LOAD_STR                 'wrong search method for this database\nrun blast directly'
             1164  CALL_FUNCTION_1       1  '1 positional argument'
             1166  POP_TOP          

 L. 216      1168  LOAD_FAST                'genome_file'
             1170  STORE_FAST               'searchfile_genome'

 L. 217      1172  LOAD_FAST                'orf_file'
             1174  STORE_FAST               'searchfile_orf'
           1176_0  COME_FROM          1158  '1158'
           1176_1  COME_FROM           688  '688'
             1176  JUMP_FORWARD       1186  'to 1186'
             1178  ELSE                     '1186'

 L. 220      1178  LOAD_FAST                'genome_file'
             1180  STORE_FAST               'searchfile_genome'

 L. 221      1182  LOAD_FAST                'orf_file'
             1184  STORE_FAST               'searchfile_orf'
           1186_0  COME_FROM          1176  '1176'
           1186_1  COME_FROM           232  '232'

 L. 223      1186  LOAD_GLOBAL              args
             1188  LOAD_ATTR                bp
             1190  LOAD_STR                 'None'
             1192  COMPARE_OP               !=
             1194  POP_JUMP_IF_FALSE  3192  'to 3192'

 L. 224      1198  LOAD_CONST               0
             1200  STORE_FAST               'Blastsearch'

 L. 225      1202  SETUP_LOOP         1298  'to 1298'
             1204  LOAD_GLOBAL              os
             1206  LOAD_ATTR                walk
             1208  LOAD_GLOBAL              args
             1210  LOAD_ATTR                r
             1212  LOAD_STR                 '/search_output'
             1214  BINARY_ADD       
             1216  CALL_FUNCTION_1       1  '1 positional argument'
             1218  GET_ITER         
             1220  FOR_ITER           1296  'to 1296'
             1222  UNPACK_SEQUENCE_3     3 
             1224  STORE_FAST               'root'
             1226  STORE_FAST               'dirs'
             1228  STORE_FAST               'files'

 L. 226      1230  SETUP_EXCEPT       1270  'to 1270'

 L. 227      1232  LOAD_GLOBAL              os
             1234  LOAD_ATTR                path
             1236  LOAD_ATTR                join
             1238  LOAD_FAST                'root'
             1240  LOAD_FAST                'genome_output'
             1242  LOAD_STR                 '.blast.txt'
             1244  BINARY_ADD       
             1246  CALL_FUNCTION_2       2  '2 positional arguments'
             1248  STORE_FAST               'ftry_blast_file'

 L. 228      1250  LOAD_GLOBAL              open
             1252  LOAD_FAST                'ftry_blast_file'
             1254  LOAD_STR                 'r'
             1256  CALL_FUNCTION_2       2  '2 positional arguments'
             1258  STORE_FAST               'ftry_blast'

 L. 229      1260  LOAD_CONST               1
             1262  STORE_FAST               'Blastsearch'

 L. 230      1264  BREAK_LOOP       
             1266  POP_BLOCK        
             1268  JUMP_FORWARD       1292  'to 1292'
           1270_0  COME_FROM_EXCEPT   1230  '1230'

 L. 231      1270  DUP_TOP          
             1272  LOAD_GLOBAL              IOError
             1274  COMPARE_OP               exception-match
             1276  POP_JUMP_IF_FALSE  1290  'to 1290'
             1280  POP_TOP          
             1282  POP_TOP          
             1284  POP_TOP          

 L. 232      1286  POP_EXCEPT       
             1288  JUMP_FORWARD       1292  'to 1292'
             1290  END_FINALLY      
           1292_0  COME_FROM          1288  '1288'
           1292_1  COME_FROM          1268  '1268'
             1292  JUMP_BACK          1220  'to 1220'
             1296  POP_BLOCK        
           1298_0  COME_FROM_LOOP     1202  '1202'

 L. 233      1298  LOAD_FAST                'Blastsearch'
             1300  LOAD_CONST               0
             1302  COMPARE_OP               ==
             1304  POP_JUMP_IF_FALSE  1738  'to 1738'

 L. 234      1308  LOAD_GLOBAL              args
             1310  LOAD_ATTR                dbf
             1312  LOAD_CONST               2
             1314  COMPARE_OP               ==
             1316  POP_JUMP_IF_FALSE  1530  'to 1530'

 L. 236      1320  LOAD_FAST                'cmds'

 L. 238      1322  LOAD_GLOBAL              split_string_last
             1324  LOAD_GLOBAL              args
             1326  LOAD_ATTR                bp
             1328  LOAD_STR                 'blast'
             1330  CALL_FUNCTION_2       2  '2 positional arguments'
             1332  LOAD_STR                 'blastp -query '
             1334  BINARY_ADD       
             1336  LOAD_FAST                'searchfile_orf'
             1338  BINARY_ADD       
             1340  LOAD_STR                 ' -db '
             1342  BINARY_ADD       
             1344  LOAD_GLOBAL              args
             1346  LOAD_ATTR                db
             1348  BINARY_ADD       
             1350  LOAD_STR                 ' -out '
             1352  BINARY_ADD       
             1354  LOAD_GLOBAL              args
             1356  LOAD_ATTR                r
             1358  BINARY_ADD       
             1360  LOAD_STR                 '/search_output/'
             1362  BINARY_ADD       
             1364  LOAD_GLOBAL              str
             1366  LOAD_GLOBAL              folder_id
             1368  CALL_FUNCTION_1       1  '1 positional argument'
             1370  BINARY_ADD       
             1372  LOAD_STR                 '/'
             1374  BINARY_ADD       
             1376  LOAD_FAST                'orf_output'
             1378  BINARY_ADD       
             1380  LOAD_STR                 '.blast.txt  -outfmt 6  -evalue '
             1382  BINARY_ADD       
             1384  LOAD_GLOBAL              str
             1386  LOAD_GLOBAL              args
             1388  LOAD_ATTR                e
             1390  CALL_FUNCTION_1       1  '1 positional argument'
             1392  BINARY_ADD       
             1394  LOAD_STR                 ' -num_threads '
             1396  BINARY_ADD       
             1398  LOAD_GLOBAL              str
             1400  LOAD_GLOBAL              min
             1402  LOAD_GLOBAL              int
             1404  LOAD_GLOBAL              i_max
             1406  CALL_FUNCTION_1       1  '1 positional argument'
             1408  LOAD_CONST               40
             1410  CALL_FUNCTION_2       2  '2 positional arguments'
             1412  CALL_FUNCTION_1       1  '1 positional argument'
             1414  BINARY_ADD       
             1416  LOAD_STR                 ' \n'
             1418  BINARY_ADD       
             1420  INPLACE_ADD      
             1422  STORE_FAST               'cmds'

 L. 239      1424  LOAD_FAST                'cmds'

 L. 243      1426  LOAD_GLOBAL              split_string_last
             1428  LOAD_GLOBAL              args
             1430  LOAD_ATTR                bp
             1432  LOAD_STR                 'blast'
             1434  CALL_FUNCTION_2       2  '2 positional arguments'
             1436  LOAD_STR                 'blastx -query '
             1438  BINARY_ADD       
             1440  LOAD_FAST                'searchfile_genome'
             1442  BINARY_ADD       
             1444  LOAD_STR                 ' -db '
             1446  BINARY_ADD       
             1448  LOAD_GLOBAL              args
             1450  LOAD_ATTR                db
             1452  BINARY_ADD       
             1454  LOAD_STR                 ' -out '
             1456  BINARY_ADD       
             1458  LOAD_GLOBAL              args
             1460  LOAD_ATTR                r
             1462  BINARY_ADD       
             1464  LOAD_STR                 '/search_output/'
             1466  BINARY_ADD       
             1468  LOAD_GLOBAL              str
             1470  LOAD_GLOBAL              folder_id
             1472  CALL_FUNCTION_1       1  '1 positional argument'
             1474  BINARY_ADD       
             1476  LOAD_STR                 '/'
             1478  BINARY_ADD       
             1480  LOAD_FAST                'genome_output'
             1482  BINARY_ADD       
             1484  LOAD_STR                 '.blast.txt  -outfmt 6 -evalue '
             1486  BINARY_ADD       
             1488  LOAD_GLOBAL              str
             1490  LOAD_GLOBAL              args
             1492  LOAD_ATTR                e
             1494  CALL_FUNCTION_1       1  '1 positional argument'
             1496  BINARY_ADD       
             1498  LOAD_STR                 ' -num_threads '
             1500  BINARY_ADD       
             1502  LOAD_GLOBAL              str
             1504  LOAD_GLOBAL              min
             1506  LOAD_GLOBAL              int
             1508  LOAD_GLOBAL              i_max
             1510  CALL_FUNCTION_1       1  '1 positional argument'
             1512  LOAD_CONST               40
             1514  CALL_FUNCTION_2       2  '2 positional arguments'
             1516  CALL_FUNCTION_1       1  '1 positional argument'
             1518  BINARY_ADD       
             1520  LOAD_STR                 ' \n'
             1522  BINARY_ADD       
             1524  INPLACE_ADD      
             1526  STORE_FAST               'cmds'
             1528  JUMP_FORWARD       1738  'to 1738'
             1530  ELSE                     '1738'

 L. 246      1530  LOAD_FAST                'cmds'

 L. 248      1532  LOAD_GLOBAL              split_string_last
             1534  LOAD_GLOBAL              args
             1536  LOAD_ATTR                bp
             1538  LOAD_STR                 'blast'
             1540  CALL_FUNCTION_2       2  '2 positional arguments'
             1542  LOAD_STR                 'tblastn -query '
             1544  BINARY_ADD       
             1546  LOAD_FAST                'searchfile_orf'
             1548  BINARY_ADD       
             1550  LOAD_STR                 ' -db '
             1552  BINARY_ADD       
             1554  LOAD_GLOBAL              args
             1556  LOAD_ATTR                db
             1558  BINARY_ADD       
             1560  LOAD_STR                 ' -out '
             1562  BINARY_ADD       
             1564  LOAD_GLOBAL              args
             1566  LOAD_ATTR                r
             1568  BINARY_ADD       
             1570  LOAD_STR                 '/search_output/'
             1572  BINARY_ADD       
             1574  LOAD_GLOBAL              str
             1576  LOAD_GLOBAL              folder_id
             1578  CALL_FUNCTION_1       1  '1 positional argument'
             1580  BINARY_ADD       
             1582  LOAD_STR                 '/'
             1584  BINARY_ADD       
             1586  LOAD_FAST                'orf_output'
             1588  BINARY_ADD       
             1590  LOAD_STR                 '.blast.txt  -outfmt 6  -evalue '
             1592  BINARY_ADD       
             1594  LOAD_GLOBAL              str
             1596  LOAD_GLOBAL              args
             1598  LOAD_ATTR                e
             1600  CALL_FUNCTION_1       1  '1 positional argument'
             1602  BINARY_ADD       
             1604  LOAD_STR                 ' -num_threads '
             1606  BINARY_ADD       
             1608  LOAD_GLOBAL              str
             1610  LOAD_GLOBAL              min
             1612  LOAD_GLOBAL              int
             1614  LOAD_GLOBAL              i_max
             1616  CALL_FUNCTION_1       1  '1 positional argument'
             1618  LOAD_CONST               40
             1620  CALL_FUNCTION_2       2  '2 positional arguments'
             1622  CALL_FUNCTION_1       1  '1 positional argument'
             1624  BINARY_ADD       
             1626  LOAD_STR                 ' \n'
             1628  BINARY_ADD       
             1630  INPLACE_ADD      
             1632  STORE_FAST               'cmds'

 L. 249      1634  LOAD_FAST                'cmds'

 L. 253      1636  LOAD_GLOBAL              split_string_last
             1638  LOAD_GLOBAL              args
             1640  LOAD_ATTR                bp
             1642  LOAD_STR                 'blast'
             1644  CALL_FUNCTION_2       2  '2 positional arguments'
             1646  LOAD_STR                 'blastn -query '
             1648  BINARY_ADD       
             1650  LOAD_FAST                'searchfile_genome'
             1652  BINARY_ADD       
             1654  LOAD_STR                 ' -db '
             1656  BINARY_ADD       
             1658  LOAD_GLOBAL              args
             1660  LOAD_ATTR                db
             1662  BINARY_ADD       
             1664  LOAD_STR                 ' -out '
             1666  BINARY_ADD       
             1668  LOAD_GLOBAL              args
             1670  LOAD_ATTR                r
             1672  BINARY_ADD       
             1674  LOAD_STR                 '/search_output/'
             1676  BINARY_ADD       
             1678  LOAD_GLOBAL              str
             1680  LOAD_GLOBAL              folder_id
             1682  CALL_FUNCTION_1       1  '1 positional argument'
             1684  BINARY_ADD       
             1686  LOAD_STR                 '/'
             1688  BINARY_ADD       
             1690  LOAD_FAST                'genome_output'
             1692  BINARY_ADD       
             1694  LOAD_STR                 '.blast.txt  -outfmt 6 -evalue '
             1696  BINARY_ADD       
             1698  LOAD_GLOBAL              str
             1700  LOAD_GLOBAL              args
             1702  LOAD_ATTR                e
             1704  CALL_FUNCTION_1       1  '1 positional argument'
             1706  BINARY_ADD       
             1708  LOAD_STR                 ' -num_threads '
             1710  BINARY_ADD       
             1712  LOAD_GLOBAL              str
             1714  LOAD_GLOBAL              min
             1716  LOAD_GLOBAL              int
             1718  LOAD_GLOBAL              i_max
             1720  CALL_FUNCTION_1       1  '1 positional argument'
             1722  LOAD_CONST               40
             1724  CALL_FUNCTION_2       2  '2 positional arguments'
             1726  CALL_FUNCTION_1       1  '1 positional argument'
             1728  BINARY_ADD       
             1730  LOAD_STR                 ' \n'
             1732  BINARY_ADD       
             1734  INPLACE_ADD      
             1736  STORE_FAST               'cmds'
           1738_0  COME_FROM          1528  '1528'
           1738_1  COME_FROM          1304  '1304'

 L. 255      1738  LOAD_CONST               0
             1740  STORE_FAST               'Blastsearchfilter'

 L. 256      1742  SETUP_LOOP         1834  'to 1834'
             1744  LOAD_GLOBAL              os
             1746  LOAD_ATTR                walk
             1748  LOAD_GLOBAL              args
             1750  LOAD_ATTR                r
             1752  LOAD_STR                 '/search_output'
             1754  BINARY_ADD       
             1756  CALL_FUNCTION_1       1  '1 positional argument'
             1758  GET_ITER         
             1760  FOR_ITER           1832  'to 1832'
             1762  UNPACK_SEQUENCE_3     3 
             1764  STORE_FAST               'root'
             1766  STORE_FAST               'dirs'
             1768  STORE_FAST               'files'

 L. 257      1770  SETUP_EXCEPT       1806  'to 1806'

 L. 258      1772  LOAD_GLOBAL              open
             1774  LOAD_GLOBAL              os
             1776  LOAD_ATTR                path
             1778  LOAD_ATTR                join
             1780  LOAD_FAST                'root'
             1782  LOAD_FAST                'genome_output'
             1784  LOAD_STR                 '.blast.txt.filter'
             1786  BINARY_ADD       
             1788  CALL_FUNCTION_2       2  '2 positional arguments'
             1790  LOAD_STR                 'r'
             1792  CALL_FUNCTION_2       2  '2 positional arguments'
             1794  STORE_FAST               'ftry'

 L. 259      1796  LOAD_CONST               1
             1798  STORE_FAST               'Blastsearchfilter'

 L. 260      1800  BREAK_LOOP       
             1802  POP_BLOCK        
             1804  JUMP_FORWARD       1828  'to 1828'
           1806_0  COME_FROM_EXCEPT   1770  '1770'

 L. 261      1806  DUP_TOP          
             1808  LOAD_GLOBAL              IOError
             1810  COMPARE_OP               exception-match
             1812  POP_JUMP_IF_FALSE  1826  'to 1826'
             1816  POP_TOP          
             1818  POP_TOP          
             1820  POP_TOP          

 L. 262      1822  POP_EXCEPT       
             1824  JUMP_FORWARD       1828  'to 1828'
             1826  END_FINALLY      
           1828_0  COME_FROM          1824  '1824'
           1828_1  COME_FROM          1804  '1804'
             1828  JUMP_BACK          1760  'to 1760'
             1832  POP_BLOCK        
           1834_0  COME_FROM_LOOP     1742  '1742'

 L. 263      1834  LOAD_FAST                'Blastsearchfilter'
             1836  LOAD_CONST               0
             1838  COMPARE_OP               ==
             1840  POP_JUMP_IF_FALSE  2408  'to 2408'

 L. 264      1844  LOAD_FAST                'Blastsearch'
             1846  LOAD_CONST               0
             1848  COMPARE_OP               ==
             1850  POP_JUMP_IF_FALSE  1874  'to 1874'

 L. 266      1854  LOAD_GLOBAL              args
             1856  LOAD_ATTR                r
             1858  LOAD_STR                 '/search_output/'
             1860  BINARY_ADD       
             1862  LOAD_GLOBAL              str

 L. 267      1864  LOAD_GLOBAL              folder_id
             1866  CALL_FUNCTION_1       1  '1 positional argument'
             1868  BINARY_ADD       
             1870  STORE_FAST               'tempbamoutput_filter'
             1872  JUMP_FORWARD       1890  'to 1890'
             1874  ELSE                     '1890'

 L. 270      1874  LOAD_GLOBAL              os
             1876  LOAD_ATTR                path
             1878  LOAD_ATTR                split
             1880  LOAD_FAST                'ftry_blast_file'
             1882  CALL_FUNCTION_1       1  '1 positional argument'
             1884  LOAD_CONST               0
             1886  BINARY_SUBSCR    
             1888  STORE_FAST               'tempbamoutput_filter'
           1890_0  COME_FROM          1872  '1872'

 L. 271      1890  LOAD_GLOBAL              args
             1892  LOAD_ATTR                dbf
             1894  LOAD_CONST               1
             1896  COMPARE_OP               ==
             1898  POP_JUMP_IF_FALSE  2072  'to 2072'

 L. 274      1902  LOAD_FAST                'cmds'

 L. 276      1904  LOAD_STR                 'python '
             1906  LOAD_GLOBAL              workingdir
             1908  BINARY_ADD       
             1910  LOAD_STR                 '/Filter.WG.py -i '
             1912  BINARY_ADD       
             1914  LOAD_FAST                'tempbamoutput_filter'
             1916  BINARY_ADD       
             1918  LOAD_STR                 ' -f '
             1920  BINARY_ADD       
             1922  LOAD_FAST                'genome_output'
             1924  BINARY_ADD       
             1926  LOAD_STR                 '.blast.txt '
             1928  BINARY_ADD       
             1930  LOAD_STR                 '-db '
             1932  BINARY_ADD       
             1934  LOAD_GLOBAL              args
             1936  LOAD_ATTR                db
             1938  BINARY_ADD       
             1940  LOAD_STR                 ' -s '
             1942  BINARY_ADD       
             1944  LOAD_GLOBAL              str
             1946  LOAD_GLOBAL              args
             1948  LOAD_ATTR                s
             1950  CALL_FUNCTION_1       1  '1 positional argument'
             1952  BINARY_ADD       
             1954  LOAD_STR                 ' --ht '
             1956  BINARY_ADD       
             1958  LOAD_GLOBAL              str
             1960  LOAD_GLOBAL              args
             1962  LOAD_ATTR                ht
             1964  CALL_FUNCTION_1       1  '1 positional argument'
             1966  BINARY_ADD       
             1968  LOAD_STR                 ' --id '
             1970  BINARY_ADD       
             1972  LOAD_GLOBAL              str
             1974  LOAD_GLOBAL              args
             1976  LOAD_ATTR                id
             1978  CALL_FUNCTION_1       1  '1 positional argument'
             1980  BINARY_ADD       
             1982  LOAD_STR                 ' --e '
             1984  BINARY_ADD       
             1986  LOAD_GLOBAL              str
             1988  LOAD_GLOBAL              args
             1990  LOAD_ATTR                e
             1992  CALL_FUNCTION_1       1  '1 positional argument'
             1994  BINARY_ADD       
             1996  LOAD_STR                 ' \n'
             1998  BINARY_ADD       
             2000  INPLACE_ADD      
             2002  STORE_FAST               'cmds'

 L. 277      2004  LOAD_FAST                'cmds'

 L. 278      2006  LOAD_STR                 'python '
             2008  LOAD_GLOBAL              workingdir
             2010  BINARY_ADD       
             2012  LOAD_STR                 '/Extract.MG.py -p 2 -d 500 -ni .usearch.txt.aa -i '
             2014  BINARY_ADD       
             2016  LOAD_GLOBAL              os
             2018  LOAD_ATTR                path
             2020  LOAD_ATTR                split
             2022  LOAD_FAST                'searchfile_genome'
             2024  CALL_FUNCTION_1       1  '1 positional argument'
             2026  LOAD_CONST               0
             2028  BINARY_SUBSCR    
             2030  BINARY_ADD       
             2032  LOAD_STR                 ' -f '
             2034  BINARY_ADD       
             2036  LOAD_GLOBAL              os
             2038  LOAD_ATTR                path
             2040  LOAD_ATTR                split
             2042  LOAD_FAST                'searchfile_genome'
             2044  CALL_FUNCTION_1       1  '1 positional argument'
             2046  LOAD_CONST               1
             2048  BINARY_SUBSCR    
             2050  BINARY_ADD       
             2052  LOAD_STR                 ' -n .blast.txt.filter -r '
             2054  BINARY_ADD       
             2056  LOAD_FAST                'tempbamoutput_filter'
             2058  BINARY_ADD       
             2060  LOAD_STR                 ' \n'
             2062  BINARY_ADD       
             2064  INPLACE_ADD      
             2066  STORE_FAST               'cmds'
             2068  JUMP_FORWARD       2404  'to 2404'
             2072  ELSE                     '2404'

 L. 282      2072  LOAD_FAST                'cmds'

 L. 284      2074  LOAD_STR                 'python '
             2076  LOAD_GLOBAL              workingdir
             2078  BINARY_ADD       
             2080  LOAD_STR                 '/Filter.WG.py -i '
             2082  BINARY_ADD       
             2084  LOAD_FAST                'tempbamoutput_filter'
             2086  BINARY_ADD       
             2088  LOAD_STR                 ' -f '
             2090  BINARY_ADD       
             2092  LOAD_FAST                'orf_output'
             2094  BINARY_ADD       
             2096  LOAD_STR                 '.blast.txt '
             2098  BINARY_ADD       
             2100  LOAD_STR                 '-db '
             2102  BINARY_ADD       
             2104  LOAD_GLOBAL              args
             2106  LOAD_ATTR                db
             2108  BINARY_ADD       
             2110  LOAD_STR                 ' -s '
             2112  BINARY_ADD       
             2114  LOAD_GLOBAL              str
             2116  LOAD_GLOBAL              args
             2118  LOAD_ATTR                s
             2120  CALL_FUNCTION_1       1  '1 positional argument'
             2122  BINARY_ADD       
             2124  LOAD_STR                 ' --ht '
             2126  BINARY_ADD       
             2128  LOAD_GLOBAL              str
             2130  LOAD_GLOBAL              args
             2132  LOAD_ATTR                ht
             2134  CALL_FUNCTION_1       1  '1 positional argument'
             2136  BINARY_ADD       
             2138  LOAD_STR                 ' --id '
             2140  BINARY_ADD       
             2142  LOAD_GLOBAL              str
             2144  LOAD_GLOBAL              args
             2146  LOAD_ATTR                id
             2148  CALL_FUNCTION_1       1  '1 positional argument'
             2150  BINARY_ADD       
             2152  LOAD_STR                 ' --e '
             2154  BINARY_ADD       
             2156  LOAD_GLOBAL              str
             2158  LOAD_GLOBAL              args
             2160  LOAD_ATTR                e
             2162  CALL_FUNCTION_1       1  '1 positional argument'
             2164  BINARY_ADD       
             2166  LOAD_STR                 ' \n'
             2168  BINARY_ADD       
             2170  INPLACE_ADD      
             2172  STORE_FAST               'cmds'

 L. 285      2174  LOAD_FAST                'cmds'

 L. 286      2176  LOAD_STR                 'python '
             2178  LOAD_GLOBAL              workingdir
             2180  BINARY_ADD       
             2182  LOAD_STR                 '/Extract.WG.py -ni .usearch.txt.aa -i '
             2184  BINARY_ADD       
             2186  LOAD_GLOBAL              os
             2188  LOAD_ATTR                path
             2190  LOAD_ATTR                split
             2192  LOAD_FAST                'searchfile_orf'
             2194  CALL_FUNCTION_1       1  '1 positional argument'
             2196  LOAD_CONST               0
             2198  BINARY_SUBSCR    
             2200  BINARY_ADD       
             2202  LOAD_STR                 ' -f '
             2204  BINARY_ADD       
             2206  LOAD_GLOBAL              os
             2208  LOAD_ATTR                path
             2210  LOAD_ATTR                split
             2212  LOAD_FAST                'searchfile_orf'
             2214  CALL_FUNCTION_1       1  '1 positional argument'
             2216  LOAD_CONST               1
             2218  BINARY_SUBSCR    
             2220  BINARY_ADD       
             2222  LOAD_STR                 ' -n .blast.txt.filter -r '
             2224  BINARY_ADD       
             2226  LOAD_FAST                'tempbamoutput_filter'
             2228  BINARY_ADD       
             2230  LOAD_STR                 ' \n'
             2232  BINARY_ADD       
             2234  INPLACE_ADD      
             2236  STORE_FAST               'cmds'

 L. 288      2238  LOAD_FAST                'cmds'

 L. 290      2240  LOAD_STR                 'python '
             2242  LOAD_GLOBAL              workingdir
             2244  BINARY_ADD       
             2246  LOAD_STR                 '/Filter.WG.py -i '
             2248  BINARY_ADD       
             2250  LOAD_FAST                'tempbamoutput_filter'
             2252  BINARY_ADD       
             2254  LOAD_STR                 ' -f '
             2256  BINARY_ADD       
             2258  LOAD_FAST                'genome_output'
             2260  BINARY_ADD       
             2262  LOAD_STR                 '.blast.txt '
             2264  BINARY_ADD       
             2266  LOAD_STR                 '-db '
             2268  BINARY_ADD       
             2270  LOAD_GLOBAL              args
             2272  LOAD_ATTR                db
             2274  BINARY_ADD       
             2276  LOAD_STR                 ' -s '
             2278  BINARY_ADD       
             2280  LOAD_GLOBAL              str
             2282  LOAD_GLOBAL              args
             2284  LOAD_ATTR                s
             2286  CALL_FUNCTION_1       1  '1 positional argument'
             2288  BINARY_ADD       
             2290  LOAD_STR                 ' --ht '
             2292  BINARY_ADD       
             2294  LOAD_GLOBAL              str
             2296  LOAD_GLOBAL              args
             2298  LOAD_ATTR                ht
             2300  CALL_FUNCTION_1       1  '1 positional argument'
             2302  BINARY_ADD       
             2304  LOAD_STR                 ' --id '
             2306  BINARY_ADD       
             2308  LOAD_GLOBAL              str
             2310  LOAD_GLOBAL              args
             2312  LOAD_ATTR                id
             2314  CALL_FUNCTION_1       1  '1 positional argument'
             2316  BINARY_ADD       
             2318  LOAD_STR                 ' --e '
             2320  BINARY_ADD       
             2322  LOAD_GLOBAL              str
             2324  LOAD_GLOBAL              args
             2326  LOAD_ATTR                e
             2328  CALL_FUNCTION_1       1  '1 positional argument'
             2330  BINARY_ADD       
             2332  LOAD_STR                 ' \n'
             2334  BINARY_ADD       
             2336  INPLACE_ADD      
             2338  STORE_FAST               'cmds'

 L. 291      2340  LOAD_FAST                'cmds'

 L. 293      2342  LOAD_STR                 'python '
             2344  LOAD_GLOBAL              workingdir
             2346  BINARY_ADD       
             2348  LOAD_STR                 '/Extract.MG.py  -p 2 -d 500 -ni .usearch.txt.aa  -i '
             2350  BINARY_ADD       
             2352  LOAD_GLOBAL              os
             2354  LOAD_ATTR                path
             2356  LOAD_ATTR                split
             2358  LOAD_FAST                'searchfile_genome'
             2360  CALL_FUNCTION_1       1  '1 positional argument'
             2362  LOAD_CONST               0
             2364  BINARY_SUBSCR    
             2366  BINARY_ADD       
             2368  LOAD_STR                 ' -f '
             2370  BINARY_ADD       
             2372  LOAD_GLOBAL              os
             2374  LOAD_ATTR                path
             2376  LOAD_ATTR                split
             2378  LOAD_FAST                'searchfile_genome'
             2380  CALL_FUNCTION_1       1  '1 positional argument'
             2382  LOAD_CONST               1
             2384  BINARY_SUBSCR    
             2386  BINARY_ADD       
             2388  LOAD_STR                 ' -n .blast.txt.filter -r '
             2390  BINARY_ADD       
             2392  LOAD_FAST                'tempbamoutput_filter'
             2394  BINARY_ADD       
             2396  LOAD_STR                 ' \n'
             2398  BINARY_ADD       
             2400  INPLACE_ADD      
             2402  STORE_FAST               'cmds'
           2404_0  COME_FROM          2068  '2068'

 L. 294      2404  LOAD_CONST               1
             2406  STORE_FAST               'Blastsearchfilter'
           2408_0  COME_FROM          1840  '1840'

 L. 296      2408  LOAD_GLOBAL              args
             2410  LOAD_ATTR                bwa
             2412  LOAD_STR                 'None'
             2414  COMPARE_OP               !=
             2416  POP_JUMP_IF_TRUE   2442  'to 2442'
             2420  LOAD_GLOBAL              args
             2422  LOAD_ATTR                mf
             2424  LOAD_STR                 'None'
             2426  COMPARE_OP               !=
             2428  POP_JUMP_IF_FALSE  3192  'to 3192'
             2432  LOAD_FAST                'Blastsearchfilter'
             2434  LOAD_CONST               1
             2436  COMPARE_OP               ==
           2438_0  COME_FROM          2428  '2428'
           2438_1  COME_FROM          2416  '2416'
             2438  POP_JUMP_IF_FALSE  3192  'to 3192'

 L. 297      2442  LOAD_GLOBAL              os
             2444  LOAD_ATTR                path
             2446  LOAD_ATTR                join
             2448  LOAD_GLOBAL              args
             2450  LOAD_ATTR                r
             2452  LOAD_STR                 '/search_output/'
             2454  BINARY_ADD       
             2456  LOAD_GLOBAL              str
             2458  LOAD_GLOBAL              folder_id
             2460  CALL_FUNCTION_1       1  '1 positional argument'
             2462  BINARY_ADD       

 L. 298      2464  LOAD_FAST                'genome_output'
             2466  LOAD_STR                 '.blast.txt.filter.aa'
             2468  BINARY_ADD       
             2470  CALL_FUNCTION_2       2  '2 positional arguments'
             2472  STORE_FAST               'tempinput'

 L. 299      2474  LOAD_GLOBAL              os
             2476  LOAD_ATTR                path
             2478  LOAD_ATTR                join
             2480  LOAD_GLOBAL              args
             2482  LOAD_ATTR                r
             2484  LOAD_STR                 '/bwa/'
             2486  BINARY_ADD       
             2488  LOAD_GLOBAL              str
             2490  LOAD_GLOBAL              folder_id
             2492  CALL_FUNCTION_1       1  '1 positional argument'
             2494  BINARY_ADD       
             2496  LOAD_GLOBAL              str

 L. 300      2498  LOAD_FAST                'genome_output'
             2500  CALL_FUNCTION_1       1  '1 positional argument'
             2502  LOAD_STR                 '.blast.txt.filter.aa'
             2504  BINARY_ADD       
             2506  CALL_FUNCTION_2       2  '2 positional arguments'
             2508  STORE_FAST               'tempbamoutput'

 L. 301      2510  SETUP_EXCEPT       2528  'to 2528'

 L. 302      2512  LOAD_GLOBAL              open
             2514  LOAD_STR                 '%s.sorted.bam'
             2516  LOAD_FAST                'tempbamoutput'
             2518  BINARY_MODULO    
             2520  CALL_FUNCTION_1       1  '1 positional argument'
             2522  STORE_FAST               'f1'
             2524  POP_BLOCK        
             2526  JUMP_FORWARD       2676  'to 2676'
           2528_0  COME_FROM_EXCEPT   2510  '2510'

 L. 303      2528  DUP_TOP          
             2530  LOAD_GLOBAL              IOError
             2532  COMPARE_OP               exception-match
             2534  POP_JUMP_IF_FALSE  2674  'to 2674'
             2538  POP_TOP          
             2540  POP_TOP          
             2542  POP_TOP          

 L. 304      2544  LOAD_GLOBAL              args
             2546  LOAD_ATTR                bwa
             2548  LOAD_STR                 'None'
             2550  COMPARE_OP               !=
             2552  POP_JUMP_IF_FALSE  2610  'to 2610'

 L. 305      2556  LOAD_FAST                'cmds'
             2558  LOAD_GLOBAL              args
             2560  LOAD_ATTR                bwa
             2562  LOAD_STR                 ' mem %s %s |samtools view -S -b >%s.bam \nsamtools sort %s.bam -o %s.sorted.bam\n samtools index %s.sorted.bam\n'

 L. 306      2564  LOAD_GLOBAL              args
             2566  LOAD_ATTR                db
             2568  LOAD_FAST                'tempinput'

 L. 307      2570  LOAD_FAST                'tempbamoutput'
             2572  LOAD_FAST                'tempbamoutput'
             2574  LOAD_FAST                'tempbamoutput'
             2576  LOAD_FAST                'tempbamoutput'
             2578  BUILD_TUPLE_6         6 
             2580  BINARY_MODULO    
             2582  BINARY_ADD       
             2584  INPLACE_ADD      
             2586  STORE_FAST               'cmds'

 L. 308      2588  LOAD_FAST                'cmds'
             2590  LOAD_STR                 'bcftools mpileup -Ou -f %s %s.sorted.bam  | bcftools call -mv > %s.vcf\n'

 L. 309      2592  LOAD_GLOBAL              args
             2594  LOAD_ATTR                db
             2596  LOAD_FAST                'tempbamoutput'
             2598  LOAD_FAST                'tempbamoutput'
             2600  BUILD_TUPLE_3         3 
             2602  BINARY_MODULO    
             2604  INPLACE_ADD      
             2606  STORE_FAST               'cmds'
             2608  JUMP_FORWARD       2670  'to 2670'
             2610  ELSE                     '2670'

 L. 310      2610  LOAD_GLOBAL              args
             2612  LOAD_ATTR                mf
             2614  LOAD_STR                 'None'
             2616  COMPARE_OP               !=
             2618  POP_JUMP_IF_FALSE  2670  'to 2670'

 L. 312      2622  LOAD_FAST                'cmds'
             2624  LOAD_GLOBAL              args
             2626  LOAD_ATTR                bwa
             2628  LOAD_STR                 ' --nuc --adjustdirection --quiet --retree 2 --maxiterate 100 --thread %s %s > %s.align \n'

 L. 313      2630  LOAD_GLOBAL              str
             2632  LOAD_GLOBAL              int
             2634  LOAD_GLOBAL              i_max
             2636  CALL_FUNCTION_1       1  '1 positional argument'
             2638  CALL_FUNCTION_1       1  '1 positional argument'
             2640  LOAD_FAST                'tempinput'
             2642  LOAD_FAST                'tempbamoutput'
             2644  BUILD_TUPLE_3         3 
             2646  BINARY_MODULO    
             2648  BINARY_ADD       
             2650  INPLACE_ADD      
             2652  STORE_FAST               'cmds'

 L. 315      2654  LOAD_FAST                'cmds'
             2656  LOAD_STR                 'snp-sites -v -o %s.align %s.vcf \n'

 L. 316      2658  LOAD_FAST                'tempbamoutput'
             2660  LOAD_FAST                'tempbamoutput'
             2662  BUILD_TUPLE_2         2 
             2664  BINARY_MODULO    
             2666  INPLACE_ADD      
             2668  STORE_FAST               'cmds'
           2670_0  COME_FROM          2618  '2618'
           2670_1  COME_FROM          2608  '2608'
             2670  POP_EXCEPT       
             2672  JUMP_FORWARD       2676  'to 2676'
             2674  END_FINALLY      
           2676_0  COME_FROM          2672  '2672'
           2676_1  COME_FROM          2526  '2526'
             2676  JUMP_FORWARD       3192  'to 3192'
             2680  ELSE                     '3192'

 L. 319      2680  LOAD_GLOBAL              args
             2682  LOAD_ATTR                s
             2684  LOAD_CONST               2
             2686  COMPARE_OP               ==
             2688  POP_JUMP_IF_FALSE  2954  'to 2954'

 L. 321      2692  LOAD_CONST               0
             2694  STORE_FAST               'Blastsearch'

 L. 322      2696  SETUP_LOOP         2788  'to 2788'
             2698  LOAD_GLOBAL              os
             2700  LOAD_ATTR                walk
             2702  LOAD_GLOBAL              args
             2704  LOAD_ATTR                r
             2706  LOAD_STR                 '/search_output'
             2708  BINARY_ADD       
             2710  CALL_FUNCTION_1       1  '1 positional argument'
             2712  GET_ITER         
             2714  FOR_ITER           2786  'to 2786'
             2716  UNPACK_SEQUENCE_3     3 
             2718  STORE_FAST               'root'
             2720  STORE_FAST               'dirs'
             2722  STORE_FAST               'files'

 L. 323      2724  SETUP_EXCEPT       2760  'to 2760'

 L. 324      2726  LOAD_GLOBAL              open
             2728  LOAD_GLOBAL              os
             2730  LOAD_ATTR                path
             2732  LOAD_ATTR                join
             2734  LOAD_FAST                'root'
             2736  LOAD_FAST                'orf_file'
             2738  LOAD_STR                 '.hmm'
             2740  BINARY_ADD       
             2742  CALL_FUNCTION_2       2  '2 positional arguments'
             2744  LOAD_STR                 'r'
             2746  CALL_FUNCTION_2       2  '2 positional arguments'
             2748  STORE_FAST               'ftry'

 L. 325      2750  LOAD_CONST               1
             2752  STORE_FAST               'Blastsearch'

 L. 326      2754  BREAK_LOOP       
             2756  POP_BLOCK        
             2758  JUMP_FORWARD       2782  'to 2782'
           2760_0  COME_FROM_EXCEPT   2724  '2724'

 L. 327      2760  DUP_TOP          
             2762  LOAD_GLOBAL              IOError
             2764  COMPARE_OP               exception-match
             2766  POP_JUMP_IF_FALSE  2780  'to 2780'
             2770  POP_TOP          
             2772  POP_TOP          
             2774  POP_TOP          

 L. 328      2776  POP_EXCEPT       
             2778  JUMP_FORWARD       2782  'to 2782'
             2780  END_FINALLY      
           2782_0  COME_FROM          2778  '2778'
           2782_1  COME_FROM          2758  '2758'
             2782  JUMP_BACK          2714  'to 2714'
             2786  POP_BLOCK        
           2788_0  COME_FROM_LOOP     2696  '2696'

 L. 329      2788  LOAD_FAST                'Blastsearch'
             2790  LOAD_CONST               0
             2792  COMPARE_OP               ==
             2794  POP_JUMP_IF_FALSE  3192  'to 3192'

 L. 332      2798  LOAD_GLOBAL              args
             2800  LOAD_ATTR                hmm
             2802  LOAD_STR                 ' --tblout '
             2804  BINARY_ADD       
             2806  LOAD_GLOBAL              os
             2808  LOAD_ATTR                path
             2810  LOAD_ATTR                join
             2812  LOAD_GLOBAL              args
             2814  LOAD_ATTR                r
             2816  LOAD_STR                 '/search_output/'
             2818  BINARY_ADD       
             2820  LOAD_GLOBAL              str
             2822  LOAD_GLOBAL              folder_id
             2824  CALL_FUNCTION_1       1  '1 positional argument'
             2826  BINARY_ADD       
             2828  LOAD_GLOBAL              str
             2830  LOAD_FAST                'orf_output'
             2832  CALL_FUNCTION_1       1  '1 positional argument'
             2834  LOAD_STR                 '.hmm'
             2836  BINARY_ADD       
             2838  CALL_FUNCTION_2       2  '2 positional arguments'
             2840  BINARY_ADD       
             2842  LOAD_STR                 ' --cpu '
             2844  BINARY_ADD       
             2846  LOAD_GLOBAL              str
             2848  LOAD_GLOBAL              int
             2850  LOAD_GLOBAL              i_max
             2852  CALL_FUNCTION_1       1  '1 positional argument'
             2854  CALL_FUNCTION_1       1  '1 positional argument'
             2856  BINARY_ADD       
             2858  LOAD_STR                 ' -E '
             2860  BINARY_ADD       
             2862  LOAD_GLOBAL              str
             2864  LOAD_GLOBAL              args
             2866  LOAD_ATTR                e
             2868  CALL_FUNCTION_1       1  '1 positional argument'
             2870  BINARY_ADD       
             2872  LOAD_STR                 ' '
             2874  BINARY_ADD       
             2876  LOAD_GLOBAL              split_string_last
             2878  LOAD_GLOBAL              args
             2880  LOAD_ATTR                db
             2882  LOAD_STR                 '.hmm'
             2884  CALL_FUNCTION_2       2  '2 positional arguments'
             2886  BINARY_ADD       
             2888  LOAD_STR                 '.hmm '
             2890  BINARY_ADD       
             2892  LOAD_FAST                'orf_file'
             2894  BINARY_ADD       
             2896  LOAD_STR                 ' \n'
             2898  BINARY_ADD       
             2900  STORE_FAST               'cmds'

 L. 333      2902  LOAD_FAST                'cmds'

 L. 334      2904  LOAD_STR                 'python '
             2906  LOAD_GLOBAL              workingdir
             2908  BINARY_ADD       
             2910  LOAD_STR                 '/Format.WG.py -i '
             2912  BINARY_ADD       
             2914  LOAD_GLOBAL              args
             2916  LOAD_ATTR                r
             2918  BINARY_ADD       
             2920  LOAD_STR                 '/search_output/'
             2922  BINARY_ADD       
             2924  LOAD_GLOBAL              str
             2926  LOAD_GLOBAL              folder_id
             2928  CALL_FUNCTION_1       1  '1 positional argument'
             2930  BINARY_ADD       
             2932  LOAD_STR                 ' -f '
             2934  BINARY_ADD       
             2936  LOAD_GLOBAL              str
             2938  LOAD_FAST                'orf_output'
             2940  CALL_FUNCTION_1       1  '1 positional argument'
             2942  BINARY_ADD       
             2944  LOAD_STR                 '.hmm \n'
             2946  BINARY_ADD       
             2948  INPLACE_ADD      
             2950  STORE_FAST               'cmds'
             2952  JUMP_FORWARD       3192  'to 3192'
             2954  ELSE                     '3192'

 L. 335      2954  LOAD_GLOBAL              args
             2956  LOAD_ATTR                s
             2958  LOAD_CONST               3
             2960  COMPARE_OP               ==
             2962  POP_JUMP_IF_FALSE  3192  'to 3192'

 L. 337      2966  LOAD_GLOBAL              os
             2968  LOAD_ATTR                path
             2970  LOAD_ATTR                join
             2972  LOAD_FAST                'roottemp'
             2974  LOAD_GLOBAL              str

 L. 338      2976  LOAD_FAST                'genome_output'
             2978  CALL_FUNCTION_1       1  '1 positional argument'
             2980  CALL_FUNCTION_2       2  '2 positional arguments'
             2982  STORE_FAST               'tempinput'

 L. 339      2984  LOAD_GLOBAL              os
             2986  LOAD_ATTR                path
             2988  LOAD_ATTR                join
             2990  LOAD_GLOBAL              args
             2992  LOAD_ATTR                r
             2994  LOAD_STR                 '/bwa/'
             2996  BINARY_ADD       
             2998  LOAD_GLOBAL              str
             3000  LOAD_GLOBAL              folder_id
             3002  CALL_FUNCTION_1       1  '1 positional argument'
             3004  BINARY_ADD       
             3006  LOAD_GLOBAL              str

 L. 340      3008  LOAD_FAST                'genome_output'
             3010  CALL_FUNCTION_1       1  '1 positional argument'
             3012  CALL_FUNCTION_2       2  '2 positional arguments'
             3014  STORE_FAST               'tempbamoutput'

 L. 341      3016  SETUP_EXCEPT       3034  'to 3034'

 L. 342      3018  LOAD_GLOBAL              open
             3020  LOAD_STR                 '%s.sorted.bam'
             3022  LOAD_FAST                'tempbamoutput'
             3024  BINARY_MODULO    
             3026  CALL_FUNCTION_1       1  '1 positional argument'
             3028  STORE_FAST               'f1'
             3030  POP_BLOCK        
             3032  JUMP_FORWARD       3192  'to 3192'
           3034_0  COME_FROM_EXCEPT   3016  '3016'

 L. 343      3034  DUP_TOP          
             3036  LOAD_GLOBAL              IOError
             3038  COMPARE_OP               exception-match
             3040  POP_JUMP_IF_FALSE  3190  'to 3190'
             3044  POP_TOP          
             3046  POP_TOP          
             3048  POP_TOP          

 L. 344      3050  LOAD_GLOBAL              args
             3052  LOAD_ATTR                bwa
             3054  LOAD_STR                 'None'
             3056  COMPARE_OP               !=
             3058  POP_JUMP_IF_FALSE  3116  'to 3116'

 L. 345      3062  LOAD_FAST                'cmds'
             3064  LOAD_GLOBAL              args
             3066  LOAD_ATTR                bwa
             3068  LOAD_STR                 ' mem %s %s |samtools view -S -b >%s.bam \nsamtools sort %s.bam -o %s.sorted.bam\n samtools index %s.sorted.bam\n'

 L. 346      3070  LOAD_GLOBAL              args
             3072  LOAD_ATTR                db
             3074  LOAD_FAST                'tempinput'

 L. 347      3076  LOAD_FAST                'tempbamoutput'
             3078  LOAD_FAST                'tempbamoutput'
             3080  LOAD_FAST                'tempbamoutput'
             3082  LOAD_FAST                'tempbamoutput'
             3084  BUILD_TUPLE_6         6 
             3086  BINARY_MODULO    
             3088  BINARY_ADD       
             3090  INPLACE_ADD      
             3092  STORE_FAST               'cmds'

 L. 348      3094  LOAD_FAST                'cmds'
             3096  LOAD_STR                 'bcftools mpileup -Ou -f %s %s.sorted.bam  | bcftools call -mv > %s.vcf\n'

 L. 349      3098  LOAD_GLOBAL              args
             3100  LOAD_ATTR                db
             3102  LOAD_FAST                'tempbamoutput'
             3104  LOAD_FAST                'tempbamoutput'
             3106  BUILD_TUPLE_3         3 
             3108  BINARY_MODULO    
             3110  INPLACE_ADD      
             3112  STORE_FAST               'cmds'
             3114  JUMP_FORWARD       3186  'to 3186'
             3116  ELSE                     '3186'

 L. 350      3116  LOAD_GLOBAL              args
             3118  LOAD_ATTR                mf
             3120  LOAD_STR                 'None'
             3122  COMPARE_OP               !=
             3124  POP_JUMP_IF_FALSE  3178  'to 3178'

 L. 352      3128  LOAD_FAST                'cmds'
             3130  LOAD_GLOBAL              args
             3132  LOAD_ATTR                bwa
             3134  LOAD_STR                 ' --nuc --adjustdirection --quiet --retree 2 --maxiterate 100 --thread %s %s > %s.align \n'

 L. 353      3136  LOAD_GLOBAL              str
             3138  LOAD_GLOBAL              int
             3140  LOAD_GLOBAL              i_max
             3142  CALL_FUNCTION_1       1  '1 positional argument'
             3144  CALL_FUNCTION_1       1  '1 positional argument'
             3146  LOAD_FAST                'tempinput'
             3148  LOAD_FAST                'tempbamoutput'
             3150  BUILD_TUPLE_3         3 
             3152  BINARY_MODULO    
             3154  BINARY_ADD       
             3156  INPLACE_ADD      
             3158  STORE_FAST               'cmds'

 L. 355      3160  LOAD_FAST                'cmds'
             3162  LOAD_STR                 'snp-sites -v -o %s.align %s.vcf \n'

 L. 356      3164  LOAD_FAST                'tempbamoutput'
             3166  LOAD_FAST                'tempbamoutput'
             3168  BUILD_TUPLE_2         2 
             3170  BINARY_MODULO    
             3172  INPLACE_ADD      
             3174  STORE_FAST               'cmds'
             3176  JUMP_FORWARD       3186  'to 3186'
             3178  ELSE                     '3186'

 L. 358      3178  LOAD_GLOBAL              print
             3180  LOAD_STR                 'please provide --bwa or --mafft for alignment (--s 3)'
             3182  CALL_FUNCTION_1       1  '1 positional argument'
             3184  POP_TOP          
           3186_0  COME_FROM          3176  '3176'
           3186_1  COME_FROM          3114  '3114'
             3186  POP_EXCEPT       
             3188  JUMP_FORWARD       3192  'to 3192'
             3190  END_FINALLY      
           3192_0  COME_FROM          3188  '3188'
           3192_1  COME_FROM          3032  '3032'
           3192_2  COME_FROM          2962  '2962'
           3192_3  COME_FROM          2952  '2952'
           3192_4  COME_FROM          2794  '2794'
           3192_5  COME_FROM          2676  '2676'
           3192_6  COME_FROM          2438  '2438'

 L. 360      3192  LOAD_CONST               0
             3194  STORE_FAST               'Search16s'

 L. 361      3196  SETUP_LOOP         3284  'to 3284'
             3198  LOAD_GLOBAL              os
             3200  LOAD_ATTR                walk
             3202  LOAD_GLOBAL              args
             3204  LOAD_ATTR                r16
             3206  CALL_FUNCTION_1       1  '1 positional argument'
             3208  GET_ITER         
             3210  FOR_ITER           3282  'to 3282'
             3212  UNPACK_SEQUENCE_3     3 
             3214  STORE_FAST               'root'
             3216  STORE_FAST               'dirs'
             3218  STORE_FAST               'files'

 L. 362      3220  SETUP_EXCEPT       3256  'to 3256'

 L. 363      3222  LOAD_GLOBAL              open
             3224  LOAD_GLOBAL              os
             3226  LOAD_ATTR                path
             3228  LOAD_ATTR                join
             3230  LOAD_FAST                'root'
             3232  LOAD_FAST                'genome_output'
             3234  LOAD_STR                 '.16S.txt'
             3236  BINARY_ADD       
             3238  CALL_FUNCTION_2       2  '2 positional arguments'
             3240  LOAD_STR                 'r'
             3242  CALL_FUNCTION_2       2  '2 positional arguments'
             3244  STORE_FAST               'ftry'

 L. 364      3246  LOAD_CONST               1
             3248  STORE_FAST               'Search16s'

 L. 365      3250  BREAK_LOOP       
             3252  POP_BLOCK        
             3254  JUMP_FORWARD       3278  'to 3278'
           3256_0  COME_FROM_EXCEPT   3220  '3220'

 L. 366      3256  DUP_TOP          
             3258  LOAD_GLOBAL              IOError
             3260  COMPARE_OP               exception-match
             3262  POP_JUMP_IF_FALSE  3276  'to 3276'
             3266  POP_TOP          
             3268  POP_TOP          
             3270  POP_TOP          

 L. 367      3272  POP_EXCEPT       
             3274  JUMP_FORWARD       3278  'to 3278'
             3276  END_FINALLY      
           3278_0  COME_FROM          3274  '3274'
           3278_1  COME_FROM          3254  '3254'
             3278  JUMP_BACK          3210  'to 3210'
             3282  POP_BLOCK        
           3284_0  COME_FROM_LOOP     3196  '3196'

 L. 368      3284  LOAD_FAST                'Search16s'
             3286  LOAD_CONST               0
             3288  COMPARE_OP               ==
             3290  POP_JUMP_IF_FALSE  3662  'to 3662'

 L. 369      3294  LOAD_GLOBAL              args
             3296  LOAD_ATTR                hs
             3298  LOAD_STR                 'None'
             3300  COMPARE_OP               !=
             3302  POP_JUMP_IF_FALSE  3480  'to 3480'

 L. 373      3306  LOAD_FAST                'cmds'
             3308  LOAD_STR                 'python '
             3310  LOAD_GLOBAL              workingdir
             3312  BINARY_ADD       
             3314  LOAD_STR                 '/undone.WG.py -i '
             3316  BINARY_ADD       
             3318  LOAD_GLOBAL              os
             3320  LOAD_ATTR                path
             3322  LOAD_ATTR                join
             3324  LOAD_FAST                'roottemp'
             3326  LOAD_FAST                'genome_output'
             3328  LOAD_STR                 ' \n'
             3330  BINARY_ADD       
             3332  CALL_FUNCTION_2       2  '2 positional arguments'
             3334  BINARY_ADD       
             3336  INPLACE_ADD      
             3338  STORE_FAST               'cmds'

 L. 374      3340  LOAD_FAST                'cmds'
             3342  LOAD_STR                 '%s align -db %s -window_masker_db %s.counts.obinary -query %s -out %s -outfmt 6 -evalue %s -num_threads %s\n'

 L. 375      3344  LOAD_GLOBAL              args
             3346  LOAD_ATTR                hs
             3348  LOAD_GLOBAL              workingdir
             3350  LOAD_STR                 '/../database/85_otus.fasta'
             3352  BINARY_ADD       

 L. 376      3354  LOAD_GLOBAL              workingdir
             3356  LOAD_STR                 '/../database/85_otus.fasta'
             3358  BINARY_ADD       
             3360  LOAD_FAST                'genome_file'
             3362  LOAD_GLOBAL              os
             3364  LOAD_ATTR                path
             3366  LOAD_ATTR                join

 L. 377      3368  LOAD_GLOBAL              args
             3370  LOAD_ATTR                r16
             3372  LOAD_STR                 '/'
             3374  BINARY_ADD       
             3376  LOAD_GLOBAL              str
             3378  LOAD_GLOBAL              folder_id
             3380  CALL_FUNCTION_1       1  '1 positional argument'
             3382  BINARY_ADD       

 L. 378      3384  LOAD_FAST                'genome_output'
             3386  LOAD_STR                 '.16S.txt'
             3388  BINARY_ADD       
             3390  CALL_FUNCTION_2       2  '2 positional arguments'

 L. 379      3392  LOAD_GLOBAL              str
             3394  LOAD_GLOBAL              args
             3396  LOAD_ATTR                e
             3398  CALL_FUNCTION_1       1  '1 positional argument'
             3400  LOAD_GLOBAL              str
             3402  LOAD_GLOBAL              min
             3404  LOAD_GLOBAL              int
             3406  LOAD_GLOBAL              i_max
             3408  CALL_FUNCTION_1       1  '1 positional argument'
             3410  LOAD_CONST               40
             3412  CALL_FUNCTION_2       2  '2 positional arguments'
             3414  CALL_FUNCTION_1       1  '1 positional argument'
             3416  BUILD_TUPLE_7         7 
             3418  BINARY_MODULO    
             3420  INPLACE_ADD      
             3422  STORE_FAST               'cmds'

 L. 380      3424  LOAD_FAST                'cmds'

 L. 382      3426  LOAD_STR                 'python '
             3428  LOAD_GLOBAL              workingdir
             3430  BINARY_ADD       
             3432  LOAD_STR                 '/Extract.16S.WG.py -i '
             3434  BINARY_ADD       
             3436  LOAD_FAST                'roottemp'
             3438  BINARY_ADD       
             3440  LOAD_STR                 ' -f '
             3442  BINARY_ADD       
             3444  LOAD_FAST                'genome_output'
             3446  BINARY_ADD       
             3448  LOAD_STR                 ' -n .16S.txt -r '
             3450  BINARY_ADD       
             3452  LOAD_GLOBAL              args
             3454  LOAD_ATTR                r16
             3456  BINARY_ADD       
             3458  LOAD_STR                 '/'
             3460  BINARY_ADD       
             3462  LOAD_GLOBAL              str
             3464  LOAD_GLOBAL              folder_id
             3466  CALL_FUNCTION_1       1  '1 positional argument'
             3468  BINARY_ADD       
             3470  LOAD_STR                 ' \n'
             3472  BINARY_ADD       
             3474  INPLACE_ADD      
             3476  STORE_FAST               'cmds'
             3478  JUMP_FORWARD       3662  'to 3662'
             3480  ELSE                     '3662'

 L. 384      3480  LOAD_GLOBAL              args
             3482  LOAD_ATTR                u
             3484  LOAD_STR                 'None'
             3486  COMPARE_OP               !=
             3488  POP_JUMP_IF_FALSE  3662  'to 3662'

 L. 386      3492  LOAD_FAST                'cmds'
             3494  LOAD_STR                 'python '
             3496  LOAD_GLOBAL              workingdir
             3498  BINARY_ADD       
             3500  LOAD_STR                 '/undone.WG.py -i '
             3502  BINARY_ADD       
             3504  LOAD_GLOBAL              os
             3506  LOAD_ATTR                path
             3508  LOAD_ATTR                join
             3510  LOAD_FAST                'roottemp'
             3512  LOAD_FAST                'genome_output'
             3514  LOAD_STR                 ' \n'
             3516  BINARY_ADD       
             3518  CALL_FUNCTION_2       2  '2 positional arguments'
             3520  BINARY_ADD       
             3522  INPLACE_ADD      
             3524  STORE_FAST               'cmds'

 L. 387      3526  LOAD_FAST                'cmds'

 L. 390      3528  LOAD_GLOBAL              args
             3530  LOAD_ATTR                u
             3532  LOAD_STR                 ' -usearch_global '
             3534  BINARY_ADD       
             3536  LOAD_FAST                'genome_file'
             3538  BINARY_ADD       
             3540  LOAD_STR                 ' -db '
             3542  BINARY_ADD       
             3544  LOAD_GLOBAL              workingdir
             3546  BINARY_ADD       
             3548  LOAD_STR                 '/../database/85_otus.fasta.udb -strand plus -id 0.7 -evalue 1e-1 -blast6out '
             3550  BINARY_ADD       
             3552  LOAD_GLOBAL              os
             3554  LOAD_ATTR                path
             3556  LOAD_ATTR                join
             3558  LOAD_GLOBAL              args
             3560  LOAD_ATTR                r16
             3562  LOAD_STR                 '/'
             3564  BINARY_ADD       
             3566  LOAD_GLOBAL              str
             3568  LOAD_GLOBAL              folder_id
             3570  CALL_FUNCTION_1       1  '1 positional argument'
             3572  BINARY_ADD       
             3574  LOAD_FAST                'genome_output'
             3576  LOAD_STR                 '.16S.txt'
             3578  BINARY_ADD       
             3580  CALL_FUNCTION_2       2  '2 positional arguments'
             3582  BINARY_ADD       
             3584  LOAD_STR                 ' -threads '
             3586  BINARY_ADD       
             3588  LOAD_GLOBAL              str
             3590  LOAD_GLOBAL              int
             3592  LOAD_GLOBAL              i_max
             3594  CALL_FUNCTION_1       1  '1 positional argument'
             3596  CALL_FUNCTION_1       1  '1 positional argument'
             3598  BINARY_ADD       
             3600  LOAD_STR                 ' \n'
             3602  BINARY_ADD       
             3604  INPLACE_ADD      
             3606  STORE_FAST               'cmds'

 L. 391      3608  LOAD_FAST                'cmds'

 L. 393      3610  LOAD_STR                 'python '
             3612  LOAD_GLOBAL              workingdir
             3614  BINARY_ADD       
             3616  LOAD_STR                 '/Extract.16S.WG.py -i '
             3618  BINARY_ADD       
             3620  LOAD_FAST                'roottemp'
             3622  BINARY_ADD       
             3624  LOAD_STR                 ' -f '
             3626  BINARY_ADD       
             3628  LOAD_FAST                'genome_output'
             3630  BINARY_ADD       
             3632  LOAD_STR                 ' -n .16S.txt -r '
             3634  BINARY_ADD       
             3636  LOAD_GLOBAL              args
             3638  LOAD_ATTR                r16
             3640  BINARY_ADD       
             3642  LOAD_STR                 '/'
             3644  BINARY_ADD       
             3646  LOAD_GLOBAL              str
             3648  LOAD_GLOBAL              folder_id
             3650  CALL_FUNCTION_1       1  '1 positional argument'
             3652  BINARY_ADD       
             3654  LOAD_STR                 ' \n'
             3656  BINARY_ADD       
             3658  INPLACE_ADD      
             3660  STORE_FAST               'cmds'
           3662_0  COME_FROM          3488  '3488'
           3662_1  COME_FROM          3478  '3478'
           3662_2  COME_FROM          3290  '3290'

 L. 394      3662  LOAD_FAST                'cmds'
             3664  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `COME_FROM' instruction at offset 834_0


i = 0
i_max = int(args.t)
try:
    os.mkdir('subscripts')
except OSError:
    pass

try:
    os.mkdir(args.r + '/search_output')
except OSError:
    pass

try:
    os.mkdir(args.r + '/usearch')
except OSError:
    pass

try:
    os.mkdir(args.r16)
except OSError:
    pass

if args.bwa != 'None':
    try:
        os.mkdir(args.r + '/bwa/')
    except OSError:
        pass

folder_id = 0
try:
    os.mkdir(args.r + '/search_output/' + str(folder_id))
except OSError:
    pass

try:
    os.mkdir(args.r + '/usearch/' + str(folder_id))
except OSError:
    pass

try:
    os.mkdir(args.r16 + '/' + str(folder_id))
except OSError:
    pass

if args.bwa != 'None':
    try:
        os.mkdir(args.r + '/bwa/' + str(folder_id))
    except OSError:
        pass

flist = open('Filelist.txt', 'w')
flist_list = []
in_dir = args.i
for root, dirs, files in os.walk(in_dir):
    if fasta_format != 'None':
        list_fasta1 = glob.glob(os.path.join(root, '*' + fasta_format))
        if list_fasta1 != []:
            for genomefile in list_fasta1:
                f1 = open(os.path.join('subscripts', str(i % int(args.t)) + '.sh'), 'a')
                i += 1
                roottemp, genomefilename = os.path.split(genomefile)
                flist_list.append(str(genomefile))
                folder_id = int(i / 10000)
                if folder_id > int(i - 0.0001):
                    try:
                        os.mkdir(args.r + '/search_output/' + str(folder_id))
                    except OSError:
                        pass

                    try:
                        os.mkdir(args.r + '/usearch/' + str(folder_id))
                    except OSError:
                        pass

                    try:
                        os.mkdir(args.r16 + '/' + str(folder_id))
                    except OSError:
                        pass

                    if args.bwa != 'None':
                        try:
                            os.mkdir(args.r + '/bwa/' + str(folder_id))
                        except OSError:
                            pass

                orffile = split_string_last(genomefile, fasta_format) + orfs_format
                orffilename = split_string_last(genomefilename, fasta_format) + orfs_format
                try:
                    ftry_orf = open(orffile, 'r')
                except IOError:
                    if args.pro != 'None':
                        os.system('%s -q -a %s -i %s' % (args.pro, orffile, genomefile))

                if '.add' not in orffile:
                    try:
                        ftry = open(orffile + '.add', 'r')
                    except IOError:
                        addname(orffile)

                    orffile = orffile + '.add'
                    orffilename = orffilename + '.add'
                cmds = search(roottemp, genomefilename, orffilename)
                f1.write(cmds)
                f1.close()

flist.write('\n'.join(flist_list))
flist.close()