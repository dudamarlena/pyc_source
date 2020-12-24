# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/jnvilo/Projects/web/mycms/mycms/view_handlers/formatters.py
# Compiled at: 2019-03-04 11:47:19
# Size of source mod 2**32: 9227 bytes
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from django.utils.text import slugify
try:
    unicode('test')
except NameError as e:
    try:
        unicode = str
    finally:
        e = None
        del e

from loremipsum import generate_paragraphs
from mycms.creole import creole2html
from pprint import pformat
import simplejson as json
from django.conf import settings
import shlex
from xml.sax.saxutils import escape
try:
    from pygments import highlight
    from pygments.formatters.html import HtmlFormatter
    PYGMENTS = True
except ImportError:
    PYGMENTS = False

from mycms.creole.shared.utils import get_pygments_lexer, get_pygments_formatter

def html(text):
    """
    Macro tag <<html>>...<</html>>
    Pass-trought for html code (or other stuff)
    """
    return text


def HTML(*args, **kwargs):
    """"""
    text = kwargs.get('text', None)
    return html(text)


def NEWLINE(*args, **kwargs):
    text = kwargs.get('text', 0)
    text_result = '</br>'
    try:
        numlines = int(text)
        for i in range(numlines):
            text_result += '</br>'

        return text_result
    except ValueError as e:
        try:
            return '[[ERROR: NEWLINE tag requires a number. {} was given'.format(text)
        finally:
            e = None
            del e


def pre(text):
    """
    Macro tag <<pre>>...<</pre>>.
    Put text between html pre tag.
    """
    return '<pre>%s</pre>' % escape(text)


def code(*args, **kwargs):
    """
    Macro tag <<code ext=".some_extension">>...<</code>>
    If pygments is present, highlight the text according to the extension.
    """
    text = kwargs.get('text', None)
    ext = kwargs.get('ext', '.sh')
    nums = kwargs.get('nums', None)
    if not PYGMENTS:
        return pre(text)
    try:
        source_type = ''
        if '.' in ext:
            source_type = ext.strip().split('.')[1]
        else:
            source_type = ext.strip()
    except IndexError:
        source_type = ''

    lexer = get_pygments_lexer(source_type, text)
    try:
        if nums:
            formatter = HtmlFormatter(linenos='table', lineseparator='\n')
        else:
            formatter = HtmlFormatter(lineseparator='\n')
        highlighted_text = highlight(text, lexer, formatter)
    except Exception as e:
        try:
            print(e)
            highlighted_text = pre(text)
        finally:
            e = None
            del e

    return highlighted_text


def alertblock(*args, **kwargs):
    """"""
    text = kwargs.get('text', None)
    return template.format(text)


def alertwarning(*args, **kwargs):
    """"""
    text = kwargs.get('text', None)
    template = '<div class="alert alert-warning">{}</div>'
    return template.format(text)


def alertsuccess(*args, **kwargs):
    """"""
    text = kwargs.get('text', None)
    template = '<div class="alert alert-success ">{}</div>'
    return template.format(text)


def alertinfo(*args, **kwargs):
    """"""
    text = kwargs.get('text', None)
    template = '<div class="alert alert-info">{}</div>'
    return template.format(text)


def H1(*args, **kwargs):
    """"""
    text = kwargs.get('text', None)
    template = '<a  name="{}"></a><h1 class="multipage-submenu-h1">{}</h2> '
    anchor_text_url = slugify(text)
    return template.format(text, anchor_text_url)


def H2(*args, **kwargs):
    """"""
    text = kwargs.get('text', None)
    template = '<h2 class="multipage-submenu-h2">{}</h2><a name="{}"></a> '
    anchor_text_url = slugify(text)
    return template.format(text, anchor_text_url)


def infoblock(*args, **kwargs):
    """"""
    text = kwargs.get('text', 'No text provided.')
    style = kwargs.get('style', 'width: 400px; float: right; margin-left:10px')
    image = kwargs.get('image', None)
    author = kwargs.get('author', None)
    if image:
        image = '<div class="quote-photo"><img src="img/temp/user.jpg" alt=""></div>'
    else:
        image = ''
    if author:
        author = '<div class="quote-author">James Livinston - <span>The New York Post</span></div>'
    else:
        author = ''
    template = '\n    <div class="boxinfo" style="{}">\n        <div class="testimonials-user">{}<p>{}</p>{}</div>\n</div>'.format(style, image, text, author)
    return template


def image(*args, **kwargs):
    """
    We parse the content of the text to get the information about the image.
    """
    text = kwargs.get('text', None)
    name = kwargs.get('name', None)
    view = kwargs.get('view', None)
    class_ = kwargs.get('class', 'article-image')
    style = kwargs.get('style', 'width:80%')
    path_str = view.path_str
    img_url = '/static/assets/{}/{}'.format(view.path_str, name)
    img = '<div class="image-holder">\n    <img src="{}" class="{}" style="{}" />\n    <p class="image-description">{}</p>\n    </div>'.format(img_url, class_, style, text)
    return img


def google_addsense_code(*args, **kwargs):
    """"""
    text = kwargs.get('text', None)
    if settings.FORCE_SHOW_ADVERTS or settings.DEBUG == False:
        code = '\n<script async src="//pagead2.googlesyndication.com/pagead/js/adsbygoogle.js"></script>\n<!-- 200x200 -->\n<ins class="adsbygoogle"\n     style="display:inline-block;width:200px;height:200px"\n     data-ad-client="ca-pub-9449210019187312"\n     data-ad-slot="6494365200"></ins>\n<script>\n(adsbygoogle = window.adsbygoogle || []).push({});\n</script>\n\t'
    else:
        code = '<img src="/static/mycms/images/200x200.png">'
    frame = '<div class="frame_200x200" style="float: right;width: 205px;height: 205px;padding-left:15px;">{}</div>'.format(code)
    return frame


def debug(*args, **kwargs):
    """
    Just a simple example which shows the view's json_data.

    """
    view = kwargs.get('view', None)
    if view is None:
        return 'MACRO: Debug did not get a view'
    result = 'Object dictionary: {} '.format(view.json_data)
    return result


class CreoleFormatter(object):
    __doc__ = ''

    def __init__(self, raw_content=None, view=None):
        """Constructor"""
        self.raw_content = raw_content
        self.view = view

    def html(self, fake_content=False, view=None):
        """Returns the html"""
        if view is None:
            view = self.view
        if fake_content:
            paragraphs = generate_paragraphs(5, start_with_lorem=False)
            p = ''
            for paragraph in paragraphs:
                p = unicode(paragraph[2]) + '\n\n' + p

            return creole2html(p)
        return creole2html((self.raw_content), macros={'code':code,  'pre':pre, 
         'html':html, 
         'HTML':HTML, 
         'H1':H1, 
         'H2':H2, 
         'alertblock':alertblock, 
         'alertsuccess':alertsuccess, 
         'alertinfo':alertinfo, 
         'alerterror':alertwarning, 
         'infoblock':infoblock, 
         'image':image, 
         'debug':debug, 
         'google_addsense_code':google_addsense_code, 
         'NEWLINE':NEWLINE},
          verbose=None,
          stderr=None,
          view=view)