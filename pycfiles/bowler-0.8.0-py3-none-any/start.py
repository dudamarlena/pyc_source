# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/clewis/Desktop/old-air/github-public/bowl/bowl/cli_opts/start.py
# Compiled at: 2014-07-27 23:50:54
__doc__ = '\nThis module is the start command of bowl.\n\nCreated on 14 July 2014\n@author: Charlie Lewis\n'
import os, sys, bowl.api

class start(object):
    """
    This class is responsible for the start command of the cli.
    """

    @classmethod
    def check_pid(self, pid):
        """
        Check for the existence of a unix pid.
        """
        try:
            os.kill(int(pid), 0)
        except OSError:
            return False

        return True

    @classmethod
    def main(self, args):
        running = False
        directory = args.metadata_path
        directory = os.path.expanduser(directory)
        pid_file = os.path.join(directory, 'pid')
        if not os.path.exists(directory):
            os.makedirs(directory)
        if os.path.isfile(pid_file):
            with open(pid_file, 'r') as (f):
                pid = f.readline()
                running = self.check_pid(pid)
        if running:
            if not args.z:
                print 'The API Server is already running.'
        else:
            try:
                pid = os.fork()
                if pid > 0:
                    with open(pid_file, 'a') as (f):
                        f.write(str(pid))
                    sys.exit(0)
            except OSError as e:
                if not args.z:
                    print >> sys.stderr, 'fork failed: %d (%s)' % (e.errno, e.strerror)
                sys.exit(1)

            bowl.api.main()