# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\tests\core\parsers\q3a\test_abstractParser.py
# Compiled at: 2016-03-08 18:42:10
from b3.parsers.q3a.abstractParser import AbstractParser
from mock import Mock
import unittest2 as unittest

class Test(unittest.TestCase):

    def test_getCvar(self):
        mock_parser = Mock(spec=AbstractParser)
        mock_parser._reCvarName = AbstractParser._reCvarName
        mock_parser._reCvar = AbstractParser._reCvar
        mock_parser.getCvar = AbstractParser.getCvar

        def assertGetCvar(cvar_name, gameserver_response, expected_response):
            mock_parser.write = Mock(return_value=gameserver_response)
            cvar = mock_parser.getCvar(mock_parser, cvar_name)
            if cvar is None:
                self.assertEqual(expected_response, None)
            else:
                self.assertEqual(expected_response, (cvar.name, cvar.value, cvar.default))
            return

        assertGetCvar('g_password', '"g_password" is:"^7" default:"scrim^7"', ('g_password',
                                                                               '',
                                                                               'scrim'))
        assertGetCvar('g_password', '"g_password" is:"^7" default:"^7"', ('g_password',
                                                                          '', ''))
        assertGetCvar('g_password', '"g_password" is:"test^7" default:"^7"', ('g_password',
                                                                              'test',
                                                                              ''))
        assertGetCvar('g_password', 'whatever', None)
        assertGetCvar('g_password', '"g_password" is:"^7"', ('g_password', '', None))
        assertGetCvar('sv_maxclients', '"sv_maxclients" is:"16^7" default:"8^7"', ('sv_maxclients',
                                                                                   '16',
                                                                                   '8'))
        assertGetCvar('g_maxGameClients', '"g_maxGameClients" is:"0^7", the default', ('g_maxGameClients',
                                                                                       '0',
                                                                                       '0'))
        assertGetCvar('mapname', '"mapname" is:"ut4_abbey^7"', ('mapname', 'ut4_abbey',
                                                                None))
        return


if __name__ == '__main__':
    unittest.main()