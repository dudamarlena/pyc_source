# uncompyle6 version 3.6.7
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Library/Python/2.5/site-packages/ldaplib.py
# Compiled at: 2009-07-28 02:44:11
import socket, struct
AND = 0
OR = 1
NOT = 2
EQUALITYMATCH = 3
SUBSTRINGS = 4
GREATEROREQUAL = 5
LESSOREQUAL = 6
PRESENT = 7
APPROXMATCH = 8
EXTENSIBLEMATCH = 9
LDAPVERSION1 = 1
LDAPVERSION2 = 2
LDAPVERSION3 = 3
UNIVERSAL = 0
APPLICATION = 64
CONTEXT = 128
PRIVATE = 192
PRIMITIVE = 0
CONSTRUCTED = 32
EOC = 0
BOOLEAN = 1
INTEGER = 2
BITSTRING = 3
OCTETSTRING = 4
NULL = 5
OID = 6
OD = 7
EXTERNAL = 8
REAL = 9
ENUMERATED = 10
EMBEDDED = 11
UTF8String = 12
RELATIVEOID = 13
SEQUENCE = 16
SET = 17
NumericString = 18
PrintableString = 19
T61String = 20
VideotexString = 21
IA5String = 22
UTCTime = 23
GraphicString = 25
VisibleString = 26
GeneralString = 27
UniversalString = 28
CHARACTERSTRING = 29
BMPString = 30
ADD = 0
DELETE = 1
REPLACE = 2
BIND = 0
BINDRESP = 1
UNBIND = 2
SEARCHREQ = 3
SEARCHRESENTRY = 4
SEARCHRESDONE = 5
SEARCHRESREF = 6
MODIFYREQUEST = 6
MODIFYRESP = 7
ADDREQUEST = 8
ADDRESP = 9
DEL = 10
DELRESP = 11
MODIFYRDN = 12
MODIFYRDNRESP = 13
COMPARE = 14
COMPARERESP = 15
ABANDON = 16
EXTENDEDREQ = 17
EXTENDEDRESP = 18
modifyops = {'add': 0, 
   'delete': 1, 
   'replace': 2}

class sock:
    """Lightweight Wrapper around Socket and SSL, so we can use the same code everywhere else
        and ignore if SSL is actually on the link or not.
        NOTE: SSL is just magically trusted, keys and stuff are beyond this code!
        Not for using across an insecure link!
        """

    def __init__(self):
        self.socket = socket.socket()
        self.ssl = False

    def connect(self, address, ssl=None):
        """Address should look like: ('ad.yumaed.org',389)
                if SSL = True, then start an SSL connection. otherwise regular.
                Or if port is 636, then auto-start SSL connection.
                """
        if address[1] == 636:
            ssl = True
        self.socket.connect(address)
        if ssl:
            self.ssl = socket.ssl(self.socket)

    def recv(self, options=None):
        if self.ssl:
            return self.ssl.read(options)
        else:
            return self.socket.recv(options)

    def send(self, data):
        if self.ssl:
            return self.ssl.write(data)
        else:
            return self.socket.send(data)


class ldap_command:

    def __init__(self):
        """overloaded in inherited classes"""
        pass

    def encode(self):
        buffer = ''
        for arg in self.myargs:
            (cls, pc, no, data) = arg
            buffer += ber_encode(cls, pc, no, data)

        buffer = ber_encode(APPLICATION, CONSTRUCTED, self.app_code, buffer)
        messageid = get_sqn()
        buffer = ber_encode(UNIVERSAL, PRIMITIVE, INTEGER, messageid) + buffer
        buffer = ber_encode(UNIVERSAL, CONSTRUCTED, SEQUENCE, buffer)
        return buffer

    def decode(self, parent=1, cls=None, pc=None, buffer=None, remainder=None, no=None):
        self.keyvals = {}
        if parent:
            (cls, pc, no, self.messageid, remainder) = ber_decode(self.buffer)
            (cls, pc, self.app_code, buffer, remainder) = ber_decode(remainder)
            self.args = []
        while 1:
            if pc == PRIMITIVE and not len(remainder):
                return
            if pc == PRIMITIVE:
                (cls, pc, no, buffer, remainder) = ber_decode(remainder)
                if pc == PRIMITIVE:
                    self.args.append((cls, pc, no, buffer))
            else:
                if no == SEQUENCE:
                    res = self.decode_sequence(buffer)
                    self.args.append((cls, pc, no, res))
                    if len(remainder):
                        (c, p, n, b, r) = ber_decode(remainder)
                        if p == PRIMITIVE:
                            self.args.append((c, p, n, b))
                        self.decode(parent=0, cls=c, no=n, pc=p, buffer=b, remainder=r)
                    return
                (cls, pc, no, buffer, remainder) = ber_decode(buffer)
                if pc == PRIMITIVE:
                    self.args.append((cls, pc, no, buffer))
                if len(remainder):
                    (c, p, n, b, r) = ber_decode(remainder)
                    if p == PRIMITIVE:
                        self.args.append((c, p, n, b))
                    self.decode(parent=0, cls=c, no=n, pc=p, buffer=b, remainder=r)

    def decode_sequence(self, buff):
        r2 = buff
        while len(r2):
            (cls, pc, no, r1, r2) = ber_decode(r2)
            while len(r1):
                (cls, pc, no, key, r1) = ber_decode(r1)
                if not len(r1):
                    break
                (cls, pc, no, buff, remainder) = ber_decode(r1)
                (cls, pc, no, buff, remainder) = ber_decode(buff)
                self.keyvals[key] = [buff]
                while len(remainder):
                    (cls, pc, no, buff, remainder) = ber_decode(remainder)
                    self.keyvals[key].append(buff)


class bind(ldap_command):
    app_code = BIND

    def __init__(self, username, password, version=LDAPVERSION2):
        self.myargs = []
        self.myargs.append((UNIVERSAL, PRIMITIVE, INTEGER, chr(version)))
        self.myargs.append((UNIVERSAL, PRIMITIVE, OCTETSTRING, username))
        self.myargs.append((CONTEXT, PRIMITIVE, 0, password))


class bindresp(ldap_command):

    def __init__(self, buffer):
        self.buffer = buffer
        self.decode()
        if self.app_code != BINDRESP:
            raise Exception('BUFFER_MISMATCH', '%s!=%s' % (self.app_code, BINDRESP))
        self.resultcode = ord(self.args[0][3])
        self.matcheddn = self.args[1][3]
        self.errorMessage = self.args[2][3]


class unbind(ldap_command):
    app_code = UNBIND

    def __init__(self):
        self.myargs = []


class search(ldap_command):
    app_code = SEARCHREQ

    def __init__(self, filter, base='o=solution.cmg.nl', scope='\x02', derefaliases='\x00', sizelimit='\x00', timelimit='\x03', typesonly='\x00', attribs=[]):
        self.myargs = []
        self.myargs.append((UNIVERSAL, PRIMITIVE, OCTETSTRING, base))
        self.myargs.append((UNIVERSAL, PRIMITIVE, ENUMERATED, scope))
        self.myargs.append((UNIVERSAL, PRIMITIVE, ENUMERATED, derefaliases))
        self.myargs.append((UNIVERSAL, PRIMITIVE, INTEGER, sizelimit))
        self.myargs.append((UNIVERSAL, PRIMITIVE, INTEGER, timelimit))
        self.myargs.append((UNIVERSAL, PRIMITIVE, BOOLEAN, typesonly))
        if '=' in filter:
            (f1, f2) = filter.split('=')
            ctx = EQUALITYMATCH
        if '>' in filter:
            (f1, f2) = filter.split('>')
            ctx = GREATEROREQUAL
        if '<' in filter:
            (f1, f2) = filter.split('<')
            ctx = LESSOREQUAL
        filterbuff = ber_encode(UNIVERSAL, PRIMITIVE, OCTETSTRING, f1)
        filterbuff += ber_encode(UNIVERSAL, PRIMITIVE, OCTETSTRING, f2)
        filterbuff = ber_encode(CONTEXT, CONSTRUCTED, ctx, filterbuff)
        self.myargs.append((CONTEXT, CONSTRUCTED, EOC, filterbuff))
        attribbuff = ''
        for attrib in attribs:
            attribbuff += ber_encode(UNIVERSAL, PRIMITIVE, OCTETSTRING, attrib)

        self.myargs.append((UNIVERSAL, CONSTRUCTED, SEQUENCE, attribbuff))


class searchresentry(ldap_command):

    def __init__(self, buffer):
        self.myargs = []
        self.buffer = buffer
        self.decode()
        if self.app_code == SEARCHRESDONE:
            self.resultcode = self.args[0][3]
            self.matcheddn = self.args[1][3]
            self.errorMessage = self.args[2][3]
        else:
            return


class modify(ldap_command):
    app_code = MODIFYREQUEST

    def __init__(self, dn, commands):
        self.myargs = []
        self.myargs.append((UNIVERSAL, PRIMITIVE, OCTETSTRING, dn))
        attribbuffer = ''
        itembuff = ''
        for i in commands:
            (op, type, vals) = i
            op = modifyops[op]
            minibuff = ''
            type = ber_encode(UNIVERSAL, PRIMITIVE, OCTETSTRING, type)
            op = ber_encode(UNIVERSAL, PRIMITIVE, ENUMERATED, chr(op))
            valbuff = ''
            for val in vals:
                valbuff += ber_encode(UNIVERSAL, PRIMITIVE, OCTETSTRING, val)

            valbuff = type + ber_encode(UNIVERSAL, CONSTRUCTED, SET, valbuff)
            valbuff = op + ber_encode(UNIVERSAL, CONSTRUCTED, SEQUENCE, valbuff)
            itembuff += ber_encode(UNIVERSAL, CONSTRUCTED, SEQUENCE, valbuff)

        self.myargs.append((UNIVERSAL, CONSTRUCTED, SEQUENCE, itembuff))


class modify_resp(ldap_command):

    def __init__(self, buffer):
        self.myargs = []
        self.buffer = buffer
        self.decode()
        if self.app_code != MODIFYRESP:
            raise Exception('BUFFER_MISMATCH', '%s!=%s' % (self.app_code, MODIFYRESP))
        self.resultcode = self.args[0][3]
        self.matcheddn = self.args[1][3]
        self.errorMessage = self.args[2][3]


class add_entry(ldap_command):
    app_code = ADDREQUEST

    def __init__(self, dn, attribs={}):
        self.myargs = []
        self.myargs.append((UNIVERSAL, PRIMITIVE, OCTETSTRING, dn))
        attribbuffer = ''
        keys = attribs.keys()
        for key in keys:
            itemvalbuff = ber_encode(UNIVERSAL, PRIMITIVE, OCTETSTRING, key)
            valbuff = ''
            for val in attribs[key]:
                valbuff += ber_encode(UNIVERSAL, PRIMITIVE, OCTETSTRING, val)

            itemvalbuff += ber_encode(UNIVERSAL, CONSTRUCTED, SET, valbuff)
            attribbuffer += ber_encode(UNIVERSAL, CONSTRUCTED, SEQUENCE, itemvalbuff)

        self.myargs.append((UNIVERSAL, CONSTRUCTED, SEQUENCE, attribbuffer))


class add_resp(ldap_command):

    def __init__(self, buffer):
        self.myargs = []
        self.buffer = buffer
        self.decode()
        if self.app_code != ADDRESP:
            raise Exception('BUFFER_MISMATCH', '%s!=%s' % (self.app_code, ADDRESP))
        self.resultcode = self.args[0][3]
        self.matcheddn = self.args[1][3]
        self.errorMessage = self.args[2][3]


class del_entry(ldap_command):
    app_code = DEL

    def __init__(self, dn):
        self.myargs = []
        self.dn = dn
        self.myargs.append((UNIVERSAL, PRIMITIVE, OCTETSTRING, dn))

    def encode(self):
        buffer = ber_encode(APPLICATION, PRIMITIVE, self.app_code, self.dn)
        messageid = get_sqn()
        buffer = ber_encode(UNIVERSAL, PRIMITIVE, INTEGER, messageid) + buffer
        buffer = ber_encode(UNIVERSAL, CONSTRUCTED, SEQUENCE, buffer)
        return buffer


class del_resp(ldap_command):

    def __init__(self, buffer):
        self.myargs = []
        self.buffer = buffer
        self.decode()
        if self.app_code != DELRESP:
            raise Exception('BUFFER_MISMATCH', '%s!=%s' % (self.app_code, DELRESP))
        self.resultcode = self.args[0][3]
        self.matcheddn = self.args[1][3]
        self.errorMessage = self.args[2][3]


class modifyrdn(ldap_command):
    app_code = MODIFYRDN


class compare(ldap_command):
    app_code = COMPARE


class abandon(ldap_command):
    app_code = ABANDON


sqn = 0

def get_sqn():
    global sqn
    sqn += 1
    if sqn > 255:
        sqn = 1
    return chr(sqn)


def ber_encode(cls, pc, no, data):
    encoded_data = chr(cls + pc + no)
    if len(data) < 128:
        encoded_data += chr(len(data))
    else:
        length = struct.pack('>Q', len(data)).replace('\x00', '')
        encoded_data += chr(128 + len(length)) + length
    encoded_data += data
    return encoded_data


def ber_decode(buffer):
    res = []
    header = ord(buffer[0])
    if header < 64:
        cl = UNIVERSAL
    elif header < 128:
        cl = APPLICATION
        header = header - 64
    elif header < 192:
        cl = CONTEXT
        header = header - 128
    else:
        cl = PRIVATE
        header = header - 192
    if header < 32:
        pr = 0
    else:
        pr = 1
        header = header - 32
    num = header
    length = ord(buffer[1])
    buffer = buffer[2:]
    if length > 127:
        noofbytes = length - 128
        bytes = buffer[:noofbytes]
        buffer = buffer[noofbytes:]
        length = 0
        counter = 1
        while len(bytes):
            length += ord(bytes[(-1)]) * counter
            counter = counter * 256
            bytes = bytes[:-1]

    unusedbuffer = buffer[length:]
    buffer = buffer[:length]
    return (
     cl, pr, num, buffer, unusedbuffer)


BER_ERROR = ''

class ldap_connection:

    def __init__(self, address):
        self.address = address
        self.conn = sock()
        self.conn.connect(address)

    def get_buff(self):
        header = self.conn.recv(2)
        if ord(header[0]) != UNIVERSAL + CONSTRUCTED + SEQUENCE:
            raise BER_ERROR
        length = ord(header[1])
        if length > 121:
            bytes = self.conn.recv(length - 128)
            length = 0
            counter = 1
            while len(bytes):
                length += ord(bytes[(-1)]) * counter
                counter = counter * 256
                bytes = bytes[:-1]

        buffer = ''
        while len(buffer) < length:
            buffer += self.conn.recv(length - len(buffer))

        return buffer

    def bind(self, username, password):
        """do an ldap bind to the server"""
        data = bind(username, password)
        self.conn.send(data.encode())
        buffer = self.get_buff()
        resp = bindresp(buffer)

    def unbind(self):
        """close the connection"""
        data = unbind()
        self.conn.send(data.encode())

    def abandon(self):
        """do an abandon to the server"""
        data = abandon()
        self.conn.send(data.encode)

    def search(self, filter, base='o=solution.cmg.nl', attributes=[]):
        data = search(filter, base, attribs=attributes)
        self.conn.send(data.encode())
        res = []
        while 1:
            buffer = self.get_buff()
            resp = searchresentry(buffer)
            res.append(resp)
            if resp.app_code == SEARCHRESDONE:
                break

        return res

    def compare_entry(self):
        pass

    def add_entry(self, dn, attribs):
        data = add_entry(dn, attribs)
        self.conn.send(data.encode())
        buffer = self.get_buff()
        return add_resp(buffer)

    def delete_entry(self, dn):
        data = del_entry(dn)
        self.conn.send(data.encode())
        buffer = self.get_buff()
        return del_resp(buffer)

    def modify(self, dn, commands):
        """Modify takes 2 arguments, the first is a DN string.
                the second is a [].
                        the first item is an operation (add,delete,replace)
                        second item is the 'type' (i.e. cn, or whatever you want to change)
                        the 3rd item is a list of values: ['John Smith','Tito Jones]
                returns a Modify Result Object: ['__doc__', '__init__', '__module__', 'app_code', 'args', 'buffer', 'decode', 'decode_sequence', 'encode', 'errorMessage', 'keyvals', 'matcheddn', 'messageid', 'myargs', 'resultcode']
                """
        data = modify(dn=dn, commands=commands)
        self.conn.send(data.encode())
        buffer = self.get_buff()
        return modify_resp(buffer)