# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dataclay/util/ReferenceCounting.py
# Compiled at: 2019-10-28 11:50:26
# Size of source mod 2**32: 2308 bytes
""" Class description goes here. """
import dataclay.serialization.python.lang.IntegerWrapper as IntegerWrapper
import dataclay.serialization.python.lang.BooleanWrapper as BooleanWrapper
import dataclay.serialization.python.lang.StringWrapper as StringWrapper
import logging
logger = logging.getLogger('ReferenceCounting')

class ReferenceCounting(object):
    __doc__ = '\n    classdocs+\n    '

    def __init__(self):
        """
        Constructor
        """
        self.reference_counting = dict()

    def increment_reference_counting(self, oid, hint):
        if hint not in self.reference_counting:
            references_per_hint = dict()
            self.reference_counting[hint] = references_per_hint
        else:
            references_per_hint = self.reference_counting.get(hint)
        if oid in references_per_hint:
            num_refs = references_per_hint.get(oid) + 1
        else:
            num_refs = 1
        references_per_hint[oid] = num_refs

    def serialize_reference_counting(self, referrer_oid, io_file):
        """ TODO: IMPORTANT: this should be removed in new serialization by using paddings to directly access reference counters inside
         metadata. """
        IntegerWrapper().write(io_file, len(self.reference_counting))
        for location, ref_counting_in_loc in self.reference_counting.items():
            if location is None:
                BooleanWrapper().write(io_file, True)
            else:
                BooleanWrapper().write(io_file, False)
                StringWrapper().write(io_file, str(location))
            IntegerWrapper().write(io_file, len(ref_counting_in_loc))
            for oid, counter in ref_counting_in_loc.items():
                StringWrapper().write(io_file, str(oid))
                IntegerWrapper().write(io_file, counter)

    def has_no_references(self):
        return len(self.reference_counting) == 0