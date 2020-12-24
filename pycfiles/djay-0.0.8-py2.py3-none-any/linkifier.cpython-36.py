# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-m_4qh6p6/bleach/bleach/linkifier.py
# Compiled at: 2019-07-30 18:47:12
# Size of source mod 2**32: 19596 bytes
from __future__ import unicode_literals
import re, six
from bleach import callbacks as linkify_callbacks
from bleach import html5lib_shim
from bleach.utils import alphabetize_attributes, force_unicode
DEFAULT_CALLBACKS = [
 linkify_callbacks.nofollow]
TLDS = 'ac ad ae aero af ag ai al am an ao aq ar arpa as asia at au aw ax az\n       ba bb bd be bf bg bh bi biz bj bm bn bo br bs bt bv bw by bz ca cat\n       cc cd cf cg ch ci ck cl cm cn co com coop cr cu cv cx cy cz de dj dk\n       dm do dz ec edu ee eg er es et eu fi fj fk fm fo fr ga gb gd ge gf gg\n       gh gi gl gm gn gov gp gq gr gs gt gu gw gy hk hm hn hr ht hu id ie il\n       im in info int io iq ir is it je jm jo jobs jp ke kg kh ki km kn kp\n       kr kw ky kz la lb lc li lk lr ls lt lu lv ly ma mc md me mg mh mil mk\n       ml mm mn mo mobi mp mq mr ms mt mu museum mv mw mx my mz na name nc ne\n       net nf ng ni nl no np nr nu nz om org pa pe pf pg ph pk pl pm pn post\n       pr pro ps pt pw py qa re ro rs ru rw sa sb sc sd se sg sh si sj sk sl\n       sm sn so sr ss st su sv sx sy sz tc td tel tf tg th tj tk tl tm tn to\n       tp tr travel tt tv tw tz ua ug uk us uy uz va vc ve vg vi vn vu wf ws\n       xn xxx ye yt yu za zm zw'.split()
TLDS.reverse()

def build_url_re(tlds=TLDS, protocols=html5lib_shim.allowed_protocols):
    """Builds the url regex used by linkifier

   If you want a different set of tlds or allowed protocols, pass those in
   and stomp on the existing ``url_re``::

       from bleach import linkifier

       my_url_re = linkifier.build_url_re(my_tlds_list, my_protocols)

       linker = LinkifyFilter(url_re=my_url_re)

    """
    return re.compile('\\(*  # Match any opening parentheses.\n        \\b(?<![@.])(?:(?:{0}):/{{0,3}}(?:(?:\\w+:)?\\w+@)?)?  # http://\n        ([\\w-]+\\.)+(?:{1})(?:\\:[0-9]+)?(?!\\.\\w)\\b   # xx.yy.tld(:##)?\n        (?:[/?][^\\s\\{{\\}}\\|\\\\\\^\\[\\]`<>"]*)?\n            # /path/zz (excluding "unsafe" chars from RFC 1738,\n            # except for # and ~, which happen in practice)\n        '.format('|'.join(protocols), '|'.join(tlds)), re.IGNORECASE | re.VERBOSE | re.UNICODE)


URL_RE = build_url_re()
PROTO_RE = re.compile('^[\\w-]+:/{0,3}', re.IGNORECASE)
EMAIL_RE = re.compile('(?<!//)\n    (([-!#$%&\'*+/=?^_`{}|~0-9A-Z]+\n        (\\.[-!#$%&\'*+/=?^_`{}|~0-9A-Z]+)*  # dot-atom\n    |^"([\\001-\\010\\013\\014\\016-\\037!#-\\[\\]-\\177]\n        |\\\\[\\001-\\011\\013\\014\\016-\\177])*"  # quoted-string\n    )@(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\\.)+[A-Z]{2,6})  # domain\n    ', re.IGNORECASE | re.MULTILINE | re.VERBOSE)

class Linker(object):
    __doc__ = 'Convert URL-like strings in an HTML fragment to links\n\n    This function converts strings that look like URLs, domain names and email\n    addresses in text that may be an HTML fragment to links, while preserving:\n\n    1. links already in the string\n    2. urls found in attributes\n    3. email addresses\n\n    linkify does a best-effort approach and tries to recover from bad\n    situations due to crazy text.\n\n    '

    def __init__(self, callbacks=DEFAULT_CALLBACKS, skip_tags=None, parse_email=False, url_re=URL_RE, email_re=EMAIL_RE, recognized_tags=html5lib_shim.HTML_TAGS):
        """Creates a Linker instance

        :arg list callbacks: list of callbacks to run when adjusting tag attributes;
            defaults to ``bleach.linkifier.DEFAULT_CALLBACKS``

        :arg list skip_tags: list of tags that you don't want to linkify the
            contents of; for example, you could set this to ``['pre']`` to skip
            linkifying contents of ``pre`` tags

        :arg bool parse_email: whether or not to linkify email addresses

        :arg re url_re: url matching regex

        :arg re email_re: email matching regex

        :arg list-of-strings recognized_tags: the list of tags that linkify knows about;
            everything else gets escaped

        :returns: linkified text as unicode

        """
        self.callbacks = callbacks
        self.skip_tags = skip_tags
        self.parse_email = parse_email
        self.url_re = url_re
        self.email_re = email_re
        self.parser = html5lib_shim.BleachHTMLParser(tags=recognized_tags,
          strip=False,
          consume_entities=True,
          namespaceHTMLElements=False)
        self.walker = html5lib_shim.getTreeWalker('etree')
        self.serializer = html5lib_shim.BleachHTMLSerializer(quote_attr_values='always',
          omit_optional_tags=False,
          sanitize=False,
          alphabetical_attributes=False)

    def linkify(self, text):
        """Linkify specified text

        :arg str text: the text to add links to

        :returns: linkified text as unicode

        :raises TypeError: if ``text`` is not a text type

        """
        if not isinstance(text, six.string_types):
            raise TypeError('argument must be of text type')
        text = force_unicode(text)
        if not text:
            return ''
        else:
            dom = self.parser.parseFragment(text)
            filtered = LinkifyFilter(source=(self.walker(dom)),
              callbacks=(self.callbacks),
              skip_tags=(self.skip_tags),
              parse_email=(self.parse_email),
              url_re=(self.url_re),
              email_re=(self.email_re))
            return self.serializer.render(filtered)


class LinkifyFilter(html5lib_shim.Filter):
    __doc__ = 'html5lib filter that linkifies text\n\n    This will do the following:\n\n    * convert email addresses into links\n    * convert urls into links\n    * edit existing links by running them through callbacks--the default is to\n      add a ``rel="nofollow"``\n\n    This filter can be used anywhere html5lib filters can be used.\n\n    '

    def __init__(self, source, callbacks=None, skip_tags=None, parse_email=False, url_re=URL_RE, email_re=EMAIL_RE):
        """Creates a LinkifyFilter instance

        :arg TreeWalker source: stream

        :arg list callbacks: list of callbacks to run when adjusting tag attributes;
            defaults to ``bleach.linkifier.DEFAULT_CALLBACKS``

        :arg list skip_tags: list of tags that you don't want to linkify the
            contents of; for example, you could set this to ``['pre']`` to skip
            linkifying contents of ``pre`` tags

        :arg bool parse_email: whether or not to linkify email addresses

        :arg re url_re: url matching regex

        :arg re email_re: email matching regex

        """
        super(LinkifyFilter, self).__init__(source)
        self.callbacks = callbacks or []
        self.skip_tags = skip_tags or []
        self.parse_email = parse_email
        self.url_re = url_re
        self.email_re = email_re

    def apply_callbacks(self, attrs, is_new):
        """Given an attrs dict and an is_new bool, runs through callbacks

        Callbacks can return an adjusted attrs dict or ``None``. In the case of
        ``None``, we stop going through callbacks and return that and the link
        gets dropped.

        :arg dict attrs: map of ``(namespace, name)`` -> ``value``

        :arg bool is_new: whether or not this link was added by linkify

        :returns: adjusted attrs dict or ``None``

        """
        for cb in self.callbacks:
            attrs = cb(attrs, is_new)
            if attrs is None:
                return

        return attrs

    def extract_character_data(self, token_list):
        """Extracts and squashes character sequences in a token stream"""
        out = []
        for token in token_list:
            token_type = token['type']
            if token_type in ('Characters', 'SpaceCharacters'):
                out.append(token['data'])

        return ''.join(out)

    def handle_email_addresses(self, src_iter):
        """Handle email addresses in character tokens"""
        for token in src_iter:
            if token['type'] == 'Characters':
                text = token['data']
                new_tokens = []
                end = 0
                for match in self.email_re.finditer(text):
                    if match.start() > end:
                        new_tokens.append({'type':'Characters', 
                         'data':text[end:match.start()]})
                    else:
                        attrs = {(None, 'href'): 'mailto:%s' % match.group(0), 
                         '_text': match.group(0)}
                        attrs = self.apply_callbacks(attrs, True)
                        if attrs is None:
                            new_tokens.append({'type':'Characters', 
                             'data':match.group(0)})
                        else:
                            _text = attrs.pop('_text', '')
                            attrs = alphabetize_attributes(attrs)
                            new_tokens.extend([
                             {'type':'StartTag', 
                              'name':'a',  'data':attrs},
                             {'type':'Characters', 
                              'data':force_unicode(_text)},
                             {'type':'EndTag', 
                              'name':'a'}])
                    end = match.end()

                if new_tokens:
                    if end < len(text):
                        new_tokens.append({'type':'Characters',  'data':text[end:]})
                    for new_token in new_tokens:
                        yield new_token

                    continue
            yield token

    def strip_non_url_bits(self, fragment):
        """Strips non-url bits from the url

        This accounts for over-eager matching by the regex.

        """
        prefix = suffix = ''
        while fragment:
            if fragment.startswith('('):
                prefix = prefix + '('
                fragment = fragment[1:]
                if fragment.endswith(')'):
                    suffix = ')' + suffix
                    fragment = fragment[:-1]
            else:
                if fragment.endswith(')'):
                    if '(' not in fragment:
                        fragment = fragment[:-1]
                        suffix = ')' + suffix
                        continue
                if fragment.endswith(','):
                    fragment = fragment[:-1]
                    suffix = ',' + suffix
                elif fragment.endswith('.'):
                    fragment = fragment[:-1]
                    suffix = '.' + suffix
                else:
                    break

        return (
         fragment, prefix, suffix)

    def handle_links(self, src_iter):
        """Handle links in character tokens"""
        in_a = False
        for token in src_iter:
            if in_a:
                if token['type'] == 'EndTag':
                    if token['name'] == 'a':
                        in_a = False
                yield token
                continue
            else:
                if token['type'] == 'StartTag':
                    if token['name'] == 'a':
                        in_a = True
                        yield token
                        continue
            if token['type'] == 'Characters':
                text = token['data']
                new_tokens = []
                end = 0
                for match in self.url_re.finditer(text):
                    if match.start() > end:
                        new_tokens.append({'type':'Characters', 
                         'data':text[end:match.start()]})
                    else:
                        url = match.group(0)
                        prefix = suffix = ''
                        url, prefix, suffix = self.strip_non_url_bits(url)
                        if PROTO_RE.search(url):
                            href = url
                        else:
                            href = 'http://%s' % url
                    attrs = {(None, 'href'): href, 
                     '_text': url}
                    attrs = self.apply_callbacks(attrs, True)
                    if attrs is None:
                        new_tokens.append({'type':'Characters', 
                         'data':prefix + url + suffix})
                    else:
                        if prefix:
                            new_tokens.append({'type':'Characters', 
                             'data':prefix})
                        _text = attrs.pop('_text', '')
                        attrs = alphabetize_attributes(attrs)
                        new_tokens.extend([
                         {'type':'StartTag', 
                          'name':'a',  'data':attrs},
                         {'type':'Characters', 
                          'data':force_unicode(_text)},
                         {'type':'EndTag', 
                          'name':'a'}])
                    if suffix:
                        new_tokens.append({'type':'Characters', 
                         'data':suffix})
                    end = match.end()

                if new_tokens:
                    if end < len(text):
                        new_tokens.append({'type':'Characters',  'data':text[end:]})
                    for new_token in new_tokens:
                        yield new_token

                    continue
            yield token

    def handle_a_tag(self, token_buffer):
        """Handle the "a" tag

        This could adjust the link or drop it altogether depending on what the
        callbacks return.

        This yields the new set of tokens.

        """
        a_token = token_buffer[0]
        if a_token['data']:
            attrs = a_token['data']
        else:
            attrs = {}
        text = self.extract_character_data(token_buffer)
        attrs['_text'] = text
        attrs = self.apply_callbacks(attrs, False)
        if attrs is None:
            yield {'type':'Characters', 
             'data':text}
        else:
            new_text = attrs.pop('_text', '')
            a_token['data'] = alphabetize_attributes(attrs)
            if text == new_text:
                yield a_token
                for mem in token_buffer[1:]:
                    yield mem

            else:
                yield a_token
                yield {'type':'Characters',  'data':force_unicode(new_text)}
                yield token_buffer[(-1)]

    def __iter__(self):
        in_a = False
        in_skip_tag = None
        token_buffer = []
        for token in super(LinkifyFilter, self).__iter__():
            if in_a:
                if token['type'] == 'EndTag':
                    if token['name'] == 'a':
                        token_buffer.append(token)
                        for new_token in self.handle_a_tag(token_buffer):
                            yield new_token

                        in_a = False
                        token_buffer = []
                token_buffer.append(token)
                continue
            if token['type'] in ('StartTag', 'EmptyTag'):
                if token['name'] in self.skip_tags:
                    in_skip_tag = token['name']
                elif token['name'] == 'a':
                    in_a = True
                    token_buffer.append(token)
                    continue
            else:
                if in_skip_tag and self.skip_tags:
                    if token['type'] == 'EndTag':
                        if token['name'] == in_skip_tag:
                            in_skip_tag = None
                else:
                    if not in_a and not in_skip_tag and token['type'] == 'Characters':
                        new_stream = iter([token])
                        if self.parse_email:
                            new_stream = self.handle_email_addresses(new_stream)
                        new_stream = self.handle_links(new_stream)
                        for token in new_stream:
                            yield token

                        continue
                yield token