# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Library/Frameworks/Python.framework/Versions/3.4/lib/python3.4/site-packages/org/py4grid/scripts/py4gridserver_entrypoint.py
# Compiled at: 2014-09-03 22:05:30
# Size of source mod 2**32: 2581 bytes
__doc__ = '\nPY4GRID : a little framework to simule multiprocessing over a lot of computers\nCopyright (C) 2014  João Jorge Pereira Farias Junior\nThis program is free software: you can redistribute it and/or modify\nit under the terms of the GNU General Public License as published by\nthe Free Software Foundation, either version 3 of the License, or\n(at your option) any later version.\nThis program is distributed in the hope that it will be useful,\nbut WITHOUT ANY WARRANTY; without even the implied warranty of\nMERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the\nGNU General Public License for more details.\nYou should have received a copy of the GNU General Public License\nalong with this program. If not, see <http://www.gnu.org/licenses/>.\n'
import argparse, socketserver, sys, os, signal
MODEL_BASE = None
if hasattr(os, 'fork'):
    MODEL_BASE = socketserver.ForkingTCPServer
else:
    MODEL_BASE = socketserver.ThreadingTCPServer
    MODEL_BASE.daemon_threads = True

def main(init_args=None):
    import org.py4grid.GPR as gpr, org.py4grid.multicast.daemons.DiscoverServers as discover
    discover_server = None
    server = None
    server_thread = None
    parse = argparse.ArgumentParser(prog='PY4GRIDSERVER')
    parse.add_argument('-port', help='a port to server usage to listen, default is 4680', default=4680, type=int)
    init_args = parse.parse_args(init_args)
    try:
        try:
            dic = {'port': init_args.port,  'ip': ''}
            host = (
             dic['ip'], init_args.port)
            print('HOST', host)
            server = MODEL_BASE(host, gpr.ProcessRemoteClient)

            def handle_controlz(signum, frame):
                print(signum, frame, 'CONTROl + Z')
                raise Exception('Press CTRL + Z')

            signal.signal(signal.SIGTSTP, handle_controlz)
            discover_server = discover.ServerDaemon(port=init_args.port)
            discover_server.start()
            print('SERVER_ADDRESS', server.server_address)
            server.serve_forever()
        except KeyboardInterrupt as kex:
            print('KEYBOARD interrupt...')
        except Exception as ex:
            print('Exception :', ex, '...')

    finally:
        print('Stoping DiscoverDaemon')
        discover_server.StopDaemon()
        print('DiscoverDaemon Stoped')
        print('Stoping PY4GRIDSERVER')
        server.server_close()
        print('PY4GRIDSERVER Stoped')
        sys.exit(0)


if __name__ == '__main__':
    print(sys.argv)
    main(init_args=sys.argv[1:])
    sys.exit(0)