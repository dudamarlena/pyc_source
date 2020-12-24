# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/emantools/daemon.py
# Compiled at: 2008-04-07 00:02:10
import os, sys, logging, time, datetime, create_daemon
PIDFILE = '/var/run/start-stop.pid'
LOGDIR = '/var/log'

def logit():
    fp = open('test.log', 'a')
    current_time = datetime.datetime.now()
    fp.write(str(current_time) + '\n')
    fp.close()


class Daemon(object):
    interval = 5
    pid_file = PIDFILE
    log_dir = LOGDIR
    log_file = '/dev/null'

    def __init__(self):
        self.main()

    def get_running_pid(self):
        try:
            fp = open(self.pid_file, 'r')
        except IOError:
            return

        self.pid = fp.read()
        fp.close()
        return self.pid

    def init_log(self):
        logging.basicConfig()
        for handler in logging.root.handlers[:]:
            logging.root.removeHandler(handler)

        handler = logging.FileHandler(self.log_file)
        fmt = '[%(asctime)s] %(name)s %(levelname)s: %(message)s'
        handler.setFormatter(logging.Formatter(fmt))
        logging.root.addHandler(handler)
        logging.root.setLevel(logging.DEBUG)
        self.log = logging.getLogger('Daemon')
        self.log.info('Log started')
        return self.log

    def write_pid(self):
        fp = open(self.pid_file, 'w')
        fp.write(str(os.getpid()))
        fp.close()
        return True

    def get_status(self):
        if self.get_running_pid() is not None:
            return True
        return

    def run(self):
        logit()

    def status(self):
        if self.get_status():
            print 'Daemon running'
        else:
            print 'Daemon not running'
        return True

    def start(self):
        print 'Starting Daemon ...'
        if self.get_status():
            print 'Daemon already started.'
            return False
        create_daemon.createDaemon()
        self.log.info('Daemon Started')
        self.write_pid()
        while True:
            time.sleep(self.interval)
            self.run()

        return True

    def stop(self):
        print 'Stopping Daemon ...'
        pid = self.get_running_pid()
        if pid is None:
            print 'Daemon not started.'
            return False
        try:
            os.kill(int(pid), 15)
        except OSError:
            pass

        os.unlink(self.pid_file)
        return True

    def restart(self):
        self.stop()
        return self.start()

    def print_usage(self):
        print 'USAGE:\n        %(script)s start|stop|status|help\n        ' % dict(script=self.filename)

    def main(self):
        self.filename = sys.argv[0]
        self.init_log()
        try:
            command = sys.argv[1]
        except IndexError:
            command = 'help'

        if command == 'start':
            self.start()
        elif command == 'stop':
            self.stop()
        elif command == 'restart':
            self.restart()
        elif command == 'status':
            self.status()
        else:
            self.print_usage()


if __name__ == '__main__':
    Daemon()