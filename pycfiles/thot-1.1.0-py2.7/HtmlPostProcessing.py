# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/thot/plugins/HtmlPostProcessing.py
# Compiled at: 2013-03-05 21:43:25
import logging, re
from HTMLParser import HTMLParser
from thot.utils import partition
try:
    from StringIO import StringIO
except:
    from io import StringIO

try:
    import pyphen
    has_pyphen = True
except:
    has_pyphen = False
    logging.warn('Pyphen has not been found and cannot be used for hyphenation.')

try:
    from wordaxe.DCWHyphenator import DCWHyphenator
    has_wordaxe = True
    wordaxe_languages = ['da', 'de', 'de_DE', 'en', 'en_GB', 'en_US', 'ru']
except:
    has_wordaxe = False
    logging.warn('Wordaxe has not been found and cannot be used for hyphenation.')

__all__ = [
 'HtmlPostProcessor']

def wordaxe_hyphenation_wrapper(hyphenator, word):
    word_obj = hyphenator.hyphenate(unicode(word))
    partitions = partition(word, [ h.indx for h in word_obj.hyphenations ])
    marked_word = HtmlPostProcessor.html_hypenation_mark.join(partitions)
    return marked_word


class HtmlPostProcessor(HTMLParser):
    """Collector of HTML postprocessing functions.

    Extend or monkey-aptch this class to add more features to it.
    Unmodified it is the hub for hyphenation.
    """
    run_at = [
     'after_rendering']
    hyphenator = dict()
    hyphenator_f = dict()
    html_hypenation_mark = '\xad'
    dont_hyphenate_if_in = set(['head', 'pre', 'code', 'script', 'style'])
    word_detection_pattern = re.compile('\\w{5,}', re.UNICODE)

    def __init__(self, site, settings):
        HTMLParser.__init__(self)
        self.site = site
        self.site_settings = settings
        self.modified_contents = None
        self._reset_state(0)
        logging.debug('Plugin "%s" has been initalized.', self)
        return

    def after_rendering(self, page):
        """Entry point. Gets the rendered page as unicode string."""
        self._reset_state(buffer_size=len(page['rendered']) + 1024)
        self._page = page
        self.feed(page['rendered'])
        page['rendered'] = self.modified_contents.getvalue()

    def _reset_state(self, buffer_size):
        """This is called before handling every new page."""
        if self.modified_contents:
            self.modified_contents.close()
        self.modified_contents = StringIO(buffer_size) if buffer_size > 0 else None
        self.tag_path = []
        self._in_tag = None
        self._page = None
        self._warned_about_tag_mismatch = False
        self._language = []
        return

    def _get_hyphenator(self, lang):
        if lang in HtmlPostProcessor.hyphenator:
            return HtmlPostProcessor.hyphenator[lang]
        else:
            if has_wordaxe and lang in wordaxe_languages:
                h = DCWHyphenator(lang, minWordLength=3)
                HtmlPostProcessor.hyphenator[lang] = h
                HtmlPostProcessor.hyphenator_f[lang] = lambda w: wordaxe_hyphenation_wrapper(h, w)
                return HtmlPostProcessor.hyphenator[lang]
            else:
                if has_pyphen and lang in pyphen.LANGUAGES:
                    h = pyphen.Pyphen(lang=lang)
                    HtmlPostProcessor.hyphenator[lang] = h
                    HtmlPostProcessor.hyphenator_f[lang] = lambda w: h.inserted(w, hyphen=HtmlPostProcessor.html_hypenation_mark)
                    return HtmlPostProcessor.hyphenator[lang]
                return

            return

    def _hyphenate(self, text):
        pathlength, lang = self._language[(-1)]
        hyphenator = self._get_hyphenator(lang)
        if hyphenator:
            return HtmlPostProcessor.word_detection_pattern.sub(lambda matchobj: HtmlPostProcessor.hyphenator_f[lang](matchobj.group(0)), text)
        else:
            return text

    def handle_starttag(self, tag, attrs):
        self.tag_path.append(tag)
        self._in_tag = tag
        if attrs:
            d = dict(attrs)
            if 'lang' in d or 'xml:lang' in d:
                position = len(self.tag_path)
                language_tag = d['lang'] if 'lang' in d else d['xml:lang']
                self._language.append((position, language_tag))
        self._store_tag(tag, attrs)

    def handle_endtag(self, tag):
        got_tag = tag
        expected_tag = self.tag_path[(-1)]
        if got_tag == expected_tag:
            self.tag_path.pop()
            self._in_tag = self.tag_path[(-1)] if len(self.tag_path) > 1 else None
        else:
            stripped_path = []
            if got_tag in self.tag_path:
                while True:
                    tmp = self.tag_path.pop()
                    if tmp != got_tag:
                        stripped_path.append(tmp)
                    else:
                        break

                stripped_path.reverse()
            if not self._warned_about_tag_mismatch:
                self._warned_about_tag_mismatch = True
                logging.warn('Got tail of tag "%s" but have been expecting end of "%s" in "%s"', got_tag, expected_tag, self._page['output_path'].decode('utf-8'))
                logging.debug('"%s": starting from %r these tags have been stripped from stack: %r', self._page['output_path'].decode('utf-8'), self.tag_path, [got_tag] + stripped_path)
        self._store_tag(tag, None, prefix='</')
        if self._language:
            while self._language:
                pathlength, lang = self._language[(-1)]
                if len(self.tag_path) < pathlength:
                    self._language.pop()
                else:
                    break

        return

    def handle_startendtag(self, tag, attrs):
        self._in_tag = tag
        self._store_tag(tag, attrs, suffix=' />')

    def handle_decl(self, raw):
        self.modified_contents.write('<!' + raw + '>')

    def handle_pi(self, raw):
        self.modified_contents.write('<?' + raw + '>')

    def unknown_decl(self, raw):
        self.modified_contents.write('<![' + raw + ']>')

    def handle_entityref(self, raw):
        self.modified_contents.write('&' + raw + ';')

    def handle_charref(self, raw):
        self.modified_contents.write('&#' + raw + ';')

    def handle_comment(self, raw):
        self.modified_contents.write('<!--')
        self.modified_contents.write(raw)
        self.modified_contents.write('-->')

    def _store_tag(self, tag, attrs, prefix='<', suffix='>'):
        self.modified_contents.write(prefix)
        self.modified_contents.write(tag)
        if attrs:
            for k, v in attrs:
                self.modified_contents.write(' ')
                self.modified_contents.write(k)
                self.modified_contents.write('="')
                self.modified_contents.write(v)
                self.modified_contents.write('"')

        self.modified_contents.write(suffix)

    def handle_data(self, data):
        if len(self._language) == 0 or HtmlPostProcessor.dont_hyphenate_if_in.intersection(self.tag_path) or not data.strip():
            self.modified_contents.write(data)
        else:
            self.modified_contents.write(self._hyphenate(data))