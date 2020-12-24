# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/grey/.pyenv/versions/cm/lib/python2.7/site-packages/tests/cm_libcloud/test_libcloud_api.py
# Compiled at: 2017-04-23 10:30:41
""" run with

python setup.py install; nosetests -v --nocapture  tests/cm_libcloud/test_libcloud_api.py:Test_libcloud_api.test_001

nosetests -v --nocapture tests/libcloud/test_libcloud_api.py

or

nosetests -v tests/test_image.py

"""
from cloudmesh_client.cloud.iaas.CloudProvider import CloudProvider
from cloudmesh_client.common.util import HEADING

class Test_libcloud_api(object):
    """
        This class tests the ImageCommand
    """

    def test_001(self):
        """test image list :return: """
        HEADING()
        from pprint import pprint
        cloud = 'chameleon-ec2'
        provider = CloudProvider(cloud).provider
        print (
         provider, type(provider))
        for kind in ['image']:
            r = provider.list(kind, cloud)
            pprint(r)

        assert True

    def test_002(self):
        """ test flavor list :return:  """
        HEADING()
        from pprint import pprint
        cloud = 'chameleon-ec2'
        provider = CloudProvider(cloud).provider
        kind = 'flavor'
        r = provider.list(kind, cloud)
        pprint(r)
        assert 't2.small' in str(r)
        r = provider.list_flavor(cloud)
        pprint(r)
        assert 't2.small' in str(r)
        r = provider.provider.list_sizes(cloud)
        pprint(r)
        assert 't2.small' in str(r)

    def test_003(self):
        """ test vm list:return:  """
        HEADING()
        from pprint import pprint
        cloud = 'chameleon-ec2'
        provider = CloudProvider(cloud).provider
        print (
         provider, type(provider))
        for kind in ['vm']:
            r = provider.list(kind, cloud)
            pprint(r)

        assert True

    def test_004(self):
        """ test key list:return:"""
        HEADING()
        from pprint import pprint
        cloud = 'chameleon-ec2'
        provider = CloudProvider(cloud).provider
        print (
         provider, type(provider))
        for kind in ['key']:
            r = provider.list(kind, cloud)
            pprint(r)

        assert True