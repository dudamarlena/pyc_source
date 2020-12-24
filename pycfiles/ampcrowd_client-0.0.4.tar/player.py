# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/nivekuil/code/amp/amp/player.py
# Compiled at: 2015-08-11 04:43:40
__doc__ = '\nPlayer daemon that handles asynchronous playback.\n'
import sys, os, time, atexit, signal, subprocess, pafy
from process import kill_process_tree

class Player:
    """Daemon that controls the music player. Based on implementation by anon at
    http://jejik.com/articles/2007/02/a_simple_unix_linux_daemon_in_python/#c35
    """

    def __init__(self, pidfile, url, show_video=False, verbose=False):
        self.pidfile = pidfile
        self.url = url
        self.show_video = show_video
        self.verbose = verbose

    def print_info(self):
        """Prints video information and usage output to stdout"""
        video_data = pafy.new(self.url)
        print 'Now playing: ' + video_data.title + ' [' + video_data.duration + ']'
        if self.verbose:
            print 'URL: ' + self.url
            print 'Description: ' + video_data.description
        if self.show_video:
            print 'Showing video in an external window.'

    def daemonize(self):
        """Daemonize class. UNIX double fork mechanism."""
        try:
            pid = os.fork()
            if pid > 0:
                sys.exit(0)
        except OSError as err:
            sys.stderr.write(('fork #1 failed: {0}\n').format(err))
            sys.exit(1)

        os.chdir('/')
        os.setsid()
        os.umask(0)
        try:
            pid = os.fork()
            if pid > 0:
                sys.exit(0)
        except OSError as err:
            sys.stderr.write(('fork #2 failed: {0}\n').format(err))
            sys.exit(1)

        sys.stdout.flush()
        sys.stderr.flush()
        si = open(os.devnull, 'r')
        so = open(os.devnull, 'a+')
        se = open(os.devnull, 'a+')
        os.dup2(si.fileno(), sys.stdin.fileno())
        atexit.register(self.delpid)
        pid = str(os.getpid())
        with open(self.pidfile, 'w+') as (f):
            f.write(pid + '\n')

    def delpid(self):
        os.remove(self.pidfile)

    def start(self):
        try:
            with open(self.pidfile, 'r') as (f):
                pid = int(f.read().strip())
        except IOError:
            pid = None

        if pid:
            print 'Stopping current song..'
            kill_process_tree(pid)
            self.delpid()
        self.print_info()
        self.daemonize()
        self.run()
        return

    def stop(self):
        """Stop the daemon."""
        try:
            with open(self.pidfile, 'r') as (pf):
                pid = int(pf.read().strip())
        except IOError:
            pid = None

        if not pid:
            message = 'pidfile {0} does not exist. ' + 'Daemon not running?\n'
        sys.stderr.write(message.format(self.pidfile))
        return
        try:
            while 1:
                os.kill(pid, signal.SIGTERM)
                time.sleep(0.1)

        except OSError as err:
            e = str(err.args)
            if e.find('No such process') > 0:
                if os.path.exists(self.pidfile):
                    os.remove(self.pidfile)
                else:
                    print str(err.args)
                    sys.exit(1)

        return

    def restart(self):
        """Restart the daemon."""
        self.stop()
        self.start()

    def run(self):
        if self.show_video:
            subprocess_args = [
             'mpv', self.url, '--really-quiet']
        else:
            subprocess_args = [
             'mpv', self.url, '--really-quiet', '--no-video']
        subprocess.call(subprocess_args)