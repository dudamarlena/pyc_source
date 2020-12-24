# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/topfm/__main__.py
# Compiled at: 2019-12-30 20:32:35
# Size of source mod 2**32: 10463 bytes
import os, sys, argparse
from textwrap import dedent
from datetime import datetime
import pylast
from nicfit.aio import Application
from nicfit.logger import getLogger
from . import lastfm, collage, CACHE_D, version, PromptMode
log = getLogger('topfm.__main__')

class TopFmApp(Application):

    def _addArguments(self, parser: argparse.ArgumentParser):
        parser.add_argument('--display-name')
        parser.add_argument('-u', '--user', default='nicfit', dest='lastfm_user',
          metavar='LASTFM_USER')
        prompt_group = parser.add_mutually_exclusive_group()
        prompt_group.add_argument('--no-prompt', action='store_true')
        prompt_group.add_argument('--fail-if-prompt', action='store_true')
        subs = parser.add_subparsers(title='Subcommands', dest='subcommand')
        artists_parser = subs.add_parser('artists', help='Query top artists.')
        albums_parser = subs.add_parser('albums', help='Query top albums.')
        tracks_parser = subs.add_parser('tracks', help='Query top tracks.')
        loved_parser = subs.add_parser('loved', help='Query loved tracks.')
        recent_parser = subs.add_parser('recent', help='Query recent tracks.')
        for args, kwargs, parsers in (
         (
          ('-N', '--top-n'),
          {'default':10, 
           'type':int,  'dest':'top_n',  'metavar':'N'},
          (
           artists_parser, albums_parser, tracks_parser)),
         (
          ('-n', '--limit'),
          {'default':50, 
           'type':int,  'dest':'limit',  'metavar':'N'},
          (
           recent_parser, loved_parser)),
         (
          ('-P', '--period'),
          {'default':'overall',  'choices':lastfm.PERIODS, 
           'dest':'period'},
          (
           artists_parser, albums_parser, tracks_parser)),
         (
          ('--collage', ),
          {'default':None,  'const':'1x2x2',  'nargs':'?',  'choices':[
            '2x2', '2x4', '3x3', '4x4', '4x2',
            '5x5', '5x2', '5x3', '5x100',
            '1x2x2', '10x10', '20x20', '8x8'], 
           'dest':'collage'},
          (
           artists_parser, albums_parser)),
         (
          ('--collage-name', ),
          {'default':None,  'type':str,  'dest':'collage_name', 
           'metavar':'NAME'},
          (
           artists_parser, albums_parser)),
         (
          ('--image-size', ),
          {'default':collage.IMG_SZ,  'type':int,  'dest':'image_size', 
           'metavar':'N'},
          (
           artists_parser, albums_parser)),
         (
          ('--image-margin', ),
          {'default':0,  'type':int,  'dest':'image_margin', 
           'metavar':'N'},
          (
           artists_parser, albums_parser)),
         (
          ('--no-image-view', ), {'action': 'store_true'},
          (
           artists_parser, albums_parser)),
         (
          ('--exclude-artist', ),
          {'action':'append',  'dest':'artist_excludes'},
          (
           artists_parser, albums_parser, tracks_parser, recent_parser, loved_parser)),
         (
          ('--exclude-album', ),
          {'action':'append',  'dest':'album_excludes'},
          (
           artists_parser, albums_parser, tracks_parser, recent_parser, loved_parser)),
         (
          ('--exclude-track', ),
          {'action':'append',  'dest':'track_excludes'},
          (
           artists_parser, albums_parser, tracks_parser, recent_parser, loved_parser)),
         (
          ('--unique-artist', ),
          {'action':'store_true',  'help':'Only include top item for each artist.'},
          (
           albums_parser, tracks_parser)),
         (
          ('--no-cache', ),
          {'action':'store_true',  'help':'Refrain from using/updating image cache.'},
          (
           albums_parser, artists_parser)),
         (
          ('-L', '--show-listens'),
          {'action':'store_true',  'help':'Show # of listens with each result.'},
          (
           artists_parser, albums_parser, tracks_parser))):
            for p in parsers:
                (p.add_argument)(*args, **kwargs)

    @staticmethod
    async def _handleAlbumsCmd--- This code section failed: ---

 L. 100         0  LOAD_GLOBAL              _getTops
                2  LOAD_FAST                'args'
                4  LOAD_FAST                'lastfm_user'
                6  CALL_FUNCTION_2       2  ''
                8  UNPACK_SEQUENCE_2     2 
               10  STORE_FAST               'tops'
               12  STORE_FAST               'formatted'

 L. 101        14  LOAD_GLOBAL              print
               16  LOAD_FAST                'formatted'
               18  CALL_FUNCTION_1       1  ''
               20  POP_TOP          

 L. 103        22  LOAD_FAST                'args'
               24  LOAD_ATTR                collage
            26_28  POP_JUMP_IF_FALSE   314  'to 314'

 L. 104        30  SETUP_FINALLY       146  'to 146'

 L. 105        32  LOAD_FAST                'args'
               34  LOAD_ATTR                collage
               36  LOAD_STR                 '1x2x2'
               38  COMPARE_OP               ==
               40  POP_JUMP_IF_FALSE    64  'to 64'

 L. 106        42  LOAD_GLOBAL              collage
               44  LOAD_ATTR                img1x2x2
               46  LOAD_FAST                'tops'
               48  LOAD_FAST                'args'
               50  LOAD_ATTR                prompt_mode

 L. 107        52  LOAD_FAST                'args'
               54  LOAD_ATTR                no_cache

 L. 106        56  LOAD_CONST               ('prompts', 'disable_cache')
               58  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               60  STORE_FAST               'img'
               62  JUMP_FORWARD        142  'to 142'
             64_0  COME_FROM            40  '40'

 L. 109        64  LOAD_FAST                'args'
               66  LOAD_ATTR                collage
               68  LOAD_METHOD              count
               70  LOAD_STR                 'x'
               72  CALL_METHOD_1         1  ''
               74  LOAD_CONST               1
               76  COMPARE_OP               ==
               78  POP_JUMP_IF_TRUE     84  'to 84'
               80  LOAD_ASSERT              AssertionError
               82  RAISE_VARARGS_1       1  'exception instance'
             84_0  COME_FROM            78  '78'

 L. 110        84  LOAD_GENEXPR             '<code_object <genexpr>>'
               86  LOAD_STR                 'TopFmApp._handleAlbumsCmd.<locals>.<genexpr>'
               88  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
               90  LOAD_FAST                'args'
               92  LOAD_ATTR                collage
               94  LOAD_METHOD              split
               96  LOAD_STR                 'x'
               98  CALL_METHOD_1         1  ''
              100  GET_ITER         
              102  CALL_FUNCTION_1       1  ''
              104  UNPACK_SEQUENCE_2     2 
              106  STORE_FAST               'rows'
              108  STORE_FAST               'cols'

 L. 111       110  LOAD_GLOBAL              collage
              112  LOAD_ATTR                imgNxN
              114  LOAD_FAST                'tops'
              116  LOAD_FAST                'rows'
              118  LOAD_FAST                'cols'

 L. 112       120  LOAD_FAST                'args'
              122  LOAD_ATTR                image_size

 L. 113       124  LOAD_FAST                'args'
              126  LOAD_ATTR                image_margin

 L. 114       128  LOAD_FAST                'args'
              130  LOAD_ATTR                prompt_mode

 L. 115       132  LOAD_FAST                'args'
              134  LOAD_ATTR                no_cache

 L. 111       136  LOAD_CONST               ('rows', 'cols', 'sz', 'margin', 'prompts', 'disable_cache')
              138  CALL_FUNCTION_KW_7     7  '7 total positional and keyword args'
              140  STORE_FAST               'img'
            142_0  COME_FROM            62  '62'
              142  POP_BLOCK        
              144  JUMP_FORWARD        198  'to 198'
            146_0  COME_FROM_FINALLY    30  '30'

 L. 116       146  DUP_TOP          
              148  LOAD_GLOBAL              ValueError
              150  COMPARE_OP               exception-match
              152  POP_JUMP_IF_FALSE   196  'to 196'
              154  POP_TOP          
              156  STORE_FAST               'err'
              158  POP_TOP          
              160  SETUP_FINALLY       184  'to 184'

 L. 117       162  LOAD_GLOBAL              print
              164  LOAD_GLOBAL              str
              166  LOAD_FAST                'err'
              168  CALL_FUNCTION_1       1  ''
              170  CALL_FUNCTION_1       1  ''
              172  POP_TOP          

 L. 118       174  POP_BLOCK        
              176  POP_EXCEPT       
              178  CALL_FINALLY        184  'to 184'
              180  LOAD_CONST               4
              182  RETURN_VALUE     
            184_0  COME_FROM           178  '178'
            184_1  COME_FROM_FINALLY   160  '160'
              184  LOAD_CONST               None
              186  STORE_FAST               'err'
              188  DELETE_FAST              'err'
              190  END_FINALLY      
              192  POP_EXCEPT       
              194  JUMP_FORWARD        198  'to 198'
            196_0  COME_FROM           152  '152'
              196  END_FINALLY      
            198_0  COME_FROM           194  '194'
            198_1  COME_FROM           144  '144'

 L. 120       198  LOAD_FAST                'img'
              200  POP_JUMP_IF_TRUE    206  'to 206'
              202  LOAD_ASSERT              AssertionError
              204  RAISE_VARARGS_1       1  'exception instance'
            206_0  COME_FROM           200  '200'

 L. 121       206  LOAD_FAST                'args'
              208  LOAD_ATTR                collage_name
              210  LOAD_CONST               None
              212  COMPARE_OP               is
          214_216  POP_JUMP_IF_FALSE   254  'to 254'

 L. 123       218  LOAD_STR                 '['
              220  LOAD_FAST                'lastfm_user'
              222  FORMAT_VALUE          0  ''
              224  LOAD_STR                 ']'
              226  LOAD_FAST                'args'
              228  LOAD_ATTR                subcommand
              230  FORMAT_VALUE          0  ''
              232  LOAD_STR                 '_collage-'
              234  LOAD_FAST                'args'
              236  LOAD_ATTR                collage
              238  FORMAT_VALUE          0  ''
              240  LOAD_STR                 '-'
              242  LOAD_FAST                'args'
              244  LOAD_ATTR                period
              246  FORMAT_VALUE          0  ''
              248  BUILD_STRING_8        8 

 L. 122       250  LOAD_FAST                'args'
              252  STORE_ATTR               collage_name
            254_0  COME_FROM           214  '214'

 L. 125       254  LOAD_STR                 '{}.png'
              256  LOAD_METHOD              format
              258  LOAD_FAST                'args'
              260  LOAD_ATTR                collage_name
              262  CALL_METHOD_1         1  ''
              264  STORE_FAST               'collage_path'

 L. 126       266  LOAD_GLOBAL              print
              268  LOAD_STR                 '\nWriting {}...'
              270  LOAD_METHOD              format
              272  LOAD_FAST                'collage_path'
              274  CALL_METHOD_1         1  ''
              276  CALL_FUNCTION_1       1  ''
              278  POP_TOP          

 L. 127       280  LOAD_FAST                'img'
              282  LOAD_METHOD              save
              284  LOAD_FAST                'collage_path'
              286  CALL_METHOD_1         1  ''
              288  POP_TOP          

 L. 129       290  LOAD_FAST                'args'
              292  LOAD_ATTR                no_image_view
          294_296  POP_JUMP_IF_TRUE    314  'to 314'

 L. 130       298  LOAD_GLOBAL              os
              300  LOAD_METHOD              system
              302  LOAD_STR                 'eog {}'
              304  LOAD_METHOD              format
              306  LOAD_FAST                'collage_path'
              308  CALL_METHOD_1         1  ''
              310  CALL_METHOD_1         1  ''
              312  POP_TOP          
            314_0  COME_FROM           294  '294'
            314_1  COME_FROM            26  '26'

Parse error at or near `CALL_FINALLY' instruction at offset 178

    @staticmethod
    async def _handleArtistsCmd(args, lastfm_user):
        return await TopFmApp._handleAlbumsCmd(args, lastfm_user)

    @staticmethod
    async def _handleTracksCmd(args, lastfm_user):
        tops, formatted = _getTopsargslastfm_user
        print(formatted)

    @staticmethod
    async def _handleRecentCmd(args, lastfm_user):
        tracks = lastfm_user.get_recent_tracks(limit=(args.limit + 1))
        tracks = lastfm.filterExcludes(tracks, excludes={'artist':args.artist_excludes,  'album':args.album_excludes, 
         'track':args.track_excludes})
        text = _formatResults(tracks, args, lastfm_user, list_label='')
        print(text)

    @staticmethod
    async def _handleLovedCmd(args, lastfm_user):
        loved = lastfm.filterExcludes(lastfm_user.get_loved_tracks(limit=(args.limit or None)),
          excludes={'artist':args.artist_excludes, 
         'album':args.album_excludes, 
         'track':args.track_excludes})
        text = _formatResults(loved, args, lastfm_user, list_label='Last')
        print(text)

    async def _main--- This code section failed: ---

 L. 175         0  LOAD_GLOBAL              log
                2  LOAD_METHOD              debug
                4  LOAD_STR                 '{} started: {}'
                6  LOAD_METHOD              format
                8  LOAD_GLOBAL              sys
               10  LOAD_ATTR                argv
               12  LOAD_CONST               0
               14  BINARY_SUBSCR    
               16  LOAD_FAST                'args'
               18  CALL_METHOD_2         2  ''
               20  CALL_METHOD_1         1  ''
               22  POP_TOP          

 L. 176        24  LOAD_GLOBAL              log
               26  LOAD_METHOD              verbose
               28  LOAD_STR                 'main args: {}'
               30  LOAD_METHOD              format
               32  LOAD_FAST                'args'
               34  CALL_METHOD_1         1  ''
               36  CALL_METHOD_1         1  ''
               38  POP_TOP          

 L. 177        40  LOAD_FAST                'args'
               42  LOAD_ATTR                no_prompt
               44  POP_JUMP_IF_FALSE    62  'to 62'

 L. 178        46  LOAD_GLOBAL              PromptMode
               48  LOAD_ATTR                OFF
               50  LOAD_FAST                'args'
               52  STORE_ATTR               prompt_mode

 L. 179        54  LOAD_CONST               True
               56  LOAD_FAST                'args'
               58  STORE_ATTR               no_image_view
               60  JUMP_FORWARD         86  'to 86'
             62_0  COME_FROM            44  '44'

 L. 180        62  LOAD_FAST                'args'
               64  LOAD_ATTR                fail_if_prompt
               66  POP_JUMP_IF_FALSE    78  'to 78'

 L. 181        68  LOAD_GLOBAL              PromptMode
               70  LOAD_ATTR                FAIL
               72  LOAD_FAST                'args'
               74  STORE_ATTR               prompt_mode
               76  JUMP_FORWARD         86  'to 86'
             78_0  COME_FROM            66  '66'

 L. 183        78  LOAD_GLOBAL              PromptMode
               80  LOAD_ATTR                ON
               82  LOAD_FAST                'args'
               84  STORE_ATTR               prompt_mode
             86_0  COME_FROM            76  '76'
             86_1  COME_FROM            60  '60'

 L. 185        86  LOAD_GLOBAL              CACHE_D
               88  LOAD_METHOD              exists
               90  CALL_METHOD_0         0  ''
               92  POP_JUMP_IF_TRUE    106  'to 106'

 L. 186        94  LOAD_GLOBAL              CACHE_D
               96  LOAD_ATTR                mkdir
               98  LOAD_CONST               True
              100  LOAD_CONST               ('parents',)
              102  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              104  POP_TOP          
            106_0  COME_FROM            92  '92'

 L. 187       106  LOAD_GLOBAL              log
              108  LOAD_METHOD              debug
              110  LOAD_STR                 'Using cache directory '
              112  LOAD_GLOBAL              CACHE_D
              114  FORMAT_VALUE          0  ''
              116  BUILD_STRING_2        2 
              118  CALL_METHOD_1         1  ''
              120  POP_TOP          

 L. 189       122  LOAD_GLOBAL              lastfm
              124  LOAD_METHOD              User
              126  LOAD_FAST                'args'
              128  LOAD_ATTR                lastfm_user
              130  LOAD_GLOBAL              os
              132  LOAD_METHOD              getenv
              134  LOAD_STR                 'LASTFM_PASSWORD'
              136  CALL_METHOD_1         1  ''
              138  CALL_METHOD_2         2  ''
              140  STORE_FAST               'lastfm_user'

 L. 191       142  LOAD_GLOBAL              getattr
              144  LOAD_FAST                'self'
              146  LOAD_STR                 '_handle'
              148  LOAD_FAST                'args'
              150  LOAD_ATTR                subcommand
              152  LOAD_METHOD              title
              154  CALL_METHOD_0         0  ''
              156  FORMAT_VALUE          0  ''
              158  LOAD_STR                 'Cmd'
              160  BUILD_STRING_3        3 
              162  LOAD_CONST               None
              164  CALL_FUNCTION_3       3  ''
              166  STORE_FAST               'handler'

 L. 192       168  SETUP_FINALLY       190  'to 190'

 L. 193       170  LOAD_FAST                'handler'
              172  LOAD_FAST                'args'
              174  LOAD_FAST                'lastfm_user'
              176  CALL_FUNCTION_2       2  ''
              178  GET_AWAITABLE    
              180  LOAD_CONST               None
              182  YIELD_FROM       
              184  POP_TOP          
              186  POP_BLOCK        
              188  JUMP_FORWARD        248  'to 248'
            190_0  COME_FROM_FINALLY   168  '168'

 L. 194       190  DUP_TOP          
              192  LOAD_GLOBAL              pylast
              194  LOAD_ATTR                WSError
              196  COMPARE_OP               exception-match
              198  POP_JUMP_IF_FALSE   246  'to 246'
              200  POP_TOP          
              202  STORE_FAST               'auth_err'
              204  POP_TOP          
              206  SETUP_FINALLY       234  'to 234'

 L. 195       208  LOAD_GLOBAL              print
              210  LOAD_FAST                'auth_err'
              212  FORMAT_VALUE          0  ''
              214  LOAD_GLOBAL              sys
              216  LOAD_ATTR                stderr
              218  LOAD_CONST               ('file',)
              220  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              222  POP_TOP          

 L. 196       224  POP_BLOCK        
              226  POP_EXCEPT       
              228  CALL_FINALLY        234  'to 234'
              230  LOAD_CONST               2
              232  RETURN_VALUE     
            234_0  COME_FROM           228  '228'
            234_1  COME_FROM_FINALLY   206  '206'
              234  LOAD_CONST               None
              236  STORE_FAST               'auth_err'
              238  DELETE_FAST              'auth_err'
              240  END_FINALLY      
              242  POP_EXCEPT       
              244  JUMP_FORWARD        248  'to 248'
            246_0  COME_FROM           198  '198'
              246  END_FINALLY      
            248_0  COME_FROM           244  '244'
            248_1  COME_FROM           188  '188'

Parse error at or near `CALL_FINALLY' instruction at offset 228


def _getTops(args, lastfm_user):
    handler = getattrlastfmf"top{args.subcommand.title()}"
    handler_kwargs = dict(num=(args.top_n), excludes={'artist':args.artist_excludes, 
     'album':args.album_excludes, 
     'track':args.track_excludes})
    if 'unique_artist' in args:
        if args.unique_artist:
            handler_kwargs['unique_artist'] = args.unique_artist
    tops = handler(lastfm_user, (args.period), **handler_kwargs)
    text = _formatResults(tops, args, lastfm_user)
    return (tops, text)


def _formatResults(top_items, args, lastfm_user, list_label='Top'):
    display_name = args.display_name or lastfm_user.name
    if 'period' not in args or args.period == 'overall':
        reg = datetime.fromtimestamp(lastfm_user.get_unixtime_registered())
        period = f"overall (Since {reg:%b %d, %Y})"
    else:
        period = lastfm.periodString(args.period)
    if 'top_n' not in args:
        if 'limit' in args:
            args.top_n = args.limit
    list_label = f" {list_label}" if list_label else ''
    text = dedent(f"\n        {display_name}'s{list_label} {args.top_n} {args.subcommand} {period}:\n\n        ")
    iwitdh = len(str(len(top_items))) + 2
    for i, obj in enumeratetop_items1:
        itext = f"#{i:d}:"
        weight = None
        if isinstanceobjpylast.TopItem:
            obj_text = str(obj.item)
            weight = obj.weight
        else:
            if isinstanceobj(pylast.LovedTrack, pylast.PlayedTrack):
                obj_text = f"{obj.track.artist.name} - {obj.track.title}"
            else:
                raise NotImplemented(f"Unknown format type: {obj.__class__.__name__}")
        weight_text = ''
        if weight:
            if args.show_listens:
                weight_text = f" ({weight} listens)"
        text += f" {itext:>{iwitdh}} {obj_text}{weight_text}\n"
    else:
        text += '\n'
        return text


app = TopFmApp(version=version)
if __name__ == '__main__':
    app.run()