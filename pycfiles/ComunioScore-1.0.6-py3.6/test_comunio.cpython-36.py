# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ComunioScore/test/test_comunio.py
# Compiled at: 2020-03-29 20:59:07
# Size of source mod 2**32: 6158 bytes
import os, unittest, configparser
from ComunioScore.comunio import Comunio
from ComunioScore import ROOT_DIR

class TestComunio(unittest.TestCase):

    def setUp(self) -> None:
        self.config = configparser.ConfigParser()
        self.config.read(ROOT_DIR + '/config/cfg.ini')
        self.use_env = False
        try:
            self.username = self.config.get('comunio', 'username')
            self.password = self.config.get('comunio', 'password')
        except (KeyError, configparser.NoSectionError) as e:
            self.use_env = True

        self.comunio = Comunio()
        self.test_login()

    def test_login(self):
        if self.use_env:
            login = self.comunio.login(username=(os.environ['comunio_username']), password=(os.environ['comunio_password']))
        else:
            login = self.comunio.login(username=(self.username), password=(self.password))
        self.assertTrue(login, msg='Login process for comunio failed')

    def test_get_auth_info(self):
        auth_info = self.comunio.get_auth_info()
        self.assertIsInstance(auth_info, dict, msg='auth_info must be type of dict')

    def test_get_all_user_ids(self):
        user_ids = self.comunio.get_all_user_ids()
        self.assertIsInstance(user_ids, list, msg='user_ids must be type of list')
        for user in user_ids:
            self.assertIsInstance(user, dict, msg='user in user_ids must be type of dict')
            self.assertIn('id', user, msg="'id' not in user dict")
            self.assertIn('name', user, msg="'name' not in user dict")

    def test_get_player_standings(self):
        player_standing = self.comunio.get_player_standings()
        self.assertIsInstance(player_standing, list, msg='player_standing must be type of list')
        for player in player_standing:
            self.assertIsInstance(player, dict, msg='player within player_standing must be type of dict')
            self.assertIn('id', player, msg='player dict has no key id')
            self.assertIn('name', player, msg='player dict has no key name')
            self.assertIn('points', player, msg='player dict has no key points')
            self.assertIn('teamValue', player, msg='player dict has no key teamValue')

    def test_set_auth_token(self):
        pass

    def test_get_auth_token(self):
        auth_token = self.comunio.get_auth_token()
        self.assertIsInstance(auth_token, str, msg='auth_token must be type of string')

    def test_get_auth_expire_time(self):
        auth_expire_time = self.comunio.get_auth_expire_time()
        self.assertIsInstance(auth_expire_time, str, msg='auth_expire_time must be type of string')

    def test_get_user_id(self):
        user_id = self.comunio.get_user_id()
        self.assertIsInstance(user_id, str, msg='user_id must be type of str')

    def test_get_community_id(self):
        community_id = self.comunio.get_community_id()
        self.assertIsInstance(community_id, str, msg='community_id must be type of string')

    def test_get_get_community_name(self):
        community_name = self.comunio.get_community_name()
        self.assertIsInstance(community_name, str, msg='community_name must be type of string')

    def test_get_wealth(self):
        user_id = self.comunio.get_user_id()
        wealth = self.comunio.get_wealth(userid=user_id)
        if wealth is None:
            self.assertIsNone(wealth, msg='wealth must be of type None')
        else:
            self.assertIsInstance(wealth, int, msg='wealth must be type of int')

    def test_get_squad(self):
        user_id = self.comunio.get_user_id()
        squad = self.comunio.get_squad(userid=user_id)
        self.assertIsInstance(squad, list, msg="'squad' must be type of list")
        for player in squad:
            self.assertIsInstance(player, dict, msg='player within squad list must be type of dict')
            self.assertIn('id', player, msg='player dict has no key id')
            self.assertIn('name', player, msg='player dict has no key name')
            self.assertIn('club', player, msg='player dict has no key club')

    def test_get_comunio_user_data(self):
        user_data = self.comunio.get_comunio_user_data()
        self.assertIsInstance(user_data, list, msg='comunio_user_data must be type of list')
        for user in user_data:
            self.assertIsInstance(user, dict, msg='user in comunio_user_data must be type of dict')
            self.assertIn('id', user, msg='user in comunio_user_data has no key id')
            self.assertIn('name', user, msg='user in comunio_user_data has no key name')
            self.assertIn('squad', user, msg='user in comunio_user_data has no key squad')
            for player_dict in user['squad']:
                self.assertIsInstance(player_dict, dict, msg='player_dict in user[squad] must be type of dict')
                self.assertIn('name', player_dict, msg='player_dict has no key name')
                self.assertIn('club', player_dict, msg='player_dict has no key club')
                self.assertIn('position', player_dict, msg='player_dict has no key position')

    def tearDown(self) -> None:
        self.comunio.__del__()


if __name__ == '__main__':
    unittest.main()