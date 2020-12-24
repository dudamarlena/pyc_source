# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/sk/seckiss/rfw/rfw/iptables.py
# Compiled at: 2014-03-26 05:26:42
import inspect, re, subprocess, logging, json
from collections import namedtuple
from threading import RLock
log = logging.getLogger(('lib.{}').format(__name__))
log.addHandler(logging.NullHandler())
IPTABLES_HEADERS = [
 'num', 'pkts', 'bytes', 'target', 'prot', 'opt', 'in', 'out', 'source', 'destination']
RULE_ATTRS = ['chain', 'num', 'pkts', 'bytes', 'target', 'prot', 'opt', 'inp', 'out', 'source', 'destination', 'extra']
RULE_TARGETS = ['DROP', 'ACCEPT', 'REJECT']
RULE_CHAINS = ['INPUT', 'OUTPUT', 'FORWARD']
RuleProto = namedtuple('Rule', RULE_ATTRS)

class Rule(RuleProto):
    """Lightweight immutable value object to store iptables rule
    """

    def __new__(_cls, *args, **kwargs):
        """Construct Rule tuple from a list or a dictionary
        """
        if args:
            if len(args) != 1:
                raise ValueError('The Rule constructor takes either list, dictionary or named properties')
            props = args[0]
            if isinstance(props, list):
                return RuleProto.__new__(_cls, *props)
            if isinstance(props, dict):
                d = {'chain': None, 'num': None, 'pkts': None, 'bytes': None, 'target': None, 'prot': 'all', 'opt': '--', 'inp': '*', 'out': '*', 'source': '0.0.0.0/0', 'destination': '0.0.0.0/0', 'extra': ''}
                d.update(props)
                return RuleProto.__new__(_cls, **d)
            raise ValueError('The Rule constructor takes either list, dictionary or named properties')
        else:
            if kwargs:
                return RuleProto.__new__(_cls, **kwargs)
            else:
                return RuleProto.__new__(_cls, [])

        return

    def __eq__(self, other):
        """Rule equality should ignore such parameters like num, pkts, bytes
        """
        if isinstance(other, self.__class__):
            return self.chain == other.chain and self.target == other.target and self.prot == other.prot and self.opt == other.opt and self.inp == other.inp and self.out == other.out and self.source == other.source and self.destination == other.destination
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)


class Iptables:
    lock = RLock()
    ipt_path = 'iptables'

    def __init__(self, rules):
        if inspect.stack()[1][3] == 'load':
            self.rules = rules
        else:
            raise Exception('Use Iptables.load() to create an instance with loaded current list of rules')

    @staticmethod
    def load():
        rules = Iptables._iptables_list()
        inst = Iptables(rules)
        return inst

    @staticmethod
    def verify_install():
        """Check if iptables installed
        """
        try:
            Iptables.exe(['-h'])
        except OSError as e:
            raise Exception(('Could not find {}. Check if it is correctly installed and if the path is correct.').format(Iptables.ipt_path))

    @staticmethod
    def verify_permission():
        """Check if root - iptables installed but cannot list rules
        """
        try:
            Iptables.exe(['-n', '-L', 'OUTPUT'])
        except subprocess.CalledProcessError as e:
            raise Exception(('No sufficient permission to run {}. You must be root.').format(Iptables.ipt_path))

    @staticmethod
    def verify_original():
        pass

    @staticmethod
    def _iptables_list():
        """List and parse iptables rules. Do not call directly. Use Iptables.load().rules instead
        return list of rules of type Rule.
        """
        rules = []
        out = Iptables.exe(['-n', '-L', '-v', '-x', '--line-numbers'])
        chain = None
        header = None
        for line in out.split('\n'):
            line = line.strip()
            if not line:
                chain = None
                continue
            m = re.match('Chain (\\w+) .*', line)
            if m and m.group(1) in RULE_CHAINS:
                chain = m.group(1)
                continue
            if 'source' in line and 'destination' in line:
                assert line.split() == IPTABLES_HEADERS
                continue
            if chain:
                columns = line.split()
                if columns and columns[0].isdigit():
                    extra = (' ').join(columns[10:])
                    columns = columns[:10]
                    columns.append(extra)
                    columns.insert(0, chain)
                    rule = Rule(columns)
                    rules.append(rule)

        return rules

    @staticmethod
    def rule_to_command(r):
        """Convert Rule object r to the list representing iptables command arguments like: 
        ['INPUT', '-p', 'tcp', '-d', '0.0.0.0/0', '-s', '1.2.3.4', '-j', 'ACCEPT']
        It is assumed that the rule is from trusted source (from Iptables.find())
        """
        assert r.chain == 'INPUT' or r.chain == 'OUTPUT' or r.chain == 'FORWARD'
        lcmd = []
        lcmd.append(r.chain)
        if r.prot != 'all':
            lcmd.append('-p')
            lcmd.append(r.prot)
        if r.extra:
            es = r.extra.split()
            for e in es:
                if e[:4] == 'dpt:':
                    dport = e.split(':')[1]
                    lcmd.append('--dport')
                    lcmd.append(dport)
                if e[:4] == 'spt:':
                    sport = e.split(':')[1]
                    lcmd.append('--sport')
                    lcmd.append(sport)

        if r.destination != '0.0.0.0/0':
            lcmd.append('-d')
            lcmd.append(r.destination)
        if r.source != '0.0.0.0/0':
            lcmd.append('-s')
            lcmd.append(r.source)
        lcmd.append('-j')
        lcmd.append(r.target)
        return lcmd

    @staticmethod
    def exe_rule(modify, rule):
        assert modify == 'I' or modify == 'D'
        lcmd = Iptables.rule_to_command(rule)
        return Iptables.exe(['-' + modify] + lcmd)

    @staticmethod
    def exe(lcmd):
        cmd = [Iptables.ipt_path] + lcmd
        try:
            log.debug(('Iptables.exe(): {}').format((' ').join(cmd)))
            with Iptables.lock:
                out = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
            if out:
                log.debug(('Iptables.exe() output: {}').format(out))
            return out
        except subprocess.CalledProcessError as e:
            log.error(("Error code {} returned when called '{}'. Command output: '{}'").format(e.returncode, e.cmd, e.output))
            raise e

    @staticmethod
    def read_simple_rules(chain=None):
        assert chain is None or chain in RULE_CHAINS
        rules = []
        ipt = Iptables.load()
        if chain == 'INPUT' or chain is None:
            input_rules = ipt.find({'target': RULE_TARGETS, 'chain': ['INPUT'], 'destination': ['0.0.0.0/0'], 'out': ['*'], 'prot': ['all'], 'extra': ['']})
            rules.extend(input_rules)
        if chain == 'OUTPUT' or chain is None:
            output_rules = ipt.find({'target': RULE_TARGETS, 'chain': ['OUTPUT'], 'source': ['0.0.0.0/0'], 'inp': ['*'], 'prot': ['all'], 'extra': ['']})
            rules.extend(output_rules)
        if chain == 'FORWARD' or chain is None:
            forward_rules = ipt.find({'target': RULE_TARGETS, 'chain': ['FORWARD'], 'prot': ['all'], 'extra': ['']})
            rules.extend(forward_rules)
        return rules

    def find(self, query):
        """Find rules based on query
        For example:
            query = {'chain': ['INPUT', 'OUTPUT'], 'prot': ['all'], 'extra': ['']}
            is searching for the rules where:
            (chain == INPUT or chain == OUTPUT) and prot == all and extra == ''
        """
        ret = []
        for r in self.rules:
            matched_all = True
            for param, vals in query.items():
                rule_val = getattr(r, param)
                if rule_val not in vals:
                    matched_all = False
                    break

            if matched_all:
                ret.append(r)

        return ret