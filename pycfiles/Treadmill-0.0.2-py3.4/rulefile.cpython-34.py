# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/treadmill/rulefile.py
# Compiled at: 2017-04-03 02:32:49
# Size of source mod 2**32: 6823 bytes
"""Functions for handling the network rules directory files"""
import errno, logging, os, re
from . import firewall
from . import fs
_LOGGER = logging.getLogger(__name__)
_DNAT_FILE_PATTERN = 'dnat:{proto}:{orig_ip}:{orig_port}-{new_ip}:{new_port}'
_PASSTHROUGH_FILE_PATTERN = 'passthrough:{src_ip}-{dst_ip}'
_DNAT_FILE_RE = re.compile('^' + _DNAT_FILE_PATTERN.format(proto='(?P<proto>(?:tcp|udp))', orig_ip='(?P<orig_ip>(?:\\d{1,3}\\.){3}\\d{1,3})', orig_port='(?P<orig_port>\\d{1,5})', new_ip='(?P<new_ip>(?:\\d{1,3}\\.){3}\\d{1,3})', new_port='(?P<new_port>\\d{1,5})') + '$')
_PASSTHROUGH_FILE_RE = re.compile('^' + _PASSTHROUGH_FILE_PATTERN.format(src_ip='(?P<src_ip>(?:\\d{1,3}\\.){3}\\d{1,3})', dst_ip='(?P<dst_ip>(?:\\d{1,3}\\.){3}\\d{1,3})') + '$')

class RuleMgr(object):
    __doc__ = 'Network rule manager.\n\n    :param ``str`` base_path:\n        Base directory that will contain all the rule files\n    :param ``str`` owner_path:\n        Base directory that will contain all the rule owners.\n    '
    __slots__ = ('_base_path', '_owner_path')

    def __init__(self, base_path, owner_path):
        fs.mkdir_safe(base_path)
        self._base_path = os.path.realpath(base_path)
        self._owner_path = os.path.realpath(owner_path)

    def initialize(self):
        """Initialize the network folder."""
        for rule in os.listdir(self._base_path):
            os.unlink(os.path.join(self._base_path, rule))

    @property
    def path(self):
        """Currently managed rules directory.

        :returns:
            ``str`` -- Rules directory.
        """
        return self._base_path

    @staticmethod
    def get_rule(rulespec):
        """Parse a forwarding rule spec into a usable firewall rule.

        :param ``str`` rulespec:
            Forward rule in string form
        :returns:
            ``DNATRule``|``PassThroughRule`` | ``None`` -- A tuple of the table
            and the parsed rule. If parsing failed, returns ``None``
        """
        match = _DNAT_FILE_RE.match(rulespec)
        if match:
            data = match.groupdict()
            return firewall.DNATRule(data['proto'], data['orig_ip'], int(data['orig_port']), data['new_ip'], int(data['new_port']))
        match = _PASSTHROUGH_FILE_RE.match(rulespec)
        if match:
            data = match.groupdict()
            return firewall.PassThroughRule(data['src_ip'], data['dst_ip'])

    def get_rules(self):
        """Scrapes the network directory for redirect files.

        :returns:
            ``set`` -- Set of rules in the rules directory
        """
        rules = set()
        for entry in os.listdir(self._base_path):
            rule = self.get_rule(entry)
            if rule:
                rules.add(rule)
            else:
                _LOGGER.warning('Ignoring unparseable file %r', entry)

        return rules

    def create_rule(self, rule, owner):
        """Creates a symlink who's name represents the port redirection.

        :param ``DNATRule | PassThroughRule`` rule:
            Firewall Rule
        :param ``str`` owner:
            Unique container ID of the owner of the rule
        """
        filename = self._filenameify(rule)
        rule_file = os.path.join(self._base_path, filename)
        owner_file = os.path.join(self._owner_path, owner)
        try:
            os.symlink(os.path.relpath(owner_file, self._base_path), rule_file)
            _LOGGER.info('Created %r for %r', filename, owner)
        except OSError as err:
            if err.errno == errno.EEXIST:
                existing_owner = os.path.basename(os.readlink(rule_file))
                if existing_owner != owner:
                    raise
            else:
                raise

    def unlink_rule(self, rule, owner):
        """Unlinks the empty file who's name represents the port redirection.

        :param ``DNATRule | PassThroughRule`` rule:
            Firewall Rule
        :param ``str`` owner:
            Unique container ID of the owner of the rule
        """
        filename = self._filenameify(rule)
        rule_file = os.path.join(self._base_path, filename)
        try:
            existing_owner = os.path.basename(os.readlink(rule_file))
            if existing_owner != owner:
                _LOGGER.critical('%r tried to free %r that it does not own', owner, filename)
                return
            os.unlink(rule_file)
            _LOGGER.debug('Removed %r', filename)
        except OSError as err:
            if err.errno == errno.ENOENT:
                _LOGGER.info('Network rule %r does not exist.', rule_file)
            else:
                _LOGGER.exception('Unable to remove network rule: %r', rule_file)
                raise

    def garbage_collect(self):
        """Garbage collect all rules without owner.
        """
        for rule in os.listdir(self._base_path):
            link = os.path.join(self._base_path, rule)
            try:
                os.stat(link)
            except OSError as err:
                if err.errno == errno.ENOENT:
                    _LOGGER.warning('Reclaimed: %r', rule)
                    try:
                        os.unlink(link)
                    except OSError as err:
                        if err.errno == errno.ENOENT:
                            pass
                        else:
                            raise

                else:
                    raise

    @staticmethod
    def _filenameify(rule):
        """Format the rule using rule patterns

        :param ``DNATRule | PassThroughRule`` rule:
            Firewall Rule
        :returns:
            ``str`` -- Filename representation of the rule
        """
        if isinstance(rule, firewall.DNATRule):
            return _DNAT_FILE_PATTERN.format(proto=rule.proto, orig_ip=rule.orig_ip, orig_port=rule.orig_port, new_ip=rule.new_ip, new_port=rule.new_port)
        if isinstance(rule, firewall.PassThroughRule):
            return _PASSTHROUGH_FILE_PATTERN.format(src_ip=rule.src_ip, dst_ip=rule.dst_ip)
        raise ValueError('Invalid rule: %r' % (rule,))