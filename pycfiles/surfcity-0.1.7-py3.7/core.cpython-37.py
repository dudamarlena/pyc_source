# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/surfcity/app/core.py
# Compiled at: 2019-04-07 10:39:03
# Size of source mod 2**32: 31410 bytes
import asyncio
from asyncio import ensure_future
import base64, copy, hashlib, json, logging, os, random, re, sys, time, traceback
import surfcity.app.db as db
import surfcity.app.net as net
import ssb.local.config as config
logger = logging.getLogger('ssb_app_core')
the_db = None
frontier_window = 2419200
refresh_requested = False
new_friends_flag = False

def text2synopsis(txt, ascii=False):
    txt = ' '.join(txt.split('\n'))
    txt = re.sub('\\[([^\\]]*)\\]\\([^\\)]*\\)', '[\\1]', txt)
    txt = re.sub(' +', ' ', txt)
    if ascii:
        txt = txt.encode('ascii', errors='replace').decode()
    return txt.strip()


def utc2txt(ts, fixed_width=True):
    now = time.time()
    t = time.localtime(ts)
    if now - ts < 15552000:
        t = time.strftime('%b %e/%H:%M', t)
    else:
        t = time.strftime('%b %e, %Y', t)
    if fixed_width:
        return t
    return t.replace('  ', ' ')


def feed2name(feedID):
    global the_db
    n = the_db.get_about(feedID, 'myname')
    if not n:
        n = the_db.get_about(feedID, 'name')
        if not n:
            n = the_db.get_about(feedID, 'named')
            if n:
                n = json.loads(n)
                if type(n) == list and len(n) > 0:
                    n = n[0]
                else:
                    n = None
    return n


def update_about_name(feedID, name=None, named=None, myalias=None):
    if name:
        the_db.update_about(feedID, 'name', name)
    if named:
        n = the_db.get_about(feedID, 'named')
        if n:
            n = json.loads(n)
        else:
            n = []
        if named not in n:
            n.append(named)
        the_db.update_about(feedID, 'named', json.dumps(n))
    if myalias:
        the_db.update_about(feedID, 'myname', myalias)


new_back = 0
new_forw = 0

def counter_add(b, f, ntfy=None):
    global new_back
    global new_forw
    new_back += b
    new_forw += f
    ntfy and ntfy()


def counter_reset(ntfy=None):
    global new_back
    global new_forw
    new_back, new_forw = (0, 0)
    ntfy and ntfy()


def mstr2dict(secr, mstr):
    if not mstr:
        return
        d = json.loads(mstr)
        if type(d) != dict:
            return
        if 'value' not in d:
            m = config.formatMsg(d['previous'], d['sequence'], d['author'], d['timestamp'], d['hash'], d['content'], d['signature'])
            key = hashlib.sha256(m.encode('utf8')).digest()
            key = f"%{base64.b64encode(key).decode('ascii')}.sha256"
            d = {'key':key,  'value':d,  'timestamp':int(time.time() * 1000)}
            mstr = json.dumps(d, indent=2)
        v = d['value']
        if 'content' not in v:
            return
    else:
        if type(v['content']) == str:
            c = base64.b64decode(v['content'].split('.')[0])
            c = secr.unboxPrivateData(c)
            if c != None:
                try:
                    v['content'] = json.loads(c.decode('utf8'))
                except:
                    v['content'] = '?decoding error?'

                v['private'] = True
        c = v['content']
        if type(c) == dict and c['type'] == 'post':
            the_db.add_key(d['key'], [v['author'], v['sequence']])
    v['raw'] = mstr
    v['key'] = d['key']
    return v


async def get_msgs--- This code section failed: ---

 L. 139         0  BUILD_LIST_0          0 
                2  STORE_FAST               'msgs'

 L. 140         4  SETUP_LOOP           80  'to 80'
                6  LOAD_GLOBAL              net
                8  LOAD_METHOD              get_msgs
               10  LOAD_FAST                'name'
               12  LOAD_FAST                'limit'
               14  CALL_METHOD_2         2  '2 positional arguments'
               16  GET_AITER        
             18_0  COME_FROM            54  '54'
               18  SETUP_EXCEPT         32  'to 32'
               20  GET_ANEXT        
               22  LOAD_CONST               None
               24  YIELD_FROM       
               26  STORE_FAST               'mstr'
               28  POP_BLOCK        
               30  JUMP_FORWARD         42  'to 42'
             32_0  COME_FROM_EXCEPT     18  '18'
               32  DUP_TOP          
               34  LOAD_GLOBAL              StopAsyncIteration
               36  COMPARE_OP               exception-match
               38  POP_JUMP_IF_TRUE     68  'to 68'
               40  END_FINALLY      
             42_0  COME_FROM            30  '30'

 L. 141        42  LOAD_GLOBAL              mstr2dict
               44  LOAD_FAST                'secr'
               46  LOAD_FAST                'mstr'
               48  CALL_FUNCTION_2       2  '2 positional arguments'
               50  STORE_FAST               'm'

 L. 142        52  LOAD_FAST                'm'
               54  POP_JUMP_IF_FALSE    18  'to 18'

 L. 143        56  LOAD_FAST                'msgs'
               58  LOAD_METHOD              append
               60  LOAD_FAST                'm'
               62  CALL_METHOD_1         1  '1 positional argument'
               64  POP_TOP          
               66  JUMP_BACK            18  'to 18'
             68_0  COME_FROM            38  '38'
               68  POP_TOP          
               70  POP_TOP          
               72  POP_TOP          
               74  POP_EXCEPT       
               76  POP_TOP          
               78  POP_BLOCK        
             80_0  COME_FROM_LOOP        4  '4'

 L. 144        80  LOAD_FAST                'msgs'
               82  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `COME_FROM' instruction at offset 18_0


async def id_get_frontier(secr, author, out=None):
    logger.debug(f" id_get_frontier{author}")
    low, high = (1, 256)
    key = None
    star = '|/-\\'
    starndx = 0
    while True:
        if out:
            out((star[starndx] + '\r'), end='', flush=True)
            starndx = (starndx + 1) % len(star)
        msgs = await get_msgs(secr, [author, high], 1)
        if len(msgs) == 0:
            break
        low, high = high, 2 * high
        key = msgs[0]['key']

    while high - low > 1:
        if out:
            out((star[starndx] + '\r'), end='', flush=True)
            starndx = (starndx + 1) % len(star)
        seqno = int((high + low) / 2)
        msgs = await get_msgs(secr, [author, seqno], 1)
        if len(msgs) != 0:
            low = seqno
            key = msgs[0]['key']
        else:
            high = seqno

    return (
     low, key)


def msg2recps(msg, me):
    recps = []
    if 'private' in msg:
        if msg['private']:
            c = msg['content']
            if 'recps' in c:
                if type(c['recps']) == list:
                    for r in c['recps']:
                        if type(r) == str:
                            recps.append(r)
                        else:
                            recps.append('?')

            if msg['author'] not in recps:
                recps.append(msg['author'])
            recps.sort()
    return recps


def process_msg--- This code section failed: ---

 L. 201         0  LOAD_FAST                'msg'
                2  LOAD_STR                 'author'
                4  BINARY_SUBSCR    
                6  LOAD_STR                 ':'
                8  BINARY_ADD       
               10  LOAD_GLOBAL              str
               12  LOAD_FAST                'msg'
               14  LOAD_STR                 'sequence'
               16  BINARY_SUBSCR    
               18  CALL_FUNCTION_1       1  '1 positional argument'
               20  BINARY_ADD       
               22  LOAD_FAST                'msg'
               24  LOAD_STR                 'this'
               26  STORE_SUBSCR     

 L. 202        28  LOAD_GLOBAL              type
               30  LOAD_FAST                'msg'
               32  LOAD_STR                 'content'
               34  BINARY_SUBSCR    
               36  CALL_FUNCTION_1       1  '1 positional argument'
               38  LOAD_GLOBAL              dict
               40  COMPARE_OP               !=
               42  POP_JUMP_IF_FALSE    48  'to 48'

 L. 203        44  LOAD_CONST               None
               46  RETURN_VALUE     
             48_0  COME_FROM            42  '42'

 L. 204        48  LOAD_GLOBAL              logger
               50  LOAD_METHOD              debug
               52  LOAD_STR                 'process_msg '
               54  LOAD_FAST                'msg'
               56  LOAD_STR                 'this'
               58  BINARY_SUBSCR    
               60  FORMAT_VALUE          0  ''
               62  BUILD_STRING_2        2 
               64  CALL_METHOD_1         1  '1 positional argument'
               66  POP_TOP          

 L. 205        68  LOAD_FAST                'msg'
               70  LOAD_STR                 'content'
               72  BINARY_SUBSCR    
               74  LOAD_STR                 'type'
               76  BINARY_SUBSCR    
               78  STORE_FAST               't'

 L. 206        80  LOAD_GLOBAL              int
               82  LOAD_GLOBAL              time
               84  LOAD_METHOD              time
               86  CALL_METHOD_0         0  '0 positional arguments'
               88  CALL_FUNCTION_1       1  '1 positional argument'
               90  LOAD_GLOBAL              frontier_window
               92  BINARY_SUBTRACT  
               94  STORE_FAST               'cutoff'

 L. 207        96  LOAD_FAST                't'
               98  LOAD_STR                 'post'
              100  COMPARE_OP               ==
          102_104  POP_JUMP_IF_FALSE   766  'to 766'

 L. 210       106  LOAD_GLOBAL              int
              108  LOAD_FAST                'msg'
              110  LOAD_STR                 'timestamp'
              112  BINARY_SUBSCR    
              114  LOAD_CONST               1000
              116  BINARY_TRUE_DIVIDE
              118  CALL_FUNCTION_1       1  '1 positional argument'
              120  STORE_FAST               'ts'

 L. 211       122  LOAD_FAST                'ts'
              124  LOAD_GLOBAL              time
              126  LOAD_METHOD              time
              128  CALL_METHOD_0         0  '0 positional arguments'
              130  COMPARE_OP               >
              132  POP_JUMP_IF_FALSE   142  'to 142'

 L. 212       134  LOAD_GLOBAL              time
              136  LOAD_METHOD              time
              138  CALL_METHOD_0         0  '0 positional arguments'
              140  STORE_FAST               'ts'
            142_0  COME_FROM           132  '132'

 L. 213       142  LOAD_FAST                'ts'
              144  LOAD_FAST                'msg'
              146  LOAD_STR                 'timestamp'
              148  STORE_SUBSCR     

 L. 214       150  LOAD_FAST                'ts'
              152  LOAD_FAST                'cutoff'
              154  COMPARE_OP               >=
              156  POP_JUMP_IF_FALSE   216  'to 216'

 L. 215       158  LOAD_GLOBAL              logger
              160  LOAD_METHOD              debug
              162  LOAD_STR                 'process_msg() add '
              164  LOAD_FAST                'msg'
              166  LOAD_STR                 'author'
              168  BINARY_SUBSCR    
              170  LOAD_FAST                'msg'
              172  LOAD_STR                 'sequence'
              174  BINARY_SUBSCR    
              176  BUILD_TUPLE_2         2 
              178  FORMAT_VALUE          0  ''
              180  BUILD_STRING_2        2 
              182  CALL_METHOD_1         1  '1 positional argument'
              184  POP_TOP          

 L. 216       186  LOAD_GLOBAL              the_db
              188  LOAD_METHOD              add_post
              190  LOAD_FAST                'msg'
              192  LOAD_STR                 'raw'
              194  BINARY_SUBSCR    
              196  LOAD_FAST                'msg'
              198  LOAD_STR                 'author'
              200  BINARY_SUBSCR    
              202  LOAD_FAST                'msg'
              204  LOAD_STR                 'sequence'
              206  BINARY_SUBSCR    
              208  BUILD_TUPLE_2         2 
              210  LOAD_FAST                'ts'
              212  CALL_METHOD_3         3  '3 positional arguments'
              214  POP_TOP          
            216_0  COME_FROM           156  '156'

 L. 217       216  LOAD_STR                 'mentions'
              218  LOAD_FAST                'msg'
              220  LOAD_STR                 'content'
              222  BINARY_SUBSCR    
              224  COMPARE_OP               in
          226_228  POP_JUMP_IF_FALSE   400  'to 400'
              230  LOAD_FAST                'msg'
              232  LOAD_STR                 'content'
              234  BINARY_SUBSCR    
              236  LOAD_STR                 'mentions'
              238  BINARY_SUBSCR    
          240_242  POP_JUMP_IF_FALSE   400  'to 400'

 L. 218       244  SETUP_LOOP          400  'to 400'
              246  LOAD_FAST                'msg'
              248  LOAD_STR                 'content'
              250  BINARY_SUBSCR    
              252  LOAD_STR                 'mentions'
              254  BINARY_SUBSCR    
              256  GET_ITER         
            258_0  COME_FROM           374  '374'
            258_1  COME_FROM           356  '356'
            258_2  COME_FROM           292  '292'
            258_3  COME_FROM           278  '278'
            258_4  COME_FROM           268  '268'
              258  FOR_ITER            398  'to 398'
              260  STORE_FAST               'm'

 L. 220       262  LOAD_STR                 'link'
              264  LOAD_FAST                'm'
              266  COMPARE_OP               in
          268_270  POP_JUMP_IF_FALSE   258  'to 258'
              272  LOAD_STR                 'name'
              274  LOAD_FAST                'm'
              276  COMPARE_OP               in
          278_280  POP_JUMP_IF_FALSE   258  'to 258'
              282  LOAD_FAST                'm'
              284  LOAD_STR                 'name'
              286  BINARY_SUBSCR    
              288  LOAD_STR                 'undefined'
              290  COMPARE_OP               !=
          292_294  POP_JUMP_IF_FALSE   258  'to 258'

 L. 221       296  LOAD_FAST                'm'
              298  LOAD_STR                 'link'
              300  BINARY_SUBSCR    
              302  STORE_FAST               'l'

 L. 222       304  LOAD_GLOBAL              type
              306  LOAD_FAST                'l'
              308  CALL_FUNCTION_1       1  '1 positional argument'
              310  LOAD_GLOBAL              dict
              312  COMPARE_OP               ==
          314_316  POP_JUMP_IF_FALSE   346  'to 346'
              318  LOAD_STR                 'link'
              320  LOAD_FAST                'l'
              322  COMPARE_OP               in
          324_326  POP_JUMP_IF_FALSE   346  'to 346'
              328  LOAD_STR                 'name'
              330  LOAD_FAST                'l'
              332  COMPARE_OP               in
          334_336  POP_JUMP_IF_FALSE   346  'to 346'

 L. 223       338  LOAD_FAST                'l'
              340  LOAD_STR                 'link'
              342  BINARY_SUBSCR    
              344  STORE_FAST               'l'
            346_0  COME_FROM           334  '334'
            346_1  COME_FROM           324  '324'
            346_2  COME_FROM           314  '314'

 L. 224       346  LOAD_GLOBAL              type
              348  LOAD_FAST                'l'
              350  CALL_FUNCTION_1       1  '1 positional argument'
              352  LOAD_GLOBAL              str
              354  COMPARE_OP               ==
          356_358  POP_JUMP_IF_FALSE   258  'to 258'
              360  LOAD_FAST                'l'
              362  LOAD_CONST               None
              364  LOAD_CONST               1
              366  BUILD_SLICE_2         2 
              368  BINARY_SUBSCR    
              370  LOAD_STR                 '@'
              372  COMPARE_OP               ==
          374_376  POP_JUMP_IF_FALSE   258  'to 258'

 L. 225       378  LOAD_GLOBAL              update_about_name
              380  LOAD_FAST                'l'
              382  LOAD_FAST                'm'
              384  LOAD_STR                 'name'
              386  BINARY_SUBSCR    
              388  LOAD_CONST               ('named',)
              390  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              392  POP_TOP          
          394_396  JUMP_BACK           258  'to 258'
              398  POP_BLOCK        
            400_0  COME_FROM_LOOP      244  '244'
            400_1  COME_FROM           240  '240'
            400_2  COME_FROM           226  '226'

 L. 226       400  LOAD_STR                 'root'
              402  LOAD_FAST                'msg'
              404  LOAD_STR                 'content'
              406  BINARY_SUBSCR    
              408  COMPARE_OP               in
          410_412  POP_JUMP_IF_FALSE   630  'to 630'

 L. 227       414  LOAD_GLOBAL              type
              416  LOAD_FAST                'msg'
              418  LOAD_STR                 'content'
              420  BINARY_SUBSCR    
              422  LOAD_STR                 'root'
              424  BINARY_SUBSCR    
              426  CALL_FUNCTION_1       1  '1 positional argument'
              428  LOAD_GLOBAL              str
              430  COMPARE_OP               ==
          432_434  POP_JUMP_IF_FALSE   762  'to 762'

 L. 228       436  LOAD_FAST                'msg'
              438  LOAD_STR                 'content'
              440  BINARY_SUBSCR    
              442  LOAD_STR                 'root'
              444  BINARY_SUBSCR    
              446  STORE_FAST               'rkey'

 L. 233       448  LOAD_FAST                'msg'
              450  LOAD_STR                 'timestamp'
              452  BINARY_SUBSCR    
              454  STORE_FAST               'ts'

 L. 234       456  SETUP_EXCEPT        490  'to 490'

 L. 235       458  LOAD_GLOBAL              the_db
              460  LOAD_METHOD              get_thread_newest
              462  LOAD_FAST                'rkey'
              464  CALL_METHOD_1         1  '1 positional argument'
              466  LOAD_FAST                'ts'
              468  COMPARE_OP               <
          470_472  POP_JUMP_IF_FALSE   486  'to 486'

 L. 236       474  LOAD_GLOBAL              the_db
              476  LOAD_METHOD              update_thread_newest
              478  LOAD_FAST                'rkey'
              480  LOAD_FAST                'ts'
              482  CALL_METHOD_2         2  '2 positional arguments'
              484  POP_TOP          
            486_0  COME_FROM           470  '470'
              486  POP_BLOCK        
              488  JUMP_FORWARD        522  'to 522'
            490_0  COME_FROM_EXCEPT    456  '456'

 L. 237       490  POP_TOP          
              492  POP_TOP          
              494  POP_TOP          

 L. 238       496  LOAD_GLOBAL              the_db
              498  LOAD_METHOD              add_thread
              500  LOAD_GLOBAL              msg2recps
              502  LOAD_FAST                'msg'
              504  LOAD_FAST                'me'
              506  CALL_FUNCTION_2       2  '2 positional arguments'
              508  LOAD_FAST                'rkey'
              510  LOAD_FAST                'ts'
              512  CALL_METHOD_3         3  '3 positional arguments'
              514  POP_TOP          
              516  POP_EXCEPT       
              518  JUMP_FORWARD        522  'to 522'
              520  END_FINALLY      
            522_0  COME_FROM           518  '518'
            522_1  COME_FROM           488  '488'

 L. 239       522  LOAD_GLOBAL              the_db
              524  LOAD_METHOD              add_tip_to_thread
              526  LOAD_FAST                'rkey'
              528  LOAD_FAST                'msg'
              530  LOAD_STR                 'key'
              532  BINARY_SUBSCR    
              534  CALL_METHOD_2         2  '2 positional arguments'
              536  POP_TOP          

 L. 240       538  LOAD_STR                 'branch'
              540  LOAD_FAST                'msg'
              542  LOAD_STR                 'content'
              544  BINARY_SUBSCR    
              546  COMPARE_OP               in
          548_550  POP_JUMP_IF_FALSE   612  'to 612'

 L. 241       552  LOAD_FAST                'msg'
              554  LOAD_STR                 'content'
              556  BINARY_SUBSCR    
              558  LOAD_STR                 'branch'
              560  BINARY_SUBSCR    
              562  STORE_FAST               'br'

 L. 242       564  LOAD_GLOBAL              type
              566  LOAD_FAST                'br'
              568  CALL_FUNCTION_1       1  '1 positional argument'
              570  LOAD_GLOBAL              str
              572  COMPARE_OP               ==
          574_576  POP_JUMP_IF_FALSE   584  'to 584'

 L. 243       578  LOAD_FAST                'br'
              580  BUILD_LIST_1          1 
              582  STORE_FAST               'br'
            584_0  COME_FROM           574  '574'

 L. 244       584  SETUP_LOOP          612  'to 612'
              586  LOAD_FAST                'br'
              588  GET_ITER         
              590  FOR_ITER            610  'to 610'
              592  STORE_FAST               'key'

 L. 245       594  LOAD_GLOBAL              the_db
              596  LOAD_METHOD              add_tip_to_thread
              598  LOAD_FAST                'rkey'
              600  LOAD_FAST                'key'
              602  CALL_METHOD_2         2  '2 positional arguments'
              604  POP_TOP          
          606_608  JUMP_BACK           590  'to 590'
              610  POP_BLOCK        
            612_0  COME_FROM_LOOP      584  '584'
            612_1  COME_FROM           548  '548'

 L. 246       612  LOAD_GLOBAL              the_db
              614  LOAD_METHOD              add_author_to_thread
              616  LOAD_FAST                'rkey'
              618  LOAD_FAST                'msg'
              620  LOAD_STR                 'author'
              622  BINARY_SUBSCR    
              624  CALL_METHOD_2         2  '2 positional arguments'
              626  POP_TOP          
              628  JUMP_FORWARD       1264  'to 1264'
            630_0  COME_FROM           410  '410'

 L. 247       630  LOAD_STR                 'text'
              632  LOAD_FAST                'msg'
              634  LOAD_STR                 'content'
              636  BINARY_SUBSCR    
              638  COMPARE_OP               in
          640_642  POP_JUMP_IF_FALSE  1264  'to 1264'
              644  LOAD_GLOBAL              type
              646  LOAD_FAST                'msg'
              648  LOAD_STR                 'content'
              650  BINARY_SUBSCR    
              652  LOAD_STR                 'text'
              654  BINARY_SUBSCR    
              656  CALL_FUNCTION_1       1  '1 positional argument'
              658  LOAD_GLOBAL              str
              660  COMPARE_OP               ==
          662_664  POP_JUMP_IF_FALSE  1264  'to 1264'

 L. 249       666  LOAD_FAST                'msg'
              668  LOAD_STR                 'key'
              670  BINARY_SUBSCR    
              672  STORE_FAST               'mkey'

 L. 250       674  LOAD_GLOBAL              the_db
              676  LOAD_METHOD              add_thread
              678  LOAD_GLOBAL              msg2recps
              680  LOAD_FAST                'msg'
              682  LOAD_FAST                'me'
              684  CALL_FUNCTION_2       2  '2 positional arguments'
              686  LOAD_FAST                'mkey'
              688  LOAD_FAST                'msg'
              690  LOAD_STR                 'timestamp'
              692  BINARY_SUBSCR    
              694  CALL_METHOD_3         3  '3 positional arguments'
              696  POP_TOP          

 L. 251       698  LOAD_GLOBAL              the_db
              700  LOAD_METHOD              add_author_to_thread
              702  LOAD_FAST                'mkey'
              704  LOAD_FAST                'msg'
              706  LOAD_STR                 'author'
              708  BINARY_SUBSCR    
              710  CALL_METHOD_2         2  '2 positional arguments'
              712  POP_TOP          

 L. 252       714  LOAD_GLOBAL              the_db
              716  LOAD_METHOD              add_tip_to_thread
              718  LOAD_FAST                'mkey'
              720  LOAD_FAST                'mkey'
              722  CALL_METHOD_2         2  '2 positional arguments'
              724  POP_TOP          

 L. 253       726  LOAD_GLOBAL              text2synopsis
              728  LOAD_FAST                'msg'
              730  LOAD_STR                 'content'
              732  BINARY_SUBSCR    
              734  LOAD_STR                 'text'
              736  BINARY_SUBSCR    
              738  CALL_FUNCTION_1       1  '1 positional argument'
              740  LOAD_CONST               None
              742  LOAD_CONST               256
              744  BUILD_SLICE_2         2 
              746  BINARY_SUBSCR    
              748  STORE_FAST               'txt'

 L. 254       750  LOAD_GLOBAL              the_db
              752  LOAD_METHOD              update_thread_title
              754  LOAD_FAST                'mkey'
              756  LOAD_FAST                'txt'
              758  CALL_METHOD_2         2  '2 positional arguments'
              760  POP_TOP          
            762_0  COME_FROM           432  '432'
          762_764  JUMP_FORWARD       1264  'to 1264'
            766_0  COME_FROM           102  '102'

 L. 255       766  LOAD_FAST                't'
              768  LOAD_STR                 'about'
              770  COMPARE_OP               ==
          772_774  POP_JUMP_IF_FALSE   934  'to 934'
              776  LOAD_STR                 'name'
              778  LOAD_FAST                'msg'
              780  LOAD_STR                 'content'
              782  BINARY_SUBSCR    
              784  COMPARE_OP               in
          786_788  POP_JUMP_IF_FALSE   934  'to 934'

 L. 256       790  LOAD_STR                 'about'
              792  LOAD_FAST                'msg'
              794  LOAD_STR                 'content'
              796  BINARY_SUBSCR    
              798  COMPARE_OP               in
          800_802  POP_JUMP_IF_FALSE   934  'to 934'
              804  LOAD_FAST                'msg'
              806  LOAD_STR                 'content'
              808  BINARY_SUBSCR    
              810  LOAD_STR                 'name'
              812  BINARY_SUBSCR    
              814  LOAD_STR                 'undefined'
              816  COMPARE_OP               !=
          818_820  POP_JUMP_IF_FALSE   934  'to 934'

 L. 257       822  LOAD_FAST                'msg'
              824  LOAD_STR                 'content'
              826  BINARY_SUBSCR    
              828  LOAD_STR                 'about'
              830  BINARY_SUBSCR    
              832  STORE_FAST               'a'

 L. 258       834  LOAD_FAST                'a'
              836  LOAD_FAST                'msg'
              838  LOAD_STR                 'author'
              840  BINARY_SUBSCR    
              842  COMPARE_OP               ==
          844_846  POP_JUMP_IF_FALSE   874  'to 874'

 L. 259       848  LOAD_GLOBAL              update_about_name
              850  LOAD_FAST                'msg'
              852  LOAD_STR                 'author'
              854  BINARY_SUBSCR    
              856  LOAD_FAST                'msg'
              858  LOAD_STR                 'content'
              860  BINARY_SUBSCR    
              862  LOAD_STR                 'name'
              864  BINARY_SUBSCR    
              866  LOAD_CONST               ('name',)
              868  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              870  POP_TOP          
              872  JUMP_FORWARD       1264  'to 1264'
            874_0  COME_FROM           844  '844'

 L. 260       874  LOAD_FAST                'msg'
              876  LOAD_STR                 'author'
              878  BINARY_SUBSCR    
              880  LOAD_FAST                'me'
              882  COMPARE_OP               ==
          884_886  POP_JUMP_IF_FALSE   910  'to 910'

 L. 261       888  LOAD_GLOBAL              update_about_name
              890  LOAD_FAST                'a'
              892  LOAD_FAST                'msg'
              894  LOAD_STR                 'content'
              896  BINARY_SUBSCR    
              898  LOAD_STR                 'name'
              900  BINARY_SUBSCR    
              902  LOAD_CONST               ('myalias',)
              904  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              906  POP_TOP          
              908  JUMP_FORWARD       1264  'to 1264'
            910_0  COME_FROM           884  '884'

 L. 263       910  LOAD_GLOBAL              update_about_name
              912  LOAD_FAST                'a'
              914  LOAD_FAST                'msg'
              916  LOAD_STR                 'content'
              918  BINARY_SUBSCR    
              920  LOAD_STR                 'name'
              922  BINARY_SUBSCR    
              924  LOAD_CONST               ('named',)
              926  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              928  POP_TOP          
          930_932  JUMP_FORWARD       1264  'to 1264'
            934_0  COME_FROM           818  '818'
            934_1  COME_FROM           800  '800'
            934_2  COME_FROM           786  '786'
            934_3  COME_FROM           772  '772'

 L. 264       934  LOAD_FAST                't'
              936  LOAD_STR                 'contact'
              938  COMPARE_OP               ==
          940_942  POP_JUMP_IF_FALSE  1188  'to 1188'
              944  LOAD_GLOBAL              type
              946  LOAD_FAST                'msg'
              948  LOAD_STR                 'content'
              950  BINARY_SUBSCR    
              952  CALL_FUNCTION_1       1  '1 positional argument'
              954  LOAD_GLOBAL              dict
              956  COMPARE_OP               ==
          958_960  POP_JUMP_IF_FALSE  1188  'to 1188'

 L. 265       962  LOAD_STR                 'pub'
              964  LOAD_FAST                'msg'
              966  LOAD_STR                 'content'
              968  BINARY_SUBSCR    
              970  COMPARE_OP               not-in
          972_974  POP_JUMP_IF_FALSE  1188  'to 1188'
              976  LOAD_STR                 'contact'
              978  LOAD_FAST                'msg'
              980  LOAD_STR                 'content'
              982  BINARY_SUBSCR    
              984  COMPARE_OP               in
          986_988  POP_JUMP_IF_FALSE  1188  'to 1188'

 L. 266       990  LOAD_GLOBAL              type
              992  LOAD_FAST                'msg'
              994  LOAD_STR                 'content'
              996  BINARY_SUBSCR    
              998  LOAD_STR                 'contact'
             1000  BINARY_SUBSCR    
             1002  CALL_FUNCTION_1       1  '1 positional argument'
             1004  LOAD_GLOBAL              str
             1006  COMPARE_OP               ==
         1008_1010  POP_JUMP_IF_FALSE  1188  'to 1188'

 L. 267      1012  LOAD_FAST                'msg'
             1014  LOAD_STR                 'content'
             1016  BINARY_SUBSCR    
             1018  STORE_FAST               'c'

 L. 268      1020  LOAD_STR                 'blocking'
             1022  LOAD_FAST                'c'
             1024  COMPARE_OP               in
         1026_1028  POP_JUMP_IF_FALSE  1066  'to 1066'
             1030  LOAD_FAST                'c'
             1032  LOAD_STR                 'blocking'
             1034  BINARY_SUBSCR    
         1036_1038  POP_JUMP_IF_FALSE  1066  'to 1066'

 L. 269      1040  LOAD_GLOBAL              the_db
             1042  LOAD_METHOD              update_follow
             1044  LOAD_FAST                'msg'
             1046  LOAD_STR                 'author'
             1048  BINARY_SUBSCR    
             1050  LOAD_FAST                'c'
             1052  LOAD_STR                 'contact'
             1054  BINARY_SUBSCR    
             1056  LOAD_CONST               2
             1058  LOAD_FAST                'backwards'
             1060  CALL_METHOD_4         4  '4 positional arguments'
             1062  POP_TOP          
             1064  JUMP_FORWARD       1186  'to 1186'
           1066_0  COME_FROM          1036  '1036'
           1066_1  COME_FROM          1026  '1026'

 L. 270      1066  LOAD_STR                 'following'
             1068  LOAD_FAST                'c'
             1070  COMPARE_OP               in
         1072_1074  POP_JUMP_IF_FALSE  1264  'to 1264'

 L. 271      1076  LOAD_FAST                'c'
             1078  LOAD_STR                 'following'
             1080  BINARY_SUBSCR    
         1082_1084  POP_JUMP_IF_FALSE  1162  'to 1162'

 L. 272      1086  LOAD_GLOBAL              new_friends_flag
         1088_1090  POP_JUMP_IF_TRUE   1136  'to 1136'
             1092  LOAD_FAST                'msg'
             1094  LOAD_STR                 'author'
             1096  BINARY_SUBSCR    
             1098  LOAD_FAST                'me'
             1100  COMPARE_OP               ==
         1102_1104  POP_JUMP_IF_FALSE  1136  'to 1136'

 L. 273      1106  LOAD_FAST                'backwards'
         1108_1110  POP_JUMP_IF_FALSE  1132  'to 1132'
             1112  LOAD_FAST                'c'
             1114  LOAD_STR                 'contact'
             1116  BINARY_SUBSCR    

 L. 274      1118  LOAD_GLOBAL              the_db
             1120  LOAD_METHOD              get_following
             1122  LOAD_FAST                'me'
             1124  CALL_METHOD_1         1  '1 positional argument'
             1126  COMPARE_OP               not-in
           1128_0  COME_FROM           628  '628'
         1128_1130  POP_JUMP_IF_FALSE  1136  'to 1136'
           1132_0  COME_FROM          1108  '1108'

 L. 275      1132  LOAD_CONST               True
             1134  STORE_GLOBAL             new_friends_flag
           1136_0  COME_FROM          1128  '1128'
           1136_1  COME_FROM          1102  '1102'
           1136_2  COME_FROM          1088  '1088'

 L. 276      1136  LOAD_GLOBAL              the_db
             1138  LOAD_METHOD              update_follow
             1140  LOAD_FAST                'msg'
             1142  LOAD_STR                 'author'
             1144  BINARY_SUBSCR    
             1146  LOAD_FAST                'c'
             1148  LOAD_STR                 'contact'
             1150  BINARY_SUBSCR    

 L. 277      1152  LOAD_CONST               0
             1154  LOAD_FAST                'backwards'
             1156  CALL_METHOD_4         4  '4 positional arguments'
             1158  POP_TOP          
             1160  JUMP_FORWARD       1186  'to 1186'
           1162_0  COME_FROM          1082  '1082'

 L. 279      1162  LOAD_GLOBAL              the_db
             1164  LOAD_METHOD              update_follow
             1166  LOAD_FAST                'msg'
             1168  LOAD_STR                 'author'
             1170  BINARY_SUBSCR    
             1172  LOAD_FAST                'c'
             1174  LOAD_STR                 'contact'
             1176  BINARY_SUBSCR    

 L. 280      1178  LOAD_CONST               1
             1180  LOAD_FAST                'backwards'
             1182  CALL_METHOD_4         4  '4 positional arguments'
             1184  POP_TOP          
           1186_0  COME_FROM          1160  '1160'
           1186_1  COME_FROM          1064  '1064'
             1186  JUMP_FORWARD       1264  'to 1264'
           1188_0  COME_FROM          1008  '1008'
           1188_1  COME_FROM           986  '986'
           1188_2  COME_FROM           972  '972'
           1188_3  COME_FROM           958  '958'
           1188_4  COME_FROM           940  '940'

 L. 281      1188  LOAD_FAST                't'
             1190  LOAD_STR                 'pub'
             1192  COMPARE_OP               ==
         1194_1196  POP_JUMP_IF_FALSE  1264  'to 1264'
             1198  LOAD_FAST                'msg'
             1200  LOAD_STR                 'author'
             1202  BINARY_SUBSCR    
           1204_0  COME_FROM           872  '872'
             1204  LOAD_FAST                'me'
             1206  COMPARE_OP               ==
         1208_1210  POP_JUMP_IF_FALSE  1264  'to 1264'
             1212  LOAD_STR                 'address'
             1214  LOAD_FAST                'msg'
             1216  LOAD_STR                 'content'
             1218  BINARY_SUBSCR    
             1220  COMPARE_OP               in
         1222_1224  POP_JUMP_IF_FALSE  1264  'to 1264'

 L. 282      1226  LOAD_FAST                'msg'
             1228  LOAD_STR                 'content'
             1230  BINARY_SUBSCR    
             1232  LOAD_STR                 'address'
             1234  BINARY_SUBSCR    
             1236  STORE_FAST               'a'

 L. 283      1238  LOAD_GLOBAL              the_db
           1240_0  COME_FROM           908  '908'
             1240  LOAD_METHOD              add_pub
             1242  LOAD_FAST                'a'
             1244  LOAD_STR                 'key'
             1246  BINARY_SUBSCR    
             1248  LOAD_FAST                'a'
             1250  LOAD_STR                 'host'
             1252  BINARY_SUBSCR    
             1254  LOAD_FAST                'a'
             1256  LOAD_STR                 'port'
             1258  BINARY_SUBSCR    
             1260  CALL_METHOD_3         3  '3 positional arguments'
             1262  POP_TOP          
           1264_0  COME_FROM          1222  '1222'
           1264_1  COME_FROM          1208  '1208'
           1264_2  COME_FROM          1194  '1194'
           1264_3  COME_FROM          1186  '1186'
           1264_4  COME_FROM          1072  '1072'
           1264_5  COME_FROM           930  '930'
           1264_6  COME_FROM           762  '762'
           1264_7  COME_FROM           662  '662'
           1264_8  COME_FROM           640  '640'

Parse error at or near `POP_JUMP_IF_FALSE' instruction at offset 1128_1130


async def scan_my_log(secr, args, out=None, ntfy=None):
    global refresh_requested
    front, _ = the_db.get_id_front(secr.id)
    if front <= 1:
        out and out('Bootstrapping into own log, determining its size...')
        front, key = await id_get_frontier(secr, secr.id, out)
        out and out(f"Log for {secr.id} has {front} entries.")
        the_db.update_id_front(secr.id, front, key)
        refresh_requested = True
    elif front == 0:
        out and out('own log is empty')
        return
        low = the_db.get_id_low(secr.id)
        if args.nocatchup or low == 1:
            return
        if low == -1:
            end = front + 1
    else:
        end = low
    start = end
    ts = 0
    cnt = 0
    if start > 1:
        out and out('\rscanned 0 entries of own log', end='', flush=True)
    while start > 1:
        start = 1 if start - 40 < 1 else start - 40
        msgs = await get_msgs(secr, [secr.id, start], end - start)
        msgs.reverse()
        for msg in msgs:
            process_msg(msg, (secr.id), backwards=True)
            counter_add(1, 0, ntfy)
            cnt += 1
            out and out(('\r' + f"scanned {cnt} entries of own log"), end='', flush=True)

        if len(the_db.get_following(secr.id)) > 0:
            break
        end = start

    the_db.update_id_low(secr.id, start)
    out and out('\r' + f"Total of {front - start + 1} from {front} own log entries scanned so far.")


async def scan_wavefront(me, secr, args, out=None, ntfy=None):
    await scan_my_log(secr, args, out, ntfy)
    out and out('Visiting logs of followed feeds')
    following = the_db.get_following(me)
    following.append(me)
    i = 0
    out and out(f"0 of {len(following)} followed feeds visited...", end='', flush=True)
    for f in following:
        front, _ = the_db.get_id_front(f)
        if front <= 1:
            continue
        if not args.nocatchup:
            low = the_db.get_id_low(f)
            if low != 1:
                if low == -1:
                    start = front - 10
                    end = front + 1
                else:
                    start = low - 10
                    end = low
                if start < 1:
                    start = 1
                msgs = await get_msgs(secr, [f, start], end - start)
                msgs.reverse()
                for m in msgs:
                    process_msg(m, me, backwards=True)
                    counter_add(1, 0, ntfy)

                if len(msgs) > 0:
                    the_db.update_id_low(f, start)
            if refresh_requested:
                out and out('\nList refresh requested')
                return
            i += 1
            out and out(('\r' + f"{i} of {len(following)} followed feeds visited..."), end='', flush=True)

    if args.narrow:
        return
    out and out('\nVisiting logs of randomly selected follo-followed feeds')
    ffollowing = the_db.get_follofollowing(me)
    for f in following:
        if f in ffollowing:
            ffollowing.remove(f)

    if 2 * len(following) < len(ffollowing):
        ffollowing = random.sample(ffollowing, 2 * len(following))
    i = 0
    out and out(f"0 of {len(ffollowing)} random follo-followed feeds visited...", end='', flush=True)
    for f in ffollowing:
        front, _ = the_db.get_id_front(f)
        if front <= 1:
            front, key = await id_get_frontier(secr, f, out)
            the_db.update_id_front(f, front, key)
        if not args.nocatchup:
            low = the_db.get_id_low(f)
            batch_size = 20
            if low != 1:
                if low == -1:
                    start = front - batch_size
                    end = front + 1
                else:
                    start = low - batch_size
                    end = low
                if start < 1:
                    start = 1
                msgs = await get_msgs(secr, [f, start], end - start)
                msgs.reverse()
                for m in msgs:
                    process_msg(m, me, backwards=True)
                    counter_add(1, 0, ntfy)

                if len(msgs) > 0:
                    the_db.update_id_low(f, start)
            if refresh_requested:
                out and out('\nList refresh requested')
                return
            msgs = await get_msgs(secr, [f, front + 1], 5)
            if len(msgs) > 0:
                for m in msgs:
                    process_msg(m, me, backwards=False)
                    counter_add(0, 1, ntfy)

                the_db.update_id_front(f, m['sequence'], m['key'])
            i += 1
            if refresh_requested:
                out and out('\nList refresh requested')
                return
            out and out(('\r' + f"{i} of {len(ffollowing)} random follo-followed feeds visited..."), end='', flush=True)


async def mk_convo_list(secr, args, cache_only):
    threads = the_db.list_newest_threads(limit=(args.nr_thr), public=False)
    convos = {}
    order = []
    for t in threads:
        recps = the_db.get_thread_recps(t)
        if secr.id in recps:
            recps.remove(secr.id)
        recps.sort()
        r = str(recps)
        if r not in order:
            order.append(r)
        if r not in convos:
            convos[r] = {'threads':[],  'recps':recps}
        r = convos[r]
        r['threads'].append(t)

    lst = []
    for r in order:
        msgs = []
        new_count = 0
        for t in convos[r]['threads']:
            lastread = the_db.get_thread_lastread(t)
            queue = the_db.get_thread_tips(t)
            queue.append(t)
            done = []
            while len(queue) > 0:
                k = queue.pop()
                if k in done:
                    continue
                done.append(k)
                nm = the_db.get_msgName(k)
                if not nm:
                    continue
                rec = the_db.get_post(nm)
                m = None
                if rec:
                    m = mstr2dictsecrrec[0]
                    if m:
                        m['timestamp'] = rec[1]
                if not m:
                    if args.offline or cache_only:
                        continue
                    m = await get_msgssecrnm
                    if len(m) == 0:
                        continue
                    m = m[0]
                    ts = int(m['timestamp'] / 1000)
                    if ts > time.time():
                        ts = time.time()
                    m['timestamp'] = ts
                    the_db.add_post(m['raw'], (m['author'], m['sequence']), ts)
                c = m['content']
                if type(c) != dict or c['type'] != 'post':
                    continue
                msgs.append(m)
                if m['timestamp'] > lastread:
                    new_count += 1

        msgs.sort(key=(lambda x: x['timestamp']))
        convos[r]['msgs'] = msgs
        convos[r]['new_count'] = new_count
        lst.append(convos[r])

    return lst


def mk_thread_list(secr, args, cache_only=False, extended_network=False):
    lst = the_db.list_newest_threads(limit=(args.nr_thr), public=True)
    if not extended_network:
        fol = the_db.get_following(secr.id)
        if secr.id not in fol:
            fol.append(secr.id)
        following = set(fol)
        lst2 = []
        for t in lst:
            authors = the_db.get_thread_authors(t)
            isect = [a for a in authors if a in following]
            if len(isect) == 0:
                pass
            else:
                lst2.append(t)
            lst = lst2

    return lst


async def expand_convo(secr, convo, args, cache_only, ascii=False):
    txt = []
    nms = []
    lst = convo['recps']
    if len(lst) == 0:
        lst = [
         secr.id]
    else:
        for r in lst:
            n = feed2name(r)
            if not n:
                n = r
            else:
                if ascii:
                    n = n.encode('ascii', errors='replace').decode()
            nms.append(n)

        txt.append((False, f"<{', '.join(nms)[:50]}>"))
        msgs = convo['msgs']
        msgs.sort(key=(lambda x: x['timestamp']))
        new_count = 0
        msgs2 = msgs[-args.nr_msg:]
        for m in msgs2:
            a = m['author']
            n = feed2name(m['author'])
            if not n:
                n = m['author']
            if ascii:
                n = n.encode('ascii', errors='replace').decode()
            t = text2synopsis((m['content']['text']), ascii=ascii)
            txt.append((utc2txt(m['timestamp']), n, t))

        if len(msgs2) > 0:
            pass
        else:
            txt.append(('?', '?', '?'))
    return (
     msgs, txt, convo['new_count'])


async def expand_thread(secr, t, args, cache_only, blocked=None, ascii=False):
    """ returns a tuple (a,b,c) with two lists:
     a) list of sorted messages
     b) list with
           ndx=0     (new_count, titleStr)
           ndx=1..   (date, author, msgStartStr)
     c) isPrivateFlag
    """
    recps = the_db.get_thread_recps(t)
    title = the_db.get_thread_title(t)
    title = text2synopsistitleascii if title else '..'
    lastread = the_db.get_thread_lastread(t)
    msgs = []
    new_count = 0
    done = []
    queue = the_db.get_thread_tips(t)
    queue.append(t)
    while len(queue) > 0:
        k = queue.pop()
        if k in done:
            continue
        done.append(k)
        nm = the_db.get_msgName(k)
        if not nm:
            continue
        r = the_db.get_post(nm)
        m = None
        if r:
            m = mstr2dictsecrr[0]
            if m:
                m['timestamp'] = r[1]
        if not m:
            if args.offline or cache_only:
                continue
            m = await get_msgssecrnm
            if len(m) == 0:
                continue
            m = m[0]
            ts = int(m['timestamp'] / 1000)
            if ts > time.time():
                ts = time.time()
            m['timestamp'] = ts
            the_db.add_post(m['raw'], (m['author'], m['sequence']), ts)
        if blocked:
            if m['author'] in blocked:
                continue
        c = m['content']
        if type(c) != dict or c['type'] != 'post':
            continue
        msgs.append(m)
        if m['timestamp'] > lastread:
            new_count += 1

    msgs.sort(key=(lambda x: x['timestamp']))
    txt = [
     (
      new_count, title)]
    msgs2 = msgs[-args.nr_msg:]
    for m in msgs2:
        a = m['author']
        n = feed2name(m['author'])
        if not n:
            n = m['author']
        if ascii:
            n = n.encode('ascii', errors='replace').decode()
        t = text2synopsis((m['content']['text']), ascii=ascii)
        txt.append((utc2txt(m['timestamp']), n, t))

    return (
     msgs, txt, recps != [])


def my_cb(secr, data, ntfy=None):
    try:
        msg = mstr2dictsecrdata.decode('utf8')
        if msg:
            process_msgmsgsecr.id
            front, _ = the_db.get_id_front(msg['author'])
            if msg['sequence'] > front:
                the_db.update_id_front(msg['author'], msg['sequence'], msg['key'])
                counter_add(0, 1, ntfy)
    except Exception as e:
        try:
            logger.info(' ** my_cb exception %s', str(e))
            logger.info(' ** %s', traceback.format_exc())
        finally:
            e = None
            del e


async def process_new_friends(secr, out=None, ntfy=None):
    following = the_db.get_following(secr.id)
    following.append(secr.id)
    try:
        for feed in following:
            front, _ = the_db.get_id_front(feed)
            if front < 1:
                out and out(f"Probe frontier for {feed}")
                front, key = await id_get_frontier(secr, feed, out)
                msgs = await get_msgssecr(feed, front)
                process_msgmsgs[0]secr.id
                the_db.update_id_front(feed, front, key)
            net.start_feed_watching((feed, front + 1), lambda data: my_cb(secr, data, ntfy))

    except:
        logger.exception('process_new_friend')
        print('exception in process_new_friend()')


async def push(msg):
    try:
        net.my_feed_send_queue.put(msg)
    except Exception as e:
        try:
            logger.info(' ** push %s', str(e))
            logger.info(' ** %s', traceback.format_exc())
        finally:
            e = None
            del e


def submit_public_post(secr, txt, root=None, branch=None):
    seq, key = the_db.get_id_front(secr.id)
    txt = {'type':'post', 
     'text':txt, 
     'recps':None}
    if root:
        txt['root'] = root
    else:
        if branch:
            txt['branch'] = branch
        msg = config.formatMsg(key, seq + 1, secr.id, int(time.time() * 1000), 'sha256', txt, None)
        sig = base64.b64encode(secr.sign(msg.encode('utf8'))).decode('ascii') + '.sig.ed25519'
        msg = msg[:-2] + ',\n  "signature": "%s"\n}' % sig
        jmsg = json.loads(msg)
        if not 'author' not in jmsg:
            if 'signature' not in jmsg:
                raise ValueError
            s = base64.b64decode(jmsg['signature'])
            i = msg.find(',\n  "signature":')
            m = (msg[:i] + '\n}').encode('utf8')
            if not config.verify_signature(jmsg['author'], m, s):
                logger.info('  invalid signature')
            else:
                logger.info('  valid signature')
            withKeys = False
            if withKeys:
                h = hashlib.sha256(msg.encode('utf8')).digest()
                msg = {'key':'%' + base64.b64encode(h).decode('ascii') + '.sha256',  'value':json.loads(msg), 
                 'timestamp':int(time.time() * 1000)}
        else:
            msg = json.loads(msg)
    asyncio.ensure_future(push(msg))


def submit_private_post(secr, txt, root=None, branch=None):
    seq, key = the_db.get_id_front(secr.id)
    recps = ['@AiBJDta+4boyh2USNGwIagH/wKjeruTcDX2Aj1r/haM=.ed25519', secr.id]
    txt = {'type':'post', 
     'text':txt, 
     'recps':recps}
    if root:
        txt['root'] = root
    else:
        if branch:
            txt['branch'] = branch
        box = secr.boxPrivateData(json.dumps(txt).encode('utf8'), recps)
        box = base64.b64encode(box).decode('ascii') + '.box'
        msg = config.formatMsg(key, seq + 1, secr.id, int(time.time() * 1000), 'sha256', box, None)
        sig = base64.b64encode(secr.sign(msg.encode('utf8'))).decode('ascii') + '.sig.ed25519'
        msg = msg[:-2] + ',\n  "signature": "%s"\n}' % sig
        jmsg = json.loads(msg)
        if not 'author' not in jmsg:
            if 'signature' not in jmsg:
                raise ValueError
            s = base64.b64decode(jmsg['signature'])
            i = msg.find(',\n  "signature":')
            m = (msg[:i] + '\n}').encode('utf8')
            if not config.verify_signature(jmsg['author'], m, s):
                logger.info('  invalid signature')
            else:
                logger.info('  valid signature')
            withKeys = False
            if withKeys:
                h = hashlib.sha256(msg.encode('utf8')).digest()
                msg = {'key':'%' + base64.b64encode(h).decode('ascii') + '.sha256',  'value':json.loads(msg), 
                 'timestamp':int(time.time() * 1000)}
        else:
            msg = json.loads(msg)
    asyncio.ensure_future(net.my_feed_send_queue.put(msg))


def init():
    global the_db
    the_db = db.SURFCITY_DB()


if __name__ == '__main__':
    print('nothing to see here')
# global new_friends_flag ## Warning: Unused global