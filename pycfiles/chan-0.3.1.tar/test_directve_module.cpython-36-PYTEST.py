# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/jeremyr/dev/perso/champollion/test/unit/directive/test_directve_module.py
# Compiled at: 2018-07-06 19:25:28
# Size of source mod 2**32: 25479 bytes
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
        f.write("/**\n * A cool application.\n */\n\nimport {\n    VARIABLE_OBJECT as ALIASED_VARIABLE_OBJECT\n} from './test_attribute';\n\n\nconst undocumentedFunction = (arg) => {\n    console.log(arg)\n};\n\n\n/** A private function */\nfunction _privateFunction(arg) {\n    console.log(arg)\n}\n\nexport ALIASED_VARIABLE_OBJECT;\nexport * from './test_class';\n")
    with open(os.path.join(js_source, 'test_attribute.js'), 'w') as (f):
        f.write("/**\n * A variable\n *\n * .. note::\n *\n *     A note.\n */\nexport const VARIABLE_OBJECT = {\n    key1: 'value1',\n    key2: 'value2',\n    key3: 'value3',\n};\n\n/** Another variable. */\nlet VARIABLE_INT = 42;\n")
    with open(os.path.join(js_source, 'test_class.js'), 'w') as (f):
        f.write("/** A file with a great class. */\n\n\nimport {Element as AliasedElement} from 'wherever';\n\n/**\n * Inherited class\n */\nclass AwesomeClass {\n\n    /**\n     * Constructor.\n     */\n    constructor(name) {\n        super();\n        this.name = name;\n    }\n\n    /**\n     * Get name.\n     *\n     * .. warning::\n     *\n     *     The name is awesome\n     */\n    get name() {\n        return this.name;\n    }\n\n    /**\n     * Set name.\n     *\n     * .. warning::\n     *\n     *     Keep the name awesome\n     */\n    set name(value) {\n        this.name = value;\n    }\n\n    /**\n     * awesomeMethod.\n     */\n    awesomeMethod = () => {\n        console.log('Method has been called');\n    };\n\n    undocumentedMethod(arg1, arg2) {\n        console.log('An un-documented method has been called');\n    }\n\n    /**\n     * Private Method.\n     */\n    _privateMethod(arg1) {\n        console.log('An private method has been called');\n    }\n\n    /**\n     * staticMethod.\n     */\n    static staticMethod() {\n        console.log('Static method has been called');\n    }\n\n    /**\n     * attribute.\n     */\n    static attribute = 42;\n\n    /**\n     * another attribute.\n     */\n    classicAttribute = {\n        test: 'a test',\n    };\n}\n\nexport AliasedElement;\nexport default AwesomeClass;\n")
    return doc_folder


def test_directive_automodule_error(doc_folder_with_code):
    """Do not generate doc for non existing module.
    """
    index_file = os.path.join(doc_folder_with_code, 'index.rst')
    with open(index_file, 'w') as (f):
        f.write('.. js:automodule:: example.wrong')
    with cd(doc_folder_with_code):
        sphinx_main(['-c', '.', '-b', 'text', '-E', '.', '_build'])
    with open(os.path.join(doc_folder_with_code, '_build', 'index.txt'), 'r') as (f):
        @py_assert1 = f.read
        @py_assert3 = @py_assert1()
        @py_assert6 = ''
        @py_assert5 = @py_assert3 == @py_assert6
        if not @py_assert5:
            @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.read\n}()\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(f) if 'f' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(f) else 'f',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
            @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
            raise AssertionError(@pytest_ar._format_explanation(@py_format10))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None


def test_directive_automodule(doc_folder_with_code):
    """Generate documentation from modules.
    """
    index_file = os.path.join(doc_folder_with_code, 'index.rst')
    with open(index_file, 'w') as (f):
        f.write('.. js:automodule:: example\n\n.. js:automodule:: example.test_attribute\n\n.. js:automodule:: example.test_class\n')
    with cd(doc_folder_with_code):
        sphinx_main(['-c', '.', '-b', 'text', '-E', '.', '_build'])
    with open(os.path.join(doc_folder_with_code, '_build', 'index.txt'), 'rb') as (f):
        content = _sanitise_value(f.read())
        @py_assert2 = 'A cool application.\n\nA file with a great class.\n'
        @py_assert1 = content == @py_assert2
        if not @py_assert1:
            @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (content, @py_assert2)) % {'py0':@pytest_ar._saferepr(content) if 'content' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(content) else 'content',  'py3':@pytest_ar._saferepr(@py_assert2)}
            @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert1 = @py_assert2 = None


def test_directive_automodule_with_members(doc_folder_with_code):
    """Generate documentation from modules with members.
    """
    index_file = os.path.join(doc_folder_with_code, 'index.rst')
    with open(index_file, 'w') as (f):
        f.write('.. js:automodule:: example\n    :members:\n\n.. js:automodule:: example.test_attribute\n    :members:\n\n.. js:automodule:: example.test_class\n    :members:\n')
    with cd(doc_folder_with_code):
        sphinx_main(['-c', '.', '-b', 'text', '-E', '.', '_build'])
    with open(os.path.join(doc_folder_with_code, '_build', 'index.txt'), 'rb') as (f):
        content = _sanitise_value(f.read())
        @py_assert2 = 'A cool application.\n\nconst example.ALIASED_VARIABLE_OBJECT = { key1: value1, key2: value2, key3: value3, }\n\n   "import {ALIASED_VARIABLE_OBJECT} from "example""\n\n   A variable\n\n   Note: A note.\n\nclass example.AwesomeClass(name)\n\n   "import {AwesomeClass} from "example""\n\n   Inherited class\n\nconst example.test_attribute.VARIABLE_OBJECT = { key1: value1, key2: value2, key3: value3, }\n\n   "import {VARIABLE_OBJECT} from "example/test_attribute""\n\n   A variable\n\n   Note: A note.\n\nlet example.test_attribute.VARIABLE_INT = 42\n\n   Another variable.\n\nA file with a great class.\n\nclass example.test_class.AwesomeClass(name)\n\n   "import AwesomeClass from "example/test_class""\n\n   Inherited class\n'
        @py_assert1 = content == @py_assert2
        if not @py_assert1:
            @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (content, @py_assert2)) % {'py0':@pytest_ar._saferepr(content) if 'content' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(content) else 'content',  'py3':@pytest_ar._saferepr(@py_assert2)}
            @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert1 = @py_assert2 = None


def test_directive_automodule_with_specific_members(doc_folder_with_code):
    """Generate documentation from modules with specific members.
    """
    index_file = os.path.join(doc_folder_with_code, 'index.rst')
    with open(index_file, 'w') as (f):
        f.write('.. js:automodule:: example.test_attribute\n    :members: VARIABLE_OBJECT\n')
    with cd(doc_folder_with_code):
        sphinx_main(['-c', '.', '-b', 'text', '-E', '.', '_build'])
    with open(os.path.join(doc_folder_with_code, '_build', 'index.txt'), 'rb') as (f):
        content = _sanitise_value(f.read())
        @py_assert2 = 'const example.test_attribute.VARIABLE_OBJECT = { key1: value1, key2: value2, key3: value3, }\n\n   "import {VARIABLE_OBJECT} from "example/test_attribute""\n\n   A variable\n\n   Note: A note.\n'
        @py_assert1 = content == @py_assert2
        if not @py_assert1:
            @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (content, @py_assert2)) % {'py0':@pytest_ar._saferepr(content) if 'content' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(content) else 'content',  'py3':@pytest_ar._saferepr(@py_assert2)}
            @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert1 = @py_assert2 = None


def test_directive_automodule_with_undocumented_members(doc_folder_with_code):
    """Generate documentation from modules with undocumented members.
    """
    index_file = os.path.join(doc_folder_with_code, 'index.rst')
    with open(index_file, 'w') as (f):
        f.write('.. js:automodule:: example\n    :members:\n    :undoc-members:\n\n.. js:automodule:: example.test_attribute\n    :members:\n    :undoc-members:\n\n.. js:automodule:: example.test_class\n    :members:\n    :undoc-members:\n')
    with cd(doc_folder_with_code):
        sphinx_main(['-c', '.', '-b', 'text', '-E', '.', '_build'])
    with open(os.path.join(doc_folder_with_code, '_build', 'index.txt'), 'rb') as (f):
        content = _sanitise_value(f.read())
        @py_assert2 = 'A cool application.\n\nexample.undocumentedFunction(arg)\n\nconst example.ALIASED_VARIABLE_OBJECT = { key1: value1, key2: value2, key3: value3, }\n\n   "import {ALIASED_VARIABLE_OBJECT} from "example""\n\n   A variable\n\n   Note: A note.\n\nclass example.AwesomeClass(name)\n\n   "import {AwesomeClass} from "example""\n\n   Inherited class\n\nconst example.test_attribute.VARIABLE_OBJECT = { key1: value1, key2: value2, key3: value3, }\n\n   "import {VARIABLE_OBJECT} from "example/test_attribute""\n\n   A variable\n\n   Note: A note.\n\nlet example.test_attribute.VARIABLE_INT = 42\n\n   Another variable.\n\nA file with a great class.\n\nclass example.test_class.AwesomeClass(name)\n\n   "import AwesomeClass from "example/test_class""\n\n   Inherited class\n'
        @py_assert1 = content == @py_assert2
        if not @py_assert1:
            @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (content, @py_assert2)) % {'py0':@pytest_ar._saferepr(content) if 'content' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(content) else 'content',  'py3':@pytest_ar._saferepr(@py_assert2)}
            @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert1 = @py_assert2 = None


def test_directive_automodule_with_undocumented_members_default(doc_folder_with_code):
    """Generate documentation from modules with undocumented members by default.
    """
    conf_file = os.path.join(doc_folder_with_code, 'conf.py')
    with open(conf_file, 'a') as (f):
        f.write("\njs_module_options = ['undoc-members']")
    index_file = os.path.join(doc_folder_with_code, 'index.rst')
    with open(index_file, 'w') as (f):
        f.write('.. js:automodule:: example\n    :members:\n\n.. js:automodule:: example.test_attribute\n    :members:\n\n.. js:automodule:: example.test_class\n    :members:\n')
    with cd(doc_folder_with_code):
        sphinx_main(['-c', '.', '-b', 'text', '-E', '.', '_build'])
    with open(os.path.join(doc_folder_with_code, '_build', 'index.txt'), 'rb') as (f):
        content = _sanitise_value(f.read())
        @py_assert2 = 'A cool application.\n\nexample.undocumentedFunction(arg)\n\nconst example.ALIASED_VARIABLE_OBJECT = { key1: value1, key2: value2, key3: value3, }\n\n   "import {ALIASED_VARIABLE_OBJECT} from "example""\n\n   A variable\n\n   Note: A note.\n\nclass example.AwesomeClass(name)\n\n   "import {AwesomeClass} from "example""\n\n   Inherited class\n\nconst example.test_attribute.VARIABLE_OBJECT = { key1: value1, key2: value2, key3: value3, }\n\n   "import {VARIABLE_OBJECT} from "example/test_attribute""\n\n   A variable\n\n   Note: A note.\n\nlet example.test_attribute.VARIABLE_INT = 42\n\n   Another variable.\n\nA file with a great class.\n\nclass example.test_class.AwesomeClass(name)\n\n   "import AwesomeClass from "example/test_class""\n\n   Inherited class\n'
        @py_assert1 = content == @py_assert2
        if not @py_assert1:
            @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (content, @py_assert2)) % {'py0':@pytest_ar._saferepr(content) if 'content' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(content) else 'content',  'py3':@pytest_ar._saferepr(@py_assert2)}
            @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert1 = @py_assert2 = None


def test_directive_automodule_with_private_members(doc_folder_with_code):
    """Generate documentation from modules with private members.
    """
    index_file = os.path.join(doc_folder_with_code, 'index.rst')
    with open(index_file, 'w') as (f):
        f.write('.. js:automodule:: example\n    :members:\n    :private-members:\n\n.. js:automodule:: example.test_attribute\n    :members:\n    :private-members:\n\n.. js:automodule:: example.test_class\n    :members:\n    :private-members:\n')
    with cd(doc_folder_with_code):
        sphinx_main(['-c', '.', '-b', 'text', '-E', '.', '_build'])
    with open(os.path.join(doc_folder_with_code, '_build', 'index.txt'), 'rb') as (f):
        content = _sanitise_value(f.read())
        @py_assert2 = 'A cool application.\n\nexample._privateFunction(arg)\n\n   A private function\n\nconst example.ALIASED_VARIABLE_OBJECT = { key1: value1, key2: value2, key3: value3, }\n\n   "import {ALIASED_VARIABLE_OBJECT} from "example""\n\n   A variable\n\n   Note: A note.\n\nclass example.AwesomeClass(name)\n\n   "import {AwesomeClass} from "example""\n\n   Inherited class\n\nconst example.test_attribute.VARIABLE_OBJECT = { key1: value1, key2: value2, key3: value3, }\n\n   "import {VARIABLE_OBJECT} from "example/test_attribute""\n\n   A variable\n\n   Note: A note.\n\nlet example.test_attribute.VARIABLE_INT = 42\n\n   Another variable.\n\nA file with a great class.\n\nclass example.test_class.AwesomeClass(name)\n\n   "import AwesomeClass from "example/test_class""\n\n   Inherited class\n'
        @py_assert1 = content == @py_assert2
        if not @py_assert1:
            @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (content, @py_assert2)) % {'py0':@pytest_ar._saferepr(content) if 'content' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(content) else 'content',  'py3':@pytest_ar._saferepr(@py_assert2)}
            @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert1 = @py_assert2 = None


def test_directive_automodule_with_private_members_default(doc_folder_with_code):
    """Generate documentation from modules with private members by default.
    """
    conf_file = os.path.join(doc_folder_with_code, 'conf.py')
    with open(conf_file, 'a') as (f):
        f.write("\njs_module_options = ['private-members']")
    index_file = os.path.join(doc_folder_with_code, 'index.rst')
    with open(index_file, 'w') as (f):
        f.write('.. js:automodule:: example\n    :members:\n\n.. js:automodule:: example.test_attribute\n    :members:\n\n.. js:automodule:: example.test_class\n    :members:\n')
    with cd(doc_folder_with_code):
        sphinx_main(['-c', '.', '-b', 'text', '-E', '.', '_build'])
    with open(os.path.join(doc_folder_with_code, '_build', 'index.txt'), 'rb') as (f):
        content = _sanitise_value(f.read())
        @py_assert2 = 'A cool application.\n\nexample._privateFunction(arg)\n\n   A private function\n\nconst example.ALIASED_VARIABLE_OBJECT = { key1: value1, key2: value2, key3: value3, }\n\n   "import {ALIASED_VARIABLE_OBJECT} from "example""\n\n   A variable\n\n   Note: A note.\n\nclass example.AwesomeClass(name)\n\n   "import {AwesomeClass} from "example""\n\n   Inherited class\n\nconst example.test_attribute.VARIABLE_OBJECT = { key1: value1, key2: value2, key3: value3, }\n\n   "import {VARIABLE_OBJECT} from "example/test_attribute""\n\n   A variable\n\n   Note: A note.\n\nlet example.test_attribute.VARIABLE_INT = 42\n\n   Another variable.\n\nA file with a great class.\n\nclass example.test_class.AwesomeClass(name)\n\n   "import AwesomeClass from "example/test_class""\n\n   Inherited class\n'
        @py_assert1 = content == @py_assert2
        if not @py_assert1:
            @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (content, @py_assert2)) % {'py0':@pytest_ar._saferepr(content) if 'content' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(content) else 'content',  'py3':@pytest_ar._saferepr(@py_assert2)}
            @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert1 = @py_assert2 = None


def test_directive_automodule_with_module_alias(doc_folder_with_code):
    """Generate documentation from modules with module alias.
    """
    index_file = os.path.join(doc_folder_with_code, 'index.rst')
    with open(index_file, 'w') as (f):
        f.write('.. js:automodule:: example\n    :members:\n    :module-alias: alias_module\n\n.. js:automodule:: example.test_attribute\n    :members:\n    :module-alias: alias_module\n\n.. js:automodule:: example.test_class\n    :members:\n    :module-alias: alias_module\n')
    with cd(doc_folder_with_code):
        sphinx_main(['-c', '.', '-b', 'text', '-E', '.', '_build'])
    with open(os.path.join(doc_folder_with_code, '_build', 'index.txt'), 'rb') as (f):
        content = _sanitise_value(f.read())
        @py_assert2 = 'A cool application.\n\nconst alias_module.ALIASED_VARIABLE_OBJECT = { key1: value1, key2: value2, key3: value3, }\n\n   "import {ALIASED_VARIABLE_OBJECT} from "example""\n\n   A variable\n\n   Note: A note.\n\nclass alias_module.AwesomeClass(name)\n\n   "import {AwesomeClass} from "example""\n\n   Inherited class\n\nconst alias_module.VARIABLE_OBJECT = { key1: value1, key2: value2, key3: value3, }\n\n   "import {VARIABLE_OBJECT} from "example/test_attribute""\n\n   A variable\n\n   Note: A note.\n\nlet alias_module.VARIABLE_INT = 42\n\n   Another variable.\n\nA file with a great class.\n\nclass alias_module.AwesomeClass(name)\n\n   "import AwesomeClass from "example/test_class""\n\n   Inherited class\n'
        @py_assert1 = content == @py_assert2
        if not @py_assert1:
            @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (content, @py_assert2)) % {'py0':@pytest_ar._saferepr(content) if 'content' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(content) else 'content',  'py3':@pytest_ar._saferepr(@py_assert2)}
            @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert1 = @py_assert2 = None


def test_directive_automodule_with_module_path_alias(doc_folder_with_code):
    """Generate documentation from modules with module path alias.
    """
    index_file = os.path.join(doc_folder_with_code, 'index.rst')
    with open(index_file, 'w') as (f):
        f.write('.. js:automodule:: example\n    :members:\n    :module-path-alias: alias/module\n\n.. js:automodule:: example.test_attribute\n    :members:\n    :module-path-alias: alias/module\n\n.. js:automodule:: example.test_class\n    :members:\n    :module-path-alias: alias/module\n')
    with cd(doc_folder_with_code):
        sphinx_main(['-c', '.', '-b', 'text', '-E', '.', '_build'])
    with open(os.path.join(doc_folder_with_code, '_build', 'index.txt'), 'rb') as (f):
        content = _sanitise_value(f.read())
        @py_assert2 = 'A cool application.\n\nconst example.ALIASED_VARIABLE_OBJECT = { key1: value1, key2: value2, key3: value3, }\n\n   "import {ALIASED_VARIABLE_OBJECT} from "alias/module""\n\n   A variable\n\n   Note: A note.\n\nclass example.AwesomeClass(name)\n\n   "import {AwesomeClass} from "alias/module""\n\n   Inherited class\n\nconst example.test_attribute.VARIABLE_OBJECT = { key1: value1, key2: value2, key3: value3, }\n\n   "import {VARIABLE_OBJECT} from "alias/module""\n\n   A variable\n\n   Note: A note.\n\nlet example.test_attribute.VARIABLE_INT = 42\n\n   Another variable.\n\nA file with a great class.\n\nclass example.test_class.AwesomeClass(name)\n\n   "import AwesomeClass from "alias/module""\n\n   Inherited class\n'
        @py_assert1 = content == @py_assert2
        if not @py_assert1:
            @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (content, @py_assert2)) % {'py0':@pytest_ar._saferepr(content) if 'content' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(content) else 'content',  'py3':@pytest_ar._saferepr(@py_assert2)}
            @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert1 = @py_assert2 = None


def test_directive_automodule_with_partial_import_forced(doc_folder_with_code):
    """Generate documentation from modules with partial import forced.
    """
    index_file = os.path.join(doc_folder_with_code, 'index.rst')
    with open(index_file, 'w') as (f):
        f.write('.. js:automodule:: example\n    :members:\n    :force-partial-import:\n\n.. js:automodule:: example.test_attribute\n    :members:\n    :force-partial-import:\n\n.. js:automodule:: example.test_class\n    :members:\n    :force-partial-import:\n')
    with cd(doc_folder_with_code):
        sphinx_main(['-c', '.', '-b', 'text', '-E', '.', '_build'])
    with open(os.path.join(doc_folder_with_code, '_build', 'index.txt'), 'rb') as (f):
        content = _sanitise_value(f.read())
        @py_assert2 = 'A cool application.\n\nconst example.ALIASED_VARIABLE_OBJECT = { key1: value1, key2: value2, key3: value3, }\n\n   "import {ALIASED_VARIABLE_OBJECT} from "example""\n\n   A variable\n\n   Note: A note.\n\nclass example.AwesomeClass(name)\n\n   "import {AwesomeClass} from "example""\n\n   Inherited class\n\nconst example.test_attribute.VARIABLE_OBJECT = { key1: value1, key2: value2, key3: value3, }\n\n   "import {VARIABLE_OBJECT} from "example/test_attribute""\n\n   A variable\n\n   Note: A note.\n\nlet example.test_attribute.VARIABLE_INT = 42\n\n   Another variable.\n\nA file with a great class.\n\nclass example.test_class.AwesomeClass(name)\n\n   "import {AwesomeClass} from "example/test_class""\n\n   Inherited class\n'
        @py_assert1 = content == @py_assert2
        if not @py_assert1:
            @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (content, @py_assert2)) % {'py0':@pytest_ar._saferepr(content) if 'content' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(content) else 'content',  'py3':@pytest_ar._saferepr(@py_assert2)}
            @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert1 = @py_assert2 = None