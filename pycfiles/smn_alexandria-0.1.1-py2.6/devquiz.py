# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/alexandria/examples/devquiz.py
# Compiled at: 2011-04-12 08:16:41
from alexandria.dsl.core import MenuSystem, prompt, end
from alexandria.dsl.validators import pick_one

def get_menu():
    return MenuSystem(prompt('What is your favorite programming language?', options=('java',
                                                                                     'c',
                                                                                     'python',
                                                                                     'ruby',
                                                                                     'javascript',
                                                                                     'php',
                                                                                     'other'), validator=pick_one), prompt('What is your favorite development operating system?', options=('windows',
                                                                                                                                                                                           'apple',
                                                                                                                                                                                           '*nix',
                                                                                                                                                                                           'other'), validator=pick_one), prompt('What is your favorite development environment?', options=('netbeans',
                                                                                                                                                                                                                                                                                            'eclipse',
                                                                                                                                                                                                                                                                                            'vim',
                                                                                                                                                                                                                                                                                            'emacs',
                                                                                                                                                                                                                                                                                            'textmate',
                                                                                                                                                                                                                                                                                            'notepad'), validator=pick_one), end('Thanks! You have completed the quiz'))