# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/srtmerge/srt.py
# Compiled at: 2014-01-14 16:27:02
__author__ = 'wistful'
import codecs, re, sys
from collections import namedtuple, Sequence, Iterable
if sys.version_info[0] > 2:
    unicode = str
from chardet.universaldetector import UniversalDetector
SubRecord = namedtuple('SubRecord', ['start', 'finish', 'text'])
DEFAULT_ENCODING = 'utf-8'

class Subtitles(Sequence, Iterable):
    """
    Class represents container for subtitle records.
    """

    def __init__(self):
        self.__records = []

    def append(self, subrecord):
        rec = SubRecord(subrecord.start, subrecord.finish, subrecord.text)
        self.__records.append(rec)

    def __iter__(self):
        return iter(self.__records[:])

    def __getitem__(self, index):
        return self.__records[index]

    def __len__(self):
        return len(self.__records)

    def __add__(self, other):

        def repack_record(rec, index):
            return SubRecord(rec.start, rec.finish, (index, rec.text))

        subs = []
        new_obj = Subtitles()
        for (index, instance) in enumerate((self, other)):
            subs.extend([ repack_record(rec, index) for rec in instance ])

        subs.sort(key=lambda item: item.start)
        index_start = 0
        while index_start < len(subs):
            (start, finish, rec_text) = subs[index_start]
            text = [rec_text]
            index_end = index_start + 1
            while index_end < len(subs) and subs[index_end].start < finish:
                rec = subs[index_end]
                text.append(rec.text)
                finish = max(finish, start + (rec.finish - rec.start) * 2 / 3)
                index_end += 1

            text = ('').join(map(lambda item: item[1], sorted(text)))
            new_obj.append(SubRecord(start, finish, text))
            if index_end < len(subs):
                index_start = index_end
                continue
            else:
                break

        return new_obj


class SrtFormatError(Exception):

    def __init__(self, message):
        self.message = message

    def __str__(self):
        return repr(self.message)


def parse_time(str_time):
    """
    convert string format of start-finish to integer(ms) format
    >>> parse_time("00:14:33,460 --> 00:14:35,419")
    (873460, 875419)
    """

    def get_ms(hours, minutes, seconds, miliseconds):
        all_seconds = seconds + minutes * 60 + hours * 60 * 60
        return all_seconds * 1000 + int(miliseconds)

    pattern_time = '(?P<h1>\\d+):(?P<m1>\\d+):(?P<s1>\\d+),(?P<ms1>\\d+)\\W*-->\\W*(?P<h2>\\d+):(?P<m2>\\d+):(?P<s2>\\d+),(?P<ms2>\\d+)$'
    try:
        d = re.match(pattern_time, str_time.strip()).groupdict()
    except:
        message = "Invalid string format '{0}', expect hh:mm:ss,msc --> hh:mm:ss,msc"
        raise SrtFormatError(message.format(str_time))

    d = dict(zip(d.keys(), map(int, d.values())))
    result = (get_ms(d['h1'], d['m1'], d['s1'], d['ms1']),
     get_ms(d['h2'], d['m2'], d['s2'], d['ms2']))
    return result


def ms2time(ms):
    """
    convert msc to string format
    >>> ms2time(233243)
    '00:03:53,243'
    >>> ms2time(442)
    '00:00:00,442'
    """
    it = int(ms / 1000)
    ms = ms - it * 1000
    ss = it % 60
    mm = (it - ss) / 60 % 60
    hh = (it - mm * 60 - ss) / 3600 % 60
    return '%02d:%02d:%02d,%03d' % (hh, mm, ss, ms)


def parse_ms(start, finish):
    """
    convert msc representation to string format
    >>> parse_ms(442, 233243)
    '00:00:00,442 --> 00:03:53,243'
    """
    return '%s --> %s' % (ms2time(start), ms2time(finish))


def detect_encoding(file_path):
    with open(file_path, 'rb') as (f):
        u = UniversalDetector()
        for line in f:
            u.feed(line)

        u.close()
        return u.result['encoding']


def srtmerge(in_srt_files, out_srt, offset=0, use_chardet=False, encoding=DEFAULT_ENCODING):
    subs = Subtitles()
    for file_path in in_srt_files:
        in_encoding = detect_encoding(file_path) if use_chardet else DEFAULT_ENCODING
        subs = subs + subreader(file_path, encoding=in_encoding)

    subwriter(out_srt, subs, offset, encoding)


def subreader(file_path, encoding=DEFAULT_ENCODING):
    """
    Reads srt-file and returns Subtitles instance.
    Args:
        file_path: full path to srt-file
    """
    subtitles = Subtitles()
    pattern_index = '^\\d+$'
    start = finish = None
    text = []
    with codecs.open(file_path, 'rb') as (fd):
        for line in fd:
            line = line.decode(encoding).strip()
            if re.match(pattern_index, line):
                if start and finish:
                    subtitles.append(SubRecord(start, finish, text=unicode('{0}\n').format(('\n').join(text))))
                    start = finish = None
                    text = []
            elif '-->' in line:
                (start, finish) = parse_time(line)
            elif line:
                text.append(line)

    if start and finish:
        subtitles.append(SubRecord(start, finish, text=unicode('{0}\n').format(('\n').join(text))))
    return subtitles


def subwriter(filepath, subtitles, offset=0, encoding=DEFAULT_ENCODING):
    """Writes Subtitles into srt-file.

    Args:
        filepath: path to srt-file
        subtitles: Subtitles instance
    """
    line = unicode('{index}\n{time}\n{text}\n')
    with codecs.open(filepath, 'w', encoding=encoding) as (fd):
        for (index, rec) in enumerate(subtitles, 1):
            text = line.format(index=unicode(index), time=parse_ms(rec.start + offset, rec.finish + offset), text=rec.text)
            fd.write(text)


if __name__ == '__main__':
    import doctest
    print doctest.testmod()