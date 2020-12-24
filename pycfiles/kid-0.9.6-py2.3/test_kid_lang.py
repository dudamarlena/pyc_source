# uncompyle6 version 3.7.4
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/kid/test/test_kid_lang.py
# Compiled at: 2007-07-16 07:02:51
__revision__ = '$Rev: 421 $'
__author__ = 'David Stanek <dstanek@dstanek.com>'
__copyright__ = 'Copyright 2005, David Stanek'
import kid

def test_strip_no_expr():
    """A py:strip without an expression will strip that element."""
    source = '\n        <test xmlns:py="http://purl.org/kid/ns#">\n            <wrapper py:strip="">\n                <present>stuff</present>\n            </wrapper>\n        </test>\n    '
    data = kid.Template(source=source).serialize()
    assert 'wrapper' not in data
    assert 'present' in data


def test_strip_with_boolean_expression__or():
    """Test for the bug that was reported in ticket #97."""
    source_template = '\n        <?python\n        a = %s\n        b = %s\n        ?>\n        <test xmlns:py="http://purl.org/kid/ns#">\n            <el py:strip="(a or b)">content</el>\n            <el py:strip="a or b">content</el>\n        </test>\n    '
    t = kid.Template(source=source_template % (True, True))
    assert '<el>' not in t.serialize()
    t = kid.Template(source=source_template % (True, False))
    assert '<el>' not in t.serialize()
    t = kid.Template(source=source_template % (False, True))
    assert '<el>' not in t.serialize()
    t = kid.Template(source=source_template % (False, False))
    assert t.serialize().count('<el>') == 2


def test_strip_with_boolean_expression__eq():
    source = '\n        <test xmlns:py="http://purl.org/kid/ns#">\n            <el0 py:strip="1==1" />\n            <el1 py:strip="1==0" />\n        </test>\n    '
    data = kid.Template(source=source).serialize()
    assert '<el0' not in data
    assert '<el1' in data


def test_replace():
    source = '\n        <test xmlns:py="http://purl.org/kid/ns#">\n            <element py:replace="\'x\'">\n                you will never see this\n            </element>\n        </test>\n    '
    data = kid.Template(source=source).serialize()
    assert 'wrapper' not in data
    assert 'x' in data


def test_replace_with_strip():
    """py:strip as ignored if py:replace exists in the same element."""
    source = '\n        <test xmlns:py="http://purl.org/kid/ns#">\n            <element py:replace="\'x\'" py:strip="">\n                content\n            </element>\n        </test>\n    '
    data = kid.Template(source=source).serialize()
    assert 'wrapper' not in data
    assert 'x' in data


def test_attr():
    source = '\n        <test xmlns:py="http://purl.org/kid/ns#">\n            <elem py:attrs="{\'a\':1, \'ns:b\':2}" />\n            <elem py:attrs="\'a\':1, \'ns:b\':2" />\n            <elem py:attrs="((\'a\',1), (\'ns:b\',2))" />\n            <elem py:attrs="a=1, ns:b=2" />\n        </test>\n    '
    data = kid.Template(source=source).serialize()
    assert data.count('<elem a="1" ns:b="2" />') == 4


def test_attr_with_strip():
    source = '\n        <test xmlns:py="http://purl.org/kid/ns#">\n            <element py:strip="False" py:attrs="a=1, b=2"/>\n        </test>\n    '
    data = kid.Template(source=source).serialize()
    print data
    assert 'a="1"' in data
    assert 'b="2"' in data