# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /opt/hostedtoolcache/Python/3.8.2/x64/lib/python3.8/site-packages/musicbot/commands/local.py
# Compiled at: 2020-04-15 22:39:47
# Size of source mod 2**32: 9300 bytes
import logging, io, os, codecs, json, datetime
from shutil import copyfile
from textwrap import indent
import click
from tqdm import tqdm
from prettytable import PrettyTable
from musicbot import helpers, user
from musicbot.lib import bytes_to_human, find_files, all_files, empty_dirs, except_directories
from musicbot.music import mfilter
from musicbot.player import play
from musicbot.playlist import print_playlist
import musicbot.config as config
from musicbot.music.file import supported_formats
logger = logging.getLogger(__name__)

@click.group(help='Local music management', cls=(helpers.GroupWithHelp))
def cli():
    pass


@cli.command(help='Raw query')
@click.argument('query')
@helpers.add_options(user.auth_options)
def execute(user, query):
    print(json.dumps(user._post(query)['data']))


@cli.command()
@helpers.add_options(user.auth_options)
def load_filters(user):
    """Load default filters"""
    user.load_default_filters()


@cli.command(help='List filters')
@helpers.add_options(user.auth_options + helpers.output_option)
def filters(user, output):
    if output == 'json':
        print(json.dumps(user.filters))
    else:
        if output == 'table':
            pt = PrettyTable()
            pt.field_names = ['Name', 'Keywords', 'No keywords', 'Min rating', 'Max rating']
            for f in user.filters:
                pt.add_row([f['name'], f['keywords'], f['noKeywords'], f['minRating'], f['maxRating']])
            else:
                print(pt)


@cli.command('filter', help='Print a filter')
@helpers.add_options(user.auth_options + helpers.output_option)
@click.argument('name')
def _filter(user, name, output):
    f = user.filter(name)
    if output == 'json':
        print(json.dumps(f))
    else:
        if output == 'table':
            print(f)


@cli.command(help='Generate some stats for music collection with filters', aliases=['stat'])
@helpers.add_options(user.auth_options + helpers.output_option + mfilter.options)
def stats(user, output, **kwargs):
    mf = (mfilter.Filter)(**kwargs)
    stats = user.do_stat(mf)
    if output == 'json':
        print(json.dumps(stats))
    else:
        if output == 'table':
            pt = PrettyTable()
            pt.field_names = ['Stat', 'Value']
            pt.add_row(['Music', stats['musics']])
            pt.add_row(['Artist', stats['artists']])
            pt.add_row(['Album', stats['albums']])
            pt.add_row(['Genre', stats['genres']])
            pt.add_row(['Keywords', stats['keywords']])
            pt.add_row(['Size', bytes_to_human(int(stats['size']))])
            pt.add_row(['Total duration', datetime.timedelta(seconds=(int(stats['duration'])))])
            print(pt)


@cli.command(help='List folders')
@helpers.add_options(user.auth_options + helpers.output_option)
def folders(user, output):
    _folders = user.folders
    if output == 'json':
        print(json.dumps(_folders))
    else:
        if output == 'table':
            pt = PrettyTable()
            pt.field_names = ['Folder']
            for f in _folders:
                pt.add_row([f])
            else:
                print(pt)


@cli.command(help='(re)Load musics')
@helpers.add_options(user.auth_options + helpers.folders_argument)
def scan(user, folders):
    if not folders:
        folders = user.folders
    files = helpers.genfiles(folders)
    user.bulk_insert(files)


@cli.command(help='Just list music files')
@helpers.add_options(user.auth_options + helpers.folders_argument)
def find(user, folders):
    if not folders:
        folders = user.folders
    files = find_files(folders, supported_formats)
    for f in files:
        print(f[1])


@cli.command(help='Watch files changes in folders')
@helpers.add_options(user.auth_options)
def watch(user):
    user.watch()


@cli.command(help='Clean all musics')
@helpers.add_options(user.auth_options)
def clean(user):
    user.clean_musics()


@cli.command(help='Copy selected musics with filters to destination folder')
@helpers.add_options(user.auth_options + helpers.dry_option + mfilter.options)
@click.argument('destination')
def sync--- This code section failed: ---

 L. 137         0  LOAD_GLOBAL              logger
                2  LOAD_METHOD              info
                4  LOAD_STR                 'Destination: %s'
                6  LOAD_DEREF               'destination'
                8  CALL_METHOD_2         2  ''
               10  POP_TOP          

 L. 138        12  LOAD_GLOBAL              mfilter
               14  LOAD_ATTR                Filter
               16  BUILD_TUPLE_0         0 
               18  LOAD_FAST                'kwargs'
               20  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               22  STORE_FAST               'mf'

 L. 139        24  LOAD_FAST                'user'
               26  LOAD_METHOD              do_filter
               28  LOAD_FAST                'mf'
               30  CALL_METHOD_1         1  ''
               32  STORE_FAST               'musics'

 L. 141        34  LOAD_GLOBAL              list
               36  LOAD_GLOBAL              all_files
               38  LOAD_DEREF               'destination'
               40  CALL_FUNCTION_1       1  ''
               42  CALL_FUNCTION_1       1  ''
               44  STORE_FAST               'files'

 L. 142        46  LOAD_GLOBAL              logger
               48  LOAD_METHOD              info
               50  LOAD_STR                 'Files : '
               52  LOAD_GLOBAL              len
               54  LOAD_FAST                'files'
               56  CALL_FUNCTION_1       1  ''
               58  FORMAT_VALUE          0  ''
               60  BUILD_STRING_2        2 
               62  CALL_METHOD_1         1  ''
               64  POP_TOP          

 L. 143        66  LOAD_FAST                'files'
               68  POP_JUMP_IF_TRUE     80  'to 80'

 L. 144        70  LOAD_GLOBAL              logger
               72  LOAD_METHOD              warning
               74  LOAD_STR                 'No files found in destination'
               76  CALL_METHOD_1         1  ''
               78  POP_TOP          
             80_0  COME_FROM            68  '68'

 L. 146        80  LOAD_CLOSURE             'destination'
               82  BUILD_TUPLE_1         1 
               84  LOAD_DICTCOMP            '<code_object <dictcomp>>'
               86  LOAD_STR                 'sync.<locals>.<dictcomp>'
               88  MAKE_FUNCTION_8          'closure'
               90  LOAD_FAST                'files'
               92  GET_ITER         
               94  CALL_FUNCTION_1       1  ''
               96  STORE_FAST               'destinations'

 L. 147        98  LOAD_GLOBAL              logger
              100  LOAD_METHOD              info
              102  LOAD_STR                 'Destinations : '
              104  LOAD_GLOBAL              len
              106  LOAD_FAST                'destinations'
              108  CALL_FUNCTION_1       1  ''
              110  FORMAT_VALUE          0  ''
              112  BUILD_STRING_2        2 
              114  CALL_METHOD_1         1  ''
              116  POP_TOP          

 L. 148       118  LOAD_DICTCOMP            '<code_object <dictcomp>>'
              120  LOAD_STR                 'sync.<locals>.<dictcomp>'
              122  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              124  LOAD_FAST                'musics'
              126  GET_ITER         
              128  CALL_FUNCTION_1       1  ''
              130  STORE_FAST               'sources'

 L. 149       132  LOAD_GLOBAL              logger
              134  LOAD_METHOD              info
              136  LOAD_STR                 'Sources : '
              138  LOAD_GLOBAL              len
              140  LOAD_FAST                'sources'
              142  CALL_FUNCTION_1       1  ''
              144  FORMAT_VALUE          0  ''
              146  BUILD_STRING_2        2 
              148  CALL_METHOD_1         1  ''
              150  POP_TOP          

 L. 150       152  LOAD_GLOBAL              set
              154  LOAD_FAST                'destinations'
              156  LOAD_METHOD              keys
              158  CALL_METHOD_0         0  ''
              160  CALL_FUNCTION_1       1  ''
              162  LOAD_GLOBAL              set
              164  LOAD_FAST                'sources'
              166  LOAD_METHOD              keys
              168  CALL_METHOD_0         0  ''
              170  CALL_FUNCTION_1       1  ''
              172  BINARY_SUBTRACT  
              174  STORE_FAST               'to_delete'

 L. 151       176  LOAD_GLOBAL              logger
              178  LOAD_METHOD              info
              180  LOAD_STR                 'To delete: '
              182  LOAD_GLOBAL              len
              184  LOAD_FAST                'to_delete'
              186  CALL_FUNCTION_1       1  ''
              188  FORMAT_VALUE          0  ''
              190  BUILD_STRING_2        2 
              192  CALL_METHOD_1         1  ''
              194  POP_TOP          

 L. 152       196  LOAD_FAST                'to_delete'
          198_200  POP_JUMP_IF_FALSE   386  'to 386'

 L. 153       202  LOAD_GLOBAL              tqdm
              204  LOAD_GLOBAL              len
              206  LOAD_FAST                'to_delete'
              208  CALL_FUNCTION_1       1  ''
              210  LOAD_GLOBAL              config
              212  LOAD_ATTR                quiet
              214  LOAD_CONST               ('total', 'disable')
              216  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              218  SETUP_WITH          380  'to 380'
              220  STORE_FAST               'pbar'

 L. 154       222  LOAD_FAST                'to_delete'
              224  GET_ITER         
              226  FOR_ITER            376  'to 376'
              228  STORE_DEREF              'd'

 L. 155       230  LOAD_FAST                'pbar'
              232  LOAD_METHOD              set_description
              234  LOAD_STR                 'Deleting musics and playlists: '
              236  LOAD_GLOBAL              os
              238  LOAD_ATTR                path
              240  LOAD_METHOD              basename
              242  LOAD_FAST                'destinations'
              244  LOAD_DEREF               'd'
              246  BINARY_SUBSCR    
              248  CALL_METHOD_1         1  ''
              250  FORMAT_VALUE          0  ''
              252  BUILD_STRING_2        2 
              254  CALL_METHOD_1         1  ''
              256  POP_TOP          

 L. 156       258  LOAD_FAST                'dry'
          260_262  POP_JUMP_IF_TRUE    348  'to 348'

 L. 157       264  SETUP_FINALLY       300  'to 300'

 L. 158       266  LOAD_GLOBAL              logger
              268  LOAD_METHOD              info
              270  LOAD_STR                 'Deleting %s'
              272  LOAD_FAST                'destinations'
              274  LOAD_DEREF               'd'
              276  BINARY_SUBSCR    
              278  CALL_METHOD_2         2  ''
              280  POP_TOP          

 L. 159       282  LOAD_GLOBAL              os
              284  LOAD_METHOD              remove
              286  LOAD_FAST                'destinations'
              288  LOAD_DEREF               'd'
              290  BINARY_SUBSCR    
              292  CALL_METHOD_1         1  ''
              294  POP_TOP          
              296  POP_BLOCK        
              298  JUMP_FORWARD        346  'to 346'
            300_0  COME_FROM_FINALLY   264  '264'

 L. 160       300  DUP_TOP          
              302  LOAD_GLOBAL              OSError
              304  COMPARE_OP               exception-match
          306_308  POP_JUMP_IF_FALSE   344  'to 344'
              310  POP_TOP          
              312  STORE_FAST               'e'
              314  POP_TOP          
              316  SETUP_FINALLY       332  'to 332'

 L. 161       318  LOAD_GLOBAL              logger
              320  LOAD_METHOD              error
              322  LOAD_FAST                'e'
              324  CALL_METHOD_1         1  ''
              326  POP_TOP          
              328  POP_BLOCK        
              330  BEGIN_FINALLY    
            332_0  COME_FROM_FINALLY   316  '316'
              332  LOAD_CONST               None
              334  STORE_FAST               'e'
              336  DELETE_FAST              'e'
              338  END_FINALLY      
              340  POP_EXCEPT       
              342  JUMP_FORWARD        346  'to 346'
            344_0  COME_FROM           306  '306'
              344  END_FINALLY      
            346_0  COME_FROM           342  '342'
            346_1  COME_FROM           298  '298'
              346  JUMP_FORWARD        364  'to 364'
            348_0  COME_FROM           260  '260'

 L. 163       348  LOAD_GLOBAL              logger
              350  LOAD_METHOD              info
              352  LOAD_STR                 '[DRY-RUN] False Deleting %s'
              354  LOAD_FAST                'destinations'
              356  LOAD_DEREF               'd'
              358  BINARY_SUBSCR    
              360  CALL_METHOD_2         2  ''
              362  POP_TOP          
            364_0  COME_FROM           346  '346'

 L. 164       364  LOAD_FAST                'pbar'
              366  LOAD_METHOD              update
              368  LOAD_CONST               1
              370  CALL_METHOD_1         1  ''
              372  POP_TOP          
              374  JUMP_BACK           226  'to 226'
              376  POP_BLOCK        
              378  BEGIN_FINALLY    
            380_0  COME_FROM_WITH      218  '218'
              380  WITH_CLEANUP_START
              382  WITH_CLEANUP_FINISH
              384  END_FINALLY      
            386_0  COME_FROM           198  '198'

 L. 166       386  LOAD_GLOBAL              set
              388  LOAD_FAST                'sources'
              390  LOAD_METHOD              keys
              392  CALL_METHOD_0         0  ''
              394  CALL_FUNCTION_1       1  ''
              396  LOAD_GLOBAL              set
              398  LOAD_FAST                'destinations'
              400  LOAD_METHOD              keys
              402  CALL_METHOD_0         0  ''
              404  CALL_FUNCTION_1       1  ''
              406  BINARY_SUBTRACT  
              408  STORE_FAST               'to_copy'

 L. 167       410  LOAD_GLOBAL              logger
              412  LOAD_METHOD              info
              414  LOAD_STR                 'To copy: '
              416  LOAD_GLOBAL              len
              418  LOAD_FAST                'to_copy'
              420  CALL_FUNCTION_1       1  ''
              422  FORMAT_VALUE          0  ''
              424  BUILD_STRING_2        2 
              426  CALL_METHOD_1         1  ''
              428  POP_TOP          

 L. 168       430  LOAD_FAST                'to_copy'
          432_434  POP_JUMP_IF_FALSE   676  'to 676'

 L. 169       436  LOAD_GLOBAL              tqdm
              438  LOAD_GLOBAL              len
              440  LOAD_FAST                'to_copy'
              442  CALL_FUNCTION_1       1  ''
              444  LOAD_GLOBAL              config
              446  LOAD_ATTR                quiet
              448  LOAD_CONST               ('total', 'disable')
              450  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              452  SETUP_WITH          670  'to 670'
              454  STORE_FAST               'pbar'

 L. 170       456  LOAD_GLOBAL              sorted
              458  LOAD_FAST                'to_copy'
              460  CALL_FUNCTION_1       1  ''
              462  GET_ITER         
              464  FOR_ITER            666  'to 666'
              466  STORE_FAST               'c'

 L. 171       468  LOAD_GLOBAL              os
              470  LOAD_ATTR                path
              472  LOAD_METHOD              join
              474  LOAD_DEREF               'destination'
              476  LOAD_FAST                'c'
              478  CALL_METHOD_2         2  ''
              480  STORE_FAST               'final_destination'

 L. 172       482  SETUP_FINALLY       612  'to 612'

 L. 173       484  LOAD_FAST                'pbar'
              486  LOAD_METHOD              set_description
              488  LOAD_STR                 'Copying '
              490  LOAD_GLOBAL              os
              492  LOAD_ATTR                path
              494  LOAD_METHOD              basename
              496  LOAD_FAST                'sources'
              498  LOAD_FAST                'c'
              500  BINARY_SUBSCR    
              502  CALL_METHOD_1         1  ''
              504  FORMAT_VALUE          0  ''
              506  LOAD_STR                 ' to '
              508  LOAD_DEREF               'destination'
              510  FORMAT_VALUE          0  ''
              512  BUILD_STRING_4        4 
              514  CALL_METHOD_1         1  ''
              516  POP_TOP          

 L. 174       518  LOAD_FAST                'dry'
          520_522  POP_JUMP_IF_TRUE    580  'to 580'

 L. 175       524  LOAD_GLOBAL              logger
              526  LOAD_METHOD              info
              528  LOAD_STR                 'Copying %s to %s'
              530  LOAD_FAST                'sources'
              532  LOAD_FAST                'c'
              534  BINARY_SUBSCR    
              536  LOAD_FAST                'final_destination'
              538  CALL_METHOD_3         3  ''
              540  POP_TOP          

 L. 176       542  LOAD_GLOBAL              os
              544  LOAD_ATTR                makedirs
              546  LOAD_GLOBAL              os
              548  LOAD_ATTR                path
              550  LOAD_METHOD              dirname
              552  LOAD_FAST                'final_destination'
              554  CALL_METHOD_1         1  ''
              556  LOAD_CONST               True
              558  LOAD_CONST               ('exist_ok',)
              560  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              562  POP_TOP          

 L. 177       564  LOAD_GLOBAL              copyfile
              566  LOAD_FAST                'sources'
              568  LOAD_FAST                'c'
              570  BINARY_SUBSCR    
              572  LOAD_FAST                'final_destination'
              574  CALL_FUNCTION_2       2  ''
              576  POP_TOP          
              578  JUMP_FORWARD        598  'to 598'
            580_0  COME_FROM           520  '520'

 L. 179       580  LOAD_GLOBAL              logger
              582  LOAD_METHOD              info
              584  LOAD_STR                 '[DRY-RUN] False Copying %s to %s'
              586  LOAD_FAST                'sources'
              588  LOAD_FAST                'c'
              590  BINARY_SUBSCR    
              592  LOAD_FAST                'final_destination'
              594  CALL_METHOD_3         3  ''
              596  POP_TOP          
            598_0  COME_FROM           578  '578'

 L. 180       598  LOAD_FAST                'pbar'
              600  LOAD_METHOD              update
              602  LOAD_CONST               1
              604  CALL_METHOD_1         1  ''
              606  POP_TOP          
              608  POP_BLOCK        
              610  JUMP_BACK           464  'to 464'
            612_0  COME_FROM_FINALLY   482  '482'

 L. 181       612  DUP_TOP          
              614  LOAD_GLOBAL              KeyboardInterrupt
              616  COMPARE_OP               exception-match
          618_620  POP_JUMP_IF_FALSE   660  'to 660'
              622  POP_TOP          
              624  POP_TOP          
              626  POP_TOP          

 L. 182       628  LOAD_GLOBAL              logger
              630  LOAD_METHOD              debug
              632  LOAD_STR                 'Cleanup '
              634  LOAD_FAST                'final_destination'
              636  FORMAT_VALUE          0  ''
              638  BUILD_STRING_2        2 
              640  CALL_METHOD_1         1  ''
              642  POP_TOP          

 L. 183       644  LOAD_GLOBAL              os
              646  LOAD_METHOD              remove
              648  LOAD_FAST                'final_destination'
              650  CALL_METHOD_1         1  ''
              652  POP_TOP          

 L. 184       654  RAISE_VARARGS_0       0  'reraise'
              656  POP_EXCEPT       
              658  JUMP_BACK           464  'to 464'
            660_0  COME_FROM           618  '618'
              660  END_FINALLY      
          662_664  JUMP_BACK           464  'to 464'
              666  POP_BLOCK        
              668  BEGIN_FINALLY    
            670_0  COME_FROM_WITH      452  '452'
              670  WITH_CLEANUP_START
              672  WITH_CLEANUP_FINISH
              674  END_FINALLY      
            676_0  COME_FROM           432  '432'

 L. 186       676  LOAD_CONST               0
              678  LOAD_CONST               None
              680  IMPORT_NAME              shutil
              682  STORE_FAST               'shutil'

 L. 187       684  LOAD_GLOBAL              empty_dirs
              686  LOAD_DEREF               'destination'
              688  CALL_FUNCTION_1       1  ''
              690  GET_ITER         
              692  FOR_ITER            772  'to 772'
              694  STORE_DEREF              'd'

 L. 188       696  LOAD_GLOBAL              any
              698  LOAD_CLOSURE             'd'
              700  BUILD_TUPLE_1         1 
              702  LOAD_GENEXPR             '<code_object <genexpr>>'
              704  LOAD_STR                 'sync.<locals>.<genexpr>'
              706  MAKE_FUNCTION_8          'closure'
              708  LOAD_GLOBAL              except_directories
              710  GET_ITER         
              712  CALL_FUNCTION_1       1  ''
              714  CALL_FUNCTION_1       1  ''
          716_718  POP_JUMP_IF_FALSE   740  'to 740'

 L. 189       720  LOAD_GLOBAL              logger
              722  LOAD_METHOD              debug
              724  LOAD_STR                 'Invalid path '
              726  LOAD_DEREF               'd'
              728  FORMAT_VALUE          0  ''
              730  BUILD_STRING_2        2 
              732  CALL_METHOD_1         1  ''
              734  POP_TOP          

 L. 190   736_738  JUMP_BACK           692  'to 692'
            740_0  COME_FROM           716  '716'

 L. 191       740  LOAD_FAST                'dry'
          742_744  POP_JUMP_IF_TRUE    756  'to 756'

 L. 192       746  LOAD_FAST                'shutil'
              748  LOAD_METHOD              rmtree
              750  LOAD_DEREF               'd'
              752  CALL_METHOD_1         1  ''
              754  POP_TOP          
            756_0  COME_FROM           742  '742'

 L. 193       756  LOAD_GLOBAL              logger
              758  LOAD_METHOD              info
              760  LOAD_STR                 '[DRY-RUN] Removing empty dir %s'
              762  LOAD_DEREF               'd'
              764  CALL_METHOD_2         2  ''
              766  POP_TOP          
          768_770  JUMP_BACK           692  'to 692'

Parse error at or near `LOAD_DICTCOMP' instruction at offset 84


@cli.command(help='Generate a new playlist')
@helpers.add_options(user.auth_options + helpers.dry_option + mfilter.options + helpers.playlist_output_option)
@click.argument('path', type=(click.File('w')), default='-')
def playlist(user, output, path, dry, **kwargs):
    mf = (mfilter.Filter)(**kwargs)
    if output == 'm3u':
        p = user.playlist(mf)
        if not dry:
            print(p, file=path)
        else:
            logger.info'DRY RUN: Writing playlist to %s with content:\n%s'pathp
    elif output == 'json':
        tracks = user.do_filter(mf)
        print((json.dumps(tracks)), file=path)
    else:
        if output == 'table':
            tracks = user.do_filter(mf)
            print_playlist(tracks, path)


@cli.command(help='Generate bests playlists with some rules')
@helpers.add_options(user.auth_options + helpers.dry_option + mfilter.options)
@click.argument('path', type=click.Path(exists=True))
@click.option('--prefix', envvar='MB_PREFIX', help='Append prefix before each path (implies relative)', default='')
@click.option('--suffix', envvar='MB_SUFFIX', help='Append this suffix to playlist name', default='')
def bests(user, dry, path, prefix, suffix, **kwargs):
    if prefix:
        kwargs['relative'] = True
        if not prefix.endswith('/'):
            prefix += '/'
    mf = (mfilter.Filter)(**kwargs)
    playlists = user.bests(mf)
    with tqdm(total=(len(playlists)), disable=(config.quiet)) as (pbar):
        for p in playlists:
            playlist_filepath = os.path.joinpath(p['name'] + suffix + '.m3u')
            pbar.set_description(f"Best playlist {prefix} {suffix}: {os.path.basename(playlist_filepath)}")
            content = indent(p['content'], prefix, lambda line: line != '#EXTM3U\n')
            if not dry:
                try:
                    with codecs.openplaylist_filepath'w''utf-8-sig' as (playlist_file):
                        logger.debug'Writing playlist to %s with content:\n%s'playlist_filepathcontent
                        playlist_file.write(content)
                except (FileNotFoundError, LookupError, ValueError, UnicodeError) as e:
                    try:
                        logger.warning(f"Unable to write playlist to {playlist_filepath} because of {e}")
                    finally:
                        e = None
                        del e

            else:
                logger.info'DRY RUN: Writing playlist to %s with content:\n%s'playlist_filepathcontent
            pbar.update(1)


@cli.command(help='Music player', aliases=['play'])
@helpers.add_options(user.auth_options + mfilter.options)
def player(user, **kwargs):
    try:
        mf = (mfilter.Filter)(**kwargs)
        tracks = user.do_filter(mf)
        play(tracks)
    except io.UnsupportedOperation:
        logger.critical('Unable to load UI')