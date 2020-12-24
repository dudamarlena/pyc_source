# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/chkconfig.py
# Compiled at: 2019-05-16 13:41:33
"""
ChkConfig - command ``chkconfig``
=================================
"""
from collections import namedtuple
from .. import parser, CommandParser
import re
from insights.specs import Specs

@parser(Specs.chkconfig)
class ChkConfig(CommandParser):
    """
    A parser for working with data gathered from `chkconfig` utility.

    Sample input data is shown as `content` in the examples below.

    Examples:
        >>> content = '''
        ... auditd         0:off   1:off   2:on    3:on    4:on    5:on    6:off
        ... crond          0:off   1:off   2:on    3:on    4:on    5:on    6:off
        ... iptables       0:off   1:off   2:on    3:on    4:on    5:on    6:off
        ... kdump          0:off   1:off   2:off   3:on    4:on    5:on    6:off
        ... restorecond    0:off   1:off   2:off   3:off   4:off   5:off   6:off
        ... xinetd:        0:off   1:off   2:on    3:on    4:on    5:on    6:off
        ...         rexec:         off
        ...         rlogin:        off
        ...         rsh:           off
        ...         telnet:        on
        ... '''
        >>> shared[ChkConfig].is_on('crond')
        True
        >>> shared[ChkConfig].is_on('httpd')
        False
        >>> shared[ChkConfig].is_on('rexec')
        False
        >>> shared[ChkConfig].is_on('telnet')
        True
        >>> shared[ChkConfig].parsed_lines['crond']
        'crond          0:off   1:off   2:on    3:on    4:on    5:on    6:off'
        >>> shared[ChkConfig].parsed_lines['telnet']
        '        telnet:        on'
        >>> shared[ChkConfig].levels_on('crond')
        set(['3', '2', '5', '4'])
        >>> shared[ChkConfig].levels_off('crond')
        set(['1', '0', '6'])
        >>> shared[ChkConfig].levels_on('telnet')
        set([])
        >>> shared[ChkConfig].levels_off('telnet')
        set([])
    """
    LevelState = namedtuple('LevelState', ['level', 'state'])

    def __init__(self, *args, **kwargs):
        self.services = {}
        self.service_list = []
        self.parsed_lines = {}
        self.level_states = {}
        super(ChkConfig, self).__init__(*args, **kwargs)

    def parse_content(self, content):
        """
        Main parsing class method which stores all interesting data from the content.

        Args:
            content (context.content): Parser context content
        """
        state_re = re.compile(':\\s*(?P<state>on|off)(?:\\s+|$)')
        for line in content:
            if state_re.search(line):
                service = line.split()[0].strip(' \t:')
                enabled = ':on' in line or line.endswith('on')
                self.services[service] = enabled
                self.parsed_lines[service] = line
                self.service_list.append(service)
                states = []
                for level in line.split()[1:]:
                    if len(level.split(':')) < 2:
                        if enabled:
                            if 'xinetd' in self.level_states:
                                states = self.level_states['xinetd']
                            else:
                                states = [ self.LevelState(str(x), 'on') for x in range(7)
                                         ]
                        else:
                            states = [ self.LevelState(str(x), 'off') for x in range(7) ]
                        continue
                    num, state = level.split(':')
                    states.append(self.LevelState(num.strip(), state.strip()))

                self.level_states[service] = states

    def is_on(self, service_name):
        """
        Checks if the service is enabled in chkconfig.

        Args:
            service_name (str): service name

        Returns:
            bool: True if service is enabled, False otherwise
        """
        return self.services.get(service_name, False)

    def _level_check(self, service_name, state):
        if service_name in self.parsed_lines:
            return set([ l.level for l in self.level_states[service_name] if l.state == state
                       ])
        raise KeyError(('Service {0} not in Chkconfig').format(service_name))

    def levels_on(self, service_name):
        """set (str): Returns set of level numbers where `service_name` is `on`.

        Raises:
            KeyError: Raises exception if `service_name` is not in Chkconfig.
        """
        return self._level_check(service_name, state='on')

    def levels_off(self, service_name):
        """set (str): Returns set of levels where `service_name` is `off`.

        Raises:
            KeyError: Raises exception if `service_name` is not in Chkconfig.
        """
        return self._level_check(service_name, state='off')