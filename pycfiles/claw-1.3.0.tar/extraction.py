# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/adam/code/talon/talon/signature/extraction.py
# Compiled at: 2015-07-20 12:14:52
import os, logging, regex as re
from PyML import SparseDataSet
from talon.constants import RE_DELIMITER
from talon.signature.constants import SIGNATURE_MAX_LINES, TOO_LONG_SIGNATURE_LINE
from talon.signature.learning.featurespace import features, build_pattern
from talon.utils import get_delimiter
from talon.signature.bruteforce import get_signature_candidate
from talon.signature.learning.helpers import has_signature
log = logging.getLogger(__name__)
EXTRACTOR = None
RE_REVERSE_SIGNATURE = re.compile('\n# signature should consists of blocks like this\n(?:\n   # it could end with empty line\n   e*\n   # there could be text lines but no more than 2 in a row\n   (te*){,2}\n   # every block should end with signature line\n   s\n)+\n', re.I | re.X | re.M | re.S)

def is_signature_line(line, sender, classifier):
    """Checks if the line belongs to signature. Returns True or False."""
    data = SparseDataSet([build_pattern(line, features(sender))])
    return classifier.decisionFunc(data, 0) > 0


def extract(body, sender):
    """Strips signature from the body of the message.

    Returns stripped body and signature as a tuple.
    If no signature is found the corresponding returned value is None.
    """
    try:
        delimiter = get_delimiter(body)
        body = body.strip()
        if has_signature(body, sender):
            lines = body.splitlines()
            markers = _mark_lines(lines, sender)
            text, signature = _process_marked_lines(lines, markers)
            if signature:
                text = delimiter.join(text)
                if text.strip():
                    return (text, delimiter.join(signature))
    except Exception as e:
        log.exception('ERROR when extracting signature with classifiers')

    return (body, None)


def _mark_lines(lines, sender):
    """Mark message lines with markers to distinguish signature lines.

    Markers:

    * e - empty line
    * s - line identified as signature
    * t - other i.e. ordinary text line

    >>> mark_message_lines(['Some text', '', 'Bob'], 'Bob')
    'tes'
    """
    global EXTRACTOR
    candidate = get_signature_candidate(lines)
    markers = bytearray('t' * len(lines))
    for i, line in reversed(list(enumerate(candidate))):
        j = len(lines) - len(candidate) + i
        if not line.strip():
            markers[j] = 'e'
        elif is_signature_line(line, sender, EXTRACTOR):
            markers[j] = 's'

    return markers


def _process_marked_lines(lines, markers):
    """Run regexes against message's marked lines to strip signature.

    >>> _process_marked_lines(['Some text', '', 'Bob'], 'tes')
    (['Some text', ''], ['Bob'])
    """
    signature = RE_REVERSE_SIGNATURE.match(markers[::-1])
    if signature:
        return (lines[:-signature.end()], lines[-signature.end():])
    else:
        return (
         lines, None)