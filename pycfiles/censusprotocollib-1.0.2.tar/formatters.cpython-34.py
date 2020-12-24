# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/neil/Scripts/random_name/build/lib/censusname/formatters.py
# Compiled at: 2015-02-15 13:32:53
# Size of source mod 2**32: 892 bytes
import re
surname_patterns = [
 {'pattern': '^O(BR[IEYA]{2}N|BRYANT|GORMAN|FLANAGAN|HALLORAN|HARA|LOUGHLIN|SHAUGHNESSY|CONNOR|N[EAI]+LL?|CALLAG?HAN|SHEA|ROURKE|TOOLE?|GRADY|BANNON|BARR|SULLIVAN|DONOHUE|.ONN?ELL?Y?|KEEFE|DOHERTY|[KM][AE]LLE?Y|DONLEY|BAUGH|R[EI]{2}LLEY|BOYLE|.ARR.LL|DELL|HARROLL|DOUGHERTY|[CD]ON[AE]Ll?)(S?)$', 
  'replace': lambda pattern: "O'" + pattern.group(1).capitalize() + pattern.group(2).lower()},
 {'pattern': '^ST([^AEIOURY]\\w+$)', 
  'replace': lambda pattern: 'St. ' + pattern.group(1).capitalize()},
 {'pattern': '^MC(\\w+)$', 
  'replace': lambda pattern: 'Mc' + pattern.group(1).capitalize()}]

def recapitalize_surnames(fragment):
    for reformat in surname_patterns:
        fragment = re.sub(reformat['pattern'], reformat['replace'], fragment, flags=re.IGNORECASE)

    return fragment