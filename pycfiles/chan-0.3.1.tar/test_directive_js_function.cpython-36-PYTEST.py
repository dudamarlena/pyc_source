# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/jeremyr/dev/perso/champollion/test/unit/directive/test_directive_js_function.py
# Compiled at: 2018-07-06 19:24:53
# Size of source mod 2**32: 11285 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, pytest, os, re, unicodedata
from sphinx.cmdline import main as sphinx_main
from sphinx.util.osutil import cd

def _sanitise_value(value):
    """Return *value* suitable for comparison using python 2 and python 3.
    """
    value = value.decode('UTF-8')
    value = unicodedata.normalize('NFKD', value)
    value = value.encode('ascii', 'ignore').decode('UTF-8')
    value = re.sub('[^\\w*._\\-\\\\/:% \\"()\\[\\]{}\\n=,]', '', value)
    return value


@pytest.fixture()
def doc_folder_with_code(doc_folder):
    """Return Doc folder with Javascript example source code.
    """
    js_source = os.path.join(doc_folder, 'example')
    with open(os.path.join(js_source, 'index.js'), 'w') as (f):
        f.write("/**\n * A function\n *\n * .. note::\n *\n *     A note.\n */\nexport default function doSomething1(arg1, arg2 = null) {\n    console.log('test1')\n}\n\n/**\n * Another function\n *\n * A citation::\n *\n *     A citation\n */\nconst doSomething2 = (arg) => {\n    console.log('test2')\n};\n\nexport const doSomething3 = () => {};\n\nexport default function() {}\n\n/** generator function */\nconst yieldSomethingAliased = function* yieldSomething(arg) {}\n")
    return doc_folder


def test_directive_autofunction(doc_folder_with_code):
    """Generate documentation from functions.
    """
    index_file = os.path.join(doc_folder_with_code, 'index.rst')
    with open(index_file, 'w') as (f):
        f.write('.. js:autofunction:: example.doSomething1\n\n.. js:autofunction:: example.doSomething2\n\n.. js:autofunction:: example.doSomething3\n\n.. js:autofunction:: example.__ANONYMOUS_FUNCTION__\n\n.. js:autofunction:: example.yieldSomethingAliased\n')
    with cd(doc_folder_with_code):
        sphinx_main(['-c', '.', '-b', 'text', '-E', '.', '_build'])
    with open(os.path.join(doc_folder_with_code, '_build', 'index.txt'), 'rb') as (f):
        content = _sanitise_value(f.read())
        @py_assert2 = 'example.doSomething1(arg1, arg2 = null)\n\n   "import doSomething1 from "example""\n\n   A function\n\n   Note: A note.\n\nexample.doSomething2(arg)\n\n   Another function\n\n   A citation:\n\n      A citation\n\nexample.doSomething3()\n\n   "import {doSomething3} from "example""\n\nexample.__ANONYMOUS_FUNCTION__()\n\nfunction* example.yieldSomethingAliased(arg)\n\n   generator function\n'
        @py_assert1 = content == @py_assert2
        if not @py_assert1:
            @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (content, @py_assert2)) % {'py0':@pytest_ar._saferepr(content) if 'content' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(content) else 'content',  'py3':@pytest_ar._saferepr(@py_assert2)}
            @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert1 = @py_assert2 = None


def test_directive_autofunction_with_alias(doc_folder_with_code):
    """Generate documentation from functions with alias.
    """
    index_file = os.path.join(doc_folder_with_code, 'index.rst')
    with open(index_file, 'w') as (f):
        f.write('.. js:autofunction:: example.doSomething1\n    :alias: aliased_doSomething1\n\n.. js:autofunction:: example.doSomething2\n    :alias: aliased_doSomething2\n\n.. js:autofunction:: example.doSomething3\n    :alias: aliased_doSomething3\n\n.. js:autofunction:: example.__ANONYMOUS_FUNCTION__\n    :alias: alias_anonymous\n\n.. js:autofunction:: example.yieldSomethingAliased\n    :alias: aliased_generate\n')
    with cd(doc_folder_with_code):
        sphinx_main(['-c', '.', '-b', 'text', '-E', '.', '_build'])
    with open(os.path.join(doc_folder_with_code, '_build', 'index.txt'), 'rb') as (f):
        content = _sanitise_value(f.read())
        @py_assert2 = 'example.aliased_doSomething1(arg1, arg2 = null)\n\n   "import aliased_doSomething1 from "example""\n\n   A function\n\n   Note: A note.\n\nexample.aliased_doSomething2(arg)\n\n   Another function\n\n   A citation:\n\n      A citation\n\nexample.aliased_doSomething3()\n\n   "import {aliased_doSomething3} from "example""\n\nexample.alias_anonymous()\n\nfunction* example.aliased_generate(arg)\n\n   generator function\n'
        @py_assert1 = content == @py_assert2
        if not @py_assert1:
            @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (content, @py_assert2)) % {'py0':@pytest_ar._saferepr(content) if 'content' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(content) else 'content',  'py3':@pytest_ar._saferepr(@py_assert2)}
            @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert1 = @py_assert2 = None


def test_directive_autofunction_with_module_alias(doc_folder_with_code):
    """Generate documentation from functions with module alias.
    """
    index_file = os.path.join(doc_folder_with_code, 'index.rst')
    with open(index_file, 'w') as (f):
        f.write('.. js:autofunction:: example.doSomething1\n    :module-alias: alias_module\n\n.. js:autofunction:: example.doSomething2\n    :module-alias: alias_module\n\n.. js:autofunction:: example.doSomething3\n    :module-alias: alias_module\n\n.. js:autofunction:: example.__ANONYMOUS_FUNCTION__\n    :module-alias: alias_module\n\n.. js:autofunction:: example.yieldSomethingAliased\n    :module-alias: alias_module\n')
    with cd(doc_folder_with_code):
        sphinx_main(['-c', '.', '-b', 'text', '-E', '.', '_build'])
    with open(os.path.join(doc_folder_with_code, '_build', 'index.txt'), 'rb') as (f):
        content = _sanitise_value(f.read())
        @py_assert2 = 'alias_module.doSomething1(arg1, arg2 = null)\n\n   "import doSomething1 from "example""\n\n   A function\n\n   Note: A note.\n\nalias_module.doSomething2(arg)\n\n   Another function\n\n   A citation:\n\n      A citation\n\nalias_module.doSomething3()\n\n   "import {doSomething3} from "example""\n\nalias_module.__ANONYMOUS_FUNCTION__()\n\nfunction* alias_module.yieldSomethingAliased(arg)\n\n   generator function\n'
        @py_assert1 = content == @py_assert2
        if not @py_assert1:
            @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (content, @py_assert2)) % {'py0':@pytest_ar._saferepr(content) if 'content' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(content) else 'content',  'py3':@pytest_ar._saferepr(@py_assert2)}
            @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert1 = @py_assert2 = None


def test_directive_autofunction_with_module_path_alias(doc_folder_with_code):
    """Generate documentation from functions with module path alias.
    """
    index_file = os.path.join(doc_folder_with_code, 'index.rst')
    with open(index_file, 'w') as (f):
        f.write('.. js:autofunction:: example.doSomething1\n    :module-path-alias: test/alias/module\n\n.. js:autofunction:: example.doSomething2\n    :module-path-alias: test/alias/module\n\n.. js:autofunction:: example.doSomething3\n    :module-path-alias: test/alias/module\n\n.. js:autofunction:: example.__ANONYMOUS_FUNCTION__\n    :module-path-alias: test/alias/module\n\n.. js:autofunction:: example.yieldSomethingAliased\n    :module-path-alias: test/alias/module\n')
    with cd(doc_folder_with_code):
        sphinx_main(['-c', '.', '-b', 'text', '-E', '.', '_build'])
    with open(os.path.join(doc_folder_with_code, '_build', 'index.txt'), 'rb') as (f):
        content = _sanitise_value(f.read())
        @py_assert2 = 'example.doSomething1(arg1, arg2 = null)\n\n   "import doSomething1 from "test/alias/module""\n\n   A function\n\n   Note: A note.\n\nexample.doSomething2(arg)\n\n   Another function\n\n   A citation:\n\n      A citation\n\nexample.doSomething3()\n\n   "import {doSomething3} from "test/alias/module""\n\nexample.__ANONYMOUS_FUNCTION__()\n\nfunction* example.yieldSomethingAliased(arg)\n\n   generator function\n'
        @py_assert1 = content == @py_assert2
        if not @py_assert1:
            @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (content, @py_assert2)) % {'py0':@pytest_ar._saferepr(content) if 'content' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(content) else 'content',  'py3':@pytest_ar._saferepr(@py_assert2)}
            @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert1 = @py_assert2 = None


def test_directive_autofunction_with_partial_import_forced(doc_folder_with_code):
    """Generate documentation from functions with partial import forced.
    """
    index_file = os.path.join(doc_folder_with_code, 'index.rst')
    with open(index_file, 'w') as (f):
        f.write('.. js:autofunction:: example.doSomething1\n    :force-partial-import:\n\n.. js:autofunction:: example.doSomething2\n    :force-partial-import:\n\n.. js:autofunction:: example.doSomething3\n    :force-partial-import:\n\n.. js:autofunction:: example.__ANONYMOUS_FUNCTION__\n    :force-partial-import:\n\n.. js:autofunction:: example.yieldSomethingAliased\n    :force-partial-import:\n')
    with cd(doc_folder_with_code):
        sphinx_main(['-c', '.', '-b', 'text', '-E', '.', '_build'])
    with open(os.path.join(doc_folder_with_code, '_build', 'index.txt'), 'rb') as (f):
        content = _sanitise_value(f.read())
        @py_assert2 = 'example.doSomething1(arg1, arg2 = null)\n\n   "import {doSomething1} from "example""\n\n   A function\n\n   Note: A note.\n\nexample.doSomething2(arg)\n\n   Another function\n\n   A citation:\n\n      A citation\n\nexample.doSomething3()\n\n   "import {doSomething3} from "example""\n\nexample.__ANONYMOUS_FUNCTION__()\n\nfunction* example.yieldSomethingAliased(arg)\n\n   generator function\n'
        @py_assert1 = content == @py_assert2
        if not @py_assert1:
            @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (content, @py_assert2)) % {'py0':@pytest_ar._saferepr(content) if 'content' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(content) else 'content',  'py3':@pytest_ar._saferepr(@py_assert2)}
            @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert1 = @py_assert2 = None