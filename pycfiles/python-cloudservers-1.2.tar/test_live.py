# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jacob/Projects/cloudservers/tests/test_live.py
# Compiled at: 2009-12-04 19:16:30
import os, functools, cloudservers, time
from nose.plugins.skip import SkipTest
TESTABLE = 'CLOUD_SERVERS_USERNAME' in os.environ and 'CLOUD_SERVERS_API_KEY' in os.environ
if TESTABLE:
    cs = cloudservers.CloudServers(os.environ['CLOUD_SERVERS_USERNAME'], os.environ['CLOUD_SERVERS_API_KEY'])

def live(test):

    @functools.wraps(test)
    def _test():
        if not TESTABLE:
            raise SkipTest('no creds in environ')
        test()

    return _test


@live
def test_create_destroy():
    for im in cs.images.list():
        if im.name == 'Ubuntu 9.10 (karmic)':
            break

    for flav in cs.flavors.list():
        if flav.ram == 256:
            break

    s = cs.servers.create('testserver', im, flav)
    while s.status != 'ACTIVE':
        time.sleep(10)
        s.get()

    s.delete()