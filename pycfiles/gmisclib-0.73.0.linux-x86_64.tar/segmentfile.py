# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/gmisclib/segmentfile.py
# Compiled at: 2007-08-13 06:22:59
"""This parses a '.in' file from xwaves.   The '.in' files
show segmentation of an utterance.    segmentfile.parse(s)
takes a list of lines from such a file, and returns
three things:
* the title of the file (typically the utterance)
* a list of groups (a group is typically a word)
* a list of segments.

Groups include a list of the segments of which they are made,
along with a name and an index.
Segments contain a phoneme, a start/end time,
an index, and the group to which they belong.
"""

def _indented(s):
    return len(s) > 0 and (s[0] == '\t' or s[0] == ' ')


def _title(s):
    i = 0
    while s[i] == '*':
        i = i + 1

    return s[i:].lstrip()


class segment:

    def __init__(self, st, en, phn, si):
        self.start = st
        self.end = en
        self.phn = phn
        self.segidx = si
        self.group = None
        return

    def setgroup(self, g):
        self.group = g

    def __str__(self):
        return '<segment [%d]/%s[%d] %g-%g>' % (
         self.group.groupidx,
         self.phn, self.segidx,
         self.start, self.end)

    def __repr__(self):
        return self.__str__()


class group:

    def __init__(self, gi, gn):
        self.s = []
        self.groupidx = gi
        self.groupname = gn

    def add(self, seg):
        self.s.append(seg)

    def __str__(self):
        tmp = (', ').join(map(lambda x: x.__str__(), self.s))
        return '<group %s[%d] %s >' % (self.groupname, self.groupidx, tmp)

    def __repr__(self):
        return self.__str__()


def parse(l):
    """Parses a list of lines from an ESPS Xmark file (.in),
        and returns a tuple (title, list of groups, list of segments)."""
    pseg = []
    pg = []
    title = None
    last_t = None
    groupidx = 0
    curgroup = group(groupidx, '')
    segidx = -1
    for line in l:
        line = line.rstrip()
        if not _indented(line):
            if title is None and len(line) > 0 and line[0] == '*':
                title = _title(line)
            elif len(line) > 0:
                curgroup = group(groupidx, line)
                pg.append(curgroup)
                groupidx += 1
        else:
            ss = line.lstrip().split()
            if len(ss) != 2:
                continue
            t = float(ss[1])
            if last_t is not None:
                seg = segment(last_t, t, ss[0], segidx)
                seg.setgroup(curgroup)
                curgroup.add(seg)
                pseg.append(seg)
            last_t = t
            segidx += 1

    return (
     title, pg, pseg)


def read(f):
    """Read a ESPS Xmark (.in) file, and return information.  See parse()."""
    ii = open(f, 'rb')
    o = parse(ii.readlines())
    ii.close()
    return o


def test():
    teststring = [
     '** o cen s',
     'o',
     '           o          1.620417',
     'cen',
     '         Ccl          1.679583',
     '           C           1.76925',
     '           ^         1.8527499',
     '           N          1.941583',
     's\t',
     '           s         2.0380001',
     '']
    title, grp, seg = parse(teststring)
    assert title == 'o cen s'
    assert seg[0].phn == 'Ccl'
    assert seg[0].start == 1.620417
    assert seg[0].end == 1.679583
    assert seg[0].group.groupidx == 1
    assert seg[0].segidx == 0
    assert grp[0].groupidx == 0
    assert grp[0].groupname == 'o'
    for t in grp:
        for q in t.s:
            assert q.group == t

    assert len(seg) == 5
    assert len(grp) == 3


if __name__ == '__main__':
    test()