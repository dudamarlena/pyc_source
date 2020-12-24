# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/nicfit/shell/output.py
# Compiled at: 2019-09-28 20:42:58
# Size of source mod 2**32: 2471 bytes
import operator, textwrap
from pygments.token import Token
from prompt_toolkit import print_formatted_text
from prompt_toolkit.formatted_text import PygmentsTokens
from prompt_toolkit.styles.pygments import style_from_pygments_dict

class Styles:
    NAME_VALUE_DICT = {Token.Name: 'bold', 
     Token.Delim: '#0000ee', 
     Token.Value: ''}
    NAME_VALUE = style_from_pygments_dict(NAME_VALUE_DICT)
    DEFN_LIST_DICT = {Token.Name: 'italic', 
     Token.Delim: '#0000ee', 
     Token.Definition: ''}
    DEFN_LIST = style_from_pygments_dict(DEFN_LIST_DICT)
    TITLE_DICT = {Token.Title: 'bold', 
     Token.Ruler: '#0000ee'}
    TITLE = style_from_pygments_dict(TITLE_DICT)


def printNameValues(pairs, delim=' : ', pad_names=True, style=None):
    nmax = max((len(p[0] or '') for p in pairs)) if pad_names else 0
    tokens = []
    for n, v in pairs:
        if n:
            tokens += [(Token.Name, n),
             (
              Token, ' ' * (nmax - len(n)) if pad_names else ''),
             (
              Token.Delim, delim),
             (
              Token.Value, str(v)),
             (
              Token, '\n')]
    else:
        print_formatted_text((PygmentsTokens(tokens)), style=(style or Styles.NAME_VALUE))


def printDefList(pairs, delim='\n', indent=4, width=None, style=None):
    tokens = []
    for n, v in pairs:
        tokens += [(Token.Name, n), (Token.Delim, delim if v else ''),
         (
          Token, ' ' * indent if v else ''),
         (
          Token.Definition,
          textwrap.fill((str(v)), width=70, initial_indent=indent) if v else ''),
         (
          Token, '\n')]
    else:
        print_formatted_text((PygmentsTokens(tokens)), style=(style or Styles.DEFN_LIST))


def printTitle(t, hr='=', style=None):
    print_formatted_text((PygmentsTokens([
     (
      Token.Title, t), (Token, '\n'),
     (
      Token.Ruler, hr * len(t)), (Token, '\n')])),
      style=(style or Styles.TITLE))


def printRoomList(rooms_list):
    rooms = sorted(rooms_list, key=(operator.itemgetter('population')))
    for room in rooms:
        name, slug = room['name'], room['slug']
        print(f"* [{slug}]  :  {name}")
        if room['dj']:
            print(f"\tListeners: {room['population']}  |  DJ: {room['dj']}  |  Media: {room['media']}")