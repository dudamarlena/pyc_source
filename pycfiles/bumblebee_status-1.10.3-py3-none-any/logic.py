# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/bumblebee_indicator/logic.py
# Compiled at: 2014-07-01 13:38:21
import logging, re, os.path as p, subprocess

class Optimus:

    class DualMonitor:

        def __init__(self, optimus):
            pass

        def is_active(self):
            proc_file = file(p.join('/', 'etc', 'bumblebee', 'bumblebee.conf'))
            contents = proc_file.read().strip()
            logging.debug('DualMonitor::is_active() - /etc/bumblebee/bumblebee.conf: %s' % contents[-100:-1])
            regex = re.compile('^PMMethod=none\\s*?(?:\\#.*)?$', re.MULTILINE)
            match = regex.search(contents)
            ret = match != None
            logging.debug('DualMonitor::is_active() %s' % repr(ret))
            return ret

        def turn(self, setting=True):
            if setting:
                ret = self.__exec('gksu /usr/local/bin/hidden/nvidia-enable')
            else:
                ret = self.__exec('gksu /usr/local/bin/hidden/nvidia-disable')
            return ret

        def __exec(self, command):
            logging.info('Exec[%s]' % command)
            p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            retval = p.wait()
            for line in p.stdout.readlines():
                logging.debug('Exec[%s]: %s' % (command, line))

            for line in p.stderr.readlines():
                logging.error('Exec[%s]: %s' % (command, line))

            return retval

    def __init__(self):
        self.__dual = Optimus.DualMonitor(self)

    def is_active(self):
        proc_file = file(p.join('/', 'proc', 'acpi', 'bbswitch'))
        contents = proc_file.read().strip()
        logging.debug('Optimus::is_active() - /proc/acpi/bbswitch: %s' % repr(contents))
        idx = contents.rfind('ON')
        ret = idx >= 0
        logging.debug('Optimus::is_active() => %s' % repr(ret))
        return ret

    def dual_monitor(self):
        return self.__dual