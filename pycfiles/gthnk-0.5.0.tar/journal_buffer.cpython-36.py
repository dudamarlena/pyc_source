# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./gthnk/adaptors/journal_buffer.py
# Compiled at: 2017-11-21 20:58:03
# Size of source mod 2**32: 3876 bytes
import re, io, datetime, sys
from collections import defaultdict
from gthnk import models

def split_filename_list(filename_str):
    """
    """
    return [x.strip() for x in filename_str.split(',')]


class JournalBuffer(object):
    __doc__ = '\n    A Journal Buffer is an in-memory representation of Journal entries.\n    '

    def __init__(self):
        """
        """
        PY3 = sys.version_info[0] > 2
        if PY3:
            self.entries = defaultdict(lambda : defaultdict(str))
        else:
            self.entries = defaultdict(lambda : defaultdict(unicode))
        self.re_day = re.compile('^(\\d\\d\\d\\d-\\d\\d-\\d\\d)\\s*$')
        self.re_time = re.compile('^(\\d\\d\\d\\d)\\s*$')
        self.re_time_tag = re.compile('^(\\d\\d\\d\\d)\\s(\\w+)\\s*$')
        self.re_newlines = re.compile('\\n\\n\\n', re.MULTILINE)

    def parse(self, raw_text):
        """
        parse a Journal-encoded text string; add content to an Entries dictionary, with timestamp.
        """
        current_day = None
        current_time = None
        for line in raw_text.splitlines():
            line = line.rstrip()
            match_day = self.re_day.match(line)
            match_time = self.re_time.match(line)
            match_time_tag = self.re_time_tag.match(line)
            tag = ''
            if match_day:
                current_day = match_day.group(1)
                current_time = None
            else:
                if not current_day:
                    if line == '':
                        continue
                else:
                    if not current_time:
                        if line == '':
                            continue
                    if current_time:
                        if line == '' and current_time not in self.entries[current_day]:
                            continue
                if match_time:
                    current_time = match_time.group(1)
                else:
                    if match_time_tag:
                        current_time = match_time_tag.group(1)
                        tag = match_time_tag.group(2)
                    else:
                        self.entries[current_day][current_time] += '{0}\n'.format(line)

        for day in self.entries:
            for timestamp in self.entries[day]:
                self.entries[day][timestamp] = self.entries[day][timestamp].rstrip()

    def get_entries(self):
        """
        """
        return self.entries

    def save_entries(self):
        """
        add the current entries to the database
        """
        for day in self.entries.keys():
            for timestamp in self.entries[day].keys():
                try:
                    time_obj = datetime.datetime.strptime('{} {}'.format(day, timestamp), '%Y-%m-%d %H%M')
                except:
                    import flask
                    flask.current_app.logger.warn("Cannot determine day for '{}' '{}'".format(day, timestamp))
                    continue

                models.Entry.create(timestamp=time_obj,
                  content=(self.entries[day][timestamp]))

    def dump(self):
        """
        """
        import json
        return json.dumps(self.get_entries())


class TextFileJournalBuffer(JournalBuffer):
    __doc__ = '\n    provide functions for loading content from a text file\n    '

    def process_one(self, filename):
        with io.open(filename, 'r', encoding='utf-8') as (f):
            contents = f.read()
        self.parse(contents)

    def process_list(self, filename_list):
        for filename in filename_list:
            self.process_one(filename)