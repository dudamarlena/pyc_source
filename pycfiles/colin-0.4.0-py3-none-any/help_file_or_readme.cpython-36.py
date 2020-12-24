# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/jpopelka/git/user-cont/colin/colin/checks/best_practices/help_file_or_readme.py
# Compiled at: 2018-04-05 06:15:36
# Size of source mod 2**32: 821 bytes
from colin.checks.abstract.filesystem import FileSystemCheck

class HelpFileOrReadmeCheck(FileSystemCheck):

    def __init__(self):
        super().__init__(name='help_file_or_readme_required', message="The 'helpfile' has to be provided.",
          description="Just like traditional packages, containers need some 'man page' information about how they are to be used, configured, and integrated into a larger stack.",
          reference_url='https://fedoraproject.org/wiki/Container:Guidelines#Help_File',
          files=[
         '/help.1', '/README.md'],
          tags=[
         'filesystem', 'helpfile', 'man'],
          all_must_be_present=False)