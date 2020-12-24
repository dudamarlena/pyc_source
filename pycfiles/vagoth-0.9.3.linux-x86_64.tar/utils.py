# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/vagoth/utils.py
# Compiled at: 2013-12-28 15:30:28


def matches_tags(tag_matches, tags):
    """Do the given tag_matches match the given tags?

    If the tag_matches value is None, it only checks for tag existence.

    If the tag_matches value is not None, it does a direct comparison.
    For each key/value pair, check if the tag exists, and if the value is
    not None, if the value matches.

    :param tag_matches: key-value pairs we want to check for
    :param tags: key-value pairs that we'll check against
    :returns: bool
    """
    assert tag_matches
    assert type(tags) == dict
    for tag_name, tag_value in tag_matches.items():
        if tag_name not in tags:
            return False
        if tag_value is not None and tag_value != tags[tag_name]:
            return False

    return True