# uncompyle6 version 3.7.4
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/net6mon/pmap.py
# Compiled at: 2006-06-19 03:29:49
import os, tempfile, socket, threading, Queue, time
from xml.dom import minidom
VERSION = '0.1.3'
NAME = 'pmap'
VERBOSE = 0

def vprint(message):
    if VERBOSE:
        print 'pmap: ', message


def check_nmap():
    """Checks if nmap is installed on system and returns the version if it is"""
    data = os.popen('nmap --version').read()
    if 'nmap version' not in data:
        vprint('Nmap not found')
        return None
    nmap_version = data.split()[2]
    return nmap_version
    return


def scan_host(host, args=None):
    """Scans a host on the network with nmap, then parses the XML output.
       Returns a dictonary with all of the information"""
    filename = tempfile.mkstemp(prefix='pynmap-')[1]
    nmap_output = os.popen('nmap %s -oX %s' % (host, filename)).read()
    info = parse_file(filename)
    info['.nmap_output'] = nmap_output
    return info


def ping_sweep(network):
    """Use's nmap's ping sweep (-sP) scan to find live hosts on the network.
    Returns a list of the live host's ip address's"""
    filename = tempfile.mkstemp(prefix='pynmap-')[1]
    vprint('Ping Scanning %s and saving data to %s' % (network, filename))
    nmap_output = os.popen('nmap -sP %s -oX %s' % (network, filename)).read()
    info = parse_file(filename)
    if not info:
        return None
    host_list = []
    for host in info['hosts'].keys():
        if info['hosts'][host]['state'] == 'up':
            if host not in host_list:
                host_list.append(host.encode())

    return host_list
    return


def parse_file(filename):
    stime = time.time()
    root = {}
    try:
        dom = minidom.parse(filename)
    except:
        vprint('Bad XML File: %s' % filename)
        return

    nmaprun = dom.getElementsByTagName('nmaprun')[0]
    root['.scanner'] = nmaprun.getAttribute('scanner')
    root['.args'] = nmaprun.getAttribute('args')
    root['.starttime'] = nmaprun.getAttribute('start')
    root['.starttimestr'] = nmaprun.getAttribute('startstr')
    root['.nmapversion'] = nmaprun.getAttribute('version')
    root['.xmloutputversion'] = nmaprun.getAttribute('xmloutputversion')
    try:
        scaninfo = dom.getElementsByTagName('scaninfo')[0]
        root['.scantype'] = scaninfo.getAttribute('type')
        root['.scanprotocol'] = scaninfo.getAttribute('protocol')
        root['.numservices'] = scaninfo.getAttribute('numservices')
        root['.scannedports'] = scaninfo.getAttribute('services')
    except IndexError:
        pass

    verbose = dom.getElementsByTagName('verbose')[0]
    root['.verboselevel'] = verbose.getAttribute('level')
    debugging = dom.getElementsByTagName('debugging')[0]
    root['.debugginglevel'] = debugging.getAttribute('level')
    root['hosts'] = {}
    hosts = dom.getElementsByTagName('host')
    for (hindex, host) in enumerate(hosts):
        root['hosts'][hindex] = {}
        hroot = root['hosts'][hindex]

        def elem_filter(elem):
            try:
                data = elem.data
                return False
            except AttributeError:
                return True

        for elem in filter(elem_filter, host.childNodes):
            if elem.nodeName == 'status':
                hroot['state'] = elem.getAttribute('state')
            if elem.nodeName == 'address':
                addrtype = elem.getAttribute('addrtype')
                if addrtype == 'ipv4':
                    ipv4 = elem.getAttribute('addr')
                    root['hosts'][ipv4] = hroot
                    hroot = root['hosts'][ipv4]
                    del root['hosts'][hindex]
                    hroot['ipv4addr'] = ipv4
                if addrtype == 'ipv6':
                    hroot['ipc6addr'] = elem.getAttribute('addr')
                if addrtype == 'mac':
                    hroot['macaddr'] = elem.getAttribute('addr')
                    hroot['cardvendor'] = elem.getAttribute('vendor')
            if elem.nodeName == 'hostnames':
                hostnames = elem.getElementsByTagName('hostname')
                for hostname in hostnames:
                    hroot['hostname'] = hostname.getAttribute('name')
                    hroot['.hostnametype'] = hostname.getAttribute('type')

            if elem.nodeName == 'ports':
                ports = elem.getElementsByTagName('port')
                hroot['ports'] = {}
                for port in ports:
                    portid = port.getAttribute('portid')
                    hroot['ports'][portid] = {}
                    proot = hroot['ports'][portid]
                    proot['portid'] = port.getAttribute('portid')
                    proot['protocol'] = port.getAttribute('protocol')
                    for pelem in filter(elem_filter, port.childNodes):
                        if pelem.tagName == 'state':
                            proot['state'] = pelem.getAttribute('state')
                        if pelem.tagName == 'service':
                            proot['service'] = pelem.getAttribute('name')
                            proot['product'] = pelem.getAttribute('product')
                            proot['version'] = pelem.getAttribute('version')
                            proot['extrainfo'] = pelem.getAttribute('extrainfo')
                            proot['.method'] = pelem.getAttribute('method')
                            proot['ostype'] = pelem.getAttribute('ostype')
                            proot['devicetype'] = pelem.getAttribute('devicetype')
                            proot['.conf'] = pelem.getAttribute('conf')

            if elem.nodeName == 'portused':
                state = elem.getAttribute('state')
                if state == 'open':
                    hroot['.openportusedId'] = elem.getAttribute('portid')
                    hroot['.openportusedProtocol'] = elem.getAttribute('proto')
                if state == 'closed':
                    hroot['.closedportusedId'] = elem.getAttribute('portid')
                    hroot['.closedportusedProtcol'] = elem.getAttribute('proto')
            if elem.nodeName == 'osclass':
                hroot['ostype'] = elem.getAttribute('type')
                hroot['osvendor'] = elem.getAttribute('vendor')
                hroot['osfamily'] = elem.getAttribute('osfamily')
                hroot['osgen'] = elem.getAttribute('osgen')
                hroot['.osclassaccuracy'] = elem.getAttribute('osaccuracy')
            if elem.nodeName == 'osmatch':
                hroot['osname'] = elem.getAttribute('name')
                hroot['.osmatchaccuracy'] = elem.getAttribute('accuracy')
                hroot['.osmatchline'] = elem.getAttribute('line')
            if elem.nodeName == 'uptime':
                hroot['uptime'] = elem.getAttribute('seconds')
                hroot['lastboot'] = elem.getAttribute('lastboot')
            if elem.nodeName == 'tcpsequence':
                hroot['.tcpsequenceIndex'] = elem.getAttribute('index')
                hroot['.tcpsequenceClass'] = elem.getAttribute('class')
                hroot['.tcpsequenceDifficulty'] = elem.getAttribute('difficulty')
                hroot['.tcpsequenceValues'] = elem.getAttribute('values')
            if elem.nodeName == 'ipidsequence':
                hroot['.ipidsequenceClass'] = elem.getAttribute('class')
                hroot['.ipidsequenceValues'] = elem.getAttribute('values')
            if elem.nodeName == 'tcptssequence':
                hroot['.tcptssequenceClass'] = elem.getAttribute('class')
                hroot['.tcptssequenceValues'] = elem.getAttribute('values')

    finished = dom.getElementsByTagName('finished')[0]
    root['_endtime'] = finished.getAttribute('time')
    root['_endtimestr'] = finished.getAttribute('timestr')
    hosts = dom.getElementsByTagName('hosts')[0]
    root['hostsup'] = hosts.getAttribute('up')
    root['hostsdown'] = hosts.getAttribute('down')
    root['totalhosts'] = hosts.getAttribute('total')

    def clean(root):
        """Removes any keys that link to None values and Removes Unicode Strings"""
        sub_dicts = [
         root]
        while len(sub_dicts) > 0:
            dict = sub_dicts.pop()
            for key in dict.keys():
                if type(dict[key]) == type({'dict': 'tionary'}):
                    sub_dicts.append(dict[key])
                elif not dict[key]:
                    del dict[key]
                else:
                    dict[key] = dict[key].encode()

        return root

    return clean(root)


def port_scan(host, **kwargs):
    """Scan a network host to find open ports"""
    MAXTHREADS = 10
    PORT_RANGE = (0, 6001)
    SCAN_TYPE = 'TCP'

    class Scanner(threading.Thread):
        __module__ = __name__

        def __init__(self, qin, qout):
            threading.Thread.__init__(self)
            self.setDaemon(1)
            self._running = True
            self.qin = qin
            self.qout = qout

        def run(self):
            while self._running:
                if qin.empty():
                    self._running = False
                    break
                else:
                    port = self.qin.get()
                if SCAN_TYPE == 'TCP':
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.settimeout(0.25)
                    try:
                        s.connect((host, port))
                        self.qout.put(port)
                    except socket.error:
                        pass
                    else:
                        s.close()
                elif SCAN_TYPE == 'UDP':
                    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                    s.connect((host, port))
                    try:
                        s.send('')
                        s.send('')
                        self.qout.put(port)
                    except socket.error:
                        pass

    qin = Queue.Queue()
    qout = Queue.Queue()
    scan_threads = [ Scanner(qin, qout) for t in range(MAXTHREADS) ]
    for thread in scan_threads:
        thread.start()

    ports = [ port for port in range(PORT_RANGE[0], PORT_RANGE[1]) ]
    for port in ports:
        qin.put(port)

    open_ports = []
    while not qin.empty():
        pass

    while not qout.empty():
        open_ports.append(qout.get())

    return open_ports


def dumb_scan(host):
    """Very Simple Port Scan"""
    ports = [ p for p in range(6001) ]
    open_ports = []
    while len(ports) > 0:
        port = ports.pop()
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.connect((host, port))
            open_ports.append(port)
        except socket.error:
            pass

        s.close()

    return open_ports


def get_hosts_ips(root):
    return root['hosts'].keys()


def get_up_hosts(root):
    host_list = []
    for host in root['hosts'].keys():
        h = root['hosts'][host]
        if h['state'] == 'up':
            host_list.append(host)

    return host_list


def get_open_ports(host):
    return root['hosts'][host]['ports'].keys()


if __name__ == '__main__':
    if not check_nmap():
        print 'Nmap not installed'
        print 'Your open ports ', port_scan('127.0.0.1')
    else:
        print scan_host('127.0.0.1')