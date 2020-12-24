# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/gmisclib/HTK_MLF_io.py
# Compiled at: 2010-02-05 17:00:31
"""This reads MLF (Master Label Files) for/from the HTK speech recognition
toolkit.
"""
import os, glob
from gmisclib import die
from gmisclib.xwaves_errs import *
TIME_QUANTUM = 1e-07

class ReferencedFileNotFound(Error):

    def __init__(self, *s):
        Error.__init__(self, *s)


def _findfile--- This code section failed: ---

 L.  28         0  LOAD_FAST             0  'f'
                3  POP_JUMP_IF_TRUE     10  'to 10'

 L.  29         6  LOAD_CONST               (None, None)
                9  RETURN_END_IF    
             10_0  COME_FROM             3  '3'

 L.  30        10  LOAD_GLOBAL           1  'os'
               13  LOAD_ATTR             2  'path'
               16  LOAD_ATTR             3  'split'
               19  LOAD_FAST             0  'f'
               22  CALL_FUNCTION_1       1  None
               25  UNPACK_SEQUENCE_2     2 
               28  STORE_FAST            3  'd0'
               31  STORE_FAST            4  'f0'

 L.  31        34  LOAD_GLOBAL           1  'os'
               37  LOAD_ATTR             2  'path'
               40  LOAD_ATTR             4  'splitext'
               43  LOAD_FAST             4  'f0'
               46  CALL_FUNCTION_1       1  None
               49  LOAD_CONST               0
               52  BINARY_SUBSCR    
               53  STORE_FAST            4  'f0'

 L.  32        56  LOAD_GLOBAL           1  'os'
               59  LOAD_ATTR             2  'path'
               62  LOAD_ATTR             5  'join'
               65  LOAD_FAST             3  'd0'
               68  LOAD_FAST             4  'f0'
               71  CALL_FUNCTION_2       2  None
               74  LOAD_FAST             1  'postfix'
               77  BINARY_ADD       
               78  STORE_FAST            5  'fx'

 L.  33        81  LOAD_FAST             2  'verbose'
               84  POP_JUMP_IF_FALSE   107  'to 107'

 L.  34        87  LOAD_GLOBAL           6  'die'
               90  LOAD_ATTR             7  'info'
               93  LOAD_CONST               'HTK_MLF_io._findfile: glob=%s'
               96  LOAD_FAST             5  'fx'
               99  BINARY_MODULO    
              100  CALL_FUNCTION_1       1  None
              103  POP_TOP          
              104  JUMP_FORWARD          0  'to 107'
            107_0  COME_FROM           104  '104'

 L.  35       107  LOAD_GLOBAL           8  'glob'
              110  LOAD_ATTR             8  'glob'
              113  LOAD_FAST             5  'fx'
              116  CALL_FUNCTION_1       1  None
              119  STORE_FAST            6  'gl'

 L.  36       122  LOAD_FAST             2  'verbose'
              125  POP_JUMP_IF_FALSE   157  'to 157'

 L.  37       128  LOAD_GLOBAL           6  'die'
              131  LOAD_ATTR             7  'info'
              134  LOAD_CONST               'HTK_MLF_io._findfile globs=%s'
              137  LOAD_CONST               ','
              140  LOAD_ATTR             5  'join'
              143  LOAD_FAST             6  'gl'
              146  CALL_FUNCTION_1       1  None
              149  BINARY_MODULO    
              150  CALL_FUNCTION_1       1  None
              153  POP_TOP          
              154  JUMP_FORWARD          0  'to 157'
            157_0  COME_FROM           154  '154'

 L.  38       157  LOAD_GLOBAL           9  'len'
              160  LOAD_FAST             6  'gl'
              163  CALL_FUNCTION_1       1  None
              166  LOAD_CONST               0
              169  COMPARE_OP            2  ==
              172  POP_JUMP_IF_FALSE   187  'to 187'

 L.  39       175  LOAD_GLOBAL          10  'ReferencedFileNotFound'
              178  LOAD_FAST             5  'fx'
              181  RAISE_VARARGS_2       2  None
              184  JUMP_FORWARD          0  'to 187'
            187_0  COME_FROM           184  '184'

 L.  40       187  LOAD_GLOBAL           9  'len'
              190  LOAD_FAST             6  'gl'
              193  CALL_FUNCTION_1       1  None
              196  LOAD_CONST               1
              199  COMPARE_OP            2  ==
              202  POP_JUMP_IF_TRUE    230  'to 230'
              205  LOAD_ASSERT              AssertionError
              208  LOAD_CONST               'Too many alternatives for %s: %d'
              211  LOAD_FAST             5  'fx'
              214  LOAD_GLOBAL           9  'len'
              217  LOAD_FAST             6  'gl'
              220  CALL_FUNCTION_1       1  None
              223  BUILD_TUPLE_2         2 
              226  BINARY_MODULO    
              227  RAISE_VARARGS_2       2  None

 L.  41       230  LOAD_GLOBAL           1  'os'
              233  LOAD_ATTR             2  'path'
              236  LOAD_ATTR             3  'split'
              239  LOAD_FAST             6  'gl'
              242  LOAD_CONST               0
              245  BINARY_SUBSCR    
              246  CALL_FUNCTION_1       1  None
              249  UNPACK_SEQUENCE_2     2 
              252  STORE_FAST            7  'd1'
              255  STORE_FAST            8  'f1'

 L.  43       258  LOAD_GLOBAL           1  'os'
              261  LOAD_ATTR             2  'path'
              264  LOAD_ATTR             4  'splitext'
              267  LOAD_FAST             8  'f1'
              270  CALL_FUNCTION_1       1  None
              273  LOAD_CONST               0
              276  BINARY_SUBSCR    
              277  STORE_FAST            8  'f1'

 L.  45       280  LOAD_FAST             2  'verbose'
              283  POP_JUMP_IF_FALSE   312  'to 312'

 L.  46       286  LOAD_GLOBAL           6  'die'
              289  LOAD_ATTR             7  'info'
              292  LOAD_CONST               'HTK_MLF_io._findfile d1=%s d1=%s'
              295  LOAD_FAST             7  'd1'
              298  LOAD_FAST             8  'f1'
              301  BUILD_TUPLE_2         2 
              304  BINARY_MODULO    
              305  CALL_FUNCTION_1       1  None
              308  POP_TOP          
              309  JUMP_FORWARD          0  'to 312'
            312_0  COME_FROM           309  '309'

 L.  47       312  LOAD_FAST             7  'd1'
              315  LOAD_FAST             8  'f1'
              318  BUILD_TUPLE_2         2 
              321  RETURN_VALUE     

Parse error at or near `BUILD_TUPLE_2' instruction at offset 318


def parse_label_line(s, tq):
    """This parses a line from a MLF into a tuple.
        @param tq: time quantum (normally 1e-7 seconds)
        @type tq: L{float}
        @param s: line to be parsed
        @type s: C{str}
        @raise BadFileFormatError: when parsing is not possible.
        """
    a = s.strip().split()
    la = len(a)
    if la == 1:
        if a[0] == '///':
            die.die('Sorry! cannot handle /// in MLF.')
        return a[0]
    else:
        if tq is None:
            raise ValueError, 'File data needs time_quantum to be a number.'
        else:
            if la >= 3:
                tmp = (
                 float(a[0]) * tq, float(a[1]) * tq, a[2])
                if la == 3:
                    return tmp
                tmp = list(tmp)
                a = a[3:]
                while a:
                    tmp.append(float(a.pop(0)))
                    if not a:
                        break
                    tmp.append(a.pop(0))

                return tuple(tmp)
            if la == 2:
                return (float(a[0]) * tq, a[1])
        raise BadFileFormatError
        return


def _get_symbols(fd, time_quantum):
    """This reads part of a MLF, grabbing all the labels for one utterance."""
    sym = []
    while True:
        s = fd.readline()
        if s == '':
            break
        s = s.rstrip('\r\n')
        if s == '.':
            break
        elif s != '':
            sym.append(parse_label_line(s, time_quantum))

    return sym


def readone(mlf_efn, postfix='.wav', datapath='.', strict=True, findfile=True, pathedit=None, time_quantum=TIME_QUANTUM, verbose=False):
    """Read a single set of labels from a MLF file.
        You specify the labels as part of the extended filename, like this:
        name_of_MLF_file:name_of_labels'.    The function returns
        only a single value and raises an exception if the  extended
        filename is ambiguous.
        @type mlf_efn: string in the form "F:S"
        @rtype dict()
        @return: a dictionary that describes the labels as per
                L{readiter}.
        """
    filename, subname = mlf_efn.split(':')
    candidate = None
    for x in readiter(filename, postfix=postfix, datapath=datapath, strict=strict, findfile=findfile, pathedit=pathedit, time_quantum=time_quantum, verbose=verbose):
        if subname in x['filespec']:
            if candidate is not None:
                raise ValueError, 'Not unique: %s in %s' % (subname, filename)
            candidate = x

    return candidate


def readiter--- This code section failed: ---

 L. 151         0  LOAD_FAST             5  'pathedit'
                3  LOAD_CONST               None
                6  COMPARE_OP            8  is
                9  POP_JUMP_IF_FALSE    27  'to 27'

 L. 152        12  LOAD_GLOBAL           1  'os'
               15  LOAD_ATTR             2  'path'
               18  LOAD_ATTR             3  'join'
               21  STORE_FAST            5  'pathedit'
               24  JUMP_FORWARD          0  'to 27'
             27_0  COME_FROM            24  '24'

 L. 154        27  LOAD_GLOBAL           1  'os'
               30  LOAD_ATTR             2  'path'
               33  LOAD_ATTR             4  'split'
               36  LOAD_FAST             0  'mlf_fn'
               39  CALL_FUNCTION_1       1  None
               42  UNPACK_SEQUENCE_2     2 
               45  STORE_FAST            8  'dmlf'
               48  STORE_FAST            9  'fmlf'

 L. 156        51  SETUP_EXCEPT         19  'to 73'

 L. 157        54  LOAD_GLOBAL           5  'open'
               57  LOAD_FAST             0  'mlf_fn'
               60  LOAD_CONST               'r'
               63  CALL_FUNCTION_2       2  None
               66  STORE_FAST           10  'fd'
               69  POP_BLOCK        
               70  JUMP_FORWARD         34  'to 107'
             73_0  COME_FROM            51  '51'

 L. 158        73  DUP_TOP          
               74  LOAD_GLOBAL           6  'IOError'
               77  COMPARE_OP           10  exception-match
               80  POP_JUMP_IF_FALSE   106  'to 106'
               83  POP_TOP          
               84  STORE_FAST           11  'x'
               87  POP_TOP          

 L. 159        88  LOAD_GLOBAL           7  'NoSuchFileError'
               91  LOAD_FAST            11  'x'
               94  LOAD_ATTR             8  'args'
               97  CALL_FUNCTION_VAR_0     0  None
              100  RAISE_VARARGS_1       1  None
              103  JUMP_FORWARD          1  'to 107'
              106  END_FINALLY      
            107_0  COME_FROM           106  '106'
            107_1  COME_FROM            70  '70'

 L. 160       107  LOAD_FAST            10  'fd'
              110  LOAD_ATTR             9  'readline'
              113  CALL_FUNCTION_0       0  None
              116  STORE_FAST           12  'l'

 L. 161       119  LOAD_FAST            12  'l'
              122  LOAD_CONST               '#!MLF!#\n'
              125  COMPARE_OP            2  ==
              128  POP_JUMP_IF_TRUE    144  'to 144'
              131  LOAD_ASSERT              AssertionError
              134  LOAD_CONST               'l=%s'
              137  LOAD_FAST            12  'l'
              140  BINARY_MODULO    
              141  RAISE_VARARGS_2       2  None

 L. 162       144  LOAD_CONST               0
              147  STORE_FAST           13  'i'

 L. 163       150  SETUP_LOOP          351  'to 504'
              153  LOAD_GLOBAL          11  'True'
              156  POP_JUMP_IF_FALSE   503  'to 503'

 L. 164       159  LOAD_FAST            10  'fd'
              162  LOAD_ATTR             9  'readline'
              165  CALL_FUNCTION_0       0  None
              168  STORE_FAST           14  'f'

 L. 165       171  LOAD_FAST            14  'f'
              174  LOAD_CONST               ''
              177  COMPARE_OP            2  ==
              180  POP_JUMP_IF_FALSE   187  'to 187'

 L. 166       183  BREAK_LOOP       
              184  JUMP_FORWARD          0  'to 187'
            187_0  COME_FROM           184  '184'

 L. 167       187  LOAD_FAST            14  'f'
              190  LOAD_ATTR            12  'strip'
              193  CALL_FUNCTION_0       0  None
              196  STORE_FAST           14  'f'

 L. 168       199  LOAD_FAST            14  'f'
              202  LOAD_CONST               ''
              205  COMPARE_OP            2  ==
              208  POP_JUMP_IF_FALSE   217  'to 217'

 L. 169       211  CONTINUE            153  'to 153'
              214  JUMP_FORWARD          0  'to 217'
            217_0  COME_FROM           214  '214'

 L. 170       217  LOAD_FAST            14  'f'
              220  LOAD_ATTR            13  'startswith'
              223  LOAD_CONST               '"'
              226  CALL_FUNCTION_1       1  None
              229  POP_JUMP_IF_FALSE   263  'to 263'
              232  LOAD_FAST            14  'f'
              235  LOAD_ATTR            14  'endswith'
              238  LOAD_CONST               '"'
              241  CALL_FUNCTION_1       1  None
            244_0  COME_FROM           229  '229'
              244  POP_JUMP_IF_FALSE   263  'to 263'

 L. 171       247  LOAD_FAST            14  'f'
              250  LOAD_CONST               1
              253  LOAD_CONST               -1
              256  SLICE+3          
              257  STORE_FAST           14  'f'
              260  JUMP_FORWARD          0  'to 263'
            263_0  COME_FROM           260  '260'

 L. 172       263  LOAD_FAST            14  'f'
              266  STORE_FAST           15  'fspec'

 L. 173       269  BUILD_MAP_2           2  None
              272  LOAD_FAST            15  'fspec'
              275  LOAD_CONST               'filespec'
              278  STORE_MAP        
              279  LOAD_FAST            13  'i'
              282  LOAD_CONST               'i'
              285  STORE_MAP        
              286  STORE_FAST           16  'rv'

 L. 174       289  LOAD_FAST             4  'findfile'
              292  POP_JUMP_IF_FALSE   466  'to 466'

 L. 175       295  LOAD_FAST             7  'verbose'
              298  POP_JUMP_IF_FALSE   330  'to 330'

 L. 176       301  LOAD_GLOBAL          15  'die'
              304  LOAD_ATTR            16  'info'
              307  LOAD_CONST               'dmlf=%s; datapath=%s; f=%s'
              310  LOAD_FAST             8  'dmlf'
              313  LOAD_FAST             2  'datapath'
              316  LOAD_FAST            14  'f'
              319  BUILD_TUPLE_3         3 
              322  BINARY_MODULO    
              323  CALL_FUNCTION_1       1  None
              326  POP_TOP          
              327  JUMP_FORWARD          0  'to 330'
            330_0  COME_FROM           327  '327'

 L. 177       330  SETUP_EXCEPT         40  'to 373'

 L. 178       333  LOAD_GLOBAL          17  '_findfile'
              336  LOAD_FAST             5  'pathedit'
              339  LOAD_FAST             8  'dmlf'
              342  LOAD_FAST             2  'datapath'
              345  LOAD_FAST            14  'f'
              348  CALL_FUNCTION_3       3  None
              351  LOAD_FAST             1  'postfix'
              354  LOAD_FAST             7  'verbose'
              357  CALL_FUNCTION_3       3  None
              360  UNPACK_SEQUENCE_2     2 
              363  STORE_FAST           17  'd1'
              366  STORE_FAST           18  'f1'
              369  POP_BLOCK        
              370  JUMP_FORWARD         70  'to 443'
            373_0  COME_FROM           330  '330'

 L. 179       373  DUP_TOP          
              374  LOAD_GLOBAL          18  'ReferencedFileNotFound'
              377  COMPARE_OP           10  exception-match
              380  POP_JUMP_IF_FALSE   442  'to 442'
              383  POP_TOP          
              384  STORE_FAST           11  'x'
              387  POP_TOP          

 L. 180       388  LOAD_FAST             3  'strict'
              391  POP_JUMP_IF_FALSE   400  'to 400'

 L. 181       394  RAISE_VARARGS_0       0  None
              397  JUMP_ABSOLUTE       463  'to 463'

 L. 183       400  LOAD_GLOBAL          15  'die'
              403  LOAD_ATTR            19  'warn'
              406  LOAD_CONST               'No such file: %s from %s'
              409  LOAD_FAST            11  'x'
              412  LOAD_FAST            15  'fspec'
              415  BUILD_TUPLE_2         2 
              418  BINARY_MODULO    
              419  CALL_FUNCTION_1       1  None
              422  POP_TOP          

 L. 184       423  LOAD_GLOBAL          20  '_get_symbols'
              426  LOAD_FAST            10  'fd'
              429  LOAD_CONST               None
              432  CALL_FUNCTION_2       2  None
              435  POP_TOP          

 L. 185       436  CONTINUE            153  'to 153'
              439  JUMP_ABSOLUTE       466  'to 466'
              442  END_FINALLY      
            443_0  COME_FROM           370  '370'

 L. 187       443  LOAD_FAST            17  'd1'
              446  LOAD_FAST            16  'rv'
              449  LOAD_CONST               'd'
              452  STORE_SUBSCR     

 L. 188       453  LOAD_FAST            18  'f1'
              456  LOAD_FAST            16  'rv'
              459  LOAD_CONST               'f'
              462  STORE_SUBSCR     
            463_0  COME_FROM           442  '442'
              463  JUMP_FORWARD          0  'to 466'
            466_0  COME_FROM           463  '463'

 L. 189       466  LOAD_GLOBAL          20  '_get_symbols'
              469  LOAD_FAST            10  'fd'
              472  LOAD_FAST             6  'time_quantum'
              475  CALL_FUNCTION_2       2  None
              478  LOAD_FAST            16  'rv'
              481  LOAD_CONST               'symbols'
              484  STORE_SUBSCR     

 L. 190       485  LOAD_FAST            16  'rv'
              488  YIELD_VALUE      
              489  POP_TOP          

 L. 191       490  LOAD_FAST            13  'i'
              493  LOAD_CONST               1
              496  INPLACE_ADD      
              497  STORE_FAST           13  'i'
              500  JUMP_BACK           153  'to 153'
              503  POP_BLOCK        
            504_0  COME_FROM           150  '150'
              504  LOAD_CONST               None
              507  RETURN_VALUE     

Parse error at or near `LOAD_CONST' instruction at offset 504


def read(mlf_fn, **kw):
    return list(readiter(mlf_fn, **kw))


read.__doc__ = readiter.__doc__

class writer(object):

    def __init__(self, mlf_fd, time_quantum=TIME_QUANTUM):
        assert time_quantum > 0.0
        self.fd = mlf_fd
        self.fd.writelines('#!MLF!#\n')
        self.nchunks = 0
        self.scale = 1.0 / time_quantum

    def chunk(self, filespec, data):
        if self.nchunks > 0:
            self.fd.writelines('.\n')
        self.fd.writelines(['"%s"\n' % filespec,
         ('\n').join(data), '\n'])
        self.nchunks += 1
        self.fd.flush()

    def threecol(self, filespec, tcdata):
        d = [ '%d %d %s' % (int(round(t0 * self.scale)), int(round(te * self.scale)), lbl) for t0, te, lbl in tcdata
            ]
        self.chunk(filespec, d)

    def close(self):
        self.fd.writelines('\n')
        self.fd.flush()
        os.fsync(self.fd.fileno())
        self.fd = None
        return

    def __del__(self):
        if self.fd is not None:
            self.close()
        return


if __name__ == '__main__':
    import sys
    DATAPATH = None
    arglist = sys.argv[1:]
    while arglist and arglist[0].startswith('-'):
        arg = arglist.pop(0)
        if arg == '-datapath':
            DATAPATH = arglist.pop(0)
        else:
            die.die('Unrecognized argument: %s' % arg)

    for tmp in readiter(arglist[0], datapath=DATAPATH, findfile=DATAPATH is not None):
        print '[', tmp['filespec'], tmp.get('d', ''), tmp.get('f', ''), ']'
        for tmps in tmp['symbols']:
            if isinstance(tmps, tuple):
                print (' ').join([ str(q) for q in tmps ])
            else:
                print tmps