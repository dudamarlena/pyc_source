# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.cygwin-2.2.1-i686/egg/tvrenamer/core/patterns.py
# Compiled at: 2015-11-08 18:31:47
"""Regular expression patterns for filename formats.

Supported filename formats::

    * Sample.Show.S01E01.S01E02.S01E03.S01E04.eps.mp4
    * Sample-Show.S02e22e23e24.avi
    * Sample.Show.3x12.3x13.3x14.avi
    * Sample.Show.4x4x5x6.mp4
    * Sample.Show.S02E11-15-stuff.mkv
    * Sample-Show.2x11-15.avi
    * Sample-Show.[3x11-13].mp4
    * Sample.Show-[013].avi
    * Sample.S0202.mp4
    * Sample_Show-7x17.avi
    * Sample-Show S09.E11.mkv
    * Sample-Show S09_E11.mkv
    * Sample-Show S09 - E11.mkv
    * Sample_Show-[09.01].avi
    * Sample.Show - S9 E 9.avi
    * SampleShow - episode 1219 [S 13 - E 07].mkv
    * SampleShow - episode 1219 [S 13 Ep 07].avi
    * Sample Show 2 of 7.mp4
    * Sample.Show.Part.1.and.Part.2.avi
    * Sample.Show.pt.1 & pt 2 & pt.3.avi
    * Sample Show part 5.mkv
    * Sample.Show season 10 episode 15.mp4
    * Sample Show 909.mkv
    * Sample Show 1011.avi
    * Sample Show e19.mp4

"""
import re
FILENAME_PATTERNS = [
 '\n    ^((?P<seriesname>.+?)[ \\._\\-])?          # show name\n    [Ss](?P<seasonnumber>[0-9]+)             # s01\n    [\\.\\- ]?                                 # separator\n    [Ee](?P<episodenumberstart>[0-9]+)       # first e23\n    ([\\.\\- ]+                                # separator\n    [Ss](?P=seasonnumber)                    # s01\n    [\\.\\- ]?                                 # separator\n    [Ee][0-9]+)*                             # e24 etc (middle groups)\n    ([\\.\\- ]+                                # separator\n    [Ss](?P=seasonnumber)                    # last s01\n    [\\.\\- ]?                                 # separator\n    [Ee](?P<episodenumberend>[0-9]+))        # final episode number\n    [^\\/]*$\n    ',
 '\n    ^((?P<seriesname>.+?)[ \\._\\-])?          # show name\n    [Ss](?P<seasonnumber>[0-9]+)             # s01\n    [\\.\\- ]?                                 # separator\n    [Ee](?P<episodenumberstart>[0-9]+)       # first e23\n    ([\\.\\- ]?                                # separator\n    [Ee][0-9]+)*                             # e24e25 etc\n    [\\.\\- ]?[Ee](?P<episodenumberend>[0-9]+) # final episode num\n    [^\\/]*$\n    ',
 '\n    ^((?P<seriesname>.+?)[ \\._\\-])?          # show name\n    (?P<seasonnumber>[0-9]+)                 # first season number (1)\n    [xX](?P<episodenumberstart>[0-9]+)       # first episode (x23)\n    ([ \\._\\-]+                               # separator\n    (?P=seasonnumber)                        # more season numbers (1)\n    [xX][0-9]+)*                             # more episode numbers (x24)\n    ([ \\._\\-]+                               # separator\n    (?P=seasonnumber)                        # last season number (1)\n    [xX](?P<episodenumberend>[0-9]+))        # last episode number (x25)\n    [^\\/]*$\n    ',
 '\n    ^((?P<seriesname>.+?)[ \\._\\-])?          # show name\n    (?P<seasonnumber>[0-9]+)                 # 1\n    [xX](?P<episodenumberstart>[0-9]+)       # first x23\n    ([xX][0-9]+)*                            # x24x25 etc\n    [xX](?P<episodenumberend>[0-9]+)         # final episode num\n    [^\\/]*$\n    ',
 '\n    ^((?P<seriesname>.+?)[ \\._\\-])?          # show name\n    [Ss](?P<seasonnumber>[0-9]+)             # s01\n    [\\.\\- ]?                                 # separator\n    [Ee](?P<episodenumberstart>[0-9]+)       # first e23\n    (                                        # -24 etc\n         [\\-]\n         [Ee]?[0-9]+\n    )*\n         [\\-]                                # separator\n         [Ee]?(?P<episodenumberend>[0-9]+)   # final episode num\n    [\\.\\- ]                                  # must have a separator (prevents s01e01-720p from being 720 episodes) # noqa\n    [^\\/]*$\n    ',
 '\n    ^((?P<seriesname>.+?)[ \\._\\-])?          # show name\n    (?P<seasonnumber>[0-9]+)                 # 1\n    [xX](?P<episodenumberstart>[0-9]+)       # first x23\n    (                                        # -24 etc\n         [\\-+][0-9]+\n    )*\n         [\\-+]                               # separator\n         (?P<episodenumberend>[0-9]+)        # final episode num\n    ([\\.\\-+ ].*                              # must have a separator (prevents 1x01-720p from being 720 episodes) # noqa\n    |\n    $)\n    ',
 '\n    ^(?P<seriesname>.+?)[ \\._\\-]          # show name and padding\n    \\[                                       # [\n        ?(?P<seasonnumber>[0-9]+)            # season\n    [xX]                                     # x\n        (?P<episodenumberstart>[0-9]+)       # episode\n        ([\\-+] [0-9]+)*\n    [\\-+]                                    # -\n        (?P<episodenumberend>[0-9]+)         # episode\n    \\]                                       # \\]\n    [^\\\\/]*$\n    ',
 '\n    ^((?P<seriesname>.+?)[ \\._\\-])?       # show name and padding\n    \\[                                       # [ not optional (or too ambigious) # noqa\n    (?P<episodenumber>[0-9]+)                # episode\n    \\]                                       # ]\n    [^\\\\/]*$\n    ',
 '\n    ^(?P<seriesname>.+?)[ \\._\\-]\n    [Ss](?P<seasonnumber>[0-9]{2})\n    [\\.\\- ]?\n    (?P<episodenumber>[0-9]{2})\n    [^0-9]*$\n    ',
 '\n    ^((?P<seriesname>.+?)[ \\._\\-])?       # show name and padding\n    \\[?                                      # [ optional\n    (?P<seasonnumber>[0-9]+)                 # season\n    [xX]                                     # x\n    (?P<episodenumber>[0-9]+)                # episode\n    \\]?                                      # ] optional\n    [^\\\\/]*$\n    ',
 '\n    ^((?P<seriesname>.+?)[ \\._\\-])?\n    \\[?\n    [Ss](?P<seasonnumber>[0-9]+)[ ]?[\\._\\- ]?[ ]?\n    [Ee]?(?P<episodenumber>[0-9]+)\n    \\]?\n    [^\\\\/]*$\n    ',
 '\n    ^((?P<seriesname>.+?))                # show name\n    [ \\._\\-]?                                # padding\n    \\[                                       # [\n    (?P<seasonnumber>[0-9]+?)                # season\n    [.]                                      # .\n    (?P<episodenumber>[0-9]+?)               # episode\n    \\]                                       # ]\n    [ \\._\\-]?                                # padding\n    [^\\\\/]*$\n    ',
 '\n    ^(?P<seriesname>.+?)[ ]?[ \\._\\-][ ]?\n    [Ss](?P<seasonnumber>[0-9]+)[\\.\\- ]?\n    [Ee]?[ ]?(?P<episodenumber>[0-9]+)\n    [^\\\\/]*$\n    ',
 '\n    (?P<seriesname>.+)                       # Showname\n    [ ]-[ ]                                  # -\n    [Ee]pisode[ ]\\d+                         # Episode 1234 (ignored)\n    [ ]\n    \\[                                       # [\n    [sS][ ]?(?P<seasonnumber>\\d+)            # s 12\n    ([ ]|[ ]-[ ]|-)                          # space, or -\n    ([eE]|[eE]p)[ ]?(?P<episodenumber>\\d+)   # e or ep 12\n    \\]                                       # ]\n    .*$                                      # rest of file\n    ',
 '\n    ^(?P<seriesname>.+?)                  # Show name\n    [ \\._\\-]                                 # Padding\n    (?P<episodenumber>[0-9]+)                # 2\n    [ \\._\\-]?                                # Padding\n    of                                       # of\n    [ \\._\\-]?                                # Padding\n    \\d+                                      # 6\n    ([\\._ -]|$|[^\\\\/]*$)                     # More padding, then anything\n    ',
 '\n    ^(?i)\n    (?P<seriesname>.+?)                        # Show name\n    [ \\._\\-]                                   # Padding\n    (?:part|pt)?[\\._ -]\n    (?P<episodenumberstart>[0-9]+)             # Part 1\n    (?:\n      [ \\._-](?:and|&|to)                        # and\n      [ \\._-](?:part|pt)?                        # Part 2\n      [ \\._-](?:[0-9]+))*                        # (middle group, optional, repeating) # noqa\n    [ \\._-](?:and|&|to)                        # and\n    [ \\._-]?(?:part|pt)?                       # Part 3\n    [ \\._-](?P<episodenumberend>[0-9]+)        # last episode number, save it\n    [\\._ -][^\\\\/]*$                            # More padding, then anything\n    ',
 '\n    ^(?P<seriesname>.+?)                  # Show name\\n\n    [ \\\\._\\\\-]                               # Padding\\n\n    [Pp]art[ ](?P<episodenumber>[0-9]+)      # Part 1\\n\n    [\\\\._ -][^\\\\/]*$                         # More padding, then anything\\n\n    ',
 '\n    ^(?P<seriesname>.+?)[ ]?               # Show name\n    [Ss]eason[ ]?(?P<seasonnumber>[0-9]+)[ ]? # Season 1\n    [Ee]pisode[ ]?(?P<episodenumber>[0-9]+)   # Episode 20\n    [^\\\\/]*$                                # Anything\n    ',
 '\n    ^(?P<seriesname>.+)[ \\._\\-]\n    (?P<seasonnumber>[0-9]{1})\n    (?P<episodenumber>[0-9]{2})\n    [\\._ -][^\\\\/]*$\n    ',
 '\n    ^(?P<seriesname>.+)[ \\._\\-]\n    (?P<seasonnumber>[0-9]{2})\n    (?P<episodenumber>[0-9]{2,3})\n    [\\._ -][^\\\\/]*$\n    ',
 '\n    ^(?P<seriesname>.+?)                  # Show name\n    [ \\._\\-]                                 # Padding\n    [Ee](?P<episodenumber>[0-9]+)            # E123\n    [\\._ -][^\\\\/]*$                          # More padding, then anything\n    ']
_EXPRESSIONS = []

def get_expressions():
    """Retrieve compiled pattern expressions.

    :returns: compiled regular expressions for supported filename formats
    :rtype: list
    """
    if len(_EXPRESSIONS) == len(FILENAME_PATTERNS):
        return _EXPRESSIONS
    for cpattern in FILENAME_PATTERNS:
        _EXPRESSIONS.append(re.compile(cpattern, re.VERBOSE))

    return _EXPRESSIONS


get_expressions()