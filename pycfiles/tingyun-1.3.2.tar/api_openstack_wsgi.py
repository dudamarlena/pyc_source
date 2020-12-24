# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nb/publish/btw/tingyun/tingyun/armoury/nova/api_openstack_wsgi.py
# Compiled at: 2016-06-30 06:13:10
"""Define this module for openstack nova model

"""
from tingyun.armoury.trigger.wsgi_entrance import wsgi_application_wrapper, TARGET_NOVA_APP

def resource_wsgi_entrance(module):
    """
    :param module:
    :return:
    """
    version = 'xx'
    try:
        import nova
        version = getattr(nova, '__version__', 'xx')
    except Exception as _:
        pass

    wsgi_application_wrapper(module.Resource, '__call__', ('nova', version, TARGET_NOVA_APP))