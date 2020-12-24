# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.7/site-packages/guessit/transfo/guess_filetype.py
# Compiled at: 2013-03-18 16:30:48
from __future__ import unicode_literals
from guessit import Guess
from guessit.patterns import subtitle_exts, video_exts, episode_rexps, find_properties, compute_canonical_form
from guessit.date import valid_year
from guessit.textutils import clean_string
import os.path, re, mimetypes, logging
log = logging.getLogger(__name__)
MOVIES = [
 b'OSS 117']
SERIES = [b'Band of Brothers']
MOVIES = [ m.lower() for m in MOVIES ]
SERIES = [ s.lower() for s in SERIES ]

def guess_filetype(mtree, filetype):
    filetype_container = [
     filetype]
    other = {}
    filename = mtree.string

    def upgrade_episode():
        if filetype_container[0] == b'video':
            filetype_container[0] = b'episode'
        elif filetype_container[0] == b'subtitle':
            filetype_container[0] = b'episodesubtitle'

    def upgrade_movie():
        if filetype_container[0] == b'video':
            filetype_container[0] = b'movie'
        elif filetype_container[0] == b'subtitle':
            filetype_container[0] = b'moviesubtitle'

    def upgrade_subtitle():
        if b'movie' in filetype_container[0]:
            filetype_container[0] = b'moviesubtitle'
        elif b'episode' in filetype_container[0]:
            filetype_container[0] = b'episodesubtitle'
        else:
            filetype_container[0] = b'subtitle'

    def upgrade(type=b'unknown'):
        if filetype_container[0] == b'autodetect':
            filetype_container[0] = type

    fileext = os.path.splitext(filename)[1][1:].lower()
    if fileext in subtitle_exts:
        upgrade_subtitle()
        other = {b'container': fileext}
    else:
        if fileext in video_exts:
            upgrade(type=b'video')
            other = {b'container': fileext}
        else:
            upgrade(type=b'unknown')
            other = {b'extension': fileext}
        folder_rexps = [
         (
          b'Movies?', upgrade_movie),
         (
          b'Tv[ _-]?Shows?', upgrade_episode),
         (
          b'Series', upgrade_episode)]
        for frexp, upgrade_func in folder_rexps:
            frexp = re.compile(frexp, re.IGNORECASE)
            for pathgroup in mtree.children:
                if frexp.match(pathgroup.value):
                    upgrade_func()

        fname = clean_string(filename).lower()
        for m in MOVIES:
            if m in fname:
                upgrade_movie()

        for s in SERIES:
            if s in fname:
                upgrade_episode()

    if filetype_container[0] in ('video', 'subtitle'):
        for rexp, _, _ in episode_rexps:
            match = re.search(rexp, filename, re.IGNORECASE)
            if match:
                upgrade_episode()
                break

        match = re.search(b'[^0-9]([0-9]{3,4})[^0-9]', filename)
        if match:
            fullnumber = int(match.group()[1:-1])
            epnumber = fullnumber % 100
            possible = True
            if epnumber > 40:
                possible = False
            if valid_year(fullnumber):
                possible = False
            if possible:
                upgrade_episode()
        for prop, value, _, _ in find_properties(filename):
            log.debug(b'prop: %s = %s' % (prop, value))
            if prop == b'episodeFormat':
                upgrade_episode()
                break
            elif compute_canonical_form(b'format', value) == b'DVB':
                upgrade_episode()
                break

        if b'tvu.org.ru' in filename:
            upgrade_episode()
        upgrade_movie()
    filetype = filetype_container[0]
    return (filetype, other)


def process(mtree, filetype=b'autodetect'):
    filetype, other = guess_filetype(mtree, filetype)
    mtree.guess.set(b'type', filetype, confidence=1.0)
    log.debug(b'Found with confidence %.2f: %s' % (1.0, mtree.guess))
    filetype_info = Guess(other, confidence=1.0)
    mime, _ = mimetypes.guess_type(mtree.string, strict=False)
    if mime is not None:
        filetype_info.update({b'mimetype': mime}, confidence=1.0)
    node_ext = mtree.node_at((-1, ))
    node_ext.guess = filetype_info
    log.debug(b'Found with confidence %.2f: %s' % (1.0, node_ext.guess))
    return