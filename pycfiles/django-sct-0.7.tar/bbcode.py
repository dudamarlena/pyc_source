# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/herbert/dev/python/sctdev/simpleproject/simpleproject/../../communitytools/sphenecoll/sphene/contrib/libs/common/text/bbcode.py
# Compiled at: 2012-03-17 12:42:14
import re
from sphene.community.sphutils import render_blockquote, get_sph_setting
from django.conf import settings
EMOTICONS_ROOT = get_sph_setting('board_emoticons_root')

def get_member_link(member):
    return member


def obfuscate_email(email):
    return email


def escape(html):
    """Returns the given HTML with ampersands, quotes and carets encoded"""
    if not isinstance(html, basestring):
        html = str(html)
    return html.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')


class BBTag:
    """Represents an allowed tag with its name and meta data."""

    def __init__(self, name, allowed_children, implicit_tag, self_closing=False, prohibited_elements=None, discardable=False):
        """Creates a new BBTag.
        - name is the text appears in square brackets e.g. for [b], name = 'b'
        - allowed_children is a list of the names of tags that can be added to this element
        - implicit_tag is a tag that can automatically be added before this one 
          if necessary to allow it to be added.
        - self_closing means the element never has child elements
        - prohibited_elements is a list of elements that can never be 
          descendent elements of this one
        - discardable = True indicates that the tag can be discarded if 
          it can't be added at the current point in the tree.
        """
        if prohibited_elements is None:
            self.prohibited_elements = ()
        else:
            self.prohibited_elements = prohibited_elements
        self.self_closing = self_closing
        self.name = name
        self.implicit_tag = implicit_tag
        self.allowed_children = allowed_children
        self.discardable = discardable
        return

    def render_node_xhtml(self, node):
        """
        Renders a node of this BBTag as HTML.
        node is the node to render.
        """
        raise NotImplementedException()

    def render_node_bbcode(self, node):
        opening = self.name
        if node.parameter:
            opening += '=' + node.parameter
        if self.self_closing:
            return '[%s/]' % opening
        else:
            return '[%s]%s[/%s]' % (
             opening, node.render_children_bbcode(), self.name)


class HtmlEquivTag(BBTag):
    """
    A BBTag that is a direct equivalent of an HTML tag, and can render itself.
    """

    def __init__(self, *args, **kwargs):
        self.html_equiv = kwargs.pop('html_equiv')
        self.attributes = kwargs.pop('attributes', None)
        BBTag.__init__(self, *args, **kwargs)
        return

    def render_node_xhtml(self, node):
        opening = self.html_equiv
        if self.attributes:
            opening += ' ' + (' ').join([ '%s="%s"' % (k, escape(v)) for (k, v) in self.attributes.items()
                                        ])
        if self.self_closing:
            ret = '<' + opening + '/>'
        elif len(node.children) > 0:
            ret = '<' + opening + '>' + node.render_children_xhtml() + '</' + self.html_equiv + '>'
        else:
            ret = ''
        return ret


class SoftBrTag(BBTag):
    """A tag representing an optional <br>"""

    def render_node_xhtml(self, node):
        if node.parent.allows('br'):
            return '<br/>'
        else:
            return '\n'

    def render_node_bbcode(self, node):
        return '\n'


class Emoticon(BBTag):

    def render_node_xhtml(self, node):
        if len(node.children) == 0:
            return ''
        emoticon = node.children[0].text
        if node.parent.allows('img'):
            imagename = _EMOTICONS.get(emoticon, '')
            if imagename == '':
                return ''
            return '<img src="' + EMOTICONS_ROOT + imagename + '" alt="' + escape(emoticon) + '" />'
        else:
            return emoticon

    def render_node_bbcode(self, node):
        return node.children[0].text


class ImgTag(BBTag):

    def render_node_xhtml(self, node):
        if len(node.children) == 0:
            return ''
        else:
            imgurl = node.children[0].text
            if node.parent.allows('img'):
                return '<img src="' + imgurl + '" border="0"/>'
            return imgurl

    def render_node_bbcode(self, node):
        return node.children[0].text


class ColorTag(BBTag):

    def render_node_xhtml(self, node):
        if len(node.children) > 0 and (node.parameter.lower() in _COLORS or _COLOR_REGEXP.match(node.parameter) is not None):
            return '<span style="color: ' + node.parameter + ';">' + node.render_children_xhtml() + '</span>'
            return node.render_children_xhtml()
        else:
            return ''
        return


class MemberTag(BBTag):

    def render_node_xhtml(self, node):
        if len(node.children) == 0:
            return ''
        else:
            member_name = escape(node.children[0].text.strip().replace(' ', ''))
            if len(member_name) == 0:
                return ''
            return get_member_link(member_name)


class EmailTag(BBTag):

    def render_node_xhtml(self, node):
        if len(node.children) > 0:
            return obfuscate_email(escape(node.children[0].text.strip()))
        else:
            return ''


class UrlTag(BBTag):

    def render_node_xhtml(self, node):
        if len(node.children) == 0:
            return ''
        else:
            if node.parameter is not None:
                url = node.parameter.strip()
            else:
                url = node.children[0].text.strip()
            linktext = node.render_children_xhtml()
            if len(url) == 0:
                return ''
            post_link = get_sph_setting('board_post_link')
            return post_link % {'url': escape(url), 'text': linktext}
            return


from sphene import sphboard

class QuoteTag(BBTag):

    def render_node_xhtml(self, node):
        if node.parameter is None:
            node.parameter = ''
        else:
            node.parameter = node.parameter.strip()
        citation = node.render_children_xhtml()
        post = None
        membername = None
        match = _MEMBER_REGEXP.search(node.parameter)
        if match is not None:
            membername = match.group('username')
            if match.group('post_id'):
                try:
                    post = sphboard.models.Post.objects.get(pk=match.group('post_id'))
                except sphboard.models.Post.DoesNotExist:
                    pass

        return render_blockquote(citation, membername, post)


_COLORS = ('aqua', 'black', 'blue', 'fuchsia', 'gray', 'green', 'lime', 'maroon', 'navy',
           'olive', 'purple', 'red', 'silver', 'teal', 'white', 'yellow')
_COLOR_REGEXP = re.compile('#[0-9A-F]{6}')
_MEMBER_REGEXP = re.compile('^[\\\'"]?(?P<username>[0-9A-Za-z_]{1,30})[\\\'"]?(?:;(?P<post_id>[0-9]+))?$')
_BBTAG_REGEXP = re.compile('\\[\\[?\\/?([A-Za-z\\*]+)(:[a-f0-9]+)?(=[^\\]]+)?\\]?\\]')
_INLINE_TAGS = ('b', 'i', 'color', 'member', 'email', 'url', 'br', 'text', 'img', 'softbr',
                'emoticon', 'u')
_BLOCK_LEVEL_TAGS = ('p', 'quote', 'list', 'pre', 'code', 'div')
_FLOW_TAGS = _INLINE_TAGS + _BLOCK_LEVEL_TAGS
_OTHER_TAGS = ('*', )
_ANCHOR_TAGS = ('member', 'email', 'url')
_TAGS = (
 HtmlEquivTag('br', (), 'div', self_closing=True, discardable=True, html_equiv='br'),
 SoftBrTag('softbr', (), 'div', self_closing=True, discardable=True),
 Emoticon('emoticon', ('text', ), 'div'),
 HtmlEquivTag('b', _INLINE_TAGS, 'div', html_equiv='b'),
 HtmlEquivTag('u', _INLINE_TAGS, 'div', html_equiv='u'),
 ImgTag('img', _INLINE_TAGS, 'div'),
 HtmlEquivTag('i', _INLINE_TAGS, 'div', html_equiv='i'),
 ColorTag('color', _INLINE_TAGS, 'div'),
 MemberTag('member', ('text', ), 'div'),
 EmailTag('email', ('text', ), 'div'),
 UrlTag('url', _INLINE_TAGS, 'div'),
 HtmlEquivTag('p', _INLINE_TAGS, None, html_equiv='p'),
 HtmlEquivTag('div', _FLOW_TAGS, None, html_equiv='div'),
 QuoteTag('quote', _BLOCK_LEVEL_TAGS + ('softbr', ), 'div'),
 HtmlEquivTag('list', ('*', 'softbr'), None, html_equiv='ul'),
 HtmlEquivTag('pre', _INLINE_TAGS, None, prohibited_elements=('img', 'big', 'small',
                                                             'sub', 'sup', 'br'), html_equiv='pre'),
 HtmlEquivTag('code', _INLINE_TAGS, None, prohibited_elements=('img', 'big', 'small',
                                                              'sub', 'sup', 'br'), html_equiv='pre', attributes={'class': 'code'}),
 HtmlEquivTag('*', _FLOW_TAGS, 'list', html_equiv='li'))
_TAGDICT = {}
for t in _TAGS:
    if t.name != 'text':
        _TAGDICT[t.name] = t

_TAGNAMES = [ t.name for t in _TAGS ]
_EMOTICONS = get_sph_setting('board_emoticons_list')
_EMOTICON_LIST = _EMOTICONS.keys()

class BBNode:
    """Abstract base class for a node of BBcode."""

    def __init__(self, parent):
        self.parent = parent
        self.children = []

    def render_children_xhtml(self):
        """Render the child nodes as XHTML"""
        return ('').join([ child.render_xhtml() for child in self.children ])

    def render_children_bbcode(self):
        """Render the child nodes as BBCode"""
        return ('').join([ child.render_bbcode() for child in self.children ])


class BBRootNode(BBNode):
    """Represents a root node"""

    def __init__(self, allow_inline=False):
        BBNode.__init__(self, None)
        self.children = []
        self.allow_inline = allow_inline
        return

    def render_xhtml(self):
        """Render the node as XHTML"""
        return self.render_children_xhtml()

    def allows(self, tagname):
        """Returns true if the tag with 'tagname' can be added to this node"""
        if self.allow_inline:
            return tagname in _FLOW_TAGS
        else:
            return tagname in _BLOCK_LEVEL_TAGS

    def render_bbcode(self):
        """Render the node as correct BBCode"""
        return self.render_children_bbcode()


class BBTextNode(BBNode):
    """A text node, containing only plain text"""

    def __init__(self, parent, text):
        BBNode.__init__(self, parent)
        self.text = text

    def render_xhtml(self):
        """Render the node as XHTML"""
        return escape(self.text)

    def render_bbcode(self):
        return self.text

    def allows(self, tagname):
        return False


class BBEscapedTextNode(BBTextNode):

    def render_bbcode(self):
        return '[' + self.text + ']'


class BBTagNode(BBNode):

    def __init__(self, parent, name, parameter):
        BBNode.__init__(self, parent)
        self.bbtag = _TAGDICT[name]
        self.parameter = parameter

    def prohibited(self, tagname):
        """Return True if the element 'tagname' is prohibited by
        this node or any parent nodes"""
        if tagname in self.bbtag.prohibited_elements:
            return True
        else:
            if self.parent is None or not hasattr(self.parent, 'prohibited'):
                return False
            else:
                return self.parent.prohibited(tagname)
            return

    def allows(self, tagname):
        """Returns true if the tag with 'tagname' can be added to this node"""
        if tagname in self.bbtag.allowed_children:
            return not self.prohibited(tagname)
        else:
            return False

    def render_xhtml(self):
        """Render the node as XHTML"""
        return self.bbtag.render_node_xhtml(self)

    def render_bbcode(self):
        return self.bbtag.render_node_bbcode(self)


class BBCodeParser:

    def __init__(self, root_allows_inline=False):
        self.root_allows_inline = root_allows_inline

    def push_text_node(self, text, escaped=False):
        """Add a text node to the current node"""
        if escaped:
            text_class = BBEscapedTextNode
        else:
            text_class = BBTextNode
        if not self.current_node.allows('text'):
            if len(text.strip()) == 0:
                self.current_node.children.append(text_class(self.current_node, text))
            else:
                if self.current_node.allows('div'):
                    self.current_node.children.append(BBTagNode(self.current_node, 'div', ''))
                    self.descend()
                else:
                    self.ascend()
                self.push_text_node(text)
        else:
            self.current_node.children.append(text_class(self.current_node, text))

    def descend(self):
        """Move to the last child of the current node"""
        self.current_node = self.current_node.children[(-1)]

    def ascend(self):
        """Move to the parent node of the current node"""
        self.current_node = self.current_node.parent

    def push_tag_node(self, name, parameter):
        """Add a BBTagNode of name 'name' onto the tree"""
        new_tag = self.current_node.allows(name) or _TAGDICT[name]
        if new_tag.discardable:
            return
        else:
            if self.current_node == self.root_node or self.current_node.bbtag.name in _BLOCK_LEVEL_TAGS:
                if new_tag.implicit_tag is not None:
                    self.push_tag_node(new_tag.implicit_tag, '')
                    self.push_tag_node(name, parameter)
                else:
                    self.current_node = self.current_node.parent
                    self.push_tag_node(name, parameter)
            else:
                node = BBTagNode(self.current_node, name, parameter)
                self.current_node.children.append(node)
                if not node.bbtag.self_closing:
                    self.descend()
            return

    def close_tag_node(self, name):
        """Pop the stack back to the first node with the 
        specified tag name, and 'close' that node."""
        temp_node = self.current_node
        while True:
            if temp_node == self.root_node:
                break
            if hasattr(temp_node, 'bbtag'):
                if temp_node.bbtag.name == name:
                    self.current_node = temp_node
                    self.ascend()
                    break
            temp_node = temp_node.parent
            continue

    def _prepare(self, bbcode):
        bbcode = bbcode.replace('\n', '[softbr]')
        keys = {}
        uid = 1
        for emoticon in _EMOTICON_LIST:
            ukey = '$$$______%s______$$$' % uid
            bbcode = bbcode.replace(emoticon, ukey)
            keys[ukey] = '[emoticon]' + emoticon + '[/emoticon]'
            uid += 1

        for (key, val) in keys.items():
            bbcode = bbcode.replace(key, val)

        bbcode = re.sub('(?<!url=|url\\]|img=|img\\])(?:<?)((http|ftp|https)://[^\\s\\]>\\)\\[]+)(>?)', '[url]\\1[/url]', bbcode)
        return bbcode

    def parse(self, bbcode):
        """Parse the bbcode into a tree of elements"""
        self.root_node = BBRootNode(self.root_allows_inline)
        self.current_node = self.root_node
        bbcode = self._prepare(bbcode)
        pos = 0
        while pos < len(bbcode):
            match = _BBTAG_REGEXP.search(bbcode, pos)
            if match is not None:
                self.push_text_node(bbcode[pos:match.start()])
                tagname = match.groups()[0]
                parameter = match.groups()[2]
                wholematch = match.group()
                if wholematch.startswith('[[') and wholematch.endswith(']]'):
                    self.push_text_node(wholematch[1:-1], escaped=True)
                else:
                    if parameter is not None and len(parameter) > 0:
                        parameter = parameter[1:]
                    if tagname in _TAGNAMES:
                        if wholematch.startswith('[['):
                            self.push_text_node('[')
                        if wholematch.startswith('[/'):
                            self.close_tag_node(tagname)
                        else:
                            self.push_tag_node(tagname, parameter)
                        if wholematch.endswith(']]'):
                            self.push_text_node(']')
                    else:
                        self.push_text_node(wholematch)
                pos = match.end()
            else:
                self.push_text_node(bbcode[pos:])
                pos = len(bbcode)

        return

    def render_xhtml(self):
        """Render the parsed tree as XHTML"""
        return self.root_node.render_xhtml()

    def render_bbcode(self):
        """Render the parsed tree as corrected BBCode"""
        return self.root_node.render_bbcode()


def bb2xhtml(bbcode, root_allows_inline=False):
    """Render bbcode as XHTML"""
    parser = BBCodeParser(root_allows_inline)
    parser.parse(bbcode)
    return parser.render_xhtml()


def correct(bbcode):
    """Renders corrected bbcode"""
    parser = BBCodeParser(True)
    parser.parse(bbcode)
    return parser.render_bbcode()


def to_html(text):
    return bb2xhtml(text, False)


def name():
    return 'bbcode'


def quote(text, url):
    return '[quote]\n%s\n[/quote]\n' % text