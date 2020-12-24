# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/lib/dotnessus_v2.py
# Compiled at: 2012-04-13 00:17:38
import sys, re, xml.etree.ElementTree as ET
from datetime import datetime
from StringIO import StringIO
MULTI_VALUED_ATTS = [
 'cve',
 'bid',
 'xref']
HOST_DATE_FORMAT = '%a %b %d %H:%M:%S %Y'
re_ip = re.compile('\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}')
re_wmi_ip = re.compile('IPAddress/IPSubnet.*?(?P<value>\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}\\.\\d{1,3})', re.I)
re_wmi_man = re.compile('Computer Manufacturer : (?P<manufacturer>.*?)\n.*?Computer Model : (?P<model>.*?)\n.*?Computer Memory : (?P<memory>\\d+)\\s', re.I | re.M | re.S)
re_shares = re.compile('- (?P<value>.*?)\n', re.I | re.M | re.S)
re_local_admins = re.compile('- (?P<value>.*?)\\s\\(', re.I | re.M | re.S)
re_wsus = re.compile('WUServer: (?P<wsus_server>.*?)\n.*?AUOptions: (?P<wsus_auoption>.*?)\n.*?Detect LastSuccessTime: (?P<wsus_lastdetect>.*?)\n.*?Download LastSuccessTime: (?P<wsus_lastdownload>.*?)\n.*?Install LastSuccessTime: (?P<wsus_lastinstall>.*?)\n.*?RebootRequired: (?P<wsus_rebootneeded>.*?)\n.*?ServiceStatus: (?P<wsus_auenabled>.*?)(\n|$)', re.I | re.M | re.S)
re_unix_memory = re.compile('Total memory: (?P<memory>\\d+)\\s', re.I)
re_unix_model = re.compile('Serial Number\\s+: (?P<serial>.*?)\\s.*?\nProduct Name\\s+: (?P<model>.*?)(\n|$)', re.I | re.M)
re_unix_cpu = re.compile('Current Speed\\s+: (?P<cpu_speed>.*?)\\s*\nManufacturer\\s+: (?P<cpu_vendor>.*?)\\s*\nFamily\\s+: (?P<cpu_model>.*?)\\s*\nExternal Clock\\s+: (?P<cpu_externalclock>.*?)\\s*\nVersion\\s+: (?P<cpu_version>.*?)\\s*\nType\\s+: (?P<cpu_type>.*?)($|\\s*\n)', re.I | re.M)
REGEX_MAP = {'24272': (
           'ips', re_wmi_ip, 'plugin_output', True), 
   '25203': (
           'ips', re_ip, 'plugin_output', True), 
   '24270': (
           '', re_wmi_man, 'description', False), 
   '10395': (
           'shares', re_shares, 'plugin_output', True), 
   '10902': (
           'local_admins', re_local_admins, 'plugin_output', True), 
   '10860': (
           'local_users', re_local_admins, 'plugin_output', True), 
   '55555': (
           '', re_wsus, 'description', False), 
   '45433': (
           '', re_unix_memory, 'plugin_output', False), 
   '35351': (
           '', re_unix_model, 'plugin_output', False), 
   '45432': (
           '', re_unix_cpu, 'plugin_output', False)}
LOCAL_IP_LIST = [
 '0.0.0.0',
 '127.0.0.1']

class Report(object):

    def __init__(self):
        self.name = None
        self.targets = []
        self.scan_start = None
        self.scan_end = None
        return

    def parse(self, xml_file, from_string=False):
        """Import .nessus file"""
        if from_string:
            xml_file = StringIO(xml_file)
        for event, elem in ET.iterparse(xml_file):
            if event == 'end' and elem.tag == 'Report':
                self.name = elem.attrib.get('name')
                continue
            elif event == 'end' and elem.tag != 'ReportHost':
                continue
            rh_obj = ReportHost(elem)
            if rh_obj:
                self.targets.append(rh_obj)
                if not self.scan_start:
                    self.scan_start = rh_obj.host_start
                if not self.scan_end:
                    self.scan_end = rh_obj.host_end
                if rh_obj.get('host_start'):
                    if rh_obj.host_start < self.scan_start:
                        self.scan_start = rh_obj.host_start
                if rh_obj.host_end > self.scan_end:
                    self.scan_end = rh_obj.host_end

    def __repr__(self):
        return '<Report: %s>' % self.name

    def get_target(self, name):
        """Returns a target object given a name"""
        for t in self.targets:
            if name.lower() == t.name.lower():
                return t


class ReportHost(object):

    def __init__(self, xml_report_host):
        self.name = None
        self.dead = False
        self.vulns = []
        self.name = xml_report_host.attrib.get('name')
        for n in xml_report_host.findall('HostProperties/tag'):
            setattr(self, n.attrib.get('name'), n.text)

        if self.get('HOST_START'):
            self.host_start = datetime.strptime(self.get('HOST_START'), HOST_DATE_FORMAT)
        else:
            self.dead = True
        self.host_end = datetime.strptime(self.get('HOST_END'), HOST_DATE_FORMAT)
        for ri in xml_report_host.findall('ReportItem'):
            ri_obj = ReportItem(ri)
            if ri_obj:
                self.vulns.append(ri_obj)

        xml_report_host.clear()
        for v in self.find_vuln(plugin_id='10180'):
            if 'dead' in str(v.get('plugin_output')):
                self.dead = True

        for plugin_id in REGEX_MAP:
            att, regex, dest_att, multi = REGEX_MAP[plugin_id]
            vulns = self.find_vuln(plugin_id=plugin_id)
            if multi:
                results = []
            for v in vulns:
                if multi:
                    setattr(self, att, regex.findall(v.get(dest_att)))
                else:
                    plugin_output = v.get(dest_att)
                    if not plugin_output:
                        continue
                    res = regex.search(v.get(dest_att))
                    if not res:
                        continue
                    if res.groupdict():
                        for k, v in res.groupdict().iteritems():
                            setattr(self, k, v)

                    else:
                        setattr(self, att, res.group())

        return

    def __repr__(self):
        return '<ReportHost: %s>' % self.name

    def get(self, attr):
        """Returns attribute value if it exists"""
        try:
            return getattr(self, attr)
        except AttributeError:
            return

        return

    def find_vuln(self, **kwargs):
        """Find a ReportItem given the search params"""
        results = []
        for r in self.vulns:
            match = True
            for k in kwargs:
                if kwargs.get(k) != r.get(k):
                    match = False

            if match:
                results.append(r)

        return results

    def get_ips(self, exclude_local=True):
        """Return a list of IPs for host"""
        ip_list = set()
        if re_ip.search(self.name):
            ip_list.add(self.name)
        if self.get('host-ip'):
            ip_list.add(self.get('host-ip'))
        if self.get('ips'):
            ip_list.update(self.ips)
        if exclude_local:
            for i in LOCAL_IP_LIST:
                if i in ip_list:
                    ip_list.remove(i)

        return list(ip_list)

    def get_open_ports(self):
        """Returns a dict of open ports found"""
        results = {}
        vulns = self.find_vuln(plugin_id='0')
        for v in vulns:
            proto = v.get('protocol')
            port = v.get('port')
            if proto not in results:
                results[proto] = []
            results[proto].append(port)

        return results

    def get_name(self):
        """Returns a friendly name for host"""
        if re_ip.search(self.name):
            if self.get('netbios-name'):
                return self.get('netbios-name').lower()
            else:
                if self.get('host-fqdn'):
                    return self.get('host-fqdn').lower()
                return self.name

        else:
            return self.name


class ReportItem(object):

    def __init__(self, xml_report_item):
        self.port = xml_report_item.attrib.get('port')
        self.svc_name = xml_report_item.attrib.get('svc_name')
        self.protocol = xml_report_item.attrib.get('protocol')
        self.severity = xml_report_item.attrib.get('severity')
        self.plugin_id = xml_report_item.attrib.get('pluginID')
        self.plugin_name = xml_report_item.attrib.get('pluginName')
        self.plugin_family = xml_report_item.attrib.get('pluginFamily')
        for m in MULTI_VALUED_ATTS:
            setattr(self, m, list())

        for n in xml_report_item.getchildren():
            if n.tag in MULTI_VALUED_ATTS:
                v = getattr(self, n.tag)
                v.append(n.text.strip())
                setattr(self, n.tag, v)
                continue
            setattr(self, n.tag, n.text.strip())

        xml_report_item.clear()

    def __repr__(self):
        return '<ReportItem: %s/%s %s %s>' % (self.port, self.protocol, self.plugin_id, self.plugin_name)

    def get(self, attr):
        """Returns attribute value if it exists"""
        try:
            return getattr(self, attr)
        except AttributeError:
            return

        return