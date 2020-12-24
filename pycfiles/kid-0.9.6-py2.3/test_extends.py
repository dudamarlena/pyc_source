# uncompyle6 version 3.7.4
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/kid/test/test_extends.py
# Compiled at: 2007-07-16 07:02:51
"""Unit Tests for Template Reuse."""
__revision__ = '$Rev: 455 $'
__author__ = 'Christoph Zwerschke <cito@online.de>'
__copyright__ = 'Copyright 2006, Christoph Zwerschke'
from os.path import join as joinpath
from tempfile import mkdtemp
from shutil import rmtree
import kid

def setup_module(module):
    global tmpdir
    tmpdir = mkdtemp(prefix='kid_test_extends_')
    kid.path.insert(tmpdir)
    open(joinpath(tmpdir, 'layout.kid'), 'w').write('        <html xmlns:py="http://purl.org/kid/ns#">\n            <body py:match="item.tag == \'body\'">\n                <p>my header</p>\n                <div py:replace="item[:]" />\n                <p>my footer</p>\n            </body>\n        </html>')


def teardown_module(module):
    kid.path.remove(tmpdir)
    rmtree(tmpdir)


def test_extends():
    """Test the basic template reuse functionality."""
    page = '        <html py:extends="%s" xmlns:py="http://purl.org/kid/ns#">\n            <body>\n                <p>my content</p>\n            </body>\n        </html>'
    for extends in ("'layout.kid'", 'layout.kid', "'layout'", 'layout'):
        source = page % extends
        rslt = kid.Template(source=source).serialize()
        assert 'my header' in rslt
        assert 'my content' in rslt
        assert 'my footer' in rslt

    source = page % 'layout_module'
    from kid.template_util import TemplateExtendsError
    try:
        rslt = kid.Template(source=source).serialize()
    except TemplateExtendsError, e:
        e = str(e)
    except Exception:
        e = 'wrong error'
    else:
        e = 'silent'

    assert "'layout_module'" in e
    assert 'not defined' in e
    assert 'while processing extends=' in e
    source = "<?python\n        layout_module = kid.load_template(\n        kid.path.find('layout.kid')) ?>\n        " + source
    for extends in ('layout_module', 'layout_module.Template'):
        rslt = kid.Template(source=source).serialize()
        assert 'my header' in rslt
        assert 'my content' in rslt
        assert 'my footer' in rslt


def test_comments_in_extends():
    """Test for the bug that was reported in ticket #66."""
    open(joinpath(tmpdir, 'layout2.kid'), 'w').write('        <!-- layout -->\n        <html xmlns:py="http://purl.org/kid/ns#">\n            <head><title>layout</title></head>\n            <body py:match="item.tag == \'body\'">\n                <div>header</div>\n                <!-- comment 1 -->\n                <p align="center" py:replace="item[:]">\n                    ... content will be inserted here ...\n                </p>\n                <!-- comment 2 -->\n                <div>footer</div>\n            </body>\n        </html>')
    open(joinpath(tmpdir, 'page2.kid'), 'w').write('        <!-- page -->\n        <html xmlns:py="http://purl.org/kid/ns#"\n                py:extends="\'layout2.kid\'">\n            <head><title>page</title></head>\n            <body>\n                <!-- comment 3 -->\n                <p>my content</p>\n                <!-- comment 4 -->\n            </body>\n        </html>')
    t = kid.Template(file='page2.kid')
    rslt = t.serialize(output='xhtml')
    expected = '        <!-- page -->\n        <html>\n            <head>\n            <title>page</title></head>\n            <body>\n                <div>header</div>\n                <!-- comment 1 -->\n                <!-- comment 3 -->\n                <p>my content</p>\n                <!-- comment 4 -->\n                <!-- comment 2 -->\n                <div>footer</div>\n            </body>\n        </html>'
    i = 0
    for line in expected.splitlines():
        line = line.strip()
        i = rslt.find(line, i)
        assert i >= 0, 'Missing or misplaced: ' + line


def test_layout_and_extends():
    """Test for the bug that was reported in ticket #194."""
    open(joinpath(tmpdir, 'page3.kid'), 'w').write('        <html xmlns:py="http://purl.org/kid/ns#"\n            py:layout="\'layout3.kid\'"\n            py:extends="\'page3e.kid\'">\n        <title>Welcome to the test</title>\n        <body>\n            <div py:def="insertContent()">\n                Welcome <span py:replace="pageString()" />\n            </div>\n        </body>\n        </html>')
    open(joinpath(tmpdir, 'page3e.kid'), 'w').write('        <html xmlns:py="http://purl.org/kid/ns#">\n        <head><title>Extend Page</title></head>\n        <body>\n            <b py:def="pageString()">page</b>\n        </body>\n        </html>')
    open(joinpath(tmpdir, 'layout3.kid'), 'w').write('        <html xmlns:py="http://purl.org/kid/ns#"\n            py:extends="\'layout3e.kid\'">\n        <head><title>Layout Title</title></head>\n        <body>\n            <h1 py:content="layoutString()" />\n            <div py:replace="insertContent()" />\n        </body>\n        </html>')
    open(joinpath(tmpdir, 'layout3e.kid'), 'w').write('        <html xmlns:py="http://purl.org/kid/ns#">\n        <head><title>Extend Layout</title></head>\n        <body>\n            <b py:def="layoutString()">layout</b>\n        </body>\n        </html>')
    t = kid.Template(file='page3.kid')
    rslt = t.serialize(output='xhtml')
    expected = '        <html>\n        <head>\n            <title>Layout Title</title></head>\n        <body>\n            <h1><b>layout</b></h1>\n            <div>\n                Welcome <b>page</b>\n            </div>\n        </body>\n        </html>'
    i = 0
    for line in expected.splitlines():
        line = line.strip()
        i = rslt.find(line, i)
        assert i >= 0, 'Missing or misplaced: ' + line


def test_pudge_layout():
    """This is how Pudge implements layouts.

    This will cause a generator to be sent to template_util.generate_content.
    For each of the (ev, item) pairs yielded from the generator will be
    fed through generate content. Before the fix the tuples were treated as
    text for the output.
    """
    open(joinpath(tmpdir, 'pudge_layout.kid'), 'w').write(('\n        <?xml version="1.0"?>\n        <div xmlns="http://www.w3.org/1999/xhtml"\n            xmlns:py="http://purl.org/kid/ns#"\n            py:extends="\'testlayout.kid\'"\n            py:strip="1">\n        <span>Interesting text here</span>\n        </div>\n    ').strip())
    open(joinpath(tmpdir, 'testlayout.kid'), 'w').write(('        <?xml version="1.0"?>\n        <html xmlns="http://www.w3.org/1999/xhtml"\n            xmlns:py="http://purl.org/kid/ns#"\n            py:def="layout">\n        <body>\n        <div id="main-content" py:content="content()"/>\n        </body>\n        </html>\n    ').strip())
    t = kid.Template(file='pudge_layout.kid')
    rslt = t.serialize(output='xml')
    print rslt
    expected = '        <?xml version="1.0" encoding="utf-8"?>\n        <html xmlns="http://www.w3.org/1999/xhtml">\n        <body>\n        <div id="main-content">\n        <span>Interesting text here</span>\n        </div>\n        </body>\n        </html>\n    '
    rslt = [ x.strip() for x in rslt.splitlines() if x.strip() ]
    expected = [ x.strip() for x in expected.splitlines() if x.strip() ]
    assert expected == rslt