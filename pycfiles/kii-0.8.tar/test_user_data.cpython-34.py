# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/eliotberriot/Seafile/kii/kii_main/kii/user/tests/test_user_data.py
# Compiled at: 2014-10-10 08:40:24
# Size of source mod 2**32: 491 bytes
from . import base
from ...tests import test_user

class TestUserData(base.UserTestCase):

    def test_user_data_created_when_user_is_saved(self):
        u = self.user_model(username='hello')
        u.save()
        self.assertEqual(u.data.__class__.__name__, 'UserData')

    def test_can_link_model_to_user_data(self):
        m = self.users[0].data
        recipe = test_user.models.Recipe(title='Something', userdata=m)
        recipe.save()
        m.recipes.add(recipe)