# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/luto/snotes20/osf.py/venv/lib/python3.4/site-packages/osf/objectify.py
# Compiled at: 2015-08-23 11:29:24
# Size of source mod 2**32: 4300 bytes
from .grammar import *
from .timeutils import hhmmss_to_milliseconds
from .classes import OSFLine, ParentlessNoteError

def objectify_line_time(line, osf_line, time_offset=0):
    time_hhmmss = line.find(HHMMSSTime)
    time_unix = line.find(UnixTime)
    if time_hhmmss:
        hun = time_hhmmss.find(HHMMSSHundredthsComponent)
        hun_val = 0
        if hun:
            hun_val = hun.string
        osf_line.time = hhmmss_to_milliseconds(time_hhmmss.find(HHMMSSTimeHourComponent).string, time_hhmmss.find(HHMMSSTimeMinuteComponent).string, time_hhmmss.find(HHMMSSSecondComponent).string, hun_val)
    else:
        if time_unix:
            osf_line.time = (int(time_unix.string) - time_offset) * 1000
        else:
            osf_line.time = None


def objectify_line_text(line, osf_line):
    osf_line.text = line.find(Text).string


def objectify_line_link(line, osf_line):
    link = line.find(Link)
    if link:
        osf_line.link = link[1].string


def f7(seq):
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]


def objectify_line_tags(line, osf_line):
    tags = line.find_all(Tag)
    osf_line.tags = f7([tag[1].string for tag in tags])


def objectify_line(line, time_offset=0):
    osf_line = OSFLine()
    if hasattr(line, '_line'):
        osf_line._line = line._line
    objectify_line_time(line, osf_line, time_offset)
    objectify_line_text(line, osf_line)
    objectify_line_link(line, osf_line)
    objectify_line_tags(line, osf_line)
    return (
     osf_line, len(line.find_all(Indentation)))


def objectify_lines(lines):
    if not lines:
        return []
    time_offset = 0
    if not isinstance(lines[0], ParseError):
        unix_time = lines[0].find(UnixTime)
        if unix_time:
            time_offset = int(unix_time.string)
    notes = []
    depth_note = {}
    max_depth = 0
    last_depth = 0
    inside_chapter = False
    for line in lines:
        if isinstance(line, modgrammar.ParseError):
            notes.append(line)
        else:
            note, n_depth = objectify_line(line, time_offset)
            if inside_chapter:
                if 'c' not in note.tags and 'chapter' not in note.tags:
                    n_depth += 1
            if n_depth == 0:
                if 'c' in note.tags or 'chapter' in note.tags:
                    inside_chapter = True
                    depth_note[0] = note
            if n_depth == 0:
                notes.append(note)
            else:
                parent_depth = n_depth - 1
                while parent_depth not in depth_note and parent_depth > -1:
                    parent_depth -= 1

                if parent_depth < 0:
                    if not hasattr(note, '_line'):
                        raise ParentlessNoteError()
                    else:
                        notes.append(ParentlessNoteError(note._line))
                    continue
                else:
                    depth_note[parent_depth].notes.append(note)
                depth_note[n_depth] = note
                if n_depth < last_depth:
                    for d in range(n_depth + 1, max_depth + 1):
                        if d in depth_note:
                            del depth_note[d]
                            continue

                if n_depth > max_depth:
                    max_depth = n_depth
            last_depth = n_depth

    return notes