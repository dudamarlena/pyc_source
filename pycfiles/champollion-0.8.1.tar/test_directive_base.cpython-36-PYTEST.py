# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jeremyr/dev/perso/champollion/test/unit/directive/test_directive_base.py
# Compiled at: 2018-07-06 19:20:39
# Size of source mod 2**32: 946 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, pytest, os
from sphinx.cmdline import main as sphinx_main
from sphinx.util.osutil import cd

def test_directive_error(doc_folder):
    """Do not generate doc for non existing data.
    """
    js_source = os.path.join(doc_folder, 'example')
    with open(os.path.join(js_source, 'index.js'), 'w') as (f):
        f.write('/**\n * A variable\n *\n * .. note::\n *\n *     A note.\n */\nconst VARIABLE = 42;\n')
    index_file = os.path.join(doc_folder, 'index.rst')
    with open(index_file, 'w') as (f):
        f.write('.. js:autodata:: example.UNEXISTING_VARIABLE')
    with cd(doc_folder):
        sphinx_main(['-c', '.', '-b', 'text', '-E', '.', '_build'])
    with open(os.path.join(doc_folder, '_build', 'index.txt'), 'r') as (f):
        @py_assert1 = f.read
        @py_assert3 = @py_assert1()
        @py_assert6 = ''
        @py_assert5 = @py_assert3 == @py_assert6
        if not @py_assert5:
            @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.read\n}()\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(f) if 'f' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(f) else 'f',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
            @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
            raise AssertionError(@pytest_ar._format_explanation(@py_format10))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None