# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.6-universal/egg/pyogp/apps/examples/inventory_transfer_specify_agent.py
# Compiled at: 2009-12-22 03:50:08
import re, getpass, sys, logging
from optparse import OptionParser
import time
from eventlet import api
from pyogp.lib.client.agent import Agent
from pyogp.lib.client.agentmanager import AgentManager
from pyogp.lib.client.settings import Settings
from pyogp.lib.base.helpers import Wait

def login():
    """ login an to a login endpoint """
    parser = OptionParser(usage='usage: %prog [options] firstname lastname')
    logger = logging.getLogger('client.example')
    parser.add_option('-l', '--loginuri', dest='loginuri', default='https://login.aditi.lindenlab.com/cgi-bin/login.cgi', help='specified the target loginuri')
    parser.add_option('-r', '--region', dest='region', default=None, help='specifies the region (regionname/x/y/z) to connect to')
    parser.add_option('-q', '--quiet', dest='verbose', default=True, action='store_false', help='enable verbose mode')
    parser.add_option('-t', '--to_agent_id', dest='to_agent_id', default=None, help='agent id to offer inventory to (required)')
    parser.add_option('-s', '--search', dest='search', default=None, help='name of inventory item to search for and transfer to account number 2')
    parser.add_option('-p', '--password', dest='password', default=None, help='specifies password instead of being prompted for one')
    (options, args) = parser.parse_args()
    if len(args) != 2:
        parser.error('Expected arguments: firstname lastname')
    if options.to_agent_id == None:
        parser.error('Missing required target agent id')
    if options.verbose:
        console = logging.StreamHandler()
        console.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)-30s%(name)-30s: %(levelname)-8s %(message)s')
        console.setFormatter(formatter)
        logging.getLogger('').addHandler(console)
        logging.getLogger('').setLevel(logging.DEBUG)
    else:
        print 'Attention: This script will print nothing if you use -q. So it might be boring to use it like that ;-)'
    settings = Settings()
    settings.ENABLE_INVENTORY_MANAGEMENT = True
    settings.ENABLE_COMMUNICATIONS_TRACKING = False
    settings.ENABLE_OBJECT_TRACKING = False
    settings.ENABLE_UDP_LOGGING = True
    settings.ENABLE_EQ_LOGGING = True
    settings.ENABLE_CAPS_LOGGING = True
    settings.MULTIPLE_SIM_CONNECTIONS = False
    if options.password:
        password = options.password
    else:
        password = getpass.getpass()
    client = Agent(settings=settings)
    api.spawn(client.login, options.loginuri, args[0], args[1], password, start_location=options.region, connect_region=True)
    while client.connected == False:
        api.sleep(0)

    while client.region.connected == False:
        api.sleep(0)

    [ client.inventory._request_folder_contents(folder.FolderID) for folder in client.inventory.folders if folder.ParentID == client.inventory.inventory_root.FolderID ]
    Wait(10)
    if options.search != None:
        matches = client.inventory.search_inventory(name=options.search)
        item_to_give = matches[0]
        print ''
        print ''
        print ''
        print ''
        print 'Found item to give to another agent: %s' % str(item_to_give.__dict__)
        print ''
        print ''
        print ''
        print ''
        client.inventory.give_inventory(item_to_give.ItemID, options.to_agent_id)
    while client.running:
        api.sleep(0)

    return


def main():
    return login()


if __name__ == '__main__':
    main()