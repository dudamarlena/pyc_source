# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/moul/Git/moul/advanced-ssh-config/venv2.6/lib/python2.6/site-packages/advanced_ssh_config/tests/test_advanced_ssh_config.py
# Compiled at: 2015-03-23 05:07:58
import unittest
from advanced_ssh_config.advanced_ssh_config import AdvancedSshConfig
from advanced_ssh_config.exceptions import ConfigError
from . import set_config, prepare_config, DEFAULT_CONFIG
from .. import __version__

class TestRoot(unittest.TestCase):

    def test_version(self):
        self.assertIsInstance(__version__, str)


class TestAdvancedSshConfig(unittest.TestCase):

    def setUp(self):
        prepare_config()

    def test_load_advanced_ssh_config(self):
        advssh = AdvancedSshConfig()
        self.assertIsInstance(advssh, AdvancedSshConfig)

    def test_routing_simple(self):
        advssh = AdvancedSshConfig(hostname='test', port=23, verbose=True, dry_run=True)
        routing = advssh.get_routing()
        self.assertEqual(routing['port'], 23)
        self.assertEqual(routing['hostname'], 'test')
        self.assertEqual(routing['reallocalcommand'], None)
        self.assertEqual(routing['gateways'], ['direct'])
        self.assertEqual(routing['verbose'], True)
        self.assertEqual(routing['proxy_type'], 'nc')
        self.assertEqual(routing['proxy_commands'][0], [
         'nc', '-v', '-w', 180, '-G', 5, 'test', 23])
        return

    def test_routing_hostname_in_config(self):
        contents = '\n[test.com]\nhostname = 1.2.3.4\nport = 25\n'
        set_config(contents)
        advssh = AdvancedSshConfig(hostname='test.com', port=25, verbose=True, dry_run=True, configfiles=[
         DEFAULT_CONFIG])
        routing = advssh.get_routing()
        self.assertEqual(routing['port'], 25)
        self.assertEqual(routing['hostname'], '1.2.3.4')
        self.assertEqual(routing['proxy_type'], 'nc')
        self.assertEqual(routing['proxy_commands'][0], [
         'nc', '-v', '-w', 180, '-G', 5, '1.2.3.4', 25])

    def test_routing_config_override(self):
        contents = '\n[test.com]\nport = 25\n'
        set_config(contents)
        advssh = AdvancedSshConfig(hostname='test.com', port=23, verbose=True, dry_run=True, configfiles=[
         DEFAULT_CONFIG])
        routing = advssh.get_routing()
        self.assertEqual(routing['port'], 23)
        self.assertEqual(routing['hostname'], 'test.com')
        self.assertEqual(routing['proxy_type'], 'nc')
        self.assertEqual(routing['proxy_commands'][0], [
         'nc', '-v', '-w', 180, '-G', 5, 'test.com', 23])

    def test_routing_via_two_other_hosts(self):
        advssh = AdvancedSshConfig(hostname='aaa.com/bbb.com/ccc.com')
        routing = advssh.get_routing()
        self.assertEqual(routing['hostname'], 'aaa.com')
        self.assertEqual(routing['proxy_type'], 'nc')
        self.assertEqual(routing['gateways'], ['direct'])
        self.assertEqual(routing['proxy_commands'][0], [
         'nc', '-w', 180, '-G', 5, 'aaa.com', 22])
        self.assertEqual(routing['gateway_route'], ['bbb.com', 'ccc.com'])

    def test_routing_via_two_other_hosts_with_config_one(self):
        contents = '\n[ddd.com]\nhostname = 1.2.3.4\nport = 25\n'
        set_config(contents)
        advssh = AdvancedSshConfig(hostname='ddd.com/eee.com', configfiles=[
         DEFAULT_CONFIG])
        routing = advssh.get_routing()
        self.assertEqual(routing['hostname'], '1.2.3.4')
        self.assertEqual(routing['proxy_type'], 'nc')
        self.assertEqual(routing['gateways'], ['direct'])
        self.assertEqual(routing['proxy_commands'][0], [
         'nc', '-w', 180, '-G', 5, '1.2.3.4', 25])
        self.assertEqual(routing['gateway_route'], ['eee.com'])

    def test_prepare_sshconfig_simple(self):
        contents = '\n[test]\nport = 25\n\n[default]\nport = 24\n'
        set_config(contents)
        advssh = AdvancedSshConfig(hostname='test', configfiles=[
         DEFAULT_CONFIG])
        config = advssh.prepare_sshconfig()
        self.assertEqual(len(config.keys()), 2)
        self.assertEqual(config['test'].host, 'test')
        self.assertEqual(config['test'].config, [('port', '25')])
        self.assertEqual(config['default'].host, 'default')
        self.assertEqual(config['default'].config, [('port', '24')])

    def test_prepare_sshconfig_multiline(self):
        contents = '\n[test]\nlocalforward = 1 2.3.4.5 6 \n 7 8.9.10.11 12\n'
        set_config(contents)
        advssh = AdvancedSshConfig(hostname='test', configfiles=[
         DEFAULT_CONFIG])
        config = advssh.prepare_sshconfig()
        self.assertEqual(config['test'].host, 'test')
        self.assertEqual(config['test'].config, [
         ('localforward', '1 2.3.4.5 6'),
         ('localforward', '7 8.9.10.11 12')])

    def test_inherits(self):
        contents = '\n[aaa]\nhostname = 1.2.3.4\nuser = toto\n\n[bbb]\ninherits = aaa\nport = 23\n'
        set_config(contents)
        advssh = AdvancedSshConfig(hostname='test', configfiles=[
         DEFAULT_CONFIG])
        config = advssh.config.full
        self.assertEqual(config['aaa'].clean_config['user'], ['toto'])
        self.assertEqual('port' in config['aaa'].clean_config, False)
        self.assertEqual(config['bbb'].clean_config['user'], ['toto'])
        self.assertEqual(config['bbb'].clean_config['port'], ['23'])

    def test_build_ssh_config(self):
        contents = '\n[aaa]\nhostname = 1.2.3.4\nuser = toto\n\n[bbb]\ninherits = aaa\nport = 23\n'
        set_config(contents)
        advssh = AdvancedSshConfig(hostname='test', configfiles=[
         DEFAULT_CONFIG])
        config = advssh.prepare_sshconfig()
        arr = advssh.build_sshconfig()
        string = ('\n').join(arr)
        self.assertEquals(len(arr), 14)
        dest = ('\n# assh version: {}\n\nHost aaa\n  user toto\n  # hostname 1.2.3.4\n\nHost bbb\n  port 23\n  user toto\n  # inherits aaa\n\nHost *\n  proxycommand assh connect %h --port=%p\n').format(__version__)
        self.assertEquals(string.strip(), dest.strip())

    def test_build_ssh_config_with_proxycommand(self):
        contents = '\n[aaa]\nhostname = 1.2.3.4\nuser = toto\n\n[bbb]\ninherits = aaa\nport = 23\n\n[default]\nProxyCommand = assh connect %h --port=%p\nUser = titi\n'
        set_config(contents)
        advssh = AdvancedSshConfig(hostname='test', configfiles=[
         DEFAULT_CONFIG])
        config = advssh.prepare_sshconfig()
        arr = advssh.build_sshconfig()
        string = ('\n').join(arr)
        dest = ('\n# assh version: {}\n\nHost aaa\n  user toto\n  # hostname 1.2.3.4\n\nHost bbb\n  port 23\n  user toto\n  # inherits aaa\n\nHost *\n  proxycommand assh connect %h --port=%p\n  user titi\n').format(__version__)
        self.assertEquals(string.strip(), dest.strip())

    def test_build_ssh_config_sorted(self):
        contents = '\n[ddd]\ninherits = aaa\nport = 23\nuser = titi\n\n[bbb]\nuser = titi\ninherits = aaa\nport = 23\nhostname = 1.1.1.1\n\n[ccc]\nhostname = 5.4.3.2\ninherits = aaa\nport = 23\n\n[aaa]\nhostname = 1.2.3.4\nuser = toto\n'
        set_config(contents)
        advssh = AdvancedSshConfig(hostname='test', configfiles=[
         DEFAULT_CONFIG])
        config = advssh.prepare_sshconfig()
        arr = advssh.build_sshconfig()
        string = ('\n').join(arr)
        dest = ('\n# assh version: {}\n\nHost aaa\n  user toto\n  # hostname 1.2.3.4\n\nHost bbb\n  port 23\n  user titi\n  # hostname 1.1.1.1\n  # inherits aaa\n\nHost ccc\n  port 23\n  user toto\n  # hostname 5.4.3.2\n  # inherits aaa\n\nHost ddd\n  port 23\n  user titi\n  # inherits aaa\n\nHost *\n  proxycommand assh connect %h --port=%p\n').format(__version__)
        self.assertEquals(string.strip(), dest.strip())

    def test_inherits_noexists(self):
        contents = '\n[aaa]\nhostname = 1.2.3.4\nuser = toto\n\n[bbb]\ninherits = ccc\nport = 23\n'
        set_config(contents)
        advssh = AdvancedSshConfig(hostname='test', configfiles=[
         DEFAULT_CONFIG])
        config = advssh.config.full

        def call():
            return config['bbb'].clean_config

        self.assertRaises(ConfigError, call)

    def test_inherits_deep(self):
        contents = '\n[aaa]\nhostname = 1.2.3.4\nuser = toto\n\n[bbb]\ninherits = aaa\ntcpkeepalive = 42\n\n[ccc]\ninherits = bbb\n'
        set_config(contents)
        advssh = AdvancedSshConfig(hostname='test', configfiles=[
         DEFAULT_CONFIG])
        config = advssh.config.full
        self.assertEqual(config['ccc'].clean_config['user'], ['toto'])
        self.assertEqual(config['ccc'].clean_config['tcpkeepalive'], ['42'])

    def test_inherits_override(self):
        contents = '\n[aaa]\nuser = toto\n\n[bbb]\ninherits = aaa\nuser = titi\n'
        set_config(contents)
        advssh = AdvancedSshConfig(hostname='test', configfiles=[
         DEFAULT_CONFIG])
        config = advssh.config.full
        self.assertEqual(config['aaa'].clean_config['user'], ['toto'])
        self.assertEqual(config['bbb'].clean_config['user'], ['titi'])

    def test_inherits_loop(self):
        contents = '\n[aaa]\ninherits = ccc\n\n[bbb]\ninherits = aaa\n\n[ccc]\ninherits = bbb\n'
        set_config(contents)
        advssh = AdvancedSshConfig(hostname='test', configfiles=[
         DEFAULT_CONFIG])
        config = advssh.config.full

        def call(key):
            return config[key].clean_config

        self.assertRaises(ConfigError, call, 'aaa')
        self.assertRaises(ConfigError, call, 'bbb')
        self.assertRaises(ConfigError, call, 'ccc')

    def test_inherits_loop_self(self):
        contents = '\n[aaa]\ninherits = aaa\n'
        set_config(contents)
        advssh = AdvancedSshConfig(hostname='test', configfiles=[
         DEFAULT_CONFIG])
        config = advssh.config.full

        def call(key):
            return config[key].clean_config

        self.assertRaises(ConfigError, call, 'aaa')

    def test_reserved_key(self):
        contents = '\n[aaa]\nuser = toto\nproxycommand = nc\nhostname = titi\nalias = tutu\ngateways = toutou\nreallocalcommand = tonton\nremotecommand = tantan\nincludes = tuotuo\ninherits = bbb\npassword = 4242\ncomment = 4343\n[bbb]\n'
        set_config(contents)
        advssh = AdvancedSshConfig(hostname='test', configfiles=[
         DEFAULT_CONFIG])
        config = advssh.config.full
        self.assertEquals(config['aaa'].clean_config, {'user': ['toto'], 'proxycommand': ['nc']})

    def test_comment_simple(self):
        contents = '\n[test]\ncomment = Hello\n'
        config = set_config(contents)
        advssh = AdvancedSshConfig(hostname='test', configfiles=[
         DEFAULT_CONFIG])
        routing = advssh.get_routing()
        self.assertEquals(routing['comment'], ['Hello'])

    def test_comment_multiline(self):
        contents = '\n[test]\ncomment = Hello\n          World\n                         !\n\nport = 22\n'
        config = set_config(contents)
        advssh = AdvancedSshConfig(hostname='test', configfiles=[
         DEFAULT_CONFIG])
        routing = advssh.get_routing()
        self.assertEquals(routing['comment'], ['Hello', 'World', '!'])

    def test_build_ssh_config_with_multiline_localforward_onliner(self):
        contents = '\n[localhost]\nuser = toto\nlocalforward = 1 2.3.4.5 6 \n 7 8.9.10.11 12\nport = 22\n'
        set_config(contents)
        advssh = AdvancedSshConfig(hostname='localhost', configfiles=[
         DEFAULT_CONFIG])
        config = advssh.prepare_sshconfig()
        arr = advssh.build_sshconfig()
        string = ('\n').join(arr)
        self.assertEquals(len(arr), 11)
        dest = ('\n# assh version: {}\n\nHost localhost\n  localforward 1 2.3.4.5 6\n  localforward 7 8.9.10.11 12\n  port 22\n  user toto\n\nHost *\n  proxycommand assh connect %h --port=%p\n').format(__version__)
        self.assertEquals(string.strip(), dest.strip())

    def test_build_ssh_config_with_multiline_localforward(self):
        contents = '\n[localhost]\nuser = toto\nlocalforward = 1 2.3.4.5 6\n               7 8.9.10.11 12\nport = 22\n'
        set_config(contents)
        advssh = AdvancedSshConfig(hostname='localhost', configfiles=[
         DEFAULT_CONFIG])
        config = advssh.prepare_sshconfig()
        arr = advssh.build_sshconfig()
        string = ('\n').join(arr)
        self.assertEquals(len(arr), 11)
        dest = ('\n# assh version: {}\n\nHost localhost\n  localforward 1 2.3.4.5 6\n  localforward 7 8.9.10.11 12\n  port 22\n  user toto\n\nHost *\n  proxycommand assh connect %h --port=%p\n').format(__version__)
        self.assertEquals(string.strip(), dest.strip())

    def test_build_ssh_config_with_multiline_comment(self):
        contents = '\n[localhost]\nport = 22\ncomment = .\n          .            O\n          .     _______O_\n          .    /       O \\\n          .   / _ _ O _ _ \\\n          .    |    _    |\n          .    | o | | o |\n          .    |___|_|___|\n          .\nuser = toto\n'
        set_config(contents)
        advssh = AdvancedSshConfig(hostname='localhost', configfiles=[
         DEFAULT_CONFIG])
        config = advssh.prepare_sshconfig()
        arr = advssh.build_sshconfig()
        string = ('\n').join(arr)
        dest = ('\n# assh version: {}\n\nHost localhost\n  port 22\n  user toto\n  # comment .\n  # comment .            O\n  # comment .     _______O_\n  # comment .    /       O \\\n  # comment .   / _ _ O _ _ \\\n  # comment .    |    _    |\n  # comment .    | o | | o |\n  # comment .    |___|_|___|\n  # comment .\n\nHost *\n  proxycommand assh connect %h --port=%p\n').format(__version__)
        self.assertEquals(string.strip(), dest.strip())