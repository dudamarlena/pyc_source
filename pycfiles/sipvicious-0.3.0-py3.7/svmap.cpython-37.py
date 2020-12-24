# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sipvicious/svmap.py
# Compiled at: 2020-02-18 00:36:42
# Size of source mod 2**32: 24946 bytes
__GPL__ = '\n\n   SIPvicious SIP scanner searches for SIP devices on a given network\n   Copyright (C) 2007-2020  Sandro Gauci <sandro@enablesecurity.com>\n\n   This program is free software: you can redistribute it and/or modify\n   it under the terms of the GNU General Public License as published by\n   the Free Software Foundation, either version 3 of the License, or\n   (at your option) any later version.\n\n   This program is distributed in the hope that it will be useful,\n   but WITHOUT ANY WARRANTY; without even the implied warranty of\n   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the\n   GNU General Public License for more details.\n\n   You should have received a copy of the GNU General Public License\n   along with this program.  If not, see <http://www.gnu.org/licenses/>.\n'
import dbm, logging, os, pickle, random, select, socket, traceback
from datetime import datetime
from optparse import OptionParser
from struct import pack, unpack
from sys import exit
from libs.pptable import to_string
from libs.svhelper import __version__, calcloglevel, createTag, fingerPrintPacket, getranges, getTag, getTargetFromSRV, ip4range, makeRequest, getRange, scanlist, mysendto, packetcounter, reportBugToAuthor, dbexists, scanfromfile, scanrandom, standardoptions, standardscanneroptions, resumeFromIP, scanfromdb
__prog__ = 'svmap'

class DrinkOrSip:

    def __init__(self, scaniter, selecttime=0.005, compact=False, bindingip='0.0.0.0', fromname='sipvicious', fromaddr='sip:100@1.1.1.1', extension=None, sessionpath=None, socktimeout=3, externalip=None, localport=5060, printdebug=False, first=None, fpworks=False):
        self.log = logging.getLogger('DrinkOrSip')
        self.bindingip = bindingip
        self.sessionpath = sessionpath
        self.dbsyncs = False
        if self.sessionpath is not None:
            self.resultip = dbm.open(os.path.join(self.sessionpath, 'resultip'), 'c')
            self.resultua = dbm.open(os.path.join(self.sessionpath, 'resultua'), 'c')
            self.resultfp = dbm.open(os.path.join(self.sessionpath, 'resultfp'), 'c')
            try:
                self.resultip.sync()
                self.dbsyncs = True
                self.log.info('Db does sync')
            except AttributeError:
                self.log.info('Db does not sync')

        else:
            self.resultip = dict()
            self.resultua = dict()
            self.resultfp = dict()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.settimeout(socktimeout)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.rlist = [
         self.sock]
        self.wlist = list()
        self.xlist = list()
        self.scaniter = scaniter
        self.selecttime = selecttime
        self.localport = localport
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
        self.log.debug('External ip: %s:%s' % (self.externalip, localport))
        self.compact = compact
        self.log.debug('Compact mode: %s' % self.compact)
        self.fromname = fromname
        self.fromaddr = fromaddr
        self.log.debug('From: %s <%s>' % (self.fromname, self.fromaddr))
        self.nomoretoscan = False
        self.originallocalport = self.localport
        self.nextip = None
        self.extension = extension
        self.fpworks = fpworks
        self.printdebug = printdebug
        self.first = first
        if self.sessionpath is not None:
            self.packetcount = packetcounter(50)
        self.sentpackets = 0

    def getResponse(self, buff, srcaddr):
        srcip, srcport = srcaddr
        uaname = 'unknown'
        buff = buff.decode('utf-8')
        if not buff.startswith('OPTIONS '):
            if buff.startswith('INVITE ') or buff.startswith('REGISTER '):
                if self.externalip == srcip:
                    self.log.debug('We received our own packet from %s:%s' % srcaddr)
                else:
                    self.log.info('Looks like we received a SIP request from %s:%s' % srcaddr)
                    self.log.debug(buff.__repr__())
                return
            self.log.debug('running fingerPrintPacket()')
            res = fingerPrintPacket(buff)
            if res is not None:
                if 'name' in res:
                    uaname = res['name'][0]
        else:
            uaname = 'unknown'
            self.log.debug(buff.__repr__())
        if not self.fpworks:
            fp = None
        elif fp is None:
            if self.fpworks:
                fpname = 'unknown'
            else:
                fpname = 'disabled'
        else:
            fpname = ' / '.join(fp)
        self.log.debug('Fingerprint: %s' % fpname)
        self.log.debug('Uaname: %s' % uaname)
        originaldst = getTag(buff)
        try:
            dstip = socket.inet_ntoa(pack('!L', int(originaldst[:8], 16)))
            dstport = int(originaldst[8:12], 16)
        except (ValueError, TypeError, socket.error):
            self.log.debug('original destination could not be decoded: %s' % originaldst)
            dstip, dstport = ('unknown', 'unknown')

        resultstr = '%s:%s\t->\t%s:%s\t->\t%s\t->\t%s' % (dstip, dstport, srcip, srcport, uaname, fpname)
        self.log.info(resultstr)
        self.resultip['%s:%s' % (srcip, srcport)] = '%s:%s' % (dstip, dstport)
        self.resultua['%s:%s' % (srcip, srcport)] = uaname
        self.resultfp['%s:%s' % (srcip, srcport)] = fpname
        if self.sessionpath is not None:
            if self.dbsyncs:
                self.resultip.sync()
                self.resultua.sync()
                self.resultfp.sync()
            else:
                self.log.info('Packet from %s:%s did not contain a SIP msg' % srcaddr)
                self.log.debug('Packet: %s' % buff.__repr__())

    def start(self):
        self.log.debug('binding to %s:%s' % (self.bindingip, self.localport))
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
            self.log.warn('could not bind to %s:%s - some process might already be listening on this port. Listening on port %s instead' % (self.bindingip, self.originallocalport, self.localport))
            self.log.info('Make use of the -P option to specify a port to bind to yourself')
        while True:
            r, _, _ = select.select(self.rlist, self.wlist, self.xlist, self.selecttime)
            if r:
                try:
                    buff, srcaddr = self.sock.recvfrom(8192)
                    self.log.debug('got data from %s:%s' % srcaddr)
                    self.log.debug('data: %s' % buff.__repr__())
                    if self.printdebug:
                        print(srcaddr)
                        print(buff)
                except socket.error:
                    continue

                self.getResponse(buff, srcaddr)
            elif self.nomoretoscan:
                try:
                    self.log.debug('Making sure that no packets get lost')
                    self.log.debug('Come to daddy')
                    while True:
                        buff, srcaddr = self.sock.recvfrom(8192)
                        if self.printdebug:
                            print(srcaddr)
                            print(buff)
                        self.getResponse(buff, srcaddr)

                except socket.error:
                    break

            try:
                nextscan = next(self.scaniter)
            except StopIteration:
                self.log.debug('no more hosts to scan')
                self.nomoretoscan = True
                continue

            dstip, dstport, method = nextscan
            self.nextip = dstip
            dsthost = (dstip, dstport)
            branchunique = '%s' % random.getrandbits(32)
            localtag = createTag('%s%s' % (''.join(map(lambda x: '%02x' % int(x), dsthost[0].split('.'))), '%04x' % dsthost[1]))
            fromaddr = '"%s"<%s>' % (self.fromname, self.fromaddr)
            toaddr = fromaddr
            callid = '%s' % random.getrandbits(80)
            contact = None
            if method != 'REGISTER':
                contact = 'sip:%s@%s:%s' % (self.extension, self.externalip, self.localport)
            data = makeRequest(method,
              fromaddr,
              toaddr,
              (dsthost[0]),
              (dsthost[1]),
              callid,
              (self.externalip),
              branchunique,
              compact=(self.compact),
              localtag=localtag,
              contact=contact,
              accept='application/sdp',
              localport=(self.localport),
              extension=(self.extension))
            try:
                self.log.debug('sending packet to %s:%s' % dsthost)
                self.log.debug('packet: %s' % data.__repr__())
                mysendto(self.sock, data, dsthost)
                self.sentpackets += 1
                if self.sessionpath is not None:
                    if next(self.packetcount):
                        try:
                            f = open(os.path.join(self.sessionpath, 'lastip.pkl'), 'wb+')
                            pickle.dump(self.nextip, f)
                            f.close()
                            self.log.debug('logged last ip %s' % self.nextip)
                        except IOError:
                            self.log.warn('could not log the last ip scanned')

                if self.first is not None:
                    if self.sentpackets >= self.first:
                        self.log.info('Reached the limit to scan the first %s packets' % self.first)
                        self.nomoretoscan = True
            except socket.error as err:
                try:
                    self.log.error('socket error while sending to %s:%s -> %s' % (dsthost[0], dsthost[1], err))
                finally:
                    err = None
                    del err


def main--- This code section failed: ---

 L. 280         0  LOAD_STR                 'usage: %prog [options] host1 host2 hostrange\r\n'
                2  STORE_FAST               'usage'

 L. 281         4  LOAD_FAST                'usage'
                6  LOAD_STR                 'Scans for SIP devices on a given network\r\n\r\n'
                8  INPLACE_ADD      
               10  STORE_FAST               'usage'

 L. 282        12  LOAD_FAST                'usage'
               14  LOAD_STR                 'examples:\r\n\r\n'
               16  INPLACE_ADD      
               18  STORE_FAST               'usage'

 L. 283        20  LOAD_FAST                'usage'
               22  LOAD_STR                 '%prog 10.0.0.1-10.0.0.255 '
               24  INPLACE_ADD      
               26  STORE_FAST               'usage'

 L. 284        28  LOAD_FAST                'usage'
               30  LOAD_STR                 '172.16.131.1 sipvicious.org/22 10.0.1.1/24'
               32  INPLACE_ADD      
               34  STORE_FAST               'usage'

 L. 285        36  LOAD_FAST                'usage'
               38  LOAD_STR                 '1.1.1.1-20 1.1.2-20.* 4.1.*.*\r\n\r\n'
               40  INPLACE_ADD      
               42  STORE_FAST               'usage'

 L. 286        44  LOAD_FAST                'usage'
               46  LOAD_STR                 '%prog -s session1 --randomize 10.0.0.1/8\r\n\r\n'
               48  INPLACE_ADD      
               50  STORE_FAST               'usage'

 L. 287        52  LOAD_FAST                'usage'
               54  LOAD_STR                 '%prog --resume session1 -v\r\n\r\n'
               56  INPLACE_ADD      
               58  STORE_FAST               'usage'

 L. 288        60  LOAD_FAST                'usage'
               62  LOAD_STR                 '%prog -p5060-5062 10.0.0.3-20 -m INVITE\r\n\r\n'
               64  INPLACE_ADD      
               66  STORE_FAST               'usage'

 L. 289        68  LOAD_GLOBAL              OptionParser
               70  LOAD_FAST                'usage'
               72  LOAD_STR                 '%prog v'
               74  LOAD_GLOBAL              str
               76  LOAD_GLOBAL              __version__
               78  CALL_FUNCTION_1       1  '1 positional argument'
               80  BINARY_ADD       
               82  LOAD_GLOBAL              __GPL__
               84  BINARY_ADD       
               86  LOAD_CONST               ('version',)
               88  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               90  STORE_FAST               'parser'

 L. 290        92  LOAD_GLOBAL              standardoptions
               94  LOAD_FAST                'parser'
               96  CALL_FUNCTION_1       1  '1 positional argument'
               98  STORE_FAST               'parser'

 L. 291       100  LOAD_GLOBAL              standardscanneroptions
              102  LOAD_FAST                'parser'
              104  CALL_FUNCTION_1       1  '1 positional argument'
              106  STORE_FAST               'parser'

 L. 292       108  LOAD_FAST                'parser'
              110  LOAD_ATTR                add_option
              112  LOAD_STR                 '--randomscan'
              114  LOAD_STR                 'randomscan'
              116  LOAD_STR                 'store_true'

 L. 293       118  LOAD_CONST               False

 L. 294       120  LOAD_STR                 'Scan random IP addresses'
              122  LOAD_CONST               ('dest', 'action', 'default', 'help')
              124  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
              126  POP_TOP          

 L. 295       128  LOAD_FAST                'parser'
              130  LOAD_ATTR                add_option
              132  LOAD_STR                 '-i'
              134  LOAD_STR                 '--input'
              136  LOAD_STR                 'input'

 L. 296       138  LOAD_STR                 'Scan IPs which were found in a previous scan. Pass the session name as the argument'
              140  LOAD_STR                 'scan1'
              142  LOAD_CONST               ('dest', 'help', 'metavar')
              144  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
              146  POP_TOP          

 L. 297       148  LOAD_FAST                'parser'
              150  LOAD_ATTR                add_option
              152  LOAD_STR                 '-I'
              154  LOAD_STR                 '--inputtext'
              156  LOAD_STR                 'inputtext'

 L. 298       158  LOAD_STR                 'Scan IPs from a text file - use the same syntax as command line but with new lines instead of commas. Pass the file name as the argument'
              160  LOAD_STR                 'scan1'
              162  LOAD_CONST               ('dest', 'help', 'metavar')
              164  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
              166  POP_TOP          

 L. 299       168  LOAD_FAST                'parser'
              170  LOAD_ATTR                add_option
              172  LOAD_STR                 '-m'
              174  LOAD_STR                 '--method'
              176  LOAD_STR                 'method'

 L. 300       178  LOAD_STR                 'Specify the request method - by default this is OPTIONS.'

 L. 301       180  LOAD_STR                 'OPTIONS'
              182  LOAD_CONST               ('dest', 'help', 'default')
              184  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
              186  POP_TOP          

 L. 303       188  LOAD_FAST                'parser'
              190  LOAD_ATTR                add_option
              192  LOAD_STR                 '-d'
              194  LOAD_STR                 '--debug'
              196  LOAD_STR                 'printdebug'

 L. 304       198  LOAD_STR                 'Print SIP messages received'

 L. 305       200  LOAD_CONST               False
              202  LOAD_STR                 'store_true'
              204  LOAD_CONST               ('dest', 'help', 'default', 'action')
              206  CALL_FUNCTION_KW_6     6  '6 total positional and keyword args'
              208  POP_TOP          

 L. 307       210  LOAD_FAST                'parser'
              212  LOAD_ATTR                add_option
              214  LOAD_STR                 '--first'
              216  LOAD_STR                 'first'

 L. 308       218  LOAD_STR                 'Only send the first given number of messages (i.e. usually used to scan only X IPs)'

 L. 309       220  LOAD_STR                 'long'
              222  LOAD_CONST               ('dest', 'help', 'type')
              224  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              226  POP_TOP          

 L. 311       228  LOAD_FAST                'parser'
              230  LOAD_ATTR                add_option
              232  LOAD_STR                 '-e'
              234  LOAD_STR                 '--extension'
              236  LOAD_STR                 'extension'
              238  LOAD_STR                 '100'

 L. 312       240  LOAD_STR                 'Specify an extension - by default this is not set'
              242  LOAD_CONST               ('dest', 'default', 'help')
              244  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
              246  POP_TOP          

 L. 313       248  LOAD_FAST                'parser'
              250  LOAD_ATTR                add_option
              252  LOAD_STR                 '--randomize'
              254  LOAD_STR                 'randomize'
              256  LOAD_STR                 'store_true'

 L. 314       258  LOAD_CONST               False

 L. 315       260  LOAD_STR                 'Randomize scanning instead of scanning consecutive ip addresses'
              262  LOAD_CONST               ('dest', 'action', 'default', 'help')
              264  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
              266  POP_TOP          

 L. 316       268  LOAD_FAST                'parser'
              270  LOAD_ATTR                add_option
              272  LOAD_STR                 '--srv'
              274  LOAD_STR                 'srvscan'
              276  LOAD_STR                 'store_true'

 L. 317       278  LOAD_CONST               False

 L. 318       280  LOAD_STR                 'Scan the SRV records for SIP on the destination domain name.The targets have to be domain names - example.org domain1.com'
              282  LOAD_CONST               ('dest', 'action', 'default', 'help')
              284  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
              286  POP_TOP          

 L. 320       288  LOAD_FAST                'parser'
              290  LOAD_ATTR                add_option
              292  LOAD_STR                 '--fromname'
              294  LOAD_STR                 'fromname'
              296  LOAD_STR                 'sipvicious'

 L. 321       298  LOAD_STR                 'specify a name for the from header'
              300  LOAD_CONST               ('dest', 'default', 'help')
              302  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              304  POP_TOP          

 L. 322       306  LOAD_FAST                'parser'
              308  LOAD_ATTR                add_option
              310  LOAD_STR                 '--crashandburn'
              312  LOAD_STR                 'crashandburn'
              314  LOAD_STR                 'store_true'
              316  LOAD_CONST               False
              318  LOAD_CONST               ('dest', 'action', 'default')
              320  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              322  POP_TOP          

 L. 323       324  LOAD_FAST                'parser'
              326  LOAD_METHOD              parse_args
              328  CALL_METHOD_0         0  '0 positional arguments'
              330  UNPACK_SEQUENCE_2     2 
              332  STORE_FAST               'options'
              334  STORE_FAST               'args'

 L. 324       336  LOAD_CONST               None
              338  STORE_FAST               'exportpath'

 L. 325       340  LOAD_FAST                'options'
              342  LOAD_ATTR                resume
              344  LOAD_CONST               None
              346  COMPARE_OP               is-not
          348_350  POP_JUMP_IF_FALSE   524  'to 524'

 L. 326       352  LOAD_GLOBAL              os
              354  LOAD_ATTR                path
              356  LOAD_METHOD              join
              358  LOAD_GLOBAL              os
              360  LOAD_ATTR                path
              362  LOAD_METHOD              expanduser
              364  LOAD_STR                 '~'
              366  CALL_METHOD_1         1  '1 positional argument'
              368  LOAD_STR                 '.sipvicious'
              370  LOAD_GLOBAL              __prog__
              372  LOAD_FAST                'options'
              374  LOAD_ATTR                resume
              376  CALL_METHOD_4         4  '4 positional arguments'
              378  STORE_FAST               'exportpath'

 L. 327       380  LOAD_GLOBAL              os
              382  LOAD_ATTR                path
              384  LOAD_METHOD              exists
              386  LOAD_GLOBAL              os
              388  LOAD_ATTR                path
              390  LOAD_METHOD              join
              392  LOAD_FAST                'exportpath'
              394  LOAD_STR                 'closed'
              396  CALL_METHOD_2         2  '2 positional arguments'
              398  CALL_METHOD_1         1  '1 positional argument'
          400_402  POP_JUMP_IF_FALSE   422  'to 422'

 L. 328       404  LOAD_GLOBAL              logging
              406  LOAD_METHOD              error
              408  LOAD_STR                 'Cannot resume a session that is complete'
              410  CALL_METHOD_1         1  '1 positional argument'
              412  POP_TOP          

 L. 329       414  LOAD_GLOBAL              exit
              416  LOAD_CONST               1
              418  CALL_FUNCTION_1       1  '1 positional argument'
              420  POP_TOP          
            422_0  COME_FROM           400  '400'

 L. 330       422  LOAD_GLOBAL              os
              424  LOAD_ATTR                path
              426  LOAD_METHOD              exists
              428  LOAD_FAST                'exportpath'
              430  CALL_METHOD_1         1  '1 positional argument'
          432_434  POP_JUMP_IF_TRUE    460  'to 460'

 L. 331       436  LOAD_GLOBAL              logging
              438  LOAD_METHOD              critical
              440  LOAD_STR                 'A session with the name %s was not found'
              442  LOAD_FAST                'options'
              444  LOAD_ATTR                resume
              446  BINARY_MODULO    
              448  CALL_METHOD_1         1  '1 positional argument'
              450  POP_TOP          

 L. 332       452  LOAD_GLOBAL              exit
              454  LOAD_CONST               1
              456  CALL_FUNCTION_1       1  '1 positional argument'
              458  POP_TOP          
            460_0  COME_FROM           432  '432'

 L. 333       460  LOAD_GLOBAL              os
              462  LOAD_ATTR                path
              464  LOAD_METHOD              join
              466  LOAD_FAST                'exportpath'
              468  LOAD_STR                 'options.pkl'
              470  CALL_METHOD_2         2  '2 positional arguments'
              472  STORE_FAST               'optionssrc'

 L. 334       474  LOAD_FAST                'options'
              476  LOAD_ATTR                resume
              478  STORE_FAST               'previousresume'

 L. 335       480  LOAD_FAST                'options'
              482  LOAD_ATTR                verbose
              484  STORE_FAST               'previousverbose'

 L. 336       486  LOAD_GLOBAL              pickle
              488  LOAD_ATTR                load
              490  LOAD_GLOBAL              open
              492  LOAD_FAST                'optionssrc'
              494  LOAD_STR                 'rb'
              496  CALL_FUNCTION_2       2  '2 positional arguments'
              498  LOAD_STR                 'bytes'
              500  LOAD_CONST               ('encoding',)
              502  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              504  UNPACK_SEQUENCE_2     2 
              506  STORE_FAST               'options'
              508  STORE_FAST               'args'

 L. 337       510  LOAD_FAST                'previousresume'
              512  LOAD_FAST                'options'
              514  STORE_ATTR               resume

 L. 338       516  LOAD_FAST                'previousverbose'
              518  LOAD_FAST                'options'
              520  STORE_ATTR               verbose
              522  JUMP_FORWARD        564  'to 564'
            524_0  COME_FROM           348  '348'

 L. 339       524  LOAD_FAST                'options'
              526  LOAD_ATTR                save
              528  LOAD_CONST               None
              530  COMPARE_OP               is-not
          532_534  POP_JUMP_IF_FALSE   564  'to 564'

 L. 340       536  LOAD_GLOBAL              os
              538  LOAD_ATTR                path
              540  LOAD_METHOD              join
              542  LOAD_GLOBAL              os
              544  LOAD_ATTR                path
              546  LOAD_METHOD              expanduser
              548  LOAD_STR                 '~'
              550  CALL_METHOD_1         1  '1 positional argument'
              552  LOAD_STR                 '.sipvicious'
              554  LOAD_GLOBAL              __prog__
              556  LOAD_FAST                'options'
              558  LOAD_ATTR                save
              560  CALL_METHOD_4         4  '4 positional arguments'
              562  STORE_FAST               'exportpath'
            564_0  COME_FROM           532  '532'
            564_1  COME_FROM           522  '522'

 L. 341       564  LOAD_GLOBAL              logging
              566  LOAD_ATTR                basicConfig
              568  LOAD_GLOBAL              calcloglevel
              570  LOAD_FAST                'options'
              572  CALL_FUNCTION_1       1  '1 positional argument'
              574  LOAD_CONST               ('level',)
              576  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              578  POP_TOP          

 L. 342       580  LOAD_GLOBAL              logging
              582  LOAD_METHOD              debug
              584  LOAD_STR                 'started logging'
              586  CALL_METHOD_1         1  '1 positional argument'
              588  POP_TOP          

 L. 343       590  LOAD_CONST               None
              592  STORE_FAST               'scanrandomstore'

 L. 344       594  LOAD_FAST                'options'
              596  LOAD_ATTR                input
              598  LOAD_CONST               None
              600  COMPARE_OP               is-not
          602_604  POP_JUMP_IF_FALSE   688  'to 688'

 L. 345       606  LOAD_GLOBAL              os
              608  LOAD_ATTR                path
              610  LOAD_METHOD              join
              612  LOAD_GLOBAL              os
              614  LOAD_ATTR                path
              616  LOAD_METHOD              expanduser
              618  LOAD_STR                 '~'
              620  CALL_METHOD_1         1  '1 positional argument'
              622  LOAD_STR                 '.sipvicious'
              624  LOAD_GLOBAL              __prog__
              626  LOAD_FAST                'options'
              628  LOAD_ATTR                input
              630  LOAD_STR                 'resultua'
              632  CALL_METHOD_5         5  '5 positional arguments'
              634  STORE_FAST               'db'

 L. 346       636  LOAD_GLOBAL              dbexists
              638  LOAD_FAST                'db'
              640  CALL_FUNCTION_1       1  '1 positional argument'
          642_644  POP_JUMP_IF_FALSE   666  'to 666'

 L. 347       646  LOAD_GLOBAL              scanfromdb
              648  LOAD_FAST                'db'
              650  LOAD_FAST                'options'
              652  LOAD_ATTR                method
              654  LOAD_METHOD              split
              656  LOAD_STR                 ','
              658  CALL_METHOD_1         1  '1 positional argument'
              660  CALL_FUNCTION_2       2  '2 positional arguments'
              662  STORE_FAST               'scaniter'
              664  JUMP_FORWARD       1624  'to 1624'
            666_0  COME_FROM           642  '642'

 L. 349       666  LOAD_GLOBAL              logging
              668  LOAD_METHOD              error
              670  LOAD_STR                 'the session name does not exist. Please use svreport to list existing scans'
              672  CALL_METHOD_1         1  '1 positional argument'
              674  POP_TOP          

 L. 350       676  LOAD_GLOBAL              exit
              678  LOAD_CONST               1
              680  CALL_FUNCTION_1       1  '1 positional argument'
              682  POP_TOP          
          684_686  JUMP_FORWARD       1624  'to 1624'
            688_0  COME_FROM           602  '602'

 L. 351       688  LOAD_FAST                'options'
              690  LOAD_ATTR                randomscan
          692_694  POP_JUMP_IF_FALSE   864  'to 864'

 L. 352       696  LOAD_GLOBAL              logging
              698  LOAD_METHOD              debug
              700  LOAD_STR                 'making use of random scan'
              702  CALL_METHOD_1         1  '1 positional argument'
              704  POP_TOP          

 L. 353       706  LOAD_GLOBAL              logging
              708  LOAD_METHOD              debug
              710  LOAD_STR                 'parsing range of ports: %s'
              712  LOAD_FAST                'options'
              714  LOAD_ATTR                port
              716  BINARY_MODULO    
              718  CALL_METHOD_1         1  '1 positional argument'
              720  POP_TOP          

 L. 354       722  LOAD_GLOBAL              getRange
              724  LOAD_FAST                'options'
              726  LOAD_ATTR                port
              728  CALL_FUNCTION_1       1  '1 positional argument'
              730  STORE_FAST               'portrange'

 L. 355       732  LOAD_CONST               16777216
              734  LOAD_CONST               167772159
              736  BUILD_LIST_2          2 

 L. 356       738  LOAD_CONST               184549376
              740  LOAD_CONST               234881023
              742  BUILD_LIST_2          2 

 L. 357       744  LOAD_CONST               251658240
              746  LOAD_CONST               2130706431
              748  BUILD_LIST_2          2 

 L. 358       750  LOAD_CONST               2147549184
              752  LOAD_CONST               2851995647
              754  BUILD_LIST_2          2 

 L. 359       756  LOAD_CONST               2852061184
              758  LOAD_CONST               2886729727
              760  BUILD_LIST_2          2 

 L. 360       762  LOAD_CONST               2886795264
              764  LOAD_CONST               3221159935
              766  BUILD_LIST_2          2 

 L. 361       768  LOAD_CONST               3221226240
              770  LOAD_CONST               3227017983
              772  BUILD_LIST_2          2 

 L. 362       774  LOAD_CONST               3227018240
              776  LOAD_CONST               3232235519
              778  BUILD_LIST_2          2 

 L. 363       780  LOAD_CONST               3232301056
              782  LOAD_CONST               3323068415
              784  BUILD_LIST_2          2 

 L. 364       786  LOAD_CONST               3323199488
              788  LOAD_CONST               3758096127
              790  BUILD_LIST_2          2 
              792  BUILD_LIST_10        10 
              794  STORE_FAST               'internetranges'

 L. 366       796  LOAD_STR                 '.sipviciousrandomtmp'
              798  STORE_FAST               'scanrandomstore'

 L. 367       800  LOAD_CONST               False
              802  STORE_FAST               'resumescan'

 L. 368       804  LOAD_FAST                'options'
              806  LOAD_ATTR                save
              808  LOAD_CONST               None
              810  COMPARE_OP               is-not
          812_814  POP_JUMP_IF_FALSE   834  'to 834'

 L. 369       816  LOAD_GLOBAL              os
              818  LOAD_ATTR                path
              820  LOAD_METHOD              join
              822  LOAD_FAST                'exportpath'
              824  LOAD_STR                 'random'
              826  CALL_METHOD_2         2  '2 positional arguments'
              828  STORE_FAST               'scanrandomstore'

 L. 370       830  LOAD_CONST               True
              832  STORE_FAST               'resumescan'
            834_0  COME_FROM           812  '812'

 L. 371       834  LOAD_GLOBAL              scanrandom

 L. 372       836  LOAD_FAST                'internetranges'

 L. 373       838  LOAD_FAST                'portrange'

 L. 374       840  LOAD_FAST                'options'
              842  LOAD_ATTR                method
              844  LOAD_METHOD              split
              846  LOAD_STR                 ','
              848  CALL_METHOD_1         1  '1 positional argument'

 L. 375       850  LOAD_FAST                'scanrandomstore'

 L. 376       852  LOAD_FAST                'resumescan'
              854  LOAD_CONST               ('randomstore', 'resume')
              856  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
              858  STORE_FAST               'scaniter'
          860_862  JUMP_FORWARD       1624  'to 1624'
            864_0  COME_FROM           692  '692'

 L. 378       864  LOAD_FAST                'options'
              866  LOAD_ATTR                inputtext
          868_870  POP_JUMP_IF_FALSE  1194  'to 1194'

 L. 379       872  LOAD_GLOBAL              logging
              874  LOAD_METHOD              debug
              876  LOAD_STR                 'Using IP addresses from input text file'
              878  CALL_METHOD_1         1  '1 positional argument'
              880  POP_TOP          

 L. 380       882  SETUP_EXCEPT        916  'to 916'

 L. 381       884  LOAD_GLOBAL              open
              886  LOAD_FAST                'options'
              888  LOAD_ATTR                inputtext
              890  LOAD_STR                 'r'
              892  CALL_FUNCTION_2       2  '2 positional arguments'
              894  STORE_FAST               'f'

 L. 382       896  LOAD_FAST                'f'
              898  LOAD_METHOD              readlines
              900  CALL_METHOD_0         0  '0 positional arguments'
              902  STORE_FAST               'args'

 L. 383       904  LOAD_FAST                'f'
              906  LOAD_METHOD              close
              908  CALL_METHOD_0         0  '0 positional arguments'
              910  POP_TOP          
              912  POP_BLOCK        
              914  JUMP_FORWARD        962  'to 962'
            916_0  COME_FROM_EXCEPT    882  '882'

 L. 384       916  DUP_TOP          
              918  LOAD_GLOBAL              IOError
              920  COMPARE_OP               exception-match
          922_924  POP_JUMP_IF_FALSE   960  'to 960'
              926  POP_TOP          
              928  POP_TOP          
              930  POP_TOP          

 L. 385       932  LOAD_GLOBAL              logging
              934  LOAD_METHOD              critical
              936  LOAD_STR                 'Could not open %s'
              938  LOAD_FAST                'options'
              940  LOAD_ATTR                inputtext
              942  BINARY_MODULO    
              944  CALL_METHOD_1         1  '1 positional argument'
              946  POP_TOP          

 L. 386       948  LOAD_GLOBAL              exit
              950  LOAD_CONST               1
              952  CALL_FUNCTION_1       1  '1 positional argument'
              954  POP_TOP          
              956  POP_EXCEPT       
              958  JUMP_FORWARD        962  'to 962'
            960_0  COME_FROM           922  '922'
              960  END_FINALLY      
            962_0  COME_FROM           958  '958'
            962_1  COME_FROM           914  '914'

 L. 387       962  LOAD_GLOBAL              list
              964  LOAD_GLOBAL              map
              966  LOAD_LAMBDA              '<code_object <lambda>>'
              968  LOAD_STR                 'main.<locals>.<lambda>'
              970  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              972  LOAD_FAST                'args'
              974  CALL_FUNCTION_2       2  '2 positional arguments'
              976  CALL_FUNCTION_1       1  '1 positional argument'
              978  STORE_FAST               'args'

 L. 388       980  LOAD_LISTCOMP            '<code_object <listcomp>>'
              982  LOAD_STR                 'main.<locals>.<listcomp>'
              984  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              986  LOAD_FAST                'args'
              988  GET_ITER         
              990  CALL_FUNCTION_1       1  '1 positional argument'
              992  STORE_FAST               'args'

 L. 389       994  LOAD_GLOBAL              logging
              996  LOAD_METHOD              debug
              998  LOAD_STR                 'ip addresses %s'
             1000  LOAD_FAST                'args'
             1002  BINARY_MODULO    
             1004  CALL_METHOD_1         1  '1 positional argument'
             1006  POP_TOP          

 L. 390      1008  SETUP_EXCEPT       1022  'to 1022'

 L. 391      1010  LOAD_GLOBAL              ip4range
             1012  LOAD_FAST                'args'
             1014  CALL_FUNCTION_EX      0  'positional arguments only'
             1016  STORE_FAST               'iprange'
             1018  POP_BLOCK        
             1020  JUMP_FORWARD       1076  'to 1076'
           1022_0  COME_FROM_EXCEPT   1008  '1008'

 L. 392      1022  DUP_TOP          
             1024  LOAD_GLOBAL              ValueError
             1026  COMPARE_OP               exception-match
         1028_1030  POP_JUMP_IF_FALSE  1074  'to 1074'
             1032  POP_TOP          
             1034  STORE_FAST               'err'
             1036  POP_TOP          
             1038  SETUP_FINALLY      1062  'to 1062'

 L. 393      1040  LOAD_GLOBAL              logging
             1042  LOAD_METHOD              error
             1044  LOAD_FAST                'err'
             1046  CALL_METHOD_1         1  '1 positional argument'
             1048  POP_TOP          

 L. 394      1050  LOAD_GLOBAL              exit
             1052  LOAD_CONST               1
             1054  CALL_FUNCTION_1       1  '1 positional argument'
             1056  POP_TOP          
             1058  POP_BLOCK        
             1060  LOAD_CONST               None
           1062_0  COME_FROM_FINALLY  1038  '1038'
             1062  LOAD_CONST               None
             1064  STORE_FAST               'err'
             1066  DELETE_FAST              'err'
             1068  END_FINALLY      
             1070  POP_EXCEPT       
             1072  JUMP_FORWARD       1076  'to 1076'
           1074_0  COME_FROM          1028  '1028'
             1074  END_FINALLY      
           1076_0  COME_FROM          1072  '1072'
           1076_1  COME_FROM          1020  '1020'

 L. 395      1076  LOAD_GLOBAL              getRange
             1078  LOAD_FAST                'options'
             1080  LOAD_ATTR                port
             1082  CALL_FUNCTION_1       1  '1 positional argument'
             1084  STORE_FAST               'portrange'

 L. 396      1086  LOAD_FAST                'options'
             1088  LOAD_ATTR                randomize
         1090_1092  POP_JUMP_IF_FALSE  1170  'to 1170'

 L. 397      1094  LOAD_STR                 '.sipviciousrandomtmp'
             1096  STORE_FAST               'scanrandomstore'

 L. 398      1098  LOAD_CONST               False
             1100  STORE_FAST               'resumescan'

 L. 399      1102  LOAD_FAST                'options'
             1104  LOAD_ATTR                save
             1106  LOAD_CONST               None
             1108  COMPARE_OP               is-not
         1110_1112  POP_JUMP_IF_FALSE  1132  'to 1132'

 L. 400      1114  LOAD_GLOBAL              os
             1116  LOAD_ATTR                path
             1118  LOAD_METHOD              join
             1120  LOAD_FAST                'exportpath'
             1122  LOAD_STR                 'random'
             1124  CALL_METHOD_2         2  '2 positional arguments'
             1126  STORE_FAST               'scanrandomstore'

 L. 401      1128  LOAD_CONST               True
             1130  STORE_FAST               'resumescan'
           1132_0  COME_FROM          1110  '1110'

 L. 402      1132  LOAD_GLOBAL              scanrandom
             1134  LOAD_GLOBAL              list
             1136  LOAD_GLOBAL              map
             1138  LOAD_GLOBAL              getranges
             1140  LOAD_FAST                'args'
             1142  CALL_FUNCTION_2       2  '2 positional arguments'
             1144  CALL_FUNCTION_1       1  '1 positional argument'
             1146  LOAD_FAST                'portrange'

 L. 403      1148  LOAD_FAST                'options'
             1150  LOAD_ATTR                method
             1152  LOAD_METHOD              split
             1154  LOAD_STR                 ','
             1156  CALL_METHOD_1         1  '1 positional argument'
             1158  LOAD_FAST                'scanrandomstore'
             1160  LOAD_FAST                'resumescan'
             1162  LOAD_CONST               ('randomstore', 'resume')
             1164  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
             1166  STORE_FAST               'scaniter'
             1168  JUMP_FORWARD       1624  'to 1624'
           1170_0  COME_FROM          1090  '1090'

 L. 405      1170  LOAD_GLOBAL              scanlist
             1172  LOAD_FAST                'iprange'
             1174  LOAD_FAST                'portrange'
             1176  LOAD_FAST                'options'
             1178  LOAD_ATTR                method
             1180  LOAD_METHOD              split
             1182  LOAD_STR                 ','
             1184  CALL_METHOD_1         1  '1 positional argument'
             1186  CALL_FUNCTION_3       3  '3 positional arguments'
             1188  STORE_FAST               'scaniter'
         1190_1192  JUMP_FORWARD       1624  'to 1624'
           1194_0  COME_FROM           868  '868'

 L. 407      1194  LOAD_GLOBAL              len
             1196  LOAD_FAST                'args'
             1198  CALL_FUNCTION_1       1  '1 positional argument'
             1200  LOAD_CONST               1
             1202  COMPARE_OP               <
         1204_1206  POP_JUMP_IF_FALSE  1226  'to 1226'

 L. 408      1208  LOAD_FAST                'parser'
             1210  LOAD_METHOD              error
             1212  LOAD_STR                 'Provide at least one target'
             1214  CALL_METHOD_1         1  '1 positional argument'
             1216  POP_TOP          

 L. 409      1218  LOAD_GLOBAL              exit
             1220  LOAD_CONST               1
             1222  CALL_FUNCTION_1       1  '1 positional argument'
             1224  POP_TOP          
           1226_0  COME_FROM          1204  '1204'

 L. 410      1226  LOAD_GLOBAL              logging
             1228  LOAD_METHOD              debug
             1230  LOAD_STR                 'parsing range of ports: %s'
             1232  LOAD_FAST                'options'
             1234  LOAD_ATTR                port
             1236  BINARY_MODULO    
             1238  CALL_METHOD_1         1  '1 positional argument'
             1240  POP_TOP          

 L. 411      1242  LOAD_GLOBAL              getRange
             1244  LOAD_FAST                'options'
             1246  LOAD_ATTR                port
             1248  CALL_FUNCTION_1       1  '1 positional argument'
             1250  STORE_FAST               'portrange'

 L. 412      1252  LOAD_FAST                'options'
             1254  LOAD_ATTR                randomize
         1256_1258  POP_JUMP_IF_FALSE  1338  'to 1338'

 L. 413      1260  LOAD_STR                 '.sipviciousrandomtmp'
             1262  STORE_FAST               'scanrandomstore'

 L. 414      1264  LOAD_CONST               False
             1266  STORE_FAST               'resumescan'

 L. 415      1268  LOAD_FAST                'options'
             1270  LOAD_ATTR                save
             1272  LOAD_CONST               None
             1274  COMPARE_OP               is-not
         1276_1278  POP_JUMP_IF_FALSE  1298  'to 1298'

 L. 416      1280  LOAD_GLOBAL              os
             1282  LOAD_ATTR                path
             1284  LOAD_METHOD              join
             1286  LOAD_FAST                'exportpath'
             1288  LOAD_STR                 'random'
             1290  CALL_METHOD_2         2  '2 positional arguments'
             1292  STORE_FAST               'scanrandomstore'

 L. 417      1294  LOAD_CONST               True
             1296  STORE_FAST               'resumescan'
           1298_0  COME_FROM          1276  '1276'

 L. 418      1298  LOAD_GLOBAL              scanrandom
             1300  LOAD_GLOBAL              list
             1302  LOAD_GLOBAL              map
             1304  LOAD_GLOBAL              getranges
             1306  LOAD_FAST                'args'
             1308  CALL_FUNCTION_2       2  '2 positional arguments'
             1310  CALL_FUNCTION_1       1  '1 positional argument'
             1312  LOAD_FAST                'portrange'

 L. 419      1314  LOAD_FAST                'options'
             1316  LOAD_ATTR                method
             1318  LOAD_METHOD              split
             1320  LOAD_STR                 ','
             1322  CALL_METHOD_1         1  '1 positional argument'
             1324  LOAD_FAST                'scanrandomstore'
             1326  LOAD_FAST                'resumescan'
             1328  LOAD_CONST               ('randomstore', 'resume')
             1330  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
             1332  STORE_FAST               'scaniter'
         1334_1336  JUMP_FORWARD       1624  'to 1624'
           1338_0  COME_FROM          1256  '1256'

 L. 420      1338  LOAD_FAST                'options'
             1340  LOAD_ATTR                srvscan
         1342_1344  POP_JUMP_IF_FALSE  1376  'to 1376'

 L. 421      1346  LOAD_GLOBAL              logging
             1348  LOAD_METHOD              debug
             1350  LOAD_STR                 'making use of SRV records'
             1352  CALL_METHOD_1         1  '1 positional argument'
             1354  POP_TOP          

 L. 422      1356  LOAD_GLOBAL              getTargetFromSRV
             1358  LOAD_FAST                'args'
             1360  LOAD_FAST                'options'
             1362  LOAD_ATTR                method
             1364  LOAD_METHOD              split
             1366  LOAD_STR                 ','
             1368  CALL_METHOD_1         1  '1 positional argument'
             1370  CALL_FUNCTION_2       2  '2 positional arguments'
             1372  STORE_FAST               'scaniter'
             1374  JUMP_FORWARD       1624  'to 1624'
           1376_0  COME_FROM          1342  '1342'

 L. 424      1376  LOAD_FAST                'options'
             1378  LOAD_ATTR                resume
             1380  LOAD_CONST               None
             1382  COMPARE_OP               is-not
         1384_1386  POP_JUMP_IF_FALSE  1536  'to 1536'

 L. 425      1388  LOAD_GLOBAL              os
             1390  LOAD_ATTR                path
             1392  LOAD_METHOD              join
             1394  LOAD_FAST                'exportpath'
             1396  LOAD_STR                 'lastip.pkl'
             1398  CALL_METHOD_2         2  '2 positional arguments'
             1400  STORE_FAST               'lastipsrc'

 L. 426      1402  SETUP_EXCEPT       1440  'to 1440'

 L. 427      1404  LOAD_GLOBAL              open
             1406  LOAD_FAST                'lastipsrc'
             1408  LOAD_STR                 'rb'
             1410  CALL_FUNCTION_2       2  '2 positional arguments'
             1412  STORE_FAST               'f'

 L. 428      1414  LOAD_GLOBAL              pickle
             1416  LOAD_ATTR                load
             1418  LOAD_FAST                'f'
             1420  LOAD_STR                 'bytes'
             1422  LOAD_CONST               ('encoding',)
             1424  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1426  STORE_FAST               'previousip'

 L. 429      1428  LOAD_FAST                'f'
             1430  LOAD_METHOD              close
             1432  CALL_METHOD_0         0  '0 positional arguments'
             1434  POP_TOP          
             1436  POP_BLOCK        
             1438  JUMP_FORWARD       1484  'to 1484'
           1440_0  COME_FROM_EXCEPT   1402  '1402'

 L. 430      1440  DUP_TOP          
             1442  LOAD_GLOBAL              IOError
             1444  COMPARE_OP               exception-match
         1446_1448  POP_JUMP_IF_FALSE  1482  'to 1482'
             1450  POP_TOP          
             1452  POP_TOP          
             1454  POP_TOP          

 L. 431      1456  LOAD_GLOBAL              logging
             1458  LOAD_METHOD              critical
             1460  LOAD_STR                 'Could not read from %s'
             1462  LOAD_FAST                'lastipsrc'
             1464  BINARY_MODULO    
             1466  CALL_METHOD_1         1  '1 positional argument'
             1468  POP_TOP          

 L. 432      1470  LOAD_GLOBAL              exit
             1472  LOAD_CONST               1
             1474  CALL_FUNCTION_1       1  '1 positional argument'
             1476  POP_TOP          
             1478  POP_EXCEPT       
             1480  JUMP_FORWARD       1484  'to 1484'
           1482_0  COME_FROM          1446  '1446'
             1482  END_FINALLY      
           1484_0  COME_FROM          1480  '1480'
           1484_1  COME_FROM          1438  '1438'

 L. 433      1484  LOAD_GLOBAL              logging
             1486  LOAD_METHOD              debug
             1488  LOAD_STR                 'Previous args: %s'
             1490  LOAD_FAST                'args'
             1492  BINARY_MODULO    
             1494  CALL_METHOD_1         1  '1 positional argument'
             1496  POP_TOP          

 L. 434      1498  LOAD_GLOBAL              resumeFromIP
             1500  LOAD_FAST                'previousip'
             1502  LOAD_FAST                'args'
             1504  CALL_FUNCTION_2       2  '2 positional arguments'
             1506  STORE_FAST               'args'

 L. 435      1508  LOAD_GLOBAL              logging
             1510  LOAD_METHOD              debug
             1512  LOAD_STR                 'New args: %s'
             1514  LOAD_FAST                'args'
             1516  BINARY_MODULO    
             1518  CALL_METHOD_1         1  '1 positional argument'
             1520  POP_TOP          

 L. 436      1522  LOAD_GLOBAL              logging
             1524  LOAD_METHOD              info
             1526  LOAD_STR                 'Resuming from %s'
             1528  LOAD_FAST                'previousip'
             1530  BINARY_MODULO    
             1532  CALL_METHOD_1         1  '1 positional argument'
             1534  POP_TOP          
           1536_0  COME_FROM          1384  '1384'

 L. 439      1536  SETUP_EXCEPT       1550  'to 1550'

 L. 440      1538  LOAD_GLOBAL              ip4range
             1540  LOAD_FAST                'args'
             1542  CALL_FUNCTION_EX      0  'positional arguments only'
             1544  STORE_FAST               'iprange'
             1546  POP_BLOCK        
             1548  JUMP_FORWARD       1604  'to 1604'
           1550_0  COME_FROM_EXCEPT   1536  '1536'

 L. 441      1550  DUP_TOP          
             1552  LOAD_GLOBAL              ValueError
             1554  COMPARE_OP               exception-match
         1556_1558  POP_JUMP_IF_FALSE  1602  'to 1602'
             1560  POP_TOP          
             1562  STORE_FAST               'err'
             1564  POP_TOP          
             1566  SETUP_FINALLY      1590  'to 1590'

 L. 442      1568  LOAD_GLOBAL              logging
             1570  LOAD_METHOD              error
             1572  LOAD_FAST                'err'
             1574  CALL_METHOD_1         1  '1 positional argument'
             1576  POP_TOP          

 L. 443      1578  LOAD_GLOBAL              exit
             1580  LOAD_CONST               1
             1582  CALL_FUNCTION_1       1  '1 positional argument'
             1584  POP_TOP          
             1586  POP_BLOCK        
             1588  LOAD_CONST               None
           1590_0  COME_FROM_FINALLY  1566  '1566'
             1590  LOAD_CONST               None
             1592  STORE_FAST               'err'
             1594  DELETE_FAST              'err'
             1596  END_FINALLY      
             1598  POP_EXCEPT       
           1600_0  COME_FROM          1168  '1168'
             1600  JUMP_FORWARD       1604  'to 1604'
           1602_0  COME_FROM          1556  '1556'
           1602_1  COME_FROM           664  '664'
             1602  END_FINALLY      
           1604_0  COME_FROM          1600  '1600'
           1604_1  COME_FROM          1548  '1548'

 L. 444      1604  LOAD_GLOBAL              scanlist
             1606  LOAD_FAST                'iprange'
             1608  LOAD_FAST                'portrange'
             1610  LOAD_FAST                'options'
             1612  LOAD_ATTR                method
             1614  LOAD_METHOD              split
             1616  LOAD_STR                 ','
             1618  CALL_METHOD_1         1  '1 positional argument'
             1620  CALL_FUNCTION_3       3  '3 positional arguments'
             1622  STORE_FAST               'scaniter'
           1624_0  COME_FROM          1374  '1374'
           1624_1  COME_FROM          1334  '1334'
           1624_2  COME_FROM          1190  '1190'
           1624_3  COME_FROM           860  '860'
           1624_4  COME_FROM           684  '684'

 L. 445      1624  LOAD_FAST                'options'
             1626  LOAD_ATTR                save
             1628  LOAD_CONST               None
             1630  COMPARE_OP               is-not
         1632_1634  POP_JUMP_IF_FALSE  1836  'to 1836'

 L. 446      1636  LOAD_FAST                'options'
             1638  LOAD_ATTR                resume
             1640  LOAD_CONST               None
             1642  COMPARE_OP               is
         1644_1646  POP_JUMP_IF_FALSE  1836  'to 1836'

 L. 447      1648  LOAD_GLOBAL              os
             1650  LOAD_ATTR                path
             1652  LOAD_METHOD              join
             1654  LOAD_GLOBAL              os
             1656  LOAD_ATTR                path
             1658  LOAD_METHOD              expanduser
             1660  LOAD_STR                 '~'
             1662  CALL_METHOD_1         1  '1 positional argument'
             1664  LOAD_STR                 '.sipvicious'
             1666  LOAD_GLOBAL              __prog__
             1668  LOAD_FAST                'options'
             1670  LOAD_ATTR                save
             1672  CALL_METHOD_4         4  '4 positional arguments'
             1674  STORE_FAST               'exportpath'

 L. 448      1676  LOAD_GLOBAL              os
             1678  LOAD_ATTR                path
             1680  LOAD_METHOD              exists
             1682  LOAD_FAST                'exportpath'
             1684  CALL_METHOD_1         1  '1 positional argument'
         1686_1688  POP_JUMP_IF_FALSE  1708  'to 1708'

 L. 449      1690  LOAD_GLOBAL              logging
             1692  LOAD_METHOD              warn
             1694  LOAD_STR                 'we found a previous scan with the same name. Please choose a new session name'
             1696  CALL_METHOD_1         1  '1 positional argument'
             1698  POP_TOP          

 L. 450      1700  LOAD_GLOBAL              exit
             1702  LOAD_CONST               1
             1704  CALL_FUNCTION_1       1  '1 positional argument'
             1706  POP_TOP          
           1708_0  COME_FROM          1686  '1686'

 L. 451      1708  LOAD_GLOBAL              logging
             1710  LOAD_METHOD              debug
             1712  LOAD_STR                 'creating an export location %s'
             1714  LOAD_FAST                'exportpath'
             1716  BINARY_MODULO    
             1718  CALL_METHOD_1         1  '1 positional argument'
             1720  POP_TOP          

 L. 452      1722  SETUP_EXCEPT       1742  'to 1742'

 L. 453      1724  LOAD_GLOBAL              os
             1726  LOAD_ATTR                makedirs
             1728  LOAD_FAST                'exportpath'
             1730  LOAD_CONST               448
             1732  LOAD_CONST               ('mode',)
             1734  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1736  POP_TOP          
             1738  POP_BLOCK        
             1740  JUMP_FORWARD       1786  'to 1786'
           1742_0  COME_FROM_EXCEPT   1722  '1722'

 L. 454      1742  DUP_TOP          
             1744  LOAD_GLOBAL              OSError
             1746  COMPARE_OP               exception-match
         1748_1750  POP_JUMP_IF_FALSE  1784  'to 1784'
             1752  POP_TOP          
             1754  POP_TOP          
             1756  POP_TOP          

 L. 455      1758  LOAD_GLOBAL              logging
             1760  LOAD_METHOD              critical
             1762  LOAD_STR                 'could not create the export location %s'
             1764  LOAD_FAST                'exportpath'
             1766  BINARY_MODULO    
             1768  CALL_METHOD_1         1  '1 positional argument'
             1770  POP_TOP          

 L. 456      1772  LOAD_GLOBAL              exit
             1774  LOAD_CONST               1
             1776  CALL_FUNCTION_1       1  '1 positional argument'
             1778  POP_TOP          
             1780  POP_EXCEPT       
             1782  JUMP_FORWARD       1786  'to 1786'
           1784_0  COME_FROM          1748  '1748'
             1784  END_FINALLY      
           1786_0  COME_FROM          1782  '1782'
           1786_1  COME_FROM          1740  '1740'

 L. 457      1786  LOAD_GLOBAL              os
             1788  LOAD_ATTR                path
             1790  LOAD_METHOD              join
             1792  LOAD_FAST                'exportpath'
             1794  LOAD_STR                 'options.pkl'
             1796  CALL_METHOD_2         2  '2 positional arguments'
             1798  STORE_FAST               'optionsdst'

 L. 458      1800  LOAD_GLOBAL              logging
             1802  LOAD_METHOD              debug
             1804  LOAD_STR                 'saving options to %s'
             1806  LOAD_FAST                'optionsdst'
             1808  BINARY_MODULO    
             1810  CALL_METHOD_1         1  '1 positional argument'
             1812  POP_TOP          

 L. 459      1814  LOAD_GLOBAL              pickle
             1816  LOAD_METHOD              dump
             1818  LOAD_FAST                'options'
             1820  LOAD_FAST                'args'
             1822  BUILD_LIST_2          2 
             1824  LOAD_GLOBAL              open
             1826  LOAD_FAST                'optionsdst'
             1828  LOAD_STR                 'wb+'
             1830  CALL_FUNCTION_2       2  '2 positional arguments'
             1832  CALL_METHOD_2         2  '2 positional arguments'
             1834  POP_TOP          
           1836_0  COME_FROM          1644  '1644'
           1836_1  COME_FROM          1632  '1632'

 L. 460      1836  SETUP_EXCEPT       1848  'to 1848'

 L. 461      1838  LOAD_FAST                'options'
             1840  LOAD_ATTR                extension
             1842  POP_TOP          
             1844  POP_BLOCK        
             1846  JUMP_FORWARD       1876  'to 1876'
           1848_0  COME_FROM_EXCEPT   1836  '1836'

 L. 462      1848  DUP_TOP          
             1850  LOAD_GLOBAL              AttributeError
             1852  COMPARE_OP               exception-match
         1854_1856  POP_JUMP_IF_FALSE  1874  'to 1874'
             1858  POP_TOP          
             1860  POP_TOP          
             1862  POP_TOP          

 L. 463      1864  LOAD_CONST               None
             1866  LOAD_FAST                'options'
             1868  STORE_ATTR               extension
             1870  POP_EXCEPT       
             1872  JUMP_FORWARD       1876  'to 1876'
           1874_0  COME_FROM          1854  '1854'
             1874  END_FINALLY      
           1876_0  COME_FROM          1872  '1872'
           1876_1  COME_FROM          1846  '1846'

 L. 464      1876  LOAD_FAST                'options'
             1878  LOAD_ATTR                autogetip
         1880_1882  POP_JUMP_IF_FALSE  1932  'to 1932'

 L. 465      1884  LOAD_GLOBAL              socket
             1886  LOAD_METHOD              socket
             1888  LOAD_GLOBAL              socket
             1890  LOAD_ATTR                AF_INET
             1892  LOAD_GLOBAL              socket
             1894  LOAD_ATTR                SOCK_STREAM
             1896  CALL_METHOD_2         2  '2 positional arguments'
             1898  STORE_FAST               'tmpsocket'

 L. 466      1900  LOAD_FAST                'tmpsocket'
             1902  LOAD_METHOD              connect
             1904  LOAD_CONST               ('msn.com', 80)
             1906  CALL_METHOD_1         1  '1 positional argument'
             1908  POP_TOP          

 L. 467      1910  LOAD_FAST                'tmpsocket'
             1912  LOAD_METHOD              getsockname
             1914  CALL_METHOD_0         0  '0 positional arguments'
             1916  LOAD_CONST               0
             1918  BINARY_SUBSCR    
             1920  LOAD_FAST                'options'
             1922  STORE_ATTR               externalip

 L. 468      1924  LOAD_FAST                'tmpsocket'
             1926  LOAD_METHOD              close
             1928  CALL_METHOD_0         0  '0 positional arguments'
             1930  POP_TOP          
           1932_0  COME_FROM          1880  '1880'

 L. 469      1932  LOAD_GLOBAL              DrinkOrSip

 L. 470      1934  LOAD_FAST                'scaniter'

 L. 471      1936  LOAD_FAST                'options'
             1938  LOAD_ATTR                selecttime

 L. 472      1940  LOAD_FAST                'options'
             1942  LOAD_ATTR                enablecompact

 L. 473      1944  LOAD_FAST                'options'
             1946  LOAD_ATTR                localport

 L. 474      1948  LOAD_FAST                'options'
             1950  LOAD_ATTR                externalip

 L. 475      1952  LOAD_FAST                'options'
             1954  LOAD_ATTR                bindingip

 L. 476      1956  LOAD_FAST                'exportpath'

 L. 477      1958  LOAD_FAST                'options'
             1960  LOAD_ATTR                extension

 L. 478      1962  LOAD_FAST                'options'
             1964  LOAD_ATTR                printdebug

 L. 479      1966  LOAD_FAST                'options'
             1968  LOAD_ATTR                first

 L. 480      1970  LOAD_FAST                'options'
             1972  LOAD_ATTR                fromname
             1974  LOAD_CONST               ('selecttime', 'compact', 'localport', 'externalip', 'bindingip', 'sessionpath', 'extension', 'printdebug', 'first', 'fromname')
             1976  CALL_FUNCTION_KW_11    11  '11 total positional and keyword args'
             1978  STORE_FAST               'sipvicious'

 L. 482      1980  LOAD_GLOBAL              datetime
             1982  LOAD_METHOD              now
             1984  CALL_METHOD_0         0  '0 positional arguments'
             1986  STORE_FAST               'start_time'

 L. 483      1988  LOAD_GLOBAL              logging
             1990  LOAD_METHOD              info
             1992  LOAD_STR                 'start your engines'
             1994  CALL_METHOD_1         1  '1 positional argument'
             1996  POP_TOP          

 L. 484      1998  SETUP_EXCEPT       2118  'to 2118'

 L. 485      2000  LOAD_FAST                'options'
             2002  LOAD_ATTR                crashandburn
         2004_2006  POP_JUMP_IF_FALSE  2012  'to 2012'

 L. 486      2008  LOAD_GLOBAL              ValueError
             2010  RAISE_VARARGS_1       1  'exception instance'
           2012_0  COME_FROM          2004  '2004'

 L. 487      2012  SETUP_EXCEPT       2026  'to 2026'

 L. 488      2014  LOAD_FAST                'sipvicious'
             2016  LOAD_METHOD              start
             2018  CALL_METHOD_0         0  '0 positional arguments'
             2020  POP_TOP          
             2022  POP_BLOCK        
             2024  JUMP_FORWARD       2080  'to 2080'
           2026_0  COME_FROM_EXCEPT   2012  '2012'

 L. 489      2026  DUP_TOP          
             2028  LOAD_GLOBAL              AssertionError
             2030  COMPARE_OP               exception-match
         2032_2034  POP_JUMP_IF_FALSE  2078  'to 2078'
             2036  POP_TOP          
             2038  STORE_FAST               'err'
             2040  POP_TOP          
             2042  SETUP_FINALLY      2066  'to 2066'

 L. 490      2044  LOAD_GLOBAL              logging
             2046  LOAD_METHOD              critical
             2048  LOAD_FAST                'err'
             2050  CALL_METHOD_1         1  '1 positional argument'
             2052  POP_TOP          

 L. 491      2054  LOAD_GLOBAL              exit
             2056  LOAD_CONST               1
             2058  CALL_FUNCTION_1       1  '1 positional argument'
             2060  POP_TOP          
             2062  POP_BLOCK        
             2064  LOAD_CONST               None
           2066_0  COME_FROM_FINALLY  2042  '2042'
             2066  LOAD_CONST               None
             2068  STORE_FAST               'err'
             2070  DELETE_FAST              'err'
             2072  END_FINALLY      
             2074  POP_EXCEPT       
             2076  JUMP_FORWARD       2080  'to 2080'
           2078_0  COME_FROM          2032  '2032'
             2078  END_FINALLY      
           2080_0  COME_FROM          2076  '2076'
           2080_1  COME_FROM          2024  '2024'

 L. 492      2080  LOAD_FAST                'exportpath'
             2082  LOAD_CONST               None
             2084  COMPARE_OP               is-not
         2086_2088  POP_JUMP_IF_FALSE  2114  'to 2114'

 L. 493      2090  LOAD_GLOBAL              open
             2092  LOAD_GLOBAL              os
             2094  LOAD_ATTR                path
             2096  LOAD_METHOD              join
             2098  LOAD_FAST                'exportpath'
             2100  LOAD_STR                 'closed'
             2102  CALL_METHOD_2         2  '2 positional arguments'
             2104  LOAD_STR                 'w'
             2106  CALL_FUNCTION_2       2  '2 positional arguments'
             2108  LOAD_METHOD              close
             2110  CALL_METHOD_0         0  '0 positional arguments'
             2112  POP_TOP          
           2114_0  COME_FROM          2086  '2086'
             2114  POP_BLOCK        
             2116  JUMP_FORWARD       2236  'to 2236'
           2118_0  COME_FROM_EXCEPT   1998  '1998'

 L. 494      2118  DUP_TOP          
             2120  LOAD_GLOBAL              KeyboardInterrupt
             2122  COMPARE_OP               exception-match
         2124_2126  POP_JUMP_IF_FALSE  2148  'to 2148'
             2128  POP_TOP          
             2130  POP_TOP          
             2132  POP_TOP          

 L. 495      2134  LOAD_GLOBAL              logging
             2136  LOAD_METHOD              warn
             2138  LOAD_STR                 'caught your control^c - quiting'
             2140  CALL_METHOD_1         1  '1 positional argument'
             2142  POP_TOP          

 L. 496      2144  POP_EXCEPT       
             2146  JUMP_FORWARD       2236  'to 2236'
           2148_0  COME_FROM          2124  '2124'

 L. 497      2148  DUP_TOP          
             2150  LOAD_GLOBAL              Exception
             2152  COMPARE_OP               exception-match
         2154_2156  POP_JUMP_IF_FALSE  2234  'to 2234'
             2158  POP_TOP          
             2160  STORE_FAST               'err'
             2162  POP_TOP          
             2164  SETUP_FINALLY      2222  'to 2222'

 L. 498      2166  LOAD_FAST                'options'
             2168  LOAD_ATTR                reportBack
         2170_2172  POP_JUMP_IF_FALSE  2198  'to 2198'

 L. 499      2174  LOAD_GLOBAL              logging
             2176  LOAD_METHOD              critical
             2178  LOAD_STR                 'Got unhandled exception : sending report to author'
             2180  CALL_METHOD_1         1  '1 positional argument'
             2182  POP_TOP          

 L. 500      2184  LOAD_GLOBAL              reportBugToAuthor
             2186  LOAD_GLOBAL              traceback
             2188  LOAD_METHOD              format_exc
             2190  CALL_METHOD_0         0  '0 positional arguments'
             2192  CALL_FUNCTION_1       1  '1 positional argument'
             2194  POP_TOP          
             2196  JUMP_FORWARD       2208  'to 2208'
           2198_0  COME_FROM          2170  '2170'

 L. 502      2198  LOAD_GLOBAL              logging
             2200  LOAD_METHOD              critical
             2202  LOAD_STR                 'Unhandled exception - please run same command with the -R option to send me an automated report'
             2204  CALL_METHOD_1         1  '1 positional argument'
             2206  POP_TOP          
           2208_0  COME_FROM          2196  '2196'

 L. 504      2208  LOAD_GLOBAL              logging
             2210  LOAD_METHOD              exception
             2212  LOAD_STR                 'Exception'
             2214  CALL_METHOD_1         1  '1 positional argument'
             2216  POP_TOP          
             2218  POP_BLOCK        
             2220  LOAD_CONST               None
           2222_0  COME_FROM_FINALLY  2164  '2164'
             2222  LOAD_CONST               None
             2224  STORE_FAST               'err'
             2226  DELETE_FAST              'err'
             2228  END_FINALLY      
             2230  POP_EXCEPT       
             2232  JUMP_FORWARD       2236  'to 2236'
           2234_0  COME_FROM          2154  '2154'
             2234  END_FINALLY      
           2236_0  COME_FROM          2232  '2232'
           2236_1  COME_FROM          2146  '2146'
           2236_2  COME_FROM          2116  '2116'

 L. 505      2236  LOAD_FAST                'options'
             2238  LOAD_ATTR                save
             2240  LOAD_CONST               None
             2242  COMPARE_OP               is-not
         2244_2246  POP_JUMP_IF_FALSE  2388  'to 2388'
             2248  LOAD_FAST                'sipvicious'
             2250  LOAD_ATTR                nextip
             2252  LOAD_CONST               None
             2254  COMPARE_OP               is-not
         2256_2258  POP_JUMP_IF_FALSE  2388  'to 2388'
             2260  LOAD_FAST                'options'
             2262  LOAD_ATTR                randomize
             2264  LOAD_CONST               False
             2266  COMPARE_OP               is
         2268_2270  POP_JUMP_IF_FALSE  2388  'to 2388'
             2272  LOAD_FAST                'options'
             2274  LOAD_ATTR                randomscan
             2276  LOAD_CONST               False
             2278  COMPARE_OP               is
         2280_2282  POP_JUMP_IF_FALSE  2388  'to 2388'

 L. 506      2284  LOAD_GLOBAL              os
             2286  LOAD_ATTR                path
             2288  LOAD_METHOD              join
             2290  LOAD_FAST                'exportpath'
             2292  LOAD_STR                 'lastip.pkl'
             2294  CALL_METHOD_2         2  '2 positional arguments'
             2296  STORE_FAST               'lastipdst'

 L. 507      2298  LOAD_GLOBAL              logging
             2300  LOAD_METHOD              debug
             2302  LOAD_STR                 'saving state to %s'
             2304  LOAD_FAST                'lastipdst'
             2306  BINARY_MODULO    
             2308  CALL_METHOD_1         1  '1 positional argument'
             2310  POP_TOP          

 L. 508      2312  SETUP_EXCEPT       2350  'to 2350'

 L. 509      2314  LOAD_GLOBAL              open
             2316  LOAD_FAST                'lastipdst'
             2318  LOAD_STR                 'wb+'
             2320  CALL_FUNCTION_2       2  '2 positional arguments'
             2322  STORE_FAST               'f'

 L. 510      2324  LOAD_GLOBAL              pickle
             2326  LOAD_METHOD              dump
             2328  LOAD_FAST                'sipvicious'
             2330  LOAD_ATTR                nextip
             2332  LOAD_FAST                'f'
             2334  CALL_METHOD_2         2  '2 positional arguments'
             2336  POP_TOP          

 L. 511      2338  LOAD_FAST                'f'
             2340  LOAD_METHOD              close
             2342  CALL_METHOD_0         0  '0 positional arguments'
             2344  POP_TOP          
             2346  POP_BLOCK        
             2348  JUMP_FORWARD       2386  'to 2386'
           2350_0  COME_FROM_EXCEPT   2312  '2312'

 L. 512      2350  DUP_TOP          
             2352  LOAD_GLOBAL              OSError
             2354  COMPARE_OP               exception-match
         2356_2358  POP_JUMP_IF_FALSE  2384  'to 2384'
             2360  POP_TOP          
             2362  POP_TOP          
             2364  POP_TOP          

 L. 513      2366  LOAD_GLOBAL              logging
             2368  LOAD_METHOD              warn
             2370  LOAD_STR                 'Could not save state to %s'
             2372  LOAD_FAST                'lastipdst'
             2374  BINARY_MODULO    
             2376  CALL_METHOD_1         1  '1 positional argument'
             2378  POP_TOP          
             2380  POP_EXCEPT       
             2382  JUMP_FORWARD       2386  'to 2386'
           2384_0  COME_FROM          2356  '2356'
             2384  END_FINALLY      
           2386_0  COME_FROM          2382  '2382'
           2386_1  COME_FROM          2348  '2348'
             2386  JUMP_FORWARD       2476  'to 2476'
           2388_0  COME_FROM          2280  '2280'
           2388_1  COME_FROM          2268  '2268'
           2388_2  COME_FROM          2256  '2256'
           2388_3  COME_FROM          2244  '2244'

 L. 514      2388  LOAD_FAST                'options'
             2390  LOAD_ATTR                save
             2392  LOAD_CONST               None
             2394  COMPARE_OP               is
         2396_2398  POP_JUMP_IF_FALSE  2476  'to 2476'

 L. 515      2400  LOAD_FAST                'scanrandomstore'
             2402  LOAD_CONST               None
             2404  COMPARE_OP               is-not
         2406_2408  POP_JUMP_IF_FALSE  2476  'to 2476'

 L. 517      2410  SETUP_EXCEPT       2440  'to 2440'

 L. 518      2412  LOAD_GLOBAL              logging
             2414  LOAD_METHOD              debug
             2416  LOAD_STR                 'removing %s'
             2418  LOAD_FAST                'scanrandomstore'
             2420  BINARY_MODULO    
             2422  CALL_METHOD_1         1  '1 positional argument'
             2424  POP_TOP          

 L. 519      2426  LOAD_GLOBAL              os
             2428  LOAD_METHOD              unlink
             2430  LOAD_FAST                'scanrandomstore'
             2432  CALL_METHOD_1         1  '1 positional argument'
             2434  POP_TOP          
             2436  POP_BLOCK        
             2438  JUMP_FORWARD       2476  'to 2476'
           2440_0  COME_FROM_EXCEPT   2410  '2410'

 L. 520      2440  DUP_TOP          
             2442  LOAD_GLOBAL              OSError
             2444  COMPARE_OP               exception-match
         2446_2448  POP_JUMP_IF_FALSE  2474  'to 2474'
             2450  POP_TOP          
             2452  POP_TOP          
             2454  POP_TOP          

 L. 521      2456  LOAD_GLOBAL              logging
             2458  LOAD_METHOD              warn
             2460  LOAD_STR                 'could not remove %s'
             2462  LOAD_FAST                'scanrandomstore'
             2464  BINARY_MODULO    
             2466  CALL_METHOD_1         1  '1 positional argument'
             2468  POP_TOP          

 L. 522      2470  POP_EXCEPT       
             2472  JUMP_FORWARD       2476  'to 2476'
           2474_0  COME_FROM          2446  '2446'
             2474  END_FINALLY      
           2476_0  COME_FROM          2472  '2472'
           2476_1  COME_FROM          2438  '2438'
           2476_2  COME_FROM          2406  '2406'
           2476_3  COME_FROM          2396  '2396'
           2476_4  COME_FROM          2386  '2386'

 L. 524      2476  LOAD_FAST                'options'
             2478  LOAD_ATTR                quiet
         2480_2482  POP_JUMP_IF_TRUE   2746  'to 2746'

 L. 525      2484  LOAD_GLOBAL              len
             2486  LOAD_FAST                'sipvicious'
             2488  LOAD_ATTR                resultua
             2490  CALL_FUNCTION_1       1  '1 positional argument'
             2492  STORE_FAST               'lenres'

 L. 526      2494  LOAD_FAST                'lenres'
             2496  LOAD_CONST               0
             2498  COMPARE_OP               >
         2500_2502  POP_JUMP_IF_FALSE  2736  'to 2736'

 L. 527      2504  LOAD_GLOBAL              logging
             2506  LOAD_METHOD              info
             2508  LOAD_STR                 'we have %s devices'
             2510  LOAD_FAST                'lenres'
             2512  BINARY_MODULO    
             2514  CALL_METHOD_1         1  '1 positional argument'
             2516  POP_TOP          

 L. 528      2518  LOAD_FAST                'lenres'
             2520  LOAD_CONST               400
             2522  COMPARE_OP               <
         2524_2526  POP_JUMP_IF_FALSE  2540  'to 2540'
             2528  LOAD_FAST                'options'
             2530  LOAD_ATTR                save
             2532  LOAD_CONST               None
             2534  COMPARE_OP               is-not
         2536_2538  POP_JUMP_IF_TRUE   2552  'to 2552'
           2540_0  COME_FROM          2524  '2524'
             2540  LOAD_FAST                'options'
             2542  LOAD_ATTR                save
             2544  LOAD_CONST               None
             2546  COMPARE_OP               is
         2548_2550  POP_JUMP_IF_FALSE  2724  'to 2724'
           2552_0  COME_FROM          2536  '2536'

 L. 529      2552  LOAD_CONST               60
             2554  STORE_FAST               'width'

 L. 530      2556  LOAD_CONST               ('SIP Device', 'User Agent', 'Fingerprint')
             2558  STORE_FAST               'labels'

 L. 531      2560  LOAD_GLOBAL              list
             2562  CALL_FUNCTION_0       0  '0 positional arguments'
             2564  STORE_FAST               'rows'

 L. 532      2566  SETUP_EXCEPT       2634  'to 2634'

 L. 533      2568  SETUP_LOOP         2630  'to 2630'
             2570  LOAD_FAST                'sipvicious'
             2572  LOAD_ATTR                resultua
             2574  LOAD_METHOD              keys
             2576  CALL_METHOD_0         0  '0 positional arguments'
             2578  GET_ITER         
             2580  FOR_ITER           2628  'to 2628'
             2582  STORE_FAST               'k'

 L. 534      2584  LOAD_FAST                'rows'
             2586  LOAD_METHOD              append
             2588  LOAD_FAST                'k'
             2590  LOAD_METHOD              decode
             2592  CALL_METHOD_0         0  '0 positional arguments'
             2594  LOAD_FAST                'sipvicious'
             2596  LOAD_ATTR                resultua
             2598  LOAD_FAST                'k'
             2600  BINARY_SUBSCR    
             2602  LOAD_METHOD              decode
             2604  CALL_METHOD_0         0  '0 positional arguments'
             2606  LOAD_FAST                'sipvicious'
             2608  LOAD_ATTR                resultfp
             2610  LOAD_FAST                'k'
             2612  BINARY_SUBSCR    
             2614  LOAD_METHOD              decode
             2616  CALL_METHOD_0         0  '0 positional arguments'
             2618  BUILD_TUPLE_3         3 
             2620  CALL_METHOD_1         1  '1 positional argument'
             2622  POP_TOP          
         2624_2626  JUMP_BACK          2580  'to 2580'
             2628  POP_BLOCK        
           2630_0  COME_FROM_LOOP     2568  '2568'
             2630  POP_BLOCK        
             2632  JUMP_FORWARD       2706  'to 2706'
           2634_0  COME_FROM_EXCEPT   2566  '2566'

 L. 535      2634  DUP_TOP          
             2636  LOAD_GLOBAL              AttributeError
             2638  COMPARE_OP               exception-match
         2640_2642  POP_JUMP_IF_FALSE  2704  'to 2704'
             2644  POP_TOP          
             2646  POP_TOP          
             2648  POP_TOP          

 L. 536      2650  SETUP_LOOP         2700  'to 2700'
             2652  LOAD_FAST                'sipvicious'
             2654  LOAD_ATTR                resultua
             2656  LOAD_METHOD              keys
             2658  CALL_METHOD_0         0  '0 positional arguments'
             2660  GET_ITER         
             2662  FOR_ITER           2698  'to 2698'
             2664  STORE_FAST               'k'

 L. 537      2666  LOAD_FAST                'rows'
             2668  LOAD_METHOD              append
             2670  LOAD_FAST                'k'
             2672  LOAD_FAST                'sipvicious'
             2674  LOAD_ATTR                resultua
             2676  LOAD_FAST                'k'
             2678  BINARY_SUBSCR    
             2680  LOAD_FAST                'sipvicious'
             2682  LOAD_ATTR                resultfp
             2684  LOAD_FAST                'k'
             2686  BINARY_SUBSCR    
             2688  BUILD_TUPLE_3         3 
             2690  CALL_METHOD_1         1  '1 positional argument'
             2692  POP_TOP          
         2694_2696  JUMP_BACK          2662  'to 2662'
             2698  POP_BLOCK        
           2700_0  COME_FROM_LOOP     2650  '2650'
             2700  POP_EXCEPT       
             2702  JUMP_FORWARD       2706  'to 2706'
           2704_0  COME_FROM          2640  '2640'
             2704  END_FINALLY      
           2706_0  COME_FROM          2702  '2702'
           2706_1  COME_FROM          2632  '2632'

 L. 538      2706  LOAD_GLOBAL              print
             2708  LOAD_GLOBAL              to_string
             2710  LOAD_FAST                'rows'
             2712  LOAD_FAST                'labels'
             2714  LOAD_CONST               ('header',)
             2716  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             2718  CALL_FUNCTION_1       1  '1 positional argument'
             2720  POP_TOP          
             2722  JUMP_FORWARD       2734  'to 2734'
           2724_0  COME_FROM          2548  '2548'

 L. 540      2724  LOAD_GLOBAL              logging
             2726  LOAD_METHOD              warn
             2728  LOAD_STR                 'too many to print - use svreport for this'
             2730  CALL_METHOD_1         1  '1 positional argument'
             2732  POP_TOP          
           2734_0  COME_FROM          2722  '2722'
             2734  JUMP_FORWARD       2746  'to 2746'
           2736_0  COME_FROM          2500  '2500'

 L. 542      2736  LOAD_GLOBAL              logging
             2738  LOAD_METHOD              warn
             2740  LOAD_STR                 'found nothing'
             2742  CALL_METHOD_1         1  '1 positional argument'
             2744  POP_TOP          
           2746_0  COME_FROM          2734  '2734'
           2746_1  COME_FROM          2480  '2480'

 L. 543      2746  LOAD_GLOBAL              datetime
             2748  LOAD_METHOD              now
             2750  CALL_METHOD_0         0  '0 positional arguments'
             2752  STORE_FAST               'end_time'

 L. 544      2754  LOAD_FAST                'end_time'
             2756  LOAD_FAST                'start_time'
             2758  BINARY_SUBTRACT  
             2760  STORE_FAST               'total_time'

 L. 545      2762  LOAD_GLOBAL              logging
             2764  LOAD_METHOD              info
             2766  LOAD_STR                 'Total time: %s'
             2768  LOAD_FAST                'total_time'
             2770  BINARY_MODULO    
             2772  CALL_METHOD_1         1  '1 positional argument'
             2774  POP_TOP          

Parse error at or near `COME_FROM' instruction at offset 1600_0


if __name__ == '__main__':
    main()