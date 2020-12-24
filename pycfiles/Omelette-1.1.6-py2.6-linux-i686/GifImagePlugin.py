# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/PIL/GifImagePlugin.py
# Compiled at: 2007-09-25 20:00:35
__version__ = '0.9'
import Image, ImageFile, ImagePalette

def i16(c):
    return ord(c[0]) + (ord(c[1]) << 8)


def o16(i):
    return chr(i & 255) + chr(i >> 8 & 255)


def _accept(prefix):
    return prefix[:6] in ('GIF87a', 'GIF89a')


class GifImageFile(ImageFile.ImageFile):
    format = 'GIF'
    format_description = 'Compuserve GIF'
    global_palette = None

    def data(self):
        s = self.fp.read(1)
        if s and ord(s):
            return self.fp.read(ord(s))
        else:
            return

    def _open(self):
        s = self.fp.read(13)
        if s[:6] not in ('GIF87a', 'GIF89a'):
            raise SyntaxError, 'not a GIF file'
        self.info['version'] = s[:6]
        self.size = (
         i16(s[6:]), i16(s[8:]))
        self.tile = []
        flags = ord(s[10])
        bits = (flags & 7) + 1
        if flags & 128:
            self.info['background'] = ord(s[11])
            p = self.fp.read(3 << bits)
            for i in range(0, len(p), 3):
                if not chr(i / 3) == p[i] == p[(i + 1)] == p[(i + 2)]:
                    p = ImagePalette.raw('RGB', p)
                    self.global_palette = self.palette = p
                    break

        self.__fp = self.fp
        self.__rewind = self.fp.tell()
        self.seek(0)

    def seek--- This code section failed: ---

 L. 101         0  LOAD_FAST             1  'frame'
                3  LOAD_CONST               0
                6  COMPARE_OP            2  ==
                9  JUMP_IF_FALSE        50  'to 62'
             12_0  THEN                     63
               12  POP_TOP          

 L. 103        13  LOAD_CONST               0
               16  LOAD_FAST             0  'self'
               19  STORE_ATTR            0  '__offset'

 L. 104        22  LOAD_CONST               None
               25  LOAD_FAST             0  'self'
               28  STORE_ATTR            2  'dispose'

 L. 105        31  LOAD_CONST               -1
               34  LOAD_FAST             0  'self'
               37  STORE_ATTR            3  '__frame'

 L. 106        40  LOAD_FAST             0  'self'
               43  LOAD_ATTR             4  '__fp'
               46  LOAD_ATTR             5  'seek'
               49  LOAD_FAST             0  'self'
               52  LOAD_ATTR             6  '__rewind'
               55  CALL_FUNCTION_1       1  None
               58  POP_TOP          
               59  JUMP_FORWARD          1  'to 63'
             62_0  COME_FROM             9  '9'
               62  POP_TOP          
             63_0  COME_FROM            59  '59'

 L. 108        63  LOAD_FAST             1  'frame'
               66  LOAD_FAST             0  'self'
               69  LOAD_ATTR             3  '__frame'
               72  LOAD_CONST               1
               75  BINARY_ADD       
               76  COMPARE_OP            3  !=
               79  JUMP_IF_FALSE        17  'to 99'
             82_0  THEN                     100
               82  POP_TOP          

 L. 109        83  LOAD_GLOBAL           7  'ValueError'
               86  LOAD_CONST               'cannot seek to frame %d'
               89  LOAD_FAST             1  'frame'
               92  BINARY_MODULO    
               93  RAISE_VARARGS_2       2  None
               96  JUMP_FORWARD          1  'to 100'
             99_0  COME_FROM            79  '79'
               99  POP_TOP          
            100_0  COME_FROM            96  '96'

 L. 110       100  LOAD_FAST             1  'frame'
              103  LOAD_FAST             0  'self'
              106  STORE_ATTR            3  '__frame'

 L. 112       109  BUILD_LIST_0          0 
              112  LOAD_FAST             0  'self'
              115  STORE_ATTR            8  'tile'

 L. 114       118  LOAD_FAST             0  'self'
              121  LOAD_ATTR             4  '__fp'
              124  LOAD_FAST             0  'self'
              127  STORE_ATTR            9  'fp'

 L. 115       130  LOAD_FAST             0  'self'
              133  LOAD_ATTR             0  '__offset'
              136  JUMP_IF_FALSE        53  'to 192'
            139_0  THEN                     193
              139  POP_TOP          

 L. 117       140  LOAD_FAST             0  'self'
              143  LOAD_ATTR             9  'fp'
              146  LOAD_ATTR             5  'seek'
              149  LOAD_FAST             0  'self'
              152  LOAD_ATTR             0  '__offset'
              155  CALL_FUNCTION_1       1  None
              158  POP_TOP          

 L. 118       159  SETUP_LOOP           18  'to 180'
              162  LOAD_FAST             0  'self'
              165  LOAD_ATTR            10  'data'
              168  CALL_FUNCTION_0       0  None
              171  JUMP_IF_FALSE         4  'to 178'
              174  POP_TOP          

 L. 119       175  JUMP_BACK           162  'to 162'
              178  POP_TOP          
              179  POP_BLOCK        
            180_0  COME_FROM           159  '159'

 L. 120       180  LOAD_CONST               0
              183  LOAD_FAST             0  'self'
              186  STORE_ATTR            0  '__offset'
              189  JUMP_FORWARD          1  'to 193'
            192_0  COME_FROM           136  '136'
              192  POP_TOP          
            193_0  COME_FROM           189  '189'

 L. 122       193  LOAD_FAST             0  'self'
              196  LOAD_ATTR             2  'dispose'
              199  JUMP_IF_FALSE        25  'to 227'
            202_0  THEN                     228
              202  POP_TOP          

 L. 123       203  LOAD_FAST             0  'self'
              206  LOAD_ATTR             2  'dispose'
              209  LOAD_FAST             0  'self'
              212  STORE_ATTR           11  'im'

 L. 124       215  LOAD_CONST               None
              218  LOAD_FAST             0  'self'
              221  STORE_ATTR            2  'dispose'
              224  JUMP_FORWARD          1  'to 228'
            227_0  COME_FROM           199  '199'
              227  POP_TOP          
            228_0  COME_FROM           224  '224'

 L. 126       228  LOAD_FAST             0  'self'
              231  LOAD_ATTR            12  'global_palette'
              234  LOAD_FAST             0  'self'
              237  STORE_ATTR           13  'palette'

 L. 128       240  SETUP_LOOP          719  'to 962'

 L. 130       243  LOAD_FAST             0  'self'
              246  LOAD_ATTR             9  'fp'
              249  LOAD_ATTR            14  'read'
              252  LOAD_CONST               1
              255  CALL_FUNCTION_1       1  None
              258  STORE_FAST            2  's'

 L. 131       261  LOAD_FAST             2  's'
              264  UNARY_NOT        
              265  JUMP_IF_TRUE         13  'to 281'
              268  POP_TOP          
              269  LOAD_FAST             2  's'
              272  LOAD_CONST               ';'
              275  COMPARE_OP            2  ==
            278_0  COME_FROM           265  '265'
              278  JUMP_IF_FALSE         5  'to 286'
              281  POP_TOP          

 L. 132       282  BREAK_LOOP       
              283  JUMP_BACK           243  'to 243'
            286_0  COME_FROM           278  '278'
              286  POP_TOP          

 L. 134       287  LOAD_FAST             2  's'
              290  LOAD_CONST               '!'
              293  COMPARE_OP            2  ==
              296  JUMP_IF_FALSE       364  'to 663'
              299  POP_TOP          

 L. 138       300  LOAD_FAST             0  'self'
              303  LOAD_ATTR             9  'fp'
              306  LOAD_ATTR            14  'read'
              309  LOAD_CONST               1
              312  CALL_FUNCTION_1       1  None
              315  STORE_FAST            2  's'

 L. 139       318  LOAD_FAST             0  'self'
              321  LOAD_ATTR            10  'data'
              324  CALL_FUNCTION_0       0  None
              327  STORE_FAST            3  'block'

 L. 140       330  LOAD_GLOBAL          15  'ord'
              333  LOAD_FAST             2  's'
              336  CALL_FUNCTION_1       1  None
              339  LOAD_CONST               249
              342  COMPARE_OP            2  ==
              345  JUMP_IF_FALSE       205  'to 553'
              348  POP_TOP          

 L. 144       349  LOAD_GLOBAL          15  'ord'
              352  LOAD_FAST             3  'block'
              355  LOAD_CONST               0
              358  BINARY_SUBSCR    
              359  CALL_FUNCTION_1       1  None
              362  STORE_FAST            4  'flags'

 L. 145       365  LOAD_FAST             4  'flags'
              368  LOAD_CONST               1
              371  BINARY_AND       
              372  JUMP_IF_FALSE        27  'to 402'
            375_0  THEN                     403
              375  POP_TOP          

 L. 146       376  LOAD_GLOBAL          15  'ord'
              379  LOAD_FAST             3  'block'
              382  LOAD_CONST               3
              385  BINARY_SUBSCR    
              386  CALL_FUNCTION_1       1  None
              389  LOAD_FAST             0  'self'
              392  LOAD_ATTR            16  'info'
              395  LOAD_CONST               'transparency'
              398  STORE_SUBSCR     
              399  JUMP_FORWARD          1  'to 403'
            402_0  COME_FROM           372  '372'
              402  POP_TOP          
            403_0  COME_FROM           399  '399'

 L. 147       403  LOAD_GLOBAL          17  'i16'
              406  LOAD_FAST             3  'block'
              409  LOAD_CONST               1
              412  LOAD_CONST               3
              415  SLICE+3          
              416  CALL_FUNCTION_1       1  None
              419  LOAD_CONST               10
              422  BINARY_MULTIPLY  
              423  LOAD_FAST             0  'self'
              426  LOAD_ATTR            16  'info'
              429  LOAD_CONST               'duration'
              432  STORE_SUBSCR     

 L. 148       433  SETUP_EXCEPT         89  'to 525'

 L. 150       436  LOAD_FAST             4  'flags'
              439  LOAD_CONST               8
              442  BINARY_AND       
              443  JUMP_IF_FALSE        41  'to 487'
              446  POP_TOP          

 L. 152       447  LOAD_GLOBAL          18  'Image'
              450  LOAD_ATTR            19  'core'
              453  LOAD_ATTR            20  'fill'
              456  LOAD_CONST               'P'
              459  LOAD_FAST             0  'self'
              462  LOAD_ATTR            21  'size'

 L. 153       465  LOAD_FAST             0  'self'
              468  LOAD_ATTR            16  'info'
              471  LOAD_CONST               'background'
              474  BINARY_SUBSCR    
              475  CALL_FUNCTION_3       3  None
              478  LOAD_FAST             0  'self'
              481  STORE_ATTR            2  'dispose'
              484  JUMP_FORWARD         34  'to 521'
            487_0  COME_FROM           443  '443'
              487  POP_TOP          

 L. 154       488  LOAD_FAST             4  'flags'
              491  LOAD_CONST               16
              494  BINARY_AND       
              495  JUMP_IF_FALSE        22  'to 520'
            498_0  THEN                     521
              498  POP_TOP          

 L. 156       499  LOAD_FAST             0  'self'
              502  LOAD_ATTR            11  'im'
              505  LOAD_ATTR            22  'copy'
              508  CALL_FUNCTION_0       0  None
              511  LOAD_FAST             0  'self'
              514  STORE_ATTR            2  'dispose'
              517  JUMP_FORWARD          1  'to 521'
            520_0  COME_FROM           495  '495'
              520  POP_TOP          
            521_0  COME_FROM           517  '517'
            521_1  COME_FROM           484  '484'
              521  POP_BLOCK        
              522  JUMP_ABSOLUTE       639  'to 639'
            525_0  COME_FROM           433  '433'

 L. 157       525  DUP_TOP          
              526  LOAD_GLOBAL          23  'AttributeError'
              529  LOAD_GLOBAL          24  'KeyError'
              532  BUILD_TUPLE_2         2 
              535  COMPARE_OP           10  exception-match
              538  JUMP_IF_FALSE         7  'to 548'
              541  POP_TOP          
              542  POP_TOP          
              543  POP_TOP          
              544  POP_TOP          

 L. 158       545  JUMP_ABSOLUTE       639  'to 639'
              548  POP_TOP          
              549  END_FINALLY      
              550  JUMP_FORWARD         86  'to 639'
            553_0  COME_FROM           345  '345'
              553  POP_TOP          

 L. 159       554  LOAD_GLOBAL          15  'ord'
              557  LOAD_FAST             2  's'
              560  CALL_FUNCTION_1       1  None
              563  LOAD_CONST               255
              566  COMPARE_OP            2  ==
              569  JUMP_IF_FALSE        66  'to 638'
            572_0  THEN                     639
              572  POP_TOP          

 L. 163       573  LOAD_FAST             3  'block'
              576  LOAD_FAST             0  'self'
              579  LOAD_ATTR             9  'fp'
              582  LOAD_ATTR            25  'tell'
              585  CALL_FUNCTION_0       0  None
              588  BUILD_TUPLE_2         2 
              591  LOAD_FAST             0  'self'
              594  LOAD_ATTR            16  'info'
              597  LOAD_CONST               'extension'
              600  STORE_SUBSCR     

 L. 164       601  LOAD_FAST             3  'block'
              604  LOAD_CONST               11
              607  SLICE+2          
              608  LOAD_CONST               'NETSCAPE2.0'
              611  COMPARE_OP            2  ==
              614  JUMP_IF_FALSE        17  'to 634'
            617_0  THEN                     635
              617  POP_TOP          

 L. 165       618  LOAD_CONST               1
              621  LOAD_FAST             0  'self'
              624  LOAD_ATTR            16  'info'
              627  LOAD_CONST               'loop'
              630  STORE_SUBSCR     
              631  JUMP_ABSOLUTE       639  'to 639'
            634_0  COME_FROM           614  '614'
              634  POP_TOP          
              635  JUMP_FORWARD          1  'to 639'
            638_0  COME_FROM           569  '569'
              638  POP_TOP          
            639_0  COME_FROM           635  '635'
            639_1  COME_FROM           550  '550'

 L. 166       639  SETUP_LOOP          317  'to 959'
              642  LOAD_FAST             0  'self'
              645  LOAD_ATTR            10  'data'
              648  CALL_FUNCTION_0       0  None
              651  JUMP_IF_FALSE         4  'to 658'
              654  POP_TOP          

 L. 167       655  JUMP_BACK           642  'to 642'
              658  POP_TOP          
              659  POP_BLOCK        
              660  JUMP_BACK           243  'to 243'
            663_0  COME_FROM           296  '296'
              663  POP_TOP          

 L. 169       664  LOAD_FAST             2  's'
              667  LOAD_CONST               ','
              670  COMPARE_OP            2  ==
              673  JUMP_IF_FALSE       282  'to 958'
              676  POP_TOP          

 L. 173       677  LOAD_FAST             0  'self'
              680  LOAD_ATTR             9  'fp'
              683  LOAD_ATTR            14  'read'
              686  LOAD_CONST               9
              689  CALL_FUNCTION_1       1  None
              692  STORE_FAST            2  's'

 L. 176       695  LOAD_GLOBAL          17  'i16'
              698  LOAD_FAST             2  's'
              701  LOAD_CONST               0
              704  SLICE+1          
              705  CALL_FUNCTION_1       1  None
              708  LOAD_GLOBAL          17  'i16'
              711  LOAD_FAST             2  's'
              714  LOAD_CONST               2
              717  SLICE+1          
              718  CALL_FUNCTION_1       1  None
              721  ROT_TWO          
              722  STORE_FAST            5  'x0'
              725  STORE_FAST            6  'y0'

 L. 177       728  LOAD_FAST             5  'x0'
              731  LOAD_GLOBAL          17  'i16'
              734  LOAD_FAST             2  's'
              737  LOAD_CONST               4
              740  SLICE+1          
              741  CALL_FUNCTION_1       1  None
              744  BINARY_ADD       
              745  LOAD_FAST             6  'y0'
              748  LOAD_GLOBAL          17  'i16'
              751  LOAD_FAST             2  's'
              754  LOAD_CONST               6
              757  SLICE+1          
              758  CALL_FUNCTION_1       1  None
              761  BINARY_ADD       
              762  ROT_TWO          
              763  STORE_FAST            7  'x1'
              766  STORE_FAST            8  'y1'

 L. 178       769  LOAD_GLOBAL          15  'ord'
              772  LOAD_FAST             2  's'
              775  LOAD_CONST               8
              778  BINARY_SUBSCR    
              779  CALL_FUNCTION_1       1  None
              782  STORE_FAST            4  'flags'

 L. 180       785  LOAD_FAST             4  'flags'
              788  LOAD_CONST               64
              791  BINARY_AND       
              792  LOAD_CONST               0
              795  COMPARE_OP            3  !=
              798  STORE_FAST            9  'interlace'

 L. 182       801  LOAD_FAST             4  'flags'
              804  LOAD_CONST               128
              807  BINARY_AND       
              808  JUMP_IF_FALSE        55  'to 866'
            811_0  THEN                     867
              811  POP_TOP          

 L. 183       812  LOAD_FAST             4  'flags'
              815  LOAD_CONST               7
              818  BINARY_AND       
              819  LOAD_CONST               1
              822  BINARY_ADD       
              823  STORE_FAST           10  'bits'

 L. 185       826  LOAD_GLOBAL          26  'ImagePalette'
              829  LOAD_ATTR            27  'raw'
              832  LOAD_CONST               'RGB'
              835  LOAD_FAST             0  'self'
              838  LOAD_ATTR             9  'fp'
              841  LOAD_ATTR            14  'read'
              844  LOAD_CONST               3
              847  LOAD_FAST            10  'bits'
              850  BINARY_LSHIFT    
              851  CALL_FUNCTION_1       1  None
              854  CALL_FUNCTION_2       2  None
              857  LOAD_FAST             0  'self'
              860  STORE_ATTR           13  'palette'
              863  JUMP_FORWARD          1  'to 867'
            866_0  COME_FROM           808  '808'
              866  POP_TOP          
            867_0  COME_FROM           863  '863'

 L. 188       867  LOAD_GLOBAL          15  'ord'
              870  LOAD_FAST             0  'self'
              873  LOAD_ATTR             9  'fp'
              876  LOAD_ATTR            14  'read'
              879  LOAD_CONST               1
              882  CALL_FUNCTION_1       1  None
              885  CALL_FUNCTION_1       1  None
              888  STORE_FAST           10  'bits'

 L. 189       891  LOAD_FAST             0  'self'
              894  LOAD_ATTR             9  'fp'
              897  LOAD_ATTR            25  'tell'
              900  CALL_FUNCTION_0       0  None
              903  LOAD_FAST             0  'self'
              906  STORE_ATTR            0  '__offset'

 L. 190       909  LOAD_CONST               'gif'

 L. 191       912  LOAD_FAST             5  'x0'
              915  LOAD_FAST             6  'y0'
              918  LOAD_FAST             7  'x1'
              921  LOAD_FAST             8  'y1'
              924  BUILD_TUPLE_4         4 

 L. 192       927  LOAD_FAST             0  'self'
              930  LOAD_ATTR             0  '__offset'

 L. 193       933  LOAD_FAST            10  'bits'
              936  LOAD_FAST             9  'interlace'
              939  BUILD_TUPLE_2         2 
              942  BUILD_TUPLE_4         4 
              945  BUILD_LIST_1          1 
              948  LOAD_FAST             0  'self'
              951  STORE_ATTR            8  'tile'

 L. 194       954  BREAK_LOOP       
              955  JUMP_BACK           243  'to 243'
            958_0  COME_FROM           673  '673'
              958  POP_TOP          
            959_0  COME_FROM           639  '639'

 L. 197       959  CONTINUE            243  'to 243'
            962_0  COME_FROM           240  '240'

 L. 200       962  LOAD_FAST             0  'self'
              965  LOAD_ATTR             8  'tile'
              968  JUMP_IF_TRUE         13  'to 984'
            971_0  THEN                     985
              971  POP_TOP          

 L. 202       972  LOAD_GLOBAL          28  'EOFError'
              975  LOAD_CONST               'no more images in GIF file'
              978  RAISE_VARARGS_2       2  None
              981  JUMP_FORWARD          1  'to 985'
            984_0  COME_FROM           968  '968'
              984  POP_TOP          
            985_0  COME_FROM           981  '981'

 L. 204       985  LOAD_CONST               'L'
              988  LOAD_FAST             0  'self'
              991  STORE_ATTR           29  'mode'

 L. 205       994  LOAD_FAST             0  'self'
              997  LOAD_ATTR            13  'palette'
             1000  JUMP_IF_FALSE        13  'to 1016'
           1003_0  THEN                     1017
             1003  POP_TOP          

 L. 206      1004  LOAD_CONST               'P'
             1007  LOAD_FAST             0  'self'
             1010  STORE_ATTR           29  'mode'
             1013  JUMP_FORWARD          1  'to 1017'
           1016_0  COME_FROM          1000  '1000'
             1016  POP_TOP          
           1017_0  COME_FROM          1013  '1013'
             1017  LOAD_CONST               None
             1020  RETURN_VALUE     

Parse error at or near `CONTINUE' instruction at offset 959

    def tell(self):
        return self.__frame


try:
    import _imaging_gif
except ImportError:
    _imaging_gif = None

RAWMODE = {'1': 'L', 
   'L': 'L', 
   'P': 'P'}

def _save(im, fp, filename):
    if _imaging_gif:
        try:
            _imaging_gif.save(im, fp, filename)
            return
        except IOError:
            pass

    try:
        rawmode = RAWMODE[im.mode]
        imOut = im
    except KeyError:
        if Image.getmodebase(im.mode) == 'RGB':
            imOut = im.convert('P')
            rawmode = 'P'
        else:
            imOut = im.convert('L')
            rawmode = 'L'

    for s in getheader(imOut, im.encoderinfo):
        fp.write(s)

    flags = 0
    try:
        interlace = im.encoderinfo['interlace']
    except KeyError:
        interlace = 1

    if min(im.size) < 16:
        interlace = 0
    if interlace:
        flags = flags | 64
    try:
        transparency = im.encoderinfo['transparency']
    except KeyError:
        pass
    else:
        fp.write('!' + chr(249) + chr(4) + chr(1) + o16(0) + chr(int(transparency)) + chr(0))

    fp.write(',' + o16(0) + o16(0) + o16(im.size[0]) + o16(im.size[1]) + chr(flags) + chr(8))
    imOut.encoderconfig = (
     8, interlace)
    ImageFile._save(imOut, fp, [('gif', (0, 0) + im.size, 0, rawmode)])
    fp.write('\x00')
    fp.write(';')
    try:
        fp.flush()
    except:
        pass


def _save_netpbm(im, fp, filename):
    import os
    file = im._dump()
    if im.mode != 'RGB':
        os.system('ppmtogif %s >%s' % (file, filename))
    else:
        os.system('ppmquant 256 %s | ppmtogif >%s' % (file, filename))
    try:
        os.unlink(file)
    except:
        pass


def getheader(im, info=None):
    """Return a list of strings representing a GIF header"""
    optimize = info and info.get('optimize', 0)
    s = [
     'GIF87a' + o16(im.size[0]) + o16(im.size[1]) + chr(135) + chr(0) + chr(0)]
    if optimize:
        i = 0
        maxcolor = 0
        for count in im.histogram():
            if count:
                maxcolor = i
            i = i + 1

    else:
        maxcolor = 256
    if im.mode == 'P':
        s.append(im.im.getpalette('RGB')[:maxcolor * 3])
    for i in range(maxcolor):
        s.append(chr(i) * 3)

    return s


def getdata(im, offset=(0, 0), **params):
    """Return a list of strings representing this image.
       The first string is a local image header, the rest contains
       encoded image data."""

    class collector:
        data = []

        def write(self, data):
            self.data.append(data)

    im.load()
    fp = collector()
    try:
        im.encoderinfo = params
        fp.write(',' + o16(offset[0]) + o16(offset[1]) + o16(im.size[0]) + o16(im.size[1]) + chr(0) + chr(8))
        ImageFile._save(im, fp, [('gif', (0, 0) + im.size, 0, RAWMODE[im.mode])])
        fp.write('\x00')
    finally:
        del im.encoderinfo

    return fp.data


Image.register_open(GifImageFile.format, GifImageFile, _accept)
Image.register_save(GifImageFile.format, _save)
Image.register_extension(GifImageFile.format, '.gif')
Image.register_mime(GifImageFile.format, 'image/gif')