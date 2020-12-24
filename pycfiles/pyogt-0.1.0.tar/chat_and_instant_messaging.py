# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.6-universal/egg/pyogp/apps/examples/chat_and_instant_messaging.py
# Compiled at: 2009-12-22 03:50:08
import re, getpass, sys, logging
from optparse import OptionParser
from eventlet import api
from pyogp.lib.client.agent import Agent
from pyogp.lib.client.settings import Settings

def login():
    """ login an to a login endpoint """
    parser = OptionParser(usage='usage: %prog [options] firstname lastname')
    logger = logging.getLogger('client.example')
    parser.add_option('-l', '--loginuri', dest='loginuri', default='https://login.aditi.lindenlab.com/cgi-bin/login.cgi', help='specified the target loginuri')
    parser.add_option('-r', '--region', dest='region', default=None, help='specifies the region (regionname/x/y/z) to connect to')
    parser.add_option('-u', '--uuid', dest='uuid', default='00000000-0000-0000-0000-000000000000', help='uuid of the agent to send an instant message to')
    parser.add_option('-q', '--quiet', dest='verbose', default=True, action='store_false', help='enable verbose mode')
    parser.add_option('-p', '--password', dest='password', default=None, help='specifies password instead of being prompted for one')
    (options, args) = parser.parse_args()
    if len(args) != 2:
        parser.error('Expected arguments: firstname lastname')
    if options.verbose:
        console = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)-30s%(name)-30s: %(levelname)-8s %(message)s')
        console.setFormatter(formatter)
        logging.getLogger('').addHandler(console)
        logging.getLogger('').setLevel(logging.DEBUG)
    else:
        print 'Attention: This script will print nothing if you use -q. So it might be boring to use it like that ;-)'
    if options.password:
        password = options.password
    else:
        password = getpass.getpass()
    settings = Settings()
    settings.ENABLE_INVENTORY_MANAGEMENT = False
    settings.ENABLE_OBJECT_TRACKING = False
    client = Agent(settings=settings)
    api.spawn(client.login, options.loginuri, args[0], args[1], password, start_location=options.region, connect_region=True)
    while client.connected == False:
        api.sleep(0)

    while client.Position == None:
        api.sleep(0)

    im_handler = client.events_handler.register('InstantMessageReceived')
    im_handler.subscribe(chat_handler)
    im_handler = client.events_handler.register('ChatReceived')
    im_handler.subscribe(chat_handler)
    client.say("Hi, I'm a bot!")
    client.instant_message(options.uuid, 'Look, I can even speak to you in IM-ese')
    client.instant_message(options.uuid, 'I can even send 2 messages!')
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
    print 'Region attributes:'
    for attr in client.region.__dict__:
        print attr, ':\t\t\t', client.region.__dict__[attr]

    return


def main():
    return login()


def chat_handler(message_info):
    print ''
    print '%s: OMG, I got an message, and it is being handled by my mock application!' % message_info.name
    print ''
    for key in message_info.payload:
        print key + ': ' + str(message_info.payload[key])

    print ''


if __name__ == '__main__':
    main()