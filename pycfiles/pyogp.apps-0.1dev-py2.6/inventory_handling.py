# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-universal/egg/pyogp/apps/examples/inventory_handling.py
# Compiled at: 2009-12-22 03:50:08
import re, getpass, sys, logging
from optparse import OptionParser
import time
from eventlet import api
from pyogp.lib.client.agent import Agent
from pyogp.lib.client.settings import Settings

def login():
    """ login an to a login endpoint """
    parser = OptionParser(usage='usage: %prog [options] firstname lastname')
    logger = logging.getLogger('client.example')
    parser.add_option('-l', '--loginuri', dest='loginuri', default='https://login.aditi.lindenlab.com/cgi-bin/login.cgi', help='specified the target loginuri')
    parser.add_option('-r', '--region', dest='region', default=None, help='specifies the region (regionname/x/y/z) to connect to')
    parser.add_option('-q', '--quiet', dest='verbose', default=True, action='store_false', help='enable verbose mode')
    parser.add_option('-s', '--search', dest='search', default=None, help='inventory item to search for an rez (optional)')
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
    if options.password:
        password = options.password
    else:
        password = getpass.getpass()
    settings = Settings()
    settings.ENABLE_OBJECT_TRACKING = False
    client = Agent(settings=settings)
    api.spawn(client.login, options.loginuri, args[0], args[1], password, start_location=options.region, connect_region=True)
    while client.connected == False:
        api.sleep(0)

    while client.region.connected == False:
        api.sleep(0)

    [ client.inventory._request_folder_contents(folder.FolderID) for folder in client.inventory.folders if folder.ParentID == client.inventory.inventory_root.FolderID ]
    now = time.time()
    start = now
    while now - start < 5 and client.running:
        api.sleep()
        now = time.time()

    if options.search != None:
        matches = client.inventory.search_inventory(name=options.search)
        item_to_rez = matches[0]
        print item_to_rez.__dict__
        print dir(item_to_rez)
        item_to_rez.rez_object(client)
    now = time.time()
    start = now
    while now - start < 30 and client.running:
        api.sleep()

    client.logout()
    print ''
    print ''
    print 'At this point, we have an Agent object, Inventory dirs, and with a Region attribute'
    print 'Agent attributes:'
    for attr in client.__dict__:
        print attr, ':\t\t\t', client.__dict__[attr]

    print ''
    print ''
    print 'Inventory: %s folders' % len(client.inventory.folders)
    for inv_folder in client.inventory.folders:
        print 'Inventory Folder', ':\t\t\t', inv_folder.Name
        for item in inv_folder.inventory:
            print '    ', item.Name

    print ''
    print ''
    print 'Region attributes:'
    for attr in client.region.__dict__:
        print attr, ':\t\t\t', client.region.__dict__[attr]

    return


def main():
    return login()


if __name__ == '__main__':
    main()