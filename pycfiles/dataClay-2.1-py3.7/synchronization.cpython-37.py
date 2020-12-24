# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dataclay/contrib/synchronization.py
# Compiled at: 2019-11-14 05:52:30
# Size of source mod 2**32: 1170 bytes
"""Basic Synchronization mechanisms."""
from dataclay import dclayMethod

class SequentialConsistencyMixin(object):
    __doc__ = 'Simple sequential consistency synchronization mechanism.\n    \n    This trivial sequential consistency consists on a immediate replication to \n    all slaves. In order to achieve that, all the locations of slave locations\n    are iterated and the set operation is performed in them.\n    '

    @dclayMethod(attribute='str', value='anything')
    def synchronize(self, attribute, value):
        for exeenv_id in self.get_all_locations().keys():
            self.set_in_backend(exeenv_id, attribute, value)

    @dclayMethod(attribute='str', value='anything')
    def synchronize_federated(self, attribute, value):
        for dataclay_id in self.get_federation_targets():
            self.set_in_dataclay_instance(dataclay_id, attribute, [value])

        dataclay_id = self.get_federation_source()
        if dataclay_id is not None:
            self.set_in_dataclay_instance(dataclay_id, attribute, [value])