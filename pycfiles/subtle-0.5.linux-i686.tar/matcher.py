# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.7/site-packages/guessit/matcher.py
# Compiled at: 2013-03-18 16:30:48
from __future__ import unicode_literals
from guessit import PY3, u
from guessit.matchtree import MatchTree
import logging
log = logging.getLogger(__name__)

class IterativeMatcher(object):

    def __init__(self, filename, filetype=b'autodetect'):
        """An iterative matcher tries to match different patterns that appear
        in the filename.

        The 'filetype' argument indicates which type of file you want to match.
        If it is 'autodetect', the matcher will try to see whether it can guess
        that the file corresponds to an episode, or otherwise will assume it is
        a movie.

        The recognized 'filetype' values are:
        [ autodetect, subtitle, movie, moviesubtitle, episode, episodesubtitle ]

        The IterativeMatcher works mainly in 2 steps:

        First, it splits the filename into a match_tree, which is a tree of groups
        which have a semantic meaning, such as episode number, movie title,
        etc...

        The match_tree created looks like the following:

        0000000000000000000000000000000000000000000000000000000000000000000000000000000000 111
        0000011111111111112222222222222233333333444444444444444455555555666777777778888888 000
        0000000000000000000000000000000001111112011112222333333401123334000011233340000000 000
        __________________(The.Prestige).______.[____.HP.______.{__-___}.St{__-___}.Chaps].___
        xxxxxttttttttttttt               ffffff  vvvv    xxxxxx  ll lll     xx xxx         ccc
        [XCT].Le.Prestige.(The.Prestige).DVDRip.[x264.HP.He-Aac.{Fr-Eng}.St{Fr-Eng}.Chaps].mkv

        The first 3 lines indicates the group index in which a char in the
        filename is located. So for instance, x264 is the group (0, 4, 1), and
        it corresponds to a video codec, denoted by the letter'v' in the 4th line.
        (for more info, see guess.matchtree.to_string)

         Second, it tries to merge all this information into a single object
         containing all the found properties, and does some (basic) conflict
         resolution when they arise.
        """
        valid_filetypes = ('autodetect', 'subtitle', 'video', 'movie', 'moviesubtitle',
                           'episode', 'episodesubtitle')
        if filetype not in valid_filetypes:
            raise ValueError(b'filetype needs to be one of %s' % valid_filetypes)
        if not PY3 and not isinstance(filename, unicode):
            log.warning(b'Given filename to matcher is not unicode...')
        self.match_tree = MatchTree(filename)
        mtree = self.match_tree
        mtree.guess.set(b'type', filetype, confidence=1.0)

        def apply_transfo(transfo_name, *args, **kwargs):
            transfo = __import__(b'guessit.transfo.' + transfo_name, globals=globals(), locals=locals(), fromlist=[
             b'process'], level=0)
            transfo.process(mtree, *args, **kwargs)

        apply_transfo(b'split_path_components')
        apply_transfo(b'guess_filetype', filetype)
        if mtree.guess[b'type'] == b'unknown':
            return
        apply_transfo(b'split_explicit_groups')
        if mtree.guess[b'type'] in ('episode', 'episodesubtitle'):
            strategy = [
             b'guess_date', b'guess_website', b'guess_release_group',
             b'guess_properties', b'guess_language',
             b'guess_video_rexps',
             b'guess_episodes_rexps', b'guess_weak_episodes_rexps']
        else:
            strategy = [
             b'guess_date', b'guess_website', b'guess_release_group',
             b'guess_properties', b'guess_language',
             b'guess_video_rexps']
        for name in strategy:
            apply_transfo(name)

        for name in [b'guess_bonus_features', b'guess_year', b'guess_country']:
            apply_transfo(name)

        apply_transfo(b'split_on_dash')
        if mtree.guess[b'type'] in ('episode', 'episodesubtitle'):
            apply_transfo(b'guess_episode_info_from_position')
        else:
            apply_transfo(b'guess_movie_title_from_position')
        apply_transfo(b'post_process')
        log.debug(b'Found match tree:\n%s' % u(mtree))

    def matched(self):
        return self.match_tree.matched()