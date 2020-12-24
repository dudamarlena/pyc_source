# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/danyvohl/Documents/Etudes/Doctorat/Australie/code/shwirl/extern/vispy/testing/_runners.py
# Compiled at: 2016-11-03 01:40:19
"""Test running functions"""
from __future__ import print_function
import sys, os, warnings
from os import path as op
from copy import deepcopy
from functools import partial
from ..util import use_log_level, run_subprocess
from ..util.ptime import time
from ._testing import SkipTest, has_application, nottest
_line_sep = '-' * 70

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
         'import vispy.app; vispy.app.use_app("%s"); exit(0)' % mode], return_code=True)[2]
        if invalid:
            print('%s\n%s\n%s' % (_line_sep,
             'Skipping backend %s, not installed or working properly' % mode,
             _line_sep))
            raise SkipTest()
        msg = 'Running tests with %s backend' % mode
        if use_pytest:
            extra_args += ['-m', 'vispy_app_test']
        else:
            extra_args += ['-a', 'vispy_app_test']
    if coverage and use_pytest:
        extra_args += ['--cov', 'vispy', '--no-cov-on-fail']
    extra_arg_string = (' ').join(extra_args)
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
    return_code = run_subprocess(cmd, return_code=True, cwd=cwd, env=env, stdout=None, stderr=None)[2]
    if return_code:
        raise RuntimeError('unit failure (%s)' % return_code)
    if coverage:
        out_name = op.join(cwd, '.vispy-coverage.%s' % mode)
        if op.isfile(out_name):
            os.remove(out_name)
        os.rename(op.join(cwd, '.coverage'), out_name)
    return


def _docs():
    """test docstring paramters
    using vispy/utils/tests/test_docstring_parameters.py"""
    dev = _get_import_dir()[1]
    if not dev:
        warnings.warn("Docstring test imports Vispy from Vispy's installation. It is recommended to setup Vispy using 'python setup.py develop' so that the latest sources are used automatically")
    try:
        from ..util.tests import test_docstring_parameters
        print('Running docstring test...')
        test_docstring_parameters.test_docstring_parameters()
    except AssertionError as docstring_violations:
        raise RuntimeError(docstring_violations)


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
            from flake8.main import main
        except ImportError:
            print('Skipping flake8 test, flake8 not installed')
        else:
            print('Running flake8... ')
            sys.stdout.flush()
            try:
                main()
            except SystemExit as ex:
                if ex.code in (None, 0):
                    pass
                else:
                    raise RuntimeError('flake8 failed')

    finally:
        os.chdir(orig_dir)

    return


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
         len(report), ('\n').join(report)))


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
        if reason is not None:
            msg = 'Skipping example test: %s' % reason
            print(msg)
            raise SkipTest(msg)
        if fnames_str:
            fnames = fnames_str.split(' ')
        else:
            fnames = [ op.join(d[0], fname) for d in os.walk(op.join(import_dir, '..', 'examples')) for fname in d[2] if fname.endswith('.py')
                     ]
        fnames = sorted(fnames, key=lambda x: x.lower())
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
            sys.stdout.flush()
            cwd = op.dirname(fname)
            cmd = [sys.executable, '-c', _script.format(op.split(fname)[1][:-3])]
            sys.stdout.flush()
            stdout, stderr, retcode = run_subprocess(cmd, return_code=True, cwd=cwd, env=os.environ)
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
    return


@nottest
def test(label='full', extra_arg_string='', coverage=False):
    """Test vispy software

    Parameters
    ----------
    label : str
        Can be one of 'full', 'unit', 'nobackend', 'extra', 'lineendings',
        'flake', 'docs', or any backend name (e.g., 'qt').
    extra_arg_string : str
        Extra arguments to sent to ``pytest``.
    coverage : bool
        If True, collect coverage data.
    """
    if label == 'osmesa':
        from ..util.osmesa_gl import fix_osmesa_gl_lib
        fix_osmesa_gl_lib()
    from ..app.backends import BACKEND_NAMES as backend_names
    label = label.lower()
    label = 'pytest' if label == 'nose' else label
    known_types = ['full', 'unit', 'lineendings', 'extra', 'flake',
     'docs', 'nobackend', 'examples']
    if label not in known_types + backend_names:
        raise ValueError("label must be one of %s, or a backend name %s, not '%s'" % (
         known_types, backend_names, label))
    runs = []
    if label in ('full', 'unit'):
        for backend in backend_names:
            runs.append([partial(_unit, backend, extra_arg_string, coverage),
             backend])

    elif label in backend_names:
        runs.append([partial(_unit, label, extra_arg_string, coverage), label])
    if label in ('full', 'unit', 'nobackend'):
        runs.append([partial(_unit, 'nobackend', extra_arg_string, coverage),
         'nobackend'])
    if label == 'examples':
        runs.append([partial(_examples, extra_arg_string),
         'examples'])
    else:
        if label == 'full':
            runs.append([partial(_examples, ''), 'examples'])
        if label in ('full', 'extra', 'lineendings'):
            runs.append([_check_line_endings, 'lineendings'])
        if label in ('full', 'extra', 'flake'):
            runs.append([_flake, 'flake'])
        if label in ('extra', 'docs'):
            runs.append([_docs, 'docs'])
        t0 = time()
        fail = []
        skip = []
        for run in runs:
            try:
                run[0]()
            except RuntimeError as exp:
                print('Failed: %s' % str(exp))
                fail += [run[1]]
            except SkipTest:
                skip += [run[1]]
            except Exception as exp:
                fail += [run[1]]
                print('Failed strangely (%s): %s\n' % (type(exp), str(exp)))
                import traceback
                type_, value, tb = sys.exc_info()
                traceback.print_exception(type_, value, tb)
            else:
                print('Passed\n')

            sys.stdout.flush()

    dt = time() - t0
    stat = '%s failed, %s skipped' % (fail if fail else 0, skip if skip else 0)
    extra = 'failed' if fail else 'succeeded'
    print('Testing %s (%s) in %0.3f seconds' % (extra, stat, dt))
    sys.stdout.flush()
    if len(fail) > 0:
        raise RuntimeError('FAILURE')