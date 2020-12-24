# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-ppc/egg/oldowan/mitomotifs/str2sites.py
# Compiled at: 2008-08-24 10:54:34
import re
from polymorphism import Polymorphism
from rCRS import rCRSlist
RE_SITE = re.compile('([0-9]+)(.*)')
TRANSITIONS = {'G': 'C', 'C': 'G', 
   'A': 'T', 
   'T': 'A'}

def str2sites(a_string, add16k=False):
    """Extract a list of Polymorphisms from a string.

    """
    if isinstance(a_string, Polymorphism):
        return [
         a_string]
    entries = re.sub('[,;]', ' ', a_string).split()
    if a_string.strip().upper() == 'RCRS' or a_string.strip().upper() == 'CRS' or a_string.strip() == '':
        return []
    matches = list((RE_SITE.match(x) for x in entries))
    invalid_site_indices = list((pos for (pos, val) in enumerate(matches) if val == None))
    if len(invalid_site_indices) > 0:
        invalid_sites = list((entries[x] for x in invalid_site_indices))
        raise Exception('These sites are invalid: %s' % invalid_sites)
    positions = [ RE_SITE.match(x).groups() for x in entries ]
    sites = []
    for (k, v) in positions:
        insert = 0
        k = int(k)
        if add16k:
            k = k + 16000
        if v == '':
            v = TRANSITIONS[rCRSlist[k]]
        elif v == 'd':
            v = '-'
        elif len(v) > 1:
            if v.upper().startswith('DEL'):
                v = '-'
            elif v.startswith('.'):
                match = re.match('\\.([1-9][0-9]*)([ACGTURYMKSWBDHVN]+)', v)
                if match:
                    (insert, v) = match.groups()
                    insert = int(insert)
            elif v.upper().startswith('INS'):
                v = v.upper()
                match = re.match('INS([ACGTURYMKSWBDHVN]+)', v)
                if match:
                    (v,) = match.groups()
                    insert = 1
            elif v.startswith('+'):
                insert = True
                match = re.match('\\+([ACGTURYMKSWBDHVN]+)', v)
                if match:
                    (v,) = match.groups()
                    insert = 1
        if v == '-' or insert == 0:
            sites.append(Polymorphism(k, 0, v))
        elif insert > 0:
            if len(v) > 1:
                for i in range(len(v)):
                    sites.append(Polymorphism(k, i + 1, v[i]))

            else:
                sites.append(Polymorphism(k, insert, v))

    return sites