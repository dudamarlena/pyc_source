# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sipvicious/libs/svhelper.py
# Compiled at: 2020-03-05 23:56:50
# Size of source mod 2**32: 37686 bytes
__author__ = 'Sandro Gauci <sandro@enablesecurity.com>'
__version__ = '0.3.0'
import re, sys, uuid, base64, os, dbm, socket, random, struct, shutil, logging, optparse
from urllib.parse import quote
from random import getrandbits
from urllib.request import urlopen
from urllib.error import URLError
from urllib.parse import urlencode
from binascii import b2a_hex, a2b_hex
from binascii import Error as b2aerr
from .pptable import to_string
if sys.hexversion < 50659328:
    sys.stderr.write('Please update to python 3.5 or greater to run Sipvicious\r\n')
    sys.exit(1)

def standardoptions(parser):
    parser.add_option('-v', '--verbose', dest='verbose', action='count', help='Increase verbosity')
    parser.add_option('-q', '--quiet', dest='quiet', action='store_true', default=False,
      help='Quiet mode')
    parser.add_option('-p', '--port', dest='port', default='5060', help='Destination port or port ranges of the SIP device - eg -p5060,5061,8000-8100',
      metavar='PORT')
    parser.add_option('-P', '--localport', dest='localport', default=5060, type='int', help='Source port for our packets',
      metavar='PORT')
    parser.add_option('-x', '--externalip', dest='externalip', help='IP Address to use as the external ip. Specify this if you have multiple interfaces or if you are behind NAT',
      metavar='IP')
    parser.add_option('-b', '--bindingip', dest='bindingip', default='0.0.0.0', help='By default we bind to all interfaces. This option overrides that and binds to the specified ip address')
    parser.add_option('-t', '--timeout', dest='selecttime', type='float', default=0.005, help="This option allows you to trottle the speed at which packets are sent. Change this if you're losing packets. For example try 0.5.",
      metavar='SELECTTIME')
    parser.add_option('-R', '--reportback', dest='reportBack', default=False, action='store_true', help='Send the author an exception traceback. Currently sends the command line parameters and the traceback')
    parser.add_option('-A', '--autogetip', dest='autogetip', default=False, action='store_true', help='Automatically get the current IP address. This is useful when you are not getting any responses back due to SIPVicious not resolving your local IP.')
    return parser


def standardscanneroptions(parser):
    parser.add_option('-s', '--save', dest='save', metavar='NAME', help='save the session. Has the benefit of allowing you to resume a previous scan and allows you to export scans')
    parser.add_option('--resume', dest='resume', help='resume a previous scan', metavar='NAME')
    parser.add_option('-c', '--enablecompact', dest='enablecompact', default=False, action='store_true', help='enable compact mode. Makes packets smaller but possibly less compatible')
    return parser


def calcloglevel(options):
    logginglevel = 30
    if options.verbose is not None:
        if options.verbose >= 3:
            logginglevel = 10
        else:
            logginglevel = 30 - options.verbose * 10
    if options.quiet:
        logginglevel = 50
    return logginglevel


def bindto(bindingip, startport, s):
    log = logging.getLogger('bindto')
    localport = startport
    log.debug('binding to %s:%s' % (bindingip, localport))
    while localport > 65535:
        log.critical('Could not bind to any port')
        return
        try:
            s.bind((bindingip, localport))
            break
        except socket.error:
            log.debug('could not bind to %s' % localport)
            localport += 1

    if startport != localport:
        log.warn('could not bind to %s:%s - some process might already be listening on this port. Listening on port %s instead' % (
         bindingip, startport, localport))
        log.info('Make use of the -P option to specify a port to bind to yourself')
    return (
     localport, s)


def getRange(rangestr):
    _tmp1 = rangestr.split(',')
    numericrange = list()
    for _tmp2 in _tmp1:
        _tmp3 = _tmp2.split('-', 1)
        if len(_tmp3) > 1:
            if not _tmp3[0].isdigit():
                if not _tmp3[1].isdigit():
                    raise ValueError('the ranges need to be digits')
            startport, endport = list(map(int, [_tmp3[0], _tmp3[1]]))
            endport += 1
            numericrange.append(range(startport, endport))
        else:
            if not _tmp3[0].isdigit():
                raise ValueError('the ranges need to be digits')
            singleport = int(_tmp3[0])
            numericrange.append(anotherxrange(singleport, singleport + 1))

    return numericrange


def numericbrute(rangelist, zeropadding=0, template=None, defaults=False, staticbrute=[]):
    """numericbrute gives a yield generator. accepts either zeropadding or template as optional argument"""
    for statictry in staticbrute:
        yield statictry

    if defaults:
        for i in range(1000, 9999, 100):
            yield '%04i' % i

        for i in range(1001, 9999, 100):
            yield '%04i' % i

        for i in range(0, 9):
            for l in range(1, 8):
                yield '%s' % i * l

        for i in range(100, 999):
            yield '%s' % i

        for i in range(10000, 99999, 100):
            yield '%04i' % i

        for i in range(10001, 99999, 100):
            yield '%04i' % i

        for i in ('1234', '2345', '3456', '4567', '5678', '6789', '7890', '0123'):
            yield i

        for i in ('12345', '23456', '34567', '45678', '56789', '67890', '01234'):
            yield i

    elif zeropadding > 0:
        format = '%%0%su' % zeropadding
    else:
        if template is not None:
            format = template
        else:
            format = '%u'
    format % 1
    for x in rangelist:
        for y in x:
            r = format % y
            yield r


def dictionaryattack(dictionaryfile):
    while True:
        r = dictionaryfile.readline()
        if len(r) == 0:
            break
        yield r.strip()

    dictionaryfile.close()


class genericbrute:
    pass


def getNonce(pkt):
    nonceRE = 'nonce="(.+?)"'
    _tmp = re.findall(nonceRE, pkt)
    if _tmp is not None:
        if len(_tmp) > 0:
            return _tmp[0]


def getOpaque(pkt):
    nonceRE = 'opaque="(.+?)"'
    _tmp = re.findall(nonceRE, pkt)
    if _tmp is not None:
        if len(_tmp) > 0:
            return _tmp[0]


def getAlgorithm(pkt):
    nonceRE = 'algorithm=(.+?)[,\r]'
    _tmp = re.findall(nonceRE, pkt)
    if _tmp is not None:
        if len(_tmp) > 0:
            return _tmp[0].lower()


def getQop(pkt):
    nonceRE = 'qop="(.+?)"'
    _tmp = re.findall(nonceRE, pkt)
    if _tmp is not None:
        if len(_tmp) > 0:
            return _tmp[0]


def getRealm(pkt):
    nonceRE = 'realm="(.+?)"'
    _tmp = re.findall(nonceRE, pkt)
    if _tmp is not None:
        if len(_tmp) > 0:
            return _tmp[0]


def getCID(pkt):
    cidRE = 'Call-ID: ([:a-zA-Z0-9]+)'
    _tmp = re.findall(cidRE, pkt, re.I)
    if _tmp is not None:
        if len(_tmp) > 0:
            return _tmp[0]


def mysendto(sock, data, dst):
    while data:
        bytes_sent = sock.sendto(bytes(data[:8192], 'utf-8'), dst)
        data = data[bytes_sent:]


def parseSDP(buff):
    r = dict()
    for line in buff.splitlines():
        _tmp = line.split('=', 1)
        if len(_tmp) == 2:
            k, v = _tmp
            if k not in r:
                r[k] = list()
            r[k].append(v)

    return r


def getAudioPort(sdp):
    if 'm' in sdp:
        for media in sdp['m']:
            if media.startswith('audio'):
                mediasplit = media.split()
                if len(mediasplit) > 2:
                    port = mediasplit[1]
                    return port


def getAudioIP(sdp):
    if 'c' in sdp:
        for connect in sdp['c']:
            if connect.startswith('IN IP4'):
                connectsplit = connect.split()
                if len(connectsplit) > 2:
                    ip = connectsplit[2]
                    return ip


def getSDP(buff):
    sip = parseHeader(buff)
    if 'body' in sip:
        body = sip['body']
        sdp = parseSDP(body)
        return sdp


def getAudioIPFromBuff(buff):
    sdp = getSDP(buff)
    if sdp is not None:
        return getAudioIP(sdp)


def getAudioPortFromBuff(buff):
    sdp = getSDP(buff)
    if sdp is not None:
        return getAudioPort(sdp)


def parseHeader(buff, type='response'):
    SEP = '\r\n\r\n'
    HeadersSEP = '\r*\n(?![\t ])'
    log = logging.getLogger('parseHeader')
    if SEP in buff:
        header, body = buff.split(SEP, 1)
    else:
        header = buff
        body = ''
    headerlines = re.split(HeadersSEP, header)
    if len(headerlines) > 1:
        r = dict()
        if type == 'response':
            _t = headerlines[0].split(' ', 2)
            if len(_t) == 3:
                _, _code, _ = _t
            else:
                log.warn('Could not parse the first header line: %s' % _t.__repr__())
                return r
                try:
                    r['code'] = int(_code)
                except ValueError:
                    return r

        else:
            if type == 'request':
                _t = headerlines[0].split(' ', 2)
            else:
                log.warn('Could not parse the first header line: %s' % _t.__repr__())
                return r
        r['headers'] = dict()
        for headerline in headerlines[1:]:
            SEP = ':'
            if SEP in headerline:
                tmpname, tmpval = headerline.split(SEP, 1)
                name = tmpname.lower().strip()
                val = list(map(lambda x: x.strip(), tmpval.split(',')))
            else:
                name, val = headerline.lower(), None
            r['headers'][name] = val

        r['body'] = body
        return r


def fingerPrint(request, src=None, dst=None):
    server = dict()
    if 'headers' in request:
        header = request['headers']
        if src is not None and dst is not None:
            server['ip'] = src[0]
            server['srcport'] = src[1]
            if server['srcport'] == dst[1]:
                server['behindnat'] = False
    else:
        server['behindnat'] = True
    if 'user-agent' in header:
        server['name'] = header['user-agent']
        server['uatype'] = 'uac'
    if 'server' in header:
        server['name'] = header['server']
        server['uatype'] = 'uas'
    if 'contact' in header:
        m = re.match('<sip:(.*?)>', header['contact'][0])
        if m:
            server['contactip'] = m.group(1)
    if 'supported' in header:
        server['supported'] = header['supported']
    if 'accept-language' in header:
        server['accept-language'] = header['accept-language']
    if 'allow-events' in header:
        server['allow-events'] = header['allow-events']
    if 'allow' in header:
        server['allow'] = header['allow']
    return server


def fingerPrintPacket(buff, src=None):
    header = parseHeader(buff)
    if header is not None:
        return fingerPrint(header, src)


def getCredentials(buff):
    data = getTag(buff)
    if data is None:
        return
    userpass = data.split(b':')
    if len(userpass) > 0:
        return userpass


def getTag(buff):
    tagRE = '(From|f): .*?\\;\\s*tag=([=+/\\.:a-zA-Z0-9_]+)'
    _tmp = re.findall(tagRE, buff)
    if _tmp is not None:
        if len(_tmp) > 0:
            _tmp2 = _tmp[0][1]
            try:
                _tmp2 = a2b_hex(_tmp2.strip())
            except (TypeError, b2aerr):
                return
            else:
                if _tmp2.find(b'\x01') > 0:
                    try:
                        c, _ = _tmp2.split(b'\x01')
                    except ValueError:
                        c = 'svcrash detected'

                else:
                    c = _tmp2
                return c


def createTag(data):
    rnd = getrandbits(32)
    return b2a_hex(str(data).encode('utf-8') + b'\x01' + str(rnd).encode('utf-8'))


def getToTag(buff):
    tagRE = '(To|t): .*?\\;\\s*tag=([=+/\\.:a-zA-Z0-9_]+)'
    _tmp = re.findall(tagRE, buff)
    if _tmp is not None:
        if len(_tmp) > 0:
            _tmp2 = _tmp[0][1]
            return _tmp2


def challengeResponse(auth, method, uri):
    try:
        from hashlib import md5
    except ImportError:
        import md5 as md5sum
        md5 = md5sum.new

    username = auth['username']
    realm = auth['realm']
    passwd = auth['password']
    nonce = auth['nonce']
    opaque = auth['opaque']
    algorithm = auth['algorithm']
    cnonce = ''
    qop = None
    if auth['qop'] != None:
        qop = auth['qop'].split(',')[0]
    else:
        result = 'Digest username="%s",realm="%s",nonce="%s",uri="%s"' % (
         username, realm, nonce, uri)
        if algorithm == 'md5-sess' or qop == 'auth':
            cnonce = uuid.uuid4().hex
            nonceCount = '%08d' % auth['noncecount']
            result += ',cnonce="%s",nc=%s' % (cnonce, nonceCount)
        elif algorithm is None or algorithm == 'md5':
            ha1 = md5(('%s:%s:%s' % (username, realm, passwd)).encode('utf-8')).hexdigest()
            result += ',algorithm=MD5'
        else:
            if auth['algorithm'] == 'md5-sess':
                ha1 = md5((md5(('%s:%s:%s' % (username, realm, passwd)).encode('utf-8')).hexdigest() + ':' + nonce + ':' + cnonce).encode('utf-8')).hexdigest()
                result += ',algorithm=MD5-sess'
            else:
                print('Unknown algorithm: %s' % auth['algorithm'])
        if not qop is None:
            if qop == 'auth':
                ha2 = md5(('%s:%s' % (method, uri)).encode('utf-8')).hexdigest()
                result += ',qop=auth'
            if qop == 'auth-int':
                print('auth-int is not supported')
            if qop == 'auth':
                res = md5((ha1 + ':' + nonce + ':' + nonceCount + ':' + cnonce + ':' + qop + ':' + ha2).encode('utf-8')).hexdigest()
        else:
            res = md5(('%s:%s:%s' % (ha1, nonce, ha2)).encode('utf-8')).hexdigest()
    result += ',response="%s"' % res
    if opaque is not None:
        if opaque != '':
            result += ',opaque="%s"' % opaque
    return result


def makeRedirect(previousHeaders, rediraddr):
    response = 'SIP/2.0 301 Moved Permanently\r\n'
    superheaders = dict()
    headers = dict()
    superheaders['Via'] = ' '.join(previousHeaders['headers']['via'])
    headers['Contact'] = '<%s>' % rediraddr
    headers['To'] = ' '.join(previousHeaders['headers']['to'])
    headers['From'] = ' '.join(previousHeaders['headers']['from'])
    headers['Call-ID'] = ' '.join(previousHeaders['headers']['call-id'])
    headers['CSeq'] = ' '.join(previousHeaders['headers']['cseq'])
    r = response
    for h in superheaders.items():
        r += '%s: %s\r\n' % h

    for h in headers.items():
        r += '%s: %s\r\n' % h

    r += '\r\n'
    return r


def makeRequest(method, fromaddr, toaddr, dsthost, port, callid, srchost='', branchunique=None, cseq=1, auth=None, localtag=None, compact=False, contact='sip:123@1.1.1.1', accept='application/sdp', contentlength=None, localport=5060, extension=None, contenttype=None, body='', useragent='friendly-scanner', requesturi=None):
    """makeRequest builds up a SIP request
    method - OPTIONS / INVITE etc
    toaddr = to address
    dsthost = destination host
    port = destination port
    callid = callerid
    srchost = source host
    """
    if extension is None or method == 'REGISTER':
        uri = 'sip:%s' % dsthost
    else:
        uri = 'sip:%s@%s' % (extension, dsthost)
    if branchunique is None:
        branchunique = '%s' % random.getrandbits(32)
    headers = dict()
    finalheaders = dict()
    superheaders = dict()
    if method == 'ACK':
        localtag = None
    else:
        if compact:
            superheaders['v'] = 'SIP/2.0/UDP %s:%s;branch=z9hG4bK-%s;rport' % (srchost, port, branchunique)
            headers['t'] = toaddr
            headers['f'] = fromaddr
            if localtag is not None:
                headers['f'] += ';tag=%s' % localtag.decode('utf-8')
            headers['i'] = callid
            headers['m'] = contact
        else:
            superheaders['Via'] = 'SIP/2.0/UDP %s:%s;branch=z9hG4bK-%s;rport' % (srchost, localport, branchunique)
            headers['Max-Forwards'] = 70
            headers['To'] = toaddr
            headers['From'] = fromaddr
            headers['User-Agent'] = useragent
            if localtag is not None:
                headers['From'] += ';tag=%s' % localtag.decode('utf-8')
            headers['Call-ID'] = callid
            headers['Contact'] = contact
        headers['CSeq'] = '%s %s' % (cseq, method)
        headers['Max-Forwards'] = 70
        headers['Accept'] = accept
        if contentlength is None:
            headers['Content-Length'] = len(body)
        else:
            headers['Content-Length'] = contentlength
    if contenttype is None:
        if len(body) > 0:
            contenttype = 'application/sdp'
    if contenttype is not None:
        headers['Content-Type'] = contenttype
    elif auth is not None:
        response = challengeResponse(auth, method, uri)
        if auth['proxy']:
            finalheaders['Proxy-Authorization'] = response
        else:
            finalheaders['Authorization'] = response
    r = '%s %s SIP/2.0\r\n' % (method, uri)
    if requesturi is not None:
        r = '%s %s SIP/2.0\r\n' % (method, requesturi)
    for h in superheaders.items():
        r += '%s: %s\r\n' % h

    for h in headers.items():
        r += '%s: %s\r\n' % h

    for h in finalheaders.items():
        r += '%s: %s\r\n' % h

    r += '\r\n'
    r += body
    return r


def reportBugToAuthor(trace):
    log = logging.getLogger('reportBugToAuthor')
    data = str()
    data += 'Command line parameters:\r\n'
    data += str(sys.argv)
    data += '\r\n'
    data += 'version: %s' % __version__
    data += '\r\n'
    data += 'email: <%s>' % input('Your email address (optional): ')
    data += '\r\n'
    data += 'msg: %s' % input('Extra details (optional): ')
    data += '\r\n'
    data += 'python version: \r\n'
    data += '%s\r\n' % sys.version
    data += 'osname: %s' % os.name
    data += '\r\n'
    if os.name == 'posix':
        data += 'uname: %s' % str(os.uname())
        data += '\r\n'
    data += '\r\n\r\n'
    data += 'Trace:\r\n'
    data += str(trace)
    try:
        urlopen('https://comms.enablesecurity.com/hello.php', urlencode({'message': data}).encode('utf-8'))
        log.warn('Thanks for the bug report! We will be working on it soon')
    except URLError as err:
        try:
            log.error(err)
        finally:
            err = None
            del err

    log.warn('Make sure you are running the latest version of SIPVicious                  by running "git pull" in the current directory')


def scanlist(iprange, portranges, methods):
    for ip in iter(iprange):
        for portrange in portranges:
            for port in portrange:
                for method in methods:
                    yield (
                     ip, port, method)


def scanrandom--- This code section failed: ---

 L. 620         0  LOAD_GLOBAL              logging
                2  LOAD_METHOD              getLogger
                4  LOAD_STR                 'scanrandom'
                6  CALL_METHOD_1         1  '1 positional argument'
                8  STORE_FAST               'log'

 L. 621        10  LOAD_STR                 'n'
               12  STORE_FAST               'mode'

 L. 622        14  LOAD_FAST                'resume'
               16  POP_JUMP_IF_FALSE    22  'to 22'

 L. 623        18  LOAD_STR                 'c'
               20  STORE_FAST               'mode'
             22_0  COME_FROM            16  '16'

 L. 624        22  LOAD_GLOBAL              dbm
               24  LOAD_METHOD              open
               26  LOAD_GLOBAL              os
               28  LOAD_ATTR                path
               30  LOAD_METHOD              join

 L. 625        32  LOAD_GLOBAL              os
               34  LOAD_ATTR                path
               36  LOAD_METHOD              expanduser
               38  LOAD_STR                 '~'
               40  CALL_METHOD_1         1  '1 positional argument'
               42  LOAD_FAST                'randomstore'
               44  CALL_METHOD_2         2  '2 positional arguments'
               46  LOAD_FAST                'mode'
               48  CALL_METHOD_2         2  '2 positional arguments'
               50  STORE_FAST               'database'

 L. 626        52  LOAD_CONST               False
               54  STORE_FAST               'dbsyncs'

 L. 627        56  SETUP_EXCEPT         74  'to 74'

 L. 628        58  LOAD_FAST                'database'
               60  LOAD_METHOD              sync
               62  CALL_METHOD_0         0  '0 positional arguments'
               64  POP_TOP          

 L. 629        66  LOAD_CONST               True
               68  STORE_FAST               'dbsyncs'
               70  POP_BLOCK        
               72  JUMP_FORWARD         94  'to 94'
             74_0  COME_FROM_EXCEPT     56  '56'

 L. 630        74  DUP_TOP          
               76  LOAD_GLOBAL              AttributeError
               78  COMPARE_OP               exception-match
               80  POP_JUMP_IF_FALSE    92  'to 92'
               82  POP_TOP          
               84  POP_TOP          
               86  POP_TOP          

 L. 631        88  POP_EXCEPT       
               90  JUMP_FORWARD         94  'to 94'
             92_0  COME_FROM            80  '80'
               92  END_FINALLY      
             94_0  COME_FROM            90  '90'
             94_1  COME_FROM            72  '72'

 L. 632        94  LOAD_CONST               0
               96  STORE_FAST               'ipsleft'

 L. 633        98  SETUP_LOOP          208  'to 208'
              100  LOAD_FAST                'ipranges'
              102  GET_ITER         
              104  FOR_ITER            206  'to 206'
              106  STORE_FAST               'iprange'

 L. 634       108  LOAD_FAST                'iprange'
              110  UNPACK_SEQUENCE_2     2 
              112  STORE_FAST               'startip'
              114  STORE_FAST               'endip'

 L. 635       116  LOAD_FAST                'ipsleft'
              118  LOAD_FAST                'endip'
              120  LOAD_FAST                'startip'
              122  BINARY_SUBTRACT  
              124  LOAD_CONST               1
              126  BINARY_ADD       
              128  INPLACE_ADD      
              130  STORE_FAST               'ipsleft'

 L. 636       132  LOAD_CONST               0
              134  STORE_FAST               'hit'

 L. 637       136  SETUP_LOOP          204  'to 204'
              138  LOAD_FAST                'ipranges'
              140  GET_ITER         
            142_0  COME_FROM           184  '184'
            142_1  COME_FROM           168  '168'
            142_2  COME_FROM           160  '160'
              142  FOR_ITER            202  'to 202'
              144  STORE_FAST               'iprange2'

 L. 638       146  LOAD_FAST                'iprange2'
              148  UNPACK_SEQUENCE_2     2 
              150  STORE_FAST               'startip2'
              152  STORE_FAST               'endip2'

 L. 639       154  LOAD_FAST                'startip'
              156  LOAD_FAST                'startip2'
              158  COMPARE_OP               <=
              160  POP_JUMP_IF_FALSE   142  'to 142'

 L. 640       162  LOAD_FAST                'endip2'
              164  LOAD_FAST                'endip'
              166  COMPARE_OP               <=
              168  POP_JUMP_IF_FALSE   142  'to 142'

 L. 641       170  LOAD_FAST                'hit'
              172  LOAD_CONST               1
              174  INPLACE_ADD      
              176  STORE_FAST               'hit'

 L. 642       178  LOAD_FAST                'hit'
              180  LOAD_CONST               1
              182  COMPARE_OP               >
              184  POP_JUMP_IF_FALSE   142  'to 142'

 L. 643       186  LOAD_FAST                'log'
              188  LOAD_METHOD              error

 L. 644       190  LOAD_STR                 'Cannot use random scan and try to hit the same ip twice'
              192  CALL_METHOD_1         1  '1 positional argument'
              194  POP_TOP          

 L. 645       196  LOAD_CONST               None
              198  RETURN_VALUE     
              200  JUMP_BACK           142  'to 142'
              202  POP_BLOCK        
            204_0  COME_FROM_LOOP      136  '136'
              204  JUMP_BACK           104  'to 104'
              206  POP_BLOCK        
            208_0  COME_FROM_LOOP       98  '98'

 L. 646       208  LOAD_FAST                'resume'
              210  POP_JUMP_IF_FALSE   224  'to 224'

 L. 647       212  LOAD_FAST                'ipsleft'
              214  LOAD_GLOBAL              len
              216  LOAD_FAST                'database'
              218  CALL_FUNCTION_1       1  '1 positional argument'
              220  INPLACE_SUBTRACT 
              222  STORE_FAST               'ipsleft'
            224_0  COME_FROM           210  '210'

 L. 648       224  LOAD_FAST                'log'
              226  LOAD_METHOD              debug
              228  LOAD_STR                 'scanning a total of %s ips'
              230  LOAD_FAST                'ipsleft'
              232  BINARY_MODULO    
              234  CALL_METHOD_1         1  '1 positional argument'
              236  POP_TOP          

 L. 649       238  SETUP_LOOP          424  'to 424'
              240  LOAD_FAST                'ipsleft'
              242  LOAD_CONST               0
              244  COMPARE_OP               >
          246_248  POP_JUMP_IF_FALSE   422  'to 422'

 L. 650       250  LOAD_GLOBAL              random
              252  LOAD_METHOD              choice
              254  LOAD_FAST                'ipranges'
              256  CALL_METHOD_1         1  '1 positional argument'
              258  STORE_FAST               'randomchoice'

 L. 652       260  LOAD_GLOBAL              random
              262  LOAD_ATTR                randint
              264  LOAD_FAST                'randomchoice'
              266  CALL_FUNCTION_EX      0  'positional arguments only'
              268  STORE_FAST               'randint'

 L. 653       270  LOAD_GLOBAL              numToDottedQuad
              272  LOAD_FAST                'randint'
              274  CALL_FUNCTION_1       1  '1 positional argument'
              276  STORE_FAST               'ip'

 L. 654       278  LOAD_CONST               False
              280  STORE_FAST               'ipfound'

 L. 655       282  LOAD_FAST                'dbsyncs'
          284_286  POP_JUMP_IF_FALSE   304  'to 304'

 L. 656       288  LOAD_FAST                'ip'
              290  LOAD_FAST                'database'
              292  COMPARE_OP               not-in
          294_296  POP_JUMP_IF_FALSE   322  'to 322'

 L. 657       298  LOAD_CONST               True
              300  STORE_FAST               'ipfound'
              302  JUMP_FORWARD        322  'to 322'
            304_0  COME_FROM           284  '284'

 L. 659       304  LOAD_FAST                'ip'
              306  LOAD_FAST                'database'
              308  LOAD_METHOD              keys
              310  CALL_METHOD_0         0  '0 positional arguments'
              312  COMPARE_OP               not-in
          314_316  POP_JUMP_IF_FALSE   322  'to 322'

 L. 660       318  LOAD_CONST               True
              320  STORE_FAST               'ipfound'
            322_0  COME_FROM           314  '314'
            322_1  COME_FROM           302  '302'
            322_2  COME_FROM           294  '294'

 L. 661       322  LOAD_FAST                'ipfound'
          324_326  POP_JUMP_IF_FALSE   406  'to 406'

 L. 662       328  LOAD_STR                 ''
              330  LOAD_FAST                'database'
              332  LOAD_FAST                'ip'
              334  STORE_SUBSCR     

 L. 663       336  SETUP_LOOP          420  'to 420'
              338  LOAD_FAST                'portranges'
              340  GET_ITER         
              342  FOR_ITER            402  'to 402'
              344  STORE_FAST               'portrange'

 L. 664       346  SETUP_LOOP          398  'to 398'
              348  LOAD_FAST                'portrange'
              350  GET_ITER         
              352  FOR_ITER            396  'to 396'
              354  STORE_FAST               'port'

 L. 665       356  SETUP_LOOP          392  'to 392'
              358  LOAD_FAST                'methods'
              360  GET_ITER         
              362  FOR_ITER            390  'to 390'
              364  STORE_FAST               'method'

 L. 666       366  LOAD_FAST                'ipsleft'
              368  LOAD_CONST               1
              370  INPLACE_SUBTRACT 
              372  STORE_FAST               'ipsleft'

 L. 667       374  LOAD_FAST                'ip'
              376  LOAD_FAST                'port'
              378  LOAD_FAST                'method'
              380  BUILD_TUPLE_3         3 
              382  YIELD_VALUE      
              384  POP_TOP          
          386_388  JUMP_BACK           362  'to 362'
              390  POP_BLOCK        
            392_0  COME_FROM_LOOP      356  '356'
          392_394  JUMP_BACK           352  'to 352'
              396  POP_BLOCK        
            398_0  COME_FROM_LOOP      346  '346'
          398_400  JUMP_BACK           342  'to 342'
              402  POP_BLOCK        
              404  JUMP_BACK           240  'to 240'
            406_0  COME_FROM           324  '324'

 L. 669       406  LOAD_FAST                'log'
              408  LOAD_METHOD              debug
              410  LOAD_STR                 'found dup %s'
              412  LOAD_FAST                'ip'
              414  BINARY_MODULO    
              416  CALL_METHOD_1         1  '1 positional argument'
              418  POP_TOP          
            420_0  COME_FROM_LOOP      336  '336'
              420  JUMP_BACK           240  'to 240'
            422_0  COME_FROM           246  '246'
              422  POP_BLOCK        
            424_0  COME_FROM_LOOP      238  '238'

Parse error at or near `COME_FROM' instruction at offset 422_0


def scanfromfile(csv, methods):
    for row in csv:
        dstip, dstport, _, _, _ = row
        for method in methods:
            yield (
             dstip, int(dstport), method)


def dottedQuadToNum(ip):
    """convert decimal dotted quad string to long integer"""
    return struct.unpack('!L', socket.inet_aton(ip))[0]


def numToDottedQuad(n):
    """convert long int to dotted quad string"""
    return socket.inet_ntoa(struct.pack('!L', n))


def ip4range(*args):
    for arg in args:
        r = getranges(arg)
        if r is None:
            continue
        startip, endip = r
        curip = startip
        while curip <= endip:
            yield numToDottedQuad(curip)
            curip += 1


def getranges(ipstring):
    log = logging.getLogger('getranges')
    if re.match('^\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}-\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}$', ipstring):
        naddr1, naddr2 = list(map(dottedQuadToNum, ipstring.split('-')))
    else:
        if re.match('^(\\d{1,3}(-\\d{1,3})*)\\.(\\*|\\d{1,3}(-\\d{1,3})*)\\.(\\*|\\d{1,3}(-\\d{1,3})*)\\.(\\*|\\d{1,3}(-\\d{1,3})*)$', ipstring):
            naddr1, naddr2 = list(map(dottedQuadToNum, getranges2(ipstring)))
        else:
            if re.match('^.*?\\/\\d{,2}$', ipstring):
                r = getmaskranges(ipstring)
                if r is None:
                    return
                naddr1, naddr2 = r
            else:
                try:
                    naddr1 = dottedQuadToNum(socket.gethostbyname(ipstring))
                    naddr2 = naddr1
                except socket.error:
                    log.info('Could not resolve %s' % ipstring)
                    return

                return (
                 naddr1, naddr2)


def getranges2(ipstring):
    _tmp = ipstring.split('.')
    if len(_tmp) != 4:
        raise ValueError('needs to be a Quad dotted ip')
    _tmp2 = list(map(lambda x: x.split('-'), _tmp))
    startip = list()
    endip = list()
    for dot in _tmp2:
        if dot[0] == '*':
            startip.append('0')
            endip.append('255')
        else:
            if len(dot) == 1:
                startip.append(dot[0])
                endip.append(dot[0])

    naddr1 = '.'.join(startip)
    naddr2 = '.'.join(endip)
    return (naddr1, naddr2)


def getmaskranges(ipstring):
    log = logging.getLogger('getmaskranges')
    addr, mask = ipstring.rsplit('/', 1)
    if not re.match('^\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}$', addr):
        try:
            log.debug('Could not resolve %s' % addr)
            addr = socket.gethostbyname(addr)
        except socket.error:
            return

    assert mask.isdigit(), 'invalid IP mask (1)'
    naddr = dottedQuadToNum(addr)
    masklen = int(mask)
    assert 0 <= masklen <= 32, 'invalid IP mask (2)'
    naddr1 = naddr & (1 << masklen) - 1 << 32 - masklen
    naddr2 = naddr1 + (1 << 32 - masklen) - 1
    return (naddr1, naddr2)


def scanfromdb(db, methods):
    database = dbm.open(db, 'r')
    for k in database.keys():
        for method in methods:
            ip, port = k.split(':')
            port = int(port)
            yield (ip, port, method)


def resumeFromIP(ip, args):
    ipranges = list()
    foundit = False
    rargs = list()
    nip = dottedQuadToNum(ip)
    for arg in args:
        startip, endip = getranges(arg)
        if not foundit:
            if startip <= nip:
                if endip >= nip:
                    ipranges.append((nip, endip))
                    foundit = True
                else:
                    ipranges.append((startip, endip))

    for iprange in ipranges:
        rargs.append('-'.join(map(numToDottedQuad, iprange)))

    return rargs


def resumeFrom(val, rangestr):
    val = int(val)
    ranges = list(map(lambda x: map(int, x.split('-')), rangestr.split(',')))
    foundit = False
    tmp = list()
    for r in ranges:
        start, end = r
        if not foundit:
            if start <= val:
                if end >= val:
                    tmp.append((val, end))
                    foundit = True
                else:
                    tmp.append((start, end))

    return ','.join(map(lambda x: '-'.join(map(str, x)), tmp))


def packetcounter(n):
    i = 0
    while True:
        if i == n:
            i = 0
            r = True
        else:
            i += 1
            r = False
        yield r


sessiontypes = ['svmap', 'svwar', 'svcrack']

def findsession(chosensessiontype=None):
    listresult = dict()
    for sessiontype in sessiontypes:
        if chosensessiontype in [None, sessiontype]:
            p = os.path.join(os.path.expanduser('~'), '.sipvicious', sessiontype)
            if os.path.exists(p):
                listresult[sessiontype] = os.listdir(p)

    return listresult


def listsessions(chosensessiontype=None, count=False):
    listresult = findsession(chosensessiontype)
    for k in listresult.keys():
        print('Type of scan: %s' % k)
        for r in listresult[k]:
            sessionstatus = 'Incomplete'
            sessionpath = os.path.join(os.path.expanduser('~'), '.sipvicious', k, r)
            dblen = ''
            if count:
                if k == 'svmap':
                    dbloc = os.path.join(sessionpath, 'resultua')
                else:
                    if k == 'svwar':
                        dbloc = os.path.join(sessionpath, 'resultauth')
                    else:
                        if k == 'svcrack':
                            dbloc = os.path.join(sessionpath, 'resultpasswd')
                os.path.exists(dbloc) or logging.debug('The database could not be found: %s' % dbloc)
            else:
                db = dbm.open(dbloc, 'r')
                dblen = len(db)
            if os.path.exists(os.path.join(sessionpath, 'closed')):
                sessionstatus = 'Complete'
            print('\t- %s\t\t%s\t\t%s\n' % (r, sessionstatus, dblen))


def deletesessions--- This code section failed: ---

 L. 868         0  LOAD_GLOBAL              logging
                2  LOAD_METHOD              getLogger
                4  LOAD_STR                 'deletesessions'
                6  CALL_METHOD_1         1  '1 positional argument'
                8  STORE_FAST               'log'

 L. 869        10  LOAD_GLOBAL              list
               12  CALL_FUNCTION_0       0  '0 positional arguments'
               14  STORE_FAST               'sessionpath'

 L. 870        16  LOAD_FAST                'chosensessiontype'
               18  LOAD_CONST               None
               20  COMPARE_OP               is
               22  POP_JUMP_IF_FALSE    88  'to 88'

 L. 871        24  SETUP_LOOP          136  'to 136'
               26  LOAD_GLOBAL              sessiontypes
               28  GET_ITER         
             30_0  COME_FROM            70  '70'
               30  FOR_ITER             84  'to 84'
               32  STORE_FAST               'sessiontype'

 L. 872        34  LOAD_GLOBAL              os
               36  LOAD_ATTR                path
               38  LOAD_METHOD              join
               40  LOAD_GLOBAL              os
               42  LOAD_ATTR                path
               44  LOAD_METHOD              expanduser

 L. 873        46  LOAD_STR                 '~'
               48  CALL_METHOD_1         1  '1 positional argument'
               50  LOAD_STR                 '.sipvicious'
               52  LOAD_FAST                'sessiontype'
               54  LOAD_FAST                'chosensession'
               56  CALL_METHOD_4         4  '4 positional arguments'
               58  STORE_FAST               'p'

 L. 874        60  LOAD_GLOBAL              os
               62  LOAD_ATTR                path
               64  LOAD_METHOD              exists
               66  LOAD_FAST                'p'
               68  CALL_METHOD_1         1  '1 positional argument'
               70  POP_JUMP_IF_FALSE    30  'to 30'

 L. 875        72  LOAD_FAST                'sessionpath'
               74  LOAD_METHOD              append
               76  LOAD_FAST                'p'
               78  CALL_METHOD_1         1  '1 positional argument'
               80  POP_TOP          
               82  JUMP_BACK            30  'to 30'
               84  POP_BLOCK        
               86  JUMP_FORWARD        136  'to 136'
             88_0  COME_FROM            22  '22'

 L. 877        88  LOAD_GLOBAL              os
               90  LOAD_ATTR                path
               92  LOAD_METHOD              join
               94  LOAD_GLOBAL              os
               96  LOAD_ATTR                path
               98  LOAD_METHOD              expanduser
              100  LOAD_STR                 '~'
              102  CALL_METHOD_1         1  '1 positional argument'
              104  LOAD_STR                 '.sipvicious'

 L. 878       106  LOAD_FAST                'chosensessiontype'
              108  LOAD_FAST                'chosensession'
              110  CALL_METHOD_4         4  '4 positional arguments'
              112  STORE_FAST               'p'

 L. 879       114  LOAD_GLOBAL              os
              116  LOAD_ATTR                path
              118  LOAD_METHOD              exists
              120  LOAD_FAST                'p'
              122  CALL_METHOD_1         1  '1 positional argument'
              124  POP_JUMP_IF_FALSE   136  'to 136'

 L. 880       126  LOAD_FAST                'sessionpath'
              128  LOAD_METHOD              append
              130  LOAD_FAST                'p'
              132  CALL_METHOD_1         1  '1 positional argument'
              134  POP_TOP          
            136_0  COME_FROM           124  '124'
            136_1  COME_FROM            86  '86'
            136_2  COME_FROM_LOOP       24  '24'

 L. 881       136  LOAD_GLOBAL              len
              138  LOAD_FAST                'sessionpath'
              140  CALL_FUNCTION_1       1  '1 positional argument'
              142  LOAD_CONST               0
              144  COMPARE_OP               ==
              146  POP_JUMP_IF_FALSE   152  'to 152'

 L. 882       148  LOAD_CONST               None
              150  RETURN_VALUE     
            152_0  COME_FROM           146  '146'

 L. 883       152  SETUP_LOOP          230  'to 230'
              154  LOAD_FAST                'sessionpath'
              156  GET_ITER         
              158  FOR_ITER            228  'to 228'
              160  STORE_FAST               'sp'

 L. 884       162  SETUP_EXCEPT        192  'to 192'

 L. 885       164  LOAD_GLOBAL              shutil
              166  LOAD_METHOD              rmtree
              168  LOAD_FAST                'sp'
              170  CALL_METHOD_1         1  '1 positional argument'
              172  POP_TOP          

 L. 886       174  LOAD_FAST                'log'
              176  LOAD_METHOD              info
              178  LOAD_STR                 'Session at %s was removed'
              180  LOAD_FAST                'sp'
              182  BINARY_MODULO    
              184  CALL_METHOD_1         1  '1 positional argument'
              186  POP_TOP          
              188  POP_BLOCK        
              190  JUMP_BACK           158  'to 158'
            192_0  COME_FROM_EXCEPT    162  '162'

 L. 887       192  DUP_TOP          
              194  LOAD_GLOBAL              OSError
              196  COMPARE_OP               exception-match
              198  POP_JUMP_IF_FALSE   224  'to 224'
              200  POP_TOP          
              202  POP_TOP          
              204  POP_TOP          

 L. 888       206  LOAD_FAST                'log'
              208  LOAD_METHOD              error
              210  LOAD_STR                 'Could not delete %s'
              212  LOAD_FAST                'sp'
              214  BINARY_MODULO    
              216  CALL_METHOD_1         1  '1 positional argument'
              218  POP_TOP          
              220  POP_EXCEPT       
              222  JUMP_BACK           158  'to 158'
            224_0  COME_FROM           198  '198'
              224  END_FINALLY      
              226  JUMP_BACK           158  'to 158'
              228  POP_BLOCK        
            230_0  COME_FROM_LOOP      152  '152'

 L. 889       230  LOAD_FAST                'sessionpath'
              232  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `COME_FROM_LOOP' instruction at offset 136_2


def createReverseLookup(src, dst):
    log = logging.getLogger('createReverseLookup')
    srcdb = src
    dstdb = dst
    if len(srcdb) > 100:
        log.warn('Performing dns lookup on %s hosts. To disable reverse ip resolution make use of the -n option' % len(srcdb))
    for k in srcdb.keys():
        tmp = k.split(b':', 1)
        if len(tmp) == 2:
            ajpi, port = tmp
            try:
                tmpk = ':'.join([socket.gethostbyaddr(ajpi.decode())[0], port.decode()])
                logging.debug('Resolved %s to %s' % (k, tmpk))
                dstdb[k] = tmpk
            except socket.error:
                logging.info('Could not resolve %s' % k)

    return dstdb


def getasciitable(labels, db, resdb=None, width=60):
    rows = list()
    for k in db.keys():
        cols = [
         k.decode(), db[k].decode()]
        if resdb is not None:
            if k in resdb:
                cols.append(resdb[k].decode())
            else:
                cols.append('[not available]')
        rows.append(cols)

    o = to_string(rows, header=labels)
    return o


def outputtoxml(title, labels, db, resdb=None, xsl='resources/sv.xsl'):
    from xml.sax.saxutils import escape
    o = '<?xml version="1.0" ?>\r\n'
    o += '<?xml-stylesheet type="text/xsl" href="%s"?>\r\n' % escape(xsl)
    o += '<root>\r\n'
    o += '<title>%s</title>\r\n' % escape(title)
    o += '<labels>\r\n'
    for label in labels:
        o += '<label><name>%s</name></label>\r\n' % escape(label)

    o += '</labels>\r\n'
    o += '<results>\r\n'
    for k in db.keys():
        o += '<result>\r\n'
        o += '<%s><value>%s</value></%s>\r\n' % (
         labels[0].replace(' ', '').lower(), k, escape(labels[0]).replace(' ', '').lower())
        o += '<%s><value>%s</value></%s>\r\n' % (
         labels[1].replace(' ', '').lower(), escape(db[k]), labels[1].replace(' ', '').lower())
        if resdb is not None:
            if k in resdb:
                o += '<%s><value>%s</value></%s>\r\n' % (
                 labels[2].replace(' ', '').lower(), escape(resdb[k]), labels[2].replace(' ', '').lower())
            else:
                o += '<%s><value>N/A</value></%s>\r\n' % (
                 labels[2].replace(' ', '').lower(), labels[2].replace(' ', '').lower())
        o += '</result>\r\n'

    o += '</results>\r\n'
    o += '</root>\r\n'
    return o


def getsessionpath--- This code section failed: ---

 L. 961         0  LOAD_GLOBAL              logging
                2  LOAD_METHOD              getLogger
                4  LOAD_STR                 'getsessionpath'
                6  CALL_METHOD_1         1  '1 positional argument'
                8  STORE_FAST               'log'

 L. 962        10  LOAD_STR                 'svmap'
               12  LOAD_STR                 'svwar'
               14  LOAD_STR                 'svcrack'
               16  BUILD_LIST_3          3 
               18  STORE_FAST               'sessiontypes'

 L. 963        20  LOAD_CONST               None
               22  STORE_FAST               'sessionpath'

 L. 964        24  LOAD_FAST                'sessiontype'
               26  LOAD_CONST               None
               28  COMPARE_OP               is
               30  POP_JUMP_IF_FALSE   140  'to 140'

 L. 965        32  LOAD_FAST                'log'
               34  LOAD_METHOD              debug
               36  LOAD_STR                 'sessiontype is not specified'
               38  CALL_METHOD_1         1  '1 positional argument'
               40  POP_TOP          

 L. 966        42  SETUP_LOOP          182  'to 182'
               44  LOAD_FAST                'sessiontypes'
               46  GET_ITER         
             48_0  COME_FROM           102  '102'
               48  FOR_ITER            136  'to 136'
               50  STORE_FAST               'sessiontype'

 L. 967        52  LOAD_GLOBAL              os
               54  LOAD_ATTR                path
               56  LOAD_METHOD              join
               58  LOAD_GLOBAL              os
               60  LOAD_ATTR                path
               62  LOAD_METHOD              expanduser

 L. 968        64  LOAD_STR                 '~'
               66  CALL_METHOD_1         1  '1 positional argument'
               68  LOAD_STR                 '.sipvicious'
               70  LOAD_FAST                'sessiontype'
               72  LOAD_FAST                'session'
               74  CALL_METHOD_4         4  '4 positional arguments'
               76  STORE_FAST               'p'

 L. 969        78  LOAD_FAST                'log'
               80  LOAD_METHOD              debug
               82  LOAD_STR                 'trying %s'
               84  LOAD_FAST                'p'
               86  BINARY_MODULO    
               88  CALL_METHOD_1         1  '1 positional argument'
               90  POP_TOP          

 L. 970        92  LOAD_GLOBAL              os
               94  LOAD_ATTR                path
               96  LOAD_METHOD              exists
               98  LOAD_FAST                'p'
              100  CALL_METHOD_1         1  '1 positional argument'
              102  POP_JUMP_IF_FALSE    48  'to 48'

 L. 971       104  LOAD_FAST                'log'
              106  LOAD_METHOD              debug
              108  LOAD_STR                 '%s exists'
              110  CALL_METHOD_1         1  '1 positional argument'
              112  POP_TOP          

 L. 972       114  LOAD_FAST                'log'
              116  LOAD_METHOD              debug
              118  LOAD_STR                 'sessiontype is %s'
              120  LOAD_FAST                'sessiontype'
              122  BINARY_MODULO    
              124  CALL_METHOD_1         1  '1 positional argument'
              126  POP_TOP          

 L. 973       128  LOAD_FAST                'p'
              130  STORE_FAST               'sessionpath'

 L. 974       132  BREAK_LOOP       
              134  JUMP_BACK            48  'to 48'
              136  POP_BLOCK        
              138  JUMP_FORWARD        182  'to 182'
            140_0  COME_FROM            30  '30'

 L. 976       140  LOAD_GLOBAL              os
              142  LOAD_ATTR                path
              144  LOAD_METHOD              join
              146  LOAD_GLOBAL              os
              148  LOAD_ATTR                path
              150  LOAD_METHOD              expanduser

 L. 977       152  LOAD_STR                 '~'
              154  CALL_METHOD_1         1  '1 positional argument'
              156  LOAD_STR                 '.sipvicious'
              158  LOAD_FAST                'sessiontype'
              160  LOAD_FAST                'session'
              162  CALL_METHOD_4         4  '4 positional arguments'
              164  STORE_FAST               'p'

 L. 978       166  LOAD_GLOBAL              os
              168  LOAD_ATTR                path
              170  LOAD_METHOD              exists
              172  LOAD_FAST                'p'
              174  CALL_METHOD_1         1  '1 positional argument'
              176  POP_JUMP_IF_FALSE   182  'to 182'

 L. 979       178  LOAD_FAST                'p'
              180  STORE_FAST               'sessionpath'
            182_0  COME_FROM           176  '176'
            182_1  COME_FROM           138  '138'
            182_2  COME_FROM_LOOP       42  '42'

 L. 980       182  LOAD_FAST                'sessionpath'
              184  LOAD_CONST               None
              186  COMPARE_OP               is
              188  POP_JUMP_IF_FALSE   194  'to 194'

 L. 981       190  LOAD_CONST               None
              192  RETURN_VALUE     
            194_0  COME_FROM           188  '188'

 L. 982       194  LOAD_FAST                'sessionpath'
              196  LOAD_FAST                'sessiontype'
              198  BUILD_TUPLE_2         2 
              200  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `COME_FROM_LOOP' instruction at offset 182_2


def dbexists(name):
    if os.path.exists(name):
        return True
    if os.path.exists(name + '.db'):
        return True
    return False


def outputtopdf(outputfile, title, labels, db, resdb):
    log = logging.getLogger('outputtopdf')
    try:
        from reportlab.platypus import TableStyle, Table, SimpleDocTemplate, Paragraph
        from reportlab.lib import colors
        from reportlab.lib.styles import getSampleStyleSheet
        from reportlab.pdfgen import canvas
    except ImportError:
        log.error('Reportlab was not found. To export to pdf you need to have reportlab installed. Check out www.reportlab.org')
        return
    else:
        log.debug('ok reportlab library found')
        styles = getSampleStyleSheet()
        rows = list()
        rows.append(labels)
        for k in db.keys():
            cols = [
             k, db[k]]
            if resdb is not None:
                if k in resdb:
                    cols.append(resdb[k])
                else:
                    cols.append('N/A')
            rows.append(cols)

        t = Table(rows)
        mytable = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.black),
         (
          'TEXTCOLOR', (0, 0), (-1, 0), colors.white)])
        t.setStyle(mytable)
        doc = SimpleDocTemplate(outputfile)
        elements = []
        style = styles['Heading1']
        Title = Paragraph(title, style)
        elements.append(Title)
        elements.append(t)
        doc.build(elements)


class anotherxrange(object):
    __doc__ = 'A pure-python implementation of xrange.\n\n    Can handle float/long start/stop/step arguments and slice indexing'
    __slots__ = [
     '_slice']

    def __init__(self, *args):
        self._slice = slice(*args)
        if self._slice.stop is None:
            raise TypeError('xrange stop must not be None')

    @property
    def start(self):
        if self._slice.start is not None:
            return self._slice.start
        return 0

    @property
    def stop(self):
        return self._slice.stop

    @property
    def step(self):
        if self._slice.step is not None:
            return self._slice.step
        return 1

    def __hash__(self):
        return hash(self._slice)

    def __repr__(self):
        return '%s(%r, %r, %r)' % (self.__class__.__name__,
         self.start, self.stop, self.step)

    def __len__(self):
        return self._len()

    def _len(self):
        return max(0, int((self.stop - self.start) / self.step))

    def __getitem__(self, index):
        if isinstance(index, slice):
            start, stop, step = index.indices(self._len())
            return range(self._index(start), self._index(stop), step * self.step)
        if isinstance(index, int):
            if index < 0:
                fixed_index = index + self._len()
            else:
                fixed_index = index
            if not 0 <= fixed_index < self._len():
                raise IndexError('Index %d out of %r' % (index, self))
            return self._index(fixed_index)
        raise TypeError('xrange indices must be slices or integers')

    def _index(self, i):
        return self.start + self.step * i


def getTargetFromSRV(domainnames, methods):
    log = logging.getLogger('getTargetFromSRV')
    try:
        import dns, dns.resolver
    except ImportError:
        log.critical('could not import the DNS library. Get it from http://www.dnspython.org/')
        return
    else:
        for domainname in domainnames:
            for proto in ('udp', 'tcp'):
                name = '_sip._' + proto + '.' + domainname + '.'
                try:
                    log.debug('trying to resolve SRV for %s' % name)
                    ans = dns.resolver.query(name, 'SRV')
                except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer) as err:
                    try:
                        log.debug('Encountered error: %s' % err.__str__())
                        log.info('Could not resolve %s' % name)
                        continue
                    finally:
                        err = None
                        del err

                for a in ans.response.answer:
                    log.info('got an answer %s' % a.to_text())
                    for _tmp in a:
                        for method in methods:
                            try:
                                hostname = socket.gethostbyname(_tmp.target.to_text())
                            except socket.error:
                                log.warn('%s could not be resolved' % _tmp.target.to_text())
                                continue

                            log.debug('%s resolved to %s' % (
                             _tmp.target.to_text(), hostname))
                            yield (hostname, _tmp.port, method)


def getAuthHeader(pkt):
    nonceRE = '\r\n(www-authenticate|proxy-authenticate): (.+?)\r\n'
    _tmp = re.findall(nonceRE, pkt, re.I)
    if _tmp is not None:
        if len(_tmp) > 0:
            return _tmp[0][1]


def check_ipv6(n):
    try:
        socket.inet_pton(socket.AF_INET6, n)
        return True
    except socket.error:
        return False


if __name__ == '__main__':
    print(getranges('1.1.1.1/24'))
    seq = getranges('google.com/24')
    if seq is not None:
        a = ip4range(seq)
        for x in iter(a):
            print(x)