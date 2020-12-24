# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/alexandria/examples/voting.py
# Compiled at: 2011-04-12 08:16:41
from alexandria.dsl.core import MenuSystem, prompt, end
from alexandria.dsl.validators import pick_one

def get_menu():
    return MenuSystem(prompt('Which solution is your favorite?', options=('Tbl1-Edu',
                                                                          'Tbl2-Edu',
                                                                          'Tbl3-Commun. info',
                                                                          'Tbl4-Mob. consc.',
                                                                          'Tbl5-Health 1',
                                                                          'Tbl5-Health 2',
                                                                          'Tbl6-Sec',
                                                                          'Tbl7-Sec',
                                                                          'Tbl8-Sec',
                                                                          'Tbl8-Edu'), validator=pick_one), end('Thanks for voting!'))