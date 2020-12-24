# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/gazest/lib/markdown.py
# Compiled at: 2007-10-17 17:41:14
EXECUTABLE_NAME_FOR_USAGE = 'python markdown.py'
SPEED_TEST = 0
import re, sys, os, random, codecs
(VERBOSE, INFO, CRITICAL, NONE) = range(4)
MESSAGE_THRESHOLD = CRITICAL

def message(level, text):
    global MESSAGE_THRESHOLD
    if level >= MESSAGE_THRESHOLD:
        print text


TAB_LENGTH = 4
ENABLE_ATTRIBUTES = 1
SMART_EMPHASIS = 1
HTML_PLACEHOLDER_PREFIX = 'qaodmasdkwaspemas'
HTML_PLACEHOLDER = HTML_PLACEHOLDER_PREFIX + '%dajkqlsmdqpakldnzsdfls'
BLOCK_LEVEL_ELEMENTS = [
 'p', 'div', 'blockquote', 'pre', 'table', 'dl', 'ol', 'ul', 'script', 'noscript', 'form', 'fieldset', 'iframe', 'math', 'ins', 'del', 'hr', 'hr/', 'style']

def is_block_level(tag):
    return tag in BLOCK_LEVEL_ELEMENTS or tag[0] == 'h' and tag[1] in '0123456789'


class Document:
    __module__ = __name__

    def appendChild(self, child):
        self.documentElement = child
        child.parent = self
        self.entities = {}

    def createElement(self, tag, textNode=None):
        el = Element(tag)
        el.doc = self
        if textNode:
            el.appendChild(self.createTextNode(textNode))
        return el

    def createTextNode(self, text):
        node = TextNode(text)
        node.doc = self
        return node

    def createEntityReference(self, entity):
        if entity not in self.entities:
            self.entities[entity] = EntityReference(entity)
        return self.entities[entity]

    def toxml(self):
        return self.documentElement.toxml()

    def normalizeEntities(self, text):
        pairs = [
         ('&', '&amp;'), ('<', '&lt;'), ('>', '&gt;'), ('"', '&quot;')]
        for (old, new) in pairs:
            text = text.replace(old, new)

        return text

    def find(self, test):
        return self.documentElement.find(test)

    def unlink(self):
        self.documentElement.unlink()
        self.documentElement = None
        return


class Element:
    __module__ = __name__
    type = 'element'

    def __init__(self, tag):
        self.nodeName = tag
        self.attributes = []
        self.attribute_values = {}
        self.childNodes = []

    def unlink(self):
        for child in self.childNodes:
            if child.type == 'element':
                child.unlink()

        self.childNodes = None
        return

    def setAttribute(self, attr, value):
        if attr not in self.attributes:
            self.attributes.append(attr)
        self.attribute_values[attr] = value

    def insertChild(self, position, child):
        self.childNodes.insert(position, child)
        child.parent = self

    def removeChild(self, child):
        self.childNodes.remove(child)

    def replaceChild(self, oldChild, newChild):
        position = self.childNodes.index(oldChild)
        self.removeChild(oldChild)
        self.insertChild(position, newChild)

    def appendChild(self, child):
        self.childNodes.append(child)
        child.parent = self

    def handleAttributes(self):
        pass

    def find(self, test, depth=0):
        """ Returns a list of descendants that pass the test function """
        matched_nodes = []
        for child in self.childNodes:
            if test(child):
                matched_nodes.append(child)
            if child.type == 'element':
                matched_nodes += child.find(test, depth + 1)

        return matched_nodes

    def toxml(self):
        if ENABLE_ATTRIBUTES:
            for child in self.childNodes:
                child.handleAttributes()

        buffer = ''
        if self.nodeName in ['h1', 'h2', 'h3', 'h4']:
            buffer += '\n'
        elif self.nodeName in ['li']:
            buffer += '\n '
        buffer += '<' + self.nodeName
        for attr in self.attributes:
            value = self.attribute_values[attr]
            value = self.doc.normalizeEntities(value)
            buffer += ' %s="%s"' % (attr, value)

        if self.childNodes or self.nodeName in ['blockquote']:
            buffer += '>'
            for child in self.childNodes:
                buffer += child.toxml()

            if self.nodeName == 'p':
                buffer += '\n'
            elif self.nodeName == 'li':
                buffer += '\n '
            buffer += '</%s>' % self.nodeName
        else:
            buffer += '/>'
        if self.nodeName in ['p', 'li', 'ul', 'ol', 'h1', 'h2', 'h3', 'h4']:
            buffer += '\n'
        return buffer


class TextNode:
    __module__ = __name__
    type = 'text'
    attrRegExp = re.compile('\\{@([^\\}]*)=([^\\}]*)}')

    def __init__(self, text):
        self.value = text

    def attributeCallback(self, match):
        self.parent.setAttribute(match.group(1), match.group(2))

    def handleAttributes(self):
        self.value = self.attrRegExp.sub(self.attributeCallback, self.value)

    def toxml(self):
        text = self.value
        if not text.startswith(HTML_PLACEHOLDER_PREFIX):
            if self.parent.nodeName == 'p':
                text = text.replace('\n', '\n   ')
            elif self.parent.nodeName == 'li' and self.parent.childNodes[0] == self:
                text = '\n     ' + text.replace('\n', '\n     ')
        text = self.doc.normalizeEntities(text)
        return text


class EntityReference:
    __module__ = __name__
    type = 'entity_ref'

    def __init__(self, entity):
        self.entity = entity

    def handleAttributes(self):
        pass

    def toxml(self):
        return '&' + self.entity + ';'


class Preprocessor:
    __module__ = __name__


class HeaderPreprocessor(Preprocessor):
    """
       Replaces underlined headers with hashed headers to avoid
       the nead for lookahead later.
    """
    __module__ = __name__

    def run(self, lines):
        i = -1
        while i + 1 < len(lines):
            i = i + 1
            if not lines[i].strip():
                continue
            if lines[i].startswith('#'):
                lines.insert(i + 1, '\n')
            if i + 1 <= len(lines) and lines[(i + 1)] and lines[(i + 1)][0] in ['-', '=']:
                underline = lines[(i + 1)].strip()
                if underline == '=' * len(underline):
                    lines[i] = '# ' + lines[i].strip()
                    lines[i + 1] = ''
                elif underline == '-' * len(underline):
                    lines[i] = '## ' + lines[i].strip()
                    lines[i + 1] = ''

        return lines


HEADER_PREPROCESSOR = HeaderPreprocessor()

class LinePreprocessor(Preprocessor):
    """Deals with HR lines (needs to be done before processing lists)"""
    __module__ = __name__

    def run(self, lines):
        for i in range(len(lines)):
            if self._isLine(lines[i]):
                lines[i] = '<hr />'

        return lines

    def _isLine(self, block):
        """Determines if a block should be replaced with an <HR>"""
        if block.startswith('    '):
            return 0
        text = ('').join([ x for x in block if not x.isspace() ])
        if len(text) <= 2:
            return 0
        for pattern in ['isline1', 'isline2', 'isline3']:
            m = RE.regExp[pattern].match(text)
            if m and m.group(1):
                return 1
        else:
            return 0


LINE_PREPROCESSOR = LinePreprocessor()

class LineBreaksPreprocessor(Preprocessor):
    """Replaces double spaces at the end of the lines with <br/ >."""
    __module__ = __name__

    def run(self, lines):
        for i in range(len(lines)):
            if lines[i].endswith('  ') and not RE.regExp['tabbed'].match(lines[i]):
                lines[i] += '<br />'

        return lines


LINE_BREAKS_PREPROCESSOR = LineBreaksPreprocessor()

class HtmlBlockPreprocessor(Preprocessor):
    """Removes html blocks from self.lines"""
    __module__ = __name__

    def _get_left_tag(self, block):
        return block[1:].replace('>', ' ', 1).split()[0].lower()

    def _get_right_tag(self, left_tag, block):
        return block.rstrip()[-len(left_tag) - 2:-1].lower()

    def _equal_tags(self, left_tag, right_tag):
        if left_tag in ['?', '?php', 'div']:
            return True
        if '/' + left_tag == right_tag:
            return True
        elif left_tag == right_tag[1:] and right_tag[0] != '<':
            return True
        else:
            return False

    def _is_oneliner(self, tag):
        return tag in ['hr', 'hr/']

    def run(self, lines):
        new_blocks = []
        text = ('\n').join(lines)
        text = text.split('\n\n')
        items = []
        left_tag = ''
        right_tag = ''
        in_tag = False
        for block in text:
            if block.startswith('\n'):
                block = block[1:]
            if in_tag or block.startswith('<'):
                left_tag = self._get_left_tag(block)
                right_tag = self._get_right_tag(left_tag, block)
                if not (is_block_level(left_tag) or block[1] in ['!', '?', '@', '%']):
                    new_blocks.append(block)
                    continue
                if self._is_oneliner(left_tag):
                    new_blocks.append(block.strip())
                    continue
                if block[1] == '!':
                    left_tag = '--'
                    right_tag = self._get_right_tag(left_tag, block)
                if block.rstrip().endswith('>'):
                    if self._equal_tags(left_tag, right_tag):
                        new_blocks.append(self.stash.store(block.strip()))
                        continue
                    elif not block[1] == '!':
                        items.append(block.strip())
                        in_tag = True
                        continue
                new_blocks.append(block)
            else:
                items.append(block.strip())
                right_tag = self._get_right_tag(left_tag, block)
                if self._equal_tags(left_tag, right_tag):
                    in_tag = False
                    new_blocks.append(self.stash.store(('\n\n').join(items)))
                    items = []

        return ('\n\n').join(new_blocks).split('\n')


HTML_BLOCK_PREPROCESSOR = HtmlBlockPreprocessor()

class ReferencePreprocessor(Preprocessor):
    __module__ = __name__

    def run(self, lines):
        new_text = []
        for line in lines:
            m = RE.regExp['reference-def'].match(line)
            if m:
                id = m.group(2).strip().lower()
                t = m.group(4).strip()
                if not t:
                    self.references[id] = (
                     m.group(3), t)
                elif len(t) >= 2 and t[0] == t[(-1)] == '"' or t[0] == t[(-1)] == "'" or t[0] == '(' and t[(-1)] == ')':
                    self.references[id] = (
                     m.group(3), t[1:-1])
                else:
                    new_text.append(line)
            else:
                new_text.append(line)

        return new_text


REFERENCE_PREPROCESSOR = ReferencePreprocessor()
NOBRACKET = '[^\\]\\[]*'
BRK = '\\[(' + (NOBRACKET + '(\\[' + NOBRACKET) * 6 + (NOBRACKET + '\\])*' + NOBRACKET) * 6 + NOBRACKET + ')\\]'
BACKTICK_RE = '\\`([^\\`]*)\\`'
DOUBLE_BACKTICK_RE = '\\`\\`(.*)\\`\\`'
ESCAPE_RE = '\\\\(.)'
EMPHASIS_RE = '\\*([^\\*]*)\\*'
STRONG_RE = '\\*\\*(.*)\\*\\*'
STRONG_EM_RE = '\\*\\*\\*([^_]*)\\*\\*\\*'
if SMART_EMPHASIS:
    EMPHASIS_2_RE = '(?<!\\S)_(\\S[^_]*)_'
else:
    EMPHASIS_2_RE = '_([^_]*)_'
STRONG_2_RE = '__([^_]*)__'
STRONG_EM_2_RE = '___([^_]*)___'
LINK_RE = BRK + '\\s*\\(([^\\)]*)\\)'
LINK_ANGLED_RE = BRK + '\\s*\\(<([^\\)]*)>\\)'
IMAGE_LINK_RE = '\\!' + BRK + '\\s*\\(([^\\)]*)\\)'
REFERENCE_RE = BRK + '\\s*\\[([^\\]]*)\\]'
IMAGE_REFERENCE_RE = '\\!' + BRK + '\\s*\\[([^\\]]*)\\]'
NOT_STRONG_RE = '( \\* )'
AUTOLINK_RE = '<(http://[^>]*)>'
AUTOMAIL_RE = '<([^> \\!]*@[^> ]*)>'
HTML_RE = '(\\<[a-zA-Z/][^\\>]*\\>)'
ENTITY_RE = '(&[\\#a-zA-Z0-9]*;)'

class Pattern:
    __module__ = __name__

    def __init__(self, pattern):
        self.pattern = pattern
        self.compiled_re = re.compile('^(.*)%s(.*)$' % pattern, re.DOTALL)

    def getCompiledRegExp(self):
        return self.compiled_re


BasePattern = Pattern

class SimpleTextPattern(Pattern):
    __module__ = __name__

    def handleMatch(self, m, doc):
        return doc.createTextNode(m.group(2))


class SimpleTagPattern(Pattern):
    __module__ = __name__

    def __init__(self, pattern, tag):
        Pattern.__init__(self, pattern)
        self.tag = tag

    def handleMatch(self, m, doc):
        el = doc.createElement(self.tag)
        el.appendChild(doc.createTextNode(m.group(2)))
        return el


class BacktickPattern(Pattern):
    __module__ = __name__

    def __init__(self, pattern):
        Pattern.__init__(self, pattern)
        self.tag = 'code'

    def handleMatch(self, m, doc):
        el = doc.createElement(self.tag)
        text = m.group(2).strip()
        el.appendChild(doc.createTextNode(text))
        return el


class DoubleTagPattern(SimpleTagPattern):
    __module__ = __name__

    def handleMatch(self, m, doc):
        (tag1, tag2) = self.tag.split(',')
        el1 = doc.createElement(tag1)
        el2 = doc.createElement(tag2)
        el1.appendChild(el2)
        el2.appendChild(doc.createTextNode(m.group(2)))
        return el1


class HtmlPattern(Pattern):
    __module__ = __name__

    def handleMatch(self, m, doc):
        place_holder = self.stash.store(m.group(2))
        return doc.createTextNode(place_holder)


class LinkPattern(Pattern):
    __module__ = __name__

    def handleMatch(self, m, doc):
        el = doc.createElement('a')
        el.appendChild(doc.createTextNode(m.group(2)))
        parts = m.group(9).split()
        if parts:
            el.setAttribute('href', parts[0])
        else:
            el.setAttribute('href', '')
        if len(parts) > 1:
            title = (' ').join(parts[1:]).strip()
            title = dequote(title)
            el.setAttribute('title', title)
        return el


class ImagePattern(Pattern):
    __module__ = __name__

    def handleMatch(self, m, doc):
        el = doc.createElement('img')
        src_parts = m.group(9).split()
        el.setAttribute('src', src_parts[0])
        if len(src_parts) > 1:
            el.setAttribute('title', dequote((' ').join(src_parts[1:])))
        if ENABLE_ATTRIBUTES:
            text = doc.createTextNode(m.group(2))
            el.appendChild(text)
            text.handleAttributes()
            truealt = text.value
            el.childNodes.remove(text)
        else:
            truealt = m.group(2)
        el.setAttribute('alt', truealt)
        return el


class ReferencePattern(Pattern):
    __module__ = __name__

    def handleMatch(self, m, doc):
        if m.group(9):
            id = m.group(9).lower()
        else:
            id = m.group(2).lower()
        if not self.references.has_key(id):
            return
        (href, title) = self.references[id]
        text = m.group(2)
        return self.makeTag(href, title, text, doc)

    def makeTag(self, href, title, text, doc):
        el = doc.createElement('a')
        el.setAttribute('href', href)
        if title:
            el.setAttribute('title', title)
        el.appendChild(doc.createTextNode(text))
        return el


class ImageReferencePattern(ReferencePattern):
    __module__ = __name__

    def makeTag(self, href, title, text, doc):
        el = doc.createElement('img')
        el.setAttribute('src', href)
        if title:
            el.setAttribute('title', title)
        el.setAttribute('alt', text)
        return el


class AutolinkPattern(Pattern):
    __module__ = __name__

    def handleMatch(self, m, doc):
        el = doc.createElement('a')
        el.setAttribute('href', m.group(2))
        el.appendChild(doc.createTextNode(m.group(2)))
        return el


class AutomailPattern(Pattern):
    __module__ = __name__

    def handleMatch(self, m, doc):
        el = doc.createElement('a')
        email = m.group(2)
        if email.startswith('mailto:'):
            email = email[len('mailto:'):]
        for letter in email:
            entity = doc.createEntityReference('#%d' % ord(letter))
            el.appendChild(entity)

        mailto = 'mailto:' + email
        mailto = ('').join([ '&#%d;' % ord(letter) for letter in mailto ])
        el.setAttribute('href', mailto)
        return el


ESCAPE_PATTERN = SimpleTextPattern(ESCAPE_RE)
NOT_STRONG_PATTERN = SimpleTextPattern(NOT_STRONG_RE)
BACKTICK_PATTERN = BacktickPattern(BACKTICK_RE)
DOUBLE_BACKTICK_PATTERN = BacktickPattern(DOUBLE_BACKTICK_RE)
STRONG_PATTERN = SimpleTagPattern(STRONG_RE, 'strong')
STRONG_PATTERN_2 = SimpleTagPattern(STRONG_2_RE, 'strong')
EMPHASIS_PATTERN = SimpleTagPattern(EMPHASIS_RE, 'em')
EMPHASIS_PATTERN_2 = SimpleTagPattern(EMPHASIS_2_RE, 'em')
STRONG_EM_PATTERN = DoubleTagPattern(STRONG_EM_RE, 'strong,em')
STRONG_EM_PATTERN_2 = DoubleTagPattern(STRONG_EM_2_RE, 'strong,em')
LINK_PATTERN = LinkPattern(LINK_RE)
LINK_ANGLED_PATTERN = LinkPattern(LINK_ANGLED_RE)
IMAGE_LINK_PATTERN = ImagePattern(IMAGE_LINK_RE)
IMAGE_REFERENCE_PATTERN = ImageReferencePattern(IMAGE_REFERENCE_RE)
REFERENCE_PATTERN = ReferencePattern(REFERENCE_RE)
HTML_PATTERN = HtmlPattern(HTML_RE)
ENTITY_PATTERN = HtmlPattern(ENTITY_RE)
AUTOLINK_PATTERN = AutolinkPattern(AUTOLINK_RE)
AUTOMAIL_PATTERN = AutomailPattern(AUTOMAIL_RE)

class Postprocessor:
    __module__ = __name__


class HtmlStash:
    """This class is used for stashing HTML objects that we extract
        in the beginning and replace with place-holders."""
    __module__ = __name__

    def __init__(self):
        self.html_counter = 0
        self.rawHtmlBlocks = []

    def store(self, html):
        """Saves an HTML segment for later reinsertion.  Returns a
           placeholder string that needs to be inserted into the
           document.

           @param html: an html segment
           @returns : a placeholder string """
        self.rawHtmlBlocks.append(html)
        placeholder = HTML_PLACEHOLDER % self.html_counter
        self.html_counter += 1
        return placeholder


class BlockGuru:
    __module__ = __name__

    def _findHead(self, lines, fn, allowBlank=0):
        """Functional magic to help determine boundaries of indented
           blocks.

           @param lines: an array of strings
           @param fn: a function that returns a substring of a string
                      if the string matches the necessary criteria
           @param allowBlank: specifies whether it's ok to have blank
                      lines between matching functions
           @returns: a list of post processes items and the unused
                      remainder of the original list"""
        items = []
        item = -1
        i = 0
        for line in lines:
            if not line.strip() and not allowBlank:
                return (
                 items, lines[i:])
            if not line.strip() and allowBlank:
                i += 1
                for j in range(i, len(lines)):
                    if lines[j].strip():
                        next = lines[j]
                        break
                else:
                    break

                part = fn(next)
                if part:
                    items.append('')
                    continue
                else:
                    break
            part = fn(line)
            if part:
                items.append(part)
                i += 1
                continue
            else:
                return (
                 items, lines[i:])
        else:
            i += 1

        return (items, lines[i:])

    def detabbed_fn(self, line):
        """ An auxiliary method to be passed to _findHead """
        m = RE.regExp['tabbed'].match(line)
        if m:
            return m.group(4)
        else:
            return
        return

    def detectTabbed(self, lines):
        return self._findHead(lines, self.detabbed_fn, allowBlank=1)


def print_error(string):
    """Print an error string to stderr"""
    sys.stderr.write(string + '\n')


def dequote(string):
    """ Removes quotes from around a string """
    if string.startswith('"') and string.endswith('"') or string.startswith("'") and string.endswith("'"):
        return string[1:-1]
    else:
        return string


class CorePatterns:
    """This class is scheduled for removal as part of a refactoring
        effort."""
    __module__ = __name__
    patterns = {'header': '(#*)([^#]*)(#*)', 'reference-def': '(\\ ?\\ ?\\ ?)\\[([^\\]]*)\\]:\\s*([^ ]*)(.*)', 'containsline': '([-]*)$|^([=]*)', 'ol': '[ ]{0,3}[\\d]*\\.\\s+(.*)', 'ul': '[ ]{0,3}[*+-]\\s+(.*)', 'isline1': '(\\**)', 'isline2': '(\\-*)', 'isline3': '(\\_*)', 'tabbed': '((\\t)|(    ))(.*)', 'quoted': '> ?(.*)'}

    def __init__(self):
        self.regExp = {}
        for key in self.patterns.keys():
            self.regExp[key] = re.compile('^%s$' % self.patterns[key], re.DOTALL)

        self.regExp['containsline'] = re.compile('^([-]*)$|^([=]*)$', re.M)


RE = CorePatterns()

class Markdown:
    """ Markdown formatter class for creating an html document from
        Markdown text """
    __module__ = __name__

    def __init__(self, source=None, extensions=[], extension_configs=None, encoding=None, safe_mode=True):
        """Creates a new Markdown instance.

           @param source: The text in Markdown format.
           @param encoding: The character encoding of <text>. """
        self.safeMode = safe_mode
        self.encoding = encoding
        self.source = source
        self.blockGuru = BlockGuru()
        self.registeredExtensions = []
        self.stripTopLevelTags = 1
        self.docType = ''
        self.preprocessors = [
         HEADER_PREPROCESSOR, LINE_PREPROCESSOR, HTML_BLOCK_PREPROCESSOR, LINE_BREAKS_PREPROCESSOR, REFERENCE_PREPROCESSOR]
        self.postprocessors = []
        self.textPostprocessors = []
        self.prePatterns = []
        self.inlinePatterns = [
         DOUBLE_BACKTICK_PATTERN, BACKTICK_PATTERN, ESCAPE_PATTERN, IMAGE_LINK_PATTERN, IMAGE_REFERENCE_PATTERN, REFERENCE_PATTERN, LINK_ANGLED_PATTERN, LINK_PATTERN, AUTOLINK_PATTERN, AUTOMAIL_PATTERN, HTML_PATTERN, ENTITY_PATTERN, NOT_STRONG_PATTERN, STRONG_EM_PATTERN, STRONG_EM_PATTERN_2, STRONG_PATTERN, STRONG_PATTERN_2, EMPHASIS_PATTERN, EMPHASIS_PATTERN_2]
        self.registerExtensions(extensions=extensions, configs=extension_configs)
        self.reset()

    def registerExtensions(self, extensions, configs):
        if not configs:
            configs = {}
        for ext in extensions:
            extension_module_name = 'mdx_' + ext
            try:
                module = __import__(extension_module_name)
            except:
                message(CRITICAL, "couldn't load extension %s (looking for %s module)" % (ext, extension_module_name))
            else:
                if configs.has_key(ext):
                    configs_for_ext = configs[ext]
                else:
                    configs_for_ext = []
                extension = module.makeExtension(configs_for_ext)
                extension.extendMarkdown(self, globals())

    def registerExtension(self, extension):
        """ This gets called by the extension """
        self.registeredExtensions.append(extension)

    def reset(self):
        """Resets all state variables so that we can start
            with a new text."""
        self.references = {}
        self.htmlStash = HtmlStash()
        HTML_BLOCK_PREPROCESSOR.stash = self.htmlStash
        REFERENCE_PREPROCESSOR.references = self.references
        HTML_PATTERN.stash = self.htmlStash
        ENTITY_PATTERN.stash = self.htmlStash
        REFERENCE_PATTERN.references = self.references
        IMAGE_REFERENCE_PATTERN.references = self.references
        for extension in self.registeredExtensions:
            extension.reset()

    def _transform(self):
        """Transforms the Markdown text into a XHTML body document

           @returns: A NanoDom Document """
        self.doc = Document()
        self.top_element = self.doc.createElement('span')
        self.top_element.appendChild(self.doc.createTextNode('\n'))
        self.top_element.setAttribute('class', 'markdown')
        self.doc.appendChild(self.top_element)
        text = self.source.strip()
        text = text.replace('\r\n', '\n').replace('\r', '\n')
        text += '\n\n'
        text = text.expandtabs(TAB_LENGTH)
        self.lines = text.split('\n')
        for prep in self.preprocessors:
            self.lines = prep.run(self.lines)

        buffer = []
        for line in self.lines:
            if line.startswith('#'):
                self._processSection(self.top_element, buffer)
                buffer = [line]
            else:
                buffer.append(line)

        self._processSection(self.top_element, buffer)
        self.top_element.appendChild(self.doc.createTextNode('\n'))
        for postprocessor in self.postprocessors:
            postprocessor.run(self.doc)

        return self.doc

    def _processSection(self, parent_elem, lines, inList=0, looseList=0):
        """Process a section of a source document, looking for high
           level structural elements like lists, block quotes, code
           segments, html blocks, etc.  Some those then get stripped
           of their high level markup (e.g. get unindented) and the
           lower-level markup is processed recursively.

           @param parent_elem: A NanoDom element to which the content
                               will be added
           @param lines: a list of lines
           @param inList: a level
           @returns: None"""
        if not lines:
            return
        processFn = {'ul': self._processUList, 'ol': self._processOList, 'quoted': self._processQuote, 'tabbed': self._processCodeBlock}
        for regexp in ['ul', 'ol', 'quoted', 'tabbed']:
            m = RE.regExp[regexp].match(lines[0])
            if m:
                processFn[regexp](parent_elem, lines, inList)
                return

        if inList:
            (start, theRest) = self._linesUntil(lines, lambda line: RE.regExp['ul'].match(line) or RE.regExp['ol'].match(line) or not line.strip())
            self._processSection(parent_elem, start, inList - 1, looseList=looseList)
            self._processSection(parent_elem, theRest, inList - 1, looseList=looseList)
        else:
            (paragraph, theRest) = self._linesUntil(lines, lambda line: not line.strip())
            if len(paragraph) and paragraph[0].startswith('#'):
                m = RE.regExp['header'].match(paragraph[0])
                if m:
                    level = len(m.group(1))
                    h = self.doc.createElement('h%d' % level)
                    parent_elem.appendChild(h)
                    for item in self._handleInlineWrapper2(m.group(2).strip()):
                        h.appendChild(item)

                else:
                    message(CRITICAL, "We've got a problem header!")
            elif paragraph:
                list = self._handleInlineWrapper2(('\n').join(paragraph))
                if parent_elem.nodeName == 'li' and not (looseList or parent_elem.childNodes):
                    el = parent_elem
                else:
                    el = self.doc.createElement('p')
                    parent_elem.appendChild(el)
                for item in list:
                    el.appendChild(item)

            if theRest:
                theRest = theRest[1:]
            self._processSection(parent_elem, theRest, inList)

    def _processUList(self, parent_elem, lines, inList):
        self._processList(parent_elem, lines, inList, listexpr='ul', tag='ul')

    def _processOList(self, parent_elem, lines, inList):
        self._processList(parent_elem, lines, inList, listexpr='ol', tag='ol')

    def _processList(self, parent_elem, lines, inList, listexpr, tag):
        """Given a list of document lines starting with a list item,
           finds the end of the list, breaks it up, and recursively
           processes each list item and the remainder of the text file.

           @param parent_elem: A dom element to which the content will be added
           @param lines: a list of lines
           @param inList: a level
           @returns: None"""
        ul = self.doc.createElement(tag)
        parent_elem.appendChild(ul)
        looseList = 0
        items = []
        item = -1
        i = 0
        for line in lines:
            loose = 0
            if not line.strip():
                i += 1
                loose = 1
                for j in range(i, len(lines)):
                    if lines[j].strip():
                        next = lines[j]
                        break
                else:
                    break

                if RE.regExp['ul'].match(next) or RE.regExp['ol'].match(next) or RE.regExp['tabbed'].match(next):
                    items[item].append(line.strip())
                    looseList = loose or looseList
                    continue
                else:
                    break
            for expr in ['ul', 'ol', 'tabbed']:
                m = RE.regExp[expr].match(line)
                if m:
                    if expr in ['ul', 'ol']:
                        if m.group(1):
                            items.append([m.group(1)])
                            item += 1
                    elif expr == 'tabbed':
                        items[item].append(m.group(4))
                    i += 1
                    break
            else:
                items[item].append(line)
                i += 1

        else:
            i += 1

        for item in items:
            li = self.doc.createElement('li')
            ul.appendChild(li)
            self._processSection(li, item, inList + 1, looseList=looseList)

        self._processSection(parent_elem, lines[i:], inList)

    def _linesUntil(self, lines, condition):
        """ A utility function to break a list of lines upon the
            first line that satisfied a condition.  The condition
            argument should be a predicate function.
            """
        i = -1
        for line in lines:
            i += 1
            if condition(line):
                break
        else:
            i += 1

        return (
         lines[:i], lines[i:])

    def _processQuote(self, parent_elem, lines, inList):
        """Given a list of document lines starting with a quote finds
           the end of the quote, unindents it and recursively
           processes the body of the quote and the remainder of the
           text file.

           @param parent_elem: DOM element to which the content will be added
           @param lines: a list of lines
           @param inList: a level
           @returns: None """
        dequoted = []
        i = 0
        for line in lines:
            m = RE.regExp['quoted'].match(line)
            if m:
                dequoted.append(m.group(1))
                i += 1
            else:
                break
        else:
            i += 1

        blockquote = self.doc.createElement('blockquote')
        parent_elem.appendChild(blockquote)
        self._processSection(blockquote, dequoted, inList)
        self._processSection(parent_elem, lines[i:], inList)

    def _processCodeBlock(self, parent_elem, lines, inList):
        """Given a list of document lines starting with a code block
           finds the end of the block, puts it into the dom verbatim
           wrapped in ("<pre><code>") and recursively processes the
           the remainder of the text file.

           @param parent_elem: DOM element to which the content will be added
           @param lines: a list of lines
           @param inList: a level
           @returns: None"""
        (detabbed, theRest) = self.blockGuru.detectTabbed(lines)
        pre = self.doc.createElement('pre')
        code = self.doc.createElement('code')
        parent_elem.appendChild(pre)
        pre.appendChild(code)
        text = ('\n').join(detabbed).rstrip() + '\n'
        code.appendChild(self.doc.createTextNode(text))
        self._processSection(parent_elem, theRest, inList)

    def _handleInlineWrapper2(self, line):
        parts = [
         line]
        for pattern in self.inlinePatterns:
            i = 0
            while i < len(parts):
                x = parts[i]
                if isinstance(x, (str, unicode)):
                    result = self._applyPattern(x, pattern)
                    if result:
                        i -= 1
                        parts.remove(x)
                        for y in result:
                            parts.insert(i + 1, y)

                i += 1

        for i in range(len(parts)):
            x = parts[i]
            if isinstance(x, (str, unicode)):
                parts[i] = self.doc.createTextNode(x)

        return parts

    def _handleInlineWrapper(self, line):
        parts = [
         line]
        i = 0
        while i < len(parts):
            x = parts[i]
            if isinstance(x, (str, unicode)):
                parts.remove(x)
                result = self._handleInline(x)
                for y in result:
                    parts.insert(i, y)

            else:
                i += 1

        return parts

    def _handleInline(self, line):
        """Transform a Markdown line with inline elements to an XHTML
        fragment.

        This function uses auxiliary objects called inline patterns.
        See notes on inline patterns above.

        @param item: A block of Markdown text
        @return: A list of NanoDom nodes """
        if not line:
            return [
             self.doc.createTextNode(' ')]
        for pattern in self.inlinePatterns:
            list = self._applyPattern(line, pattern)
            if list:
                return list

        return [
         self.doc.createTextNode(line)]

    def _applyPattern(self, line, pattern):
        """ Given a pattern name, this function checks if the line
        fits the pattern, creates the necessary elements, and returns
        back a list consisting of NanoDom elements and/or strings.
        
        @param line: the text to be processed
        @param pattern: the pattern to be checked

        @returns: the appropriate newly created NanoDom element if the
                  pattern matches, None otherwise.
        """
        m = pattern.getCompiledRegExp().match(line)
        if not m:
            return
        node = pattern.handleMatch(m, self.doc)
        if node:
            return (m.groups()[(-1)], node, m.group(1))
        else:
            return
        return

    def __str__(self, source=None):
        """Return the document in XHTML format.

        @returns: A serialized XHTML body."""
        if source:
            self.source = source
        doc = self._transform()
        xml = doc.toxml()
        for i in range(self.htmlStash.html_counter):
            html = self.htmlStash.rawHtmlBlocks[i]
            if self.safeMode:
                html = '[HTML_REMOVED]'
            xml = xml.replace('<p>%s\n</p>' % (HTML_PLACEHOLDER % i), html + '\n')
            xml = xml.replace(HTML_PLACEHOLDER % i, html)

        if self.stripTopLevelTags:
            xml = xml.strip()[23:-7] + '\n'
        for pp in self.textPostprocessors:
            xml = pp.run(xml)

        return self.docType + xml

    toString = __str__

    def __unicode__(self):
        """Return the document in XHTML format as a Unicode object.
        """
        return str(self)

    toUnicode = __unicode__


def markdownFromFile(input=None, output=None, extensions=[], encoding=None, message_threshold=CRITICAL, safe=False):
    global MESSAGE_THRESHOLD
    MESSAGE_THRESHOLD = message_threshold
    message(VERBOSE, 'input file: %s' % input)
    if not encoding:
        encoding = 'utf-8'
    input_file = codecs.open(input, mode='r', encoding='utf-8')
    text = input_file.read()
    input_file.close()
    new_text = markdown(text, extensions, encoding, safe_mode=safe)
    if output:
        output_file = codecs.open(output, 'w', encoding=encoding)
        output_file.write(new_text)
        output_file.close()
    else:
        sys.stdout.write(new_text.encode(encoding))


def markdown(text, extensions=[], encoding=None, safe_mode=False):
    message(VERBOSE, 'in markdown.markdown(), received text:\n%s' % text)
    extension_names = []
    extension_configs = {}
    for ext in extensions:
        pos = ext.find('(')
        if pos == -1:
            extension_names.append(ext)
        else:
            name = ext[:pos]
            extension_names.append(name)
            pairs = [ x.split('=') for x in ext[pos + 1:-1].split(',') ]
            configs = [ (x.strip(), y.strip()) for (x, y) in pairs ]
            extension_configs[name] = configs

    md = Markdown(text, extensions=extension_names, extension_configs=extension_configs, safe_mode=safe_mode)
    return md.toString()


class Extension:
    __module__ = __name__

    def __init__(self, configs={}):
        self.config = configs

    def getConfig(self, key):
        if self.config.has_key(key):
            return self.config[key][0]
        else:
            return ''

    def getConfigInfo(self):
        return [ (key, self.config[key][1]) for key in self.config.keys() ]

    def setConfig(self, key, value):
        self.config[key][0] = value


OPTPARSE_WARNING = '\nPython 2.3 or higher required for advanced command line options.\nFor lower versions of Python use:\n\n      %s INPUT_FILE > OUTPUT_FILE\n    \n' % EXECUTABLE_NAME_FOR_USAGE

def parse_options():
    try:
        optparse = __import__('optparse')
    except:
        if len(sys.argv) == 2:
            return {'input': sys.argv[1], 'output': None, 'message_threshold': CRITICAL, 'safe': False, 'extensions': [], 'encoding': None}
        else:
            print OPTPARSE_WARNING
            return

    parser = optparse.OptionParser(usage='%prog INPUTFILE [options]')
    parser.add_option('-f', '--file', dest='filename', help='write output to OUTPUT_FILE', metavar='OUTPUT_FILE')
    parser.add_option('-e', '--encoding', dest='encoding', help='encoding for input and output files')
    parser.add_option('-q', '--quiet', default=CRITICAL, action='store_const', const=NONE, dest='verbose', help='suppress all messages')
    parser.add_option('-v', '--verbose', action='store_const', const=INFO, dest='verbose', help='print info messages')
    parser.add_option('-s', '--safe', action='store_const', const=True, dest='safe', help="same mode (strip user's HTML tag)")
    parser.add_option('--noisy', action='store_const', const=VERBOSE, dest='verbose', help='print debug messages')
    parser.add_option('-x', '--extension', action='append', dest='extensions', help='load extension EXTENSION', metavar='EXTENSION')
    (options, args) = parser.parse_args()
    if not len(args) == 1:
        parser.print_help()
        return
    else:
        input_file = args[0]
    if not options.extensions:
        options.extensions = []
    return {'input': input_file, 'output': options.filename, 'message_threshold': options.verbose, 'safe': options.safe, 'extensions': options.extensions, 'encoding': options.encoding}


if __name__ == '__main__':
    options = parse_options()
    if not options:
        sys.exit(0)
    markdownFromFile(**options)