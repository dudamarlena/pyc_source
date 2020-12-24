# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/nivekuil/code/amp/python3/amp/player.py
# Compiled at: 2016-10-28 21:41:15
# Size of source mod 2**32: 4619 bytes
__doc__ = '\nPlayer daemon that handles asynchronous playback.\n'
import sys, os, time, atexit, signal, subprocess, pafy
from .process import kill_process_tree
import logging
logging.getLogger().setLevel(logging.ERROR)
PIDFILE = '/tmp/amp.pid'
INFOFILE = '/tmp/amp.info'

class Player:
    """Player"""

    def __init__(self, url, show_video=False, verbose=False):
        self.pidfile = PIDFILE
        self.infofile = INFOFILE
        self.url = url
        self.show_video = show_video
        self.verbose = verbose

    def print_info(self):
        """Prints video information and usage output. If --verbose is set,
        prints to stdout in addition to infofile."""
        video_data = pafy.new(self.url)
        print('Now playing: ' + video_data.title + ' [' + video_data.duration + ']')
        if self.verbose:
            print('URL: ' + self.url)
            print('Description: ' + video_data.description)
        if self.show_video:
            print('Showing video in an external window.')
        with open(INFOFILE, 'w+') as (f):
            f.write('Description: %s\n\nTitle: %s\nDuration: %s\n' % (video_data.description, video_data.title,
             video_data.duration))

    def daemonize(self):
        """Daemonize class. UNIX double fork mechanism."""
        try:
            pid = os.fork()
            if pid > 0:
                sys.exit(0)
        except OSError as err:
            sys.stderr.write('fork #1 failed: {0}\n'.format(err))
            sys.exit(1)

        os.chdir('/')
        os.setsid()
        os.umask(0)
        try:
            pid = os.fork()
            if pid > 0:
                sys.exit(0)
        except OSError as err:
            sys.stderr.write('fork #2 failed: {0}\n'.format(err))
            sys.exit(1)

        sys.stdout.flush()
        sys.stderr.flush()
        si = open(os.devnull, 'r')
        so = open(os.devnull, 'a+')
        se = open(os.devnull, 'a+')
        os.dup2(si.fileno(), sys.stdin.fileno())
        atexit.register(self.delete_info_files)
        pid = str(os.getpid())
        with open(self.pidfile, 'w+') as (f):
            f.write(pid + '\n')

    def delete_info_files(self):
        os.remove(self.pidfile)
        os.remove(self.infofile)

    def start(self):
        try:
            with open(self.pidfile, 'r') as (f):
                pid = int(f.read().strip())
        except IOError:
            pid = None

        if pid:
            print('Stopping current song..')
            kill_process_tree(pid)
            self.delete_info_files()
        self.print_info()
        self.daemonize()
        self.run()

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
            while True:
                os.kill(pid, signal.SIGTERM)
                time.sleep(0.1)

        except OSError as err:
            e = str(err.args)
            if e.find('No such process') > 0:
                if os.path.exists(self.pidfile):
                    self.delete_info_files()
            else:
                print(str(err.args))
                sys.exit(1)

    def restart(self):
        """Restart the daemon."""
        self.stop()
        self.start()

    def run(self):
        subprocess_args = [
         'mpv', self.url, '--really-quiet']
        if self.show_video:
            subprocess_args.append('--fs')
        else:
            subprocess_args.append('--no-video')
        try:
            subprocess.call(subprocess_args)
        except OSError as e:
            if e.errno == 2:
                print('mpv cannot be found.')
                sys.exit(1)