# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/src/fmriprep/wrapper/build/lib/python3.7/site.py
# Compiled at: 2020-05-05 12:41:45
# Size of source mod 2**32: 28803 bytes
"""Append module search paths for third-party packages to sys.path.

****************************************************************
* This module is automatically imported during initialization. *
****************************************************************

In earlier versions of Python (up to 1.5a3), scripts or modules that
needed to use site-specific modules would place ``import site''
somewhere near the top of their code.  Because of the automatic
import, this is no longer necessary (but code that does it still
works).

This will append site-specific paths to the module search path.  On
Unix, it starts with sys.prefix and sys.exec_prefix (if different) and
appends lib/python<version>/site-packages as well as lib/site-python.
It also supports the Debian convention of
lib/python<version>/dist-packages.  On other platforms (mainly Mac and
Windows), it uses just sys.prefix (and sys.exec_prefix, if different,
but this is unlikely).  The resulting directories, if they exist, are
appended to sys.path, and also inspected for path configuration files.

FOR DEBIAN, this sys.path is augmented with directories in /usr/local.
Local addons go into /usr/local/lib/python<version>/site-packages
(resp. /usr/local/lib/site-python), Debian addons install into
/usr/{lib,share}/python<version>/dist-packages.

A path configuration file is a file whose name has the form
<package>.pth; its contents are additional directories (one per line)
to be added to sys.path.  Non-existing directories (or
non-directories) are never added to sys.path; no directory is added to
sys.path more than once.  Blank lines and lines beginning with
'#' are skipped. Lines starting with 'import' are executed.

For example, suppose sys.prefix and sys.exec_prefix are set to
/usr/local and there is a directory /usr/local/lib/python2.X/site-packages
with three subdirectories, foo, bar and spam, and two path
configuration files, foo.pth and bar.pth.  Assume foo.pth contains the
following:

  # foo package configuration
  foo
  bar
  bletch

and bar.pth contains:

  # bar package configuration
  bar

Then the following directories are added to sys.path, in this order:

  /usr/local/lib/python2.X/site-packages/bar
  /usr/local/lib/python2.X/site-packages/foo

Note that bletch is omitted because it doesn't exist; bar precedes foo
because bar.pth comes alphabetically before foo.pth; and spam is
omitted because it is not mentioned in either path configuration file.

After these path manipulations, an attempt is made to import a module
named sitecustomize, which can perform arbitrary additional
site-specific customizations.  If this import fails with an
ImportError exception, it is silently ignored.

"""
import os, sys
try:
    import __builtin__ as builtins
except ImportError:
    import builtins

try:
    set
except NameError:
    from sets import Set as set

PREFIXES = [
 sys.prefix, sys.exec_prefix]
ENABLE_USER_SITE = None
USER_SITE = None
USER_BASE = None
_is_64bit = (getattr(sys, 'maxsize', None) or getattr(sys, 'maxint')) > 4294967296
_is_pypy = hasattr(sys, 'pypy_version_info')

def makepath(*paths):
    dir = (os.path.join)(*paths)
    dir = os.path.abspath(dir)
    return (dir, os.path.normcase(dir))


def abs__file__():
    """Set all module' __file__ attribute to an absolute path"""
    for m in sys.modules.values():
        f = getattr(m, '__file__', None)
        if f is None:
            continue
        m.__file__ = os.path.abspath(f)


def removeduppaths():
    """ Remove duplicate entries from sys.path along with making them
    absolute"""
    L = []
    known_paths = set()
    for dir in sys.path:
        dir, dircase = makepath(dir)
        if dircase not in known_paths:
            L.append(dir)
            known_paths.add(dircase)

    sys.path[:] = L
    return known_paths


def addbuilddir():
    """Append ./build/lib.<platform> in case we're running in the build dir
    (especially for Guido :-)"""
    from distutils.util import get_platform
    s = ('build/lib.{}-{}.{}'.format)(get_platform(), *sys.version_info)
    if hasattr(sys, 'gettotalrefcount'):
        s += '-pydebug'
    s = os.path.join(os.path.dirname(sys.path[(-1)]), s)
    sys.path.append(s)


def _init_pathinfo():
    """Return a set containing all existing directory entries from sys.path"""
    d = set()
    for dir in sys.path:
        try:
            if os.path.isdir(dir):
                dir, dircase = makepath(dir)
                d.add(dircase)
        except TypeError:
            continue

    return d


def addpackage(sitedir, name, known_paths):
    """Add a new path to known_paths by combining sitedir and 'name' or execute
    sitedir if it starts with 'import'"""
    if known_paths is None:
        _init_pathinfo()
        reset = 1
    else:
        reset = 0
    fullname = os.path.join(sitedir, name)
    try:
        f = open(fullname, 'r')
    except IOError:
        return
    else:
        try:
            for line in f:
                if line.startswith('#'):
                    continue
                if line.startswith('import'):
                    exec(line)
                    continue
                line = line.rstrip()
                dir, dircase = makepath(sitedir, line)
                if dircase not in known_paths and os.path.exists(dir):
                    sys.path.append(dir)
                    known_paths.add(dircase)

        finally:
            f.close()

        if reset:
            known_paths = None
        return known_paths


def addsitedir(sitedir, known_paths=None):
    """Add 'sitedir' argument to sys.path if missing and handle .pth files in
    'sitedir'"""
    if known_paths is None:
        known_paths = _init_pathinfo()
        reset = 1
    else:
        reset = 0
    sitedir, sitedircase = makepath(sitedir)
    if sitedircase not in known_paths:
        sys.path.append(sitedir)
    try:
        names = os.listdir(sitedir)
    except os.error:
        return
    else:
        names.sort()
        for name in names:
            if name.endswith(os.extsep + 'pth'):
                addpackage(sitedir, name, known_paths)

        if reset:
            known_paths = None
        return known_paths


def addsitepackages--- This code section failed: ---

 L. 210         0  LOAD_GLOBAL              os
                2  LOAD_ATTR                path
                4  LOAD_METHOD              join
                6  LOAD_FAST                'sys_prefix'
                8  LOAD_STR                 'local'
               10  CALL_METHOD_2         2  '2 positional arguments'
               12  LOAD_FAST                'sys_prefix'
               14  BUILD_LIST_2          2 
               16  STORE_FAST               'prefixes'

 L. 211        18  LOAD_FAST                'exec_prefix'
               20  LOAD_FAST                'sys_prefix'
               22  COMPARE_OP               !=
               24  POP_JUMP_IF_FALSE    46  'to 46'

 L. 212        26  LOAD_FAST                'prefixes'
               28  LOAD_METHOD              append
               30  LOAD_GLOBAL              os
               32  LOAD_ATTR                path
               34  LOAD_METHOD              join
               36  LOAD_FAST                'exec_prefix'
               38  LOAD_STR                 'local'
               40  CALL_METHOD_2         2  '2 positional arguments'
               42  CALL_METHOD_1         1  '1 positional argument'
               44  POP_TOP          
             46_0  COME_FROM            24  '24'

 L. 214     46_48  SETUP_LOOP          748  'to 748'
               50  LOAD_FAST                'prefixes'
               52  GET_ITER         
             54_0  COME_FROM            62  '62'
            54_56  FOR_ITER            746  'to 746'
               58  STORE_FAST               'prefix'

 L. 215        60  LOAD_FAST                'prefix'
               62  POP_JUMP_IF_FALSE    54  'to 54'

 L. 216        64  LOAD_GLOBAL              sys
               66  LOAD_ATTR                platform
               68  LOAD_CONST               ('os2emx', 'riscos')
               70  COMPARE_OP               in
               72  POP_JUMP_IF_FALSE    96  'to 96'

 L. 217        74  LOAD_GLOBAL              os
               76  LOAD_ATTR                path
               78  LOAD_METHOD              join
               80  LOAD_FAST                'prefix'
               82  LOAD_STR                 'Lib'
               84  LOAD_STR                 'site-packages'
               86  CALL_METHOD_3         3  '3 positional arguments'
               88  BUILD_LIST_1          1 
               90  STORE_FAST               'sitedirs'
            92_94  JUMP_FORWARD        620  'to 620'
             96_0  COME_FROM            72  '72'

 L. 218        96  LOAD_GLOBAL              _is_pypy
               98  POP_JUMP_IF_FALSE   120  'to 120'

 L. 219       100  LOAD_GLOBAL              os
              102  LOAD_ATTR                path
              104  LOAD_METHOD              join
              106  LOAD_FAST                'prefix'
              108  LOAD_STR                 'site-packages'
              110  CALL_METHOD_2         2  '2 positional arguments'
              112  BUILD_LIST_1          1 
              114  STORE_FAST               'sitedirs'
          116_118  JUMP_FORWARD        620  'to 620'
            120_0  COME_FROM            98  '98'

 L. 220       120  LOAD_GLOBAL              sys
              122  LOAD_ATTR                platform
              124  LOAD_STR                 'darwin'
              126  COMPARE_OP               ==
              128  POP_JUMP_IF_FALSE   224  'to 224'
              130  LOAD_FAST                'prefix'
              132  LOAD_FAST                'sys_prefix'
              134  COMPARE_OP               ==
              136  POP_JUMP_IF_FALSE   224  'to 224'

 L. 222       138  LOAD_FAST                'prefix'
              140  LOAD_METHOD              startswith
              142  LOAD_STR                 '/System/Library/Frameworks/'
              144  CALL_METHOD_1         1  '1 positional argument'
              146  POP_JUMP_IF_FALSE   192  'to 192'

 L. 225       148  LOAD_GLOBAL              os
              150  LOAD_ATTR                path
              152  LOAD_METHOD              join
              154  LOAD_STR                 '/Library/Python'
              156  LOAD_STR                 '{}.{}'
              158  LOAD_ATTR                format
              160  LOAD_GLOBAL              sys
              162  LOAD_ATTR                version_info
              164  CALL_FUNCTION_EX      0  'positional arguments only'
              166  LOAD_STR                 'site-packages'
              168  CALL_METHOD_3         3  '3 positional arguments'

 L. 226       170  LOAD_GLOBAL              os
              172  LOAD_ATTR                path
              174  LOAD_METHOD              join
              176  LOAD_FAST                'prefix'
              178  LOAD_STR                 'Extras'
              180  LOAD_STR                 'lib'
              182  LOAD_STR                 'python'
              184  CALL_METHOD_4         4  '4 positional arguments'
              186  BUILD_LIST_2          2 
              188  STORE_FAST               'sitedirs'
              190  JUMP_FORWARD        620  'to 620'
            192_0  COME_FROM           146  '146'

 L. 230       192  LOAD_GLOBAL              os
              194  LOAD_ATTR                path
              196  LOAD_METHOD              join
              198  LOAD_FAST                'prefix'
              200  LOAD_STR                 'lib'
              202  LOAD_STR                 'python{}.{}'
              204  LOAD_ATTR                format
              206  LOAD_GLOBAL              sys
              208  LOAD_ATTR                version_info
              210  CALL_FUNCTION_EX      0  'positional arguments only'
              212  LOAD_STR                 'site-packages'
              214  CALL_METHOD_4         4  '4 positional arguments'
              216  BUILD_LIST_1          1 
              218  STORE_FAST               'sitedirs'
          220_222  JUMP_FORWARD        620  'to 620'
            224_0  COME_FROM           136  '136'
            224_1  COME_FROM           128  '128'

 L. 232       224  LOAD_GLOBAL              os
              226  LOAD_ATTR                sep
              228  LOAD_STR                 '/'
              230  COMPARE_OP               ==
          232_234  POP_JUMP_IF_FALSE   600  'to 600'

 L. 234       236  LOAD_GLOBAL              os
              238  LOAD_ATTR                path
              240  LOAD_METHOD              join
              242  LOAD_FAST                'prefix'
              244  LOAD_STR                 'lib'
              246  LOAD_STR                 'python{}.{}'
              248  LOAD_ATTR                format
              250  LOAD_GLOBAL              sys
              252  LOAD_ATTR                version_info
              254  CALL_FUNCTION_EX      0  'positional arguments only'
              256  LOAD_STR                 'site-packages'
              258  CALL_METHOD_4         4  '4 positional arguments'

 L. 235       260  LOAD_GLOBAL              os
              262  LOAD_ATTR                path
              264  LOAD_METHOD              join
              266  LOAD_FAST                'prefix'
              268  LOAD_STR                 'lib'
              270  LOAD_STR                 'site-python'
              272  CALL_METHOD_3         3  '3 positional arguments'

 L. 236       274  LOAD_GLOBAL              os
              276  LOAD_ATTR                path
              278  LOAD_METHOD              join
              280  LOAD_FAST                'prefix'
              282  LOAD_STR                 'python{}.{}'
              284  LOAD_ATTR                format
              286  LOAD_GLOBAL              sys
              288  LOAD_ATTR                version_info
              290  CALL_FUNCTION_EX      0  'positional arguments only'
              292  LOAD_STR                 'lib-dynload'
              294  CALL_METHOD_3         3  '3 positional arguments'
              296  BUILD_LIST_3          3 
              298  STORE_FAST               'sitedirs'

 L. 238       300  LOAD_GLOBAL              os
              302  LOAD_ATTR                path
              304  LOAD_METHOD              join
              306  LOAD_FAST                'prefix'
              308  LOAD_STR                 'lib64'
              310  LOAD_STR                 'python{}.{}'
              312  LOAD_ATTR                format
              314  LOAD_GLOBAL              sys
              316  LOAD_ATTR                version_info
              318  CALL_FUNCTION_EX      0  'positional arguments only'
              320  LOAD_STR                 'site-packages'
              322  CALL_METHOD_4         4  '4 positional arguments'
              324  STORE_FAST               'lib64_dir'

 L. 239       326  LOAD_GLOBAL              os
              328  LOAD_ATTR                path
              330  LOAD_METHOD              exists
              332  LOAD_FAST                'lib64_dir'
              334  CALL_METHOD_1         1  '1 positional argument'
          336_338  POP_JUMP_IF_FALSE   398  'to 398'
              340  LOAD_GLOBAL              os
              342  LOAD_ATTR                path
              344  LOAD_METHOD              realpath
              346  LOAD_FAST                'lib64_dir'
              348  CALL_METHOD_1         1  '1 positional argument'

 L. 240       350  LOAD_LISTCOMP            '<code_object <listcomp>>'
              352  LOAD_STR                 'addsitepackages.<locals>.<listcomp>'
              354  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              356  LOAD_FAST                'sitedirs'
              358  GET_ITER         
              360  CALL_FUNCTION_1       1  '1 positional argument'
              362  COMPARE_OP               not-in
          364_366  POP_JUMP_IF_FALSE   398  'to 398'

 L. 242       368  LOAD_GLOBAL              _is_64bit
          370_372  POP_JUMP_IF_FALSE   388  'to 388'

 L. 243       374  LOAD_FAST                'sitedirs'
              376  LOAD_METHOD              insert
              378  LOAD_CONST               0
              380  LOAD_FAST                'lib64_dir'
              382  CALL_METHOD_2         2  '2 positional arguments'
              384  POP_TOP          
              386  JUMP_FORWARD        398  'to 398'
            388_0  COME_FROM           370  '370'

 L. 245       388  LOAD_FAST                'sitedirs'
              390  LOAD_METHOD              append
              392  LOAD_FAST                'lib64_dir'
              394  CALL_METHOD_1         1  '1 positional argument'
              396  POP_TOP          
            398_0  COME_FROM           386  '386'
            398_1  COME_FROM           364  '364'
            398_2  COME_FROM           336  '336'

 L. 246       398  SETUP_EXCEPT        436  'to 436'

 L. 248       400  LOAD_GLOBAL              sys
              402  LOAD_ATTR                getobjects
              404  POP_TOP          

 L. 249       406  LOAD_FAST                'sitedirs'
              408  LOAD_METHOD              insert
              410  LOAD_CONST               0
              412  LOAD_GLOBAL              os
              414  LOAD_ATTR                path
              416  LOAD_METHOD              join
              418  LOAD_FAST                'sitedirs'
              420  LOAD_CONST               0
              422  BINARY_SUBSCR    
              424  LOAD_STR                 'debug'
              426  CALL_METHOD_2         2  '2 positional arguments'
              428  CALL_METHOD_2         2  '2 positional arguments'
              430  POP_TOP          
              432  POP_BLOCK        
              434  JUMP_FORWARD        458  'to 458'
            436_0  COME_FROM_EXCEPT    398  '398'

 L. 250       436  DUP_TOP          
              438  LOAD_GLOBAL              AttributeError
              440  COMPARE_OP               exception-match
          442_444  POP_JUMP_IF_FALSE   456  'to 456'
              446  POP_TOP          
              448  POP_TOP          
              450  POP_TOP          

 L. 251       452  POP_EXCEPT       
              454  JUMP_FORWARD        458  'to 458'
            456_0  COME_FROM           442  '442'
              456  END_FINALLY      
            458_0  COME_FROM           454  '454'
            458_1  COME_FROM           434  '434'

 L. 253       458  LOAD_FAST                'sitedirs'
              460  LOAD_METHOD              append

 L. 254       462  LOAD_GLOBAL              os
              464  LOAD_ATTR                path
              466  LOAD_METHOD              join
              468  LOAD_FAST                'prefix'
              470  LOAD_STR                 'local/lib'
              472  LOAD_STR                 'python{}.{}'
              474  LOAD_ATTR                format
              476  LOAD_GLOBAL              sys
              478  LOAD_ATTR                version_info
              480  CALL_FUNCTION_EX      0  'positional arguments only'
              482  LOAD_STR                 'dist-packages'
              484  CALL_METHOD_4         4  '4 positional arguments'
              486  CALL_METHOD_1         1  '1 positional argument'
              488  POP_TOP          

 L. 256       490  LOAD_GLOBAL              sys
              492  LOAD_ATTR                version_info
              494  LOAD_CONST               0
              496  BINARY_SUBSCR    
              498  LOAD_CONST               2
              500  COMPARE_OP               ==
          502_504  POP_JUMP_IF_FALSE   540  'to 540'

 L. 257       506  LOAD_FAST                'sitedirs'
              508  LOAD_METHOD              append

 L. 258       510  LOAD_GLOBAL              os
              512  LOAD_ATTR                path
              514  LOAD_METHOD              join
              516  LOAD_FAST                'prefix'
              518  LOAD_STR                 'lib'
              520  LOAD_STR                 'python{}.{}'
              522  LOAD_ATTR                format
              524  LOAD_GLOBAL              sys
              526  LOAD_ATTR                version_info
              528  CALL_FUNCTION_EX      0  'positional arguments only'
              530  LOAD_STR                 'dist-packages'
              532  CALL_METHOD_4         4  '4 positional arguments'
              534  CALL_METHOD_1         1  '1 positional argument'
              536  POP_TOP          
              538  JUMP_FORWARD        576  'to 576'
            540_0  COME_FROM           502  '502'

 L. 261       540  LOAD_FAST                'sitedirs'
              542  LOAD_METHOD              append

 L. 262       544  LOAD_GLOBAL              os
              546  LOAD_ATTR                path
              548  LOAD_METHOD              join
              550  LOAD_FAST                'prefix'
              552  LOAD_STR                 'lib'
              554  LOAD_STR                 'python{}'
              556  LOAD_METHOD              format
              558  LOAD_GLOBAL              sys
              560  LOAD_ATTR                version_info
              562  LOAD_CONST               0
              564  BINARY_SUBSCR    
              566  CALL_METHOD_1         1  '1 positional argument'
              568  LOAD_STR                 'dist-packages'
              570  CALL_METHOD_4         4  '4 positional arguments'
              572  CALL_METHOD_1         1  '1 positional argument'
              574  POP_TOP          
            576_0  COME_FROM           538  '538'

 L. 264       576  LOAD_FAST                'sitedirs'
              578  LOAD_METHOD              append
              580  LOAD_GLOBAL              os
              582  LOAD_ATTR                path
              584  LOAD_METHOD              join
              586  LOAD_FAST                'prefix'
            588_0  COME_FROM           190  '190'
              588  LOAD_STR                 'lib'
              590  LOAD_STR                 'dist-python'
              592  CALL_METHOD_3         3  '3 positional arguments'
              594  CALL_METHOD_1         1  '1 positional argument'
              596  POP_TOP          
              598  JUMP_FORWARD        620  'to 620'
            600_0  COME_FROM           232  '232'

 L. 266       600  LOAD_FAST                'prefix'
              602  LOAD_GLOBAL              os
              604  LOAD_ATTR                path
              606  LOAD_METHOD              join
              608  LOAD_FAST                'prefix'
              610  LOAD_STR                 'lib'
              612  LOAD_STR                 'site-packages'
              614  CALL_METHOD_3         3  '3 positional arguments'
              616  BUILD_LIST_2          2 
              618  STORE_FAST               'sitedirs'
            620_0  COME_FROM           598  '598'
            620_1  COME_FROM           220  '220'
            620_2  COME_FROM           116  '116'
            620_3  COME_FROM            92  '92'

 L. 267       620  LOAD_GLOBAL              sys
              622  LOAD_ATTR                platform
              624  LOAD_STR                 'darwin'
              626  COMPARE_OP               ==
          628_630  POP_JUMP_IF_FALSE   704  'to 704'

 L. 271       632  LOAD_STR                 'Python.framework'
              634  LOAD_FAST                'prefix'
              636  COMPARE_OP               in
          638_640  POP_JUMP_IF_TRUE    652  'to 652'
              642  LOAD_STR                 'Python3.framework'
              644  LOAD_FAST                'prefix'
              646  COMPARE_OP               in
          648_650  POP_JUMP_IF_FALSE   704  'to 704'
            652_0  COME_FROM           638  '638'

 L. 272       652  LOAD_GLOBAL              os
              654  LOAD_ATTR                environ
              656  LOAD_METHOD              get
              658  LOAD_STR                 'HOME'
              660  CALL_METHOD_1         1  '1 positional argument'
              662  STORE_FAST               'home'

 L. 273       664  LOAD_FAST                'home'
          666_668  POP_JUMP_IF_FALSE   704  'to 704'

 L. 274       670  LOAD_FAST                'sitedirs'
              672  LOAD_METHOD              append

 L. 275       674  LOAD_GLOBAL              os
              676  LOAD_ATTR                path
              678  LOAD_METHOD              join
              680  LOAD_FAST                'home'
              682  LOAD_STR                 'Library'
              684  LOAD_STR                 'Python'
              686  LOAD_STR                 '{}.{}'
              688  LOAD_ATTR                format
              690  LOAD_GLOBAL              sys
              692  LOAD_ATTR                version_info
              694  CALL_FUNCTION_EX      0  'positional arguments only'
              696  LOAD_STR                 'site-packages'
              698  CALL_METHOD_5         5  '5 positional arguments'
              700  CALL_METHOD_1         1  '1 positional argument'
              702  POP_TOP          
            704_0  COME_FROM           666  '666'
            704_1  COME_FROM           648  '648'
            704_2  COME_FROM           628  '628'

 L. 277       704  SETUP_LOOP          744  'to 744'
              706  LOAD_FAST                'sitedirs'
              708  GET_ITER         
            710_0  COME_FROM           724  '724'
              710  FOR_ITER            742  'to 742'
              712  STORE_FAST               'sitedir'

 L. 278       714  LOAD_GLOBAL              os
              716  LOAD_ATTR                path
              718  LOAD_METHOD              isdir
              720  LOAD_FAST                'sitedir'
              722  CALL_METHOD_1         1  '1 positional argument'
          724_726  POP_JUMP_IF_FALSE   710  'to 710'

 L. 279       728  LOAD_GLOBAL              addsitedir
              730  LOAD_FAST                'sitedir'
              732  LOAD_FAST                'known_paths'
              734  CALL_FUNCTION_2       2  '2 positional arguments'
              736  POP_TOP          
          738_740  JUMP_BACK           710  'to 710'
              742  POP_BLOCK        
            744_0  COME_FROM_LOOP      704  '704'
              744  JUMP_BACK            54  'to 54'
              746  POP_BLOCK        
            748_0  COME_FROM_LOOP       46  '46'

Parse error at or near `COME_FROM' instruction at offset 588_0


def check_enableusersite():
    """Check if user site directory is safe for inclusion

    The function tests for the command line flag (including environment var),
    process uid/gid equal to effective uid/gid.

    None: Disabled for security reasons
    False: Disabled by user (command line option)
    True: Safe and enabled
    """
    if hasattr(sys, 'flags'):
        if getattr(sys.flags, 'no_user_site', False):
            return False
        elif hasattr(os, 'getuid') and hasattr(os, 'geteuid') and os.geteuid() != os.getuid():
            return
    elif hasattr(os, 'getgid'):
        if hasattr(os, 'getegid') and os.getegid() != os.getgid():
            return
    return True


def addusersitepackages(known_paths):
    """Add a per user site-package to sys.path

    Each user has its own python directory with site-packages in the
    home directory.

    USER_BASE is the root directory for all Python versions

    USER_SITE is the user specific site-packages directory

    USER_SITE/.. can be used for data.
    """
    global ENABLE_USER_SITE
    global USER_BASE
    global USER_SITE
    env_base = os.environ.get('PYTHONUSERBASE', None)

    def joinuser(*args):
        return os.path.expanduser((os.path.join)(*args))

    if os.name == 'nt':
        base = os.environ.get('APPDATA') or '~'
        if env_base:
            USER_BASE = env_base
        else:
            USER_BASE = joinuser(base, 'Python')
        USER_SITE = os.path.joinUSER_BASE('Python{}{}'.format)(*sys.version_info)'site-packages'
    else:
        if env_base:
            USER_BASE = env_base
        else:
            USER_BASE = joinuser('~', '.local')
        USER_SITE = os.path.joinUSER_BASE'lib'('python{}.{}'.format)(*sys.version_info)'site-packages'
    if ENABLE_USER_SITE:
        if os.path.isdir(USER_SITE):
            addsitedir(USER_SITE, known_paths)
    if ENABLE_USER_SITE:
        for dist_libdir in ('lib', 'local/lib'):
            user_site = os.path.joinUSER_BASEdist_libdir('python{}.{}'.format)(*sys.version_info)'dist-packages'
            if os.path.isdir(user_site):
                addsitedir(user_site, known_paths)

    return known_paths


def setBEGINLIBPATH():
    """The OS/2 EMX port has optional extension modules that do double duty
    as DLLs (and must use the .DLL file extension) for other extensions.
    The library search path needs to be amended so these will be found
    during module import.  Use BEGINLIBPATH so that these are at the start
    of the library search path.

    """
    dllpath = os.path.joinsys.prefix'Lib''lib-dynload'
    libpath = os.environ['BEGINLIBPATH'].split(';')
    if libpath[(-1)]:
        libpath.append(dllpath)
    else:
        libpath[-1] = dllpath
    os.environ['BEGINLIBPATH'] = ';'.join(libpath)


def setquit():
    """Define new built-ins 'quit' and 'exit'.
    These are simply strings that display a hint on how to exit.

    """
    if os.sep == ':':
        eof = 'Cmd-Q'
    else:
        if os.sep == '\\':
            eof = 'Ctrl-Z plus Return'
        else:
            eof = 'Ctrl-D (i.e. EOF)'

    class Quitter(object):

        def __init__(self, name):
            self.name = name

        def __repr__(self):
            return 'Use {}() or {} to exit'.format(self.name, eof)

        def __call__(self, code=None):
            try:
                sys.stdin.close()
            except:
                pass

            raise SystemExit(code)

    builtins.quit = Quitter('quit')
    builtins.exit = Quitter('exit')


class _Printer(object):
    __doc__ = 'interactive prompt objects for printing the license text, a list of\n    contributors and the copyright notice.'
    MAXLINES = 23

    def __init__(self, name, data, files=(), dirs=()):
        self._Printer__name = name
        self._Printer__data = data
        self._Printer__files = files
        self._Printer__dirs = dirs
        self._Printer__lines = None

    def __setup(self):
        if self._Printer__lines:
            return
        data = None
        for dir in self._Printer__dirs:
            for filename in self._Printer__files:
                filename = os.path.join(dir, filename)
                try:
                    fp = open(filename, 'r')
                    data = fp.read()
                    fp.close()
                    break
                except IOError:
                    pass

            if data:
                break

        if not data:
            data = self._Printer__data
        self._Printer__lines = data.split('\n')
        self._Printer__linecnt = len(self._Printer__lines)

    def __repr__(self):
        self._Printer__setup()
        if len(self._Printer__lines) <= self.MAXLINES:
            return '\n'.join(self._Printer__lines)
        return 'Type %s() to see the full %s text' % ((self._Printer__name,) * 2)

    def __call__(self):
        self._Printer__setup()
        prompt = 'Hit Return for more, or q (and Return) to quit: '
        lineno = 0
        while 1:
            try:
                for i in range(lineno, lineno + self.MAXLINES):
                    print(self._Printer__lines[i])

            except IndexError:
                break
            else:
                lineno += self.MAXLINES
                key = None
                while key is None:
                    try:
                        key = raw_input(prompt)
                    except NameError:
                        key = input(prompt)

                    if key not in ('', 'q'):
                        key = None

                if key == 'q':
                    break


def setcopyright():
    """Set 'copyright' and 'credits' in __builtin__"""
    builtins.copyright = _Printer('copyright', sys.copyright)
    if _is_pypy:
        builtins.credits = _Printer('credits', 'PyPy is maintained by the PyPy developers: http://pypy.org/')
    else:
        builtins.credits = _Printer('credits', '    Thanks to CWI, CNRI, BeOpen.com, Zope Corporation and a cast of thousands\n    for supporting Python development.  See www.python.org for more information.')
    here = os.path.dirname(os.__file__)
    builtins.license = _Printer('license', 'See https://www.python.org/psf/license/', [
     'LICENSE.txt', 'LICENSE'], [
     sys.prefix, os.path.join(here, os.pardir), here, os.curdir])


class _Helper(object):
    __doc__ = "Define the built-in 'help'.\n    This is a wrapper around pydoc.help (with a twist).\n\n    "

    def __repr__(self):
        return 'Type help() for interactive help, or help(object) for help about object.'

    def __call__(self, *args, **kwds):
        import pydoc
        return (pydoc.help)(*args, **kwds)


def sethelper():
    builtins.help = _Helper()


def aliasmbcs():
    """On Windows, some default encodings are not provided by Python,
    while they are always available as "mbcs" in each locale. Make
    them usable by aliasing to "mbcs" in such a case."""
    if sys.platform == 'win32':
        import locale, codecs
        enc = locale.getdefaultlocale()[1]
        if enc.startswith('cp'):
            try:
                codecs.lookup(enc)
            except LookupError:
                import encodings
                encodings._cache[enc] = encodings._unknown
                encodings.aliases.aliases[enc] = 'mbcs'


def setencoding():
    """Set the string encoding used by the Unicode implementation.  The
    default is 'ascii', but if you're willing to experiment, you can
    change this."""
    encoding = 'ascii'
    if encoding != 'ascii':
        sys.setdefaultencoding(encoding)


def execsitecustomize():
    """Run custom site specific code, if available."""
    try:
        import sitecustomize
    except ImportError:
        pass


def virtual_install_main_packages():
    f = open(os.path.join(os.path.dirname(__file__), 'orig-prefix.txt'))
    sys.real_prefix = f.read().strip()
    f.close()
    pos = 2
    hardcoded_relative_dirs = []
    if sys.path[0] == '':
        pos += 1
    if _is_pypy:
        if sys.version_info > (3, 2):
            cpyver = '%d' % sys.version_info[0]
        else:
            if sys.pypy_version_info >= (1, 5):
                cpyver = '%d.%d' % sys.version_info[:2]
            else:
                cpyver = '%d.%d.%d' % sys.version_info[:3]
        paths = [
         os.path.join(sys.real_prefix, 'lib_pypy'), os.path.joinsys.real_prefix'lib-python'cpyver]
        if sys.pypy_version_info < (1, 9):
            paths.insert(1, os.path.joinsys.real_prefix'lib-python'('modified-%s' % cpyver))
        hardcoded_relative_dirs = paths[:]
        for path in paths[:]:
            plat_path = os.path.join(path, 'plat-%s' % sys.platform)
            if os.path.exists(plat_path):
                paths.append(plat_path)

    else:
        if sys.platform == 'win32':
            paths = [
             os.path.join(sys.real_prefix, 'Lib'), os.path.join(sys.real_prefix, 'DLLs')]
        else:
            paths = [
             os.path.joinsys.real_prefix'lib'('python{}.{}'.format)(*sys.version_info)]
            hardcoded_relative_dirs = paths[:]
            lib64_path = os.path.joinsys.real_prefix'lib64'('python{}.{}'.format)(*sys.version_info)
            if os.path.exists(lib64_path):
                if _is_64bit:
                    paths.insert(0, lib64_path)
                else:
                    paths.append(lib64_path)
            try:
                arch = getattr(sys, 'implementation', sys)._multiarch
            except AttributeError:
                arch = sys.platform

            plat_path = os.path.joinsys.real_prefix'lib'('python{}.{}'.format)(*sys.version_info)('plat-%s' % arch)
            if os.path.exists(plat_path):
                paths.append(plat_path)
            for path in list(paths):
                tk_dir = os.path.join(path, 'lib-tk')
                if os.path.exists(tk_dir):
                    paths.append(tk_dir)

            if sys.platform == 'darwin':
                hardcoded_paths = [os.path.join(relative_dir, module) for relative_dir in hardcoded_relative_dirs for module in ('plat-darwin',
                                                                                                                                 'plat-mac',
                                                                                                                                 'plat-mac/lib-scriptpackages')]
                for path in hardcoded_paths:
                    if os.path.exists(path):
                        paths.append(path)

            sys.path.extend(paths)


def force_global_eggs_after_local_site_packages():
    """
    Force easy_installed eggs in the global environment to get placed
    in sys.path after all packages inside the virtualenv.  This
    maintains the "least surprise" result that packages in the
    virtualenv always mask global packages, never the other way
    around.

    """
    egginsert = getattr(sys, '__egginsert', 0)
    for i, path in enumerate(sys.path):
        if i > egginsert and path.startswith(sys.prefix):
            egginsert = i

    sys.__egginsert = egginsert + 1


def virtual_addsitepackages(known_paths):
    force_global_eggs_after_local_site_packages()
    return addsitepackages(known_paths, sys_prefix=(sys.real_prefix))


def execusercustomize():
    """Run custom user specific code, if available."""
    try:
        import usercustomize
    except ImportError:
        pass


def enablerlcompleter():
    """Enable default readline configuration on interactive prompts, by
    registering a sys.__interactivehook__.
    If the readline module can be imported, the hook will set the Tab key
    as completion key and register ~/.python_history as history file.
    This can be overridden in the sitecustomize or usercustomize module,
    or in a PYTHONSTARTUP file.
    """

    def register_readline():
        import atexit
        try:
            import readline, rlcompleter
        except ImportError:
            return
        else:
            readline_doc = getattr(readline, '__doc__', '')
            if readline_doc is not None and 'libedit' in readline_doc:
                readline.parse_and_bind('bind ^I rl_complete')
            else:
                readline.parse_and_bind('tab: complete')
            try:
                readline.read_init_file()
            except OSError:
                pass

            if readline.get_current_history_length() == 0:
                history = os.path.join(os.path.expanduser('~'), '.python_history')
                try:
                    readline.read_history_file(history)
                except OSError:
                    pass

                def write_history():
                    try:
                        readline.write_history_file(history)
                    except (FileNotFoundError, PermissionError):
                        pass

                atexit.register(write_history)

    sys.__interactivehook__ = register_readline


if _is_pypy:

    def import_builtin_stuff():
        """PyPy specific: some built-in modules should be pre-imported because
        some programs expect them to be in sys.modules on startup. This is ported
        from PyPy's site.py.
        """
        import encodings
        if 'exceptions' in sys.builtin_module_names:
            import exceptions
        if 'zipimport' in sys.builtin_module_names:
            import zipimport


def main():
    global ENABLE_USER_SITE
    virtual_install_main_packages()
    if _is_pypy:
        import_builtin_stuff()
    abs__file__()
    paths_in_sys = removeduppaths()
    if os.name == 'posix':
        if sys.path:
            if os.path.basename(sys.path[(-1)]) == 'Modules':
                addbuilddir()
    GLOBAL_SITE_PACKAGES = not os.path.exists(os.path.join(os.path.dirname(__file__), 'no-global-site-packages.txt'))
    if not GLOBAL_SITE_PACKAGES:
        ENABLE_USER_SITE = False
    if ENABLE_USER_SITE is None:
        ENABLE_USER_SITE = check_enableusersite()
    paths_in_sys = addsitepackages(paths_in_sys)
    paths_in_sys = addusersitepackages(paths_in_sys)
    if GLOBAL_SITE_PACKAGES:
        paths_in_sys = virtual_addsitepackages(paths_in_sys)
    if sys.platform == 'os2emx':
        setBEGINLIBPATH()
    setquit()
    setcopyright()
    sethelper()
    if sys.version_info[0] == 3:
        enablerlcompleter()
    aliasmbcs()
    setencoding()
    execsitecustomize()
    if ENABLE_USER_SITE:
        execusercustomize()
    if hasattr(sys, 'setdefaultencoding'):
        del sys.setdefaultencoding


main()

def _script():
    help = "    %s [--user-base] [--user-site]\n\n    Without arguments print some useful information\n    With arguments print the value of USER_BASE and/or USER_SITE separated\n    by '%s'.\n\n    Exit codes with --user-base or --user-site:\n      0 - user site directory is enabled\n      1 - user site directory is disabled by user\n      2 - uses site directory is disabled by super user\n          or for security reasons\n     >2 - unknown error\n    "
    args = sys.argv[1:]
    if not args:
        print('sys.path = [')
        for dir in sys.path:
            print('    {!r},'.format(dir))

        print(']')

        def exists(path):
            if os.path.isdir(path):
                return 'exists'
            return "doesn't exist"

        print('USER_BASE: {!r} ({})'.format(USER_BASE, exists(USER_BASE)))
        print('USER_SITE: {!r} ({})'.format(USER_SITE, exists(USER_SITE)))
        print('ENABLE_USER_SITE: %r' % ENABLE_USER_SITE)
        sys.exit(0)
    else:
        buffer = []
        if '--user-base' in args:
            buffer.append(USER_BASE)
        if '--user-site' in args:
            buffer.append(USER_SITE)
        if buffer:
            print(os.pathsep.join(buffer))
            if ENABLE_USER_SITE:
                sys.exit(0)
            else:
                if ENABLE_USER_SITE is False:
                    sys.exit(1)
                else:
                    if ENABLE_USER_SITE is None:
                        sys.exit(2)
                    else:
                        sys.exit(3)
        else:
            import textwrap
            print(textwrap.dedent(help % (sys.argv[0], os.pathsep)))
            sys.exit(10)


if __name__ == '__main__':
    _script()