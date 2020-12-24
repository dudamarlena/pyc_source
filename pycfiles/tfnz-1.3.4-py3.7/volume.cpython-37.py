# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/tfnz/volume.py
# Compiled at: 2018-05-18 20:34:30
# Size of source mod 2**32: 2471 bytes
import weakref, logging, os
from . import Taggable

class Volume(Taggable):
    __doc__ = 'An object representing a persistent volume.\n    Do not construct directly, use Location.create_volume or Location.ensure_volume;\n    or Location.volume to retrieve one that is pre-existing.'

    def __init__(self, location, uuid, tag, *, termination_callback=None):
        super().__init__((location.user_pk), uuid, tag=tag)
        self.connection = weakref.ref(location.conn)
        self.termination_callback = termination_callback

    def snapshot(self):
        """Create a snapshot."""
        self.connection().send_cmd(b'snapshot_volume', {'volume': self.uuid})
        logging.info('Set snapshot for volume: ' + self.uuid.decode())

    def rollback(self):
        """Resets the volume back to its' state when 'snapshot' was called."""
        self.connection().send_cmd(b'rollback_volume', {'volume': self.uuid})
        logging.info('Rolled back to snapshot: ' + self.uuid.decode())

    @staticmethod
    def trees_intersect(current, proposed):
        p = os.path.abspath(proposed)
        for cur in current:
            c = os.path.abspath(cur)
            if len(p) > len(c):
                if p[:len(c)] == c:
                    return (
                     p, c)
                elif c[:len(p)] == p:
                    return (
                     c, p)

    def internal_destroy(self):
        if self.termination_callback is not None:
            self.termination_callback(self, 0)

    def __repr__(self):
        return "<Volume '%s'>" % self.display_name()