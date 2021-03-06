# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/combiners/sap.py
# Compiled at: 2019-11-14 13:57:46
"""
Sap
===
This combiner combines the result of
insights.parsers.saphostctrl.SAPHostCtrlInstances` and
`:class:`insights.parsers.lssap.Lssap` to get the available SAP instances.
Prefer the ``SAPHostCtrlInstances`` to ``Lssap``.

"""
from collections import namedtuple
from insights import SkipComponent
from insights.core.plugins import combiner
from insights.combiners.hostname import hostname
from insights.parsers.lssap import Lssap
from insights.parsers.saphostctrl import SAPHostCtrlInstances
SAPInstances = namedtuple('SAPInstances', field_names=[
 'name', 'hostname', 'sid', 'type', 'number', 'fqdn', 'version'])

@combiner(hostname, [SAPHostCtrlInstances, Lssap])
class Sap(dict):
    """
    Combiner for combining the result of :class:`insights.parsers.lssap.Lssap`
    generated by command ``lssap`` and
    `insights.parsers.saphostctrl.SAPHostCtrlInstances` generated by command
    ``saphostctrl``.

    Prefer ``SAPHostCtrlInstances`` to ``Lssap``.

    Examples:
        >>> type(saps)
        <class 'insights.combiners.sap.Sap'>
        >>> 'D16' in saps
        True
        >>> saps['D16'].number
        '16'
        >>> saps.sid('HDB16')
        'HA2'
        >>> saps.hostname('HDB16')
        'lu0417'
        >>> len(saps.business_instances)
        3
        >>> saps.is_hana
        True
        >>> saps.is_netweaver
        True
        >>> saps.is_ascs
        False

    Attributes:
        all_instances (list): List of all the SAP instances listed by the command.
        function_instances (list): List of functional SAP instances
                                   E.g. Diagnostics Agents SMDA97/SMDA98
        business_instances (list): List of business SAP instances
                                   E.g. HANA, NetWeaver, ASCS, or others
        local_instances (list): List of all SAP instances running on this host
    """
    FUNC_INSTS = ('SMDA', )

    def __init__(self, hostname, insts, lssap):
        hn = hostname.hostname
        data = {}
        self.local_instances = []
        self.business_instances = []
        self.function_instances = []
        self.all_instances = []
        self._types = set()
        if insts:
            for inst in insts.data:
                k = inst['InstanceName']
                self.all_instances.append(k)
                self._types.add(inst['InstanceType'])
                self.local_instances.append(k) if hn == inst['Hostname'] else None
                data[k] = SAPInstances(k, inst['Hostname'], inst['SID'], inst['InstanceType'], inst['SystemNumber'], inst['FullQualifiedHostname'], inst['SapVersionInfo'])

        else:
            if lssap:
                for inst in lssap.data:
                    k = inst['Instance']
                    t = k.rstrip('1234567890')
                    self.all_instances.append(k)
                    self._types.add(t)
                    self.local_instances.append(k) if hn == inst['SAPLOCALHOST'] else None
                    data[k] = SAPInstances(k, inst['SAPLOCALHOST'], inst['SID'], t, inst['Nr'], None, inst['Version'])

            if not data:
                raise SkipComponent('No SAP instance.')
            self.update(data)
            for i in self.all_instances:
                (self.function_instances if i.startswith(self.FUNC_INSTS) else self.business_instances).append(i)

        return

    def version(self, instance):
        """str: Returns the version of the ``instance``."""
        if instance in self:
            return self[instance].version
        else:
            return

    def sid(self, instance):
        """str: Returns the sid of the ``instance``."""
        if instance in self:
            return self[instance].sid
        else:
            return

    def type(self, instance):
        """str: Returns the type code of the ``instance``."""
        if instance in self:
            return self[instance].type
        else:
            return

    def hostname(self, instance):
        """str: Returns the hostname of the ``instance``."""
        if instance in self:
            return self[instance].hostname
        else:
            return

    def number(self, instance):
        """str: Returns the systeme number of the ``instance``."""
        if instance in self:
            return self[instance].number
        else:
            return

    @property
    def is_netweaver(self):
        """bool: Is any SAP NetWeaver instance detected?"""
        return 'D' in self._types

    @property
    def is_hana(self):
        """bool: Is any SAP HANA instance detected?"""
        return 'HDB' in self._types

    @property
    def is_ascs(self):
        """bool: Is any SAP System Central Services instance detected?"""
        return 'ASCS' in self._types

    @property
    def data(self):
        """dict: Dict with the instance name as the key and instance details as the value."""
        return self