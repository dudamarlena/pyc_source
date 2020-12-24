# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/wangwenpei/Codes/nextoa/cabric/cabric/components/render.py
# Compiled at: 2017-03-20 03:08:12
import os
from cliez.components.init import InitComponent

class RenderComponent(InitComponent):
    """
    alias for cliez init component
    """
    exclude_global_option = True

    @classmethod
    def add_arguments(cls):
        """
        render project template variable.

        a legal template variable is named three underscore
         line as prefix and suffix.

        such like this: ___name___

        """
        return [
         (
          ('--yes', ), dict(action='store_true', help='clean .git repo')),
         (
          ('--variable', '-s'),
          dict(nargs='+', help='set extra variable,format is name:value')),
         (
          ('--skip-builtin', ),
          dict(action='store_true', help='skip replace builtin variable')),
         (
          ('--dir', ),
          dict(nargs='?', default=os.getcwd(), help='set working directory')),
         (
          ('--debug', ), dict(action='store_true', help='open debug mode')),
         (
          ('--dry-run', ),
          dict(action='store_true', help='print command instead execute it')),
         (
          ('--verbose', '-v'), dict(action='count'))]