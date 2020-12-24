# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/dominclude/tests/test_dominclude.py
# Compiled at: 2008-04-28 10:40:23
from turbogears.widgets import CSSSource
from turbogears.view import load_engines
from dominclude import DOMincConfig, DOMinclude
from dominclude.widgets import dominc_js, dominc_css

def test_dominc_config():
    load_engines()
    config = DOMincConfig()
    output = config.render()
    print output
    assert "\n    DOMinccfg={\n    // CSS classes\n    // trigger DOMinclude\n      triggerClass:'DOMpop',\n    // class of the popup\n      popupClass:'popup',\n    // class of the link when the popup\n    // is open\n      openPopupLinkClass:'popuplink',\n    // text to add to the link when the\n    // popup is open\n      displayPrefix:'Hide ',\n    // filter to define which files should\n    // not open in an iframe\n      imagetypes:'jpg|JPG|JPEG|jpeg|gif|GIF|png|PNG',\n    // dimensions of the popup\n      frameSize:[320,180]\n    }\n" in output


def test_dominc_custom_config():
    load_engines()
    config = DOMincConfig(trigger_class='1', popup_class='2', open_popup_link_class='3', display_prefix='4', image_types='5', frame_size='[2,4]')
    output = config.render()
    print output
    assert "DOMinccfg={\n    // CSS classes\n    // trigger DOMinclude\n      triggerClass:'1',\n    // class of the popup\n      popupClass:'2',\n    // class of the link when the popup\n    // is open\n      openPopupLinkClass:'3',\n    // text to add to the link when the\n    // popup is open\n      displayPrefix:'4',\n    // filter to define which files should\n    // not open in an iframe\n      imagetypes:'5',\n    // dimensions of the popup\n      frameSize:[2,4]\n    }\n" in output


def test_dominclude_js():
    popup = DOMinclude()
    assert popup.javascript == [DOMincConfig(), dominc_js]


def test_dominclude_custom_js():
    config = DOMincConfig(trigger_class='foo')
    popup = DOMinclude(config=config)
    assert popup.javascript == [config, dominc_js]


def test_dominclude_render():
    load_engines()
    popup = DOMinclude()
    output = popup.render(href='/foo/bar', text='My Link Text')
    print output
    assert output == '<a href="/foo/bar" class="DOMpop">My Link Text</a>'


def test_dominclude_css():
    popup = DOMinclude()
    assert popup.css == [dominc_css]


def test_dominclude_custom_css():
    css = CSSSource('popup { font-weight: bold }')
    popup = DOMinclude(css=css)
    assert popup.css == [css]