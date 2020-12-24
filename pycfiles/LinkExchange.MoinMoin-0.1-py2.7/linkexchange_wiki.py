# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/linkexchange/MoinMoin/parser/linkexchange_wiki.py
# Compiled at: 2011-05-12 16:28:53
import re, logging
try:
    from MoinMoin.parser.text_moin_wiki import Parser as WikiParser
except ImportError:
    from MoinMoin.parser.wiki import Parser as WikiParser

from linkexchange.MoinMoin import support
log = logging.getLogger('linkexchange.MoinMoin')
Dependencies = [
 'time']

class Parser(WikiParser):
    """
    Parser to perform content filtering, e.g. calls platform.content_filter()
    on generated content.
    """
    Dependencies = Dependencies
    _fix_empty_span = re.compile('<span\\b[^>]*></span>', re.S)

    def format(self, formatter):
        request = self.request
        try:
            platform = request.cfg.linkexchange_platform
        except AttributeError:
            support.configure(request.cfg)
            platform = request.cfg.linkexchange_platform

        if platform is None:
            return WikiParser.format(self, formatter)
        else:
            content = request.redirectedOutput(WikiParser.format, self, formatter)
            content = self._fix_empty_span.sub('', content)
            content = content.replace('<<<>>>', '<!--<<<>>>-->')
            try:
                content = platform.content_filter(support.convert_request(request), content)
            except Exception as e:
                content += '<!-- Content filter error -->'
                log.error('Content filter error', exc_info=True)

            content = content.replace('<!--<<<>>>-->', '<<<>>>')
            request.write(content)
            return