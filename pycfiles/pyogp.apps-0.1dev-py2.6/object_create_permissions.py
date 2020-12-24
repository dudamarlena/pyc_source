# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-universal/egg/pyogp/apps/examples/object_create_permissions.py
# Compiled at: 2009-12-22 03:50:08
import re, getpass, sys, logging
from optparse import OptionParser
import time
from eventlet import api
from pyogp.lib.client.agent import Agent
from pyogp.lib.client.settings import Settings
from pyogp.lib.base.helpers import Wait
object_names = [
 'Alpha', 'Bravo', 'Charlie', 'Delta', 'Echo', 'Foxtrot']

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
    if options.password:
        password = options.password
    else:
        password = getpass.getpass()
    settings = Settings()
    settings.ENABLE_INVENTORY_MANAGEMENT = False
    settings.ENABLE_EQ_LOGGING = False
    settings.ENABLE_CAPS_LOGGING = False
    client = Agent(settings=settings)
    api.spawn(client.login, options.loginuri, args[0], args[1], password, start_location=options.region, connect_region=True)
    while client.connected == False:
        api.sleep(0)

    while client.region.connected == False:
        api.sleep(0)

    waiter = Wait(5)
    for i in range(len(object_names)):
        client.region.objects.create_default_box(GroupID=client.ActiveGroupID, relative_position=(i + 1, 0, 0))

    waiter = Wait(5)
    objects_nearby = client.region.objects.find_objects_within_radius(20)
    for item in objects_nearby:
        item.select(client)

    waiter = Wait(15)
    for item in objects_nearby:
        item.deselect(client)

    my_objects = client.region.objects.my_objects()
    print 'Hey! Will try to set object names'
    print 'Hey! Will try to set permissions.'
    i = 0
    for item in my_objects:
        fixed_name = object_names[i]
        print ' for LocalID %s : %s ' % (item.LocalID, fixed_name)
        item.set_object_name(client, fixed_name)
        if fixed_name == 'Alpha':
            item.set_object_transfer_only_permissions(client)
        elif fixed_name == 'Bravo':
            item.set_object_copy_transfer_permissions(client)
        elif fixed_name == 'Charlie':
            item.set_object_mod_transfer_permissions(client)
        elif fixed_name == 'Delta':
            item.set_object_full_permissions(client)
        elif fixed_name == 'Echo':
            item.set_object_copy_only_permissions(client)
        elif fixed_name == 'Foxtrot':
            item.set_object_copy_mod_permissions(client)
        else:
            print 'Name Does Not Match!'
        i = i + 1
        waiter = Wait(2)
        item.take(client)

    waiter = Wait(30)
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
        if _object.State == 0:
            print 'Object attributes'
            for attr in _object.__dict__:
                print '\t\t%s:\t\t%s' % (attr, _object.__dict__[attr])

            print ''
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
    for _avatar in client.region.objects.avatar_store:
        print 'LocalID:', _avatar.LocalID, '\tUUID: ', _avatar.FullID, '\tNameValue: ', _avatar.NameValue, '\tPosition: ', _avatar.Position

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