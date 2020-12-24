# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pysnmp/carrier/sockmsg.py
# Compiled at: 2019-08-18 17:24:05
import sys
from pysnmp import debug
if sys.version_info[:2] < (3, 3):

    def getRecvFrom(addressType):
        raise error.CarrierError('sendmsg()/recvmsg() interface is not supported by this OS and/or Python version')


    def getSendTo(addressType):
        raise error.CarrierError('sendmsg()/recvmsg() interface is not supported by this OS and/or Python version')


else:
    import ctypes, ipaddress, socket
    from pysnmp.carrier import sockfix
    from pysnmp.carrier import error
    uint32_t = ctypes.c_uint32
    in_addr_t = uint32_t

    class in_addr(ctypes.Structure):
        __module__ = __name__
        _fields_ = [('s_addr', in_addr_t)]


    class in6_addr_U(ctypes.Union):
        __module__ = __name__
        _fields_ = [('__u6_addr8', ctypes.c_uint8 * 16), ('__u6_addr16', ctypes.c_uint16 * 8), ('__u6_addr32', ctypes.c_uint32 * 4)]


    class in6_addr(ctypes.Structure):
        __module__ = __name__
        _fields_ = [('__in6_u', in6_addr_U)]


    class in_pktinfo(ctypes.Structure):
        __module__ = __name__
        _fields_ = [('ipi_ifindex', ctypes.c_int), ('ipi_spec_dst', in_addr), ('ipi_addr', in_addr)]


    class in6_pktinfo(ctypes.Structure):
        __module__ = __name__
        _fields_ = [('ipi6_addr', in6_addr), ('ipi6_ifindex', ctypes.c_uint)]


    def getRecvFrom(addressType):

        def recvfrom(s, sz):
            _to = None
            (data, ancdata, msg_flags, _from) = s.recvmsg(sz, socket.CMSG_LEN(sz))
            for anc in ancdata:
                if anc[0] == socket.SOL_IP and anc[1] == socket.IP_PKTINFO:
                    addr = in_pktinfo.from_buffer_copy(anc[2])
                    addr = ipaddress.IPv4Address(memoryview(addr.ipi_addr).tobytes())
                    _to = (str(addr), s.getsockname()[1])
                    break
                elif anc[0] == socket.SOL_IPV6 and anc[1] == socket.IPV6_PKTINFO:
                    addr = in6_pktinfo.from_buffer_copy(anc[2])
                    addr = ipaddress.ip_address(memoryview(addr.ipi6_addr).tobytes())
                    _to = (str(addr), s.getsockname()[1])
                    break

            debug.logger & debug.flagIO and debug.logger('recvfrom: received %d octets from %s to %s; iov blob %r' % (len(data), _from, _to, ancdata))
            return (
             data, addressType(_from).setLocalAddress(_to))

        return recvfrom


    def getSendTo(addressType):

        def sendto(s, _data, _to):
            ancdata = []
            if type(_to) == addressType:
                addr = ipaddress.ip_address(_to.getLocalAddress()[0])
            else:
                addr = ipaddress.ip_address(s.getsockname()[0])
            if type(addr) == ipaddress.IPv4Address:
                _f = in_pktinfo()
                _f.ipi_spec_dst = in_addr.from_buffer_copy(addr.packed)
                ancdata = [(socket.SOL_IP, socket.IP_PKTINFO, memoryview(_f).tobytes())]
            elif s.family == socket.AF_INET6 and type(addr) == ipaddress.IPv6Address:
                _f = in6_pktinfo()
                _f.ipi6_addr = in6_addr.from_buffer_copy(addr.packed)
                ancdata = [(socket.SOL_IPV6, socket.IPV6_PKTINFO, memoryview(_f).tobytes())]
            debug.logger & debug.flagIO and debug.logger('sendto: sending %d octets to %s; address %r; iov blob %r' % (len(_data), _to, addr, ancdata))
            return s.sendmsg([_data], ancdata, 0, _to)

        return sendto