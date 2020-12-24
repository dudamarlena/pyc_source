# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/buzz/html.py
# Compiled at: 2020-05-03 14:22:19
# Size of source mod 2**32: 2551 bytes
import re
from collections import OrderedDict
from html.parser import HTMLParser
from buzz.utils import cast
SPEAKER_REGEX = re.compile('^([A-Z0-9-_]{1,30}):\\s*', re.MULTILINE)

class MetadataStripper(HTMLParser):
    """MetadataStripper"""

    def __init__(self, speakers=True):
        super().__init__()
        self.text = str()
        self.speakers = speakers

    def handle_data(self, data):
        if not self.getpos()[1]:
            if self.speakers:
                data = re.sub(SPEAKER_REGEX, '', data)
        self.text += data


class InputParser(HTMLParser):
    """InputParser"""

    def __init__(self, speakers=True):
        super().__init__()
        self.tmp = None
        self.result = OrderedDict()
        self.sent_meta = dict()
        self.text = None
        self.num_elements = 0
        self.num_done = 0
        self.speakers = speakers
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
        """
        data is the string of plain text
        """
        offset = self.getpos()[1]
        text_before_this = self.text[:offset]
        nth = text_before_this.count(data)
        if not offset:
            if self.speakers:
                found_speaker = re.search(SPEAKER_REGEX, data)
                if found_speaker:
                    self.sent_meta['speaker'] = found_speaker.group(1)
        if self.tmp:
            self.result[(data, nth)] = self.tmp
            self.tmp = None