# uncompyle6 version 3.7.4
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/kid/test/test_comment.py
# Compiled at: 2007-07-16 07:02:51
"""Unit Tests for the XML comments."""
__revision__ = '$Rev: 455 $'
__author__ = 'David Stanek <dstanek@dstanek.com>'
__copyright__ = 'Copyright 2005, David Stanek'
import kid
from kid.serialization import serialize_doctype, doctypes

def test_comments_inside():
    """Comments inside the root element."""
    t = kid.Template('<html><!-- comment 1 --><!-- comment 2 --></html>')
    assert t.serialize(output='HTML') == serialize_doctype(doctypes['html']) + '\n<HTML><!-- comment 1 --><!-- comment 2 --></HTML>'


def test_comments_outside():
    """Comments outside the root element (ticket #134)."""
    t = kid.Template('<!-- comment 1 --><html></html><!-- comment 2 -->')
    assert t.serialize(output='HTML') == serialize_doctype(doctypes['html']) + '\n<!-- comment 1 --><HTML></HTML><!-- comment 2 -->'


def test_comments_and_python():
    """Comments and PI outside the root element evaluated inside."""
    t = kid.Template('<!-- comment 1 --><?python x=42 ?><!-- comment 2 --><html>$x</html>')
    assert t.serialize(output='HTML') == serialize_doctype(doctypes['html']) + '\n<!-- comment 1 --><!-- comment 2 --><HTML>42</HTML>'


def test_nested_comments():
    """Nested comments."""
    t = kid.Template('<!--1--><html><!--2--><div><!--3--><p><!--4--></p><!--5--></div><!--7--></html><!--8-->')
    assert t.serialize(output='HTML') == serialize_doctype(doctypes['html']) + '\n<!--1--><HTML><!--2--><DIV><!--3--><P><!--4--></P><!--5--></DIV><!--7--></HTML><!--8-->'


def test_comment_removal():
    """Comments that start with '!' should not be output."""
    t = kid.Template('<html><!-- !comment --></html>')
    assert t.serialize(output='HTML') == serialize_doctype(doctypes['html']) + '\n<HTML></HTML>'
    assert t.serialize(output='xhtml') == serialize_doctype(doctypes['xhtml']) + '\n<html></html>'
    assert t.serialize(output='xml') == '<?xml version="1.0" encoding="utf-8"?>\n<html />'
    t = kid.Template('<html><!--!comment--></html>')
    assert t.serialize(output='HTML') == serialize_doctype(doctypes['html']) + '\n<HTML></HTML>'
    assert t.serialize(output='xhtml') == serialize_doctype(doctypes['xhtml']) + '\n<html></html>'
    assert t.serialize(output='xml') == '<?xml version="1.0" encoding="utf-8"?>\n<html />'


def test_comment_interpolation():
    """Comments starting with '[' or '<![' should be interpolated."""
    for b in ('', ' '):
        for c in ('! [ < <[ <! ![ <![ ${').split():
            for d in ('/ // ! ]').split():
                before_comment = '<!--%s%s $before %s-->' % (b, c, d)
                if c.startswith('!'):
                    after_comment = ''
                elif c == '[' or c == '<![' or d == '//':
                    after_comment = '<!--%s%s after %s-->' % (b, c, d)
                else:
                    after_comment = before_comment
                before = '<html>%s</html>' % before_comment
                t = kid.Template(before, before='after')
                for output in ('HTML', 'xhtml', 'xml'):
                    if output == 'HTML':
                        after = '<HTML>%s</HTML>' % after_comment
                    elif output == 'xhtml' or after_comment:
                        after = '<html>%s</html>' % after_comment
                    else:
                        after = '<html />'
                    if output == 'xml':
                        after = '<?xml version="1.0" encoding="utf-8"?>\n' + after
                    else:
                        doctype = serialize_doctype(doctypes[output.lower()])
                        after = doctype + '\n' + after
                    assert t.serialize(output=output) == after


def test_comment_for_loop():
    """Commenting out section with py:for and substitution (ticket #149)."""
    xml = '<html xmlns:py="http://purl.org/kid/ns#">\n        <!-- <select size="1" name="item">\n        <option py:for="x in mylist" value="$x">$x</option>\n        </select> -->\n        <select>\n        <option py:for="i, x in enumerate(mylist)" value="$i">$x</option>\n        </select>\n    </html>'
    t = kid.Template(xml, mylist=['peaches', 'cream'])
    assert '<!-- <select size="1" name="item">\n        <option py:for="x in mylist" value="$x">$x</option>\n        </select> -->\n        <select>\n        <option value="0">peaches</option><option value="1">cream</option>\n        </select>' in t.serialize(output='html')


def test_comment_style_sheet():
    """Allow variable substitution in style sheet (ticket #124)."""
    xml = '<html><head>\n        <style type="text/css">\n        <!--\n        #menu a#$section { background-color: yellow; }\n        //-->\n        </style></head><body>\n        <div id="menu">\n        <a href="products/" id="products">Products</a>\n        <a href="support/" id="support">Support</a>\n        </div>\n        </body></html>'
    t = kid.Template(xml, section='support')
    assert '#menu a#support' in t.serialize(output='html')