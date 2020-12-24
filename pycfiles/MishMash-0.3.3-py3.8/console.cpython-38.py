# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mishmash/console.py
# Compiled at: 2020-02-16 13:17:35
# Size of source mod 2**32: 2717 bytes
"""''"""
from nicfit.console.ansi import Fg
from eyed3.utils.prompt import prompt, parseIntList
from .orm import Artist

def selectArtist(heading, choices=None, multiselect=False, allow_create=True):
    color = Fg.green
    artist = None
    name = None
    menu_num = 0
    if heading:
        print(heading)
    else:
        while True:
            if artist is None:
                if choices:
                    name = choices[0].name
                    for menu_num, a in enumerate(choices, start=1):
                        print('   %d) %s' % (menu_num + 1, a.origin()))

                    if not multiselect:
                        if allow_create:
                            menu_num += 1
                            print('   %d) Enter a new artist' % menu_num)
                        choice = prompt('Which artist', type_=int, choices=(range(1, menu_num + 1)))
                        choice -= 1
                        if choice < len(choices):
                            artist = choices[choice]
                    else:

                        def _validate--- This code section failed: ---

 L.  35         0  SETUP_FINALLY        34  'to 34'

 L.  36         2  LOAD_CLOSURE             'menu_num'
                4  BUILD_TUPLE_1         1 
                6  LOAD_LISTCOMP            '<code_object <listcomp>>'
                8  LOAD_STR                 'selectArtist.<locals>._validate.<locals>.<listcomp>'
               10  MAKE_FUNCTION_8          'closure'
               12  LOAD_GLOBAL              parseIntList
               14  LOAD_FAST                '_resp'
               16  CALL_FUNCTION_1       1  ''
               18  GET_ITER         
               20  CALL_FUNCTION_1       1  ''
               22  STORE_FAST               '_ints'

 L.  38        24  LOAD_GLOBAL              bool
               26  LOAD_FAST                '_ints'
               28  CALL_FUNCTION_1       1  ''
               30  POP_BLOCK        
               32  RETURN_VALUE     
             34_0  COME_FROM_FINALLY     0  '0'

 L.  39        34  DUP_TOP          
               36  LOAD_GLOBAL              Exception
               38  COMPARE_OP               exception-match
               40  POP_JUMP_IF_FALSE    54  'to 54'
               42  POP_TOP          
               44  POP_TOP          
               46  POP_TOP          

 L.  40        48  POP_EXCEPT       
               50  LOAD_CONST               False
               52  RETURN_VALUE     
             54_0  COME_FROM            40  '40'
               54  END_FINALLY      

Parse error at or near `POP_TOP' instruction at offset 44

                        resp = prompt((color('Choose one or more artists')), validate=_validate)
                        artists = []
                        for choice in [i - 1 for i in parseIntList(resp)]:
                            artists.append(choices[choice])
                        else:
                            return artists

                if artist is None:
                    artist = promptArtist(None, name=name)
                    if choices:
                        Artist.checkUnique(choices + [artist]) or print(Fg.red('Artist entered is not unique, try again...'))
                        artist = None

    return artist


def promptArtist(text, name=None, default_name=None, default_city=None, default_state=None, default_country=None, artist=None):
    if text:
        print(text)
    if name is None:
        name = prompt((Fg.green('Artist name')), default=default_name)
    origin = {}
    for o in ('city', 'state', 'country'):
        origin['origin_%s' % o] = prompt(('   %s' % Fg.green(o.title())), default=(locals()[('default_%s' % o)]),
          required=False)

    if not artist:
        artist = Artist(name=name, **origin)
    else:
        artist.name = name
        for o in origin:
            setattr(artist, o, origin[o])
        else:
            return artist