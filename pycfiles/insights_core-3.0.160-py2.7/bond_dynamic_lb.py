# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/bond_dynamic_lb.py
# Compiled at: 2019-05-16 13:41:33
"""
BondDynamicLB - file ``/sys/class/net/bond[0-9]*/bonding/tlb_dynamic_lb``
=========================================================================

This file represent weather the transmit load balancing is enabled or not

tlb_dynamic_lb=1 mode:
    The outgoing traffic is distributed according to the current load.

tlb_dynamic_lb=0 mode:
    The load balancing based on current load is disabled and the load
    is distributed only using the hash distribution.

Typical content of the file is::

        1

Data is modeled as an array of ``BondDynamicLB`` objects

Examples:
    >>> type(tlb_bond)
    <class 'insights.parsers.bond_dynamic_lb.BondDynamicLB'>
    >>> tlb_bond.dynamic_lb_status
    1
    >>> tlb_bond.bond_name
    'bond0'

"""
from insights import Parser, parser
from insights.specs import Specs
from insights.parsers import ParseException, SkipException

@parser(Specs.bond_dynamic_lb)
class BondDynamicLB(Parser):
    """
    Models the ``/sys/class/net/bond[0-9]*/bonding/tlb_dynamic_lb`` file.

    0 - Hash based load balancing.

    1 - Load based load balancing.

    Raises:
        SkipException: When contents are empty
        ParseException: When contents are invalid
    """

    def parse_content(self, content):
        if not content:
            raise SkipException('No Contents')
        line = content[0].strip()
        self._dynamic_lb_status = None
        self._bond_name = self.file_path.rsplit('/')[(-3)]
        if line in ('0', '1'):
            self._dynamic_lb_status = int(line)
        else:
            raise ParseException(("Unrecognised Values '{b}'").format(b=line))
        return

    @property
    def dynamic_lb_status(self):
        """
        Returns (int): Load balancer type
        """
        return self._dynamic_lb_status

    @property
    def bond_name(self):
        """
        Returns (str): Name of bonding interface
        """
        return self._bond_name