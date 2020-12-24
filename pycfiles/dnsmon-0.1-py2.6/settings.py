# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/dnsmon/settings.py
# Compiled at: 2011-03-21 18:12:04
mail_host = None
mail_port = None
mail_username = None
mail_password = None
mail_use_TLS = None
mail_from = None
mail_to = None
delay = 14400
dns_settings = [
 {'hostname': 'www.google.com', 
    'network': '74.125.226.0/24'}]
message = '\ndnsmon discovered a mismatched host resolution.\n\nHostname         : %(hostname)s\nResolved IP      : %(resolved_ip)s\nExpected Network : %(expected_network)s\n'
try:
    from settings_local import *
except ImportError, e:
    import sys, os
    base_directory = os.path.dirname(os.path.abspath(__file__))
    print 'Could not open settings_local.py: you have to create it.  You can do so with the following commands:'
    print
    print 'sudo cp %(base_directory)s/settings_local.py.example %(base_directory)s/settings_local.py' % {'base_directory': base_directory}
    print 'sudo editor %(base_directory)s/settings_local.py' % {'base_directory': base_directory}
    sys.exit(1)