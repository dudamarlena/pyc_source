# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/benchmarks/cmp_NA19240.py
# Compiled at: 2020-04-17 02:15:05
# Size of source mod 2**32: 7106 bytes
import sys, argparse, logging, time
callset = {1:'cuteSV', 
 2:'Sniflles',  3:'PBSV',  4:'SVIM'}
USAGE = '\tEvaluate SV callset on NA19240 dataset\n'

def parseArgs(argv):
    parser = argparse.ArgumentParser(prog='NA19240_eval', description=USAGE, formatter_class=(argparse.RawDescriptionHelpFormatter))
    parser.add_argument('base', type=str, help='Base vcf file of NA19240.')
    parser.add_argument('cuteSV', type=str, help='CuteSV vcf file of NA19240.')
    parser.add_argument('sniffles', type=str, help='Sniffles vcf file of NA19240.')
    parser.add_argument('pbsv', type=str, help='PBSV vcf file of NA19240.')
    parser.add_argument('svim', type=str, help='SVIM vcf file of NA19240.')
    parser.add_argument('-b', '--bias', help='Bias of overlaping.[%(default)s]', default=0.7, type=float)
    parser.add_argument('-o', '--offect', help='Offect of breakpoint distance.[%(default)s]', default=1000, type=int)
    args = parser.parse_args(argv)
    return args


def pase_base_info(seq):
    info = {'SVLEN':0, 
     'END':0,  'SVTYPE':''}
    for i in seq.split(';'):
        if i.split('=')[0] in ('SVLEN', 'END'):
            try:
                info[i.split('=')[0]] = abs(int(i.split('=')[1]))
            except:
                pass

            if i.split('=')[0] == 'SVTYPE':
                info[i.split('=')[0]] = i.split('=')[1][0:3]

    return info


def load_base(base_path):
    base_call = dict()
    file = open(base_path, 'r')
    for line in file:
        seq = line.strip('\n').split('\t')
        if seq[0][0] == '#':
            continue
        else:
            chr = seq[0]
            pos = int(seq[1])
            ALT = seq[4][1:4]
            if ALT not in ('INS', 'INV', 'DEL', 'DUP'):
                continue
            if ALT == 'DUP':
                ALT = 'INS'
            info = pase_base_info(seq[7])
            if ALT not in base_call:
                base_call[ALT] = dict()
            if chr not in base_call[ALT]:
                base_call[ALT][chr] = list()
            if ALT == 'INV':
                base_call[ALT][chr].append([pos, info['END'] - pos + 1, info['END'], 0])
        if info['SVLEN'] >= 50 and info['SVLEN'] <= 100000:
            base_call[ALT][chr].append([pos, info['SVLEN'], info['END'], 0])

    file.close()
    return base_call


def load_cuteSV(cuteSV_path):
    cuteSV_call = dict()
    file = open(cuteSV_path, 'r')
    for line in file:
        seq = line.strip('\n').split('\t')
        if seq[0][0] == '#':
            continue
        chr = seq[0]
        pos = int(seq[1])
        ALT = seq[2][7:10]
        if ALT == 'DUP':
            ALT = 'INS'
        if ALT not in ('INS', 'INV', 'DEL', 'DUP'):
            continue
        info = pase_base_info(seq[7])
        if ALT not in cuteSV_call:
            cuteSV_call[ALT] = dict()
        if chr not in cuteSV_call[ALT]:
            cuteSV_call[ALT][chr] = list()
        if info['SVLEN'] >= 50 and info['SVLEN'] <= 100000:
            cuteSV_call[ALT][chr].append([pos, info['SVLEN'], info['END'], 0])

    file.close()
    return cuteSV_call


def load_sniffles(sniffles_path):
    sniffles_call = dict()
    file = open(sniffles_path, 'r')
    for line in file:
        seq = line.strip('\n').split('\t')
        if seq[0][0] == '#':
            continue
        chr = seq[0]
        pos = int(seq[1])
        info = pase_base_info(seq[7])
        if info['SVTYPE'] not in ('INS', 'INV', 'DEL', 'DUP'):
            continue
        if info['SVTYPE'] == 'DUP':
            info['SVTYPE'] = 'INS'
        if info['SVTYPE'] not in sniffles_call:
            sniffles_call[info['SVTYPE']] = dict()
        if chr not in sniffles_call[info['SVTYPE']]:
            sniffles_call[info['SVTYPE']][chr] = list()
        if info['SVLEN'] >= 50 and info['SVLEN'] <= 100000:
            sniffles_call[info['SVTYPE']][chr].append([pos, info['SVLEN'], info['END'], 0])

    file.close()
    return sniffles_call


def load_pbsv(pbsv_path):
    pbsv_call = dict()
    file = open(pbsv_path, 'r')
    for line in file:
        seq = line.strip('\n').split('\t')
        if seq[0][0] == '#':
            continue
        else:
            chr = seq[0]
            pos = int(seq[1])
            info = pase_base_info(seq[7])
            if info['SVTYPE'] not in ('INS', 'INV', 'DEL', 'DUP'):
                continue
            if info['SVTYPE'] == 'DUP':
                info['SVTYPE'] = 'INS'
            if info['SVTYPE'] not in pbsv_call:
                pbsv_call[info['SVTYPE']] = dict()
            if chr not in pbsv_call[info['SVTYPE']]:
                pbsv_call[info['SVTYPE']][chr] = list()
            if info['SVTYPE'] == 'INV':
                pbsv_call[info['SVTYPE']][chr].append([pos, info['END'] - pos + 1, info['END'], 0])
        if info['SVLEN'] >= 50 and info['SVLEN'] <= 100000:
            pbsv_call[info['SVTYPE']][chr].append([pos, info['SVLEN'], info['END'], 0])

    file.close()
    return pbsv_call


def cmp_callsets--- This code section failed: ---

 L. 159       0_2  SETUP_LOOP          302  'to 302'
                4  LOAD_FAST                'base'
                6  GET_ITER         
             8_10  FOR_ITER            300  'to 300'
               12  STORE_FAST               'svtype'

 L. 160        14  LOAD_FAST                'svtype'
               16  LOAD_FAST                'call'
               18  COMPARE_OP               not-in
               20  POP_JUMP_IF_FALSE    26  'to 26'

 L. 161        22  CONTINUE              8  'to 8'
               24  JUMP_BACK             8  'to 8'
             26_0  COME_FROM            20  '20'

 L. 163     26_28  SETUP_LOOP          298  'to 298'
               30  LOAD_FAST                'base'
               32  LOAD_FAST                'svtype'
               34  BINARY_SUBSCR    
               36  GET_ITER         
            38_40  FOR_ITER            296  'to 296'
               42  STORE_FAST               'chr'

 L. 164        44  LOAD_FAST                'chr'
               46  LOAD_FAST                'call'
               48  LOAD_FAST                'svtype'
               50  BINARY_SUBSCR    
               52  COMPARE_OP               not-in
               54  POP_JUMP_IF_FALSE    60  'to 60'

 L. 165        56  CONTINUE             38  'to 38'
               58  JUMP_BACK            38  'to 38'
             60_0  COME_FROM            54  '54'

 L. 167        60  SETUP_LOOP          294  'to 294'
               62  LOAD_FAST                'base'
               64  LOAD_FAST                'svtype'
               66  BINARY_SUBSCR    
               68  LOAD_FAST                'chr'
               70  BINARY_SUBSCR    
               72  GET_ITER         
               74  FOR_ITER            292  'to 292'
               76  STORE_FAST               'i'

 L. 168        78  SETUP_LOOP          290  'to 290'
               80  LOAD_FAST                'call'
               82  LOAD_FAST                'svtype'
               84  BINARY_SUBSCR    
               86  LOAD_FAST                'chr'
               88  BINARY_SUBSCR    
               90  GET_ITER         
             92_0  COME_FROM           266  '266'
             92_1  COME_FROM           216  '216'
               92  FOR_ITER            288  'to 288'
               94  STORE_FAST               'j'

 L. 169        96  LOAD_FAST                'i'
               98  LOAD_CONST               0
              100  BINARY_SUBSCR    
              102  LOAD_FAST                'Offect'
              104  BINARY_SUBTRACT  
              106  LOAD_FAST                'j'
              108  LOAD_CONST               0
              110  BINARY_SUBSCR    
              112  DUP_TOP          
              114  ROT_THREE        
              116  COMPARE_OP               <=
              118  POP_JUMP_IF_FALSE   136  'to 136'
              120  LOAD_FAST                'i'
              122  LOAD_CONST               2
              124  BINARY_SUBSCR    
              126  LOAD_FAST                'Offect'
              128  BINARY_ADD       
              130  COMPARE_OP               <=
              132  POP_JUMP_IF_TRUE    224  'to 224'
              134  JUMP_FORWARD        138  'to 138'
            136_0  COME_FROM           118  '118'
              136  POP_TOP          
            138_0  COME_FROM           134  '134'
              138  LOAD_FAST                'i'
              140  LOAD_CONST               0
              142  BINARY_SUBSCR    
              144  LOAD_FAST                'Offect'
              146  BINARY_SUBTRACT  
              148  LOAD_FAST                'j'
              150  LOAD_CONST               2
              152  BINARY_SUBSCR    
              154  DUP_TOP          
              156  ROT_THREE        
              158  COMPARE_OP               <=
              160  POP_JUMP_IF_FALSE   178  'to 178'
              162  LOAD_FAST                'i'
              164  LOAD_CONST               2
              166  BINARY_SUBSCR    
              168  LOAD_FAST                'Offect'
              170  BINARY_ADD       
              172  COMPARE_OP               <=
              174  POP_JUMP_IF_TRUE    224  'to 224'
              176  JUMP_FORWARD        180  'to 180'
            178_0  COME_FROM           160  '160'
              178  POP_TOP          
            180_0  COME_FROM           176  '176'
              180  LOAD_FAST                'j'
              182  LOAD_CONST               0
              184  BINARY_SUBSCR    
              186  LOAD_FAST                'Offect'
              188  BINARY_SUBTRACT  
              190  LOAD_FAST                'i'
              192  LOAD_CONST               0
              194  BINARY_SUBSCR    
              196  DUP_TOP          
              198  ROT_THREE        
              200  COMPARE_OP               <=
              202  POP_JUMP_IF_FALSE   220  'to 220'
              204  LOAD_FAST                'j'
              206  LOAD_CONST               2
              208  BINARY_SUBSCR    
              210  LOAD_FAST                'Offect'
              212  BINARY_ADD       
              214  COMPARE_OP               <=
              216  POP_JUMP_IF_FALSE    92  'to 92'
              218  JUMP_FORWARD        224  'to 224'
            220_0  COME_FROM           202  '202'
              220  POP_TOP          
              222  JUMP_BACK            92  'to 92'
            224_0  COME_FROM           218  '218'
            224_1  COME_FROM           174  '174'
            224_2  COME_FROM           132  '132'

 L. 170       224  LOAD_GLOBAL              min
              226  LOAD_FAST                'i'
              228  LOAD_CONST               1
              230  BINARY_SUBSCR    
              232  LOAD_FAST                'j'
              234  LOAD_CONST               1
              236  BINARY_SUBSCR    
              238  CALL_FUNCTION_2       2  '2 positional arguments'
              240  LOAD_CONST               1.0
              242  BINARY_MULTIPLY  
              244  LOAD_GLOBAL              max
              246  LOAD_FAST                'i'
              248  LOAD_CONST               1
              250  BINARY_SUBSCR    
              252  LOAD_FAST                'j'
              254  LOAD_CONST               1
              256  BINARY_SUBSCR    
              258  CALL_FUNCTION_2       2  '2 positional arguments'
              260  BINARY_TRUE_DIVIDE
              262  LOAD_FAST                'Bias'
              264  COMPARE_OP               >=
              266  POP_JUMP_IF_FALSE    92  'to 92'

 L. 171       268  LOAD_FAST                'flag'
              270  LOAD_FAST                'i'
              272  LOAD_CONST               3
              274  STORE_SUBSCR     

 L. 172       276  LOAD_FAST                'flag'
              278  LOAD_FAST                'j'
              280  LOAD_CONST               3
              282  STORE_SUBSCR     
              284  CONTINUE             92  'to 92'

 L. 174       286  JUMP_BACK            92  'to 92'
              288  POP_BLOCK        
            290_0  COME_FROM_LOOP       78  '78'
              290  JUMP_BACK            74  'to 74'
              292  POP_BLOCK        
            294_0  COME_FROM_LOOP       60  '60'
              294  JUMP_BACK            38  'to 38'
              296  POP_BLOCK        
            298_0  COME_FROM_LOOP       26  '26'
              298  JUMP_BACK             8  'to 8'
              300  POP_BLOCK        
            302_0  COME_FROM_LOOP        0  '0'

 L. 175       302  LOAD_CONST               0
              304  STORE_FAST               'total_base'

 L. 176       306  LOAD_CONST               0
              308  STORE_FAST               'tp_base'

 L. 181       310  SETUP_LOOP          400  'to 400'
              312  LOAD_CONST               ('INS', 'DEL', 'INV')
              314  GET_ITER         
              316  FOR_ITER            398  'to 398'
              318  STORE_FAST               'svtype'

 L. 184       320  SETUP_LOOP          394  'to 394'
              322  LOAD_FAST                'base'
              324  LOAD_FAST                'svtype'
              326  BINARY_SUBSCR    
              328  GET_ITER         
              330  FOR_ITER            392  'to 392'
              332  STORE_FAST               'chr'

 L. 185       334  SETUP_LOOP          388  'to 388'
              336  LOAD_FAST                'base'
              338  LOAD_FAST                'svtype'
              340  BINARY_SUBSCR    
              342  LOAD_FAST                'chr'
              344  BINARY_SUBSCR    
              346  GET_ITER         
            348_0  COME_FROM           370  '370'
              348  FOR_ITER            386  'to 386'
              350  STORE_FAST               'i'

 L. 186       352  LOAD_FAST                'total_base'
              354  LOAD_CONST               1
              356  INPLACE_ADD      
              358  STORE_FAST               'total_base'

 L. 187       360  LOAD_FAST                'i'
              362  LOAD_CONST               3
              364  BINARY_SUBSCR    
              366  LOAD_FAST                'flag'
              368  COMPARE_OP               ==
          370_372  POP_JUMP_IF_FALSE   348  'to 348'

 L. 188       374  LOAD_FAST                'tp_base'
              376  LOAD_CONST               1
              378  INPLACE_ADD      
              380  STORE_FAST               'tp_base'
          382_384  JUMP_BACK           348  'to 348'
              386  POP_BLOCK        
            388_0  COME_FROM_LOOP      334  '334'
          388_390  JUMP_BACK           330  'to 330'
              392  POP_BLOCK        
            394_0  COME_FROM_LOOP      320  '320'
          394_396  JUMP_BACK           316  'to 316'
              398  POP_BLOCK        
            400_0  COME_FROM_LOOP      310  '310'

 L. 193       400  LOAD_GLOBAL              logging
              402  LOAD_METHOD              info
              404  LOAD_STR                 '====%s===='
              406  LOAD_GLOBAL              callset
              408  LOAD_FAST                'flag'
              410  BINARY_SUBSCR    
              412  BINARY_MODULO    
              414  CALL_METHOD_1         1  '1 positional argument'
              416  POP_TOP          

 L. 194       418  LOAD_CONST               0
              420  STORE_FAST               'total_call'

 L. 195       422  LOAD_CONST               0
              424  STORE_FAST               'tp_call'

 L. 200       426  SETUP_LOOP          516  'to 516'
              428  LOAD_CONST               ('INS', 'DEL', 'INV')
              430  GET_ITER         
              432  FOR_ITER            514  'to 514'
              434  STORE_FAST               'svtype'

 L. 203       436  SETUP_LOOP          510  'to 510'
              438  LOAD_FAST                'call'
              440  LOAD_FAST                'svtype'
              442  BINARY_SUBSCR    
              444  GET_ITER         
              446  FOR_ITER            508  'to 508'
              448  STORE_FAST               'chr'

 L. 204       450  SETUP_LOOP          504  'to 504'
              452  LOAD_FAST                'call'
              454  LOAD_FAST                'svtype'
              456  BINARY_SUBSCR    
              458  LOAD_FAST                'chr'
              460  BINARY_SUBSCR    
              462  GET_ITER         
            464_0  COME_FROM           486  '486'
              464  FOR_ITER            502  'to 502'
              466  STORE_FAST               'i'

 L. 205       468  LOAD_FAST                'total_call'
              470  LOAD_CONST               1
              472  INPLACE_ADD      
              474  STORE_FAST               'total_call'

 L. 206       476  LOAD_FAST                'i'
              478  LOAD_CONST               3
              480  BINARY_SUBSCR    
              482  LOAD_FAST                'flag'
              484  COMPARE_OP               ==
          486_488  POP_JUMP_IF_FALSE   464  'to 464'

 L. 207       490  LOAD_FAST                'tp_call'
              492  LOAD_CONST               1
              494  INPLACE_ADD      
              496  STORE_FAST               'tp_call'
          498_500  JUMP_BACK           464  'to 464'
              502  POP_BLOCK        
            504_0  COME_FROM_LOOP      450  '450'
          504_506  JUMP_BACK           446  'to 446'
              508  POP_BLOCK        
            510_0  COME_FROM_LOOP      436  '436'
          510_512  JUMP_BACK           432  'to 432'
              514  POP_BLOCK        
            516_0  COME_FROM_LOOP      426  '426'

 L. 210       516  LOAD_GLOBAL              logging
              518  LOAD_METHOD              info
              520  LOAD_STR                 'Camp count: %d'
              522  LOAD_FAST                'total_call'
              524  BINARY_MODULO    
              526  CALL_METHOD_1         1  '1 positional argument'
              528  POP_TOP          

 L. 211       530  LOAD_GLOBAL              logging
              532  LOAD_METHOD              info
              534  LOAD_STR                 'TP-call count: %d'
              536  LOAD_FAST                'tp_call'
              538  BINARY_MODULO    
              540  CALL_METHOD_1         1  '1 positional argument'
              542  POP_TOP          

 L. 212       544  LOAD_GLOBAL              logging
              546  LOAD_METHOD              info
              548  LOAD_STR                 'Precision: %.2f'
              550  LOAD_CONST               100.0
              552  LOAD_FAST                'tp_call'
              554  BINARY_MULTIPLY  
              556  LOAD_FAST                'total_call'
              558  BINARY_TRUE_DIVIDE
              560  BINARY_MODULO    
              562  CALL_METHOD_1         1  '1 positional argument'
              564  POP_TOP          

 L. 213       566  LOAD_GLOBAL              logging
              568  LOAD_METHOD              info
              570  LOAD_STR                 'Recall: %.2f'
              572  LOAD_CONST               100.0
              574  LOAD_FAST                'tp_base'
              576  BINARY_MULTIPLY  
              578  LOAD_FAST                'total_base'
              580  BINARY_TRUE_DIVIDE
              582  BINARY_MODULO    
              584  CALL_METHOD_1         1  '1 positional argument'
              586  POP_TOP          

 L. 214       588  LOAD_GLOBAL              logging
              590  LOAD_METHOD              info
              592  LOAD_STR                 'F-measure: %.2f'
              594  LOAD_CONST               200.0
              596  LOAD_FAST                'tp_base'
              598  BINARY_MULTIPLY  
              600  LOAD_FAST                'tp_call'
              602  BINARY_MULTIPLY  
              604  LOAD_FAST                'total_base'
              606  LOAD_FAST                'tp_call'
              608  BINARY_MULTIPLY  
              610  LOAD_FAST                'tp_base'
              612  LOAD_FAST                'total_call'
              614  BINARY_MULTIPLY  
              616  BINARY_ADD       
              618  BINARY_TRUE_DIVIDE
              620  BINARY_MODULO    
              622  CALL_METHOD_1         1  '1 positional argument'
              624  POP_TOP          

Parse error at or near `COME_FROM_LOOP' instruction at offset 290_0


def main_ctrl(args):
    base_call = load_base(args.base)
    cuteSV_call = load_cuteSV(args.cuteSV)
    sniffles_call = load_sniffles(args.sniffles)
    pbsv_call = load_pbsv(args.pbsv)
    svim_call = load_base(args.svim)
    cmp_callsets(base_call, cuteSV_call, 1, args.bias, args.offect)
    cmp_callsets(base_call, sniffles_call, 2, args.bias, args.offect)
    cmp_callsets(base_call, pbsv_call, 3, args.bias, args.offect)
    cmp_callsets(base_call, svim_call, 4, args.bias, args.offect)


def main(argv):
    args = parseArgs(argv)
    setupLogging(False)
    starttime = time.time()
    main_ctrl(args)
    logging.info('Finished in %0.2f seconds.' % (time.time() - starttime))


def setupLogging(debug=False):
    logLevel = logging.DEBUG if debug else logging.INFO
    logFormat = '%(asctime)s [%(levelname)s] %(message)s'
    logging.basicConfig(stream=(sys.stderr), level=logLevel, format=logFormat)
    logging.info('Running %s' % ' '.join(sys.argv))


if __name__ == '__main__':
    main(sys.argv[1:])