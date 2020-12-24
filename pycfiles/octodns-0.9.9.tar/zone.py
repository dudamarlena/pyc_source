# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ross/github/octodns/octodns/zone.py
# Compiled at: 2019-10-18 13:06:59
from __future__ import absolute_import, division, print_function, unicode_literals
from collections import defaultdict
from logging import getLogger
import re
from six import text_type
from .record import Create, Delete

class SubzoneRecordException(Exception):
    pass


class DuplicateRecordException(Exception):
    pass


class InvalidNodeException(Exception):
    pass


def _is_eligible(record):
    return record._type != b'NS' or record.name != b''


class Zone(object):
    log = getLogger(b'Zone')

    def __init__(self, name, sub_zones):
        if not name[(-1)] == b'.':
            raise Exception((b'Invalid zone name {}, missing ending dot').format(name))
        self.name = text_type(name).lower() if name else name
        self.sub_zones = sub_zones
        self._records = defaultdict(set)
        self._name_re = re.compile((b'\\.?{}?$').format(name))
        self.log.debug(b'__init__: zone=%s, sub_zones=%s', self, sub_zones)

    @property
    def records(self):
        return set([ r for _, node in self._records.items() for r in node ])

    def hostname_from_fqdn(self, fqdn):
        return self._name_re.sub(b'', fqdn)

    def add_record(self, record, replace=False, lenient=False):
        name = record.name
        last = name.split(b'.')[(-1)]
        if not lenient and last in self.sub_zones:
            if name != last:
                raise SubzoneRecordException((b'Record {} is under a managed subzone').format(record.fqdn))
            elif record._type != b'NS':
                raise SubzoneRecordException((b'Record {} a managed sub-zone and not of type NS').format(record.fqdn))
        if replace:
            self._records[name].discard(record)
        node = self._records[name]
        if record in node:
            raise DuplicateRecordException((b'Duplicate record {}, type {}').format(record.fqdn, record._type))
        elif not lenient and (record._type == b'CNAME' and len(node) > 0 or b'CNAME' in [ r._type for r in node ]):
            raise InvalidNodeException((b'Invalid state, CNAME at {} cannot coexist with other records').format(record.fqdn))
        node.add(record)

    def _remove_record(self, record):
        """Only for use in tests"""
        self._records[record.name].discard(record)

    def changes(self, desired, target):
        self.log.debug(b'changes: zone=%s, target=%s', self, target)
        desired_records = {r:r for r in desired.records}
        changes = []
        for record in filter(_is_eligible, self.records):
            if record.ignored:
                continue
            elif len(record.included) > 0 and target.id not in record.included:
                self.log.debug(b'changes:  skipping record=%s %s - %s not included ', record.fqdn, record._type, target.id)
                continue
            elif target.id in record.excluded:
                self.log.debug(b'changes:  skipping record=%s %s - %s excluded ', record.fqdn, record._type, target.id)
                continue
            try:
                desired_record = desired_records[record]
                if desired_record.ignored:
                    continue
                elif len(desired_record.included) > 0 and target.id not in desired_record.included:
                    self.log.debug(b'changes:  skipping record=%s %s - %snot included ', record.fqdn, record._type, target.id)
                    continue
                elif target.id in desired_record.excluded:
                    continue
            except KeyError:
                if not target.supports(record):
                    self.log.debug(b'changes:  skipping record=%s %s - %s does not support it', record.fqdn, record._type, target.id)
                    continue
                self.log.debug(b'changes: zone=%s, removed record=%s', self, record)
                changes.append(Delete(record))
            else:
                change = record.changes(desired_record, target)
                if change:
                    self.log.debug(b'changes: zone=%s, modified\n    existing=%s,\n     desired=%s', self, record, desired_record)
                    changes.append(change)
                else:
                    self.log.debug(b'changes: zone=%s, n.c. record=%s', self, record)

        for record in filter(_is_eligible, desired.records - self.records):
            if record.ignored:
                continue
            elif len(record.included) > 0 and target.id not in record.included:
                self.log.debug(b'changes:  skipping record=%s %s - %s not included ', record.fqdn, record._type, target.id)
                continue
            elif target.id in record.excluded:
                self.log.debug(b'changes:  skipping record=%s %s - %s excluded ', record.fqdn, record._type, target.id)
                continue
            if not target.supports(record):
                self.log.debug(b'changes:  skipping record=%s %s - %s does not support it', record.fqdn, record._type, target.id)
                continue
            self.log.debug(b'changes: zone=%s, create record=%s', self, record)
            changes.append(Create(record))

        return changes

    def __repr__(self):
        return (b'Zone<{}>').format(self.name)