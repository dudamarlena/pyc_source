# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/buzz/html.py
# Compiled at: 2019-08-16 16:42:30
# Size of source mod 2**32: 2504 bytes
import re
from html.parser import HTMLParser
from collections import OrderedDict
from buzz.utils import cast

class MetadataStripper(HTMLParser):
    __doc__ = '\n    Strip HTML/XML properly\n    '

    def __init__(self):
        super().__init__()
        self.text = str()

    def handle_data(self, data):
        regex = '^[A-Za-z0-9-_]{1,40}:\\s*'
        idregex = re.compile(regex, re.MULTILINE)
        if not self.getpos()[1]:
            data = re.sub(idregex, '', data)
        self.text += data


class InputParser(HTMLParser):
    __doc__ = '\n    Get metadata out of a line of text\n    '

    def __init__(self):
        super().__init__()
        self.tmp = None
        self.result = OrderedDict()
        self.sent_meta = dict()
        self.text = None
        self.num_elements = 0
        self.num_done = 0
        self.stripper = MetadataStripper()

    def _has_sent_meta(self):
        if '<meta' not in self.text:
            return False
        n_meta = self.text.count('<meta')
        n_end = self.text.count('</meta')
        return bool(n_meta - n_end)

    def handle_starttag(self, tag, attrs):
        self.tmp = dict()
        if tag in {'metadata', 'meta'}:
            for k, v in attrs:
                self.tmp[k.strip().replace('-', '_')] = cast(v)

        is_last = self.num_elements == self.num_done + 1
        if is_last:
            if self._has_sent_meta():
                self.sent_meta = {**(self.tmp), **(self.sent_meta)}
        self.num_done += 1

    def feed(self, text, *args, **kwargs):
        self.text = text
        self.stripper.feed(text)
        self.clean_text = self.stripper.text
        self.num_elements = text.count('<meta')
        return (super().feed)(text, *args, **kwargs)

    def handle_data(self, data):
        regex = '^([A-Za-z0-9-_]{1,40}):\\s*'
        idregex = re.compile(regex, re.MULTILINE)
        offset = self.getpos()[1]
        text_before_this = self.text[:offset]
        nth = text_before_this.count(data)
        if not offset:
            found_speaker = re.search(idregex, data)
            if found_speaker:
                self.sent_meta['speaker'] = found_speaker.group(1)
        if self.tmp:
            self.result[(data, nth)] = self.tmp
            self.tmp = None