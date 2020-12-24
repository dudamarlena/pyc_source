# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/freeform/match.py
# Compiled at: 2006-03-28 20:59:12
from itertools import repeat
from heapq import *
from levenshtein import *
from pprint import pprint
__all__ = ['formtable_prepare', 'match_scentence', 'match_command', 'FIELDTYPE_INVALID', 'FIELDTYPE_UNKNOWN', 'FIELDTYPE_KEYWORD', 'FIELDTYPE_WORD', 'FIELDTYPE_WORDS', 'FIELDTYPE_MENU', 'FIELDTYPE_LIST', 'FIELDTYPE_LISTMENU', 'FIELDTYPE_FIRST', 'FIELDTYPE_LAST', 'fieldtype_flavour', 'FIELDTYPE_FLAVOUR_FLAG_SINGULAR', 'FIELDTYPE_FLAVOUR_FLAG_PLURAL', 'FIELDTYPE_FLAVOUR_FLAG_VALUE_SELECTSINGLE', 'FIELDTYPE_FLAVOUR_FLAG_VALUE_ENUMERATION', 'FIELDTYPE_FLAVOUR_FLAG_VALUE_LABEL', 'FIELDTYPE_FLAVOUR_FLAG_COUNT', 'repr_fieldtype', 'repr_fieldtype_compact', 'repr_fieldtype_flavour', 'repr_fieldtype_flavour_compact']
FIELDTYPE_INVALID = -1
FIELDTYPE_UNKNOWN = 0
FIELDTYPE_KEYWORD = 1
FIELDTYPE_WORD = 2
FIELDTYPE_WORDS = 3
FIELDTYPE_MENU = 4
FIELDTYPE_LIST = 5
FIELDTYPE_LISTMENU = 6
FIELDTYPE_FIRST = FIELDTYPE_UNKNOWN
FIELDTYPE_LAST = FIELDTYPE_LISTMENU
_fieldtype_reprtab = dict([(FIELDTYPE_INVALID, 'INVALID'), (FIELDTYPE_UNKNOWN, 'UNKNOWN'), (FIELDTYPE_KEYWORD, 'KEYWORD'), (FIELDTYPE_WORD, 'WORD'), (FIELDTYPE_WORDS, 'WORDS'), (FIELDTYPE_MENU, 'MENU'), (FIELDTYPE_LIST, 'LIST'), (FIELDTYPE_LISTMENU, 'LISTMENU')])
_fieldtype_reprtab_compact = dict([(FIELDTYPE_INVALID, 'IN'), (FIELDTYPE_UNKNOWN, 'UN'), (FIELDTYPE_KEYWORD, 'KE'), (FIELDTYPE_WORD, 'WO'), (FIELDTYPE_WORDS, 'WW'), (FIELDTYPE_MENU, 'ME'), (FIELDTYPE_LIST, 'LI'), (FIELDTYPE_LISTMENU, 'LM')])

def repr_fieldtype(typecode):
    return 'FIELDTYPE_%s' % _fieldtype_reprtab.get(typecode, 'INVALID')


def repr_fieldtype_compact(typecode):
    return _fieldtype_reprtab_compact.get(typecode, 'IN')


FIELDTYPE_FLAVOUR_FLAG_SINGULAR = 1 << 0
FIELDTYPE_FLAVOUR_FLAG_PLURAL = 1 << 1
FIELDTYPE_FLAVOUR_FLAG_VALUE_SELECTSINGLE = 1 << 2
FIELDTYPE_FLAVOUR_FLAG_VALUE_ENUMERATION = 1 << 3
FIELDTYPE_FLAVOUR_FLAG_VALUE_LABEL = 1 << 4
FIELDTYPE_FLAVOUR_FLAG_COUNT = 5
_fieldtype_flavour_reprtab = dict([(FIELDTYPE_FLAVOUR_FLAG_SINGULAR, 'SINGULAR'), (FIELDTYPE_FLAVOUR_FLAG_PLURAL, 'PLURAL'), (FIELDTYPE_FLAVOUR_FLAG_VALUE_SELECTSINGLE, 'SELECTSINGLE'), (FIELDTYPE_FLAVOUR_FLAG_VALUE_ENUMERATION, 'VALUE_ENUMERATION'), (FIELDTYPE_FLAVOUR_FLAG_VALUE_LABEL, 'VALUE_LABEL')])
_fieldtype_flavour_reprtab_compact = dict([(FIELDTYPE_FLAVOUR_FLAG_SINGULAR, 'SIN'), (FIELDTYPE_FLAVOUR_FLAG_PLURAL, 'PLU'), (FIELDTYPE_FLAVOUR_FLAG_VALUE_SELECTSINGLE, 'VSELS'), (FIELDTYPE_FLAVOUR_FLAG_VALUE_ENUMERATION, 'VENU'), (FIELDTYPE_FLAVOUR_FLAG_VALUE_LABEL, 'VLAB')])

def repr_fieldtype_flavour(flags):
    return ('|').join([ 'FIELDTYPE_FLAVOUR_FLAG_%s' % _fieldtype_flavour_reprtab[(1 << i)] for i in range(0, FIELDTYPE_FLAVOUR_FLAG_COUNT) if 1 << i & flags ])


def repr_fieldtype_flavour_compact(flags):
    if flags is None:
        return 'None'
    compact = ('|').join([ _fieldtype_flavour_reprtab_compact[(1 << i)] for i in range(0, FIELDTYPE_FLAVOUR_FLAG_COUNT) if 1 << i & flags ])
    return compact


fieldtype_flavour = dict([(FIELDTYPE_INVALID, -1), (FIELDTYPE_UNKNOWN, 0), (FIELDTYPE_KEYWORD, FIELDTYPE_FLAVOUR_FLAG_SINGULAR), (FIELDTYPE_WORD, FIELDTYPE_FLAVOUR_FLAG_SINGULAR), (FIELDTYPE_WORDS, FIELDTYPE_FLAVOUR_FLAG_PLURAL), (FIELDTYPE_MENU, FIELDTYPE_FLAVOUR_FLAG_SINGULAR | FIELDTYPE_FLAVOUR_FLAG_VALUE_SELECTSINGLE | FIELDTYPE_FLAVOUR_FLAG_VALUE_LABEL), (FIELDTYPE_LIST, FIELDTYPE_FLAVOUR_FLAG_SINGULAR | FIELDTYPE_FLAVOUR_FLAG_VALUE_SELECTSINGLE | FIELDTYPE_FLAVOUR_FLAG_VALUE_ENUMERATION), (FIELDTYPE_LISTMENU, FIELDTYPE_FLAVOUR_FLAG_SINGULAR | FIELDTYPE_FLAVOUR_FLAG_VALUE_SELECTSINGLE | FIELDTYPE_FLAVOUR_FLAG_VALUE_ENUMERATION | FIELDTYPE_FLAVOUR_FLAG_VALUE_LABEL)])

def match_scentence(formtable, words):
    """match a scentence, uses backtracking to handle plurals."""
    wordcount = len(words)
    maxfieldcount = formtable['maxfieldcount']
    formcount = formtable['formcount']
    fieldcount = min(maxfieldcount, wordcount)
    formfieldtypes = formtable['form2fieldtypes']
    fieldformidmatchsequence = formtable['fieldformidmatchsequence']
    fieldmatchformids = formtable['fieldmatchformids']
    fieldexactmatchformids = formtable['fieldexactmatchformids']
    ipluralstart = -1
    iword = 0
    match = []
    ifield = 0
    candidateforms = [ formid for formid in range(0, formcount) ]
    nextfieldforms = None
    backtrack = []
    while ifield != fieldcount and iword < len(words):
        matched = None
        word = words[iword]
        nextfieldforms = fieldexactmatchformids[ifield].get(word, None)
        if not nextfieldforms:
            asequence = []
            [ asequence.extend(fieldformidmatchsequence[ifield][formid]) for formid in candidateforms ]
            if asequence:
                asequence[:] = dict.fromkeys(asequence).keys()
                (ic, d) = levenshtein_selectone(asequence, word)
                if ic > -1:
                    word = asequence[ic]
                    nextfieldforms = fieldmatchformids[ifield][word]
        if nextfieldforms:
            match.append(word)
            if ipluralstart > -1:
                if backtrack:
                    backtrack[(-1)][1] = iword + 1
                    backtrack[(-1)][3] = candidateforms
                ipluralstart = -1
            candidateforms = [ formid for formid in candidateforms if formid in nextfieldforms ]
            ifield += 1
        else:
            if ipluralstart == -1:
                for formid in candidateforms:
                    if formfieldtypes[formid][ifield] == FIELDTYPE_WORDS:
                        match.append([])
                        ipluralstart = iword
                        ifield += 1
                        backtrack.append([ifield, iword, ipluralstart, candidateforms])
                        break

            if ipluralstart > -1:
                match[(-1)].append(word)
            else:
                candidateforms = [ formid for formid in candidateforms if formfieldtypes[formid][ifield] == FIELDTYPE_WORD ]
                if candidateforms:
                    match.append(word)
                ifield += 1
        iword += 1
        if not candidateforms:
            if backtrack:
                (ifield, iword, ipluralstart, candidateforms) = backtrack.pop()
                match = match[:ifield]
                match[(-1)].append(ipluralstart == iword and words[iword] or words[(iword - 1)])
            else:
                break

    return (
     match, candidateforms)


def match_command(formtable, scentence):
    (match, forms) = match_scentence(formtable, scentence)
    if not match or not forms:
        return (
         None, forms)
    if len(forms) > 1:
        return (
         match, forms)
    form = forms[0]
    cmd = formtable['form2command'][form]
    valuemap = {}
    for (type, name, value) in zip(formtable['form2fieldtypes'][form], formtable['form2fieldnames'][form], match):
        if type != FIELDTYPE_KEYWORD:
            valuemap.setdefault(name, []).append(value)

    return (
     (
      cmd, form), valuemap)


def _debug_current_production(matched, candidatenextformids, formfieldtypes, ifield, ifieldnext, iword, ipluralstart, ilastfield):
    """This function carries a heavy buyer beware badge. Tweak it if you need to,
    and call from match_scentence to get an idea of how the algorithm works."""
    pprint([matched, 'if=%s, ifn=%s, iw=%s, iwss=%s' % (ifield, ifieldnext, iword, ipluralstart), candidatenextformids, (' ').join(map(repr_fieldtype_compact, [ formfieldtypes[formid][ifield] for formid in candidatenextformids ])), (' ').join(map(repr_fieldtype_compact, ifield < ilastfield and [ formfieldtypes[formid][ifieldnext] for formid in candidatenextformids ] or []))])


def formtable_prepare(formtable):
    """Prepare a formtable for use in match_ xxx above.
    
    Don't call repeatedly on the same table!

    This seperation is preparing the way for dynamic asequence construction,
    ie support for convenient dynamicaly  fild list and listmenu fields.
    """
    formcount = formtable['formcount']
    maxfieldcount = formtable['maxfieldcount']
    fieldformtypes = formtable['field2fieldtypes']
    fieldselectsequences = formtable['field2selectvalues']
    fieldformidmatchsequence = []
    fieldmatchformids = []
    fieldexactmatchformids = []
    for ifield in range(0, maxfieldcount):
        fieldformidmatchsequence.append([])
        fieldmatchformids.append({})
        fieldexactmatchformids.append({})
        for formid in range(0, formcount):
            fieldformidmatchsequence[ifield].append([])
            if fieldformtypes[ifield][formid] in [FIELDTYPE_KEYWORD, FIELDTYPE_LIST]:
                asequence = fieldselectsequences[ifield][formid]
                fieldformidmatchsequence[ifield][formid] = asequence
                for match in asequence:
                    fieldmatchformids[ifield].setdefault(match, []).append(formid)

            elif fieldformtypes[ifield][formid] is FIELDTYPE_LISTMENU:
                asequence = fieldselectsequences[ifield][formid][0]
                fieldformidmatchsequence[ifield][formid] = asequence
                for match in asequence:
                    fieldmatchformids[ifield].setdefault(match, []).append(formid)

                exactsequence = fieldselectsequences[ifield][formid][1]
                for match in exactsequence:
                    fieldexactmatchformids[ifield].setdefault(match, []).append(formid)

            elif fieldformtypes[ifield][formid] is FIELDTYPE_MENU:
                exactsequence = fieldselectsequences[ifield][formid]
                for match in exactsequence:
                    fieldexactmatchformids[ifield].setdefault(match, []).append(formid)

    formtable['fieldformidmatchsequence'] = fieldformidmatchsequence
    formtable['fieldmatchformids'] = fieldmatchformids
    formtable['fieldexactmatchformids'] = fieldexactmatchformids
    return formtable