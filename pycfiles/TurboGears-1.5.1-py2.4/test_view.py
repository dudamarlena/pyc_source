# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\turbogears\tests\test_view.py
# Compiled at: 2011-07-14 10:11:07
import unittest
try:
    from json import dumps, loads
except ImportError:
    from simplejson import dumps, loads

from turbogears import view, config
from turbogears.view import TGGenshiTemplatePlugin
from turbogears.view.base import _get_plugin_options
html_strict_url = 'http://www.w3.org/TR/html4/strict.dtd'
html_transitional_url = 'http://www.w3.org/TR/html4/loose.dtd'
xhtml_strict_url = 'http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd'
xhtml_transitional_url = 'http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd'

class TestTemplateEngine(object):
    """A minimal Buffet template engine plugin for testing."""
    __module__ = __name__

    def __init__(self, extra_vars_func=None, options=None):
        self.extra_vars_func = extra_vars_func
        self.options = options or dict()

    def render(self, info, format=None, fragment=False, template=None, **options):
        try:
            info.update(self.extra_vars_func())
        except TypeError:
            pass

        opts = self.options.copy()
        opts.update(options)
        return dumps((info, opts)).encode('utf-8')

    def load_template(self, templatename):
        pass

    def transform(self, info, template):
        pass


class TestView(unittest.TestCase):
    """Test suite for turbogears.view independent of external template engines.
    """
    __module__ = __name__

    def setUp(self):
        """Reload the template engines before each run."""
        print 'Loading all template engines...'
        view.load_engines()

    def tearDown(self):
        """Destroy the template engines after each test."""
        print 'Destroying all template engines...'
        view.engines.clear()

    def test_view_pass_options(self):
        """Test that view.render correctly passes options to template engine."""
        options = dict(strict=True, cache=True)
        view.engines['testplugin'] = TestTemplateEngine(options=options)
        data = dict(fruit='apple', beverage='beer')
        template = 'testplugin:test'
        options = dict(strict=False, renderer='fast')
        output = view.render(data, template, **options)
        (info, options) = loads(output.decode('utf-8'))
        assert info['fruit'] == 'apple', 'Data dict passed to view.render() not included in output.'
        assert options['cache'] is True, 'Options passed to __init__() not used.'
        assert options['renderer'] == 'fast', 'Options passed to render() not used.'
        assert options['strict'] is not True, 'Options passed to render() do not override options passed to __init__().'

    def test_content_types(self):
        """Test that setting view format sets correct content-type header."""
        view.engines['testplugin'] = TestTemplateEngine()
        template = 'testplugin:foo'
        info = dict()
        headers = {}
        view.render(info, template, headers=headers)
        assert headers.get('Content-Type') == 'text/html; charset=utf-8'
        headers = {}
        view.render(info, template, headers=headers, format='html')
        assert headers.get('Content-Type') == 'text/html; charset=utf-8'
        headers = {}
        view.render(info, template, headers=headers, format='html-strict')
        assert headers.get('Content-Type') == 'text/html; charset=utf-8'
        headers = {}
        view.render(info, template, headers=headers, format='xhtml')
        assert headers.get('Content-Type') == 'text/html; charset=utf-8'
        headers = {}
        view.render(info, template, headers=headers, format='xhtml-strict')
        assert headers.get('Content-Type') == 'text/html; charset=utf-8'
        headers = {}
        view.render(info, template, headers=headers, format='xml')
        assert headers.get('Content-Type') == 'text/xml; charset=utf-8'
        headers = {}
        view.render(info, template, headers=headers, format='json')
        assert headers.get('Content-Type') == 'application/json'
        mime_types = config.get('tg.format_mime_types', {})
        config.update({'global': {'tg.format_mime_types': {'xhtml': 'application/xhtml+xml'}}})
        headers = {}
        view.render(info, template, headers=headers, format='xhtml')
        assert headers.get('Content-Type') == 'application/xhtml+xml; charset=utf-8'
        headers = {}
        view.render(info, template, headers=headers, format='xhtml-strict')
        assert headers.get('Content-Type') == 'application/xhtml+xml; charset=utf-8'
        config.update({'global': {'tg.format_mime_types': mime_types}})


class TestKidView(unittest.TestCase):
    """Test suite for turbogears.view using the Kid template engine."""
    __module__ = __name__

    def setUp(self):
        """Reload the template engines before each run."""
        print 'Loading all template engines...'
        view.load_engines()

    def tearDown(self):
        """Destroy the template engines after each test."""
        print 'Destroying all template engines...'
        view.engines.clear()

    def test_kid_plugins_loaded(self):
        """Test that the Kid template engine plugin is loaded."""
        assert 'kid' in view.engines

    def test_UnicodeValueAppearingInATemplateIsFine(self):
        """Test that unicode values passed to template are UTF-8 encoded in output."""
        ustr = 'micro-eXtreme Programming ( µ XP): Embedding XP Within Standard Projects'
        info = dict(someval=ustr)
        val = view.render(info, template='kid:turbogears.tests.simple')
        self.assertTrue('Paging all ' + ustr in val.decode('utf-8'))

    def test_templateRetrievalByPath(self):
        """Test that Kid can find, load and compile templates."""
        from turbokid import kidsupport
        ks = kidsupport.KidSupport()
        cls = ks.load_template('turbogears.tests.simple')
        assert cls is not None
        t = cls()
        t.someval = 'hello'
        filled = str(t)
        assert 'groovy' in filled
        assert 'html' in filled
        import turbogears.tests.simple
        return

    def test_default_output_encoding(self):
        """Test we can set Kid encoding and matching content-type header is set."""
        info = dict(someval='Español')
        template = 'kid:turbogears.tests.simple'
        headers = {}
        val = view.render(info, template, headers=headers)
        assert headers.get('Content-Type') == 'text/html; charset=utf-8'
        try:
            kid_encoding = config.get('kid.encoding', 'utf-8')
            config.update({'kid.encoding': 'iso-8859-1'})
            view.load_engines()
            headers['Content-Type'] = 'text/html'
            val = view.render(info, template, headers=headers)
            assert headers.get('Content-Type') == 'text/html; charset=iso-8859-1'
            self.assertRaises(UnicodeDecodeError, val.decode, 'utf-8')
            assert 'Paging all Español' in val.decode('iso-8859-1')
        finally:
            config.update({'kid.encoding': kid_encoding})

    def test_plain_format(self):
        """Test that Kid correctly renders templates with format 'plain' or 'test'."""
        info = dict(someval='dumbos')
        template = 'kid:turbogears.tests.simple'
        headers = {}
        plain = view.render(info, template, headers=headers, format='plain')
        assert headers.get('Content-Type') == 'text/plain; charset=utf-8'
        assert plain.strip() == 'This is the groovy test template. Paging all dumbos.'
        headers = {}
        text = view.render(info, template, headers=headers, format='text')
        assert headers.get('Content-Type') == 'text/plain; charset=utf-8'
        assert text == plain
        try:
            view.render(info, template, headers=headers, format='dumbo')
        except KeyError:
            pass
        else:
            assert False, "'dumbo' should not be accepted as format"


class TestGenshiView(unittest.TestCase):
    """Test suite for turbogears.view using Genshi template engine."""
    __module__ = __name__

    def setUp(self):
        """Reload the template engines before each run."""
        print 'Loading all template engines...'
        view.load_engines()

    def tearDown(self):
        """Destroy the template engines after each test."""
        print 'Destroying all template engines...'
        view.engines.clear()

    def test_genshi_plugins_loaded(self):
        """Test that the Genshi template engine plugin are loaded."""
        assert 'genshi' in view.engines
        assert 'genshi-markup' in view.engines
        assert 'genshi-text' in view.engines

    if TGGenshiTemplatePlugin:

        def test_custom_genshi_engine_loaded(self):
            """Test that view.load_engines replaced Genshi engine with our own implementation."""
            assert isinstance(view.engines['genshi'], TGGenshiTemplatePlugin), "Engine plugin 'genshi' was not replaced by our own implementation."
            assert isinstance(view.engines['genshi-markup'], TGGenshiTemplatePlugin), "Engine plugin 'genshi-markup' was not replaced by our own implementation."
            assert view.engines['genshi'] is not view.engines['genshi-markup'], "Engine plugins 'genshi' and 'genshi-markup' should be two different instances."

    def test_UnicodeValueAppearingInATemplateIsFine(self):
        """Test that unicode values passed to template are UTF-8 encoded in output."""
        ustr = 'micro-eXtreme Programming ( µ XP): Embedding XP Within Standard Projects'
        info = dict(someval=ustr)
        val = view.render(info, template='genshi:turbogears.tests.simple')
        assert 'Paging all ' + ustr in val.decode('utf-8')

    def test_default_output_encoding(self):
        """Test we can set Genshi default encoding and headers are set correctly."""
        info = dict(someval='Español')
        template = 'genshi:turbogears.tests.simple'
        headers = {}
        val = view.render(info, template, headers=headers)
        assert headers.get('Content-Type') == 'text/html; charset=utf-8'
        try:
            genshi_encoding = config.get('genshi.default_encoding', 'utf-8')
            config.update({'genshi.default_encoding': 'iso-8859-1'})
            view.load_engines()
            headers['Content-Type'] = 'text/html'
            val = view.render(info, template, headers=headers)
            assert headers.get('Content-Type') == 'text/html; charset=iso-8859-1'
            self.assertRaises(UnicodeDecodeError, val.decode, 'utf-8')
            assert 'Paging all Español' in val.decode('iso-8859-1')
        finally:
            config.update({'genshi.default_encoding': genshi_encoding})

    def test_default_set_encoding(self):
        """Test we can set Genshi encoding per rendering and headers are set correctly."""
        info = dict(someval='Español')
        template = 'genshi:turbogears.tests.simple'
        headers = {}
        val = view.render(info, template, headers=headers)
        assert 'Paging all Español' in val
        assert headers.get('Content-Type') == 'text/html; charset=utf-8'
        headers['Content-Type'] = 'text/html'
        val = view.render(info, template, headers=headers, encoding='iso-8859-1')
        assert headers.get('Content-Type') == 'text/html; charset=iso-8859-1'
        self.assertRaises(UnicodeDecodeError, val.decode, 'utf-8')
        assert 'Paging all Español' in val.decode('iso-8859-1')

    def test_old_text_format(self):
        """Verify that our view is able to send old text format to Genshi."""
        new_syntax = config.get('genshi.new_text_syntax', False)
        config.update({'genshi.new_text_syntax': False})
        view.load_engines()
        expected_result = 'Dear Florent Aide\nYour items:\n  * Beer\n  * Whisky\n'
        info = dict(itemlist=['Beer', 'Whisky'], name='Florent Aide')
        template = 'genshi-text:turbogears.tests.genshi_old_text_format'
        headers = {}
        val = view.render(info, template, headers=headers, format='text')
        config.update({'genshi.new_text_syntax': new_syntax})
        print 'Got this:'
        print '*' * 35
        print '%r' % val
        print '*' * 35
        print 'Expected that:'
        print '*' * 35
        print '%r' % expected_result
        print '*' * 35
        assert val == expected_result

    def test_new_text_format(self):
        """Verify that our view is able to send new text format to Genshi."""
        new_syntax = config.get('genshi.new_text_syntax', False)
        config.update({'genshi.new_text_syntax': True})
        view.load_engines()
        expected_result = 'Dear Florent Aide\nYour items:\n  * Apples\n  * Bananas\n  * Cherries\n\n'
        info = dict(name='Florent Aide', itemlist=['Apples', 'Bananas', 'Cherries'])
        template = 'genshi-text:turbogears.tests.genshi_new_text_format'
        headers = {}
        val = view.render(info, template, headers=headers, format='text')
        config.update({'genshi.new_text_syntax': new_syntax})
        print 'Got this:'
        print '*' * 35
        print '%r' % val
        print '*' * 35
        print 'Expected that:'
        print '*' * 35
        print '%r' % expected_result
        print '*' * 35
        assert val == expected_result

    if TGGenshiTemplatePlugin:

        def test_genshi_default_doctypes(self):
            """Test that Genshi uses the correct doctype with default settings."""
            template = 'genshi:turbogears.tests.simple'
            info = dict(someval='dumbo')
            headers = {}
            val = view.render(info, template, headers=headers)
            assert val.lstrip().startswith('<!DOCTYPE')
            assert html_strict_url in val
            val = view.render(info, template, headers=headers, format='xhtml')
            assert val.lstrip().startswith('<!DOCTYPE')
            assert xhtml_strict_url in val
            val = view.render(info, template, headers=headers, fragment=True, format='xhtml')
            assert not val.lstrip().startswith('<!DOCTYPE')
            assert xhtml_strict_url not in val
            val = view.render(info, template, headers=headers, format='xml')
            assert not val.lstrip().startswith('<!DOCTYPE')

        def test_genshi_set_doctypes(self):
            """Test that we can set the doctpye Genshi uses for each rendering."""
            template = 'genshi:turbogears.tests.simple'
            info = dict(someval='dumbo')
            headers = {}
            val = view.render(info, template, headers=headers, doctype='html')
            assert val.lstrip().startswith('<!DOCTYPE')
            assert html_strict_url in val
            val = view.render(info, template, headers=headers, doctype='html-strict')
            assert html_strict_url in val
            val = view.render(info, template, headers=headers, doctype='html-transitional')
            assert html_transitional_url in val
            val = view.render(info, template, headers=headers, format='xhtml', doctype='html')
            assert html_strict_url in val
            val = view.render(info, template, headers=headers, format='xhtml', doctype='xhtml-strict')
            assert val.lstrip().startswith('<!DOCTYPE')
            assert xhtml_strict_url in val
            val = view.render(info, template, headers=headers, format='xhtml', fragment=True, doctype='xhtml-strict')
            assert not val.lstrip().startswith('<!DOCTYPE')
            assert xhtml_strict_url not in val
            val = view.render(info, template, headers=headers, format='xhtml', doctype='xhtml-transitional')
            assert xhtml_transitional_url in val


def test_template_plugin_output():
    """Test that minimal template engine test plugin returns correct output."""

    def extra_vars():
        return dict(tree='Rowan')

    engine = TestTemplateEngine(extra_vars_func=extra_vars)
    data = dict(fruit='apple', beverage='beer')
    output = engine.render(data)
    (info, options) = loads(output.decode('utf-8'))
    assert info['fruit'] == 'apple', 'Data dict passed to render() not included in output.'
    assert info['tree'] == 'Rowan', 'Data returned from extra_vars_func not included in output.'
    assert isinstance(options, dict) and len(options) == 0, 'Options dict not included in output or not empty.'


def test_template_plugin_pass_options():
    """Test that minimal template engine test plugin uses correct options."""
    engine = TestTemplateEngine(options=dict(cache=True, strict=False))
    output = engine.render(dict(), strict=False, renderer='fast')
    (info, options) = loads(output.decode('utf-8'))
    assert isinstance(info, dict)
    assert isinstance(options, dict)
    assert options['cache'] is True, 'Options passed to __init__() not used.'
    assert options['renderer'] == 'fast', 'Options passed to render() not used.'
    assert options['strict'] is not True, 'Options passed to render() do not override options passed to __init__().'


def test_get_plugin_options():
    """Test that template engine options and defaults are loaded correctly."""
    config.update({'genshi.expect': 'Spanish Inquisition', 'genshi.spamm': 'egg', 'bogus': 'fail'})
    defaults = {'genshi.default_format': 'html', 'genshi.spamm': 'scrambled eggs'}
    genshi_options = _get_plugin_options('genshi', defaults)
    genshitext_options = _get_plugin_options('genshi-text', defaults)
    assert genshi_options.get('genshi.default_format') == 'html', 'Genshi default options not included.'
    assert genshi_options['genshi.spamm'] != 'scrambled eggs', 'Default options not overwritten by config setting.'
    assert 'bogus' not in genshi_options, 'Options from other plugins should not be included.'
    assert genshitext_options['genshi.spamm'] == 'egg', 'Options for base plugin not loaded in plugin variant.'
    assert 'genshi-text.foo' not in genshi_options, 'Options for plugin variant should not be loaded in base plugin.'


def test_cycle():
    """Test that view.base.cyle() returns correct values."""
    oe = view.base.cycle(('odd', 'even'))
    assert str(oe) == str(None)
    assert oe.next() == 'odd'
    assert str(oe) == 'odd'
    assert oe.next() == 'even'
    assert oe.value == 'even'
    assert oe.next() == 'odd'
    assert oe.value == 'odd'
    return


def test_selector():
    """Test that view.base.selector() returns correct values."""
    assert view.base.selector(False) is None
    assert view.base.selector(True) == 'selected'
    return


def test_checker():
    """Test that view.base.checker() returns correct values."""
    assert view.base.checker(False) is None
    assert view.base.checker(True) == 'checked'
    return


def test_ipeek():
    """Test that view.base.ipeek() returns correct values."""
    assert view.base.checker(False) is None
    assert view.base.checker(True) == 'checked'
    seq = xrange(3, 6)
    assert view.base.ipeek(seq)
    assert list(seq) == range(3, 6)
    seq = xrange(3, 3)
    assert not view.base.ipeek(seq)
    assert list(seq) == []
    return