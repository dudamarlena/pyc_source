# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/nicfit/__main__.py
# Compiled at: 2020-04-04 14:09:08
# Size of source mod 2**32: 12679 bytes
import os, shutil, subprocess, collections
from uuid import uuid4
from hashlib import md5
from pathlib import Path
from tempfile import NamedTemporaryFile
import nicfit
from . import version
from .util import copytree
from .console import ansi, perr, pout
from console.ansi import Fg, Style
try:
    from cookiecutter.main import cookiecutter
    from cookiecutter.exceptions import CookiecutterException
    import click.exceptions
except ImportError:
    cookiecutter = None
else:
    HASH_FILE = Path('./.cookiecutter.md5')
    MERGE_TOOLS = collections.OrderedDict()
    MERGE_TOOLS['meld'] = None
    MERGE_TOOLS['gvimdiff'] = '-geometry 169x60 -f'
    MERGE_TOOLS['vimdiff'] = None

    @nicfit.Command.register
    class Requirements(nicfit.Command):
        __doc__ = '\n    TODO\n        - infile arg\n\n    '
        NAME = 'requirements'
        ALIASES = ['reqs']

        def _splitPkg(self, line):
            pkg, ver = line, None
            for c in ('=', '>', '<'):
                i = line.find(c)
                if i != -1:
                    pkg = line[0:i]
                    ver = line[i:]
                    break
                return (
                 pkg, ver)

        def _readReq(self, file):
            reqs = {}
            file.seek(0)
            for line in [l.strip() for l in file.readlines() if l.strip() if not l.startswith('#')]:
                pkg, version = self._splitPkg(line)
                reqs[pkg] = version
            else:
                return reqs

        def _makeReqsFile(self, filepath, reqs):
            file_exists = filepath.exists()
            with filepath.open('r+' if file_exists else 'w') as (fp):
                new = {}
                curr = self._readReq(fp) if file_exists else {}
                for r in [r.strip() for r in reqs if r if r.strip()]:
                    pkg, ver = self._splitPkg(r)
                    if ver is None:
                        if pkg in curr:
                            ver = curr[pkg]
                    new[pkg] = ver
                else:
                    fp.seek(0)
                    fp.truncate(0)
                    for pkg in sorted(new.keys()):
                        ver = new[pkg] or ''
                        fp.write(('{pkg}{ver}\n'.format)(**locals()))
                    else:
                        pout('Wrote {}'.format(filepath))

        def _run(self):
            import yaml
            reqs_file = Path('./requirements/requirements.yml')
            if not reqs_file.exists():
                pout('Nothing to do...')
                return None
            reqs_dir = reqs_file.parent
            reqs_yaml = yaml.safe_load(reqs_file.open())
            for name in reqs_yaml.keys():
                if reqs_yaml[name]:
                    self._makeReqsFile(reqs_dir / (name + '.txt'), reqs_yaml[name])
            else:
                pkg_reqs = []
                for name, pkgs in reqs_yaml.items():
                    if name == 'main' or name.startswith('extra_'):
                        pkg_reqs += pkgs or []
                else:
                    self._makeReqsFile(Path('requirements.txt'), pkg_reqs)


    @nicfit.Command.register
    class CookieCutter(nicfit.Command):
        NAME = 'cookiecutter'
        HELP = 'Create a nicfit.py Python project skeleton.'
        OLD_CC_USER_CONFIG = '.cookiecutter.json'
        CC_USER_CONFIG = '.cookiecutter.yml'
        ALIASES = ['cc']

        def _initArgParser(self, parser):
            parser.add_argument('outdir', metavar='PATH', help='Where to output the generated project dir into')
            parser.add_argument('--config-file', metavar='PATH', help='User configuration file',
              default=None)
            parser.add_argument('--no-input', action='store_true', help=('Do not prompt for parameters and only use {} file content'.format(self.CC_USER_CONFIG)))
            parser.add_argument('--no-config', action='store_true', help='Use no user config (overrides --config_file)')
            parser.add_argument('--no-clone', action='store_true', help='Do not clone a local repo if one is found.')
            parser.add_argument('--merge', action='store_true', help='Merge CookieCutter output against local repository (if found). Ignored when used with --no-clone')
            parser.add_argument('--ignore-md5s', action='store_true', help='Causes all files to be merged even if the saved md5sum matches from a previous merge.')
            parser.add_argument('--extra-merge', action='append', nargs=2, metavar='FILE',
              default=[],
              help='Merge two files there are outside the context of the git repo (e.g. untracked files, .git/hooks, etc.). This option may be specified multiple times.')
            parser.add_argument('--merge-cmd', metavar='CMD', help='Merge command. Called with with 2 args: <src> <dest>')

        def _findTemplateDir(self):
            template_d = None
            for p in (Path(__file__).parent / 'cookiecutter',
             Path(__file__).parent.parent / 'cookiecutter'):
                if p.exists():
                    template_d = p
                    break
                assert template_d
                return template_d

        def _cookiecutter--- This code section failed: ---

 L. 152         0  SETUP_FINALLY        42  'to 42'

 L. 153         2  LOAD_GLOBAL              cookiecutter
                4  LOAD_GLOBAL              str
                6  LOAD_FAST                'template_d'
                8  CALL_FUNCTION_1       1  ''

 L. 154        10  LOAD_FAST                'self'
               12  LOAD_ATTR                args
               14  LOAD_ATTR                config_file

 L. 155        16  LOAD_FAST                'self'
               18  LOAD_ATTR                args
               20  LOAD_ATTR                no_input

 L. 156        22  LOAD_CONST               True

 L. 157        24  LOAD_FAST                'self'
               26  LOAD_ATTR                args
               28  LOAD_ATTR                outdir

 L. 153        30  LOAD_CONST               ('config_file', 'no_input', 'overwrite_if_exists', 'output_dir')
               32  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
               34  STORE_FAST               'cc_dir'

 L. 158        36  LOAD_FAST                'cc_dir'
               38  POP_BLOCK        
               40  RETURN_VALUE     
             42_0  COME_FROM_FINALLY     0  '0'

 L. 159        42  DUP_TOP          
               44  LOAD_GLOBAL              click
               46  LOAD_ATTR                exceptions
               48  LOAD_ATTR                Abort
               50  COMPARE_OP               exception-match
               52  POP_JUMP_IF_FALSE    70  'to 70'
               54  POP_TOP          
               56  POP_TOP          
               58  POP_TOP          

 L. 160        60  LOAD_GLOBAL              KeyboardInterrupt
               62  CALL_FUNCTION_0       0  ''
               64  RAISE_VARARGS_1       1  'exception instance'
               66  POP_EXCEPT       
               68  JUMP_FORWARD        138  'to 138'
             70_0  COME_FROM            52  '52'

 L. 161        70  DUP_TOP          
               72  LOAD_GLOBAL              CookiecutterException
               74  COMPARE_OP               exception-match
               76  POP_JUMP_IF_FALSE   136  'to 136'
               78  POP_TOP          
               80  STORE_FAST               'ex'
               82  POP_TOP          
               84  SETUP_FINALLY       124  'to 124'

 L. 162        86  LOAD_GLOBAL              nicfit
               88  LOAD_METHOD              CommandError
               90  LOAD_STR                 'CookieCutter error: {}'
               92  LOAD_METHOD              format

 L. 163        94  LOAD_GLOBAL              str
               96  LOAD_FAST                'ex'
               98  CALL_FUNCTION_1       1  ''
              100  POP_JUMP_IF_FALSE   110  'to 110'
              102  LOAD_GLOBAL              str
              104  LOAD_FAST                'ex'
              106  CALL_FUNCTION_1       1  ''
              108  JUMP_FORWARD        114  'to 114'
            110_0  COME_FROM           100  '100'

 L. 164       110  LOAD_FAST                'ex'
              112  LOAD_ATTR                __class__
            114_0  COME_FROM           108  '108'

 L. 162       114  CALL_METHOD_1         1  ''
              116  CALL_METHOD_1         1  ''
              118  RAISE_VARARGS_1       1  'exception instance'
              120  POP_BLOCK        
              122  BEGIN_FINALLY    
            124_0  COME_FROM_FINALLY    84  '84'
              124  LOAD_CONST               None
              126  STORE_FAST               'ex'
              128  DELETE_FAST              'ex'
              130  END_FINALLY      
              132  POP_EXCEPT       
              134  JUMP_FORWARD        138  'to 138'
            136_0  COME_FROM            76  '76'
              136  END_FINALLY      
            138_0  COME_FROM           134  '134'
            138_1  COME_FROM            68  '68'

Parse error at or near `POP_TOP' instruction at offset 56

        def _run(self):
            if not cookiecutter:
                raise nicfit.CommandError('CookierCutter not installed')
            else:
                cwd = Path(os.getcwd())
                clone_d = None
                if (cwd / '.git').is_dir():
                    if not self.args.no_clone:
                        pout('Cloning local repo for CookieCutter merging (use --no-clone to disable)')
                        clone_d = self._gitCloneRepo(cwd)
                elif self.args.no_config:
                    self.args.config_file = None
                else:
                    if not self.args.config_file:
                        local_config = Path(cwd) / self.CC_USER_CONFIG
                        old_local_config = Path(cwd) / self.OLD_CC_USER_CONFIG
                        if local_config.is_file():
                            self.args.config_file = str(local_config)
                        else:
                            if old_local_config.is_file():
                                self.args.config_file = str(old_local_config)
                if self.args.config_file:
                    pout('Using user config ./{}, use --no-config to ignore.'.format(self.CC_USER_CONFIG))
                cc_dir = self._cookiecutter(self._findTemplateDir())
                if clone_d:
                    copytree(str(cc_dir), str(clone_d))
                    shutil.rmtree(str(cc_dir))
                    os.rename(str(clone_d), str(cc_dir))
                    if self.args.merge:
                        self._merge(cc_dir)

        def _gitCloneRepo(self, repo_path):
            try:
                p = subprocess.run('git rev-parse --abbrev-ref HEAD', shell=True, stdout=(subprocess.PIPE),
                  check=True)
                branch = str(p.stdout, 'utf-8').strip()
                clone_d = Path(self.args.outdir) / str(uuid4())
                p = subprocess.run(("git clone --depth=1 --branch {branch} file://`pwd` '{clone_d}'".format)(**locals()),
                  shell=True,
                  stdout=(subprocess.PIPE),
                  check=True)
                return clone_d
                    except subprocess.CalledProcessError as err:
                try:
                    raise nicfit.CommandError(str(err))
                finally:
                    err = None
                    del err

        def _merge--- This code section failed: ---

 L. 215         0  BUILD_MAP_0           0 
                2  STORE_FAST               'md5_hashes'

 L. 216         4  LOAD_GLOBAL              HASH_FILE
                6  LOAD_METHOD              exists
                8  CALL_METHOD_0         0  ''
               10  POP_JUMP_IF_FALSE   104  'to 104'

 L. 217        12  LOAD_LISTCOMP            '<code_object <listcomp>>'
               14  LOAD_STR                 'CookieCutter._merge.<locals>.<listcomp>'
               16  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
               18  LOAD_GLOBAL              HASH_FILE
               20  LOAD_METHOD              read_text
               22  CALL_METHOD_0         0  ''
               24  LOAD_METHOD              split
               26  LOAD_STR                 '\n'
               28  CALL_METHOD_1         1  ''
               30  GET_ITER         
               32  CALL_FUNCTION_1       1  ''
               34  GET_ITER         
             36_0  COME_FROM            84  '84'
             36_1  COME_FROM            76  '76'
             36_2  COME_FROM            68  '68'
             36_3  COME_FROM            42  '42'
               36  FOR_ITER            104  'to 104'
               38  STORE_FAST               'line'

 L. 218        40  LOAD_FAST                'line'
               42  POP_JUMP_IF_FALSE    36  'to 36'

 L. 219        44  LOAD_FAST                'line'
               46  LOAD_ATTR                rsplit
               48  LOAD_STR                 ':'
               50  LOAD_CONST               1
               52  LOAD_CONST               ('maxsplit',)
               54  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               56  STORE_FAST               'values'

 L. 220        58  LOAD_GLOBAL              len
               60  LOAD_FAST                'values'
               62  CALL_FUNCTION_1       1  ''
               64  LOAD_CONST               2
               66  COMPARE_OP               ==
               68  POP_JUMP_IF_FALSE    36  'to 36'
               70  LOAD_FAST                'values'
               72  LOAD_CONST               0
               74  BINARY_SUBSCR    
               76  POP_JUMP_IF_FALSE    36  'to 36'
               78  LOAD_FAST                'values'
               80  LOAD_CONST               1
               82  BINARY_SUBSCR    
               84  POP_JUMP_IF_FALSE    36  'to 36'

 L. 221        86  LOAD_FAST                'values'
               88  LOAD_CONST               1
               90  BINARY_SUBSCR    
               92  LOAD_FAST                'md5_hashes'
               94  LOAD_FAST                'values'
               96  LOAD_CONST               0
               98  BINARY_SUBSCR    
              100  STORE_SUBSCR     
              102  JUMP_BACK            36  'to 36'
            104_0  COME_FROM            10  '10'

 L. 223       104  SETUP_FINALLY       208  'to 208'

 L. 224       106  LOAD_GLOBAL              subprocess
              108  LOAD_ATTR                run
              110  LOAD_STR                 'git -C "{cc_dir}" status --porcelain -uall'
              112  LOAD_ATTR                format
              114  BUILD_TUPLE_0         0 

 L. 225       116  LOAD_GLOBAL              locals
              118  CALL_FUNCTION_0       0  ''

 L. 224       120  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'

 L. 226       122  LOAD_CONST               True

 L. 226       124  LOAD_GLOBAL              subprocess
              126  LOAD_ATTR                PIPE

 L. 227       128  LOAD_CONST               True

 L. 224       130  LOAD_CONST               ('shell', 'stdout', 'check')
              132  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              134  STORE_FAST               'p'

 L. 228       136  BUILD_LIST_0          0 
              138  STORE_FAST               'merge_files'

 L. 229       140  LOAD_GLOBAL              str
              142  LOAD_FAST                'p'
              144  LOAD_ATTR                stdout
              146  LOAD_STR                 'utf-8'
              148  CALL_FUNCTION_2       2  ''
              150  LOAD_METHOD              strip
              152  CALL_METHOD_0         0  ''
              154  STORE_FAST               'status'

 L. 230       156  LOAD_LISTCOMP            '<code_object <listcomp>>'
              158  LOAD_STR                 'CookieCutter._merge.<locals>.<listcomp>'
              160  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              162  LOAD_FAST                'status'
              164  LOAD_METHOD              split
              166  LOAD_STR                 '\n'
              168  CALL_METHOD_1         1  ''
              170  GET_ITER         
              172  CALL_FUNCTION_1       1  ''
              174  GET_ITER         
            176_0  COME_FROM           182  '182'
              176  FOR_ITER            204  'to 204'
              178  STORE_FAST               'line'

 L. 231       180  LOAD_FAST                'line'
              182  POP_JUMP_IF_FALSE   176  'to 176'

 L. 232       184  LOAD_FAST                'merge_files'
              186  LOAD_METHOD              append
              188  LOAD_GLOBAL              tuple
              190  LOAD_FAST                'line'
              192  LOAD_METHOD              split
              194  CALL_METHOD_0         0  ''
              196  CALL_FUNCTION_1       1  ''
              198  CALL_METHOD_1         1  ''
              200  POP_TOP          
              202  JUMP_BACK           176  'to 176'
              204  POP_BLOCK        
              206  JUMP_FORWARD        260  'to 260'
            208_0  COME_FROM_FINALLY   104  '104'

 L. 233       208  DUP_TOP          
              210  LOAD_GLOBAL              subprocess
              212  LOAD_ATTR                CalledProcessError
              214  COMPARE_OP               exception-match
          216_218  POP_JUMP_IF_FALSE   258  'to 258'
              220  POP_TOP          
              222  STORE_FAST               'err'
              224  POP_TOP          
              226  SETUP_FINALLY       246  'to 246'

 L. 234       228  LOAD_GLOBAL              nicfit
              230  LOAD_METHOD              CommandError
              232  LOAD_GLOBAL              str
              234  LOAD_FAST                'err'
              236  CALL_FUNCTION_1       1  ''
              238  CALL_METHOD_1         1  ''
              240  RAISE_VARARGS_1       1  'exception instance'
              242  POP_BLOCK        
              244  BEGIN_FINALLY    
            246_0  COME_FROM_FINALLY   226  '226'
              246  LOAD_CONST               None
              248  STORE_FAST               'err'
              250  DELETE_FAST              'err'
              252  END_FINALLY      
              254  POP_EXCEPT       
              256  JUMP_FORWARD        260  'to 260'
            258_0  COME_FROM           216  '216'
              258  END_FINALLY      
            260_0  COME_FROM           256  '256'
            260_1  COME_FROM           206  '206'

 L. 236       260  LOAD_FAST                'merge_files'
              262  LOAD_FAST                'self'
              264  LOAD_ATTR                args
              266  LOAD_ATTR                extra_merge
              268  BINARY_ADD       
              270  GET_ITER         
            272_0  COME_FROM           766  '766'
            272_1  COME_FROM           468  '468'
          272_274  FOR_ITER            822  'to 822'
              276  UNPACK_SEQUENCE_2     2 
              278  STORE_FAST               'st'
              280  STORE_FAST               'file'

 L. 237       282  LOAD_GLOBAL              Path
              284  LOAD_FAST                'file'
              286  CALL_FUNCTION_1       1  ''
              288  STORE_FAST               'dst'

 L. 238       290  LOAD_FAST                'cc_dir'
              292  LOAD_FAST                'dst'
              294  BINARY_TRUE_DIVIDE
              296  STORE_FAST               'src'

 L. 240       298  LOAD_GLOBAL              md5
              300  CALL_FUNCTION_0       0  ''
              302  STORE_FAST               'hasher'

 L. 241       304  SETUP_FINALLY       324  'to 324'

 L. 242       306  LOAD_FAST                'hasher'
              308  LOAD_METHOD              update
              310  LOAD_FAST                'src'
              312  LOAD_METHOD              read_bytes
              314  CALL_METHOD_0         0  ''
              316  CALL_METHOD_1         1  ''
              318  POP_TOP          
              320  POP_BLOCK        
              322  JUMP_FORWARD        378  'to 378'
            324_0  COME_FROM_FINALLY   304  '304'

 L. 243       324  DUP_TOP          
              326  LOAD_GLOBAL              FileNotFoundError
              328  COMPARE_OP               exception-match
          330_332  POP_JUMP_IF_FALSE   376  'to 376'
              334  POP_TOP          
              336  STORE_FAST               'notfound'
              338  POP_TOP          
              340  SETUP_FINALLY       364  'to 364'

 L. 244       342  LOAD_GLOBAL              perr
              344  LOAD_FAST                'notfound'
              346  CALL_FUNCTION_1       1  ''
              348  POP_TOP          

 L. 245       350  POP_BLOCK        
              352  POP_EXCEPT       
              354  CALL_FINALLY        364  'to 364'
          356_358  JUMP_BACK           272  'to 272'
              360  POP_BLOCK        
              362  BEGIN_FINALLY    
            364_0  COME_FROM           354  '354'
            364_1  COME_FROM_FINALLY   340  '340'
              364  LOAD_CONST               None
              366  STORE_FAST               'notfound'
              368  DELETE_FAST              'notfound'
              370  END_FINALLY      
              372  POP_EXCEPT       
              374  JUMP_FORWARD        378  'to 378'
            376_0  COME_FROM           330  '330'
              376  END_FINALLY      
            378_0  COME_FROM           374  '374'
            378_1  COME_FROM           322  '322'

 L. 246       378  LOAD_FAST                'hasher'
              380  LOAD_METHOD              hexdigest
              382  CALL_METHOD_0         0  ''
              384  STORE_FAST               'md5sum'

 L. 247       386  LOAD_FAST                'self'
              388  LOAD_ATTR                args
              390  LOAD_ATTR                ignore_md5s
          392_394  JUMP_IF_TRUE_OR_POP   416  'to 416'

 L. 248       396  LOAD_FAST                'file'
              398  LOAD_FAST                'md5_hashes'
              400  COMPARE_OP               not-in

 L. 247   402_404  JUMP_IF_TRUE_OR_POP   416  'to 416'

 L. 249       406  LOAD_FAST                'md5sum'
              408  LOAD_FAST                'md5_hashes'
              410  LOAD_FAST                'file'
              412  BINARY_SUBSCR    
              414  COMPARE_OP               !=
            416_0  COME_FROM           402  '402'
            416_1  COME_FROM           392  '392'

 L. 247       416  STORE_FAST               'merge_file'

 L. 250       418  LOAD_GLOBAL              pout
              420  LOAD_STR                 'Comparing {} hash({}): {}'
              422  LOAD_METHOD              format

 L. 251       424  LOAD_FAST                'file'

 L. 251       426  LOAD_FAST                'md5sum'

 L. 252       428  LOAD_FAST                'merge_file'

 L. 251   430_432  POP_JUMP_IF_FALSE   444  'to 444'
              434  LOAD_GLOBAL              Fg
              436  LOAD_METHOD              blue
              438  LOAD_STR                 'new'
              440  CALL_METHOD_1         1  ''
              442  JUMP_FORWARD        452  'to 452'
            444_0  COME_FROM           430  '430'

 L. 252       444  LOAD_GLOBAL              Fg
              446  LOAD_METHOD              green
              448  LOAD_STR                 'merged'
              450  CALL_METHOD_1         1  ''
            452_0  COME_FROM           442  '442'

 L. 250       452  CALL_METHOD_3         3  ''
              454  CALL_FUNCTION_1       1  ''
              456  POP_TOP          

 L. 253       458  LOAD_FAST                'md5sum'
              460  LOAD_FAST                'md5_hashes'
              462  LOAD_FAST                'file'
              464  STORE_SUBSCR     

 L. 255       466  LOAD_FAST                'merge_file'
          468_470  POP_JUMP_IF_FALSE   272  'to 272'

 L. 256       472  LOAD_CONST               None
              474  STORE_FAST               'tmp_dst'

 L. 257       476  LOAD_FAST                'dst'
              478  LOAD_METHOD              exists
              480  CALL_METHOD_0         0  ''
          482_484  POP_JUMP_IF_TRUE    520  'to 520'

 L. 258       486  LOAD_GLOBAL              NamedTemporaryFile
              488  LOAD_STR                 'w'
              490  LOAD_FAST                'dst'
              492  LOAD_ATTR                suffix

 L. 259       494  LOAD_CONST               False

 L. 258       496  LOAD_CONST               ('suffix', 'delete')
              498  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              500  STORE_FAST               'tmp_dst'

 L. 261       502  LOAD_FAST                'tmp_dst'
              504  LOAD_METHOD              close
              506  CALL_METHOD_0         0  ''
              508  POP_TOP          

 L. 262       510  LOAD_GLOBAL              Path
              512  LOAD_FAST                'tmp_dst'
              514  LOAD_ATTR                name
              516  CALL_FUNCTION_1       1  ''
              518  STORE_FAST               'tmp_dst'
            520_0  COME_FROM           482  '482'

 L. 264       520  LOAD_GLOBAL              str
              522  LOAD_FAST                'tmp_dst'
              524  LOAD_CONST               None
              526  COMPARE_OP               is
          528_530  POP_JUMP_IF_FALSE   536  'to 536'
              532  LOAD_FAST                'dst'
              534  JUMP_FORWARD        538  'to 538'
            536_0  COME_FROM           528  '528'
              536  LOAD_FAST                'tmp_dst'
            538_0  COME_FROM           534  '534'
              538  CALL_FUNCTION_1       1  ''
              540  STORE_FAST               'dst_file'

 L. 265       542  LOAD_GLOBAL              subprocess
              544  LOAD_ATTR                run
              546  LOAD_STR                 "diff '{src}' '{dst_file}' >/dev/null"
              548  LOAD_ATTR                format
              550  BUILD_TUPLE_0         0 

 L. 266       552  LOAD_GLOBAL              locals
              554  CALL_FUNCTION_0       0  ''

 L. 265       556  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'

 L. 266       558  LOAD_CONST               True

 L. 265       560  LOAD_CONST               ('shell',)
              562  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              564  LOAD_ATTR                returncode

 L. 267       566  LOAD_CONST               0

 L. 265       568  COMPARE_OP               !=
              570  STORE_FAST               'diffs'

 L. 268       572  LOAD_GLOBAL              pout
              574  LOAD_STR                 'Differences: {}'
              576  LOAD_METHOD              format
              578  LOAD_FAST                'diffs'
              580  CALL_METHOD_1         1  ''
              582  CALL_FUNCTION_1       1  ''
              584  POP_TOP          

 L. 269       586  LOAD_FAST                'diffs'
          588_590  POP_JUMP_IF_FALSE   732  'to 732'

 L. 270       592  LOAD_FAST                'self'
              594  LOAD_ATTR                args
              596  LOAD_ATTR                merge_cmd
              598  STORE_FAST               'merge_cmd'

 L. 271       600  LOAD_FAST                'merge_cmd'
              602  LOAD_CONST               None
              604  COMPARE_OP               is
          606_608  POP_JUMP_IF_FALSE   668  'to 668'

 L. 272       610  LOAD_GLOBAL              MERGE_TOOLS
              612  LOAD_METHOD              items
              614  CALL_METHOD_0         0  ''
              616  GET_ITER         
            618_0  COME_FROM           634  '634'
              618  FOR_ITER            668  'to 668'
              620  UNPACK_SEQUENCE_2     2 
              622  STORE_FAST               'cmd'
              624  STORE_FAST               'opts'

 L. 273       626  LOAD_GLOBAL              shutil
              628  LOAD_METHOD              which
              630  LOAD_FAST                'cmd'
              632  CALL_METHOD_1         1  ''
          634_636  POP_JUMP_IF_FALSE   618  'to 618'

 L. 274       638  LOAD_STR                 ' '
              640  LOAD_METHOD              join
              642  LOAD_FAST                'cmd'
              644  LOAD_FAST                'opts'
          646_648  JUMP_IF_TRUE_OR_POP   652  'to 652'
              650  LOAD_STR                 ''
            652_0  COME_FROM           646  '646'
              652  BUILD_LIST_2          2 
              654  CALL_METHOD_1         1  ''
              656  STORE_FAST               'merge_cmd'

 L. 275       658  POP_TOP          
          660_662  BREAK_LOOP          668  'to 668'
          664_666  JUMP_BACK           618  'to 618'
            668_0  COME_FROM           606  '606'

 L. 276       668  LOAD_FAST                'merge_cmd'
              670  LOAD_CONST               None
              672  COMPARE_OP               is-not
          674_676  POP_JUMP_IF_FALSE   706  'to 706'

 L. 277       678  LOAD_GLOBAL              subprocess
              680  LOAD_ATTR                run
              682  LOAD_STR                 "{merge_cmd} '{src}' '{dst_file}'"
              684  LOAD_ATTR                format
              686  BUILD_TUPLE_0         0 

 L. 278       688  LOAD_GLOBAL              locals
              690  CALL_FUNCTION_0       0  ''

 L. 277       692  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'

 L. 279       694  LOAD_CONST               True

 L. 279       696  LOAD_CONST               True

 L. 277       698  LOAD_CONST               ('shell', 'check')
              700  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              702  POP_TOP          
              704  JUMP_FORWARD        732  'to 732'
            706_0  COME_FROM           674  '674'

 L. 281       706  LOAD_GLOBAL              perr
              708  LOAD_STR                 'Merge disabled, no merge command found. Install a merge tool such as: {tools}.\nOr use --merge-cmd to specify your own.'
              710  LOAD_ATTR                format

 L. 284       712  LOAD_STR                 ', '
              714  LOAD_METHOD              join
              716  LOAD_GLOBAL              MERGE_TOOLS
              718  LOAD_METHOD              keys
              720  CALL_METHOD_0         0  ''
              722  CALL_METHOD_1         1  ''

 L. 281       724  LOAD_CONST               ('tools',)
              726  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              728  CALL_FUNCTION_1       1  ''
              730  POP_TOP          
            732_0  COME_FROM           704  '704'
            732_1  COME_FROM           588  '588'

 L. 286       732  LOAD_FAST                'tmp_dst'
          734_736  POP_JUMP_IF_FALSE   764  'to 764'
              738  LOAD_FAST                'tmp_dst'
              740  LOAD_METHOD              stat
              742  CALL_METHOD_0         0  ''
              744  LOAD_ATTR                st_size
              746  LOAD_CONST               0
              748  COMPARE_OP               ==
          750_752  POP_JUMP_IF_FALSE   764  'to 764'

 L. 287       754  LOAD_FAST                'tmp_dst'
              756  LOAD_METHOD              unlink
              758  CALL_METHOD_0         0  ''
              760  POP_TOP          
              762  JUMP_BACK           272  'to 272'
            764_0  COME_FROM           750  '750'
            764_1  COME_FROM           734  '734'

 L. 288       764  LOAD_FAST                'tmp_dst'
          766_768  POP_JUMP_IF_FALSE   272  'to 272'

 L. 290       770  LOAD_FAST                'dst'
              772  LOAD_ATTR                parent
              774  LOAD_METHOD              exists
              776  CALL_METHOD_0         0  ''
          778_780  POP_JUMP_IF_TRUE    798  'to 798'

 L. 291       782  LOAD_FAST                'dst'
              784  LOAD_ATTR                parent
              786  LOAD_ATTR                mkdir
              788  LOAD_CONST               493
              790  LOAD_CONST               True
              792  LOAD_CONST               ('parents',)
              794  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              796  POP_TOP          
            798_0  COME_FROM           778  '778'

 L. 292       798  LOAD_GLOBAL              shutil
              800  LOAD_METHOD              move
              802  LOAD_GLOBAL              str
              804  LOAD_FAST                'tmp_dst'
              806  CALL_FUNCTION_1       1  ''
              808  LOAD_GLOBAL              str
              810  LOAD_FAST                'dst'
              812  CALL_FUNCTION_1       1  ''
              814  CALL_METHOD_2         2  ''
              816  POP_TOP          
          818_820  JUMP_BACK           272  'to 272'

 L. 294       822  LOAD_GLOBAL              HASH_FILE
              824  LOAD_METHOD              open
              826  LOAD_STR                 'w'
              828  CALL_METHOD_1         1  ''
              830  SETUP_WITH          880  'to 880'
              832  STORE_FAST               'hash_file'

 L. 295       834  LOAD_GLOBAL              sorted
              836  LOAD_FAST                'md5_hashes'
              838  LOAD_METHOD              keys
              840  CALL_METHOD_0         0  ''
              842  CALL_FUNCTION_1       1  ''
              844  GET_ITER         
              846  FOR_ITER            876  'to 876'
              848  STORE_FAST               'f'

 L. 296       850  LOAD_FAST                'hash_file'
              852  LOAD_METHOD              write
              854  LOAD_STR                 '{}:{}\n'
              856  LOAD_METHOD              format
              858  LOAD_FAST                'f'
              860  LOAD_FAST                'md5_hashes'
              862  LOAD_FAST                'f'
              864  BINARY_SUBSCR    
              866  CALL_METHOD_2         2  ''
              868  CALL_METHOD_1         1  ''
              870  POP_TOP          
          872_874  JUMP_BACK           846  'to 846'
              876  POP_BLOCK        
              878  BEGIN_FINALLY    
            880_0  COME_FROM_WITH      830  '830'
              880  WITH_CLEANUP_START
              882  WITH_CLEANUP_FINISH
              884  END_FINALLY      

Parse error at or near `CALL_FINALLY' instruction at offset 354


    class Nicfit(nicfit.Application):

        def __init__(self):
            super().__init__(version=version, gettext_domain='nicfit.py', pdb_opt=True)
            subparsers = self.arg_parser.add_subparsers(dest='command', required=False)
            nicfit.Command.loadCommandMap(subparsers=subparsers)

        def _main--- This code section failed: ---

 L. 308         0  LOAD_GLOBAL              ansi
                2  LOAD_METHOD              init
                4  CALL_METHOD_0         0  ''
                6  POP_TOP          

 L. 309         8  LOAD_STR                 'command_func'
               10  LOAD_FAST                'args'
               12  COMPARE_OP               not-in
               14  POP_JUMP_IF_TRUE     22  'to 22'
               16  LOAD_FAST                'args'
               18  LOAD_ATTR                command_func
               20  POP_JUMP_IF_TRUE     56  'to 56'
             22_0  COME_FROM            14  '14'

 L. 310        22  LOAD_GLOBAL              pout
               24  LOAD_GLOBAL              Fg
               26  LOAD_METHOD              red
               28  LOAD_STR                 '\\m/ {} \\m/'
               30  LOAD_METHOD              format

 L. 311        32  LOAD_GLOBAL              Style
               34  LOAD_METHOD              inverse
               36  LOAD_GLOBAL              _
               38  LOAD_STR                 'Welcome'
               40  CALL_FUNCTION_1       1  ''
               42  CALL_METHOD_1         1  ''

 L. 310        44  CALL_METHOD_1         1  ''
               46  CALL_METHOD_1         1  ''
               48  CALL_FUNCTION_1       1  ''
               50  POP_TOP          

 L. 312        52  LOAD_CONST               0
               54  RETURN_VALUE     
             56_0  COME_FROM            20  '20'

 L. 314        56  SETUP_FINALLY        70  'to 70'

 L. 315        58  LOAD_FAST                'args'
               60  LOAD_METHOD              command_func
               62  LOAD_FAST                'args'
               64  CALL_METHOD_1         1  ''
               66  POP_BLOCK        
               68  RETURN_VALUE     
             70_0  COME_FROM_FINALLY    56  '56'

 L. 316        70  DUP_TOP          
               72  LOAD_GLOBAL              nicfit
               74  LOAD_ATTR                CommandError
               76  COMPARE_OP               exception-match
               78  POP_JUMP_IF_FALSE   122  'to 122'
               80  POP_TOP          
               82  STORE_FAST               'err'
               84  POP_TOP          
               86  SETUP_FINALLY       110  'to 110'

 L. 317        88  LOAD_GLOBAL              perr
               90  LOAD_FAST                'err'
               92  CALL_FUNCTION_1       1  ''
               94  POP_TOP          

 L. 318        96  LOAD_FAST                'err'
               98  LOAD_ATTR                exit_status
              100  ROT_FOUR         
              102  POP_BLOCK        
              104  POP_EXCEPT       
              106  CALL_FINALLY        110  'to 110'
              108  RETURN_VALUE     
            110_0  COME_FROM           106  '106'
            110_1  COME_FROM_FINALLY    86  '86'
              110  LOAD_CONST               None
              112  STORE_FAST               'err'
              114  DELETE_FAST              'err'
              116  END_FINALLY      
              118  POP_EXCEPT       
              120  JUMP_FORWARD        124  'to 124'
            122_0  COME_FROM            78  '78'
              122  END_FINALLY      
            124_0  COME_FROM           120  '120'

Parse error at or near `POP_BLOCK' instruction at offset 102


    app = Nicfit()
    if __name__ == '__main__':
        app.run()