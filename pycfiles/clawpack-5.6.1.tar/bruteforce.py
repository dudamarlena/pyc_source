# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/adam/code/claw/claw/signature/bruteforce.py
# Compiled at: 2015-08-22 13:07:29
import logging, regex as re
from claw.utils import get_delimiter
from claw.signature.constants import SIGNATURE_MAX_LINES, TOO_LONG_SIGNATURE_LINE
log = logging.getLogger(__name__)
RE_SIGNATURE = re.compile('\n               (\n                   (?:\n                       ^[\\s]*--*[\\s]*[a-z \\.]*$\n                       |\n                       ^thanks[\\s,!]*$\n                       |\n                       ^regards[\\s,!]*$\n                       |\n                       ^cheers[\\s,!]*$\n                       |\n                       ^best[ a-z]*[\\s,!]*$\n                   )\n                   .*\n               )\n               ', re.I | re.X | re.M | re.S)
RE_PHONE_SIGNATURE = re.compile('\n               (\n                   (?:\n                       ^sent[ ]{1}from[ ]{1}my[\\s,!\\w]*$\n                       |\n                       ^sent[ ]from[ ]Mailbox[ ]for[ ]iPhone.*$\n                       |\n                       ^sent[ ]([\\S]*[ ])?from[ ]my[ ]BlackBerry.*$\n                       |\n                       ^Enviado[ ]desde[ ]mi[ ]([\\S]+[ ]){0,2}BlackBerry.*$\n                   )\n                   .*\n               )\n               ', re.I | re.X | re.M | re.S)
RE_SIGNATURE_CANDIDATE = re.compile('\n    (?P<candidate>c+d)[^d]\n    |\n    (?P<candidate>c+d)$\n    |\n    (?P<candidate>c+)\n    |\n    (?P<candidate>d)[^d]\n    |\n    (?P<candidate>d)$\n', re.I | re.X | re.M | re.S)

def extract_signature(msg_body):
    """
    Analyzes message for a presence of signature block (by common patterns)
    and returns tuple with two elements: message text without signature block
    and the signature itself.

    >>> extract_signature('Hey man! How r u?

--
Regards,
Roman')
    ('Hey man! How r u?', '--
Regards,
Roman')

    >>> extract_signature('Hey man!')
    ('Hey man!', None)
    """
    try:
        delimiter = get_delimiter(msg_body)
        stripped_body = msg_body.strip()
        phone_signature = None
        phone_signature = RE_PHONE_SIGNATURE.search(msg_body)
        if phone_signature:
            stripped_body = stripped_body[:phone_signature.start()]
            phone_signature = phone_signature.group()
        lines = stripped_body.splitlines()
        candidate = get_signature_candidate(lines)
        candidate = delimiter.join(candidate)
        signature = RE_SIGNATURE.search(candidate)
        if not signature:
            return (stripped_body.strip(), phone_signature)
        signature = signature.group()
        stripped_body = delimiter.join(lines)
        stripped_body = stripped_body[:-len(signature)]
        if phone_signature:
            signature = delimiter.join([signature, phone_signature])
        return (
         stripped_body.strip(),
         signature.strip())
    except Exception as e:
        log.exception('ERROR extracting signature')
        return (
         msg_body, None)

    return


def get_signature_candidate(lines):
    """Return lines that could hold signature

    The lines should:

    * be among last SIGNATURE_MAX_LINES non-empty lines.
    * not include first line
    * be shorter than TOO_LONG_SIGNATURE_LINE
    * not include more than one line that starts with dashes
    """
    non_empty = [ i for i, line in enumerate(lines) if line.strip() ]
    if len(non_empty) <= 1:
        return []
    candidate = non_empty[1:]
    candidate = candidate[-SIGNATURE_MAX_LINES:]
    markers = _mark_candidate_indexes(lines, candidate)
    candidate = _process_marked_candidate_indexes(candidate, markers)
    if candidate:
        candidate = lines[candidate[0]:]
        return candidate
    return []


def _mark_candidate_indexes(lines, candidate):
    """Mark candidate indexes with markers

    Markers:

    * c - line that could be a signature line
    * l - long line
    * d - line that starts with dashes but has other chars as well

    >>> _mark_candidate_lines(['Some text', '', '-', 'Bob'], [0, 2, 3])
    'cdc'
    """
    markers = bytearray('c' * len(candidate))
    for i, line_idx in reversed(list(enumerate(candidate))):
        if len(lines[line_idx].strip()) > TOO_LONG_SIGNATURE_LINE:
            markers[i] = 'l'
        else:
            line = lines[line_idx].strip()
            if line.startswith('-') and line.strip('-'):
                markers[i] = 'd'

    return markers


def _process_marked_candidate_indexes(candidate, markers):
    """
    Run regexes against candidate's marked indexes to strip
    signature candidate.

    >>> _process_marked_candidate_indexes([9, 12, 14, 15, 17], 'clddc')
    [15, 17]
    """
    match = RE_SIGNATURE_CANDIDATE.match(markers[::-1])
    if match:
        return candidate[-match.end('candidate'):]
    return []