# uncompyle6 version 3.7.4
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/kid/test/test_layout.py
# Compiled at: 2007-07-16 07:02:51
"""Unit Tests for layout templates."""
__revision__ = '$Rev: 421 $'
__author__ = 'Daniel Miller <millerdev@nwsdb.com>'
__copyright__ = 'Copyright 2006, David Stanek'
import kid

def test_layout_error():
    from kid.template_util import TemplateLayoutError
    try:
        kid.Template('\n            <html xmlns:py="http://purl.org/kid/ns#" py:layout="no_layout" />\n            ').serialize()
    except TemplateLayoutError, e:
        e = str(e)
    except Exception:
        e = 'wrong error'
    except:
        e = 'silent'

    assert "'no_layout'" in e
    assert 'not defined' in e
    assert 'while processing layout=' in e


def test_dynamic_layout():
    layout = kid.Template('\n        <html xmlns:py="http://purl.org/kid/ns#">\n          ${body_content()}\n        </html>\n        ')
    child = kid.Template('\n        <html py:layout="dynamic_layout" xmlns:py="http://purl.org/kid/ns#">\n          <body py:def="body_content()">body content</body>\n        </html>\n        ', dynamic_layout=type(layout))
    output = child.serialize()
    assert output.find('body content') > -1, 'body_content function was not executed'


def test_match_locals():
    layout = kid.Template('\n        <?python\n          test_var = "WRONG VALUE"\n        ?>\n        <html xmlns:py="http://purl.org/kid/ns#">\n          <body>\n            <?python\n              assert "test_var" in locals(),                 "test_var is not defined in layout locals"\n              assert test_var == "test value",                 "test_var has wrong value: %r" % test_var\n            ?>\n            <div />\n          </body>\n        </html>\n        ')
    child = kid.Template('\n        <?python\n          layout_params["test_var"] = "WRONG VALUE"\n        ?>\n        <html py:layout="layout" xmlns:py="http://purl.org/kid/ns#">\n          <content py:match="item.tag == \'div\'" py:strip="True">\n            <?python\n              assert "test_var" in locals(),                 "test_var is not defined in py:match locals"\n              assert test_var == "test value",                 "test_var has wrong value in py:match: %r" % test_var\n            ?>\n            test_var=${test_var}\n          </content>\n        </html>\n        ', layout=type(layout), test_var='test value')
    output = child.serialize()
    assert output.find('test_var=test value') > -1, 'match template was not executed'


def test_def_locals():
    layout = kid.Template('\n        <?python\n          test_var = "WRONG VALUE"\n        ?>\n        <html xmlns:py="http://purl.org/kid/ns#">\n          <body>\n            <?python\n              assert "test_var" in locals(),                 "test_var is not defined in layout locals"\n              assert test_var == "test value",                 "test_var has wrong value: %r" % test_var\n            ?>\n            ${child_content()}\n          </body>\n        </html>\n        ')
    child = kid.Template('\n        <?python\n          layout_params["test_var"] = "WRONG VALUE"\n        ?>\n        <html py:layout="layout" xmlns:py="http://purl.org/kid/ns#">\n          <content py:def="child_content()" py:strip="True">\n            <?python\n              assert "test_var" in locals(),                 "test_var is not defined in py:def locals"\n              assert test_var == "test value",                 "test_var has wrong value in py:def: %r" % test_var\n            ?>\n            test_var=${test_var}\n          </content>\n        </html>\n        ', layout=type(layout), test_var='test value')
    output = child.serialize()
    assert output.find('test_var=test value') > -1, 'child_content function was not executed'