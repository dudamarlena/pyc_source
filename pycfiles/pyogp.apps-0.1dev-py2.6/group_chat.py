# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-universal/egg/pyogp/apps/examples/group_chat.py
# Compiled at: 2009-12-22 03:50:08
import re, getpass, sys, logging
from optparse import OptionParser
import uuid
from eventlet import api
from pyogp.lib.client.agent import Agent
from pyogp.lib.client.settings import Settings
from pyogp.lib.client.groups import MockChatInterface
from pyogp.lib.base.helpers import Helpers, Wait

def login():
    """ login an to a login endpoint """
    parser = OptionParser(usage='usage: %prog [options] firstname lastname')
    logger = logging.getLogger('client.example')
    parser.add_option('-l', '--loginuri', dest='loginuri', default='https://login.aditi.lindenlab.com/cgi-bin/login.cgi', help='specified the target loginuri')
    parser.add_option('-r', '--region', dest='region', default=None, help='specifies the region (regionname/x/y/z) to connect to')
    parser.add_option('-q', '--quiet', dest='verbose', default=True, action='store_false', help='enable verbose mode')
    parser.add_option('-p', '--password', dest='password', default=None, help='specifies password instead of being prompted for one')
    (options, args) = parser.parse_args()
    if len(args) != 2:
        parser.error('Expected arguments: firstname lastname')
    if options.verbose:
        console = logging.StreamHandler()
        console.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)-30s%(name)-30s: %(levelname)-8s %(message)s')
        console.setFormatter(formatter)
        logging.getLogger('').addHandler(console)
        logging.getLogger('').setLevel(logging.DEBUG)
    else:
        print 'Attention: This script will print nothing if you use -q. So it might be boring to use it like that ;-)'
    print "we are going to try and group chat with the agent's active group. set one active, or get the uuid and create a new script that does it for you!"
    print ''
    print 'This only works on unix like machines ATM.'
    if options.password:
        password = options.password
    else:
        password = getpass.getpass()
    settings = Settings()
    settings.ENABLE_INVENTORY_MANAGEMENT = False
    settings.ENABLE_OBJECT_TRACKING = False
    settings.ENABLE_COMMUNICATIONS_TRACKING = True
    settings.ENABLE_UDP_LOGGING = False
    settings.ENABLE_EQ_LOGGING = False
    settings.ENABLE_CAPS_LOGGING = False
    client = Agent(settings=settings)
    api.spawn(client.login, options.loginuri, args[0], args[1], password, start_location=options.region, connect_region=True)
    while client.connected == False:
        api.sleep(0)

    while client.region.connected == False:
        api.sleep(0)

    Wait(10)
    chat_group = client.group_manager.get_group(client.ActiveGroupID)
    chat_group.agent = client
    print ''
    print "I know, this interface is not an interface, you'll see, just type when prompted. Saijanai, sounds like you are up for a wx application. Hit Escape to trigger the message prompt."
    if chat_group != None:
        chaty_kathy = MockChatInterface(client, chat_group.chat)
        chaty_kathy.start()
    else:
        print 'We failed to find the group to start chat session :(. Continuing'
    while client.running:
        api.sleep(0)

    print ''
    print ''
    print 'At this point, we have an Agent object, Inventory dirs, and with a Region attribute'
    print 'Agent attributes:'
    for attr in client.__dict__:
        print attr, ':\t\t\t', client.__dict__[attr]

    print ''
    print ''
    print 'Known Groups:'
    for group in client.group_manager.group_store:
        print ':\t\t\t', group.GroupName
        for attr in group.__dict__:
            print '\t\t\t\t', attr, ':\t', group.__dict__[attr]

    return


def main():
    return login()


if __name__ == '__main__':
    main()