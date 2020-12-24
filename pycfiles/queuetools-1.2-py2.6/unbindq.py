# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-intel/egg/queuetools/unbindq.py
# Compiled at: 2015-07-13 22:23:41
import getpass, optparse, sys
from queuetools.options import add_connection_options
from amqplib import client_0_8 as amqp

def unbindq_options(args):
    options = optparse.OptionParser(prog='unbindq', usage='%prog [options] queue exchange', description='Unbinds a queue from an exchange in an AMQP broker.')
    options.add_option('--routing-key', action='store', default='', metavar='KEY', help='the routing key to use when unbinding the queue to its exchange (default: unset)')
    add_connection_options(options)
    return options.parse_args(args)


def main(args=sys.argv[1:], optparse=unbindq_options, getpassword=getpass.getpass, connect=amqp.Connection):
    (options, (queue, exchange)) = optparse(args)
    if options.password is None:
        options.password = getpassword()
    con = connect(host=options.host, userid=options.userid, password=options.password, virtual_host=options.vhost)
    try:
        chan = con.channel()
        try:
            chan.queue_unbind(queue=queue, exchange=exchange, routing_key=options.routing_key)
        finally:
            chan.close()

    finally:
        con.close()

    return