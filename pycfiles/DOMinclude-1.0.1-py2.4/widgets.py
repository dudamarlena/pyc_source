# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/dominclude/widgets.py
# Compiled at: 2008-04-28 10:40:23
import pkg_resources
from turbogears import expose
from turbogears.widgets import CSSLink, JSLink, Widget, WidgetDescription, register_static_directory, JSSource
static_dir = pkg_resources.resource_filename('dominclude', 'static')
register_static_directory('dominclude', static_dir)
dominc_css = CSSLink('dominclude', 'css/DOMinclude.css')
dominc_js = JSLink('dominclude', 'javascript/DOMinclude.js')

class DOMincConfig(JSSource):
    """Configuration for DOMinclude. When creating this widget,
    you can specify frame_size (example '[320,180]' for 320 width,
    and 180 height), display_prefix which is shown when the popup
    is displayed (default "Hide "), popup_class, open_popup_link_class,
    image_types (default "jpg|JPG|JPEG|jpeg|gif|GIF|png|PNG") and
    trigger_class (the name of the CSS class that is used to find links
    to change).
    """
    __module__ = __name__

    def __init__(self, trigger_class='DOMpop', popup_class='popup', open_popup_link_class='popuplink', display_prefix='Hide ', image_types='jpg|JPG|JPEG|jpeg|gif|GIF|png|PNG', frame_size='[320,180]'):
        src = "\n    DOMinccfg={\n    // CSS classes\n    // trigger DOMinclude\n      triggerClass:'%s',\n    // class of the popup\n      popupClass:'%s',\n    // class of the link when the popup\n    // is open\n      openPopupLinkClass:'%s',\n    // text to add to the link when the\n    // popup is open\n      displayPrefix:'%s',\n    // filter to define which files should\n    // not open in an iframe\n      imagetypes:'%s',\n    // dimensions of the popup\n      frameSize:%s\n    }\n" % (trigger_class, popup_class, open_popup_link_class, display_prefix, image_types, frame_size)
        super(DOMincConfig, self).__init__(src)


class DOMincConfigDesc(WidgetDescription):
    __module__ = __name__
    for_widget = DOMincConfig()
    template = '<div>Configuration for the DOMinclude widget.</div>'
    full_class_name = 'dominclude.DOMincConfig'


default_config = DOMincConfig()

class DOMinclude(Widget):
    """Creates a DOM-based "popup" window when a link is clicked.
    You can pass in a DOMincConfig instance as 'config' to change
    the settings. You can also pass in your own CSS. You must only
    use one DOMincConfig per page, otherwise you will get
    unpredictable results.
    """
    __module__ = __name__
    params = [
     'href', 'text']
    params_doc = dict(href='URL of the resource to display on click', text='Text of the link to be displayed')
    template = '<a href="${href}" class="DOMpop">${text}</a>'

    def __init__(self, config=default_config, css=dominc_css, **params):
        if isinstance(css, Widget):
            css = [
             css]
        self.css = css
        self.javascript = [config, dominc_js]
        super(DOMinclude, self).__init__(**params)


class DOMincludeDesc(WidgetDescription):
    __module__ = __name__
    for_widget = DOMinclude()
    template = "<div>Need to do a\n    ${for_widget.display(href='http://www.google.com/', text='Google search')}?\n    How about the ${for_widget.display(href='dominclude.DOMinclude/answer', text='answer')} to the\n    ultimate question of life, the universe and everything?\n    </div>\n    "
    full_class_name = 'dominclude.DOMinclude'

    @expose()
    def answer(self):
        return '42'