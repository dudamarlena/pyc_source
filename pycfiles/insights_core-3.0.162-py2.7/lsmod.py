# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/lsmod.py
# Compiled at: 2019-05-16 13:41:33
"""
LsMod - command ``/sbin/lsmod``
===============================

This parser reads the output of ``/sbin/lsmod`` into a dictionary, keyed on
the module name.  Each item is a dictionary with three keys:

* ``size`` - the size of the module's memory footprint in bytes
* ``depnum`` - the number of modules dependent on this module
* ``deplist`` - the list of dependent modules as presented (i.e. as a string)

This dictionary is available in the ``data`` attribute.

The parser also provides pseudo-dictionary access so it can be checked for
the existence of a module or module data retrieved as if it was a dictionary.

Sample input::

    Module                  Size  Used by
    xt_CHECKSUM            12549  1
    ipt_MASQUERADE         12678  3
    nf_nat_masquerade_ipv4    13412  1 ipt_MASQUERADE
    tun                    27141  3
    ip6t_rpfilter          12546  1

Examples:

    >>> modules = shared[LsMod]
    >>> 'ip6t_rpfilter' in modules
    True
    >>> 'bridge' in modules
    False
    >>> modules['tun']['deplist']
    ''
    >>> modules['nf_nat_masquerade_ipv4']['deplist']
    'ipt_MASQUERADE'
"""
from .. import parser, CommandParser
from insights.specs import Specs

@parser(Specs.lsmod)
class LsMod(CommandParser):
    """
    Parse the output of ``/sbin/lsmod``.
    """

    def __getitem__(self, item):
        return self.data[item]

    def __contains__(self, item):
        return item in self.data

    def parse_content(self, content):
        module_dict = {}
        memb_keys = [
         'size', 'depnum', 'deplist']
        for line in content[1:]:
            if line.strip():
                line_split = line.split()
                if len(line_split) == 3:
                    line_split.append('')
                if len(line_split) == 4:
                    mod_attrs = {}
                    for i, key in enumerate(memb_keys):
                        mod_attrs[key] = line_split[(i + 1)]

                    module_dict[line_split[0]] = mod_attrs

        self.data = module_dict