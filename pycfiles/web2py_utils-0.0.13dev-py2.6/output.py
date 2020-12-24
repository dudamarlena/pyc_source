# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/web2py_utils/output.py
# Compiled at: 2010-04-28 23:01:48
import re

def compress_output(response, startswith=[
 '<pre',
 '<textarea',
 '<blockquote'], funcs=[], debug=False):

    def save_pre(match):
        s = match.group()
        for sw in startswith:
            if s.startswith(sw):
                return s

        return ''

    def compress_response(d):
        if callable(d):
            d = d()
        if isinstance(d, dict):
            cpat = re.compile('[\\n\\t\\r\\f\\v]|(?s)\\s\\s\\s|(?s)<pre(.*?)</pre>|(?s)<blockquote(.*?)</blockquote>|(?s)<textarea(.*?)</textarea>')
            d = cpat.sub(save_pre, response.render(d))
            for f in funcs:
                if callable(f):
                    f(d)

        return d

    if not debug:
        response._caller = compress_response


def html_entity_decode(text):
    """
    Removes HTML or XML character references and entities from a text string.
    
    @param text The HTML (or XML) source text.
    @return The plain text, as a Unicode string, if necessary.
    """
    import re, htmlentitydefs

    def fixup(m):
        text = m.group(0)
        if text[:2] == '&#':
            try:
                if text[:3] == '&#x':
                    return unichr(int(text[3:-1], 16))
                else:
                    return unichr(int(text[2:-1]))
            except ValueError:
                pass

        else:
            try:
                text = unichr(htmlentitydefs.name2codepoint[text[1:-1]])
            except KeyError:
                pass

        return text

    return re.sub('&#?\\w+;', fixup, text)


def __highlight__(content, dom_element='pre', linenos=True, noclasses=True):
    """
    Performs syntax highlighting on text inside of dom_element
    Uses BeautifulSoup for processing and pygments for highlighting
    
    @param content The HTML (or XML) content to parse
    @param dom_element The dom tag to search and replace with highlighted
    @return The content with highlighted code withing dom_element
    
    """
    from pygments import highlight
    from pygments.lexers import get_lexer_by_name
    from pygments.formatters import HtmlFormatter
    from BeautifulSoup import BeautifulSoup, BeautifulStoneSoup
    decodedString = unicode(BeautifulStoneSoup(content, convertEntities=BeautifulStoneSoup.HTML_ENTITIES))
    soup = BeautifulSoup(content)
    formatter = HtmlFormatter(linenos=linenos, noclasses=noclasses)
    for tag in soup.findAll(dom_element):
        language = tag.get('lang') or 'text'
        try:
            lexer = get_lexer_by_name(language, encoding='UTF-8')
        except:
            lexer = get_lexer_by_name('text', encoding='UTF-8')

        tag.replaceWith(highlight(tag.renderContents(), lexer, formatter))

    return unicode(str(soup), 'utf-8', errors='ignore')