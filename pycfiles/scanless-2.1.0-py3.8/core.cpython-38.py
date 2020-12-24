# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/scanless/core.py
# Compiled at: 2020-04-13 15:17:22
# Size of source mod 2**32: 8862 bytes
"""scanless.core"""
import os, re, bs4, requests
from random import choice
from scanless.exceptions import ScannerNotFound, ScannerRequestError
URL_HACKERTARGET = 'https://hackertarget.com/nmap-online-port-scanner/'
URL_IPFINGERPRINTS = 'https://www.ipfingerprints.com/scripts/getPortsInfo.php'
URL_SPIDERIP = 'https://spiderip.com/inc/port_scan.php'
URL_STANDINGTECH = 'https://portscanner.standingtech.com/portscan.php?port={0}&host={1}&protocol=TCP'
URL_T1SHOPPER = 'http://www.t1shopper.com/tools/port-scan/result/'
URL_VIEWDNS = 'https://viewdns.info/portscan/?host={0}'
URL_YOUGETSIGNAL = 'https://ports.yougetsignal.com/short-scan.php'
pwd = os.path.abspath(os.path.dirname(__file__))
nmap_file = os.path.join(pwd, 'static/nmap-services.txt')
ua_file = os.path.join(pwd, 'static/user-agents.txt')
NMAP_SERVICES = open(nmap_file, 'r').read().splitlines()
USER_AGENTS = open(ua_file, 'r').read().splitlines()
OUTPUT_TEMPLATE = 'PORT      STATE  SERVICE\n{lines}'
NETWORK_ERROR_MSG = 'Network error, see --debug for details.'

def lookup_service(port):
    for line in NMAP_SERVICES:
        if f"{port}/tcp" in line:
            return line.split()[0]


def generate_output(raw_data):
    lines = []
    for raw in raw_data:
        p, state = raw
        service = lookup_service(p)
        port = f"{p}/tcp"
        lines.append(f"{port:<9} {state:<6} {service}")
    else:
        return OUTPUT_TEMPLATE.format(lines=('\n'.join(lines)))


def parse(output):
    parsed_output = list()
    for line in output.split('\n'):
        if '/tcp' in line or '/udp' in line:
            port_str, state, service = line.split()
            port, protocol = port_str.split('/')
            parsed_output.append({'port':port, 
             'state':state, 
             'service':service, 
             'protocol':protocol})
        return parsed_output


class Scanless:

    def __init__(self, cli_mode=False):
        self.cli_mode = cli_mode
        self.session = requests.Session()
        self.scanners = {'hackertarget':self.hackertarget, 
         'ipfingerprints':self.ipfingerprints, 
         'spiderip':self.spiderip, 
         'standingtech':self.standingtech, 
         't1shopper':self.t1shopper, 
         'viewdns':self.viewdns, 
         'yougetsignal':self.yougetsignal}

    def scan(self, target, scanner='hackertarget'):
        if scanner not in self.scanners:
            raise ScannerNotFound(f"Unknown scanner, {scanner}.")
        return self.scanners[scanner](target)

    def _request--- This code section failed: ---

 L.  81         0  LOAD_FAST                'self'
                2  LOAD_METHOD              _randomize_user_agent
                4  CALL_METHOD_0         0  ''
                6  POP_TOP          

 L.  82         8  SETUP_FINALLY        42  'to 42'

 L.  83        10  LOAD_FAST                'self'
               12  LOAD_ATTR                session
               14  LOAD_ATTR                request
               16  LOAD_STR                 'POST'
               18  LOAD_FAST                'url'
               20  LOAD_FAST                'payload'
               22  LOAD_CONST               30
               24  LOAD_CONST               ('data', 'timeout')
               26  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
               28  STORE_FAST               'response'

 L.  84        30  LOAD_FAST                'response'
               32  LOAD_METHOD              raise_for_status
               34  CALL_METHOD_0         0  ''
               36  POP_TOP          
               38  POP_BLOCK        
               40  JUMP_FORWARD        100  'to 100'
             42_0  COME_FROM_FINALLY     8  '8'

 L.  85        42  DUP_TOP          
               44  LOAD_GLOBAL              Exception
               46  COMPARE_OP               exception-match
               48  POP_JUMP_IF_FALSE    98  'to 98'
               50  POP_TOP          
               52  STORE_FAST               'e'
               54  POP_TOP          
               56  SETUP_FINALLY        86  'to 86'

 L.  86        58  LOAD_FAST                'self'
               60  LOAD_ATTR                cli_mode
               62  POP_JUMP_IF_FALSE    74  'to 74'

 L.  87        64  POP_BLOCK        
               66  POP_EXCEPT       
               68  CALL_FINALLY         86  'to 86'
               70  LOAD_CONST               (None, 'ERROR')
               72  RETURN_VALUE     
             74_0  COME_FROM            62  '62'

 L.  88        74  LOAD_GLOBAL              ScannerRequestError
               76  LOAD_FAST                'e'
               78  CALL_FUNCTION_1       1  ''
               80  RAISE_VARARGS_1       1  'exception instance'
               82  POP_BLOCK        
               84  BEGIN_FINALLY    
             86_0  COME_FROM            68  '68'
             86_1  COME_FROM_FINALLY    56  '56'
               86  LOAD_CONST               None
               88  STORE_FAST               'e'
               90  DELETE_FAST              'e'
               92  END_FINALLY      
               94  POP_EXCEPT       
               96  JUMP_FORWARD        100  'to 100'
             98_0  COME_FROM            48  '48'
               98  END_FINALLY      
            100_0  COME_FROM            96  '96'
            100_1  COME_FROM            40  '40'

 L.  89       100  LOAD_FAST                'response'
              102  LOAD_ATTR                content
              104  LOAD_METHOD              decode
              106  LOAD_STR                 'utf-8'
              108  CALL_METHOD_1         1  ''
              110  LOAD_STR                 'OK'
              112  BUILD_TUPLE_2         2 
              114  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_EXCEPT' instruction at offset 66

    def _randomize_user_agent(self):
        self.session.headers['User-Agent'] = choice(USER_AGENTS)

    def _return_dict(self, raw_output, parsed_output):
        return {'raw':raw_output, 
         'parsed':parsed_output}

    def hackertarget(self, target):
        payload = {'theinput':target, 
         'thetest':'nmap', 
         'name_of_nonce_field':'5a8d0006b9', 
         '_wp_http_referer':'/nmap-online-port-scanner/'}
        scan_results, status = self._request(URL_HACKERTARGET, payload)
        if status != 'OK':
            return NETWORK_ERROR_MSG
        soup = bs4.BeautifulSoup(scan_results, 'html.parser')
        output = soup.findAll('pre', {'id': 'formResponse'})[0].string
        raw_output = output.replace('\\n', '\n').strip()
        parsed_output = parse(raw_output)
        return self._return_dict(raw_output, parsed_output)

    def ipfingerprints(self, target):
        payload = {'remoteHost':target, 
         'start_port':20, 
         'end_port':512, 
         'normalScan':'No', 
         'scan_type':'connect', 
         'ping_type':'none', 
         'os_detect':'on'}
        scan_results, status = self._request(URL_IPFINGERPRINTS, payload)
        if status != 'OK':
            return self._return_dict(NETWORK_ERROR_MSG, list())
        output = re.sub('<[^<]+?>', '', scan_results)
        raw_output = output.replace('\\n', '\n').replace('\\/', '/')[36:-46].strip()
        parsed_output = parse(raw_output)
        return self._return_dict(raw_output, parsed_output)

    def spiderip(self, target):
        ports = [
         21, 22, 25, 80, 110, 143, 443, 465, 993, 995, 1433, 3306, 3389,
         5900, 8080, 8443]
        payload = {'ip':target, 
         'language[]':ports}
        scan_results, status = self._request(URL_SPIDERIP, payload)
        if status != 'OK':
            return self._return_dict(NETWORK_ERROR_MSG, list())
        scan_results = scan_results.split('/images/')
        scan_results.pop(0)
        raw_data = list()
        for result, port in zip(scan_results, ports):
            if 'open' in result:
                raw_data.append((port, 'open'))
            else:
                raw_data.append((port, 'closed'))
        else:
            raw_output = generate_output(raw_data)
            parsed_output = parse(raw_output)
            return self._return_dict(raw_output, parsed_output)

    def standingtech(self, target):
        ports = [
         21, 22, 23, 25, 80, 110, 139, 143, 443, 445, 1433, 3306, 3389, 5900]
        raw_data = []
        for p in ports:
            scan_results, status = self._request((URL_STANDINGTECH.format(p, target)),
              method='GET')
            if status != 'OK':
                return self._return_dict(NETWORK_ERROR_MSG, list())
            if 'open' in scan_results:
                raw_data.append((p, 'open'))
            else:
                raw_data.append((p, 'closed'))
        else:
            raw_output = generate_output(raw_data)
            parsed_output = parse(raw_output)
            return self._return_dict(raw_output, parsed_output)

    def t1shopper(self, target):
        ports = [
         21, 23, 25, 80, 110, 139, 445, 1433, 1521, 1723, 3306, 3389,
         5900, 8080]
        payload = {'scan_host':target, 
         'port_array[]':ports}
        scan_results, status = self._request(URL_T1SHOPPER, payload)
        if status != 'OK':
            return self._return_dict(NETWORK_ERROR_MSG, list())
        soup = bs4.BeautifulSoup(scan_results, 'html.parser')
        raw_data = list()
        for tt, port in zip(soup.find('pre').find_all('tt'), ports):
            if tt.text.find("isn't") > -1:
                raw_data.append((port, 'closed'))
            else:
                raw_data.append((port, 'open'))
        else:
            raw_output = generate_output(raw_data)
            parsed_output = parse(raw_output)
            return self._return_dict(raw_output, parsed_output)

    def viewdns(self, target):
        ports = [
         21, 22, 23, 25, 53, 80, 110, 139, 143, 443, 445, 1433, 1521,
         3306, 3389]
        scan_results, status = self._request((URL_VIEWDNS.format(target)), method='GET')
        if status != 'OK':
            return self._return_dict(NETWORK_ERROR_MSG, list())
        soup = bs4.BeautifulSoup(scan_results, 'html.parser')
        table, rows = soup.find('table'), soup.findAll('tr')
        raw_data = list()
        for tr, port in zip(rows[7:22], ports):
            cols = str(tr.findAll('td'))
            if 'error.GIF' in cols:
                raw_data.append((port, 'closed'))
            else:
                raw_data.append((port, 'open'))
        else:
            raw_output = generate_output(raw_data)
            parsed_output = parse(raw_output)
            return self._return_dict(raw_output, parsed_output)

    def yougetsignal(self, target):
        ports = [
         21, 22, 23, 25, 53, 80, 110, 115, 135, 139, 143, 194, 443, 445,
         1433, 3306, 3389, 5632, 5900, 6112]
        payload = {'remoteAddress': target}
        scan_results, status = self._request(URL_YOUGETSIGNAL, payload)
        if status != 'OK':
            return self._return_dict(NETWORK_ERROR_MSG, list())
        soup = bs4.BeautifulSoup(scan_results, 'html.parser')
        imgs = soup.findAll('img')
        raw_data = list()
        for img, port in zip(imgs, ports):
            if 'red' in str(img):
                raw_data.append((port, 'closed'))
            else:
                raw_data.append((port, 'open'))
        else:
            raw_output = generate_output(raw_data)
            parsed_output = parse(raw_output)
            return self._return_dict(raw_output, parsed_output)