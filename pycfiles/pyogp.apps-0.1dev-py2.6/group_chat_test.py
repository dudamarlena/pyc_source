# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-universal/egg/pyogp/apps/examples/group_chat_test.py
# Compiled at: 2009-12-22 03:50:08
import re, getpass, sys, logging
from optparse import OptionParser
from eventlet import api
from pyogp.lib.client.agent import Agent
from pyogp.lib.client.settings import Settings
from pyogp.lib.client.enums import AssetType
from pyogp.lib.base.datatypes import UUID
from pyogp.lib.base.message.message import Message, Block
log = logging.getLogger('group_chat')

def login():
    """ login an to a login endpoint """
    parser = OptionParser(usage='usage: %prog [options] firstname lastname groupname')
    logger = logging.getLogger('client.example')
    parser.add_option('-l', '--loginuri', dest='loginuri', default='https://login.aditi.lindenlab.com/cgi-bin/login.cgi', help='specified the target loginuri')
    parser.add_option('-r', '--region', dest='region', default=None, help='specifies the region (regionname/x/y/z) to connect to')
    parser.add_option('-q', '--quiet', dest='quiet', default=False, action='store_true', help='log warnings and above (default is debug)')
    parser.add_option('-d', '--verbose', dest='verbose', default=False, action='store_true', help='log info and above (default is debug)')
    parser.add_option('-p', '--password', dest='password', default=None, help='specifies password instead of being prompted for one')
    parser.add_option('-m', '--message', dest='message', default=None, help='The message to chat')
    (options, args) = parser.parse_args()
    if len(args) != 3:
        parser.error('Expected 3 arguments')
    (firstname, lastname, groupname) = args
    console = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)-30s%(name)-30s: %(levelname)-8s %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)
    if options.verbose:
        logging.getLogger('').setLevel(logging.INFO)
    elif options.quiet:
        logging.getLogger('').setLevel(logging.WARNING)
    else:
        logging.getLogger('').setLevel(logging.DEBUG)
    if options.password:
        password = options.password
    else:
        password = getpass.getpass()
    settings = Settings()
    settings.ENABLE_INVENTORY_MANAGEMENT = False
    settings.ENABLE_COMMUNICATIONS_TRACKING = False
    settings.ENABLE_OBJECT_TRACKING = False
    settings.ENABLE_UDP_LOGGING = True
    settings.ENABLE_EQ_LOGGING = True
    settings.ENABLE_CAPS_LOGGING = True
    settings.MULTIPLE_SIM_CONNECTIONS = False
    client = Agent(settings)
    api.spawn(client.login, options.loginuri, firstname, lastname, password, start_location=options.region, connect_region=True)
    while client.connected == False:
        api.sleep(0)

    while client.region.connected == False:
        api.sleep(0)

    while len(client.group_manager.group_store) == 0:
        api.sleep(0)

    print client.group_manager.group_store
    group = [ group for group in client.group_manager.group_store if group.GroupName == groupname ]
    if not group:
        log.error("No such group: '%s'", groupname)
        sys.exit(-1)
    group = group[0]
    if options.message:
        group.chat(options.message)
    c = 0
    while client.running:
        api.sleep(0)
        if len(group.chat_history) > c:
            print group.chat_history[c:]
            c = len(group_chat_history)

    return


def main():
    return login()


if __name__ == '__main__':
    main()