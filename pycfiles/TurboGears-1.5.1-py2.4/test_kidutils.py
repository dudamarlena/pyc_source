# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\turbogears\i18n\tests\test_kidutils.py
# Compiled at: 2011-07-14 06:02:19
import kid
from turbogears.i18n.kidutils import *
from turbogears.i18n.tests import setup_module

def test_match_template():
    template = '\n    <?python\n    from turbogears.i18n.kidutils import translate\n    ?>\n    <html xmlns:py="http://purl.org/kid/ns#">\n        <translate py:match="\'lang\' in item.attrib" py:replace="translate(item, \'lang\')"/>\n        <body lang="">\n            Welcome\n            <p>Welcome</p>\n            <p lang="en">Welcome</p>\n            <p lang="fi">Welcome</p>\n        </body>\n    </html>\n    '
    t = kid.Template(source=template)
    output = t.serialize()
    assert '<p lang="en">Welcome</p>' in output
    assert '<p lang="fi">Tervetuloa</p>' in output


def test_i18n_filter():
    template = '\n    <html xmlns:py="http://purl.org/kid/ns#">\n        <body>\n            Welcome, <em>guest</em>!\n            <p>Welcome</p>\n            <p lang="en">Welcome</p>\n            <p lang="fi">Welcome<a href="" lang="de">Welcome</a></p>\n        </body>\n    </html>'
    t = kid.Template(source=template)
    t._filters += [i18n_filter]
    output = t.serialize()
    print output