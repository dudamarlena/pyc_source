# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Library/Frameworks/Python.framework/Versions/3.4/lib/python3.4/site-packages/org/py4grid/scripts/discover_entrypoint.py
# Compiled at: 2014-09-03 21:56:57
# Size of source mod 2**32: 1636 bytes
__doc__ = '\nPY4GRID : a little framework to simule multiprocessing over a lot of computers\nCopyright (C) 2014  João Jorge Pereira Farias Junior\nThis program is free software: you can redistribute it and/or modify\nit under the terms of the GNU General Public License as published by\nthe Free Software Foundation, either version 3 of the License, or\n(at your option) any later version.\nThis program is distributed in the hope that it will be useful,\nbut WITHOUT ANY WARRANTY; without even the implied warranty of\nMERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the\nGNU General Public License for more details.\nYou should have received a copy of the GNU General Public License\nalong with this program. If not, see <http://www.gnu.org/licenses/>.\n'
__author__ = 'dev'
import sys, threading, signal, time

def main(init_args=None):
    import org.py4grid.multicast.daemons.DiscoverDaemons as dv
    if init_args is None:
        init_args = sys.argv[1:]
    server = None
    try:
        try:
            server = dv.DiscoverDaemon()

            def handle_controlz(signum, frame):
                print(signum, frame, 'CONTROl + Z')
                raise Exception('Press CTRL + Z')

            signal.signal(signal.SIGTSTP, handle_controlz)
            server.start()
            server.join()
        except KeyboardInterrupt as kex:
            print('KEYBOARD interrupt...')

    finally:
        print('Closing server...')
        server.sock.stop()
        server = None
        sys.exit(0)


if __name__ == '__main__':
    print(sys.argv)
    main(init_args=sys.argv[1:])
    sys.exit(0)