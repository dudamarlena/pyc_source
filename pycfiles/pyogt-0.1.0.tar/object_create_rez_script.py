# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.6-universal/egg/pyogp/apps/examples/object_create_rez_script.py
# Compiled at: 2009-12-22 03:50:08
import re, getpass, sys, logging
from optparse import OptionParser
import time
from eventlet import api
from pyogp.lib.client.agent import Agent
from pyogp.lib.client.settings import Settings
from pyogp.lib.base.datatypes import UUID
from pyogp.lib.client.enums import AssetType, WearablesIndex, InventoryType

def login():
    """ login an to a login endpoint """
    parser = OptionParser(usage='usage: %prog [options] firstname lastname')
    logger = logging.getLogger('client.example')
    parser.add_option('-l', '--loginuri', dest='loginuri', default='https://login.aditi.lindenlab.com/cgi-bin/login.cgi', help='specified the target loginuri')
    parser.add_option('-r', '--region', dest='region', default=None, help='specifies the region to connect to')
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
    if options.password:
        password = options.password
    else:
        password = getpass.getpass()
    settings = Settings()
    settings.ENABLE_INVENTORY_MANAGEMENT = True
    settings.ENABLE_EQ_LOGGING = False
    settings.ENABLE_CAPS_LOGGING = False
    client = Agent(settings=settings)
    api.spawn(client.login, options.loginuri, args[0], args[1], password, start_location=options.region, connect_region=True)
    while client.connected == False:
        api.sleep(0)

    while client.region.connected == False:
        api.sleep(0)

    while client.Position.X == 0.0 and client.Position.Y == 0.0 and client.Position.Z == 0.0:
        api.sleep(10)

    [ client.inventory._request_folder_contents(folder.FolderID) for folder in client.inventory.folders if folder.ParentID == client.inventory.inventory_root.FolderID ]
    now = time.time()
    start = now
    while now - start < 5 and client.running:
        api.sleep()
        now = time.time()

    matches = client.inventory.search_inventory(client.inventory.folders, name='Scripts')
    folder = matches.pop()
    script = '\ndefault\n{\n    state_entry()\n    {\n        llSay(0, "Hello, PyBOT!");\n    }\n\n    touch_start(integer total_number)\n    {\n        llSay(0, "PyBOT says Hi.");\n    }\n}\n'
    client.inventory.create_new_item(folder, 'TestLSL1', 'created by PyOGP', AssetType.LSLText, InventoryType.LSL, WearablesIndex.WT_SHAPE, 0, lambda item: client.asset_manager.upload_script_via_caps(item.ItemID, script))
    api.sleep(5)
    matches = client.inventory.search_inventory(client.inventory.folders, name='TestLSL1')
    script = matches.pop()
    object_handler = client.events_handler.register('ObjectSelected')

    def rez_script(payload):
        client.region.objects.send_RezScript(client, payload.payload['object'], script.ItemID)
        object_handler.unsubscribe(rez_script)

    object_handler.subscribe(rez_script)
    client.region.objects.create_default_box(GroupID=client.ActiveGroupID)
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
    print 'Objects being tracked: %s' % len(client.region.objects.object_store)
    print ''
    print ''
    states = {}
    for _object in client.region.objects.object_store:
        if str(client.agent_id) == str(_object.OwnerID):
            print 'My OBJECT'
            print
            print
        if _object.State != None:
            print 'LocalID:', _object.LocalID, '\tUUID: ', _object.FullID, '\tState: ', _object.State, '\tPosition: ', _object.Position
        elif states.has_key(_object.State):
            states[_object.State] += 1
        else:
            states[_object.State] = 1

    print ''
    print "Object states I don't care about atm"
    for state in states:
        print '\t State: ', state, '\tFrequency: ', states[state]

    print ''
    print ''
    print 'Avatars being tracked: %s' % len(client.region.objects.avatar_store)
    print ''
    print ''
    for _avatar in client.region.objects.avatar_store:
        print 'ID:', _avatar.LocalID, '\tUUID: ', _avatar.FullID, '\tNameValue: ', _avatar.NameValue, '\tPosition: ', _avatar.Position

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