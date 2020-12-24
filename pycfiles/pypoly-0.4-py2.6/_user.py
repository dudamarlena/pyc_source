# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pypoly/_user.py
# Compiled at: 2011-11-24 06:29:45
import pypoly, pypoly.session

class User(object):
    """
    This class provides some functions to get informations on the current user.

    :since: 0.1
    """

    def get_username(self):
        """
        Get the username for the current user.

        :return: Username as String | None = not logged in
        :since: 0.1
        """
        return pypoly.session.get_pypoly('user.username', None)

    def get_groups(self):
        """
        Get all groups the user belongs to

        :return: List with all groupnames
        :since: 0.1
        """
        return pypoly.auth.get_groups(self.get_username())

    def get_languages(self):
        """
        Get the user languages

        :return: list with all languages the user can read and understand
        """
        lang = pypoly.session.get_pypoly('user.lang', '')
        lang = lang.split(',')
        langs = []
        for temp in lang:
            langs.append(temp.strip())

        return langs