# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/jabber_roster.py
# Compiled at: 2010-11-18 17:16:53
import sys, getpass, locale, warnings
from optparse import OptionParser
warnings.filterwarnings(action='ignore', category=DeprecationWarning, module='xmpp')
import xmpp
locale.setlocale(locale.LC_ALL, '')
version = '0.1.1'

def main_run():
    """Execute the whole program"""
    usage = 'Usage: %prog <server> <login> [password]\nExample: %prog jabber.org john.doe password\nProgram will output sorted list of roster contacts in form of "Alias: JID [Groups]"'
    parser = OptionParser(usage=usage, version=version)
    parser.add_option('--debug', action='store_true', default=False, help='Print debugging messages')
    (opts, args) = parser.parse_args()
    if len(args) < 2:
        parser.error('Insufficient number of arguments')
    server = args[0]
    login = args[1]
    client = xmpp.Client(server, debug='always' if opts.debug else None)
    client.connect()
    if not client.isConnected():
        print >> sys.stderr, 'Could not connect to %s' % server
        sys.exit(1)
    try:
        if len(args) < 3:
            password = getpass.getpass('Enter your password: ')
        else:
            password = args[2]
        auth = client.auth(user=login, password=password, resource='jabber-roster')
        if not auth:
            print >> sys.stderr, 'Authentication failed'
            sys.exit(2)
        roster = client.getRoster()
        jids = roster.getItems()
        output = []
        for jid in jids:
            name = roster.getName(jid)
            groups = roster.getGroups(jid)
            line = '%s: %s [%s]' % (name or '', jid, (', ').join(groups) if groups else '')
            output.append(line)

        output.sort(cmp=locale.strcoll)
        for line in output:
            sys.stdout.write(line.encode('UTF-8') + '\n')

    finally:
        client.disconnect()

    return


def main():
    """Main program entry point"""
    try:
        main_run()
    except KeyboardInterrupt:
        print 'Interrupted, exiting...'
        sys.exit(1)


if __name__ == '__main__':
    main()