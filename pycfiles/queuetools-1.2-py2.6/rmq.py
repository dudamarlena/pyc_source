# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-intel/egg/queuetools/rmq.py
# Compiled at: 2015-07-13 22:23:41
import getpass, optparse, sys
from queuetools.options import add_connection_options
from amqplib import client_0_8 as amqp

def rmq_options(args):
    options = optparse.OptionParser(prog='rmq', usage='%prog [options] queue1 [queue2 queue3...]', description='Removes queues from an AMQP broker.')
    options.add_option('-u', '--if-unused', action='store_true', default=False, help="if set, the queues will be deleted only if they're not in use")
    options.add_option('-e', '--if-empty', action='store_true', default=False, help='if set, the queues will be deleted only if they hold no undelivered messages')
    add_connection_options(options)
    return options.parse_args(args)


def main(args=sys.argv[1:], optparse=rmq_options, getpassword=getpass.getpass, connect=amqp.Connection):
    (options, queues) = optparse(args)
    if options.password is None:
        options.password = getpassword()
    con = connect(host=options.host, userid=options.userid, password=options.password, virtual_host=options.vhost)
    try:
        chan = con.channel()
        try:
            for queue in queues:
                chan.queue_delete(queue=queue, if_empty=options.if_empty, if_unused=options.if_unused)

        finally:
            chan.close()

    finally:
        con.close()

    return