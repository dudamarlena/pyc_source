# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/mara_kim/Documents/code/autochthe/kismet-py/kismet/__main__.py
# Compiled at: 2019-01-25 19:35:17
# Size of source mod 2**32: 400 bytes
from sys import exit
from prompt_toolkit import PromptSession
from kismet.core import process
print('Greetings, human! I am Kismet <3')
print('Input a roll and press ENTER.')
session = PromptSession('> ')
while True:
    try:
        text = session.prompt()
        print(process(text))
    except EOFError:
        exit(0)
    except KeyboardInterrupt:
        exit(130)