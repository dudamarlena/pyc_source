# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jeremyr/dev/perso/champollion/test/unit/directive/test_directive_js_class.py
# Compiled at: 2018-07-06 19:24:10
# Size of source mod 2**32: 26993 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, pytest, os, re, unicodedata
from sphinx.cmdline import main as sphinx_main
from sphinx.util.osutil import cd

def _sanitise_value(value):
    """Return *value* suitable for comparison using python 2 and python 3.
    """
    value = value.decode('UTF-8')
    value = unicodedata.normalize('NFKD', value)
    value = value.encode('ascii', 'ignore').decode('UTF-8')
    value = re.sub('[^\\w._\\-\\\\/:% \\"()\\[\\]{}\\n=,]', '', value)
    return value


@pytest.fixture()
def doc_folder_with_code(doc_folder):
    """Return Doc folder with Javascript example source code.
    """
    js_source = os.path.join(doc_folder, 'example')
    with open(os.path.join(js_source, 'index.js'), 'w') as (f):
        f.write("/**\n * Base Class\n */\nclass MotherClass {\n    constructor() {\n        this.attribute = 42\n    }\n}\n\nconst CustomWelcome = class Welcome {\n    greeting() {\n        return 'Hello World';\n    }\n};\n\n/**\n * Inherited class\n */\nexport default class AwesomeClass extends MotherClass {\n\n    /**\n     * Constructor.\n     */\n    constructor(name) {\n        super();\n        this.name = name;\n    }\n\n    /**\n     * Get name.\n     *\n     * .. warning::\n     *\n     *     The name is awesome\n     */\n    get name() {\n        return this.name;\n    }\n\n    /**\n     * Set name.\n     *\n     * .. warning::\n     *\n     *     Keep the name awesome\n     */\n    set name(value) {\n        this.name = value;\n    }\n\n    /**\n     * awesomeMethod.\n     */\n    awesomeMethod = () => {\n        console.log('Method has been called');\n    };\n\n    undocumentedMethod(arg1, arg2) {\n        console.log('An un-documented method has been called');\n    }\n\n    /**\n     * Private Method.\n     */\n    _privateMethod(arg1) {\n        console.log('An private method has been called');\n    }\n\n    /**\n     * staticMethod.\n     */\n    static staticMethod() {\n        console.log('Static method has been called');\n    }\n\n    /**\n     * attribute.\n     */\n    static attribute = 42;\n\n    /**\n     * another attribute.\n     */\n    classicAttribute = {\n        test: 'a test',\n    };\n}\n")
    return doc_folder


def test_directive_autoclass(doc_folder_with_code):
    """Generate documentation from classes.
    """
    index_file = os.path.join(doc_folder_with_code, 'index.rst')
    with open(index_file, 'w') as (f):
        f.write('.. js:autoclass:: example.MotherClass\n\n.. js:autoclass:: example.CustomWelcome\n\n.. js:autoclass:: example.AwesomeClass\n')
    with cd(doc_folder_with_code):
        sphinx_main(['-c', '.', '-b', 'text', '-E', '.', '_build'])
    with open(os.path.join(doc_folder_with_code, '_build', 'index.txt'), 'rb') as (f):
        content = _sanitise_value(f.read())
        @py_assert2 = 'class example.MotherClass()\n\n   Base Class\n\nclass example.CustomWelcome()\n\nclass example.AwesomeClass(name)\n\n   "import AwesomeClass from "example""\n\n   Inherited class\n'
        @py_assert1 = content == @py_assert2
        if not @py_assert1:
            @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (content, @py_assert2)) % {'py0':@pytest_ar._saferepr(content) if 'content' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(content) else 'content',  'py3':@pytest_ar._saferepr(@py_assert2)}
            @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert1 = @py_assert2 = None


def test_directive_autoclass_with_members(doc_folder_with_code):
    """Generate documentation from classes with all members.
    """
    index_file = os.path.join(doc_folder_with_code, 'index.rst')
    with open(index_file, 'w') as (f):
        f.write('.. js:autoclass:: example.MotherClass\n    :members:\n\n.. js:autoclass:: example.CustomWelcome\n    :members:\n\n.. js:autoclass:: example.AwesomeClass\n    :members:\n')
    with cd(doc_folder_with_code):
        sphinx_main(['-c', '.', '-b', 'text', '-E', '.', '_build'])
    with open(os.path.join(doc_folder_with_code, '_build', 'index.txt'), 'rb') as (f):
        content = _sanitise_value(f.read())
        @py_assert2 = 'class example.MotherClass()\n\n   Base Class\n\nclass example.CustomWelcome()\n\nclass example.AwesomeClass(name)\n\n   "import AwesomeClass from "example""\n\n   Inherited class\n\n   constructor(name)\n\n      Constructor.\n\n   get name()\n\n      Get name.\n\n      Warning: The name is awesome\n\n   set name(value)\n\n      Set name.\n\n      Warning: Keep the name awesome\n\n   awesomeMethod()\n\n      awesomeMethod.\n\n   static staticMethod()\n\n      staticMethod.\n\n   static attribute = 42\n\n      attribute.\n\n   classicAttribute = { test: a test, }\n\n      another attribute.\n'
        @py_assert1 = content == @py_assert2
        if not @py_assert1:
            @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (content, @py_assert2)) % {'py0':@pytest_ar._saferepr(content) if 'content' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(content) else 'content',  'py3':@pytest_ar._saferepr(@py_assert2)}
            @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert1 = @py_assert2 = None


def test_directive_autoclass_with_specific_members(doc_folder_with_code):
    """Generate documentation from classes with specific members.
    """
    index_file = os.path.join(doc_folder_with_code, 'index.rst')
    with open(index_file, 'w') as (f):
        f.write('.. js:autoclass:: example.AwesomeClass\n    :members: name, awesomeMethod\n')
    with cd(doc_folder_with_code):
        sphinx_main(['-c', '.', '-b', 'text', '-E', '.', '_build'])
    with open(os.path.join(doc_folder_with_code, '_build', 'index.txt'), 'rb') as (f):
        content = _sanitise_value(f.read())
        @py_assert2 = 'class example.AwesomeClass(name)\n\n   "import AwesomeClass from "example""\n\n   Inherited class\n\n   get name()\n\n      Get name.\n\n      Warning: The name is awesome\n\n   set name(value)\n\n      Set name.\n\n      Warning: Keep the name awesome\n\n   awesomeMethod()\n\n      awesomeMethod.\n'
        @py_assert1 = content == @py_assert2
        if not @py_assert1:
            @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (content, @py_assert2)) % {'py0':@pytest_ar._saferepr(content) if 'content' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(content) else 'content',  'py3':@pytest_ar._saferepr(@py_assert2)}
            @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert1 = @py_assert2 = None


def test_directive_autoclass_with_default_members(doc_folder_with_code):
    """Generate documentation from classes with all members by default.
    """
    conf_file = os.path.join(doc_folder_with_code, 'conf.py')
    with open(conf_file, 'a') as (f):
        f.write("\njs_class_options = ['members']")
    index_file = os.path.join(doc_folder_with_code, 'index.rst')
    with open(index_file, 'w') as (f):
        f.write('.. js:autoclass:: example.MotherClass\n\n.. js:autoclass:: example.CustomWelcome\n\n.. js:autoclass:: example.AwesomeClass\n')
    with cd(doc_folder_with_code):
        sphinx_main(['-c', '.', '-b', 'text', '-E', '.', '_build'])
    with open(os.path.join(doc_folder_with_code, '_build', 'index.txt'), 'rb') as (f):
        content = _sanitise_value(f.read())
        @py_assert2 = 'class example.MotherClass()\n\n   Base Class\n\nclass example.CustomWelcome()\n\nclass example.AwesomeClass(name)\n\n   "import AwesomeClass from "example""\n\n   Inherited class\n\n   constructor(name)\n\n      Constructor.\n\n   get name()\n\n      Get name.\n\n      Warning: The name is awesome\n\n   set name(value)\n\n      Set name.\n\n      Warning: Keep the name awesome\n\n   awesomeMethod()\n\n      awesomeMethod.\n\n   static staticMethod()\n\n      staticMethod.\n\n   static attribute = 42\n\n      attribute.\n\n   classicAttribute = { test: a test, }\n\n      another attribute.\n'
        @py_assert1 = content == @py_assert2
        if not @py_assert1:
            @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (content, @py_assert2)) % {'py0':@pytest_ar._saferepr(content) if 'content' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(content) else 'content',  'py3':@pytest_ar._saferepr(@py_assert2)}
            @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert1 = @py_assert2 = None


def test_directive_autoclass_without_constructor(doc_folder_with_code):
    """Generate documentation from classes without constructors.
    """
    index_file = os.path.join(doc_folder_with_code, 'index.rst')
    with open(index_file, 'w') as (f):
        f.write('.. js:autoclass:: example.AwesomeClass\n    :members:\n    :skip-constructor:\n')
    with cd(doc_folder_with_code):
        sphinx_main(['-c', '.', '-b', 'text', '-E', '.', '_build'])
    with open(os.path.join(doc_folder_with_code, '_build', 'index.txt'), 'rb') as (f):
        content = _sanitise_value(f.read())
        @py_assert2 = 'class example.AwesomeClass(name)\n\n   "import AwesomeClass from "example""\n\n   Inherited class\n\n   get name()\n\n      Get name.\n\n      Warning: The name is awesome\n\n   set name(value)\n\n      Set name.\n\n      Warning: Keep the name awesome\n\n   awesomeMethod()\n\n      awesomeMethod.\n\n   static staticMethod()\n\n      staticMethod.\n\n   static attribute = 42\n\n      attribute.\n\n   classicAttribute = { test: a test, }\n\n      another attribute.\n'
        @py_assert1 = content == @py_assert2
        if not @py_assert1:
            @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (content, @py_assert2)) % {'py0':@pytest_ar._saferepr(content) if 'content' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(content) else 'content',  'py3':@pytest_ar._saferepr(@py_assert2)}
            @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert1 = @py_assert2 = None


def test_directive_autoclass_without_constructor_default(doc_folder_with_code):
    """Generate documentation from classes without constructors by default.
    """
    conf_file = os.path.join(doc_folder_with_code, 'conf.py')
    with open(conf_file, 'a') as (f):
        f.write("\njs_class_options = ['skip-constructor']")
    index_file = os.path.join(doc_folder_with_code, 'index.rst')
    with open(index_file, 'w') as (f):
        f.write('.. js:autoclass:: example.AwesomeClass\n    :members:\n')
    with cd(doc_folder_with_code):
        sphinx_main(['-c', '.', '-b', 'text', '-E', '.', '_build'])
    with open(os.path.join(doc_folder_with_code, '_build', 'index.txt'), 'rb') as (f):
        content = _sanitise_value(f.read())
        @py_assert2 = 'class example.AwesomeClass(name)\n\n   "import AwesomeClass from "example""\n\n   Inherited class\n\n   get name()\n\n      Get name.\n\n      Warning: The name is awesome\n\n   set name(value)\n\n      Set name.\n\n      Warning: Keep the name awesome\n\n   awesomeMethod()\n\n      awesomeMethod.\n\n   static staticMethod()\n\n      staticMethod.\n\n   static attribute = 42\n\n      attribute.\n\n   classicAttribute = { test: a test, }\n\n      another attribute.\n'
        @py_assert1 = content == @py_assert2
        if not @py_assert1:
            @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (content, @py_assert2)) % {'py0':@pytest_ar._saferepr(content) if 'content' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(content) else 'content',  'py3':@pytest_ar._saferepr(@py_assert2)}
            @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert1 = @py_assert2 = None


def test_directive_autoclass_with_undocumented_members(doc_folder_with_code):
    """Generate documentation from classes with undocumented members.
    """
    index_file = os.path.join(doc_folder_with_code, 'index.rst')
    with open(index_file, 'w') as (f):
        f.write('.. js:autoclass:: example.MotherClass\n    :members:\n    :undoc-members:\n\n.. js:autoclass:: example.CustomWelcome\n    :members:\n    :undoc-members:\n\n.. js:autoclass:: example.AwesomeClass\n    :members:\n    :undoc-members:\n')
    with cd(doc_folder_with_code):
        sphinx_main(['-c', '.', '-b', 'text', '-E', '.', '_build'])
    with open(os.path.join(doc_folder_with_code, '_build', 'index.txt'), 'rb') as (f):
        content = _sanitise_value(f.read())
        @py_assert2 = 'class example.MotherClass()\n\n   Base Class\n\n   constructor()\n\nclass example.CustomWelcome()\n\n   greeting()\n\nclass example.AwesomeClass(name)\n\n   "import AwesomeClass from "example""\n\n   Inherited class\n\n   constructor(name)\n\n      Constructor.\n\n   get name()\n\n      Get name.\n\n      Warning: The name is awesome\n\n   set name(value)\n\n      Set name.\n\n      Warning: Keep the name awesome\n\n   awesomeMethod()\n\n      awesomeMethod.\n\n   undocumentedMethod(arg1, arg2)\n\n   static staticMethod()\n\n      staticMethod.\n\n   static attribute = 42\n\n      attribute.\n\n   classicAttribute = { test: a test, }\n\n      another attribute.\n'
        @py_assert1 = content == @py_assert2
        if not @py_assert1:
            @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (content, @py_assert2)) % {'py0':@pytest_ar._saferepr(content) if 'content' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(content) else 'content',  'py3':@pytest_ar._saferepr(@py_assert2)}
            @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert1 = @py_assert2 = None


def test_directive_autoclass_with_undoc_members_default(doc_folder_with_code):
    """Generate documentation from classes with undocumented members
    by default.
    """
    conf_file = os.path.join(doc_folder_with_code, 'conf.py')
    with open(conf_file, 'a') as (f):
        f.write("\njs_class_options = ['undoc-members']")
    index_file = os.path.join(doc_folder_with_code, 'index.rst')
    with open(index_file, 'w') as (f):
        f.write('.. js:autoclass:: example.MotherClass\n    :members:\n\n.. js:autoclass:: example.CustomWelcome\n    :members:\n\n.. js:autoclass:: example.AwesomeClass\n    :members:\n')
    with cd(doc_folder_with_code):
        sphinx_main(['-c', '.', '-b', 'text', '-E', '.', '_build'])
    with open(os.path.join(doc_folder_with_code, '_build', 'index.txt'), 'rb') as (f):
        content = _sanitise_value(f.read())
        @py_assert2 = 'class example.MotherClass()\n\n   Base Class\n\n   constructor()\n\nclass example.CustomWelcome()\n\n   greeting()\n\nclass example.AwesomeClass(name)\n\n   "import AwesomeClass from "example""\n\n   Inherited class\n\n   constructor(name)\n\n      Constructor.\n\n   get name()\n\n      Get name.\n\n      Warning: The name is awesome\n\n   set name(value)\n\n      Set name.\n\n      Warning: Keep the name awesome\n\n   awesomeMethod()\n\n      awesomeMethod.\n\n   undocumentedMethod(arg1, arg2)\n\n   static staticMethod()\n\n      staticMethod.\n\n   static attribute = 42\n\n      attribute.\n\n   classicAttribute = { test: a test, }\n\n      another attribute.\n'
        @py_assert1 = content == @py_assert2
        if not @py_assert1:
            @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (content, @py_assert2)) % {'py0':@pytest_ar._saferepr(content) if 'content' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(content) else 'content',  'py3':@pytest_ar._saferepr(@py_assert2)}
            @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert1 = @py_assert2 = None


def test_directive_autoclass_with_private_members(doc_folder_with_code):
    """Generate documentation from classes with private members.
    """
    index_file = os.path.join(doc_folder_with_code, 'index.rst')
    with open(index_file, 'w') as (f):
        f.write('.. js:autoclass:: example.AwesomeClass\n    :members:\n    :private-members:\n')
    with cd(doc_folder_with_code):
        sphinx_main(['-c', '.', '-b', 'text', '-E', '.', '_build'])
    with open(os.path.join(doc_folder_with_code, '_build', 'index.txt'), 'rb') as (f):
        content = _sanitise_value(f.read())
        @py_assert2 = 'class example.AwesomeClass(name)\n\n   "import AwesomeClass from "example""\n\n   Inherited class\n\n   constructor(name)\n\n      Constructor.\n\n   get name()\n\n      Get name.\n\n      Warning: The name is awesome\n\n   set name(value)\n\n      Set name.\n\n      Warning: Keep the name awesome\n\n   awesomeMethod()\n\n      awesomeMethod.\n\n   _privateMethod(arg1)\n\n      Private Method.\n\n   static staticMethod()\n\n      staticMethod.\n\n   static attribute = 42\n\n      attribute.\n\n   classicAttribute = { test: a test, }\n\n      another attribute.\n'
        @py_assert1 = content == @py_assert2
        if not @py_assert1:
            @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (content, @py_assert2)) % {'py0':@pytest_ar._saferepr(content) if 'content' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(content) else 'content',  'py3':@pytest_ar._saferepr(@py_assert2)}
            @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert1 = @py_assert2 = None


def test_directive_autoclass_with_private_members_default(doc_folder_with_code):
    """Generate documentation from classes with private members by default.
    """
    conf_file = os.path.join(doc_folder_with_code, 'conf.py')
    with open(conf_file, 'a') as (f):
        f.write("\njs_class_options = ['private-members']")
    index_file = os.path.join(doc_folder_with_code, 'index.rst')
    with open(index_file, 'w') as (f):
        f.write('.. js:autoclass:: example.AwesomeClass\n    :members:\n')
    with cd(doc_folder_with_code):
        sphinx_main(['-c', '.', '-b', 'text', '-E', '.', '_build'])
    with open(os.path.join(doc_folder_with_code, '_build', 'index.txt'), 'rb') as (f):
        content = _sanitise_value(f.read())
        @py_assert2 = 'class example.AwesomeClass(name)\n\n   "import AwesomeClass from "example""\n\n   Inherited class\n\n   constructor(name)\n\n      Constructor.\n\n   get name()\n\n      Get name.\n\n      Warning: The name is awesome\n\n   set name(value)\n\n      Set name.\n\n      Warning: Keep the name awesome\n\n   awesomeMethod()\n\n      awesomeMethod.\n\n   _privateMethod(arg1)\n\n      Private Method.\n\n   static staticMethod()\n\n      staticMethod.\n\n   static attribute = 42\n\n      attribute.\n\n   classicAttribute = { test: a test, }\n\n      another attribute.\n'
        @py_assert1 = content == @py_assert2
        if not @py_assert1:
            @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (content, @py_assert2)) % {'py0':@pytest_ar._saferepr(content) if 'content' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(content) else 'content',  'py3':@pytest_ar._saferepr(@py_assert2)}
            @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert1 = @py_assert2 = None


def test_directive_autoclass_with_alias(doc_folder_with_code):
    """Generate documentation from classes with alias.
    """
    index_file = os.path.join(doc_folder_with_code, 'index.rst')
    with open(index_file, 'w') as (f):
        f.write('.. js:autoclass:: example.MotherClass\n    :alias: AliasedMotherClass\n\n.. js:autoclass:: example.CustomWelcome\n    :alias: AliasedCustomWelcome\n\n.. js:autoclass:: example.AwesomeClass\n    :alias: AliasedAwesomeClass\n')
    with cd(doc_folder_with_code):
        sphinx_main(['-c', '.', '-b', 'text', '-E', '.', '_build'])
    with open(os.path.join(doc_folder_with_code, '_build', 'index.txt'), 'rb') as (f):
        content = _sanitise_value(f.read())
        @py_assert2 = 'class example.AliasedMotherClass()\n\n   Base Class\n\nclass example.AliasedCustomWelcome()\n\nclass example.AliasedAwesomeClass(name)\n\n   "import AliasedAwesomeClass from "example""\n\n   Inherited class\n'
        @py_assert1 = content == @py_assert2
        if not @py_assert1:
            @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (content, @py_assert2)) % {'py0':@pytest_ar._saferepr(content) if 'content' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(content) else 'content',  'py3':@pytest_ar._saferepr(@py_assert2)}
            @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert1 = @py_assert2 = None


def test_directive_autoclass_with_module_alias(doc_folder_with_code):
    """Generate documentation from classes with module alias.
    """
    index_file = os.path.join(doc_folder_with_code, 'index.rst')
    with open(index_file, 'w') as (f):
        f.write('.. js:autoclass:: example.MotherClass\n    :module-alias: alias_module\n\n.. js:autoclass:: example.CustomWelcome\n    :module-alias: alias_module\n\n.. js:autoclass:: example.AwesomeClass\n    :module-alias: alias_module\n')
    with cd(doc_folder_with_code):
        sphinx_main(['-c', '.', '-b', 'text', '-E', '.', '_build'])
    with open(os.path.join(doc_folder_with_code, '_build', 'index.txt'), 'rb') as (f):
        content = _sanitise_value(f.read())
        @py_assert2 = 'class alias_module.MotherClass()\n\n   Base Class\n\nclass alias_module.CustomWelcome()\n\nclass alias_module.AwesomeClass(name)\n\n   "import AwesomeClass from "example""\n\n   Inherited class\n'
        @py_assert1 = content == @py_assert2
        if not @py_assert1:
            @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (content, @py_assert2)) % {'py0':@pytest_ar._saferepr(content) if 'content' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(content) else 'content',  'py3':@pytest_ar._saferepr(@py_assert2)}
            @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert1 = @py_assert2 = None


def test_directive_autoclass_with_module_path_alias(doc_folder_with_code):
    """Generate documentation from classes with module path alias.
    """
    index_file = os.path.join(doc_folder_with_code, 'index.rst')
    with open(index_file, 'w') as (f):
        f.write('.. js:autoclass:: example.MotherClass\n    :module-path-alias: test/alias/module\n\n.. js:autoclass:: example.CustomWelcome\n    :module-path-alias: test/alias/module\n\n.. js:autoclass:: example.AwesomeClass\n    :module-path-alias: test/alias/module\n')
    with cd(doc_folder_with_code):
        sphinx_main(['-c', '.', '-b', 'text', '-E', '.', '_build'])
    with open(os.path.join(doc_folder_with_code, '_build', 'index.txt'), 'rb') as (f):
        content = _sanitise_value(f.read())
        @py_assert2 = 'class example.MotherClass()\n\n   Base Class\n\nclass example.CustomWelcome()\n\nclass example.AwesomeClass(name)\n\n   "import AwesomeClass from "test/alias/module""\n\n   Inherited class\n'
        @py_assert1 = content == @py_assert2
        if not @py_assert1:
            @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (content, @py_assert2)) % {'py0':@pytest_ar._saferepr(content) if 'content' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(content) else 'content',  'py3':@pytest_ar._saferepr(@py_assert2)}
            @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert1 = @py_assert2 = None


def test_directive_autoclass_with_partial_import_forced(doc_folder_with_code):
    """Generate documentation from classes with partial import forced.
    """
    index_file = os.path.join(doc_folder_with_code, 'index.rst')
    with open(index_file, 'w') as (f):
        f.write('.. js:autoclass:: example.AwesomeClass\n    :force-partial-import:\n')
    with cd(doc_folder_with_code):
        sphinx_main(['-c', '.', '-b', 'text', '-E', '.', '_build'])
    with open(os.path.join(doc_folder_with_code, '_build', 'index.txt'), 'rb') as (f):
        content = _sanitise_value(f.read())
        @py_assert2 = 'class example.AwesomeClass(name)\n\n   "import {AwesomeClass} from "example""\n\n   Inherited class\n'
        @py_assert1 = content == @py_assert2
        if not @py_assert1:
            @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (content, @py_assert2)) % {'py0':@pytest_ar._saferepr(content) if 'content' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(content) else 'content',  'py3':@pytest_ar._saferepr(@py_assert2)}
            @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert1 = @py_assert2 = None