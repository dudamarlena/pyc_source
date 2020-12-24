# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/pfhb/classes.py
# Compiled at: 2019-02-25 16:14:48
# Size of source mod 2**32: 9631 bytes
import socket, redis, re, os, subprocess
from syslog import syslog, LOG_INFO, LOG_ERR
from ipwhois.net import Net
from ipwhois.asn import IPASN, ASNOrigin
from configparser import ConfigParser, NoOptionError, NoSectionError
from .settings import load_settings
TAG_PASS_TABLE = '# PFHB:PASS_TABLE'
TAG_BLOCK_TABLE = '# PFHB:BLOCK_TABLE'
TAG_GROUPS_TABLES = '# PFHB:GROUPS_TABLES'
TAG_RULES = '# PFHB:RULES'

class PacketFilterHostBlocker(object):

    def __init__(self, settings={}, settings_path=None, debug=False):
        self.debug = debug
        self.settings = load_settings(path=settings_path)
        if settings:
            self.settings = settings
        self.redis = (redis.Redis)(**self.settings['REDIS']) if self.settings.get('STORAGE_TYPE', 'file') == 'redis' else None
        self.insane_mode = self.settings.get('INSANE_MODE')
        self.block_domain_networks = self.settings.get('BLOCK_DOMAIN_NETWORKS')
        self.resolve_www_prefix = self.settings.get('RESOLVE_WWW_PREFIX')
        self.logging = self.settings.get('USE_SYSLOG')
        self.output('Initializing (Storage: {})'.format('Redis' if self.redis else 'File'))

    def output(self, msg, syslog_level=LOG_INFO):
        """ Message output - for debugging nor logging. """
        if self.debug:
            print(msg)
        if self.logging:
            syslog(syslog_level, msg)

    def __get_asn_cidr(self, ip):
        asn = IPASN(Net(ip)).lookup()
        return asn.get('asn_cidr')

    def __get_asn_origin(self, ip):
        asn = IPASN(Net(ip)).lookup()
        return asn.get('asn')

    def __get_asn_nets(self, ip):
        asn_origin = self._PacketFilterHostBlocker__get_asn_origin(ip)
        origin = ASNOrigin(Net(ip))
        lookup = origin.lookup(asn=('AS{}'.format(asn_origin)), asn_methods=[
         'whois'])
        return lookup.get('nets')

    def get_nets_to_block(self, ip):
        nets_to_block = []
        if self.block_domain_networks:
            nets_to_block.append(self._PacketFilterHostBlocker__get_asn_cidr(ip))
        if self.insane_mode:
            try:
                nets = self._PacketFilterHostBlocker__get_asn_nets(ip)
            except:
                nets = []

            if nets:
                self.output('Networks found for IP: {} = {}'.format(ip, len(nets)))
                nets_to_block += [net.get('cidr') for net in nets]
            else:
                self.output('No Networks for IP: {}! Getting ASN CIDR...'.format(ip))
        return nets_to_block

    def nslookup(self, domain):
        """ Domain name lookup """
        if domain:
            self.output('NSLookup of "{}"...'.format(domain))
            socket.setdefaulttimeout(2)
            try:
                hosts = socket.gethostbyname_ex(domain)
            except:
                self.output('  - failed!')
                return
                resolved = hosts[2] if len(hosts) == 3 else None
                self.output('  - resolved: {}'.format(resolved))
                return resolved

    def load_domains(self):
        groups = {}
        domains_count = 0
        if not self.redis:
            config = ConfigParser()
            config.read(self.settings['DOMAINS_FILE_PATH'])
            for group in config.sections():
                try:
                    domains = config.get(group, 'domains')
                except (NoSectionError, NoOptionError):
                    pass
                else:
                    group = ''.join(re.findall('[a-zA-Z0-9]', group, re.I)).lower()
                    groups[group] = domains.split()
                    domains_count += len(groups[group])

        else:
            for group in self.redis.keys('domains_*'):
                domains = self.redis.get(group)
                if isinstance(domains, bytes):
                    domains = domains.decode('utf-8')
                group = group.decode('utf-8').split('_')[(-1)] if isinstance(group, bytes) else group.split('_')[(-1)]
                groups[group] = domains.split(',')
                domains_count += len(groups[group])

        self.output('Groups: {}'.format(len(groups.keys())))
        self.output('Domains: {}'.format(domains_count))
        return groups

    def resolve_domains(self):
        """ Get all domain groups stored on Redis to resolve each domain
        name and store it again and generate all PF rules.
        """
        asns = {}
        groups = self.load_domains()
        for group in groups:
            ips = []
            for domain in groups[group]:
                domains_to_resolve = [domain]
                if self.resolve_www_prefix:
                    domains_to_resolve.append(domain[4:] if domain.startswith('www.') else 'www.{}'.format(domain))
                for d2r in domains_to_resolve:
                    resolved = self.nslookup(d2r)
                    if resolved:
                        for ip in resolved:
                            if ip and ip not in ips:
                                ips.append(ip)

            asns[group] = []
            for ip in ips:
                asns[group].append(ip)
                nets = self.get_nets_to_block(ip)
                if nets:
                    asns[group].extend(nets)

            if self.redis:
                self.redis.set('ips_{}'.format(group), ','.join(ips))

        return asns

    def generate_pf_rules(self):
        ip_groups = self.resolve_domains()
        pass_tbl = 'table <ips_to_pass> { %s }' % ', '.join(self.settings['PF_IPS_TO_PASS'])
        block_tbl = 'table <ips_to_block> { %s }' % ', '.join(self.settings['PF_IPS_TO_BLOCK'])
        pass_rule = 'pass in quick proto tcp from <ips_to_pass> to <group_{}>'
        block_rule = 'block in {} quick proto tcp from <ips_to_block> to <group_{}>'
        group_tbls = []
        pass_rules = []
        block_rules = []
        for group in ip_groups:
            group_tbls.append('table <group_%s> { %s }' % (
             group, ', '.join(ip_groups[group])))
            pass_rules.append(pass_rule.format(group))
            block_rules.append(block_rule.format('log' if self.settings['PF_LOG_RULES'] else '', group))

        rules = pass_rules + block_rules
        self.output('Rules to be merged: {}'.format(len(rules)))
        return {'tables':{'pass':pass_tbl, 
          'block':block_tbl, 
          'groups':group_tbls}, 
         'rules':rules}

    def run(self):
        pf_conf_source = self.settings.get('PF_CONFIG_SOURCE', '/etc/pf.conf')
        pf_conf_target = self.settings.get('PF_CONFIG_TARGET', '/etc/pfhb/pf-merged.conf')
        if pf_conf_source == pf_conf_target:
            raise Exception('Nope! Source and Target pf.conf files cannot be the same. Please, keep your Source pf.conf file safe!')
        with open(pf_conf_source, 'r') as (fs):
            source_content = fs.read()
            if isinstance(source_content, bytes):
                source_content = source_content.decode('utf-8')
        if any([TAG_BLOCK_TABLE not in source_content,
         TAG_GROUPS_TABLES not in source_content,
         TAG_RULES not in source_content]):
            raise Exception('Impossible to merge. There are missing tags at source file {}.'.format(pf_conf_source))
        pf_stmts = self.generate_pf_rules()
        pass_table = pf_stmts['tables'].get('pass')
        block_table = pf_stmts['tables'].get('block')
        groups_tables = pf_stmts['tables'].get('groups')
        rules = pf_stmts.get('rules')
        with open(pf_conf_target, 'w+') as (ft):
            merged_content = source_content.replace(TAG_PASS_TABLE, pass_table)
            merged_content = merged_content.replace(TAG_BLOCK_TABLE, block_table)
            merged_content = merged_content.replace(TAG_GROUPS_TABLES, '\n'.join(groups_tables))
            merged_content = merged_content.replace(TAG_RULES, '\n'.join(rules))
            ft.write(merged_content)
        if os.path.isfile(pf_conf_target):
            cmd = '{} {}'.format(self.settings.get('PF_RELOAD_COMMAND').strip(), pf_conf_target)
            try:
                subprocess.call(cmd.split())
            except FileNotFoundError:
                self.output('Impossible to call command to reload PF.', syslog_level=LOG_ERR)