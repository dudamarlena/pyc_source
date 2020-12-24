# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\turbogears\widgets\tests\test_meta.py
# Compiled at: 2011-03-26 09:20:16
from turbogears import widgets

def test_determine_template_engine():
    """Test that the engine name can be properly determined."""
    test_templates = (
     ('<p>${doh}</p>', None), ('<html>xmlns:py="http://purl.org/kid/ns#"</html>', None), ('<html xmlfoo:py="http://purl.org/kid/ns#">bar</html>', None), ('<html xmlns:py="http://purp.org/kid/ns#"/>', None), ('<html xmlns:py="http://purl.org/kid/ns#"/>', 'kid'), ('<foo xmlns:py="http://purl.org/kid/ns#" bar="test"/>', 'kid'), ("<bar xmlns:py='http://purl.org/kid/ns#' foo='test'/>", 'kid'), ("<html xmlns='test' lang='en' xmlns:py='http://purl.org/kid/ns#'/>", 'kid'), ('\n        <?xml version="1.0" encoding="UTF-8" ?>\n        <form xmlns:py="http://purl.org/kid/ns#" name="test">\n        bla\n        </form>\n        ',
 'kid'), ('\n            <span xmlns:py="http://purl.org/kid/ns#" class="${field_class}">\n            <input type="text" /></span>\n        ',
 'kid'), ('<?python\n                x = 0\n            ?>\n            <html xmlns:py="http://purl.org/kid/ns#">\n            <?python\n                x = 1\n            ?>\n            </html>',
 'kid'), ('<?xml version=\'1.0\' encoding=\'utf-8\'?>\n            <?python\n            import time\n            title = "A Kid Template"\n            ?>\n            <html xmlns="http://www.w3.org/1999/xhtml"\n                xmlns:py="http://purl.org/kid/ns#">\n            <head/></body>\n            </html>',
 'kid'), ('\n        <html xmlns="http://www.w3.org/1999/xhtml"\n                xmlns:py="http://genshi.edgewall.org/"\n                lang="en">\n          <h1>Hello, World</h1>\n        </html>\n        ',
 'genshi'), ('<?python\n          title = "A Genshi Template"\n        ?>\n        <html xmlns:py="http://genshi.edgewall.org/">\n          <head>\n            <title py:content="title">This is replaced.</title>\n          </head>\n          <body>\n            <p>My favorite fruits.</p>\n          </body>\n        </html>',
 'genshi'), ('<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"\n                "http://www.w3.org/TR/html4/loose.dtd">\n            <html xmlns="http://www.w3.org/1999/xhtml"\n                xmlns:py="http://genshi.edgewall.org/"\n                xmlns:xi="http://www.w3.org/2001/XInclude"\n                lang="en">\n                <xi:include href="site.html" />\n            <p xmlns:py="foo">doh</p>\n            </html>\n        ',
 'genshi'))
    determine_template = widgets.meta.determine_template_engine
    for (template, expected_engine) in test_templates:
        derived_engine = determine_template(template)
        assert derived_engine == expected_engine, 'Derived engine from the following template is not as expected\n(it should be %r, but it is %r):\n%s' % (expected_engine, derived_engine, template)

    return