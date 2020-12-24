# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/trepan/client.py
# Compiled at: 2018-08-19 14:41:23
import sys, time
from trepan.interfaces import client as Mclient
from trepan.interfaces import comcodes as Mcomcodes
from optparse import OptionParser
from trepan.version import VERSION

def process_options(pkg_version, sys_argv, option_list=None):
    """Handle debugger options. Set `option_list' if you are writing
    another main program and want to extend the existing set of debugger
    options.

    The options dicionary from opt_parser is return. sys_argv is
    also updated."""
    usage_str = '%prog [debugger-options]]\n\n    Client connection to an out-of-process trepan3k debugger session'
    optparser = OptionParser(usage=usage_str, option_list=option_list, version='%%prog version %s' % pkg_version)
    optparser.add_option('-H', '--host', dest='host', default='127.0.0.1', action='store', type='string', metavar='IP-OR-HOST', help='connect IP or host name.')
    optparser.add_option('-P', '--port', dest='port', default=1027, action='store', type='int', metavar='NUMBER', help='Use TCP port number NUMBER for out-of-process connections.')
    optparser.add_option('--pid', dest='pid', default=0, action='store', type='int', metavar='NUMBER', help='Use PID to get FIFO names for out-of-process connections.')
    optparser.disable_interspersed_args()
    sys.argv = list(sys_argv)
    opts, sys.argv = optparser.parse_args()
    return (opts, sys.argv)


DEFAULT_CLIENT_CONNECTION_OPTS = {'open': True,  'IO': 'TCP',  'HOST': '127.0.0.1', 
 'PORT': 1027}

def start_client(connection_opts):
    intf = Mclient.ClientInterface(connection_opts=connection_opts)
    intf.msg('Connected.')
    done = False
    while not done:
        control, remote_msg = intf.read_remote()
        if Mcomcodes.PRINT == control:
            print(remote_msg, end=' ')
        elif control in [Mcomcodes.CONFIRM_TRUE, Mcomcodes.CONFIRM_FALSE]:
            default = Mcomcodes.CONFIRM_TRUE == control
            if intf.confirm(remote_msg.rstrip('\n'), default):
                msg = 'Y'
            else:
                msg = 'N'
            intf.write_remote(Mcomcodes.CONFIRM_REPLY, msg)
        elif Mcomcodes.PROMPT == control:
            msg = intf.read_command('(Trepan*) ').strip()
            intf.write_remote(Mcomcodes.CONFIRM_REPLY, msg)
        elif Mcomcodes.QUIT == control:
            print("trepan3kc: That's all, folks...")
            done = True
            break
        elif Mcomcodes.RESTART == control:
            if 'TCP' == connection_opts['IO']:
                print('Restarting...')
                intf.inout.close()
                time.sleep(1)
                intf.inout.open()
            else:
                print("Don't know how to hard-restart FIFO...")
                done = True
            break
        else:
            print("!! Weird status code received '%s'" % control)
            print(remote_msg, end=' ')

    intf.close()


def run(opts, sys_argv):
    if hasattr(opts, 'pid') and opts.pid > 0:
        remote_opts = {'open': opts.pid,  'IO': 'FIFO'}
    else:
        remote_opts = {'open': True,  'IO': 'TCP',  'PORT': opts.port,  'HOST': opts.host}
    start_client(remote_opts)


def main():
    opts, sys_argv = process_options(VERSION, sys.argv)
    run(opts, sys_argv)


if __name__ == '__main__':
    main()