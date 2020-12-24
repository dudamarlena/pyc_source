# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ana/dev/dexy-clean/dexy/filters/md.py
# Compiled at: 2020-03-18 15:12:33
# Size of source mod 2**32: 4559 bytes
from dexy.filter import DexyFilter
import dexy.exceptions, json, logging, markdown, re

class MarkdownFilter(DexyFilter):
    __doc__ = '\n    Runs a Markdown processor to convert markdown to HTML.\n\n    Markdown extensions can be enabled in your config:\n    http://packages.python.org/Markdown/extensions/index.html\n    '
    aliases = ['markdown']
    _settings = {'examples':[
      'markdown'], 
     'input-extensions':[
      '.*'], 
     'output-extensions':[
      '.html'], 
     'extensions':(
      'Which Markdown extensions to enable.', {'toc': {}})}

    def capture_markdown_logger(self):
        markdown_logger = logging.getLogger('MARKDOWN')
        markdown_logger.addHandler(self.doc.wrapper.log.handlers[(-1)])

    def initialize_markdown(self, *additional_extensions):
        extension_configs = self.setting('extensions')
        extensions = list(extension_configs.keys())
        dbg = 'Initializing Markdown with extensions: %s and extension configs: %s'
        self.log_debug(dbg % (json.dumps(extensions), json.dumps(extension_configs)))
        try:
            md = markdown.Markdown(extensions=(extensions + list(additional_extensions)),
              extension_configs=extension_configs)
        except ValueError as e:
            try:
                self.log_debug(e.message)
                if 'markdown.Extension' in e.message:
                    raise dexy.exceptions.UserFeedback("There's a problem with the markdown extensions you specified.")
                else:
                    raise
            finally:
                e = None
                del e

        except KeyError as e:
            try:
                raise dexy.exceptions.UserFeedback("Couldn't find a markdown extension option matching '%s'" % e.message)
            finally:
                e = None
                del e

        return md

    def process_text(self, input_text):
        self.capture_markdown_logger()
        md = self.initialize_markdown()
        return md.convert(input_text)


class MarkdownSlidesFilter(MarkdownFilter):
    __doc__ = '\n    Converts paragraphs to HTML and wrap each slide in a header and footer.\n    '
    aliases = ['slides']
    _settings = {'extensions':{'nl2br': {}}, 
     'added-in-version':'0.9.9.6', 
     'examples':[
      'slides'], 
     'comment-char':('Lines starting with this comment char will not show up in slides.', ';'), 
     'split':('String to use to split slides.', '\n\n\n'), 
     'slide-header':('Content to prepend to start of each slide.', '<section class="slide">'), 
     'slide-footer':('Content to append to end of each slide.', '</section>')}

    def process_text(self, input_text):
        self.capture_markdown_logger()
        md = self.initialize_markdown()
        slides = ''
        comment_regexp = '^%s(.*)$' % self.setting('comment-char')
        for counter, slide in enumerate(input_text.split(self.setting('split'))):
            slide = re.sub(comment_regexp, '', slide, flags=(re.MULTILINE))
            html = md.convert(slide)
            interp = {'number': counter + 1}
            header = self.setting('slide-header') % interp
            footer = self.setting('slide-footer') % interp
            slide_text = '\n%s\n%s\n%s\n' % (header, html, footer)
            slides += slide_text

        return slides


class MarkdownSpeakerNotesFilter(MarkdownSlidesFilter):
    __doc__ = '\n    Companion to slides filter which helps generate speaker notes.\n    '
    aliases = ['speakernotes']
    _settings = {'added-in-version':'1.0.7', 
     'comment-markdown':('Comment chars ; are replaced with this markdown. Use None to hide comments.', '> *')}

    def process_text(self, input_text):
        self.capture_markdown_logger()
        md = self.initialize_markdown()
        if self.setting('comment-markdown') is None:
            comment_regexp = '^%s(.*)$' % self.setting('comment-char')
            comments_removed = re.sub(comment_regexp, '', input_text, flags=(re.MULTILINE))
        else:
            comment_regexp = '^%s' % self.setting('comment-char')
            comments_removed = re.sub(comment_regexp, (self.setting('comment-markdown')), input_text, flags=(re.MULTILINE))
        return md.convert(comments_removed)