# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.cygwin-2.2.1-i686/egg/tvrenamer/core/parser.py
# Compiled at: 2015-11-08 18:31:47
from tvrenamer.core import patterns

def _get_season_no(match, namedgroups):
    if 'seasonnumber' in namedgroups:
        return int(match.group('seasonnumber'))
    return 1


def _get_episode_by_boundary(match):
    start = int(match.group('episodenumberstart'))
    end = int(match.group('episodenumberend'))
    if start > end:
        start, end = end, start
    return list(range(start, end + 1))


def _get_episodes(match, namedgroups):
    if 'episodenumberstart' in namedgroups:
        return _get_episode_by_boundary(match)
    else:
        return [
         int(match.group('episodenumber'))]


def parse_filename(filename):
    """Parse media filename for metadata.

    :param str filename: the name of media file
    :returns: dict of metadata attributes found in filename
              or None if no matching expression.
    :rtype: dict
    """
    _patterns = patterns.get_expressions()
    result = {}
    for cmatcher in _patterns:
        match = cmatcher.match(filename)
        if match:
            namedgroups = match.groupdict().keys()
            result['pattern'] = cmatcher.pattern
            result['series_name'] = match.group('seriesname')
            result['season_number'] = _get_season_no(match, namedgroups)
            result['episode_numbers'] = _get_episodes(match, namedgroups)
            break
    else:
        result = None

    return result