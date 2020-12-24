# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/pynet/pynet.py
# Compiled at: 2007-07-27 14:11:22
import re, sys

class pyNet(object):
    __module__ = __name__

    def __init__(self, input):
        """Process input, set the version, and internal variables"""
        (ip, masklen, self.ver) = self.parse_input(input)
        self.masklength = masklen
        self.ipINT = self.v4v6_to_INT(ip, self.ver)
        self.maskINT = self.masklen_to_INT(masklen, self.ver)

    def ip(self):
        """Return the ip address"""
        return self.INT_to_v4v6(self.ipINT, self.ver)

    def network(self):
        """Return the network address"""
        retval = self.INT_to_v4v6(self.ipINT & self.maskINT, self.ver)
        return retval

    def cidr(self):
        """Return a CIDR-style IP representation"""
        ip = self.INT_to_v4v6(self.ipINT, self.ver)
        masklen = self.INT_to_masklen(self.maskINT)
        return '%s/%s' % (ip, masklen)

    def broadcast(self):
        """Return the broadcast address"""
        host = long(self.binary_NOT(self.maskINT), 2)
        net = self.v4v6_to_INT(self.network(), self.ver)
        bcast_addr = long(net + host)
        retval = self.INT_to_v4v6(bcast_addr, self.ver)
        return retval

    def mask(self):
        """Return a mask as either dotted-quad (ipv4) or colon-seperated string
      (ipv6)"""
        return self.INT_to_v4v6(self.maskINT, self.ver)

    def masklen(self):
        """Return the mask length"""
        return self.masklength

    def bits(self):
        """Return the width of the network in bits"""
        if self.ver == 4:
            retval = 32
        elif self.ver == 6:
            retval = 128
        return retval

    def wildcard(self):
        """Return the wildcard representation of the netmask.  Useful in Cisco
      ACLs"""
        return self.INT_to_v4v6(long(self.binary_NOT(self.maskINT), 2), self.ver)

    def range(self):
        """Return all addresses in the subnet, including network and broadcast"""
        return '%s-%s' % (self.network(), self.broadcast())

    def hosts(self):
        """Return all USABLE addresses in the subnet.  Network and bcast 
      are excluded."""
        netINT = self.v4v6_to_INT(self.network(), self.ver)
        bcastINT = self.v4v6_to_INT(self.broadcast(), self.ver)
        if (self.masklength < 31) & (self.ver == 4) or (self.masklength < 127) & (self.ver == 6):
            host_begin = self.INT_to_v4v6(netINT + 1, self.ver)
            host_end = self.INT_to_v4v6(bcastINT - 1, self.ver)
        elif (self.masklength == 31) & (self.ver == 4) or (self.masklength == 127) & (self.ver == 6):
            host_begin = self.INT_to_v4v6(netINT, self.ver)
            host_end = self.INT_to_v4v6(bcastINT, self.ver)
        else:
            host_begin = self.INT_to_v4v6(netINT, self.ver)
            host_end = host_begin
        return '%s-%s' % (host_begin, host_end)

    def hostenum(self):
        """Return a list of all USABLE addresses in the subnet.  Network and
      broadcast addresses are excluded."""
        (begin, end) = self.hosts().split('-')
        enum = []
        beginINT = self.v4v6_to_INT(begin, self.ver)
        endINT = self.v4v6_to_INT(end, self.ver) + 1
        for ii in range(beginINT, endINT):
            enum.append(self.INT_to_v4v6(ii, self.ver))

        return enum

    def rangeenum(self):
        """Return a list of all addresses in the subnet.  Network and broadcast 
      addresses are included."""
        (begin, end) = self.range().split('-')
        enum = []
        beginINT = self.v4v6_to_INT(begin, self.ver)
        endINT = self.v4v6_to_INT(end, self.ver) + 1
        for ii in range(beginINT, endINT):
            enum.append(self.INT_to_v4v6(ii, self.ver))

        return enum

    def contains(self, arg2):
        """Return True if the self object contains the argument"""
        objA = self
        objB = pyNet(arg2)
        objA_INT = objA.ipINT & objA.maskINT
        objB_INT = objB.ipINT & objA.maskINT
        if objA_INT == objB_INT:
            retval = True
        else:
            retval = False
        return retval

    def within(self, arg2):
        """Return True if the self object is within argument"""
        objA = self
        objB = pyNet(arg2)
        objA_INT = objA.ipINT & objB.maskINT
        objB_INT = objB.ipINT & objB.maskINT
        if objA_INT == objB_INT:
            retval = True
        else:
            retval = False
        return retval

    def v4v6_to_INT(self, network, version):
        """Convert user input to (long) INT variables: ipINT and maskINT"""
        if version == 4:
            width = 32
            array = network.split('.', 4)
            ipINT = 0
            for ii in range(len(array)):
                ipINT = ipINT + long('0x100', 16) ** (len(array) - ii - 1) * long(array[ii])

        else:
            width = 128
            v6_expanded = False
            while v6_expanded == False:
                network = re.sub('::', ':0:', network)
                if not re.search('::', network):
                    v6_expanded = True

        array = network.split(':', 8)
        ipINT = 0
        for ii in range(len(array)):
            ipINT = ipINT + long('0x10000', 16) ** (len(array) - ii - 1) * long(array[ii], 16)

        return ipINT

    def masklen_to_INT(self, masklen, version):
        if version == 4:
            width = 32
        if version == 6:
            width = 128
        maskINT = long(2 ** masklen - 1 << width - masklen)
        return maskINT

    def INT_to_masklen(self, intvar):
        binstr = self.binary(intvar)
        masklen = len(re.sub('0', '', binstr))
        return masklen

    def INT_to_v4v6(self, intvar, version):
        """Convert a long INT number into v4 or v6 notation"""
        retval = ''
        strvar = re.sub('^0x([0-9a-fA-F]+)L$', '\\g<1>', str(hex(intvar))).lower()
        if version == 4:
            strvar = re.sub('\\s', '0', '%8s' % strvar)
            oo = '[0-9a-f]{2}'
            ii = '([0-9a-f]{1,2})(' + oo + ')(' + oo + ')(' + oo + ')$'
            rr = re.search(ii, strvar)
            octets = [rr.group(1), rr.group(2), rr.group(3), rr.group(4)]
            for ii in range(len(octets)):
                octets[ii] = str(int(octets[ii], 16))

            retval = ('.').join(octets)
        elif version == 6:
            strvar = re.sub('\\s', '0', '%32s' % strvar)
            oo = '[0-9a-f]{4}'
            ii = '([0-9a-f]{1,4})(%s)(%s)(%s)(%s)(%s)(%s)(%s)' % (oo, oo, oo, oo, oo, oo, oo)
            rr = re.search(ii, strvar)
            octets = [rr.group(1), rr.group(2), rr.group(3), rr.group(4), rr.group(5), rr.group(6), rr.group(7), rr.group(8)]
            retval = (':').join(octets)
        else:
            print 'pyNet: INT_to_v4v6: An undefined error occurred while processing %s' % intvar
        return retval

    def parse_input(self, input):
        """Ensure that user's network strings are formatted correctly.  Return 
      version"""
        if re.search('^(\\d{1,3}\\.){3}\\d{1,3}\\/\\d{1,3}$', input.lower()):
            (ip, masklen) = re.split('\\/', input.lower(), 2)
            version = 4
        elif re.search('^(\\d{1,3}\\.){3}\\d{1,3}\\/(\\d{1,3}\\.){3}\\d{1,3}$', input.lower()):
            (ip, mask) = re.split('\\/', input.lower(), 2)
            version = 4
            masklen = self.INT_to_masklen(self.v4v6_to_INT(mask, version))
        elif re.search('^\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}$', input.lower()):
            ip, masklen = input, '32'
            version = 4
        elif re.search('^([0-9a-f]{0,4}:){0,7}([0-9a-f]){0,3}[0-9a-f]$', input.lower()):
            version = 6
            ip, masklen = input, '128'
        elif re.search('^([0-9a-f]{0,4}:){0,7}([0-9a-f]){0,3}[0-9a-f]\\/\\d{1,3}$', input.lower()):
            version = 6
            (ip, masklen) = re.split('\\/', input.lower(), 2)
        else:
            print 'pyNet: string_to_INT: Invalid network address or mask: %s' % input
            sys.exit(0)
        masklen = long(masklen)
        return (
         ip, masklen, version)

    def binary_NOT(self, n):
        """Perform a binary NOT on the INT or LONG argument.  Return the binary
      representation as a string."""
        assert n >= 0
        bits = []
        while n:
            bits.append('10'[(n & 1)])
            n >>= 1

        bits.reverse()
        return ('').join(bits) or '0'

    def binary(self, n):
        """Perform a binary NOT on the INT or LONG argument.  Return the binary
      representation as a string."""
        assert n >= 0
        bits = []
        while n:
            bits.append('01'[(n & 1)])
            n >>= 1

        bits.reverse()
        return ('').join(bits) or '0'


if __name__ == '__main__':
    print ''