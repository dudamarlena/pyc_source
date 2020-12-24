# uncompyle6 version 3.7.4
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/kid/test/test_match.py
# Compiled at: 2007-07-16 07:02:50
"""Unit Tests for the template matching."""
__revision__ = '$Rev: 455 $'
__author__ = 'David Stanek <dstanek@dstanek.com>'
__copyright__ = 'Copyright 2005, David Stanek'
from os.path import join as joinpath
from tempfile import mkdtemp
from shutil import rmtree
import kid

def setup_module(module):
    global tmpdir
    tmpdir = mkdtemp(prefix='kid_test_match_')
    kid.path.insert(tmpdir)


def teardown_module(module):
    kid.path.remove(tmpdir)
    rmtree(tmpdir)


def test_match0():
    open(joinpath(tmpdir, 'match0_base.kid'), 'w').write('    <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"\n        "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">\n    <html xmlns="http://www.w3.org/1999/xhtml"\n        xmlns:py="http://purl.org/kid/ns#">\n\n        <head py:match="item.tag==\'{http://www.w3.org/1999/xhtml}head\'">\n            <meta content="text/html; charset=UTF-8"\n                http-equiv="content-type" py:replace="\'\'" />\n            <title py:replace="\'\'">Your title goes here</title>\n            <meta py:replace="item[:]" />\n        </head>\n\n        <body py:match="item.tag==\'{http://www.w3.org/1999/xhtml}body\'">\n            <p align="center">\n                <img src="http://www.turbogears.org/tgheader.png" />\n            </p>\n            <div py:replace="item[:]" />\n        </body>\n    </html>')
    open(joinpath(tmpdir, 'match0_page.kid'), 'w').write('    <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"\n        "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">\n    <html xmlns="http://www.w3.org/1999/xhtml"\n        xmlns:py="http://purl.org/kid/ns#" py:extends="\'match0_base.kid\'">\n\n        <head>\n            <meta content="text/html; charset=UTF-8"\n                http-equiv="content-type" py:replace="\'\'" />\n            <title>Welcome to TurboGears</title>\n        </head>\n\n        <body>\n            <strong py:match="item.tag == \'{http://www.w3.org/1999/xhtml}b\'"\n                py:content="item.text.upper()" />\n\n            <p>My Main page with <b>bold</b> text</p>\n        </body>\n    </html>')
    html = kid.Template(file='match0_page.kid').serialize()
    assert '<title>Welcome to TurboGears</title>' in html
    assert '<strong>BOLD</strong>' in html


def test_match1():
    open(joinpath(tmpdir, 'match1_base.kid'), 'w').write('    <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"\n        "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">\n    <html xmlns:py="http://purl.org/kid/ns#"\n         xmlns="http://www.w3.org/1999/xhtml" lang="en">\n\n        <head py:match="item.tag == \'{http://www.w3.org/1999/xhtml}head\'">\n            <title>Some title here</title>\n        </head>\n\n        <span py:match="item.tag == \'{http://www.w3.org/1999/xhtml}a\' and item.get(\'href\').startswith(\'http://\') and \'noicon\' not in str(item.get(\'class\')).split(\' \')" class="link-external" py:content="item"></span>\n        <span py:match="item.tag == \'{http://www.w3.org/1999/xhtml}a\' and item.get(\'href\').startswith(\'mailto:\') and \'noicon\' not in str(item.get(\'class\')).split(\' \')" class="link-mailto" py:content="item"></span>\n        <span py:match="item.tag == \'{http://www.w3.org/1999/xhtml}a\' and item.get(\'href\').startswith(\'/members/\') and item.get(\'href\').count(\'/\') == 2 and \'noicon\' not in str(item.get(\'class\')).split(\' \')" class="link-person" py:content="item"></span>\n\n        <body py:match="item.tag == \'{http://www.w3.org/1999/xhtml}body\'">\n            <div id="header">...</div>\n            <div py:replace="item[:]">Real content would go here.</div>\n            <div id="footer">...</div>\n        </body>\n    </html>')
    open(joinpath(tmpdir, 'match1_page.kid'), 'w').write('    <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"\n        "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">\n    <html xmlns="http://www.w3.org/1999/xhtml"\n        xmlns:py="http://purl.org/kid/ns#" py:extends="\'match1_base.kid\'">\n        <head />\n        <body>\n            <p>This is a <a href="http://www.google.ca/">test link</a>,\n            or an <a href="mailto:foo@bar.baz">e-mail address</a>.</p>\n        </body>\n    </html>')
    html = kid.Template(file='match1_page.kid').serialize()
    assert '<div id="header">...</div>' in html
    assert '<span class="link-external"><a href="http://www.google.ca/">test link</a></span>' in html
    assert '<span class="link-mailto"><a href="mailto:foo@bar.baz">e-mail address</a></span>' in html
    assert '<div id="footer">...</div>' in html
    assert '<div>Real content would go here.</div>' not in html


def test_match_2():
    """Test for a know bad case in the apply_matches function (ticket # 142)."""
    open(joinpath(tmpdir, 'match2_master.kid'), 'w').write('        <html xmlns="http://www.w3.org/1999/xhtml"\n            xmlns:py="http://purl.org/kid/ns#">\n            <body py:match="item.tag==\'{http://www.w3.org/1999/xhtml}body\'">\n                <div py:replace="item[:]"/>\n                <!-- MASTER MATCH -->\n            </body>\n        </html>')
    open(joinpath(tmpdir, 'match2_userform.kid'), 'w').write('        <html xmlns="http://www.w3.org/1999/xhtml"\n            xmlns:py="http://purl.org/kid/ns#">\n            <body>\n            <!-- THE INFAMOUS PY:MATCH   -->\n                <div py:match="item.tag==\'{http://testing.seasources.net/ns#}userform\'"\n                    py:strip="True">\n                    <form py:attrs="action=action,method=\'post\'" id="usereditform" />\n                </div>\n            </body>\n        </html>')
    extends = (
     'master', 'userform')
    for i in range(2):
        file = 'match2_%s_%s.kid' % extends
        open(joinpath(tmpdir, file), 'w').write('            <html xmlns="http://www.w3.org/1999/xhtml"\n                xmlns:py="http://purl.org/kid/ns#"\n                xmlns:seasources="http://testing.seasources.net/ns#"\n                py:extends="\'match2_%s.kid\',\'match2_%s.kid\'">\n                <body>\n                    <!-- THIS IS THE TAG I WANT TO PY:MATCH ON -->\n                    <seasources:userform></seasources:userform>\n                </body>\n            </html>' % extends)
        t = kid.Template(file=file)
        t.action = file
        html = t.serialize()
        assert 'THIS IS THE TAG' in html
        assert 'MASTER MATCH' in html
        assert 'seasources:userform' not in html
        extends = list(extends)
        extends.reverse()
        extends = tuple(extends)


def test_match_3():
    """Check for an issue with additional blank lines (ticket #131)."""
    template = '        <html xmlns="http://www.w3.org/1999/xhtml"\n                xmlns:py="http://purl.org/kid/ns#">\n        <span>one</span>\n        <p py:match="item.tag == \'hello\'">\n            hello world!\n        </p>\n        <span>two</span>\n        </html>'
    t = kid.Template(source=template)
    rslt = t.serialize(output='html')
    expect = '<html>\n        <span>one</span>\n        <span>two</span>\n        </html>'
    print rslt
    print expect
    assert rslt.endswith(expect)