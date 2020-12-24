# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/freegenes/main/helpers.py
# Compiled at: 2019-09-30 14:12:49
# Size of source mod 2**32: 3079 bytes
"""

Copyright (C) 2019 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""
from freegenes.logger import bot
import requests, os, re

def derive_parts(self, sequence, circular=True):
    """based on a sequence, search all freegenes parts for the sequence,
       forward and backwards. This is done by the client (and not on the
       server) as to not tax the server. We cache the parts request to
       not make the same one over and over. If the sequence is circular,
       we add it to itself, otherwise not.

       Algorithm:
       =========
       1. Cache all parts from the API (one call)
       2. Find all forward and reverse substrings that match
       3. Model as interview scheduling problem

       If the user is interested in ALL possible combinations of parts,
       we would want to remove the "best solution" parts (the first part)
       from the list and try again.
    """
    self._cache_parts()
    if circular:
        sequence = sequence + sequence
    coords = []
    for uuid, part in self.cache['parts'].items():
        if part.get('optimized_sequence'):
            forward = part['optimized_sequence']
            reverse = forward[::-1]
            if forward in sequence:
                for match in re.finditer(forward, sequence):
                    coords.append((part.get('uuid'), '>', match.start(), match.end()))

            if reverse in sequence:
                for match in re.finditer(reverse, sequence):
                    coords.append((part.get('uuid'), '<', match.start(), match.end()))

    queue = sorted(coords, key=(lambda tup: tup[3] - tup[2]))

    def overlaps_with(selected_sequences, element):
        """determine if an element overlaps with any current elements in the
           list
        """
        for selected in selected_sequences:
            if element[2] >= selected[2]:
                if element[2] < selected[3]:
                    return True
            if element[3] > selected[2] and element[3] <= selected[3]:
                return True

        return False

    selected_sequences = []
    while queue:
        element = queue.pop()
        overlaps_with(selected_sequences, element) or selected_sequences.append(element)

    selected_sequences = sorted(selected_sequences, key=(lambda tup: tup[2]))
    return selected_sequences