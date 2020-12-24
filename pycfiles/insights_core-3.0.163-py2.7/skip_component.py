# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/examples/rules/skip_component.py
# Compiled at: 2019-05-16 13:41:33
"""
Skip Component Example
======================
This module simulates a situation where you might need different parsers
that use the same spec to parse a log file or a configuration file that
may have different formats across RHEL versions.
The idea is that, for efficiency, you only want the parser to try to parse
content that it was designed to parse.

This component can be run against the local host using the following command::

    $ insights-run -p examples.rules.skip_component

or from the examples/rules directory::

    $ ./skip_component.py
"""
from __future__ import print_function
from collections import namedtuple
from insights import get_active_lines, parser, Parser
from insights import make_fail, make_pass, rule, run
from insights.core.spec_factory import SpecSet, simple_file
from insights.combiners.redhat_release import RedHatRelease
from insights.core.plugins import component
from insights.core.dr import SkipComponent
from insights.components.rhel_version import IsRhel6, IsRhel7
ERROR_KEY = 'TOO_MANY_HOSTS'
CONTENT = {make_fail: 'Too many hosts in /etc/hosts: {{num}}', 
   make_pass: 'Just right'}

@component(RedHatRelease)
class IsRhel8(object):
    """
    This component uses ``RedhatRelease`` combiner
    to determine RHEL version. It checks if RHEL8, if
    not RHEL8 it raises ``SkipComponent``.

    Raises:
        SkipComponent: When RHEL version is not RHEL8.
    """

    def __init__(self, rhel):
        if rhel.major != 8:
            raise SkipComponent('Not RHEL8')


class Specs(SpecSet):
    """ Datasources for collection from local host """
    hosts = simple_file('/etc/hosts')


class HostParser(Parser):
    """
    Parses the results of the ``hosts`` Specs

    Attributes:
        hosts (list): List of the namedtuple Host
            which are the contents of the hosts file
            including ``.ip``, ``.host``, and ``.aliases``.
    """
    Host = namedtuple('Host', ['ip', 'host', 'aliases'])

    def parse_content(self, content):
        """
        Method to parse the contents of file ``/etc/hosts``

        This method must be implemented by each parser.

        Arguments:
            content (list): List of strings that are the contents
                of the /etc/hosts file.
        """
        self.hosts = []
        for line in get_active_lines(content):
            line = line.partition('#')[0].strip()
            parts = line.split()
            ip, host = parts[:2]
            aliases = parts[2:]
            self.hosts.append(HostParser.Host(ip, host, aliases))

    def __repr__(self):
        """ str: Returns string representation of the class """
        me = self.__class__.__name__
        msg = '%s([' + (', ').join([ str(d) for d in self.hosts ]) + '])'
        return msg % me


@parser(Specs.hosts, IsRhel8)
class ParseRhel8(HostParser):
    """
    Parser only processes content for RHEL8 Hosts, if not
    RHEL8 the parser will not fire

    Arguments:
        hp (HostParser): Parser object for the custom parser in this
            module.
    """
    pass


@parser(Specs.hosts, [IsRhel6, IsRhel7])
class ParseRhelAll(HostParser):
    """
    Parser only processes content for Rhel 6, 7 Hosts, if not
    Rhel 6, 7 the parser will not fire

    Arguments:
        hp (HostParser): Parser object for the custom parser in this
            module.
    """
    pass


@rule(ParseRhel8, content=CONTENT)
def report_rhel8(hp):
    """
    Rule reports a response if there is more than 1 host
    entry defined in the /etc/hosts file.

    Arguments:
        hp (ParserFedoraHosts): Parser object for the custom parser in this
            module. This parser will only fire if the content is from a Fedora server
    """
    if len(hp.hosts) > 1:
        return make_fail('TOO_MANY_HOSTS', num=len(hp.hosts))
    return make_pass('TOO_MANY_HOSTS', num=len(hp.hosts))


@rule(ParseRhelAll, content=CONTENT)
def report_rhel_others(hp):
    """
    Rule reports a response if there is more than 1 host
    entry defined in the /etc/hosts file.

    Arguments:
        hp (HostParser): Parser object for the custom parser in this
            module.
    """
    if len(hp.hosts) > 1:
        return make_fail('TOO_MANY_HOSTS', num=len(hp.hosts))
    return make_pass('TOO_MANY_HOSTS', num=len(hp.hosts))


if __name__ == '__main__':
    run(report_rhel8, print_summary=True)
    run(report_rhel_others, print_summary=True)