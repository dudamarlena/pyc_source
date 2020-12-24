# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /data/envs/dfuzz/project/dfuzz/dfuzz/core/incident.py
# Compiled at: 2011-05-11 10:40:28
import signal, logging

class Incident(object):

    def __init__(self, cfg, fuzzer, handler_cls):
        self.crash_signals = '\n        SIGILL\n        SIGABRT\n        SIGBUS\n        SIGFPE\n        SIGSEGV\n        '
        self.translation = {4: 'Illegal instruction', 
           6: 'Process aborted', 
           7: 'Access to undefined portion of memory object', 
           8: 'Floating point exception', 
           11: 'Segmentation violation'}
        self.cfg = cfg
        self.handler_cls = handler_cls
        self.fuzzer = fuzzer

    @property
    def crash_signals(self):
        return self._crash_signals

    @crash_signals.setter
    def crash_signals(self, value):
        if type(value) == list:
            try:
                map(int, value)
            except ValueError:
                logging.error('crash_signals expects a list of intergers or string of signal names. No update - using old value.')
                return
            else:
                self._crash_signals = value
        elif type(value) == str:
            sep = ' '
            if ',' in value:
                sep = ','
            value = value.replace('\n', ' ')
            parts = map(lambda x: x.strip(), value.split(sep))
            new = []
            for i in parts:
                if len(i) == 0:
                    continue
                if hasattr(signal, str(i)):
                    new.append(getattr(signal, str(i)))
                else:
                    logging.error('No such signal "%s" defined in signal module', i)

            self._crash_signals = new

    def human_readable_reason(self, code):
        if -code in self.translation:
            return self.translation[(-code)]
        else:
            return
            return

    def serious(self, retcode):
        return -retcode in self.crash_signals

    def check(self, target_obj, input_file_path):
        if self.serious(target_obj.code):
            handler = self.handler_cls(self.cfg, self.fuzzer)
            handler.handle_failure(target_obj, input_file_path, self.human_readable_reason(target_obj.code))


class TimeIncident(Incident):

    def __init__(self, *args, **kwargs):
        super(TimeIncident, self).__init__(*args, **kwargs)
        self.translation[9] = 'Kill (timed out)'
        if self.cfg.timeout_as_incident:
            self.crash_signals.append(signal.SIGKILL)


class TimeValgrindIncident(TimeIncident):

    def __init__(self, *args, **kwargs):
        super(TimeIncident, self).__init__(*args, **kwargs)
        self.translation[101] = 'Valgrind error'
        self.crash_signals.append(101)