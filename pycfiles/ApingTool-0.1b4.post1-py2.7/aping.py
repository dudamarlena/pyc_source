# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/src/aping.py
# Compiled at: 2018-07-19 20:44:19
import sys, struct, os, re, random, signal, binascii, getopt, time, socket, array, fcntl, thread, subprocess
from default import *

def calcsum(sum_data):
    """The packet checksum algorithm (the one's complement sum of 16-bit words)
    Generates a checksum of a (ICMP) packet. Based on the function found in
    ping.c on FreeBSD.
    """
    if len(sum_data) & 1:
        sum_data += '\x00'
    words = array.array('H', sum_data)
    sum = 0
    for word in words:
        sum += word & 65535

    hi = sum >> 16
    lo = sum & 65535
    sum = hi + lo
    sum += sum >> 16
    return struct.pack('H', ~sum & 65535)


class ICMPprobe():
    """
    The program main class. Handles all the important stuff.
    From here are sent the ICMP packets
    """

    def __init__(self):
        """This method initiates the ICMPprobe class."""
        signal.signal(signal.SIGINT, self.sighandler)
        socket.setdefaulttimeout(listen_timeout)
        try:
            self.rawicmp = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
            self.rawicmp.bind((bind_addr, 0))
        except socket.error as error_msg:
            if error_msg[0] == 1:
                sys.exit('\nAPing: You must have root (superuser) privileges to run APing')
            elif error_msg[0] == 99:
                sys.exit("\nAPing: Can't bind socket to specified address: %s\n                \rThe IP address must to exist on your interface" % bind_addr)

        self.rawicmp.setsockopt(socket.IPPROTO_IP, socket.IP_TTL, time_to_live)
        self.rawicmp.setsockopt(socket.IPPROTO_IP, socket.IP_TOS, ip_tos)
        self.send_delay = send_delay
        self.pkg_sent = 0
        self.pkg_recv = 0
        self.rtt_sum = 0
        self.rtt_max = 0
        self.rtt_min = 90000
        self.code = '\x00'
        self.retrans = 0
        self.addr_mask = ''
        self.tmstamp_req = ''
        self.extradata = ''
        self.ident = struct.pack('!H', random.randrange(1, 65536))
        self.payload = self.data_gen()
        if probe_type == 'p':
            self.types = '\x08'
            self.strint_type = '8(echo request)'
        else:
            if probe_type == 'i':
                self.types = '\x0f'
                self.strint_type = '15(information request)'
            elif probe_type == 'm':
                self.types = '\x11'
                self.addr_mask = '\x00\x00\x00\x00'
                self.strint_type = '17(address mask request)'
            elif probe_type == 't':
                self.types = '\r'
                self.strint_type = '13(timestamp request)'
                self.tmstamp_req = '\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
            self.length = 8 + extra_data + len(self.tmstamp_req + self.addr_mask)
            self.islocal = 0
            a, b, c, d = ip_dst_address.split('.')
            if int(a) == int(b) == int(c) == int(d) == 0:
                self.islocal = 1
            elif int(a) == 127:
                self.islocal = 1
            else:
                for iface in self.listNetDevices():
                    if ip_dst_address == self.getProtoAddrFromIface(iface):
                        self.islocal = 1
                        break

        thread.start_new_thread(self.ondemandinfo, ())
        self.start_time = time.time()

    def listNetDevices(self):
        """
        List all the local network ifaces
        """
        if_singleMaxLen = 32
        if_totalNamesLen = 2048
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if_names = array.array('B', '\x00' * if_totalNamesLen)
        try:
            buff = fcntl.ioctl(sock.fileno(), SIOCGIFCONF, struct.pack('iL', if_totalNamesLen, if_names.buffer_info()[0]))
        except Exception as e:
            sock.close()
            return []

        sock.close()
        if_names = if_names.tostring()
        ifacesArray = []
        for i in range(0, struct.unpack('iL', buff)[0], if_singleMaxLen):
            if_label = if_names[i:i + if_singleMaxLen].split('\x00', 1)[0]
            if if_label.isalnum():
                ifacesArray.append(if_label)

        return ifacesArray

    def getProtoAddrFromIface(self, iface):
        """
        return IP address attached to a given network iface
        """
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            buff = fcntl.ioctl(sock.fileno(), SIOCGIFADDR, struct.pack('256s', iface))
            ipAddr = socket.inet_ntoa(buff[20:24])
        except Exception as e:
            ipAddr = ''

        sock.close()
        return ipAddr

    def ondemandinfo(self):
        """
        Run this thread in the background and print this info if the user
        presses the enter key
        """
        while 1:
            try:
                if raw_input() == '':
                    if self.pkg_recv:
                        rtt_aver = self.rtt_sum / self.pkg_recv
                    else:
                        rtt_aver, self.rtt_min = (0, 0)
                    if ip_dst_address == dst_address:
                        print 'Target: %s' % dst_address
                    else:
                        print 'Target: %s (%s)' % (dst_address, ip_dst_address)
                    print 'Packets sent/lost/received: %d/%d/%d\n                        \rCurrent rtt min/aver/max: %.2f/%.2f/%.2f\n                        \rElapsed time hours/minutes/seconds: %s\n' % (
                     self.pkg_sent, self.pkg_sent - self.pkg_recv,
                     self.pkg_recv, self.rtt_min, rtt_aver,
                     self.rtt_max,
                     time.strftime('%H:%M:%S', time.gmtime(time.time() - self.start_time)))
            except Exception as e:
                break

    def data_gen(self):
        """Generates some 0 bytes of extra data if specified by the user"""
        for i in xrange(extra_data):
            self.extradata += '\x00'

        return self.extradata

    def sendpkg(self):
        """The packet transmission loop"""
        while 1:
            if probe_time == self.pkg_sent + 1:
                self.send_delay = 0
            else:
                if probe_time < self.pkg_sent + 1:
                    self.reason = 'Stop after %s packet(s) sent' % probe_time
                    self.statistics()
                self.intseq = self.pkg_sent + 1
                self.seq = struct.pack('!H', self.intseq)
                checksum = calcsum(self.types + '\x00' + '\x00\x00' + self.ident + self.seq)
                try:
                    self.rawicmp.sendto(self.types + self.code + checksum + self.ident + self.seq + self.addr_mask + self.tmstamp_req + self.payload, (
                     ip_dst_address, dst_port))
                except socket.error as error_msg:
                    if error_msg[0] == 101:
                        sys.exit('\nAPing: Unable to establish a connection.Verify your network connectivity !')

            if pkg_trace:
                print '\nsent: %s bytes ttl=%s icmp type=%s icmp seq=%s ' % (
                 self.length, time_to_live,
                 self.strint_type, self.intseq)
            self.pkg_sent += 1
            rtt_starttime = time.time()
            while 1:
                try:
                    if self.islocal:
                        self.rawicmp.recvfrom(2048)
                    self.data, self.src_addr = self.rawicmp.recvfrom(2048)
                except socket.timeout:
                    self.retrans += 1
                    if self.retrans >= probes_retry:
                        self.reason = 'Retransmission exceeded after %s probe(s)' % probes_retry
                        self.statistics()
                    break

                if self.data[24:26] == self.ident or self.data[52:54] == self.ident:
                    signal.alarm(0)
                    self.rtt_current = (time.time() - rtt_starttime) * 1000
                    self.retrans = 0
                    self.pkg_recv += 1
                    self.data_analize()
                    self.rtt_sum += self.rtt_current
                    self.rtt_min = min(self.rtt_current, self.rtt_min)
                    self.rtt_max = max(self.rtt_current, self.rtt_max)
                    break

            time.sleep(self.send_delay)

    def data_analize(self):
        """Here are parsed the received packets,and printed to the stdout"""
        self.data = binascii.hexlify(self.data)
        ttl = int(self.data[16:18], 16)
        self.src_addr = self.src_addr[0]
        icmp_type = int(self.data[40:42], 16)
        if icmp_type == 0:
            icmp_msg = 'echo reply'
            icmp_seq = int(self.data[52:56], 16)
        elif icmp_type == 3:
            icmp_msg = 'dest. unreachable'
            icmp_seq = int(self.data[108:112], 16)
        elif icmp_type == 4:
            icmp_msg = 'source quench'
            icmp_seq = 0
        elif icmp_type == 5:
            icmp_msg = 'redirect'
            icmp_seq = 0
        elif icmp_type == 8:
            icmp_msg = 'echo request'
            icmp_seq = int(self.data[52:56], 16)
        elif icmp_type == 9:
            icmp_msg = 'router advertisement'
            icmp_seq = 0
        elif icmp_type == 10:
            icmp_msg = 'router sollicitation'
            icmp_seq = 0
        elif icmp_type == 11:
            icmp_msg = 'time exceeded'
            icmp_seq = int(self.data[108:112], 16)
        elif icmp_type == 12:
            icmp_msg = 'parameter problem'
            icmp_seq = 0
        elif icmp_type == 13:
            icmp_msg = 'timestamp request'
            icmp_seq = int(self.data[52:56], 16)
        elif icmp_type == 14:
            icmp_msg = 'timestamp reply'
            icmp_seq = int(self.data[52:56], 16)
        elif icmp_type == 15:
            icmp_msg = 'information request'
            icmp_seq = int(self.data[52:56], 16)
        elif icmp_type == 16:
            icmp_msg = 'information reply'
            icmp_seq = int(self.data[52:56], 16)
        elif icmp_type == 17:
            icmp_msg = 'address mask request'
            icmp_seq = int(self.data[52:56], 16)
        elif icmp_type == 18:
            icmp_msg = 'address mask reply'
            icmp_seq = int(self.data[52:56], 16)
        elif icmp_type == 30:
            icmp_msg = 'traceroute'
            icmp_seq = 0
        elif icmp_type == 31:
            icmp_msg = 'conversion error'
            icmp_seq = 0
        elif icmp_type == 37:
            icmp_msg = 'domain name request'
            icmp_seq = int(self.data[52:56], 16)
        elif icmp_type == 38:
            icmp_msg = 'domain name reply'
            icmp_seq = int(self.data[52:56], 16)
        else:
            icmp_seq = 0
            icmp_msg = 'unknown'
        length = len(self.data[40:]) / 2
        if return_time != 1 or probe_type != 't':
            if not old:
                print 'recv: %d bytes addr=%s ttl=%d icmp type=%d(%s) icmp seq=%d rtt=%.2f ms' % (
                 length, self.src_addr, ttl,
                 icmp_type, icmp_msg, icmp_seq,
                 self.rtt_current) + sonar
            else:
                print '%d bytes from %s: icmp_seq=%d time=%d ms' % (
                 length, self.src_addr, icmp_seq,
                 self.rtt_current) + sonar
        else:
            if icmp_type != 14:
                sys.exit('\nAPing: Invalid timestamp reply received\n                \rSo can not use the --time option to parse the time')
            print 'recv: timestamp reply addr=%s time -> %s - UTC' % (
             dst_address,
             time.strftime('%H:%M:%S', time.gmtime(int(self.data[72:80], 16) / 1000))) + sonar

    def sighandler(self, signum, frame):
        """The keyboard interrupt handler"""
        self.reason = 'Interrupt from keyboard (SIGINT)'
        self.statistics()

    def statistics(self):
        """The statistics are printed to the stdout every time when the program
        stops for some reason (retrans. expired, interrupt from keyboard ...)
        """
        if signal.alarm(0) > 0:
            self.last_pkg = '\n - No reply for the last sent packet because interrupted in the listening time'
        else:
            self.last_pkg = ''
        time_elapsed = time.time() - self.start_time
        pkg_lost = self.pkg_sent - self.pkg_recv
        if self.pkg_recv > 0:
            aver_time = self.rtt_sum / self.pkg_recv
        else:
            aver_time, self.rtt_min, self.src_addr = 0, 0, ip_dst_address
        if ip_dst_address in self.src_addr or self.islocal:
            from_where = ''
        else:
            from_where = '\n - The received packets are not from the target address (%s)!' % dst_address
        if self.last_pkg == '' and from_where == '':
            msg = '\n - All is OK'
        else:
            msg = ''
        msec = str(time_elapsed).split('.')
        if pkg_trace:
            print
        if not old:
            print '\nHalt reason: %s\n            \rStatus:%s%s%s\n            \r\n++++++++++++++  statistics  ++++++++++++++\n            \rPackets:\n            \r   Total sent:%s | lost:%s | received:%s\n            \r       | lost:%.2f%% | received:%.2f%%\n            \rTiming:\n            \r   rtt min:%.2f | aver:%.2f | max:%.2f ms\n            \r   Total time elapsed: %s.%ss' % (
             self.reason, from_where, self.last_pkg, msg,
             self.pkg_sent, pkg_lost, self.pkg_recv,
             100.0 * pkg_lost / self.pkg_sent,
             100.0 * self.pkg_recv / self.pkg_sent,
             self.rtt_min, aver_time, self.rtt_max,
             time.strftime('%Hh: %Mm: %S', time.gmtime(time_elapsed)),
             msec[1][:3])
        else:
            print '\n\n----%s PING Statistics----\n            \r%d packets transmitted, %d packets received, %d%% packet loss\n            \rround-trip (ms)  min/avg/max = %d/%d/%d' % (
             dst_address, self.pkg_sent, self.pkg_recv,
             100.0 * pkg_lost / self.pkg_sent,
             self.rtt_min, aver_time, self.rtt_max)
        self.rawicmp.close()
        self.rawicmp.close()
        sys.exit(0)


class Resolver():
    """The DNS resolver class.

    This class makes the resolution of the hostname or the reverse DNS resolution
    if an IPv4 is entered and the -d option used.(The class uses the system DNS 
    resolver).
    """

    def __init__(self, str_probe_type, isip):
        global ip_dst_address
        try:
            target_addr_info = socket.gethostbyname_ex(dst_address)
        except socket.gaierror:
            sys.exit('APing: Target hostname can not be resolved (%s)\n            \rAre you specified a valid hostname ? check the characters' % dst_address)

        nr_of_ips = len(target_addr_info[2])
        target_ips = str(target_addr_info[2]).strip('[]')
        addr_cnames = str(target_addr_info[1]).strip('[]')
        address_record = target_addr_info[0]
        if nr_of_ips == 1:
            ip_dst_address = target_addr_info[2][0]
        else:
            ip_dst_address = target_addr_info[2][random.randrange(0, nr_of_ips)]
        if verbose > 0:
            if not isip and nr_of_ips > 1:
                print "%s resolves to multiple IP's (%s)" % (
                 dst_address, nr_of_ips)
                if verbose == 2:
                    print "The IP's are:", target_ips
            elif not isip and nr_of_ips == 1:
                print dst_address, 'resolves to', ip_dst_address
            if not isip and verbose == 2:
                if addr_cnames == '':
                    addr_cnames = None
                print 'Canonical names:', addr_cnames
                print 'Address record:', address_record
            print 'Trying with IP:', ip_dst_address
        if isip and rev_dns:
            try:
                print 'Reverse DNS resolution: %s' % socket.gethostbyaddr(dst_address)[0]
            except socket.herror:
                print 'Warning ! Reverse DNS resolution failed'

        if not old:
            print 'Sending', str_probe_type
        else:
            print 'PING %s (%s): %d data bytes' % (
             dst_address, ip_dst_address, extra_data)
        ICMPprobe().sendpkg()
        return


def printopt(isipv4):
    """Checks the date to adjust the time zone and if it's specified by the
    user print to the stdout all the settings witch are used for the current
    session
    """
    if probe_type == 'p':
        str_probe_type = 'ICMP Echo request'
    elif probe_type == 't':
        str_probe_type = 'ICMP Timestamp request'
    elif probe_type == 'm':
        str_probe_type = 'ICMP Address Mask request'
    elif probe_type == 'i':
        str_probe_type = 'ICMP Information request'
    if time.localtime()[8] == 1:
        timezone = time.tzname[1]
    else:
        timezone = time.tzname[0]
    print '\n* Starting APing at: %s %s *' % (time.asctime(), timezone)
    if print_opt:
        print '\nICMP probe options:\n            \r-------------------\n            \r Target address: . . . .%s\n            \r Probe type: . . . . . .%s\n            \r Packets to send: . . . %s\n            \r Listening timeout: . . %s (sec)\n            \r Send delay: . . . . . .%s (sec)\n            \r Extra data: . . . . . .%s (bytes)\n            \r Time to live: . . . . .%s\n            \r Probes retry: . . . . .%s (times)\n            \r Verbosity level: . . . %s\n            \r Reverse DNS: . . . . . %s\n            \r Packet trace: . . . . .%s\n            \r Print options: . . . . %s\n            \r TOS field value: . . . %s (int)\n            \r Print timestamp time: .%s\n            \r Bond to address: . . . %s\n            \r Old style output: . . .%s\n            \r Produce sonar beeps . .%s\n' % (
         dst_address, str_probe_type, probe_time, listen_timeout,
         send_delay, extra_data, time_to_live, probes_retry,
         verbose, rev_dns, pkg_trace, print_opt, ip_tos,
         return_time, bool(bind_addr), old, bool(sonar))
    Resolver(str_probe_type, isipv4)


def help():
    """Prints this help message to the stdout if the '-h/--help' option is used"""
    sys.exit("\nUsage: aping.py {target specification} [OPTIONS]\n\nTarget:\n    {target specification}\n        Specify the target address. The target can be a hostname like\n        www.probe.com, my.example.org or any IPv4 address like 192.168.0.1\nOptions:\n    -P, --Probe <type> \n        Specify the ICMP probe type.<type> can be p, t, m or i where\n        p is for usual ping probes, t is for timestamp request m for\n        address mask request and i for information request (default\n        is the ICMP echo request) \n    --time\n        This option is used only with the timestamp requests. If a valid\n        timestamp reply is received from the target and this option is\n        enabled it prints out the time in the timestamp packets\n    -d, --rdns \n        Make reverse DNS resolution if you specified a IPv4 address\n    --print-options\n        Print out all the options configured with this session before\n        sending any packets\n    -t, --ttl <num>\n        Set up the time to live field. <num> is an integer and it is\n        between 1 and 255 (inclusive). The default value is 64\n    -b, --bind <IP number>\n        Use this option to bind the created socket to an IP address. The\n        argument <IP number> must to be a valid IPv4 address. This option\n        if useful if you have multiple public IP's or when you probe your\n        local address. In this case it's a good idea to bind the socket\n        to another local IP\n    --pkg-trace\n        If this option is specified it prints out all the packets sent to\n        the target not just the received ones\n    --old\n        Use old style output. If you use this option the output for captured\n        packets and the statistics are exactly like in the original ping\n        program from 1983 by Mike Muuss\n    -s, --size <byte>\n        Data in packets to send. <byte> is the number of extra bytes to\n        send.Default behavior for APing is to send packets with no\n        extra data\n    -o, --listen <time>\n        Set the listening timeout before APing retransmits the packet.\n        <time> is the argument in seconds. By default APing uses 2 seconds\n        to listen after a sent packet.\n    -c, --count <count>\n        Set the number of packets to send,then stop. <count> is the number of\n        packets to send. Default behaviour is to send an infinitive number of\n        packets unless you stop from the keyboard, or retransmission exceeded\n    -w, --send-delay <time>[s/m]\n        Adjust the send delay between probes. <time> is the delay time\n        in milliseconds, the default send delay is 1 second.The 's' or\n        'm' options are used to choose between seconds or milliseconds,\n        but argument has to be an integer.\n    -r, --retry <num>\n        Set the probes retry if no packet is received. <num> is the packets\n        to send, the default probes retry is 3 after that APing stops\n    -T, --tos <num>\n        Set the TOS (Type of Service) field in the IP header. The <num>\n        argument can be an integer from 0 to 255 (inclusive) or specified\n        as a hexadecimal number in format 0x (default value is 0)\n    -v, --verbose <level>\n        Verbose output for the DNS resolver. The <level> argument is a\n        integer number that can be 1 or 2 (default is 0)\n    --sonar\n        Produces short beeps on every received packets. You must to have\n        a speaker on your mother board to hear the beeps.\n        other things\n    -V, --Version\n        Print out the version and exit\n    -h, --help\n        This help message")


def checkaddr(addresses):
    isipv4 = 0
    try:
        int(addresses.replace('.', ''))
        a, b, c, d = addresses.split('.')
        for i in (a, b, c, d):
            i = int(i)
            if i > 255 or i < 0:
                sys.exit('\nAPing: Invalid IP address number range specified (%s)\n                    \rValid number range is between 0 and 255 (inclusive)' % addresses)

        if '255' in [a, b, c, d]:
            print '\nWarning : Broadcast not implemented yet in APing\n                \rBehaviour might be uncertain'
        isipv4 = 1
    except ValueError as error_msg:
        if 'need' in str(error_msg) or 'many' in str(error_msg):
            sys.exit('\nAPing: Invalid IP address length specified (%s)\n                \rThe address must to be a valid IPv4 address' % addresses)

    return isipv4


def main():
    global SIOCGIFADDR
    global SIOCGIFCONF
    global bind_addr
    global dst_address
    global extra_data
    global ip_tos
    global listen_timeout
    global old
    global pkg_trace
    global print_opt
    global probe_time
    global probe_type
    global probes_retry
    global return_time
    global rev_dns
    global send_delay
    global sonar
    global time_to_live
    global verbose
    try:
        valid_options = getopt.gnu_getopt(sys.argv[1:], 'Vt:r:w:c:o:v:s:P:hdT:b:', ('Probe=',
                                                                                    'rdns',
                                                                                    'print-options',
                                                                                    'ttl=',
                                                                                    'pkg-trace',
                                                                                    'size=',
                                                                                    'count=',
                                                                                    'retry=',
                                                                                    'verbose=',
                                                                                    'send-delay=',
                                                                                    'listen=',
                                                                                    'tos=',
                                                                                    'time',
                                                                                    'help',
                                                                                    'Version',
                                                                                    'bind=',
                                                                                    'old',
                                                                                    'sonar'))
    except getopt.GetoptError as bad_opt:
        sys.exit('\nAPing: %s \nTry -h or --help for a list of available options' % bad_opt)

    lista = []
    for opt, arg in valid_options[0]:
        if opt == '-s' or opt == '--size':
            try:
                extra_data = int(arg)
                if extra_data < 0:
                    sys.exit('\nAPing: Invalid extra data specified (%s)\n                    \rArgument must to be greater or equal to 0' % arg)
            except ValueError:
                sys.exit('\nAPing: Invalid extra data specified (%s)\n                \rArgument must be an integer not string or float value' % extra_data)

            lista.append('size')
        elif opt == '-v' or opt == '--verbose':
            try:
                verbose = int(arg)
                if verbose < 0 or verbose > 2:
                    sys.exit('\nAPing: Invalid verbosity level specified (%s)\n                    \rValid values range from 0 to 2 (inclusive)' % verbose)
            except ValueError:
                sys.exit('\nAPing: Invalid verbosity level specified (%s)\n                \rArgument must to be an integer not string or float value' % arg)

            lista.append('verbose')
        elif opt == '-P' or opt == '--Probe':
            probe_type = arg
            if probe_type not in ('p', 't', 'm', 'i'):
                sys.exit('\nAPing: Unknown probe type specified (%s)\n                \rValid probe types are: p for echo request\n                       t for timestamp request\n                       m for address mask request\n                       i for information request' % probe_type)
            lista.append('Probe')
        elif opt == '-o' or opt == '--listen':
            if arg.endswith('m'):
                listen_timeout = 1 / 1000.0
                arg = arg.replace('m', '')
            else:
                if arg.endswith('s'):
                    listen_timeout = 1
                    arg = arg.replace('s', '')
                else:
                    listen_timeout = 1
                try:
                    listen_timeout *= int(arg)
                    if listen_timeout <= 0:
                        sys.exit('\nAping: Invalid listen timeout specified (%s)\n                    \rArgument must be greater than 0' % arg)
                except ValueError:
                    sys.exit('\nAping: Invalid listen timeout specified (%s)\n                \rArgument must be an integer value not string' % arg)

            lista.append('listen')
        elif opt == '-c' or opt == '--count':
            try:
                probe_time = int(arg)
                if probe_time <= 0:
                    sys.exit('\nAPing: Invalid number of packets to send specified (%s)\n                    \rArgument must to be integer value greater than 0' % probe_time)
            except ValueError:
                probe_time = arg
                if probe_time != 'inf':
                    sys.exit('\nAPing: Invalid number of packets to send specified (%s)\n                    \rArgument must be an integer value not string or float' % arg)

            lista.append('packet')
        elif opt == '-w' or opt == '--send-delay':
            send_delay = arg
            try:
                send_delay = float(send_delay)
                if send_delay < 0:
                    sys.exit('\nAPing: Invalid send delay specified (%s)\n                    \rArgument must be greater or equal to 0' % send_delay)
            except ValueError:
                sys.exit('\nAPing: Invalid send delay specified (%s)\n                \rArgument must be a float or integer value' % arg)

            lista.append('send-delay')
        elif opt == '-t' or opt == '--ttl':
            try:
                time_to_live = int(arg)
                if time_to_live < 1 or time_to_live > 255:
                    sys.exit('\nAPing: Invalid time to live specified (%d)\n                    \rValid values range from 1 to 255 (inclusive)' % time_to_live)
            except ValueError:
                sys.exit('\nAPing: Invalid time to live specified (%s)\n                \rArgument must be an integer value' % arg)

            lista.append('ttl')
        elif opt == '-r' or opt == '--retry':
            try:
                probes_retry = int(arg)
                if probes_retry <= 0:
                    sys.exit('\nAPing: Invalid probes retry specified (%s)\n                    \rArgument must be greater than 0' % probes_retry)
            except ValueError:
                sys.exit('\nAPing: Invalid probes retry specified (%s)\n                \rArgument must be an integer value' % parg)

            lista.append('retry')
        elif opt == '-T' or opt == '--tos':
            try:
                ip_tos = int(arg)
            except ValueError:
                ip_tos = arg
                if ip_tos[:2] != '0x':
                    sys.exit('APing: Invalid TOS value specified (%s)\n                    \rArgument must be an integer or hex value' % arg)
                try:
                    ip_tos = int(ip_tos[2:], 16)
                except ValueError:
                    sys.exit('\nAping: Invalid TOS hexadecimal value specified (%s)\n                    \rArgument must be between 0x00 and 0xff (inclusive)' % arg)

            if ip_tos > 255 or ip_tos < 0:
                sys.exit('APing: Invalid TOS value specified (%s)\n                \rArgument must be between 0 and 255 (inclusive)' % arg)
            lista.append('tos')
        elif opt == '--old':
            old = True
            lista.append('old')
        elif opt == '--print-options':
            print_opt = True
            lista.append('print-options')
        elif opt == '-d' or opt == '--rdns':
            rev_dns = True
            lista.append('rdns')
        elif opt == '-b' or opt == '--bind':
            bind_addr = arg
            lista.append('bind')
        elif opt == '--time':
            return_time = True
            lista.append('time')
        elif opt == '--pkg-trace':
            pkg_trace = True
            lista.append('pkg-trace')
        elif opt == '--sonar':
            sonar = '\x07'
            lista.append('sonar')
        elif opt == '-h' or opt == '--help':
            help()
        elif opt == '-V' or opt == '--Version':
            sys.exit('\nAPing version: %s (http://www.nongnu.org/aping)' % VERSION)

    for i in xrange(len(valid_options[0]) - 1):
        if lista.count(lista[i]) > 1:
            sys.exit('\nAPing: Duplicated options detected from a type')

    try:
        dst_address = valid_options[1][0]
        if len(valid_options[1]) > 1:
            sys.exit('\nAPing: more than one non-option specified')
    except IndexError:
        sys.exit('\nAPing: At least specify a target address\n            \rTry -h or --help for a list of available options')

    platform = sys.platform
    if 'freebsd' in platform:
        SIOCGIFADDR = 3223349537
        SIOCGIFCONF = 3221776676
    elif 'linux' in platform:
        SIOCGIFADDR = 35093
        SIOCGIFCONF = 35090
    else:
        print 'APing : unsupported OS! Behavior may be unexpected!'
    printopt(map(checkaddr, [bind_addr, dst_address])[1])


if __name__ == '__main__':
    main()