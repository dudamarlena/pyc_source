# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/vohl/Documents/code/shwirl/shwirl/extern/vispy/testing/_runners.py
# Compiled at: 2018-10-01 14:58:41
# Size of source mod 2**32: 14738 bytes
"""Test running functions"""
from __future__ import print_function
import sys, os, warnings
from os import path as op
from copy import deepcopy
from functools import partial
from ..util import use_log_level, run_subprocess
from util.ptime import time
from ._testing import SkipTest, has_application, nottest
_line_sep = '----------------------------------------------------------------------'

def _get_import_dir():
    import_dir = op.abspath(op.join(op.dirname(__file__), '..'))
    up_dir = op.join(import_dir, '..')
    if op.isfile(op.join(up_dir, 'setup.py')) and op.isdir(op.join(up_dir, 'vispy')) and op.isdir(op.join(up_dir, 'examples')):
        dev = True
    else:
        dev = False
    return (
     import_dir, dev)


_unit_script = '\ntry:\n    import pytest as tester\nexcept ImportError:\n    import nose as tester\ntry:\n    import faulthandler\n    faulthandler.enable()\nexcept Exception:\n    pass\n\nraise SystemExit(tester.main(%r))\n'

def _unit(mode, extra_arg_string, coverage=False):
    """Run unit tests using a particular mode"""
    import_dir = _get_import_dir()[0]
    cwd = op.abspath(op.join(import_dir, '..'))
    extra_args = [''] + extra_arg_string.split(' ')
    del extra_arg_string
    use_pytest = False
    try:
        import pytest
        use_pytest = True
    except ImportError:
        try:
            import nose
        except ImportError:
            raise SkipTest('Skipping unit tests, neither pytest nor nose installed')

    if mode == 'nobackend':
        msg = 'Running tests with no backend'
        if use_pytest:
            extra_args += ['-m', '"not vispy_app_test"']
        else:
            extra_args += ['-a', '"!vispy_app_test"']
    else:
        invalid = run_subprocess([sys.executable, '-c',
         'import vispy.app; vispy.app.use_app("%s"); exit(0)' % mode],
          return_code=True)[2]
        if invalid:
            print('%s\n%s\n%s' % (_line_sep,
             'Skipping backend %s, not installed or working properly' % mode,
             _line_sep))
            raise SkipTest()
        else:
            msg = 'Running tests with %s backend' % mode
            if use_pytest:
                extra_args += ['-m', 'vispy_app_test']
            else:
                extra_args += ['-a', 'vispy_app_test']
    if coverage:
        if use_pytest:
            extra_args += ['--cov', 'vispy', '--no-cov-on-fail']
    extra_arg_string = ' '.join(extra_args)
    insert = extra_arg_string if use_pytest else extra_args
    extra_args += [import_dir]
    cmd = [sys.executable, '-c', _unit_script % insert]
    env = deepcopy(os.environ)
    env.update(dict(_VISPY_TESTING_APP=mode, VISPY_IGNORE_OLD_VERSION='true'))
    env_str = '_VISPY_TESTING_APP=%s ' % mode
    if len(msg) > 0:
        msg = '%s\n%s:\n%s%s' % (
         _line_sep, msg, env_str, extra_arg_string)
        print(msg)
    sys.stdout.flush()
    return_code = run_subprocess(cmd, return_code=True, cwd=cwd, env=env,
      stdout=None,
      stderr=None)[2]
    if return_code:
        raise RuntimeError('unit failure (%s)' % return_code)
    if coverage:
        out_name = op.join(cwd, '.vispy-coverage.%s' % mode)
        if op.isfile(out_name):
            os.remove(out_name)
        os.rename(op.join(cwd, '.coverage'), out_name)


def _docs():
    """test docstring paramters
    using vispy/utils/tests/test_docstring_parameters.py"""
    dev = _get_import_dir()[1]
    if not dev:
        warnings.warn("Docstring test imports Vispy from Vispy's installation. It is recommended to setup Vispy using 'python setup.py develop' so that the latest sources are used automatically")
    try:
        from util.tests import test_docstring_parameters
        print('Running docstring test...')
        test_docstring_parameters.test_docstring_parameters()
    except AssertionError as docstring_violations:
        try:
            raise RuntimeError(docstring_violations)
        finally:
            docstring_violations = None
            del docstring_violations


def _flake():
    """Test flake8"""
    orig_dir = os.getcwd()
    import_dir, dev = _get_import_dir()
    os.chdir(op.join(import_dir, '..'))
    if dev:
        sys.argv[1:] = [
         'vispy', 'examples', 'make']
    else:
        sys.argv[1:] = [
         op.basename(import_dir)]
    sys.argv.append('--ignore=E226,E241,E265,E266,W291,W293,W503,F999')
    sys.argv.append('--exclude=six.py,ordereddict.py,glfw.py,_proxy.py,_es2.py,_gl2.py,_pyopengl2.py,_constants.py,png.py,decorator.py,ipy_inputhook.py,experimental,wiki,_old,mplexporter.py,cubehelix.py,cassowary')
    try:
        try:
            import flake8.main as main
        except ImportError:
            print('Skipping flake8 test, flake8 not installed')
        else:
            print('Running flake8... ')
            sys.stdout.flush()
            try:
                main()
            except SystemExit as ex:
                try:
                    if ex.code in (None, 0):
                        pass
                    else:
                        raise RuntimeError('flake8 failed')
                finally:
                    ex = None
                    del ex

    finally:
        os.chdir(orig_dir)


def _check_line_endings():
    """Check all files in the repository for CR characters"""
    if sys.platform == 'win32':
        print('Skipping line endings check on Windows')
        sys.stdout.flush()
        return
    print('Running line endings check... ')
    sys.stdout.flush()
    report = []
    import_dir, dev = _get_import_dir()
    for dirpath, dirnames, filenames in os.walk(import_dir):
        for fname in filenames:
            if op.splitext(fname)[1] in ('.pyc', '.pyo', '.so', '.dll'):
                continue
            filename = op.join(dirpath, fname)
            relfilename = op.relpath(filename, import_dir)
            try:
                with open(filename, 'rb') as (fid):
                    text = fid.read().decode('utf-8')
            except UnicodeDecodeError:
                continue

            crcount = text.count('\r')
            if crcount:
                lfcount = text.count('\n')
                report.append('In %s found %i/%i CR/LF' % (
                 relfilename, crcount, lfcount))

    if len(report) > 0:
        raise RuntimeError('Found %s files with incorrect endings:\n%s' % (
         len(report), '\n'.join(report)))


_script = "\nimport sys\nimport time\nimport warnings\nimport os\ntry:\n    import faulthandler\n    faulthandler.enable()\nexcept Exception:\n    pass\nos.environ['VISPY_IGNORE_OLD_VERSION'] = 'true'\nimport {0}\n\nif hasattr({0}, 'canvas'):\n    canvas = {0}.canvas\nelif hasattr({0}, 'Canvas'):\n    canvas = {0}.Canvas()\nelif hasattr({0}, 'fig'):\n    canvas = {0}.fig\nelse:\n    raise RuntimeError('Bad example formatting: fix or add `# vispy: testskip`'\n                       ' to the top of the file.')\n\nwith canvas as c:\n    for _ in range(5):\n        c.update()\n        c.app.process_events()\n        time.sleep(1./60.)\n"

def _examples(fnames_str):
    """Run examples and make sure they work.

    Parameters
    ----------
    fnames_str : str
        Can be a space-separated list of paths to test, or an empty string to
        auto-detect and run all examples.
    """
    import_dir, dev = _get_import_dir()
    reason = None
    if not dev:
        reason = 'Cannot test examples unless in vispy git directory'
    else:
        with use_log_level('warning', print_msg=False):
            good, backend = has_application(capable=('multi_window', ))
        if not good:
            reason = 'Must have suitable app backend'
        else:
            if reason is not None:
                msg = 'Skipping example test: %s' % reason
                print(msg)
                raise SkipTest(msg)
            if fnames_str:
                fnames = fnames_str.split(' ')
            else:
                fnames = [op.join(d[0], fname) for d in os.walk(op.join(import_dir, '..', 'examples')) for fname in d[2] if fname.endswith('.py')]
        fnames = sorted(fnames, key=(lambda x: x.lower()))
        print(_line_sep + '\nRunning %s examples using %s backend' % (
         len(fnames), backend))
        (op.join('tutorial', 'app', 'shared_context.py'),)
        fails = []
        n_ran = n_skipped = 0
        t0 = time()
        for fname in fnames:
            n_ran += 1
            root_name = op.split(fname)
            root_name = op.join(op.split(op.split(root_name[0])[0])[1], op.split(root_name[0])[1], root_name[1])
            good = True
            with open(fname, 'r') as (fid):
                for _ in range(10):
                    line = fid.readline()
                    if line == '':
                        break
                    elif line.startswith('# vispy: ') and 'testskip' in line:
                        good = False
                        break

            if not good:
                n_ran -= 1
                n_skipped += 1
                continue
            else:
                sys.stdout.flush()
                cwd = op.dirname(fname)
                cmd = [sys.executable, '-c', _script.format(op.split(fname)[1][:-3])]
                sys.stdout.flush()
                stdout, stderr, retcode = run_subprocess(cmd, return_code=True, cwd=cwd,
                  env=(os.environ))
                if retcode or len(stderr.strip()) > 0:
                    if 'ImportError: ' in stderr:
                        print('S', end='')
                    else:
                        ext = '\n' + _line_sep + '\n'
                        fails.append('%sExample %s failed (%s):%s%s%s' % (
                         ext, root_name, retcode, ext, stderr, ext))
                        print(fails[(-1)])
                else:
                    print('.', end='')
            sys.stdout.flush()

        print('')
        t = ': %s failed, %s succeeded, %s skipped in %s seconds' % (
         len(fails), n_ran - len(fails), n_skipped, round(time() - t0))
        if len(fails) > 0:
            raise RuntimeError('Failed%s' % t)
        print('Success%s' % t)


@nottest
def test--- This code section failed: ---

 L. 350         0  LOAD_FAST                'label'
                2  LOAD_STR                 'osmesa'
                4  COMPARE_OP               ==
                6  POP_JUMP_IF_FALSE    26  'to 26'

 L. 353         8  LOAD_CONST               2
               10  LOAD_CONST               ('fix_osmesa_gl_lib',)
               12  IMPORT_NAME_ATTR         util.osmesa_gl
               14  IMPORT_FROM              fix_osmesa_gl_lib
               16  STORE_FAST               'fix_osmesa_gl_lib'
               18  POP_TOP          

 L. 354        20  LOAD_FAST                'fix_osmesa_gl_lib'
               22  CALL_FUNCTION_0       0  '0 positional arguments'
               24  POP_TOP          
             26_0  COME_FROM             6  '6'

 L. 356        26  LOAD_CONST               2
               28  LOAD_CONST               ('BACKEND_NAMES',)
               30  IMPORT_NAME_ATTR         app.backends
               32  IMPORT_FROM              BACKEND_NAMES
               34  STORE_FAST               'backend_names'
               36  POP_TOP          

 L. 357        38  LOAD_FAST                'label'
               40  LOAD_METHOD              lower
               42  CALL_METHOD_0         0  '0 positional arguments'
               44  STORE_FAST               'label'

 L. 358        46  LOAD_FAST                'label'
               48  LOAD_STR                 'nose'
               50  COMPARE_OP               ==
               52  POP_JUMP_IF_FALSE    58  'to 58'
               54  LOAD_STR                 'pytest'
               56  JUMP_FORWARD         60  'to 60'
             58_0  COME_FROM            52  '52'
               58  LOAD_FAST                'label'
             60_0  COME_FROM            56  '56'
               60  STORE_FAST               'label'

 L. 359        62  LOAD_STR                 'full'
               64  LOAD_STR                 'unit'
               66  LOAD_STR                 'lineendings'
               68  LOAD_STR                 'extra'
               70  LOAD_STR                 'flake'

 L. 360        72  LOAD_STR                 'docs'
               74  LOAD_STR                 'nobackend'
               76  LOAD_STR                 'examples'
               78  BUILD_LIST_8          8 
               80  STORE_FAST               'known_types'

 L. 362        82  LOAD_FAST                'label'
               84  LOAD_FAST                'known_types'
               86  LOAD_FAST                'backend_names'
               88  BINARY_ADD       
               90  COMPARE_OP               not-in
               92  POP_JUMP_IF_FALSE   112  'to 112'

 L. 363        94  LOAD_GLOBAL              ValueError
               96  LOAD_STR                 "label must be one of %s, or a backend name %s, not '%s'"

 L. 364        98  LOAD_FAST                'known_types'
              100  LOAD_FAST                'backend_names'
              102  LOAD_FAST                'label'
              104  BUILD_TUPLE_3         3 
              106  BINARY_MODULO    
              108  CALL_FUNCTION_1       1  '1 positional argument'
              110  RAISE_VARARGS_1       1  'exception instance'
            112_0  COME_FROM            92  '92'

 L. 366       112  BUILD_LIST_0          0 
              114  STORE_FAST               'runs'

 L. 367       116  LOAD_FAST                'label'
              118  LOAD_CONST               ('full', 'unit')
              120  COMPARE_OP               in
              122  POP_JUMP_IF_FALSE   164  'to 164'

 L. 368       124  SETUP_LOOP          196  'to 196'
              126  LOAD_FAST                'backend_names'
              128  GET_ITER         
              130  FOR_ITER            160  'to 160'
              132  STORE_FAST               'backend'

 L. 369       134  LOAD_FAST                'runs'
              136  LOAD_METHOD              append
              138  LOAD_GLOBAL              partial
              140  LOAD_GLOBAL              _unit
              142  LOAD_FAST                'backend'
              144  LOAD_FAST                'extra_arg_string'
              146  LOAD_FAST                'coverage'
              148  CALL_FUNCTION_4       4  '4 positional arguments'

 L. 370       150  LOAD_FAST                'backend'
              152  BUILD_LIST_2          2 
              154  CALL_METHOD_1         1  '1 positional argument'
              156  POP_TOP          
              158  JUMP_BACK           130  'to 130'
              160  POP_BLOCK        
              162  JUMP_FORWARD        196  'to 196'
            164_0  COME_FROM           122  '122'

 L. 371       164  LOAD_FAST                'label'
              166  LOAD_FAST                'backend_names'
              168  COMPARE_OP               in
              170  POP_JUMP_IF_FALSE   196  'to 196'

 L. 372       172  LOAD_FAST                'runs'
              174  LOAD_METHOD              append
              176  LOAD_GLOBAL              partial
              178  LOAD_GLOBAL              _unit
              180  LOAD_FAST                'label'
              182  LOAD_FAST                'extra_arg_string'
              184  LOAD_FAST                'coverage'
              186  CALL_FUNCTION_4       4  '4 positional arguments'
              188  LOAD_FAST                'label'
              190  BUILD_LIST_2          2 
              192  CALL_METHOD_1         1  '1 positional argument'
              194  POP_TOP          
            196_0  COME_FROM           170  '170'
            196_1  COME_FROM           162  '162'
            196_2  COME_FROM_LOOP      124  '124'

 L. 374       196  LOAD_FAST                'label'
              198  LOAD_CONST               ('full', 'unit', 'nobackend')
              200  COMPARE_OP               in
              202  POP_JUMP_IF_FALSE   228  'to 228'

 L. 375       204  LOAD_FAST                'runs'
              206  LOAD_METHOD              append
              208  LOAD_GLOBAL              partial
              210  LOAD_GLOBAL              _unit
              212  LOAD_STR                 'nobackend'
              214  LOAD_FAST                'extra_arg_string'
              216  LOAD_FAST                'coverage'
              218  CALL_FUNCTION_4       4  '4 positional arguments'

 L. 376       220  LOAD_STR                 'nobackend'
              222  BUILD_LIST_2          2 
              224  CALL_METHOD_1         1  '1 positional argument'
              226  POP_TOP          
            228_0  COME_FROM           202  '202'

 L. 378       228  LOAD_FAST                'label'
              230  LOAD_STR                 'examples'
              232  COMPARE_OP               ==
          234_236  POP_JUMP_IF_FALSE   260  'to 260'

 L. 380       238  LOAD_FAST                'runs'
              240  LOAD_METHOD              append
              242  LOAD_GLOBAL              partial
              244  LOAD_GLOBAL              _examples
              246  LOAD_FAST                'extra_arg_string'
              248  CALL_FUNCTION_2       2  '2 positional arguments'

 L. 381       250  LOAD_STR                 'examples'
              252  BUILD_LIST_2          2 
              254  CALL_METHOD_1         1  '1 positional argument'
              256  POP_TOP          
              258  JUMP_FORWARD        290  'to 290'
            260_0  COME_FROM           234  '234'

 L. 382       260  LOAD_FAST                'label'
              262  LOAD_STR                 'full'
              264  COMPARE_OP               ==
          266_268  POP_JUMP_IF_FALSE   290  'to 290'

 L. 384       270  LOAD_FAST                'runs'
              272  LOAD_METHOD              append
              274  LOAD_GLOBAL              partial
              276  LOAD_GLOBAL              _examples
              278  LOAD_STR                 ''
              280  CALL_FUNCTION_2       2  '2 positional arguments'
              282  LOAD_STR                 'examples'
              284  BUILD_LIST_2          2 
              286  CALL_METHOD_1         1  '1 positional argument'
              288  POP_TOP          
            290_0  COME_FROM           266  '266'
            290_1  COME_FROM           258  '258'

 L. 386       290  LOAD_FAST                'label'
              292  LOAD_CONST               ('full', 'extra', 'lineendings')
              294  COMPARE_OP               in
          296_298  POP_JUMP_IF_FALSE   314  'to 314'

 L. 387       300  LOAD_FAST                'runs'
              302  LOAD_METHOD              append
              304  LOAD_GLOBAL              _check_line_endings
              306  LOAD_STR                 'lineendings'
              308  BUILD_LIST_2          2 
              310  CALL_METHOD_1         1  '1 positional argument'
              312  POP_TOP          
            314_0  COME_FROM           296  '296'

 L. 388       314  LOAD_FAST                'label'
              316  LOAD_CONST               ('full', 'extra', 'flake')
              318  COMPARE_OP               in
          320_322  POP_JUMP_IF_FALSE   338  'to 338'

 L. 389       324  LOAD_FAST                'runs'
              326  LOAD_METHOD              append
              328  LOAD_GLOBAL              _flake
              330  LOAD_STR                 'flake'
              332  BUILD_LIST_2          2 
              334  CALL_METHOD_1         1  '1 positional argument'
              336  POP_TOP          
            338_0  COME_FROM           320  '320'

 L. 390       338  LOAD_FAST                'label'
              340  LOAD_CONST               ('extra', 'docs')
              342  COMPARE_OP               in
          344_346  POP_JUMP_IF_FALSE   362  'to 362'

 L. 391       348  LOAD_FAST                'runs'
              350  LOAD_METHOD              append
              352  LOAD_GLOBAL              _docs
              354  LOAD_STR                 'docs'
              356  BUILD_LIST_2          2 
              358  CALL_METHOD_1         1  '1 positional argument'
              360  POP_TOP          
            362_0  COME_FROM           344  '344'

 L. 393       362  LOAD_GLOBAL              time
              364  CALL_FUNCTION_0       0  '0 positional arguments'
              366  STORE_FAST               't0'

 L. 394       368  BUILD_LIST_0          0 
              370  STORE_FAST               'fail'

 L. 395       372  BUILD_LIST_0          0 
              374  STORE_FAST               'skip'

 L. 396   376_378  SETUP_LOOP          636  'to 636'
              380  LOAD_FAST                'runs'
              382  GET_ITER         
              384  FOR_ITER            634  'to 634'
              386  STORE_FAST               'run'

 L. 397       388  SETUP_EXCEPT        404  'to 404'

 L. 398       390  LOAD_FAST                'run'
              392  LOAD_CONST               0
              394  BINARY_SUBSCR    
              396  CALL_FUNCTION_0       0  '0 positional arguments'
              398  POP_TOP          
              400  POP_BLOCK        
              402  JUMP_FORWARD        612  'to 612'
            404_0  COME_FROM_EXCEPT    388  '388'

 L. 399       404  DUP_TOP          
              406  LOAD_GLOBAL              RuntimeError
              408  COMPARE_OP               exception-match
          410_412  POP_JUMP_IF_FALSE   468  'to 468'
              414  POP_TOP          
              416  STORE_FAST               'exp'
              418  POP_TOP          
              420  SETUP_FINALLY       456  'to 456'

 L. 400       422  LOAD_GLOBAL              print
              424  LOAD_STR                 'Failed: %s'
              426  LOAD_GLOBAL              str
              428  LOAD_FAST                'exp'
              430  CALL_FUNCTION_1       1  '1 positional argument'
              432  BINARY_MODULO    
              434  CALL_FUNCTION_1       1  '1 positional argument'
              436  POP_TOP          

 L. 401       438  LOAD_FAST                'fail'
              440  LOAD_FAST                'run'
              442  LOAD_CONST               1
              444  BINARY_SUBSCR    
              446  BUILD_LIST_1          1 
              448  INPLACE_ADD      
              450  STORE_FAST               'fail'
              452  POP_BLOCK        
              454  LOAD_CONST               None
            456_0  COME_FROM_FINALLY   420  '420'
              456  LOAD_CONST               None
              458  STORE_FAST               'exp'
              460  DELETE_FAST              'exp'
              462  END_FINALLY      
              464  POP_EXCEPT       
              466  JUMP_FORWARD        620  'to 620'
            468_0  COME_FROM           410  '410'

 L. 402       468  DUP_TOP          
              470  LOAD_GLOBAL              SkipTest
              472  COMPARE_OP               exception-match
          474_476  POP_JUMP_IF_FALSE   502  'to 502'
              478  POP_TOP          
              480  POP_TOP          
              482  POP_TOP          

 L. 403       484  LOAD_FAST                'skip'
              486  LOAD_FAST                'run'
              488  LOAD_CONST               1
              490  BINARY_SUBSCR    
              492  BUILD_LIST_1          1 
              494  INPLACE_ADD      
              496  STORE_FAST               'skip'
              498  POP_EXCEPT       
              500  JUMP_FORWARD        620  'to 620'
            502_0  COME_FROM           474  '474'

 L. 404       502  DUP_TOP          
              504  LOAD_GLOBAL              Exception
              506  COMPARE_OP               exception-match
          508_510  POP_JUMP_IF_FALSE   610  'to 610'
              512  POP_TOP          
              514  STORE_FAST               'exp'
              516  POP_TOP          
              518  SETUP_FINALLY       598  'to 598'

 L. 406       520  LOAD_FAST                'fail'
              522  LOAD_FAST                'run'
              524  LOAD_CONST               1
              526  BINARY_SUBSCR    
              528  BUILD_LIST_1          1 
              530  INPLACE_ADD      
              532  STORE_FAST               'fail'

 L. 407       534  LOAD_GLOBAL              print
              536  LOAD_STR                 'Failed strangely (%s): %s\n'
              538  LOAD_GLOBAL              type
              540  LOAD_FAST                'exp'
              542  CALL_FUNCTION_1       1  '1 positional argument'
              544  LOAD_GLOBAL              str
              546  LOAD_FAST                'exp'
              548  CALL_FUNCTION_1       1  '1 positional argument'
              550  BUILD_TUPLE_2         2 
              552  BINARY_MODULO    
              554  CALL_FUNCTION_1       1  '1 positional argument'
              556  POP_TOP          

 L. 408       558  LOAD_CONST               0
              560  LOAD_CONST               None
              562  IMPORT_NAME              traceback
              564  STORE_FAST               'traceback'

 L. 409       566  LOAD_GLOBAL              sys
              568  LOAD_METHOD              exc_info
              570  CALL_METHOD_0         0  '0 positional arguments'
              572  UNPACK_SEQUENCE_3     3 
              574  STORE_FAST               'type_'
              576  STORE_FAST               'value'
              578  STORE_FAST               'tb'

 L. 410       580  LOAD_FAST                'traceback'
              582  LOAD_METHOD              print_exception
              584  LOAD_FAST                'type_'
              586  LOAD_FAST                'value'
              588  LOAD_FAST                'tb'
              590  CALL_METHOD_3         3  '3 positional arguments'
              592  POP_TOP          
              594  POP_BLOCK        
              596  LOAD_CONST               None
            598_0  COME_FROM_FINALLY   518  '518'
              598  LOAD_CONST               None
              600  STORE_FAST               'exp'
              602  DELETE_FAST              'exp'
              604  END_FINALLY      
              606  POP_EXCEPT       
              608  JUMP_FORWARD        620  'to 620'
            610_0  COME_FROM           508  '508'
              610  END_FINALLY      
            612_0  COME_FROM           402  '402'

 L. 412       612  LOAD_GLOBAL              print
              614  LOAD_STR                 'Passed\n'
              616  CALL_FUNCTION_1       1  '1 positional argument'
              618  POP_TOP          
            620_0  COME_FROM           608  '608'
            620_1  COME_FROM           500  '500'
            620_2  COME_FROM           466  '466'

 L. 413       620  LOAD_GLOBAL              sys
              622  LOAD_ATTR                stdout
              624  LOAD_METHOD              flush
              626  CALL_METHOD_0         0  '0 positional arguments'
              628  POP_TOP          
          630_632  JUMP_BACK           384  'to 384'
              634  POP_BLOCK        
            636_0  COME_FROM_LOOP      376  '376'

 L. 414       636  LOAD_GLOBAL              time
              638  CALL_FUNCTION_0       0  '0 positional arguments'
              640  LOAD_FAST                't0'
              642  BINARY_SUBTRACT  
              644  STORE_FAST               'dt'

 L. 415       646  LOAD_STR                 '%s failed, %s skipped'
              648  LOAD_FAST                'fail'
          650_652  POP_JUMP_IF_FALSE   658  'to 658'
              654  LOAD_FAST                'fail'
              656  JUMP_FORWARD        660  'to 660'
            658_0  COME_FROM           650  '650'
              658  LOAD_CONST               0
            660_0  COME_FROM           656  '656'
              660  LOAD_FAST                'skip'
          662_664  POP_JUMP_IF_FALSE   670  'to 670'
              666  LOAD_FAST                'skip'
              668  JUMP_FORWARD        672  'to 672'
            670_0  COME_FROM           662  '662'
              670  LOAD_CONST               0
            672_0  COME_FROM           668  '668'
              672  BUILD_TUPLE_2         2 
              674  BINARY_MODULO    
              676  STORE_FAST               'stat'

 L. 416       678  LOAD_FAST                'fail'
          680_682  POP_JUMP_IF_FALSE   688  'to 688'
              684  LOAD_STR                 'failed'
              686  JUMP_FORWARD        690  'to 690'
            688_0  COME_FROM           680  '680'
              688  LOAD_STR                 'succeeded'
            690_0  COME_FROM           686  '686'
              690  STORE_FAST               'extra'

 L. 417       692  LOAD_GLOBAL              print
              694  LOAD_STR                 'Testing %s (%s) in %0.3f seconds'
              696  LOAD_FAST                'extra'
              698  LOAD_FAST                'stat'
              700  LOAD_FAST                'dt'
              702  BUILD_TUPLE_3         3 
              704  BINARY_MODULO    
              706  CALL_FUNCTION_1       1  '1 positional argument'
              708  POP_TOP          

 L. 418       710  LOAD_GLOBAL              sys
              712  LOAD_ATTR                stdout
              714  LOAD_METHOD              flush
              716  CALL_METHOD_0         0  '0 positional arguments'
              718  POP_TOP          

 L. 419       720  LOAD_GLOBAL              len
              722  LOAD_FAST                'fail'
              724  CALL_FUNCTION_1       1  '1 positional argument'
              726  LOAD_CONST               0
              728  COMPARE_OP               >
          730_732  POP_JUMP_IF_FALSE   742  'to 742'

 L. 420       734  LOAD_GLOBAL              RuntimeError
              736  LOAD_STR                 'FAILURE'
              738  CALL_FUNCTION_1       1  '1 positional argument'
              740  RAISE_VARARGS_1       1  'exception instance'
            742_0  COME_FROM           730  '730'

Parse error at or near `COME_FROM_LOOP' instruction at offset 196_2