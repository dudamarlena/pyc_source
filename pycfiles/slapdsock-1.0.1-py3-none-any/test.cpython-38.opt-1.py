# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /slapdsock/test.py
# Compiled at: 2019-11-11 16:56:42
# Size of source mod 2**32: 1649 bytes
"""
slapdsock.test - base classes for unit tests

slapdsock - OpenLDAP back-sock listeners with Python
see https://www.stroeder.com/slapdsock.html

(c) 2015-2019 by Michael Stroeder <michael@stroeder.com>

This software is distributed under the terms of the
Apache License Version 2.0 (Apache-2.0)
https://www.apache.org/licenses/LICENSE-2.0
"""
import ldap0.test
from .service import SlapdSockServer
from .handler import NoopHandler
__all__ = [
 'SlapdObject',
 'SlapdSockTest']
SLAPD_CONF_TEMPLATE = '\nserverID %(serverid)s\nmoduleload back_%(database)s\ninclude "%(schema_include)s"\nloglevel %(loglevel)s\nallow bind_v2\n\nauthz-regexp\n  "gidnumber=%(root_gid)s\\\\+uidnumber=%(root_uid)s,cn=peercred,cn=external,cn=auth"\n  "%(rootdn)s"\n\ndatabase %(database)s\ndirectory "%(directory)s"\nsuffix "%(suffix)s"\nrootdn "%(rootdn)s"\nrootpw "%(rootpw)s"\n'

class SlapdObject(ldap0.test.SlapdObject):
    __doc__ = '\n    run test slapd process\n    '
    database = 'sock'
    slapd_conf_template = SLAPD_CONF_TEMPLATE
    suffix = 'dc=slapdsock,dc=stroeder,dc=com'


class SlapdSockTest(ldap0.test.SlapdTestCase):
    __doc__ = '\n    test class which initializes an slapd with back-sock\n    '
    server_class = SlapdObject
    slapdsock_server_class = SlapdSockServer
    slapdsock_handler_class = NoopHandler
    init_ldif_file = None

    @classmethod
    def setUpClass(cls):
        cls.server = cls.server_class()
        cls.server.start()
        cls.server = cls.server

    @classmethod
    def tearDownClass(cls):
        cls.server.stop()