# uncompyle6 version 3.7.4
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/kid/test/test_codewriter.py
# Compiled at: 2007-07-16 07:02:51
"""kid.codewriter tests."""
__revision__ = '$Rev: 492 $'
__date__ = '$Date: 2007-07-06 21:38:45 -0400 (Fri, 06 Jul 2007) $'
__author__ = 'Ryan Tomayko (rtomayko@gmail.com)'
__copyright__ = 'Copyright 2004-2005, Ryan Tomayko'
__license__ = 'MIT <http://www.opensource.org/licenses/mit-license.php>'

def test_interpolate_expr():
    from kid.codewriter import interpolate
    tests = [
     (
      'foo ${bar} baz', ["'foo '", 'bar', "' baz'"]), ('foo $bar baz', ["'foo '", 'bar', "' baz'"]), ('foo $${bar} baz', 'foo ${bar} baz'), ('foo $$bar baz', 'foo $bar baz'), ('${foo} bar baz', ['foo', "' bar baz'"]), ('$foo bar baz', ['foo', "' bar baz'"]), ('foo bar ${baz}', ["'foo bar '", 'baz']), ('foo bar $baz', ["'foo bar '", 'baz']), ('foo $${bar}${baz}', ["'foo ${bar}'", 'baz']), ('foo $$bar$baz', ["'foo $bar'", 'baz']), ('${foo} bar ${baz}', ['foo', "' bar '", 'baz']), ('$foo bar $baz', ['foo', "' bar '", 'baz']), ('${foo}$${bar}${baz}', ['foo', "'${bar}'", 'baz']), ('$foo$$bar$baz', ['foo', "'$bar'", 'baz']), ('foo $object.attr bar', ["'foo '", 'object.attr', "' bar'"]), ('$ foo ${bar baz}', ["'$ foo '", 'bar baz']), ('foo$ ${bar.baz}', ["'foo$ '", 'bar.baz']), ('$foo $100 $bar', ['foo', "' $100 '", 'bar']), ('$foo $$100 $bar', ['foo', "' $100 '", 'bar']), ('$$foo', '$foo'), ('', '')]
    for (test, expect) in tests:
        actual = interpolate(test)
        assert actual == expect


def test_interpolate_object():
    from kid.codewriter import interpolate
    expr = interpolate('foo ${bar} baz')
    assert repr(expr) == "['foo ', bar, ' baz']"
    assert repr(interpolate('$foo')) == '[foo]'


def test_adjust_block():
    from test.blocks import blocks
    from kid.codewriter import _adjust_python_block
    for (test, expect) in blocks:
        rslt = list(_adjust_python_block(test.splitlines()))
        rslt = ('\n').join(rslt)
        assert expect == rslt


def test_exec_hack():
    """Guido may break this some day..."""
    exec 'x = 10'
    assert x == 10