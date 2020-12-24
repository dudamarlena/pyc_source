# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/zxh/LncrnaPackage/models/LncADeep/LncADeep_lncRNA/LncADeep_partial/bin/HmmFea.py
# Compiled at: 2019-10-31 08:44:25
# Size of source mod 2**32: 4621 bytes
import os, sys, numpy as np, subprocess
from .utils import GetFasta
from .utils import RevComp
from .utils import Codon2AA2
_AA_list = [
 'A', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'V', 'W', 'Y']
_DNA = [
 'A', 'C', 'G', 'T']
_3mer_list = []
for dna1 in _DNA:
    for dna2 in _DNA:
        for dna3 in _DNA:
            _3mer_list.append(dna1 + dna2 + dna3)

_IUPAC = {'A':'A', 
 'C':'C',  'G':'G',  'T':'T',  'R':'AG',  'Y':'CT',  'M':'AC',  'K':'GT',  'S':'CG',  'W':'AT',  'H':'ACT',  'B':'CGT', 
 'V':'ACG',  'D':'AGT',  'N':'ACGT'}

def IUPAC_3mer(seq):
    """Return a list of all possible 3mers of the sequence"""
    kmer_list = []
    for dna1 in _IUPAC[seq[0]]:
        for dna2 in _IUPAC[seq[1]]:
            for dna3 in _IUPAC[seq[2]]:
                if Codon2AA2(dna1 + dna2 + dna3) != 'J':
                    kmer_list.append(dna1 + dna2 + dna3)

    return kmer_list


def SixFrame--- This code section failed: ---

 L.  46         0  BUILD_LIST_0          0 
                2  STORE_FAST               'protein_list'

 L.  48         4  LOAD_FAST                'direction'
                6  LOAD_CONST               1
                8  COMPARE_OP               ==
               10  POP_JUMP_IF_FALSE    54  'to 54'

 L.  49        12  SETUP_LOOP          182  'to 182'
               14  LOAD_GLOBAL              range
               16  LOAD_CONST               3
               18  CALL_FUNCTION_1       1  '1 positional argument'
               20  GET_ITER         
               22  FOR_ITER             50  'to 50'
               24  STORE_FAST               'i'

 L.  50        26  LOAD_FAST                'protein_list'
               28  LOAD_METHOD              append
               30  LOAD_GLOBAL              Translation
               32  LOAD_FAST                'seq'
               34  LOAD_FAST                'i'
               36  LOAD_CONST               None
               38  BUILD_SLICE_2         2 
               40  BINARY_SUBSCR    
               42  CALL_FUNCTION_1       1  '1 positional argument'
               44  CALL_METHOD_1         1  '1 positional argument'
               46  POP_TOP          
               48  JUMP_BACK            22  'to 22'
               50  POP_BLOCK        
               52  JUMP_FORWARD        182  'to 182'
             54_0  COME_FROM            10  '10'

 L.  52        54  LOAD_FAST                'direction'
               56  LOAD_CONST               2
               58  COMPARE_OP               ==
               60  POP_JUMP_IF_FALSE   108  'to 108'

 L.  53        62  SETUP_LOOP          182  'to 182'
               64  LOAD_GLOBAL              range
               66  LOAD_CONST               3
               68  CALL_FUNCTION_1       1  '1 positional argument'
               70  GET_ITER         
               72  FOR_ITER            104  'to 104'
               74  STORE_FAST               'i'

 L.  54        76  LOAD_FAST                'protein_list'
               78  LOAD_METHOD              append
               80  LOAD_GLOBAL              Translation
               82  LOAD_GLOBAL              RevComp
               84  LOAD_FAST                'seq'
               86  CALL_FUNCTION_1       1  '1 positional argument'
               88  LOAD_FAST                'i'
               90  LOAD_CONST               None
               92  BUILD_SLICE_2         2 
               94  BINARY_SUBSCR    
               96  CALL_FUNCTION_1       1  '1 positional argument'
               98  CALL_METHOD_1         1  '1 positional argument'
              100  POP_TOP          
              102  JUMP_BACK            72  'to 72'
              104  POP_BLOCK        
              106  JUMP_FORWARD        182  'to 182'
            108_0  COME_FROM            60  '60'

 L.  56       108  LOAD_FAST                'direction'
              110  LOAD_CONST               0
              112  COMPARE_OP               ==
              114  POP_JUMP_IF_FALSE   182  'to 182'

 L.  57       116  SETUP_LOOP          182  'to 182'
              118  LOAD_GLOBAL              range
              120  LOAD_CONST               3
              122  CALL_FUNCTION_1       1  '1 positional argument'
              124  GET_ITER         
              126  FOR_ITER            180  'to 180'
              128  STORE_FAST               'i'

 L.  58       130  LOAD_FAST                'protein_list'
              132  LOAD_METHOD              append
              134  LOAD_GLOBAL              Translation
              136  LOAD_FAST                'seq'
              138  LOAD_FAST                'i'
              140  LOAD_CONST               None
              142  BUILD_SLICE_2         2 
              144  BINARY_SUBSCR    
              146  CALL_FUNCTION_1       1  '1 positional argument'
              148  CALL_METHOD_1         1  '1 positional argument'
              150  POP_TOP          

 L.  59       152  LOAD_FAST                'protein_list'
              154  LOAD_METHOD              append
              156  LOAD_GLOBAL              Translation
              158  LOAD_GLOBAL              RevComp
              160  LOAD_FAST                'seq'
              162  CALL_FUNCTION_1       1  '1 positional argument'
              164  LOAD_FAST                'i'
              166  LOAD_CONST               None
              168  BUILD_SLICE_2         2 
              170  BINARY_SUBSCR    
              172  CALL_FUNCTION_1       1  '1 positional argument'
              174  CALL_METHOD_1         1  '1 positional argument'
              176  POP_TOP          
              178  JUMP_BACK           126  'to 126'
              180  POP_BLOCK        
            182_0  COME_FROM_LOOP      116  '116'
            182_1  COME_FROM           114  '114'
            182_2  COME_FROM           106  '106'
            182_3  COME_FROM_LOOP       62  '62'
            182_4  COME_FROM            52  '52'
            182_5  COME_FROM_LOOP       12  '12'

 L.  61       182  LOAD_FAST                'protein_list'
              184  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `COME_FROM_LOOP' instruction at offset 182_3


def Translation(seq):
    """translate DNA to protein"""
    length = len(seq) / 3
    protein = ''
    for i in range(length):
        if Codon2AA2(seq[i * 3:(i + 1) * 3]) == 'J':
            tmpAA = '*'
        else:
            if Codon2AA2(seq[i * 3:(i + 1) * 3]) == 'Z':
                tmp_3mer_list = IUPAC_3mer(seq[i * 3:(i + 1) * 3])
                tmp_aa_list = []
                for tmp_3mer in tmp_3mer_list:
                    tmp_aa_list.append(Codon2AA2(tmp_3mer))

                if len(set(tmp_aa_list)) > 1:
                    tmpAA = 'X'
                elif len(set(tmp_aa_list)) == 1:
                    tmpAA = tmp_aa_list[0]
                else:
                    tmpAA = '*'
            else:
                tmpAA = Codon2AA2(seq[i * 3:(i + 1) * 3])
        protein += tmpAA

    return protein


def GenerateTrans(fasta, outfile):
    """generate translated fasta file"""
    try:
        f = open(outfile, 'w')
    except (IOError, ValueError) as e:
        try:
            (
             print >> sys.stderr, str(e))
            sys.exit(1)
        finally:
            e = None
            del e

    SeqID, SeqList = GetFasta(fasta)
    for seqid, seq in zip(SeqID, SeqList):
        tmp_protein_list = SixFrame(seq, direction=1)
        for tmp_protein in tmp_protein_list:
            f.write(''.join(['>', seqid]) + '\n')
            f.write(tmp_protein + '\n')

    f.close()


def RunHMM(fasta, output, pfam, thread=8):
    """run HMMER and generate output"""
    out1 = output + '.out1'
    out2 = output + '.out2'
    cmd = 'hmmsearch -o ' + out1 + ' --domtblout ' + out2 + ' --noali -E 0.1 --domE 0.1 --cpu ' + str(thread) + ' ' + pfam + ' ' + fasta
    subprocess.call(cmd, shell=True)
    subprocess.call(('rm ' + out1), shell=True)


def ReadHmm(hmmOut):
    """Read hmmer output file and extract features"""
    try:
        hmm = open(hmmOut, 'rU')
    except (IOError, ValueError) as e:
        try:
            (
             print >> sys.stderr, str(e))
            sys.exit(1)
        finally:
            e = None
            del e

    HMM_dict = {}
    for line in hmm.readlines():
        line = line.strip()
        if line[0] == '#':
            continue
        tmpfeature_list = []
        tmplist = line.split()
        tmpid = tmplist[0]
        tmpfeature_list.append(tmplist[11])
        tmpfeature_list.append(tmplist[13])
        tmpfeature_list.append(str(abs(int(tmplist[16]) - int(tmplist[15])) / float(tmplist[5])))
        tmpfeature_list.append(str(abs(int(tmplist[18]) - int(tmplist[17])) / float(tmplist[2])))
        tmpfeature_list.append(int(tmplist[17]) * 3)
        tmpfeature_list.append(int(tmplist[18]) * 3)
        if HMM_dict.has_key(tmpid):
            if HMM_dict.get(tmpid)[0] > tmpfeature_list[0]:
                HMM_dict[tmpid] = tmpfeature_list
        else:
            HMM_dict[tmpid] = tmpfeature_list

    hmm.close()
    return HMM_dict