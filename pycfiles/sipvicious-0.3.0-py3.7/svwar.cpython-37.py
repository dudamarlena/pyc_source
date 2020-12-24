# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sipvicious/svwar.py
# Compiled at: 2020-02-18 00:36:42
# Size of source mod 2**32: 29837 bytes
__GPL__ = '\n\n   Sipvicious extension line scanner scans SIP PaBXs for valid extension lines\n   Copyright (C) 2007-2020 Sandro Gauci <sandro@enablesecurity.com>\n\n   This program is free software: you can redistribute it and/or modify\n   it under the terms of the GNU General Public License as published by\n   the Free Software Foundation, either version 3 of the License, or\n   (at your option) any later version.\n\n   This program is distributed in the hope that it will be useful,\n   but WITHOUT ANY WARRANTY; without even the implied warranty of\n   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the\n   GNU General Public License for more details.\n\n   You should have received a copy of the GNU General Public License\n   along with this program.  If not, see <http://www.gnu.org/licenses/>.\n'
import logging, random, select, pickle, socket, time, dbm, os, re, traceback
from sys import exit
from optparse import OptionParser
from datetime import datetime
from socket import error as socketerror
from base64 import b64decode, b64encode
from libs.pptable import to_string
from libs.svhelper import __version__, numericbrute, dictionaryattack, mysendto, createTag, check_ipv6, makeRequest, getTag, parseHeader, getRealm, standardoptions, standardscanneroptions, calcloglevel, resumeFrom, getRange, reportBugToAuthor, packetcounter
__prog__ = 'svwar'

class TakeASip:

    def __init__(self, host='localhost', bindingip='', externalip=None, localport=5060, method='REGISTER', guessmode=1, guessargs=None, selecttime=0.005, sessionpath=None, compact=False, socktimeout=3, initialcheck=True, enableack=False, maxlastrecvtime=15, domain=None, printdebug=False, ipv6=False, port=5060):
        self.log = logging.getLogger('TakeASip')
        self.maxlastrecvtime = maxlastrecvtime
        self.sessionpath = sessionpath
        self.dbsyncs = False
        self.enableack = enableack
        if self.sessionpath is not None:
            self.resultauth = dbm.open(os.path.join(self.sessionpath, 'resultauth'), 'c')
            try:
                self.resultauth.sync()
                self.dbsyncs = True
                self.log.info('Db does sync')
            except AttributeError:
                self.log.info('Db does not sync')

        else:
            self.resultauth = dict()
        family = socket.AF_INET
        if ipv6:
            family = socket.AF_INET6
        self.sock = socket.socket(family, socket.SOCK_DGRAM)
        self.sock.settimeout(socktimeout)
        self.bindingip = bindingip
        self.localport = localport
        self.ipv6 = ipv6
        self.originallocalport = localport
        self.rlist = [self.sock]
        self.wlist = list()
        self.xlist = list()
        self.challenges = list()
        self.realm = None
        self.dsthost, self.dstport = host, int(port)
        self.domain = self.dsthost
        if domain:
            self.domain = domain
        self.guessmode = guessmode
        self.guessargs = guessargs
        if self.guessmode == 1:
            self.usernamegen = numericbrute(*self.guessargs)
        else:
            if guessmode == 2:
                self.usernamegen = dictionaryattack(self.guessargs)
            else:
                self.selecttime = selecttime
                self.compact = compact
                self.nomore = False
                self.BADUSER = None
                self.method = method.upper()
                if self.method == 'INVITE':
                    self.log.warn('using an INVITE scan on an endpoint (i.e. SIP phone) may cause it to ring and wake up people in the middle of the night')
                if self.sessionpath is not None:
                    self.packetcount = packetcounter(50)
                self.initialcheck = initialcheck
                self.lastrecvtime = time.time()
                if externalip is None:
                    self.log.debug('external ip was not set')
                    if self.bindingip != '0.0.0.0' and len(self.bindingip) > 0:
                        self.log.debug("but bindingip was set! we'll set it to the binding ip")
                        self.externalip = self.bindingip
                    else:
                        try:
                            self.log.info('trying to get self ip .. might take a while')
                            self.externalip = socket.gethostbyname(socket.gethostname())
                        except socket.error:
                            self.externalip = '127.0.0.1'

                else:
                    self.log.debug('external ip was set')
                self.externalip = externalip
            self.printdebug = printdebug

    PROXYAUTHREQ = 'SIP/2.0 407 '
    AUTHREQ = 'SIP/2.0 401 '
    OKEY = 'SIP/2.0 200 '
    NOTFOUND = 'SIP/2.0 404 '
    INVALIDPASS = 'SIP/2.0 403 '
    TRYING = 'SIP/2.0 100 '
    RINGING = 'SIP/2.0 180 '
    NOTALLOWED = 'SIP/2.0 405 '
    UNAVAILABLE = 'SIP/2.0 480 '
    DECLINED = 'SIP/2.0 603 '
    INEXISTENTTRANSACTION = 'SIP/2.0 481'
    BADREQUEST = 'SIP/2.0 400 '
    SERVICEUN = 'SIP/2.0 503 '

    def createRequest(self, m, username=None, auth=None, cid=None, cseq=1, fromaddr=None, toaddr=None, contact=None):
        if cid is None:
            cid = '%s' % str(random.getrandbits(32))
        else:
            branchunique = '%s' % random.getrandbits(32)
            localtag = createTag(username)
            domain = self.domain
            if self.ipv6:
                if check_ipv6(domain):
                    domain = '[' + self.domain + ']'
            if not contact:
                contact = 'sip:%s@%s' % (username, domain)
            if not fromaddr:
                fromaddr = '"%s"<sip:%s@%s>' % (username, username, domain)
            toaddr = toaddr or '"%s"<sip:%s@%s>' % (username, username, domain)
        request = makeRequest(m,
          fromaddr,
          toaddr,
          domain,
          (self.dstport),
          cid,
          (self.externalip),
          branchunique,
          cseq,
          auth,
          localtag,
          (self.compact),
          contact=contact,
          localport=(self.localport),
          extension=username)
        return request

    def getResponse--- This code section failed: ---

 L. 189         0  LOAD_FAST                'self'
                2  LOAD_ATTR                sock
                4  LOAD_METHOD              recvfrom
                6  LOAD_CONST               8192
                8  CALL_METHOD_1         1  '1 positional argument'
               10  UNPACK_SEQUENCE_2     2 
               12  STORE_FAST               'buff'
               14  STORE_FAST               'srcaddr'

 L. 190        16  LOAD_FAST                'self'
               18  LOAD_ATTR                printdebug
               20  POP_JUMP_IF_FALSE    38  'to 38'

 L. 191        22  LOAD_GLOBAL              print
               24  LOAD_FAST                'srcaddr'
               26  CALL_FUNCTION_1       1  '1 positional argument'
               28  POP_TOP          

 L. 192        30  LOAD_GLOBAL              print
               32  LOAD_FAST                'buff'
               34  CALL_FUNCTION_1       1  '1 positional argument'
               36  POP_TOP          
             38_0  COME_FROM            20  '20'

 L. 193        38  LOAD_FAST                'buff'
               40  LOAD_METHOD              decode
               42  LOAD_STR                 'utf-8'
               44  CALL_METHOD_1         1  '1 positional argument'
               46  STORE_FAST               'buff'

 L. 194        48  SETUP_EXCEPT         68  'to 68'

 L. 195        50  LOAD_GLOBAL              getTag
               52  LOAD_FAST                'buff'
               54  CALL_FUNCTION_1       1  '1 positional argument'
               56  LOAD_METHOD              decode
               58  LOAD_STR                 'utf-8'
               60  CALL_METHOD_1         1  '1 positional argument'
               62  STORE_FAST               'extension'
               64  POP_BLOCK        
               66  JUMP_FORWARD        108  'to 108'
             68_0  COME_FROM_EXCEPT     48  '48'

 L. 196        68  DUP_TOP          
               70  LOAD_GLOBAL              TypeError
               72  LOAD_GLOBAL              AttributeError
               74  BUILD_TUPLE_2         2 
               76  COMPARE_OP               exception-match
               78  POP_JUMP_IF_FALSE   106  'to 106'
               80  POP_TOP          
               82  POP_TOP          
               84  POP_TOP          

 L. 197        86  LOAD_FAST                'self'
               88  LOAD_ATTR                log
               90  LOAD_METHOD              error
               92  LOAD_STR                 'could not decode to tag'
               94  CALL_METHOD_1         1  '1 positional argument'
               96  POP_TOP          

 L. 198        98  LOAD_CONST               None
              100  STORE_FAST               'extension'
              102  POP_EXCEPT       
              104  JUMP_FORWARD        108  'to 108'
            106_0  COME_FROM            78  '78'
              106  END_FINALLY      
            108_0  COME_FROM           104  '104'
            108_1  COME_FROM            66  '66'

 L. 199       108  LOAD_FAST                'extension'
              110  LOAD_CONST               None
              112  COMPARE_OP               is
              114  POP_JUMP_IF_FALSE   126  'to 126'

 L. 200       116  LOAD_CONST               True
              118  LOAD_FAST                'self'
              120  STORE_ATTR               nomore

 L. 201       122  LOAD_CONST               None
              124  RETURN_VALUE     
            126_0  COME_FROM           114  '114'

 L. 202       126  SETUP_EXCEPT        144  'to 144'

 L. 203       128  LOAD_FAST                'buff'
              130  LOAD_METHOD              splitlines
              132  CALL_METHOD_0         0  '0 positional arguments'
              134  LOAD_CONST               0
              136  BINARY_SUBSCR    
              138  STORE_FAST               'firstline'
              140  POP_BLOCK        
              142  JUMP_FORWARD        182  'to 182'
            144_0  COME_FROM_EXCEPT    126  '126'

 L. 204       144  DUP_TOP          
              146  LOAD_GLOBAL              ValueError
              148  LOAD_GLOBAL              IndexError
              150  LOAD_GLOBAL              AttributeError
              152  BUILD_TUPLE_3         3 
              154  COMPARE_OP               exception-match
              156  POP_JUMP_IF_FALSE   180  'to 180'
              158  POP_TOP          
              160  POP_TOP          
              162  POP_TOP          

 L. 205       164  LOAD_FAST                'self'
              166  LOAD_ATTR                log
              168  LOAD_METHOD              error
              170  LOAD_STR                 'could not get the 1st line'
              172  CALL_METHOD_1         1  '1 positional argument'
              174  POP_TOP          

 L. 206       176  LOAD_CONST               None
              178  RETURN_VALUE     
            180_0  COME_FROM           156  '156'
              180  END_FINALLY      
            182_0  COME_FROM           142  '142'

 L. 207       182  LOAD_FAST                'self'
              184  LOAD_ATTR                enableack
          186_188  POP_JUMP_IF_FALSE   658  'to 658'

 L. 209       190  LOAD_GLOBAL              parseHeader
              192  LOAD_FAST                'buff'
              194  CALL_FUNCTION_1       1  '1 positional argument'
              196  STORE_FAST               '_tmp'

 L. 210       198  LOAD_FAST                '_tmp'
              200  POP_JUMP_IF_FALSE   210  'to 210'
              202  LOAD_STR                 'code'
              204  LOAD_FAST                '_tmp'
              206  COMPARE_OP               in
              208  POP_JUMP_IF_TRUE    214  'to 214'
            210_0  COME_FROM           200  '200'

 L. 211       210  LOAD_CONST               None
              212  RETURN_VALUE     
            214_0  COME_FROM           208  '208'

 L. 212       214  LOAD_CONST               699
              216  LOAD_FAST                '_tmp'
              218  LOAD_STR                 'code'
              220  BINARY_SUBSCR    
              222  DUP_TOP          
              224  ROT_THREE        
              226  COMPARE_OP               >
              228  POP_JUMP_IF_FALSE   240  'to 240'
              230  LOAD_CONST               200
              232  COMPARE_OP               >=
          234_236  POP_JUMP_IF_FALSE   658  'to 658'
              238  JUMP_FORWARD        246  'to 246'
            240_0  COME_FROM           228  '228'
              240  POP_TOP          
          242_244  JUMP_FORWARD        658  'to 658'
            246_0  COME_FROM           238  '238'

 L. 213       246  LOAD_FAST                'self'
              248  LOAD_ATTR                log
              250  LOAD_METHOD              debug
              252  LOAD_STR                 'will try to send an ACK response'
              254  CALL_METHOD_1         1  '1 positional argument'
              256  POP_TOP          

 L. 214       258  LOAD_STR                 'headers'
              260  LOAD_FAST                '_tmp'
              262  COMPARE_OP               not-in
          264_266  POP_JUMP_IF_FALSE   284  'to 284'

 L. 215       268  LOAD_FAST                'self'
              270  LOAD_ATTR                log
              272  LOAD_METHOD              debug
              274  LOAD_STR                 'no headers?'
              276  CALL_METHOD_1         1  '1 positional argument'
              278  POP_TOP          

 L. 216       280  LOAD_CONST               None
              282  RETURN_VALUE     
            284_0  COME_FROM           264  '264'

 L. 217       284  LOAD_STR                 'from'
              286  LOAD_FAST                '_tmp'
              288  LOAD_STR                 'headers'
              290  BINARY_SUBSCR    
              292  COMPARE_OP               not-in
          294_296  POP_JUMP_IF_FALSE   314  'to 314'

 L. 218       298  LOAD_FAST                'self'
              300  LOAD_ATTR                log
              302  LOAD_METHOD              debug
              304  LOAD_STR                 'no from?'
              306  CALL_METHOD_1         1  '1 positional argument'
              308  POP_TOP          

 L. 219       310  LOAD_CONST               None
              312  RETURN_VALUE     
            314_0  COME_FROM           294  '294'

 L. 220       314  LOAD_STR                 'cseq'
              316  LOAD_FAST                '_tmp'
              318  LOAD_STR                 'headers'
              320  BINARY_SUBSCR    
              322  COMPARE_OP               not-in
          324_326  POP_JUMP_IF_FALSE   344  'to 344'

 L. 221       328  LOAD_FAST                'self'
              330  LOAD_ATTR                log
              332  LOAD_METHOD              debug
              334  LOAD_STR                 'no cseq'
              336  CALL_METHOD_1         1  '1 positional argument'
              338  POP_TOP          

 L. 222       340  LOAD_CONST               None
              342  RETURN_VALUE     
            344_0  COME_FROM           324  '324'

 L. 223       344  LOAD_STR                 'call-id'
              346  LOAD_FAST                '_tmp'
              348  LOAD_STR                 'headers'
              350  BINARY_SUBSCR    
              352  COMPARE_OP               not-in
          354_356  POP_JUMP_IF_FALSE   374  'to 374'

 L. 224       358  LOAD_FAST                'self'
              360  LOAD_ATTR                log
              362  LOAD_METHOD              debug
              364  LOAD_STR                 'no caller id'
              366  CALL_METHOD_1         1  '1 positional argument'
              368  POP_TOP          

 L. 225       370  LOAD_CONST               None
              372  RETURN_VALUE     
            374_0  COME_FROM           354  '354'

 L. 226       374  SETUP_EXCEPT        388  'to 388'

 L. 228       376  LOAD_GLOBAL              getTag
              378  LOAD_FAST                'buff'
              380  CALL_FUNCTION_1       1  '1 positional argument'
              382  STORE_FAST               'username'
              384  POP_BLOCK        
              386  JUMP_FORWARD        438  'to 438'
            388_0  COME_FROM_EXCEPT    374  '374'

 L. 229       388  DUP_TOP          
              390  LOAD_GLOBAL              IndexError
              392  COMPARE_OP               exception-match
          394_396  POP_JUMP_IF_FALSE   436  'to 436'
              398  POP_TOP          
              400  POP_TOP          
              402  POP_TOP          

 L. 230       404  LOAD_FAST                'self'
              406  LOAD_ATTR                log
              408  LOAD_METHOD              warn
              410  LOAD_STR                 'could not parse the from address %s'
              412  LOAD_FAST                '_tmp'

 L. 231       414  LOAD_STR                 'headers'
              416  BINARY_SUBSCR    
              418  LOAD_STR                 'from'
              420  BINARY_SUBSCR    
              422  BINARY_MODULO    
              424  CALL_METHOD_1         1  '1 positional argument'
              426  POP_TOP          

 L. 232       428  LOAD_STR                 'XXX'
              430  STORE_FAST               'username'
              432  POP_EXCEPT       
              434  JUMP_FORWARD        438  'to 438'
            436_0  COME_FROM           394  '394'
              436  END_FINALLY      
            438_0  COME_FROM           434  '434'
            438_1  COME_FROM           386  '386'

 L. 233       438  LOAD_FAST                '_tmp'
              440  LOAD_STR                 'headers'
              442  BINARY_SUBSCR    
              444  LOAD_STR                 'cseq'
              446  BINARY_SUBSCR    
              448  LOAD_CONST               0
              450  BINARY_SUBSCR    
              452  STORE_FAST               'cseq'

 L. 234       454  LOAD_FAST                'cseq'
              456  LOAD_METHOD              split
              458  CALL_METHOD_0         0  '0 positional arguments'
              460  LOAD_CONST               1
              462  BINARY_SUBSCR    
              464  STORE_FAST               'cseqmethod'

 L. 235       466  LOAD_STR                 'INVITE'
              468  LOAD_FAST                'cseqmethod'
              470  COMPARE_OP               ==
          472_474  POP_JUMP_IF_FALSE   658  'to 658'

 L. 236       476  LOAD_FAST                '_tmp'
              478  LOAD_STR                 'headers'
              480  BINARY_SUBSCR    
              482  LOAD_STR                 'call-id'
              484  BINARY_SUBSCR    
              486  LOAD_CONST               0
              488  BINARY_SUBSCR    
              490  STORE_FAST               'cid'

 L. 237       492  LOAD_FAST                '_tmp'
              494  LOAD_STR                 'headers'
              496  BINARY_SUBSCR    
              498  LOAD_STR                 'from'
              500  BINARY_SUBSCR    
              502  LOAD_CONST               0
              504  BINARY_SUBSCR    
              506  STORE_FAST               'fromaddr'

 L. 238       508  LOAD_FAST                '_tmp'
              510  LOAD_STR                 'headers'
              512  BINARY_SUBSCR    
              514  LOAD_STR                 'to'
              516  BINARY_SUBSCR    
              518  LOAD_CONST               0
              520  BINARY_SUBSCR    
              522  STORE_FAST               'toaddr'

 L. 239       524  LOAD_FAST                'self'
              526  LOAD_ATTR                createRequest
              528  LOAD_STR                 'ACK'

 L. 240       530  LOAD_FAST                'cid'

 L. 241       532  LOAD_FAST                'cseq'
              534  LOAD_METHOD              replace

 L. 242       536  LOAD_FAST                'cseqmethod'
              538  LOAD_STR                 ''
              540  CALL_METHOD_2         2  '2 positional arguments'

 L. 243       542  LOAD_FAST                'fromaddr'

 L. 244       544  LOAD_FAST                'toaddr'
              546  LOAD_CONST               ('cid', 'cseq', 'fromaddr', 'toaddr')
              548  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
              550  STORE_FAST               'ackreq'

 L. 246       552  LOAD_FAST                'self'
              554  LOAD_ATTR                log
              556  LOAD_METHOD              debug
              558  LOAD_STR                 'here is your ack request: %s'
              560  LOAD_FAST                'ackreq'
              562  BINARY_MODULO    
              564  CALL_METHOD_1         1  '1 positional argument'
              566  POP_TOP          

 L. 247       568  LOAD_GLOBAL              mysendto
              570  LOAD_FAST                'self'
              572  LOAD_ATTR                sock
              574  LOAD_FAST                'ackreq'
              576  LOAD_FAST                'self'
              578  LOAD_ATTR                dsthost
              580  LOAD_FAST                'self'
              582  LOAD_ATTR                dstport
              584  BUILD_TUPLE_2         2 
              586  CALL_FUNCTION_3       3  '3 positional arguments'
              588  POP_TOP          

 L. 249       590  LOAD_FAST                '_tmp'
              592  LOAD_STR                 'code'
              594  BINARY_SUBSCR    
              596  LOAD_CONST               200
              598  COMPARE_OP               ==
          600_602  POP_JUMP_IF_FALSE   658  'to 658'

 L. 250       604  LOAD_FAST                'self'
              606  LOAD_ATTR                createRequest
              608  LOAD_STR                 'BYE'

 L. 251       610  LOAD_FAST                'cid'

 L. 252       612  LOAD_STR                 '2'

 L. 253       614  LOAD_FAST                'fromaddr'

 L. 254       616  LOAD_FAST                'toaddr'
              618  LOAD_CONST               ('cid', 'cseq', 'fromaddr', 'toaddr')
              620  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
              622  STORE_FAST               'byemsg'

 L. 256       624  LOAD_FAST                'self'
              626  LOAD_ATTR                log
              628  LOAD_METHOD              debug

 L. 257       630  LOAD_STR                 'sending a BYE to the 200 OK for the INVITE'
              632  CALL_METHOD_1         1  '1 positional argument'
              634  POP_TOP          

 L. 258       636  LOAD_GLOBAL              mysendto
              638  LOAD_FAST                'self'
              640  LOAD_ATTR                sock
              642  LOAD_FAST                'byemsg'

 L. 259       644  LOAD_FAST                'self'
              646  LOAD_ATTR                dsthost
              648  LOAD_FAST                'self'
              650  LOAD_ATTR                dstport
              652  BUILD_TUPLE_2         2 
              654  CALL_FUNCTION_3       3  '3 positional arguments'
              656  POP_TOP          
            658_0  COME_FROM           600  '600'
            658_1  COME_FROM           472  '472'
            658_2  COME_FROM           242  '242'
            658_3  COME_FROM           234  '234'
            658_4  COME_FROM           186  '186'

 L. 261       658  LOAD_FAST                'firstline'
              660  LOAD_FAST                'self'
              662  LOAD_ATTR                BADUSER
              664  COMPARE_OP               !=
          666_668  POP_JUMP_IF_FALSE   972  'to 972'

 L. 262       670  LOAD_FAST                'buff'
              672  LOAD_METHOD              startswith
              674  LOAD_FAST                'self'
              676  LOAD_ATTR                PROXYAUTHREQ
              678  CALL_METHOD_1         1  '1 positional argument'
          680_682  POP_JUMP_IF_TRUE    712  'to 712'

 L. 263       684  LOAD_FAST                'buff'
              686  LOAD_METHOD              startswith
              688  LOAD_FAST                'self'
              690  LOAD_ATTR                INVALIDPASS
              692  CALL_METHOD_1         1  '1 positional argument'
          694_696  POP_JUMP_IF_TRUE    712  'to 712'

 L. 264       698  LOAD_FAST                'buff'
              700  LOAD_METHOD              startswith
              702  LOAD_FAST                'self'
              704  LOAD_ATTR                AUTHREQ
              706  CALL_METHOD_1         1  '1 positional argument'
          708_710  POP_JUMP_IF_FALSE   792  'to 792'
            712_0  COME_FROM           694  '694'
            712_1  COME_FROM           680  '680'

 L. 265       712  LOAD_FAST                'self'
              714  LOAD_ATTR                realm
              716  LOAD_CONST               None
              718  COMPARE_OP               is
          720_722  POP_JUMP_IF_FALSE   734  'to 734'

 L. 266       724  LOAD_GLOBAL              getRealm
              726  LOAD_FAST                'buff'
              728  CALL_FUNCTION_1       1  '1 positional argument'
              730  LOAD_FAST                'self'
              732  STORE_ATTR               realm
            734_0  COME_FROM           720  '720'

 L. 267       734  LOAD_FAST                'self'
              736  LOAD_ATTR                log
              738  LOAD_METHOD              info

 L. 268       740  LOAD_STR                 "extension '%s' exists - requires authentication"
              742  LOAD_FAST                'extension'
              744  BINARY_MODULO    
              746  CALL_METHOD_1         1  '1 positional argument'
              748  POP_TOP          

 L. 269       750  LOAD_STR                 'reqauth'
              752  LOAD_FAST                'self'
              754  LOAD_ATTR                resultauth
              756  LOAD_FAST                'extension'
              758  STORE_SUBSCR     

 L. 270       760  LOAD_FAST                'self'
              762  LOAD_ATTR                sessionpath
              764  LOAD_CONST               None
              766  COMPARE_OP               is-not
          768_770  POP_JUMP_IF_FALSE   968  'to 968'
              772  LOAD_FAST                'self'
              774  LOAD_ATTR                dbsyncs
          776_778  POP_JUMP_IF_FALSE   968  'to 968'

 L. 271       780  LOAD_FAST                'self'
              782  LOAD_ATTR                resultauth
              784  LOAD_METHOD              sync
              786  CALL_METHOD_0         0  '0 positional arguments'
              788  POP_TOP          
              790  JUMP_FORWARD       1252  'to 1252'
            792_0  COME_FROM           708  '708'

 L. 272       792  LOAD_FAST                'buff'
              794  LOAD_METHOD              startswith
              796  LOAD_FAST                'self'
              798  LOAD_ATTR                TRYING
              800  CALL_METHOD_1         1  '1 positional argument'
          802_804  POP_JUMP_IF_FALSE   808  'to 808'

 L. 273       806  JUMP_FORWARD       1252  'to 1252'
            808_0  COME_FROM           802  '802'

 L. 274       808  LOAD_FAST                'buff'
              810  LOAD_METHOD              startswith
              812  LOAD_FAST                'self'
              814  LOAD_ATTR                RINGING
              816  CALL_METHOD_1         1  '1 positional argument'
          818_820  POP_JUMP_IF_FALSE   824  'to 824'

 L. 275       822  JUMP_FORWARD       1252  'to 1252'
            824_0  COME_FROM           818  '818'

 L. 276       824  LOAD_FAST                'buff'
              826  LOAD_METHOD              startswith
              828  LOAD_FAST                'self'
              830  LOAD_ATTR                OKEY
              832  CALL_METHOD_1         1  '1 positional argument'
          834_836  POP_JUMP_IF_FALSE   896  'to 896'

 L. 277       838  LOAD_FAST                'self'
              840  LOAD_ATTR                log
              842  LOAD_METHOD              info

 L. 278       844  LOAD_STR                 "extension '%s' exists - authentication not required"
              846  LOAD_FAST                'extension'
              848  BINARY_MODULO    
              850  CALL_METHOD_1         1  '1 positional argument'
              852  POP_TOP          

 L. 279       854  LOAD_STR                 'noauth'
              856  LOAD_FAST                'self'
              858  LOAD_ATTR                resultauth
              860  LOAD_FAST                'extension'
              862  STORE_SUBSCR     

 L. 280       864  LOAD_FAST                'self'
              866  LOAD_ATTR                sessionpath
              868  LOAD_CONST               None
              870  COMPARE_OP               is-not
          872_874  POP_JUMP_IF_FALSE   968  'to 968'
              876  LOAD_FAST                'self'
              878  LOAD_ATTR                dbsyncs
          880_882  POP_JUMP_IF_FALSE   968  'to 968'

 L. 281       884  LOAD_FAST                'self'
              886  LOAD_ATTR                resultauth
              888  LOAD_METHOD              sync
              890  CALL_METHOD_0         0  '0 positional arguments'
              892  POP_TOP          
              894  JUMP_FORWARD       1252  'to 1252'
            896_0  COME_FROM           834  '834'

 L. 283       896  LOAD_FAST                'self'
              898  LOAD_ATTR                log
              900  LOAD_METHOD              warn

 L. 284       902  LOAD_STR                 "extension '%s' probably exists but the response is unexpected"
              904  LOAD_FAST                'extension'
              906  BINARY_MODULO    
              908  CALL_METHOD_1         1  '1 positional argument'
              910  POP_TOP          

 L. 285       912  LOAD_FAST                'self'
              914  LOAD_ATTR                log
              916  LOAD_METHOD              debug
              918  LOAD_STR                 'response: %s'
              920  LOAD_FAST                'firstline'
              922  BINARY_MODULO    
              924  CALL_METHOD_1         1  '1 positional argument'
              926  POP_TOP          

 L. 286       928  LOAD_STR                 'weird'
              930  LOAD_FAST                'self'
              932  LOAD_ATTR                resultauth
              934  LOAD_FAST                'extension'
              936  STORE_SUBSCR     

 L. 287       938  LOAD_FAST                'self'
              940  LOAD_ATTR                sessionpath
              942  LOAD_CONST               None
              944  COMPARE_OP               is-not
          946_948  POP_JUMP_IF_FALSE  1252  'to 1252'
              950  LOAD_FAST                'self'
              952  LOAD_ATTR                dbsyncs
          954_956  POP_JUMP_IF_FALSE  1252  'to 1252'

 L. 288       958  LOAD_FAST                'self'
              960  LOAD_ATTR                resultauth
              962  LOAD_METHOD              sync
              964  CALL_METHOD_0         0  '0 positional arguments'
              966  POP_TOP          
            968_0  COME_FROM           880  '880'
            968_1  COME_FROM           872  '872'
            968_2  COME_FROM           776  '776'
            968_3  COME_FROM           768  '768'
          968_970  JUMP_FORWARD       1252  'to 1252'
            972_0  COME_FROM           666  '666'

 L. 289       972  LOAD_FAST                'buff'
              974  LOAD_METHOD              startswith
              976  LOAD_FAST                'self'
              978  LOAD_ATTR                NOTFOUND
              980  CALL_METHOD_1         1  '1 positional argument'
          982_984  POP_JUMP_IF_FALSE  1004  'to 1004'

 L. 290       986  LOAD_FAST                'self'
              988  LOAD_ATTR                log
              990  LOAD_METHOD              debug
              992  LOAD_STR                 "User '%s' not found"
              994  LOAD_FAST                'extension'
              996  BINARY_MODULO    
              998  CALL_METHOD_1         1  '1 positional argument'
             1000  POP_TOP          
             1002  JUMP_FORWARD       1252  'to 1252'
           1004_0  COME_FROM           982  '982'

 L. 291      1004  LOAD_FAST                'buff'
             1006  LOAD_METHOD              startswith
             1008  LOAD_FAST                'self'
             1010  LOAD_ATTR                INEXISTENTTRANSACTION
             1012  CALL_METHOD_1         1  '1 positional argument'
         1014_1016  POP_JUMP_IF_FALSE  1020  'to 1020'

 L. 292      1018  JUMP_FORWARD       1252  'to 1252'
           1020_0  COME_FROM          1014  '1014'

 L. 296      1020  LOAD_FAST                'buff'
             1022  LOAD_METHOD              startswith
             1024  LOAD_FAST                'self'
             1026  LOAD_ATTR                SERVICEUN
             1028  CALL_METHOD_1         1  '1 positional argument'
         1030_1032  POP_JUMP_IF_FALSE  1036  'to 1036'

 L. 297      1034  JUMP_FORWARD       1252  'to 1252'
           1036_0  COME_FROM          1030  '1030'

 L. 298      1036  LOAD_FAST                'buff'
             1038  LOAD_METHOD              startswith
             1040  LOAD_FAST                'self'
             1042  LOAD_ATTR                TRYING
             1044  CALL_METHOD_1         1  '1 positional argument'
         1046_1048  POP_JUMP_IF_FALSE  1052  'to 1052'

 L. 299      1050  JUMP_FORWARD       1252  'to 1252'
           1052_0  COME_FROM          1046  '1046'

 L. 300      1052  LOAD_FAST                'buff'
             1054  LOAD_METHOD              startswith
             1056  LOAD_FAST                'self'
             1058  LOAD_ATTR                RINGING
             1060  CALL_METHOD_1         1  '1 positional argument'
         1062_1064  POP_JUMP_IF_FALSE  1068  'to 1068'

 L. 301      1066  JUMP_FORWARD       1252  'to 1252'
           1068_0  COME_FROM          1062  '1062'

 L. 302      1068  LOAD_FAST                'buff'
             1070  LOAD_METHOD              startswith
           1072_0  COME_FROM           790  '790'
             1072  LOAD_FAST                'self'
             1074  LOAD_ATTR                OKEY
             1076  CALL_METHOD_1         1  '1 positional argument'
         1078_1080  POP_JUMP_IF_FALSE  1084  'to 1084'

 L. 303      1082  JUMP_FORWARD       1252  'to 1252'
           1084_0  COME_FROM          1078  '1078'

 L. 304      1084  LOAD_FAST                'buff'
             1086  LOAD_METHOD              startswith
           1088_0  COME_FROM           806  '806'
             1088  LOAD_FAST                'self'
             1090  LOAD_ATTR                DECLINED
             1092  CALL_METHOD_1         1  '1 positional argument'
         1094_1096  POP_JUMP_IF_FALSE  1100  'to 1100'

 L. 305      1098  JUMP_FORWARD       1252  'to 1252'
           1100_0  COME_FROM          1094  '1094'

 L. 306      1100  LOAD_FAST                'buff'
             1102  LOAD_METHOD              startswith
           1104_0  COME_FROM           822  '822'
             1104  LOAD_FAST                'self'
             1106  LOAD_ATTR                NOTALLOWED
             1108  CALL_METHOD_1         1  '1 positional argument'
         1110_1112  POP_JUMP_IF_FALSE  1136  'to 1136'

 L. 307      1114  LOAD_FAST                'self'
             1116  LOAD_ATTR                log
             1118  LOAD_METHOD              warn
             1120  LOAD_STR                 'method not allowed'
             1122  CALL_METHOD_1         1  '1 positional argument'
             1124  POP_TOP          

 L. 308      1126  LOAD_CONST               True
             1128  LOAD_FAST                'self'
             1130  STORE_ATTR               nomore

 L. 309      1132  LOAD_CONST               None
             1134  RETURN_VALUE     
           1136_0  COME_FROM          1110  '1110'

 L. 310      1136  LOAD_FAST                'buff'
             1138  LOAD_METHOD              startswith
             1140  LOAD_FAST                'self'
             1142  LOAD_ATTR                BADREQUEST
             1144  CALL_METHOD_1         1  '1 positional argument'
         1146_1148  POP_JUMP_IF_FALSE  1172  'to 1172'

 L. 311      1150  LOAD_FAST                'self'
             1152  LOAD_ATTR                log
             1154  LOAD_METHOD              error

 L. 312      1156  LOAD_STR                 'Protocol / interopability error! The remote side most probably has problems with parsing your SIP messages!'
             1158  CALL_METHOD_1         1  '1 positional argument'
             1160  POP_TOP          

 L. 313      1162  LOAD_CONST               True
             1164  LOAD_FAST                'self'
             1166  STORE_ATTR               nomore

 L. 314      1168  LOAD_CONST               None
             1170  RETURN_VALUE     
           1172_0  COME_FROM          1146  '1146'

 L. 316      1172  LOAD_FAST                'self'
             1174  LOAD_ATTR                log
           1176_0  COME_FROM           894  '894'
             1176  LOAD_METHOD              warn
             1178  LOAD_STR                 'We got an unknown response'
             1180  CALL_METHOD_1         1  '1 positional argument'
             1182  POP_TOP          

 L. 317      1184  LOAD_FAST                'self'
             1186  LOAD_ATTR                log
             1188  LOAD_METHOD              error
             1190  LOAD_STR                 'Response: %s'
             1192  LOAD_FAST                'buff'
             1194  LOAD_METHOD              __repr__
             1196  CALL_METHOD_0         0  '0 positional arguments'
             1198  BINARY_MODULO    
             1200  CALL_METHOD_1         1  '1 positional argument'
             1202  POP_TOP          

 L. 318      1204  LOAD_FAST                'self'
             1206  LOAD_ATTR                log
             1208  LOAD_METHOD              debug
             1210  LOAD_STR                 '1st line: %s'
             1212  LOAD_FAST                'firstline'
             1214  LOAD_METHOD              __repr__
             1216  CALL_METHOD_0         0  '0 positional arguments'
             1218  BINARY_MODULO    
             1220  CALL_METHOD_1         1  '1 positional argument'
             1222  POP_TOP          

 L. 319      1224  LOAD_FAST                'self'
             1226  LOAD_ATTR                log
             1228  LOAD_METHOD              debug
             1230  LOAD_STR                 'Bad user: %s'
             1232  LOAD_FAST                'self'
             1234  LOAD_ATTR                BADUSER
             1236  LOAD_METHOD              __repr__
             1238  CALL_METHOD_0         0  '0 positional arguments'
             1240  BINARY_MODULO    
             1242  CALL_METHOD_1         1  '1 positional argument'
             1244  POP_TOP          

 L. 320      1246  LOAD_CONST               True
             1248  LOAD_FAST                'self'
             1250  STORE_ATTR               nomore
           1252_0  COME_FROM          1098  '1098'
           1252_1  COME_FROM          1082  '1082'
           1252_2  COME_FROM          1066  '1066'
           1252_3  COME_FROM          1050  '1050'
           1252_4  COME_FROM          1034  '1034'
           1252_5  COME_FROM          1018  '1018'
           1252_6  COME_FROM          1002  '1002'
           1252_7  COME_FROM           968  '968'
           1252_8  COME_FROM           954  '954'
           1252_9  COME_FROM           946  '946'

Parse error at or near `COME_FROM' instruction at offset 1072_0

    def start(self):
        if self.bindingip == '':
            bindingip = 'any'
        else:
            bindingip = self.bindingip
        self.log.debug('binding to %s:%s' % (bindingip, self.localport))
        while self.localport > 65535:
            self.log.critical('Could not bind to any port')
            return
            try:
                self.sock.bind((self.bindingip, self.localport))
                break
            except socket.error:
                self.log.debug('could not bind to %s' % self.localport)
                self.localport += 1

        if self.originallocalport != self.localport:
            self.log.warn('could not bind to %s:%s - some process might already be listening on this port. Listening on port %s instead' % (
             self.bindingip, self.originallocalport, self.localport))
            self.log.info('Make use of the -P option to specify a port to bind to yourself')
        self.nextuser = random.getrandbits(32)
        data = self.createRequest(self.method, self.nextuser)
        try:
            mysendtoself.sockdata(self.dsthost, self.dstport)
        except socket.error as err:
            try:
                self.log.error('socket error: %s' % err)
                return
            finally:
                err = None
                del err

        gotbadresponse = False
        try:
            while 1:
                try:
                    buff, srcaddr = self.sock.recvfrom(8192)
                    if self.printdebug:
                        print(srcaddr)
                        print(buff)
                except socket.error as err:
                    try:
                        self.log.error('socket error: %s' % err)
                        return
                    finally:
                        err = None
                        del err

                buff = buff.decode('utf-8')
                if buff.startswith(self.TRYING) or buff.startswith(self.RINGING) or buff.startswith(self.UNAVAILABLE):
                    gotbadresponse = True
                elif not buff.startswith(self.PROXYAUTHREQ):
                    if buff.startswith(self.INVALIDPASS) or buff.startswith(self.AUTHREQ):
                        if self.initialcheck:
                            self.log.error('SIP server replied with an authentication request for an unknown extension. Set --force to force a scan.')
                            return
                    self.BADUSER = buff.splitlines()[0]
                    self.log.debug('Bad user = %s' % self.BADUSER)
                    gotbadresponse = False
                    break

        except socket.timeout:
            if gotbadresponse:
                self.log.error('The response we got was not good: %s' % buff.__repr__())
            else:
                self.log.error('No server response - are you sure that this PBX is listening? run svmap against it to find out')
            return
        except (AttributeError, ValueError, IndexError):
            self.log.error('bad response .. bailing out')
            return
        except socket.error as err:
            try:
                self.log.error('socket error: %s' % err)
                return
            finally:
                err = None
                del err

        if self.BADUSER.startswith(self.AUTHREQ):
            self.log.warn('Bad user = %s - svwar will probably not work!' % self.AUTHREQ)
        self.log.info('Ok SIP device found')
        while self.nomore:
            while True:
                try:
                    self.getResponse()
                except socket.timeout:
                    return

            r, _, _ = select.select(self.rlist, self.wlist, self.xlist, self.selecttime)
            if r:
                self.getResponse()
                self.lastrecvtime = time.time()
            else:
                timediff = time.time() - self.lastrecvtime
                if timediff > self.maxlastrecvtime:
                    self.nomore = True
                    self.log.warn('It has been %s seconds since we last received a response - stopping' % timediff)
                    continue
                try:
                    self.nextuser = next(self.usernamegen)
                except StopIteration:
                    self.nomore = True
                    continue
                except TypeError:
                    self.nomore = True
                    self.log.exception('Bad format string')

                data = self.createRequest(self.method, self.nextuser)
                try:
                    self.log.debug('sending request for %s' % self.nextuser)
                    mysendtoself.sockdata(self.dsthost, self.dstport)
                    if self.sessionpath is not None:
                        if next(self.packetcount):
                            try:
                                if self.guessmode == 1:
                                    pickle.dump(self.nextuser, open(os.path.join(exportpath, 'lastextension.pkl'), 'wb+'))
                                    self.log.debug('logged last extension %s' % self.nextuser)
                                else:
                                    if self.guessmode == 2:
                                        pickle.dump(self.guessargs.tell(), open(os.path.join(exportpath, 'lastextension.pkl'), 'wb+'))
                                        self.log.debug('logged last position %s' % self.guessargs.tell())
                            except IOError:
                                self.log.warn('could not log the last extension scanned')

                except socket.error as err:
                    try:
                        self.log.error('socket error: %s' % err)
                        break
                    finally:
                        err = None
                        del err


def main():
    global exportpath
    usage = 'usage: %prog [options] target\r\n'
    usage += 'examples:\r\n'
    usage += '%prog -e100-999 10.0.0.1\r\n'
    usage += '%prog -d dictionary.txt 10.0.0.2\r\n'
    parser = OptionParser(usage, version=('%prog v' + str(__version__) + __GPL__))
    parser = standardoptions(parser)
    parser = standardscanneroptions(parser)
    parser.add_option('-d', '--dictionary', dest='dictionary', type='string', help='specify a dictionary file with possible extension names',
      metavar='DICTIONARY')
    parser.add_option('-m', '--method', dest='method', type='string', help='specify a request method. The default is REGISTER. Other possible methods are OPTIONS and INVITE',
      default='REGISTER',
      metavar='OPTIONS')
    parser.add_option('-e', '--extensions', dest='range', default='100-999', help='specify an extension or extension range\r\nexample: -e 100-999,1000-1500,9999',
      metavar='RANGE')
    parser.add_option('-z', '--zeropadding', dest='zeropadding', type='int', help='the number of zeros used to padd the username.\n                  the options "-e 1-9999 -z 4" would give 0001 0002 0003 ... 9999',
      default=0,
      metavar='PADDING')
    parser.add_option('--force', dest='force', action='store_true', default=False,
      help='Force scan, ignoring initial sanity checks.')
    parser.add_option('--template', '-T', action='store', dest='template', help='A format string which allows us to specify a template for the extensions\n                      example svwar.py -e 1-999 --template="123%#04i999" would scan between 1230001999 to 1230999999"\n                      ')
    parser.add_option('--enabledefaults', '-D', action='store_true', dest='defaults', default=False,
      help='Scan for default / typical extensions such as\n                      1000,2000,3000 ... 1100, etc. This option is off by default.\n                      Use --enabledefaults to enable this functionality')
    parser.add_option('--maximumtime', action='store', dest='maximumtime', type='int', default=10,
      help='Maximum time in seconds to keep sending requests without\n                      receiving a response back')
    parser.add_option('--domain', dest='domain', help='force a specific domain name for the SIP message, eg. -d example.org')
    parser.add_option('--debug', dest='printdebug', help='Print SIP messages received',
      default=False,
      action='store_true')
    parser.add_option('-6', dest='ipv6', action='store_true', help='scan an IPv6 address')
    options, args = parser.parse_args()
    exportpath = None
    logging.basicConfig(level=(calcloglevel(options)))
    logging.debug('started logging')
    if options.force:
        initialcheck = False
    else:
        initialcheck = True
    if options.template is not None:
        try:
            options.template % 1
        except TypeError:
            logging.critical('The format string template is not correct. Please provide an appropiate one')
            exit(1)

    if options.resume is not None:
        exportpath = os.path.join(os.path.expanduser('~'), '.sipvicious', __prog__, options.resume)
        if os.path.exists(os.path.join(exportpath, 'closed')):
            logging.error('Cannot resume a session that is complete')
            exit(1)
        if not os.path.exists(exportpath):
            logging.critical('A session with the name %s was not found' % options.resume)
            exit(1)
        optionssrc = os.path.join(exportpath, 'options.pkl')
        previousresume = options.resume
        previousverbose = options.verbose
        options, args = pickle.load((open(optionssrc, 'rb')), encoding='bytes')
        options.resume = previousresume
        options.verbose = previousverbose
    else:
        if options.save is not None:
            exportpath = os.path.join(os.path.expanduser('~'), '.sipvicious', __prog__, options.save)
        else:
            if len(args) != 1:
                parser.error('provide one hostname')
            else:
                host = args[0]
            if options.dictionary is not None:
                guessmode = 2
                try:
                    dictionary = open(options.dictionary, 'r')
                except IOError:
                    logging.error('could not open %s' % options.dictionary)
                    exit(1)

                if options.resume is not None:
                    lastextensionsrc = os.path.join(exportpath, 'lastextension.pkl')
                    previousposition = pickle.load((open(lastextensionsrc, 'rb')), encoding='bytes')
                    dictionary.seek(previousposition)
                guessargs = dictionary
            else:
                guessmode = 1
                if options.resume is not None:
                    lastextensionsrc = os.path.join(exportpath, 'lastextension.pkl')
                    try:
                        previousextension = pickle.load((open(lastextensionsrc, 'rb')), encoding='bytes')
                    except IOError:
                        logging.critical('Could not read from %s' % lastextensionsrc)
                        exit(1)

                    logging.debug('Previous range: %s' % options.range)
                    options.range = resumeFrom(previousextension, options.range)
                    logging.debug('New range: %s' % options.range)
                    logging.info('Resuming from %s' % previousextension)
                extensionstotry = getRange(options.range)
                guessargs = (extensionstotry, options.zeropadding,
                 options.template, options.defaults)
            if options.save is not None:
                if options.resume is None:
                    exportpath = os.path.join(os.path.expanduser('~'), '.sipvicious', __prog__, options.save)
                    if os.path.exists(exportpath):
                        logging.warn('we found a previous scan with the same name. Please choose a new session name')
                        exit(1)
                    logging.debug('creating an export location %s' % exportpath)
                    try:
                        os.makedirs(exportpath, mode=448)
                    except OSError:
                        logging.critical('could not create the export location %s' % exportpath)
                        exit(1)

                    optionsdst = os.path.join(exportpath, 'options.pkl')
                    logging.debug('saving options to %s' % optionsdst)
                    pickle.dump([options, args], open(optionsdst, 'wb+'))
            if options.autogetip:
                tmpsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                tmpsocket.connect(('msn.com', 80))
                options.externalip = tmpsocket.getsockname()[0]
                tmpsocket.close()
            enableack = False
            if options.method.upper() == 'INVITE':
                enableack = True
            sipvicious = TakeASip(host,
              port=(options.port),
              selecttime=(options.selecttime),
              method=(options.method),
              compact=(options.enablecompact),
              guessmode=guessmode,
              guessargs=guessargs,
              sessionpath=exportpath,
              initialcheck=initialcheck,
              externalip=(options.externalip),
              enableack=enableack,
              maxlastrecvtime=(options.maximumtime),
              localport=(options.localport),
              domain=(options.domain),
              printdebug=(options.printdebug),
              ipv6=(options.ipv6))
            start_time = datetime.now()
            logging.info('start your engines')
            try:
                sipvicious.start()
                if exportpath is not None:
                    open(os.path.join(exportpath, 'closed'), 'w').close()
            except KeyboardInterrupt:
                logging.warn('caught your control^c - quiting')
            except Exception as err:
                try:
                    if options.reportBack:
                        logging.critical('Got unhandled exception : %s\nSending report to author' % err.__str__())
                        reportBugToAuthor(traceback.format_exc())
                    else:
                        logging.critical('Unhandled exception - please run same command with the -R option to send me an automated report')
                    logging.exception('Exception')
                finally:
                    err = None
                    del err

            if options.save is not None:
                if sipvicious.nextuser is not None:
                    lastextensiondst = os.path.join(exportpath, 'lastextension.pkl')
                    logging.debug('saving state to %s' % lastextensiondst)
                    try:
                        if guessmode == 1:
                            pickle.dump(sipvicious.nextuser, open(os.path.join(exportpath, 'lastextension.pkl'), 'wb'))
                            logging.debug('logged last extension %s' % sipvicious.nextuser)
                        else:
                            if guessmode == 2:
                                pickle.dump(sipvicious.guessargs.tell(), open(os.path.join(exportpath, 'lastextension.pkl'), 'wb'))
                                logging.debug('logged last position %s' % sipvicious.guessargs.tell())
                    except IOError:
                        logging.warn('could not log the last extension scanned')

            if not options.quiet:
                lenres = len(sipvicious.resultauth)
                if lenres > 0:
                    logging.info('we have %s extensions' % lenres)
                    if not lenres < 400 or options.save is not None or options.save is None:
                        labels = ('Extension', 'Authentication')
                        rows = list()
                        try:
                            for k in sipvicious.resultauth.keys():
                                rows.append((k.decode(), sipvicious.resultauth[k].decode()))

                        except AttributeError:
                            for k in sipvicious.resultauth.keys():
                                rows.append((k, sipvicious.resultauth[k]))

                        print(to_string(rows, header=labels))
                    else:
                        logging.warn('too many to print - use svreport for this')
                else:
                    logging.warn('found nothing')
        end_time = datetime.now()
        total_time = end_time - start_time
        logging.info('Total time: %s' % total_time)


if __name__ == '__main__':
    main()