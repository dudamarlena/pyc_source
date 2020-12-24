# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\brython\list_modules.py
# Compiled at: 2020-02-20 09:12:18
# Size of source mod 2**32: 24982 bytes
"""Detect all Python scripts in HTML pages in current folder and subfolders.
Generate brython_modules.js, a bundle with all the modules and packages used
by an application.
Generate a Python package ready for installation and upload on PyPI.
"""
import os, shutil, html.parser, json, traceback, sys, time, io, tokenize, token
setup = 'from setuptools import setup, find_packages\n\nimport os\n\nif os.path.exists(\'README.rst\'):\n    with open(\'README.rst\', encoding=\'utf-8\') as fobj:\n        LONG_DESCRIPTION = fobj.read()\n\nsetup(\n    name=\'{app_name}\',\n    version=\'{version}\',\n\n    # The project\'s main homepage.\n    url=\'{url}\',\n\n    # Author details\n    author=\'{author}\',\n    author_email=\'{author_email}\',\n\n    # License\n    license=\'{license}\',\n\n    packages=[\'data\'],\n    py_modules=["{app_name}"],\n    package_data={{\'data\':[{files}]}}\n)\n'
app = 'import os\nimport shutil\nimport argparse\n\nparser = argparse.ArgumentParser()\nparser.add_argument(\'--install\',\n    help=\'Install {app_name} in an empty directory\',\n    action="store_true")\nargs = parser.parse_args()\n\nfiles = ({files})\n\nif args.install:\n    print(\'Installing {app_name} in an empty directory\')\n\n    src_path = os.path.join(os.path.dirname(__file__), \'data\')\n\n    if os.listdir(os.getcwd()):\n        print(\'{app_name} can only be installed in an empty folder\')\n        import sys\n        sys.exit()\n\n    for path in files:\n        dst = os.path.join(os.getcwd(), path)\n        head, tail = os.path.split(dst)\n        if not os.path.exists(head):\n            os.mkdir(head)\n        shutil.copyfile(os.path.join(src_path, path), dst)\n\n'

class FromImport:

    def __init__(self):
        self.source = ''
        self.type = 'from'
        self.level = 0
        self.expect = 'source'
        self.names = []

    def __str__(self):
        return '<import ' + str(self.names) + ' from ' + str(self.source) + '>'


class Import:

    def __init__(self):
        self.type = 'import'
        self.expect = 'module'
        self.modules = []

    def __str__(self):
        return '<import ' + str(self.modules) + '>'


class ImportsFinder:

    def __init__(self, *args, **kw):
        self.package = kw.pop('package') or ''

    def find(self, src):
        """Find imports in source code src. Uses the tokenize module instead
        of ast in previous Brython version, so that this script can be run
        with CPython versions older than the one implemented in Brython."""
        imports = set()
        importing = None
        f = io.BytesIO(src.encode('utf-8'))
        for tok_type, tok_string, *_ in tokenize.tokenize(f.readline):
            tok_type = token.tok_name[tok_type]
            if importing is None:
                if tok_type == 'NAME':
                    if tok_string in ('import', 'from'):
                        context = Import() if tok_string == 'import' else FromImport()
                        importing = True
                    else:
                        if tok_type == 'NEWLINE':
                            imports.add(context)
                            importing = None
            else:
                self.transition(context, tok_type, tok_string)
        else:
            if importing:
                imports.add(context)
            self.imports = set()
            for imp in imports:
                if isinstance(imp, Import):
                    for mod in imp.modules:
                        parts = mod.split('.')
                        while True:
                            if parts:
                                self.imports.add('.'.join(parts))
                                parts.pop()

            else:
                if isinstance(imp, FromImport):
                    source = imp.source
                    if imp.level > 0:
                        if imp.level == 1:
                            imp.source = self.package
                        else:
                            parts = self.package.split('.')
                            imp.source = '.'.join(parts[:1 - imp.level])
                        if source:
                            imp.source += '.' + source
                    parts = imp.source.split('.')
                    while True:
                        if parts:
                            self.imports.add('.'.join(parts))
                            parts.pop()

                self.imports.add(imp.source)
                for name in imp.names:
                    parts = name.split('.')
                    while True:
                        if parts:
                            self.imports.add(imp.source + '.' + '.'.join(parts))
                            parts.pop()

    def transition(self, context, token, value):
        if context.type == 'from':
            if token == 'NAME':
                if context.expect == 'source':
                    if value == 'import':
                        if context.level:
                            context.expect = 'names'
                        else:
                            context.source += value
                            context.expect = '.'
                    elif context.expect == '.' and value == 'import':
                        context.expect = 'names'
                    elif context.expect == 'names':
                        context.names.append(value)
                        context.expect = ','
                elif token == 'OP':
                    if value == ',' and context.expect == ',':
                        context.expect = 'names'
                    else:
                        if value == '.' and context.expect == '.':
                            context.source += '.'
                            context.expect = 'source'
                        else:
                            if value == '.' and context.expect == 'source':
                                context.level += 1
            else:
                pass
        if context.type == 'import':
            if token == 'NAME':
                if context.expect == 'module':
                    if context.modules and context.modules[(-1)].endswith('.'):
                        context.modules[(-1)] += value
                    else:
                        context.modules.append(value)
                    context.expect = '.'
            elif token == 'OP':
                if context.expect == '.':
                    if value == '.':
                        context.modules[(-1)] += '.'
                    context.expect = 'module'


class ModulesFinder:

    def __init__(self, directory=os.getcwd()):
        self.directory = directory
        self.modules = set()

    def get_imports(self, src, package=None):
        """Get all imports in source code src."""
        finder = ImportsFinder(package=package)
        finder.find(src)
        for module in finder.imports:
            if module in self.modules:
                pass
            else:
                found = False
                for module_dict in (stdlib, user_modules):
                    if module in module_dict:
                        found = True
                        self.modules.add(module)
                        if module_dict[module][0] == '.py':
                            is_package = len(module_dict[module]) == 4
                            if is_package:
                                package = module
                            else:
                                if '.' in module:
                                    package = module[:module.rfind('.')]
                                else:
                                    package = ''
                            module_dict[module][2] = list(self.get_imports(module_dict[module][1], package))
                else:
                    return finder.imports

    def norm_indent(self, script):
        """Scripts in Brython page may start with an indent, remove it before
        building the AST.
        """
        indent = None
        lines = []
        for line in script.split('\n'):
            if line.strip() and indent is None:
                indent = len(line) - len(line.lstrip())
                line = line[indent:]
            else:
                if indent is not None:
                    line = line[indent:]
            lines.append(line)
        else:
            return '\n'.join(lines)

    def inspect--- This code section failed: ---

 L. 252         0  LOAD_STR                 'Lib{0}site-packages{0}'
                2  LOAD_METHOD              format
                4  LOAD_GLOBAL              os
                6  LOAD_ATTR                sep
                8  CALL_METHOD_1         1  ''
               10  STORE_FAST               'site_packages'

 L. 253        12  LOAD_GLOBAL              set
               14  CALL_FUNCTION_0       0  ''
               16  STORE_FAST               'imports'

 L. 254        18  LOAD_GLOBAL              os
               20  LOAD_METHOD              walk
               22  LOAD_FAST                'self'
               24  LOAD_ATTR                directory
               26  CALL_METHOD_1         1  ''
               28  GET_ITER         
            30_32  FOR_ITER            554  'to 554'
               34  UNPACK_SEQUENCE_3     3 
               36  STORE_FAST               'dirname'
               38  STORE_FAST               'dirnames'
               40  STORE_FAST               'filenames'

 L. 255        42  LOAD_FAST                'dirnames'
               44  GET_ITER         
             46_0  COME_FROM            68  '68'
               46  FOR_ITER             86  'to 86'
               48  STORE_FAST               'name'

 L. 256        50  LOAD_FAST                'name'
               52  LOAD_METHOD              endswith
               54  LOAD_STR                 '__dist__'
               56  CALL_METHOD_1         1  ''
               58  POP_JUMP_IF_TRUE     70  'to 70'
               60  LOAD_FAST                'name'
               62  LOAD_METHOD              endswith
               64  LOAD_STR                 '__pycache__'
               66  CALL_METHOD_1         1  ''
               68  POP_JUMP_IF_FALSE    46  'to 46'
             70_0  COME_FROM            58  '58'

 L. 258        70  LOAD_FAST                'dirnames'
               72  LOAD_METHOD              remove
               74  LOAD_FAST                'name'
               76  CALL_METHOD_1         1  ''
               78  POP_TOP          

 L. 259        80  POP_TOP          
               82  BREAK_LOOP           86  'to 86'
               84  JUMP_BACK            46  'to 46'

 L. 260        86  LOAD_FAST                'filenames'
               88  GET_ITER         
             90_0  COME_FROM           350  '350'
            90_92  FOR_ITER            552  'to 552'
               94  STORE_FAST               'filename'

 L. 261        96  LOAD_GLOBAL              os
               98  LOAD_ATTR                path
              100  LOAD_METHOD              join
              102  LOAD_FAST                'dirname'
              104  LOAD_FAST                'filename'
              106  CALL_METHOD_2         2  ''
              108  STORE_FAST               'path'

 L. 262       110  LOAD_FAST                'path'
              112  LOAD_GLOBAL              __file__
              114  COMPARE_OP               ==
              116  POP_JUMP_IF_FALSE   120  'to 120'

 L. 263       118  JUMP_BACK            90  'to 90'
            120_0  COME_FROM           116  '116'

 L. 264       120  LOAD_GLOBAL              os
              122  LOAD_ATTR                path
              124  LOAD_METHOD              splitext
              126  LOAD_FAST                'filename'
              128  CALL_METHOD_1         1  ''
              130  LOAD_CONST               1
              132  BINARY_SUBSCR    
              134  STORE_FAST               'ext'

 L. 265       136  LOAD_FAST                'ext'
              138  LOAD_METHOD              lower
              140  CALL_METHOD_0         0  ''
              142  LOAD_STR                 '.html'
              144  COMPARE_OP               ==
          146_148  POP_JUMP_IF_FALSE   340  'to 340'

 L. 266       150  LOAD_GLOBAL              print
              152  LOAD_STR                 'script in html'
              154  LOAD_FAST                'filename'
              156  CALL_FUNCTION_2       2  ''
              158  POP_TOP          

 L. 268       160  LOAD_GLOBAL              CharsetDetector
              162  CALL_FUNCTION_0       0  ''
              164  STORE_FAST               'charset_detector'

 L. 269       166  LOAD_GLOBAL              open
              168  LOAD_FAST                'path'
              170  LOAD_STR                 'iso-8859-1'
              172  LOAD_CONST               ('encoding',)
              174  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              176  SETUP_WITH          198  'to 198'
              178  STORE_FAST               'fobj'

 L. 270       180  LOAD_FAST                'charset_detector'
              182  LOAD_METHOD              feed
              184  LOAD_FAST                'fobj'
              186  LOAD_METHOD              read
              188  CALL_METHOD_0         0  ''
              190  CALL_METHOD_1         1  ''
              192  POP_TOP          
              194  POP_BLOCK        
              196  BEGIN_FINALLY    
            198_0  COME_FROM_WITH      176  '176'
              198  WITH_CLEANUP_START
              200  WITH_CLEANUP_FINISH
              202  END_FINALLY      

 L. 273       204  LOAD_GLOBAL              BrythonScriptsExtractor
              206  LOAD_FAST                'dirname'
              208  CALL_FUNCTION_1       1  ''
              210  STORE_FAST               'parser'

 L. 274       212  LOAD_GLOBAL              open
              214  LOAD_FAST                'path'
              216  LOAD_FAST                'charset_detector'
              218  LOAD_ATTR                encoding
              220  LOAD_CONST               ('encoding',)
              222  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              224  SETUP_WITH          246  'to 246'
              226  STORE_FAST               'fobj'

 L. 275       228  LOAD_FAST                'parser'
              230  LOAD_METHOD              feed
              232  LOAD_FAST                'fobj'
              234  LOAD_METHOD              read
              236  CALL_METHOD_0         0  ''
              238  CALL_METHOD_1         1  ''
              240  POP_TOP          
              242  POP_BLOCK        
              244  BEGIN_FINALLY    
            246_0  COME_FROM_WITH      224  '224'
              246  WITH_CLEANUP_START
              248  WITH_CLEANUP_FINISH
              250  END_FINALLY      

 L. 276       252  LOAD_FAST                'parser'
              254  LOAD_ATTR                scripts
              256  GET_ITER         
              258  FOR_ITER            338  'to 338'
              260  STORE_FAST               'script'

 L. 277       262  LOAD_FAST                'self'
              264  LOAD_METHOD              norm_indent
              266  LOAD_FAST                'script'
              268  CALL_METHOD_1         1  ''
              270  STORE_FAST               'script'

 L. 278       272  SETUP_FINALLY       288  'to 288'

 L. 279       274  LOAD_FAST                'self'
              276  LOAD_METHOD              get_imports
              278  LOAD_FAST                'script'
              280  CALL_METHOD_1         1  ''
              282  POP_TOP          
              284  POP_BLOCK        
              286  JUMP_BACK           258  'to 258'
            288_0  COME_FROM_FINALLY   272  '272'

 L. 280       288  DUP_TOP          
              290  LOAD_GLOBAL              SyntaxError
              292  COMPARE_OP               exception-match
          294_296  POP_JUMP_IF_FALSE   332  'to 332'
              298  POP_TOP          
              300  POP_TOP          
              302  POP_TOP          

 L. 281       304  LOAD_GLOBAL              print
              306  LOAD_STR                 'syntax error'
              308  LOAD_FAST                'path'
              310  CALL_FUNCTION_2       2  ''
              312  POP_TOP          

 L. 282       314  LOAD_GLOBAL              traceback
              316  LOAD_ATTR                print_exc
              318  LOAD_GLOBAL              sys
              320  LOAD_ATTR                stderr
              322  LOAD_CONST               ('file',)
              324  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              326  POP_TOP          
              328  POP_EXCEPT       
              330  JUMP_BACK           258  'to 258'
            332_0  COME_FROM           294  '294'
              332  END_FINALLY      
          334_336  JUMP_BACK           258  'to 258'
              338  JUMP_BACK            90  'to 90'
            340_0  COME_FROM           146  '146'

 L. 283       340  LOAD_FAST                'ext'
              342  LOAD_METHOD              lower
              344  CALL_METHOD_0         0  ''
              346  LOAD_STR                 '.py'
              348  COMPARE_OP               ==
              350  POP_JUMP_IF_FALSE    90  'to 90'

 L. 285       352  LOAD_FAST                'filename'
              354  LOAD_STR                 'list_modules.py'
              356  COMPARE_OP               ==
          358_360  POP_JUMP_IF_FALSE   364  'to 364'

 L. 286       362  JUMP_BACK            90  'to 90'
            364_0  COME_FROM           358  '358'

 L. 287       364  LOAD_FAST                'dirname'
              366  LOAD_FAST                'self'
              368  LOAD_ATTR                directory
              370  COMPARE_OP               !=
          372_374  POP_JUMP_IF_FALSE   388  'to 388'
              376  LOAD_GLOBAL              is_package
              378  LOAD_FAST                'dirname'
              380  CALL_FUNCTION_1       1  ''
          382_384  POP_JUMP_IF_TRUE    388  'to 388'

 L. 288       386  JUMP_BACK            90  'to 90'
            388_0  COME_FROM           382  '382'
            388_1  COME_FROM           372  '372'

 L. 290       388  LOAD_FAST                'dirname'
              390  LOAD_GLOBAL              len
              392  LOAD_FAST                'self'
              394  LOAD_ATTR                directory
              396  CALL_FUNCTION_1       1  ''
              398  LOAD_CONST               1
              400  BINARY_ADD       
              402  LOAD_CONST               None
              404  BUILD_SLICE_2         2 
              406  BINARY_SUBSCR    
          408_410  JUMP_IF_TRUE_OR_POP   414  'to 414'
              412  LOAD_CONST               None
            414_0  COME_FROM           408  '408'
              414  STORE_FAST               'package'

 L. 291       416  LOAD_FAST                'package'
              418  LOAD_CONST               None
              420  COMPARE_OP               is-not
          422_424  POP_JUMP_IF_FALSE   454  'to 454'

 L. 292       426  LOAD_FAST                'package'
              428  LOAD_METHOD              startswith
              430  LOAD_FAST                'site_packages'
              432  CALL_METHOD_1         1  ''

 L. 291   434_436  POP_JUMP_IF_FALSE   454  'to 454'

 L. 293       438  LOAD_FAST                'package'
              440  LOAD_GLOBAL              len
              442  LOAD_STR                 'Lib/site-packages/'
              444  CALL_FUNCTION_1       1  ''
              446  LOAD_CONST               None
              448  BUILD_SLICE_2         2 
              450  BINARY_SUBSCR    
              452  STORE_FAST               'package'
            454_0  COME_FROM           434  '434'
            454_1  COME_FROM           422  '422'

 L. 294       454  LOAD_GLOBAL              open
              456  LOAD_FAST                'path'
              458  LOAD_STR                 'utf-8'
              460  LOAD_CONST               ('encoding',)
              462  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              464  SETUP_WITH          544  'to 544'
              466  STORE_FAST               'fobj'

 L. 295       468  SETUP_FINALLY       494  'to 494'

 L. 296       470  LOAD_FAST                'imports'
              472  LOAD_FAST                'self'
              474  LOAD_METHOD              get_imports
              476  LOAD_FAST                'fobj'
              478  LOAD_METHOD              read
              480  CALL_METHOD_0         0  ''
              482  LOAD_FAST                'package'
              484  CALL_METHOD_2         2  ''
              486  INPLACE_OR       
              488  STORE_FAST               'imports'
              490  POP_BLOCK        
              492  JUMP_FORWARD        540  'to 540'
            494_0  COME_FROM_FINALLY   468  '468'

 L. 297       494  DUP_TOP          
              496  LOAD_GLOBAL              SyntaxError
              498  COMPARE_OP               exception-match
          500_502  POP_JUMP_IF_FALSE   538  'to 538'
              504  POP_TOP          
              506  POP_TOP          
              508  POP_TOP          

 L. 298       510  LOAD_GLOBAL              print
              512  LOAD_STR                 'syntax error'
              514  LOAD_FAST                'path'
              516  CALL_FUNCTION_2       2  ''
              518  POP_TOP          

 L. 299       520  LOAD_GLOBAL              traceback
              522  LOAD_ATTR                print_exc
              524  LOAD_GLOBAL              sys
              526  LOAD_ATTR                stderr
              528  LOAD_CONST               ('file',)
              530  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              532  POP_TOP          
              534  POP_EXCEPT       
              536  JUMP_FORWARD        540  'to 540'
            538_0  COME_FROM           500  '500'
              538  END_FINALLY      
            540_0  COME_FROM           536  '536'
            540_1  COME_FROM           492  '492'
              540  POP_BLOCK        
              542  BEGIN_FINALLY    
            544_0  COME_FROM_WITH      464  '464'
              544  WITH_CLEANUP_START
              546  WITH_CLEANUP_FINISH
              548  END_FINALLY      
              550  JUMP_BACK            90  'to 90'
              552  JUMP_BACK            30  'to 30'

Parse error at or near `JUMP_BACK' instruction at offset 550

    def make_brython_modules(self):
        """Build brython_modules.js from the list of modules needed by the
        application.
        """
        vfs = {'$timestamp': int(1000 * time.time())}
        for module in self.modules:
            dico = stdlib if module in stdlib else user_modules
            vfs[module] = dico[module]
            elts = module.split('.')
            for i in range(1, len(elts)):
                pkg = '.'.join(elts[:i])
                if pkg not in vfs:
                    vfs[pkg] = dico[pkg]
            else:
                path = os.path.join(stdlib_dir, 'brython_modules.js')
                with open(path, 'w', encoding='utf-8') as (out):
                    out.write('__BRYTHON__.VFS_timestamp = {}\n'.format(int(1000 * time.time())))
                    out.write('__BRYTHON__.use_VFS = true\nvar scripts = ')
                    json.dump(vfs, out)
                    out.write('\n__BRYTHON__.update_VFS(scripts)')

    def _dest(self, base_dir, dirname, filename):
        """Build the destination path for a file."""
        elts = dirname[len(os.getcwd()) + 1:].split(os.sep)
        dest_dir = base_dir
        for elt in elts:
            dest_dir = os.path.join(dest_dir, elt)
            if not os.path.exists(dest_dir):
                os.mkdir(dest_dir)
            return os.path.join(dest_dir, filename)

    def make_setup(self):
        """Make the setup script (setup.py) and the entry point script
        for the application."""
        temp_dir = '__dist__'
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
        else:
            os.mkdir(temp_dir)
            data_dir = os.path.join(temp_dir, 'data')
            os.mkdir(data_dir)
            with open(os.path.join(data_dir, '__init__.py'), 'w') as (out):
                out.write('')
            if os.path.exists('brython_setup.json'):
                with open('brython_setup.json', encoding='utf-8') as (fobj):
                    info = json.load(fobj)
            else:
                while True:
                    app_name = input('Application name: ')
                    if app_name:
                        break

            while True:
                version = input('Version: ')
                if version:
                    break

            author = input('Author: ')
            author_email = input('Author email: ')
            license = input('License: ')
            url = input('Project url: ')
            info = {'app_name':app_name, 
             'version':version, 
             'author':author, 
             'author_email':author_email, 
             'license':license, 
             'url':url}
            with open('brython_setup.json', 'w', encoding='utf-8') as (out):
                json.dump(info, out, indent=4)
        files = []
        for dirname, dirnames, filenames in os.walk(self.directory):
            if dirname == '__dist__':
                pass
            else:
                if '__dist__' in dirnames:
                    dirnames.remove('__dist__')
                for filename in filenames:
                    path = os.path.join(dirname, filename)
                    parts = path[len(os.getcwd()) + 1:].split(os.sep)
                    files.append('os.path.join(' + ', '.join((repr(part) for part in parts)) + ')')
                    if os.path.splitext(filename)[1] == '.html':
                        charset_detector = CharsetDetector()
                        with open(path, encoding='iso-8859-1') as (fobj):
                            charset_detector.feed(fobj.read())
                        encoding = charset_detector.encoding
                        parser = VFSReplacementParser(dirname)
                        with open(path, encoding=encoding) as (fobj):
                            parser.feed(fobj.read())
                        if not parser.has_vfs:
                            dest = self._dest(data_dir, dirname, filename)
                            shutil.copyfile(path, dest)
                        else:
                            with open(path, encoding=encoding) as (fobj):
                                lines = fobj.readlines()
                                start_line, start_pos = parser.start
                                end_line, end_pos = parser.end
                                res = ''.join(lines[:start_line - 1])
                                for num in range(start_line - 1, end_line):
                                    res += lines[num].replace('brython_stdlib.js', 'brython_modules.js')
                                else:
                                    res += ''.join(lines[end_line:])

                            dest = self._dest(data_dir, dirname, filename)
                            with open(dest, 'w', encoding=encoding) as (out):
                                out.write(res)
                    else:
                        dest = self._dest(data_dir, dirname, filename)
                        shutil.copyfile(path, dest)
                else:
                    info['files'] = ',\n'.join(files)
                    path = os.path.join(temp_dir, 'setup.py')
                    with open(path, 'w', encoding='utf-8') as (out):
                        out.write((setup.format)(**info))
                    path = os.path.join(temp_dir, '{}.py'.format(info['app_name']))
                    with open(path, 'w', encoding='utf-8') as (out):
                        out.write((app.format)(**info))


user_modules = {}
print('searching brython_stdlib.js...')
stdlib = {}
stdlib_dir = None
for dirname, dirnames, filenames in os.walk(os.getcwd()):
    for filename in filenames:
        if filename == 'brython_stdlib.js':
            stdlib_dir = dirname
            path = os.path.join(dirname, filename)
            with open(path, encoding='utf-8') as (fobj):
                modules = fobj.read()
                modules = modules[modules.find('{'):modules.find('__BRYTHON__.update_VFS(')]
                stdlib = json.loads(modules)

if stdlib_dir is None:
    raise FileNotFoundError('Could not find brython_stdlib.js in this directory or below')
else:
    sp_dir = os.path.join(stdlib_dir, 'Lib', 'site-packages')
    if os.path.exists(sp_dir):
        print('search in site-packages...')
        mf = ModulesFinder()
        for dirpath, dirnames, filenames in os.walk(sp_dir):
            if dirpath.endswith('__pycache__'):
                pass
            else:
                package = dirpath[len(sp_dir) + 1:]
            for filename in filenames:
                if not filename.endswith('.py'):
                    pass
                else:
                    fullpath = os.path.join(dirpath, filename)
                    is_package = False
                    if not package:
                        module = os.path.splitext(filename)[0]
                    else:
                        elts = package.split(os.sep)
                        is_package = filename == '__init__.py'
                        if not is_package:
                            elts.append(os.path.splitext(filename)[0])
                        module = '.'.join(elts)
                    with open(fullpath, encoding='utf-8') as (f):
                        src = f.read()
                    stdlib[module] = ['.py', src, None]
                    if is_package:
                        stdlib[module].append(1)

    packages = {
     os.getcwd(), os.getcwd() + '/Lib/site-packages'}

    def is_package(folder):
        """Test if folder is a package, ie has __init__.py and all the folders
    above until os.getcwd() also have __init__.py.
    Use set "packages" to cache results.
    """
        if folder in packages:
            return True
        else:
            current = folder
        while True:
            if not os.path.exists(os.path.join(current, '__init__.py')):
                return False
            current = os.path.dirname(current)
            if current in packages:
                packages.add(folder)
                return True


    print('finding packages...')
    for dirname, dirnames, filenames in os.walk(os.getcwd()):
        for filename in filenames:
            name, ext = os.path.splitext(filename)
            if ext == '.py':
                if filename == 'list_modules.py':
                    pass
                elif dirname == os.getcwd():
                    path = os.path.join(dirname, filename)
                    with open(path, encoding='utf-8') as (fobj):
                        src = fobj.read()
                    mf = ModulesFinder(dirname)
                    imports = sorted(list(mf.get_imports(src)))
                    user_modules[name] = [ext, src, imports]
            elif is_package(dirname):
                path = os.path.join(dirname, filename)
                package = dirname[len(os.getcwd()) + 1:].replace(os.sep, '.')
                if package.startswith('Lib.site-packages.'):
                    package = package[len('Lib.site-packages.'):]
                elif filename == '__init__.py':
                    module_name = package
                else:
                    module_name = '{}.{}'.format(package, name)
                with open(path, encoding='utf-8') as (fobj):
                    src = fobj.read()
                user_modules[module_name] = [
                 ext, src, None]
                if module_name == package:
                    user_modules[module_name].append(1)
        else:

            class CharsetDetector(html.parser.HTMLParser):
                __doc__ = 'Used to detect <meta charset="..."> in HTML page.'

                def __init__(self, *args, **kw):
                    kw.setdefault('convert_charrefs', True)
                    try:
                        (html.parser.HTMLParser.__init__)(self, *args, **kw)
                    except TypeError:
                        del kw['convert_charrefs']
                        (html.parser.HTMLParser.__init__)(self, *args, **kw)
                    else:
                        self.encoding = 'iso-8859-1'

                def handle_starttag(self, tag, attrs):
                    if tag.lower() == 'meta':
                        for key, value in attrs:
                            if key == 'charset':
                                self.encoding = value


            class BrythonScriptsExtractor(html.parser.HTMLParser):
                __doc__ = 'Used to extract all Brython scripts in HTML pages.'

                def __init__(self, dirname, **kw):
                    kw.setdefault('convert_charrefs', True)
                    try:
                        (html.parser.HTMLParser.__init__)(self, **kw)
                    except TypeError:
                        del kw['convert_charrefs']
                        (html.parser.HTMLParser.__init__)(self, **kw)
                    else:
                        self.dirname = dirname
                        self.scripts = []
                        self.py_tags = []
                        self.tag_stack = []

                def handle_starttag(self, tag, attrs):
                    if tag.lower() == 'script':
                        _type = 'js_script'
                        src = None
                        for key, value in attrs:
                            if key == 'type' and value in ('text/python', 'text/python3'):
                                _type = 'py_script'
                        else:
                            if key == 'src':
                                src = value
                            if _type == 'py_script':
                                if src:
                                    _type = 'py_script_with_src'
                                    path = os.path.join(self.dirname, src)
                                    with open(path, encoding='utf-8') as (fobj):
                                        self.scripts.append(fobj.read())
                            self.tag_stack.append(_type)

                def handle_endtag(self, tag):
                    if tag.lower() == 'script':
                        self.tag_stack.pop()

                def handle_data(self, data):
                    """Data is printed unchanged"""
                    if data.strip():
                        if self.tag_stack:
                            if self.tag_stack[(-1)].lower() == 'py_script':
                                self.scripts.append(data)


            class VFSReplacementParser(html.parser.HTMLParser):
                __doc__ = 'Used to replace brython_stdlib.js by brython_modules.js in HTML\n    pages.'

                def __init__(self, path, **kw):
                    kw.setdefault('convert_charrefs', True)
                    try:
                        (html.parser.HTMLParser.__init__)(self, **kw)
                    except TypeError:
                        del kw['convert_charrefs']
                        (html.parser.HTMLParser.__init__)(self, **kw)
                    else:
                        self.vfs = False
                        self.has_vfs = False

                def handle_starttag(self, tag, attrs):
                    if tag.lower() == 'script':
                        _type = 'js_script'
                        src = None
                        for key, value in attrs:
                            if key == 'src':
                                elts = value.split('/')
                                if elts and elts[(-1)] == 'brython_stdlib.js':
                                    self.vfs = True
                                    self.has_vfs = True
                                    self.attrs = attrs
                                    self.start = self.getpos()
                                    return None

                    self.vfs = False

                def handle_endtag(self, tag):
                    if tag.lower() == 'script':
                        if self.vfs:
                            self.end = self.getpos()


            if __name__ == '__main__':
                finder = ModulesFinder()
                finder.inspect()
                print(sorted(list(finder.modules)))