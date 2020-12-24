# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.7/site-packages/guessit/transfo/guess_release_group.py
# Compiled at: 2013-03-18 16:30:48
from __future__ import unicode_literals
from guessit.transfo import SingleNodeGuesser
from guessit.patterns import prop_multi, compute_canonical_form, _dash, _psep
import re, logging
log = logging.getLogger(__name__)

def get_patterns(property_name):
    return [ p.replace(_dash, _psep) for patterns in prop_multi[property_name].values() for p in patterns ]


CODECS = get_patterns(b'videoCodec')
FORMATS = get_patterns(b'format')

def adjust_metadata(md):
    return dict((property_name, compute_canonical_form(property_name, value) or value) for property_name, value in md.items())


def guess_release_group(string):
    group_names = [ b'(?P<videoCodec>' + codec + b')-?(?P<releaseGroup>.*?)[ \\.]' for codec in CODECS
                  ]
    group_names += [ b'(?P<format>' + fmt + b')-?(?P<releaseGroup>.*?)[ \\.]' for fmt in FORMATS
                   ]
    for rexp in group_names:
        match = re.search(rexp, string, re.IGNORECASE)
        if match:
            metadata = match.groupdict()
            release_group = compute_canonical_form(b'releaseGroup', metadata[b'releaseGroup'])
            if release_group:
                return (adjust_metadata(metadata), (match.start(1), match.end(2)))

    group_names = [ b'\\.(?P<videoCodec>' + codec + b')-(?P<releaseGroup>.*?)(-(.*?))?[ \\.]' for codec in CODECS
                  ]
    group_names += [ b'\\.(?P<format>' + fmt + b')-(?P<releaseGroup>.*?)(-(.*?))?[ \\.]' for fmt in FORMATS
                   ]
    for rexp in group_names:
        match = re.search(rexp, string, re.IGNORECASE)
        if match:
            return (adjust_metadata(match.groupdict()), (match.start(1), match.end(2)))

    return (None, None)


def process(mtree):
    SingleNodeGuesser(guess_release_group, 0.8, log).process(mtree)