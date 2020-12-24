# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/zxh/LncrnaPackage/models/LncADeep/LncADeep_lncRNA/LncADeep_partial/bin/utils.py
# Compiled at: 2019-10-31 08:43:41
# Size of source mod 2**32: 3157 bytes
import sys, numpy as np
np.seterr(all='ignore')

def sigmoid(x):
    return 1.0 / (1.0 + np.exp(-x))


def d_sigmoid(x):
    return sigmoid(x) * (1 - sigmoid(x))


def GetFasta(inputfile):
    """Get sequence from input, seqid=the first part without space"""
    try:
        f = open(inputfile, 'r')
    except (IOError, ValueError) as e:
        try:
            (
             print >> sys.stderr, str(e))
            sys.exit(1)
        finally:
            e = None
            del e

    tmpseq = ''
    seqlist = []
    seqID = []
    for line in f.readlines():
        line = line.strip()
        if not len(line):
            continue
        elif line[0] == '>':
            seqID.append(line.split()[0][1:])
            if tmpseq != '':
                seqlist.append(tmpseq)
            tmpseq = ''
        else:
            tmpseq += line.upper()

    seqlist.append(tmpseq)
    f.close()
    return [
     seqID, seqlist]


def RevComp(seq):
    """reverse complement of sequence"""
    complement = {'A':'T', 
     'C':'G',  'G':'C',  'T':'A',  'a':'T',  'c':'G',  'g':'C',  't':'A'}
    reverse_complement = ''.join((complement.get(base, base) for base in reversed(seq)))
    return reverse_complement


def Codon2AA2--- This code section failed: ---

 L.  50         0  LOAD_FAST                'codon'
                2  LOAD_STR                 'TTT'
                4  COMPARE_OP               ==
                6  POP_JUMP_IF_TRUE     16  'to 16'
                8  LOAD_FAST                'codon'
               10  LOAD_STR                 'TTC'
               12  COMPARE_OP               ==
               14  POP_JUMP_IF_FALSE    20  'to 20'
             16_0  COME_FROM             6  '6'

 L.  51        16  LOAD_STR                 'F'
               18  RETURN_VALUE     
             20_0  COME_FROM            14  '14'

 L.  52        20  LOAD_FAST                'codon'
               22  LOAD_STR                 'TTA'
               24  COMPARE_OP               ==
               26  POP_JUMP_IF_TRUE     68  'to 68'
               28  LOAD_FAST                'codon'
               30  LOAD_STR                 'TTG'
               32  COMPARE_OP               ==
               34  POP_JUMP_IF_TRUE     68  'to 68'
               36  LOAD_FAST                'codon'
               38  LOAD_STR                 'CTT'
               40  COMPARE_OP               ==
               42  POP_JUMP_IF_TRUE     68  'to 68'
               44  LOAD_FAST                'codon'
               46  LOAD_STR                 'CTA'
               48  COMPARE_OP               ==
               50  POP_JUMP_IF_TRUE     68  'to 68'
               52  LOAD_FAST                'codon'
               54  LOAD_STR                 'CTC'
               56  COMPARE_OP               ==
               58  POP_JUMP_IF_TRUE     68  'to 68'
               60  LOAD_FAST                'codon'
               62  LOAD_STR                 'CTG'
               64  COMPARE_OP               ==
               66  POP_JUMP_IF_FALSE    72  'to 72'
             68_0  COME_FROM            58  '58'
             68_1  COME_FROM            50  '50'
             68_2  COME_FROM            42  '42'
             68_3  COME_FROM            34  '34'
             68_4  COME_FROM            26  '26'

 L.  53        68  LOAD_STR                 'L'
               70  RETURN_VALUE     
             72_0  COME_FROM            66  '66'

 L.  54        72  LOAD_FAST                'codon'
               74  LOAD_STR                 'ATT'
               76  COMPARE_OP               ==
               78  POP_JUMP_IF_TRUE     96  'to 96'
               80  LOAD_FAST                'codon'
               82  LOAD_STR                 'ATC'
               84  COMPARE_OP               ==
               86  POP_JUMP_IF_TRUE     96  'to 96'
               88  LOAD_FAST                'codon'
               90  LOAD_STR                 'ATA'
               92  COMPARE_OP               ==
               94  POP_JUMP_IF_FALSE   100  'to 100'
             96_0  COME_FROM            86  '86'
             96_1  COME_FROM            78  '78'

 L.  55        96  LOAD_STR                 'I'
               98  RETURN_VALUE     
            100_0  COME_FROM            94  '94'

 L.  56       100  LOAD_FAST                'codon'
              102  LOAD_STR                 'ATG'
              104  COMPARE_OP               ==
              106  POP_JUMP_IF_FALSE   112  'to 112'

 L.  57       108  LOAD_STR                 'M'
              110  RETURN_VALUE     
            112_0  COME_FROM           106  '106'

 L.  58       112  LOAD_FAST                'codon'
              114  LOAD_STR                 'GTA'
              116  COMPARE_OP               ==
              118  POP_JUMP_IF_TRUE    144  'to 144'
              120  LOAD_FAST                'codon'
              122  LOAD_STR                 'GTC'
              124  COMPARE_OP               ==
              126  POP_JUMP_IF_TRUE    144  'to 144'
              128  LOAD_FAST                'codon'
              130  LOAD_STR                 'GTG'
              132  COMPARE_OP               ==
              134  POP_JUMP_IF_TRUE    144  'to 144'
              136  LOAD_FAST                'codon'
              138  LOAD_STR                 'GTT'
              140  COMPARE_OP               ==
              142  POP_JUMP_IF_FALSE   148  'to 148'
            144_0  COME_FROM           134  '134'
            144_1  COME_FROM           126  '126'
            144_2  COME_FROM           118  '118'

 L.  59       144  LOAD_STR                 'V'
              146  RETURN_VALUE     
            148_0  COME_FROM           142  '142'

 L.  60       148  LOAD_FAST                'codon'
              150  LOAD_STR                 'GAT'
              152  COMPARE_OP               ==
              154  POP_JUMP_IF_TRUE    164  'to 164'
              156  LOAD_FAST                'codon'
              158  LOAD_STR                 'GAC'
              160  COMPARE_OP               ==
              162  POP_JUMP_IF_FALSE   168  'to 168'
            164_0  COME_FROM           154  '154'

 L.  61       164  LOAD_STR                 'D'
              166  RETURN_VALUE     
            168_0  COME_FROM           162  '162'

 L.  62       168  LOAD_FAST                'codon'
              170  LOAD_STR                 'GAA'
              172  COMPARE_OP               ==
              174  POP_JUMP_IF_TRUE    184  'to 184'
              176  LOAD_FAST                'codon'
              178  LOAD_STR                 'GAG'
              180  COMPARE_OP               ==
              182  POP_JUMP_IF_FALSE   188  'to 188'
            184_0  COME_FROM           174  '174'

 L.  63       184  LOAD_STR                 'E'
              186  RETURN_VALUE     
            188_0  COME_FROM           182  '182'

 L.  64       188  LOAD_FAST                'codon'
              190  LOAD_STR                 'TCA'
              192  COMPARE_OP               ==
              194  POP_JUMP_IF_TRUE    222  'to 222'
              196  LOAD_FAST                'codon'
              198  LOAD_STR                 'TCC'
              200  COMPARE_OP               ==
              202  POP_JUMP_IF_TRUE    222  'to 222'
              204  LOAD_FAST                'codon'
              206  LOAD_STR                 'TCG'
              208  COMPARE_OP               ==
              210  POP_JUMP_IF_TRUE    222  'to 222'
              212  LOAD_FAST                'codon'
              214  LOAD_STR                 'TCT'
              216  COMPARE_OP               ==
          218_220  POP_JUMP_IF_FALSE   226  'to 226'
            222_0  COME_FROM           210  '210'
            222_1  COME_FROM           202  '202'
            222_2  COME_FROM           194  '194'

 L.  65       222  LOAD_STR                 'S'
              224  RETURN_VALUE     
            226_0  COME_FROM           218  '218'

 L.  66       226  LOAD_FAST                'codon'
              228  LOAD_STR                 'CCA'
              230  COMPARE_OP               ==
          232_234  POP_JUMP_IF_TRUE    266  'to 266'
              236  LOAD_FAST                'codon'
              238  LOAD_STR                 'CCC'
              240  COMPARE_OP               ==
          242_244  POP_JUMP_IF_TRUE    266  'to 266'
              246  LOAD_FAST                'codon'
              248  LOAD_STR                 'CCG'
              250  COMPARE_OP               ==
          252_254  POP_JUMP_IF_TRUE    266  'to 266'
              256  LOAD_FAST                'codon'
              258  LOAD_STR                 'CCT'
              260  COMPARE_OP               ==
          262_264  POP_JUMP_IF_FALSE   270  'to 270'
            266_0  COME_FROM           252  '252'
            266_1  COME_FROM           242  '242'
            266_2  COME_FROM           232  '232'

 L.  67       266  LOAD_STR                 'P'
              268  RETURN_VALUE     
            270_0  COME_FROM           262  '262'

 L.  68       270  LOAD_FAST                'codon'
              272  LOAD_STR                 'ACA'
              274  COMPARE_OP               ==
          276_278  POP_JUMP_IF_TRUE    310  'to 310'
              280  LOAD_FAST                'codon'
              282  LOAD_STR                 'ACG'
              284  COMPARE_OP               ==
          286_288  POP_JUMP_IF_TRUE    310  'to 310'
              290  LOAD_FAST                'codon'
              292  LOAD_STR                 'ACT'
              294  COMPARE_OP               ==
          296_298  POP_JUMP_IF_TRUE    310  'to 310'
              300  LOAD_FAST                'codon'
              302  LOAD_STR                 'ACC'
              304  COMPARE_OP               ==
          306_308  POP_JUMP_IF_FALSE   314  'to 314'
            310_0  COME_FROM           296  '296'
            310_1  COME_FROM           286  '286'
            310_2  COME_FROM           276  '276'

 L.  69       310  LOAD_STR                 'T'
              312  RETURN_VALUE     
            314_0  COME_FROM           306  '306'

 L.  70       314  LOAD_FAST                'codon'
              316  LOAD_STR                 'GCA'
              318  COMPARE_OP               ==
          320_322  POP_JUMP_IF_TRUE    354  'to 354'
              324  LOAD_FAST                'codon'
              326  LOAD_STR                 'GCC'
              328  COMPARE_OP               ==
          330_332  POP_JUMP_IF_TRUE    354  'to 354'
              334  LOAD_FAST                'codon'
              336  LOAD_STR                 'GCG'
              338  COMPARE_OP               ==
          340_342  POP_JUMP_IF_TRUE    354  'to 354'
              344  LOAD_FAST                'codon'
              346  LOAD_STR                 'GCT'
              348  COMPARE_OP               ==
          350_352  POP_JUMP_IF_FALSE   358  'to 358'
            354_0  COME_FROM           340  '340'
            354_1  COME_FROM           330  '330'
            354_2  COME_FROM           320  '320'

 L.  71       354  LOAD_STR                 'A'
              356  RETURN_VALUE     
            358_0  COME_FROM           350  '350'

 L.  72       358  LOAD_FAST                'codon'
              360  LOAD_STR                 'TAT'
              362  COMPARE_OP               ==
          364_366  POP_JUMP_IF_TRUE    378  'to 378'
              368  LOAD_FAST                'codon'
              370  LOAD_STR                 'TAC'
              372  COMPARE_OP               ==
          374_376  POP_JUMP_IF_FALSE   382  'to 382'
            378_0  COME_FROM           364  '364'

 L.  73       378  LOAD_STR                 'Y'
              380  RETURN_VALUE     
            382_0  COME_FROM           374  '374'

 L.  74       382  LOAD_FAST                'codon'
              384  LOAD_STR                 'CAT'
              386  COMPARE_OP               ==
          388_390  POP_JUMP_IF_TRUE    402  'to 402'
              392  LOAD_FAST                'codon'
              394  LOAD_STR                 'CAC'
              396  COMPARE_OP               ==
          398_400  POP_JUMP_IF_FALSE   406  'to 406'
            402_0  COME_FROM           388  '388'

 L.  75       402  LOAD_STR                 'H'
              404  RETURN_VALUE     
            406_0  COME_FROM           398  '398'

 L.  76       406  LOAD_FAST                'codon'
              408  LOAD_STR                 'CAA'
              410  COMPARE_OP               ==
          412_414  POP_JUMP_IF_TRUE    426  'to 426'
              416  LOAD_FAST                'codon'
              418  LOAD_STR                 'CAG'
              420  COMPARE_OP               ==
          422_424  POP_JUMP_IF_FALSE   430  'to 430'
            426_0  COME_FROM           412  '412'

 L.  77       426  LOAD_STR                 'Q'
              428  RETURN_VALUE     
            430_0  COME_FROM           422  '422'

 L.  78       430  LOAD_FAST                'codon'
              432  LOAD_STR                 'AAT'
              434  COMPARE_OP               ==
          436_438  POP_JUMP_IF_TRUE    450  'to 450'
              440  LOAD_FAST                'codon'
              442  LOAD_STR                 'AAC'
              444  COMPARE_OP               ==
          446_448  POP_JUMP_IF_FALSE   454  'to 454'
            450_0  COME_FROM           436  '436'

 L.  79       450  LOAD_STR                 'N'
              452  RETURN_VALUE     
            454_0  COME_FROM           446  '446'

 L.  80       454  LOAD_FAST                'codon'
              456  LOAD_STR                 'AAA'
              458  COMPARE_OP               ==
          460_462  POP_JUMP_IF_TRUE    474  'to 474'
              464  LOAD_FAST                'codon'
              466  LOAD_STR                 'AAG'
              468  COMPARE_OP               ==
          470_472  POP_JUMP_IF_FALSE   478  'to 478'
            474_0  COME_FROM           460  '460'

 L.  81       474  LOAD_STR                 'K'
              476  RETURN_VALUE     
            478_0  COME_FROM           470  '470'

 L.  82       478  LOAD_FAST                'codon'
              480  LOAD_STR                 'TGT'
              482  COMPARE_OP               ==
          484_486  POP_JUMP_IF_TRUE    498  'to 498'
              488  LOAD_FAST                'codon'
              490  LOAD_STR                 'TGC'
              492  COMPARE_OP               ==
          494_496  POP_JUMP_IF_FALSE   502  'to 502'
            498_0  COME_FROM           484  '484'

 L.  83       498  LOAD_STR                 'C'
              500  RETURN_VALUE     
            502_0  COME_FROM           494  '494'

 L.  84       502  LOAD_FAST                'codon'
              504  LOAD_STR                 'TGG'
              506  COMPARE_OP               ==
          508_510  POP_JUMP_IF_FALSE   516  'to 516'

 L.  85       512  LOAD_STR                 'W'
              514  RETURN_VALUE     
            516_0  COME_FROM           508  '508'

 L.  86       516  LOAD_FAST                'codon'
              518  LOAD_STR                 'CGA'
              520  COMPARE_OP               ==
          522_524  POP_JUMP_IF_TRUE    556  'to 556'
              526  LOAD_FAST                'codon'
              528  LOAD_STR                 'CGC'
              530  COMPARE_OP               ==
          532_534  POP_JUMP_IF_TRUE    556  'to 556'
              536  LOAD_FAST                'codon'
              538  LOAD_STR                 'CGG'
              540  COMPARE_OP               ==
          542_544  POP_JUMP_IF_TRUE    556  'to 556'
              546  LOAD_FAST                'codon'
              548  LOAD_STR                 'CGT'
              550  COMPARE_OP               ==
          552_554  POP_JUMP_IF_FALSE   560  'to 560'
            556_0  COME_FROM           542  '542'
            556_1  COME_FROM           532  '532'
            556_2  COME_FROM           522  '522'

 L.  87       556  LOAD_STR                 'R'
              558  RETURN_VALUE     
            560_0  COME_FROM           552  '552'

 L.  88       560  LOAD_FAST                'codon'
              562  LOAD_STR                 'AGT'
              564  COMPARE_OP               ==
          566_568  POP_JUMP_IF_TRUE    580  'to 580'
              570  LOAD_FAST                'codon'
              572  LOAD_STR                 'AGC'
              574  COMPARE_OP               ==
          576_578  POP_JUMP_IF_FALSE   584  'to 584'
            580_0  COME_FROM           566  '566'

 L.  89       580  LOAD_STR                 'S'
              582  RETURN_VALUE     
            584_0  COME_FROM           576  '576'

 L.  90       584  LOAD_FAST                'codon'
              586  LOAD_STR                 'AGA'
              588  COMPARE_OP               ==
          590_592  POP_JUMP_IF_TRUE    604  'to 604'
              594  LOAD_FAST                'codon'
              596  LOAD_STR                 'AGG'
              598  COMPARE_OP               ==
          600_602  POP_JUMP_IF_FALSE   608  'to 608'
            604_0  COME_FROM           590  '590'

 L.  91       604  LOAD_STR                 'R'
              606  RETURN_VALUE     
            608_0  COME_FROM           600  '600'

 L.  92       608  LOAD_FAST                'codon'
              610  LOAD_STR                 'GGA'
              612  COMPARE_OP               ==
          614_616  POP_JUMP_IF_TRUE    648  'to 648'
              618  LOAD_FAST                'codon'
              620  LOAD_STR                 'GGC'
              622  COMPARE_OP               ==
          624_626  POP_JUMP_IF_TRUE    648  'to 648'
              628  LOAD_FAST                'codon'
              630  LOAD_STR                 'GGG'
              632  COMPARE_OP               ==
          634_636  POP_JUMP_IF_TRUE    648  'to 648'
              638  LOAD_FAST                'codon'
              640  LOAD_STR                 'GGT'
              642  COMPARE_OP               ==
          644_646  POP_JUMP_IF_FALSE   652  'to 652'
            648_0  COME_FROM           634  '634'
            648_1  COME_FROM           624  '624'
            648_2  COME_FROM           614  '614'

 L.  93       648  LOAD_STR                 'G'
              650  RETURN_VALUE     
            652_0  COME_FROM           644  '644'

 L.  95       652  LOAD_FAST                'codon'
              654  LOAD_STR                 'TAA'
              656  COMPARE_OP               ==
          658_660  POP_JUMP_IF_TRUE    682  'to 682'
              662  LOAD_FAST                'codon'
              664  LOAD_STR                 'TAG'
              666  COMPARE_OP               ==
          668_670  POP_JUMP_IF_TRUE    682  'to 682'
              672  LOAD_FAST                'codon'
              674  LOAD_STR                 'TGA'
              676  COMPARE_OP               ==
          678_680  POP_JUMP_IF_FALSE   686  'to 686'
            682_0  COME_FROM           668  '668'
            682_1  COME_FROM           658  '658'

 L.  96       682  LOAD_STR                 'J'
              684  RETURN_VALUE     
            686_0  COME_FROM           678  '678'

 L.  98       686  LOAD_STR                 'Z'
              688  RETURN_VALUE     

Parse error at or near `LOAD_STR' instruction at offset 686


def SixMer2AA(seq):
    """Convert 6mer to 2 AA"""
    return Codon2AA2(seq[0:3]) + Codon2AA2(seq[3:6])