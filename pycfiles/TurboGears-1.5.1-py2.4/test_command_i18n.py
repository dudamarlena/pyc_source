# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\turbogears\tests\test_command_i18n.py
# Compiled at: 2011-07-14 09:13:19
"""Tests for the tg-admin adm18n command."""
import os, shutil, sys, tempfile, unittest
from turbogears import config
from turbogears.command.i18n import InternationalizationTool
tool = None
KID_TEMPLATE = '<html xmlns:py="http://purl.org/kid/ns#">\n<head>\n    <link py:strip="1" py:for="css in tg_css">${css.display()}</link>\n    <link py:strip="1" py:for="js in tg_js_head">${js.display()}</link>\n</head>\n<body>\n  <div>Some text to be i18n\'ed</div>\n  <div>This is text that has a kid-expression ${_(\'which is to be i18n\')}</div>\n  <div foo="${_(\'kid expression in attribute\')}"/>\n  <div foo="normal attribute text"/>\n  <div lang="en">This is english, and it shouldn\'t be collected</div>\n  <div lang="de">Dies ist Deutsch, und es sollte nicht aufgesammelt werden</div>\n  <div>These are some entities that we shouldn\'t complain about: &nbsp;</div>\n</body>\n</html>\n'
GENSHI_TEMPLATE = '<html xmlns="http://www.w3.org/1999/xhtml"\n      xmlns:py="http://genshi.edgewall.org/"\n      xmlns:xi="http://www.w3.org/2001/XInclude">\n<head>\n    <link py:strip="1" py:for="css in tg_css">${css.display()}</link>\n    <link py:strip="1" py:for="js in tg_js_head">${js.display()}</link>\n</head>\n<body>\n  <div>Some text to be i18n\'ed</div>\n  <div>This is text that has a Genshi-expression ${_(\'which is to be i18n\')}</div>\n  <div>${\'some text in an expression\'}</div>\n  <div title="title attribute text" />\n  <div foo="normal attribute text" />\n  <div title="${_(\'Python expression in attribute\')}"/>\n  <div xml:lang="en">This is english, and it shouldn\'t be collected</div>\n  <div xml:lang="de">Dies ist Deutsch, und es sollte nicht aufgesammelt werden</div>\n  <div>These are some entities that we shouldn\'t complain about: &nbsp;</div>\n</body>\n</html>\n'

class I18nToolTest(unittest.TestCase):
    """Tests for the tg-admin i18n tool."""
    __module__ = __name__

    def setUp(self):
        global tool
        tool = InternationalizationTool('1.5')
        self.work_dir = tempfile.mkdtemp()
        self.src_dir = os.path.join(self.work_dir, 'src')
        self.locale_dir = os.path.join(self.work_dir, 'locale')
        os.mkdir(self.src_dir)
        self.static_dir = os.path.join(self.src_dir, 'static')
        os.mkdir(self.static_dir)
        self.template_dir = os.path.join(self.src_dir, 'templates')
        os.mkdir(self.template_dir)
        config.update({'i18n.locale_dir': self.locale_dir, 'i18n.domain': 'testmessages'})

    def tearDown(self):
        shutil.rmtree(self.work_dir)

    def test_collect_js_strings_utf8(self):
        """Strings from JS files with non-ascii chars (UTF-8) are collected correctly"""
        js_file = os.path.join(self.static_dir, 'utf8.js')
        tf = open(js_file, 'w')
        tf.write(("msg = _('Schöne Grüße')").encode('utf-8'))
        tf.close()
        sys.argv = ['i18n.py', '--src-dir', self.src_dir, 'collect']
        tool.load_config = False
        (tool.options, dummy) = tool.parse_args()
        os.mkdir(self.locale_dir)
        (tmp_handle, tmp_potfile) = tempfile.mkstemp('.pot', 'tmp', self.locale_dir)
        tool.scan_js_files(tmp_potfile, [js_file])
        pot_content = os.read(tmp_handle, 999).decode('utf-8')
        os.close(tmp_handle)
        os.remove(tmp_potfile)
        os.rmdir(self.locale_dir)
        assert 'Schöne Grüße' in pot_content

    def test_collect_js_strings_latin1(self):
        """Strings from JS files with non-ascii chars (Latin-1) are collected correctly"""
        js_file = os.path.join(self.static_dir, 'utf8.js')
        tf = open(js_file, 'w')
        tf.write(("msg = _('Schöne Grüße')").encode('latin1'))
        tf.close()
        sys.argv = ['i18n.py', '--src-dir', self.src_dir, '--js-encoding', 'latin1', 'collect']
        tool.load_config = False
        (tool.options, dummy) = tool.parse_args()
        os.mkdir(self.locale_dir)
        (tmp_handle, tmp_potfile) = tempfile.mkstemp('.pot', 'tmp', self.locale_dir)
        tool.scan_js_files(tmp_potfile, [js_file])
        pot_content = os.read(tmp_handle, 999).decode('utf-8')
        os.close(tmp_handle)
        os.remove(tmp_potfile)
        os.rmdir(self.locale_dir)
        assert 'Schöne Grüße' in pot_content

    def test_collect_genshi_strings(self):
        """Strings from Genshi templates are collected correctly."""
        tf = open(os.path.join(self.template_dir, 'test.html'), 'w')
        tf.write(GENSHI_TEMPLATE)
        tf.close()
        assert not os.path.isdir(self.locale_dir), 'locale directory should not exist yet'
        sys.argv = ['i18n.py', '--src-dir', self.src_dir, 'collect']
        tool.load_config = False
        tool.run()
        assert os.path.isdir(self.locale_dir), 'locale directory not created'
        pot_content = open(os.path.join(self.locale_dir, 'testmessages.pot')).read()
        assert "Some text to be i18n'ed" in pot_content
        assert '"which is to be i18n"' in pot_content
        assert 'title attribute text' in pot_content
        assert 'normal attribute text' not in pot_content
        assert 'Python expression in attribute' in pot_content
        assert "it shouldn't be collected" not in pot_content
        assert 'es sollte nicht aufgesammelt werden' not in pot_content

    def test_collect_kid_strings(self):
        """Strings from Kid templates are collected correctly."""
        try:
            import kid
        except ImportError:
            import warnings
            warnings.warn('Kid is not installed. Omitting i18n test for Kid templates.')
            return

        tf = open(os.path.join(self.template_dir, 'test.kid'), 'w')
        tf.write(KID_TEMPLATE)
        tf.close()
        assert not os.path.isdir(self.locale_dir), 'locale directory should not exist yet'
        sys.argv = ['i18n.py', '--src-dir', self.src_dir, 'collect']
        tool.load_config = False
        tool.run()
        assert os.path.isdir(self.locale_dir), 'locale directory not created'
        tf = open(os.path.join(self.locale_dir, 'testmessages.pot'))
        pot_content = tf.read()
        tf.close()
        assert "Some text to be i18n'ed" in pot_content
        assert 'kid expression in attribute' in pot_content
        assert 'normal attribute text' not in pot_content
        assert "it shouldn't be collected" not in pot_content
        assert 'es sollte nicht aufgesammelt werden' not in pot_content