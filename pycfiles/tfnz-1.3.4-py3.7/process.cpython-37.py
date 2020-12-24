# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/tfnz/process.py
# Compiled at: 2018-05-18 20:34:30
# Size of source mod 2**32: 3748 bytes
import weakref, logging
from . import Killable

class Process(Killable):
    __doc__ = 'An object encapsulating a process within a container.\n    Do not instantiate directly, use container.spawn_process.'

    def __init__(self, parent, uuid, data_callback, termination_callback, stderr_callback=None):
        super().__init__()
        self.parent = weakref.ref(parent)
        self.node = weakref.ref(parent.parent())
        self.conn = weakref.ref(parent.conn())
        self.uuid = uuid
        self.data_callback = data_callback
        self.termination_callback = termination_callback
        self.stderr_callback = stderr_callback
        self.wrapper = None

    def stdin(self, data: bytes):
        r"""Inject data into stdin for the process.

        :param data: The data to inject -  bytes, not a string.

        Note that because this injects raw data, it may not behave as you expect. Remember to:

        * Turn strings into bytes with .encode()
        * Add '\\n' to emulate carriage return.
        * Turn returned bytes into strings with .decode()

        """
        self.ensure_alive()
        if len(data) == 0:
            self.destroy()
            return
        self.conn().send_cmd(b'stdin_process', {'node':self.node().pk,  'container':self.parent().uuid, 
         'process':self.uuid},
          bulk=data)

    def destroy(self, with_command=True):
        if self.bail_if_dead():
            return
        if with_command:
            self.conn().send_cmd(b'destroy_process', {'node':self.node().pk,  'container':self.parent().uuid, 
             'process':self.uuid})
        logging.info('Terminated client side: %s' % self.uuid.decode())
        self.mark_as_dead()
        if self.termination_callback is not None:
            self.termination_callback(self, 0)

    def give_me_messages(self, msg):
        if self.bail_if_dead():
            return
        if msg is None:
            logging.error('give_me_messages was sent None')
            return
        if len(msg.bulk) == 0:
            logging.info('Terminated server side: %s (%d)' % (self.uuid.decode(), msg.params['returncode']))
            self.mark_as_dead()
            if self.termination_callback is not None:
                self.termination_callback(self, msg.params['returncode'])
            return
        if 'stderr' in msg.params:
            if self.stderr_callback is not None:
                self.stderr_callback(self, msg.bulk)
            return
        if self.data_callback is not None:
            self.data_callback(self, msg.bulk)

    def __repr__(self):
        return "<Process '%s'>" % self.uuid.decode()