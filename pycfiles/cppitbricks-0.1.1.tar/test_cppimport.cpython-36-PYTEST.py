# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/tbent/Dropbox/projects/inactive/cppimport/tests/test_cppimport.py
# Compiled at: 2017-12-01 17:03:56
# Size of source mod 2**32: 4020 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, os, io, sys, copy, subprocess, contextlib, cppimport, cppimport.build_module, cppimport.templating, cppimport.import_hook
cppimport.set_quiet(False)

@contextlib.contextmanager
def appended(filename, text):
    orig = open(filename, 'r').read()
    open(filename, 'a').write(text)
    try:
        yield
    finally:
        open(filename, 'w').write(orig)


def subprocess_check(test_code, returncode=0):
    p = subprocess.Popen([
     'python', '-c', test_code],
      cwd=(os.path.dirname(__file__)))
    p.wait()
    @py_assert1 = p.returncode
    @py_assert3 = @py_assert1 == returncode
    if not @py_assert3:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.returncode\n} == %(py4)s', ), (@py_assert1, returncode)) % {'py0':@pytest_ar._saferepr(p) if 'p' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(p) else 'p',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(returncode) if 'returncode' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(returncode) else 'returncode'}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = None


def test_redirected_stream():
    sys.stderr = io.StringIO()
    with cppimport.build_module.stdchannel_redirected('stdout') as (s):
        with cppimport.build_module.stdchannel_redirected('stderr'):
            print('EEEP!')
    @py_assert1 = s.getvalue
    @py_assert3 = @py_assert1()
    @py_assert6 = 'EEEP!\n'
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.getvalue\n}()\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(s) if 's' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(s) else 's',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None


def test_find_module_cpppath():
    mymodule_loc = cppimport.find.find_module_cpppath('mymodule')
    mymodule_dir = os.path.dirname(mymodule_loc)
    @py_assert1 = os.path
    @py_assert3 = @py_assert1.basename
    @py_assert6 = @py_assert3(mymodule_loc)
    @py_assert9 = 'mymodule.cpp'
    @py_assert8 = @py_assert6 == @py_assert9
    if not @py_assert8:
        @py_format11 = @pytest_ar._call_reprcompare(('==', ), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.path\n}.basename\n}(%(py5)s)\n} == %(py10)s', ), (@py_assert6, @py_assert9)) % {'py0':@pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os) else 'os',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py5':@pytest_ar._saferepr(mymodule_loc) if 'mymodule_loc' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mymodule_loc) else 'mymodule_loc',  'py7':@pytest_ar._saferepr(@py_assert6),  'py10':@pytest_ar._saferepr(@py_assert9)}
        @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert1 = @py_assert3 = @py_assert6 = @py_assert8 = @py_assert9 = None
    apackage = cppimport.find.find_module_cpppath('apackage.mymodule')
    apackage_correct = os.path.join(mymodule_dir, 'apackage', 'mymodule.cpp')
    @py_assert1 = apackage == apackage_correct
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (apackage, apackage_correct)) % {'py0':@pytest_ar._saferepr(apackage) if 'apackage' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(apackage) else 'apackage',  'py2':@pytest_ar._saferepr(apackage_correct) if 'apackage_correct' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(apackage_correct) else 'apackage_correct'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None
    inner = cppimport.find.find_module_cpppath('apackage.inner.mymodule')
    inner_correct = os.path.join(mymodule_dir, 'apackage', 'inner', 'mymodule.cpp')
    @py_assert1 = inner == inner_correct
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (inner, inner_correct)) % {'py0':@pytest_ar._saferepr(inner) if 'inner' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(inner) else 'inner',  'py2':@pytest_ar._saferepr(inner_correct) if 'inner_correct' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(inner_correct) else 'inner_correct'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None


def test_get_rendered_source_filepath():
    rendered_path = cppimport.templating.get_rendered_source_filepath('abc.cpp')
    @py_assert2 = '.rendered.abc.cpp'
    @py_assert1 = rendered_path == @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (rendered_path, @py_assert2)) % {'py0':@pytest_ar._saferepr(rendered_path) if 'rendered_path' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(rendered_path) else 'rendered_path',  'py3':@pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None


def module_tester(mod, cheer=False):
    @py_assert1 = mod.add
    @py_assert3 = 1
    @py_assert5 = 2
    @py_assert7 = @py_assert1(@py_assert3, @py_assert5)
    @py_assert10 = 3
    @py_assert9 = @py_assert7 == @py_assert10
    if not @py_assert9:
        @py_format12 = @pytest_ar._call_reprcompare(('==', ), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py2)s\n{%(py2)s = %(py0)s.add\n}(%(py4)s, %(py6)s)\n} == %(py11)s', ), (@py_assert7, @py_assert10)) % {'py0':@pytest_ar._saferepr(mod) if 'mod' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mod) else 'mod',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py11':@pytest_ar._saferepr(@py_assert10)}
        @py_format14 = 'assert %(py13)s' % {'py13': @py_format12}
        raise AssertionError(@pytest_ar._format_explanation(@py_format14))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert10 = None
    if cheer:
        mod.Thing().cheer()


def test_mymodule():
    mymodule = cppimport.imp('mymodule')
    module_tester(mymodule)


def test_package_mymodule():
    mymodule = cppimport.imp('apackage.mymodule')
    module_tester(mymodule)


def test_inner_package_mymodule():
    mymodule = cppimport.imp('apackage.inner.mymodule')
    module_tester(mymodule)


def test_with_file_in_syspath():
    orig_sys_path = copy.copy(sys.path)
    sys.path.append(os.path.join(os.path.dirname(__file__), 'mymodule.cpp'))
    mymodule = cppimport.imp('mymodule')
    sys.path = orig_sys_path


def test_rebuild_after_failed_compile():
    mymodule = cppimport.imp('mymodule')
    test_code = '\nimport cppimport; mymodule = cppimport.imp("mymodule");assert(mymodule.add(1,2) == 3)\n'
    with appended('tests/mymodule.cpp', ';asdf;'):
        subprocess_check(test_code, 1)
    subprocess_check(test_code, 0)


add_to_thing = '\n#include <iostream>\nstruct Thing {\n    void cheer() {\n        std::cout << "WAHHOOOO" << std::endl;\n    }\n};\n#define THING_DEFINED\n'

def test_no_rebuild_if_no_deps_change():
    mymodule = cppimport.imp('mymodule')
    test_code = '\nimport cppimport;\nmymodule = cppimport.imp("mymodule");\nassert(not hasattr(mymodule, \'Thing\'))\n'
    with appended('tests/thing2.h', add_to_thing):
        subprocess_check(test_code)


def test_rebuild_header_after_change():
    mymodule = cppimport.imp('mymodule')
    test_code = '\nimport cppimport; cppimport.set_quiet(False); mymodule = cppimport.imp("mymodule"); mymodule.Thing().cheer()\n'
    with appended('tests/thing.h', add_to_thing):
        subprocess_check(test_code)


def test_raw_extensions():
    raw_extension = cppimport.imp('raw_extension')
    @py_assert1 = raw_extension.add
    @py_assert3 = 1
    @py_assert5 = 2
    @py_assert7 = @py_assert1(@py_assert3, @py_assert5)
    @py_assert10 = 3
    @py_assert9 = @py_assert7 == @py_assert10
    if not @py_assert9:
        @py_format12 = @pytest_ar._call_reprcompare(('==', ), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py2)s\n{%(py2)s = %(py0)s.add\n}(%(py4)s, %(py6)s)\n} == %(py11)s', ), (@py_assert7, @py_assert10)) % {'py0':@pytest_ar._saferepr(raw_extension) if 'raw_extension' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(raw_extension) else 'raw_extension',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py11':@pytest_ar._saferepr(@py_assert10)}
        @py_format14 = 'assert %(py13)s' % {'py13': @py_format12}
        raise AssertionError(@pytest_ar._format_explanation(@py_format14))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert10 = None


def test_extra_sources():
    mod = cppimport.imp('extra_sources')
    @py_assert1 = mod.square_sum
    @py_assert3 = 3
    @py_assert5 = 4
    @py_assert7 = @py_assert1(@py_assert3, @py_assert5)
    @py_assert10 = 25
    @py_assert9 = @py_assert7 == @py_assert10
    if not @py_assert9:
        @py_format12 = @pytest_ar._call_reprcompare(('==', ), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py2)s\n{%(py2)s = %(py0)s.square_sum\n}(%(py4)s, %(py6)s)\n} == %(py11)s', ), (@py_assert7, @py_assert10)) % {'py0':@pytest_ar._saferepr(mod) if 'mod' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mod) else 'mod',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py11':@pytest_ar._saferepr(@py_assert10)}
        @py_format14 = 'assert %(py13)s' % {'py13': @py_format12}
        raise AssertionError(@pytest_ar._format_explanation(@py_format14))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert10 = None


def test_cpprun():
    p = subprocess.Popen([
     'cpprun', '-m', 'free_module.cpp'],
      cwd=(os.path.dirname(__file__)),
      stdout=(subprocess.PIPE))
    p.wait()
    @py_assert0 = 'HI!\n'
    @py_assert4 = p.stdout
    @py_assert6 = @py_assert4.read
    @py_assert8 = @py_assert6()
    @py_assert2 = @py_assert0 == @py_assert8
    if not @py_assert2:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py9)s\n{%(py9)s = %(py7)s\n{%(py7)s = %(py5)s\n{%(py5)s = %(py3)s.stdout\n}.read\n}()\n}', ), (@py_assert0, @py_assert8)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(p) if 'p' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(p) else 'p',  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = None


def test_import_hook():
    cppimport.force_rebuild(True)
    import hook_test
    cppimport.force_rebuild(False)