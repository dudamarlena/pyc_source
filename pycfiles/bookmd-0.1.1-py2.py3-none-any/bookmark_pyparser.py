# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/bookmark_pyparser.py
# Compiled at: 2015-06-28 06:42:09
__doc__ = '\n Copyright 2009 Robert Steed\n \nThis program is free software: you can redistribute it and/or modify\nit under the terms of the GNU Lesser General Public License as published by\nthe Free Software Foundation, either version 3 of the License, or\n(at your option) any later version.\n\nThis program is distributed in the hope that it will be useful,\nbut WITHOUT ANY WARRANTY; without even the implied warranty of\nMERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the\nGNU Lesser General Public License for more details.\n\nYou should have received a copy of the GNU Lesser General Public License\nalong with this program.  If not, see <http://www.gnu.org/licenses/>.\n'
from six import print_
import pyparsing as pp, types
try:
    from collections import OrderedDict
except ImportError:
    try:
        from ordereddict import OrderedDict as dict
    except ImportError:
        raise ImportError('If you are running a version of python less than 2.7, you will need to install the ordereddict module from pypi')

headers = [
 '<!DOCTYPE NETSCAPE-Bookmark-file-1>\n<!-- This is an automatically generated file.\n     It will be read and overwritten.\n     DO NOT EDIT! -->\n<META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=UTF-8">\n<TITLE>Bookmarks</TITLE>',
 '<!DOCTYPE NETSCAPE-Bookmark-file-1>\n<!-- This is an automatically generated file.\nIt will be read and overwritten.\nDo Not Edit! -->\n<META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=UTF-8">\n<TITLE>Bookmarks</TITLE>',
 '<!DOCTYPE NETSCAPE-Bookmark-file-1>\n<!-- This is an automatically generated file.\nIt will be read and overwritten.\nDo Not Edit! -->\n<TITLE>Bookmarks</TITLE>',
 '<!DOCTYPE NETSCAPE-Bookmark-file-1>\n<html><head><!-- This is an automatically generated file.\n     It will be read and overwritten.\n     DO NOT EDIT! --><meta http-equiv="Content-Type" content="text/html; charset=UTF-8"><title>Bookmarks</title></head>\n']
headers2 = [ pp.Combine(pp.And(pp.Literal(line.strip()) + pp.ZeroOrMore(pp.White()) for line in head.splitlines()), adjacent=False) for head in headers ]
startH1 = pp.Literal('<H1')
endH1 = pp.Literal('/H1>')
H1 = pp.Combine(startH1 + pp.SkipTo(endH1) + endH1)
startBM = pp.Literal('<DT><A HREF=') | pp.Literal('<DT><A FEEDURL=')
endBM = pp.Literal('</A>') + pp.Optional(pp.ZeroOrMore(pp.White()) + pp.Literal('<DD>') + pp.SkipTo(pp.ZeroOrMore(pp.White()) + '<'))
bookmarks = pp.Combine(startBM + '"' + pp.SkipTo('"').setResultsName('HyperLink', listAllMatches=True) + '"' + pp.SkipTo(endBM, include=True))
separator = pp.Literal('<HR>')
foldernamestart = pp.Literal('<DT><H3')
foldernameend = pp.Literal('</H3>') ^ pp.Literal('</H3>') + pp.ZeroOrMore(pp.White()) + pp.Literal('<DD>') + pp.SkipTo(pp.LineEnd())
foldername = pp.Combine(foldernamestart + pp.SkipTo('>') + '>' + pp.SkipTo('</H3>').setResultsName('Folder') + foldernameend)
startlist = pp.Suppress('<DL><p>')
endlist = pp.Suppress('</DL><p>')
folderBM = pp.Forward()
foldercontents = folderBM | separator | bookmarks
folderstruct = pp.Group(foldername + startlist + pp.ZeroOrMore(foldercontents) + endlist)
folderBM << folderstruct
bookmarkshtml = pp.Or(headers2) + H1 + pp.Optional(startlist) + pp.ZeroOrMore(foldercontents) + pp.Suppress('</DL>') + pp.Optional(pp.Suppress('<p>'))

def hyperlinks(parseresults):
    """returns all hyperlinks from parsed file"""
    try:
        itemlist = parseresults.HyperLink.asList()
    except:
        itemlist = []

    for item in parseresults:
        if type(item) == str:
            pass
        elif 'Folder' in item:
            foldercontents = hyperlinks(item)
            itemlist.extend(foldercontents)

    return itemlist


def clean_tree(parseresults):
    """returns a set of nested lists/tuples from parsed file. Maintains the original folder structure but only containing foldernames and hyperlinks"""
    try:
        itemlist = parseresults.HyperLink.asList()
    except:
        itemlist = []

    for item in parseresults:
        if type(item) == str:
            pass
        elif 'Folder' in item:
            foldercontents = clean_tree(item)
            itemlist.append((item.Folder, foldercontents))

    return itemlist


def bookmarkDict(parseresults):
    """returns a set of nested dictionaries from parsed file. Keys are hyperlinks, values are original strings. Original Folder headers strings are contained under key 'Folder'"""
    new = OrderedDict()
    hyperlinks = dict([ (pos, href) for href, pos in parseresults._ParseResults__tokdict.get('HyperLink', []) ])
    for pos, item in enumerate(parseresults):
        if type(item) == str:
            href = hyperlinks.get(pos, None)
            if href:
                if href in new:
                    new[href] = merge_entries(new[href], parseresults[pos])
                else:
                    new[href] = parseresults[pos]
        elif 'Folder' in item:
            foldercontents = bookmarkDict(item)
            foldercontents['Folder'] = item[0]
            if item['Folder'] in new:
                print_('|' * 30 + ' merging 2 bookmarkDict folders named:', item.Folder)
                new[item['Folder']] = merge_bookmarkDict(new[item['Folder']], foldercontents)
            else:
                new[item['Folder']] = foldercontents

    return new


def depersonalisefolders(parseresults):
    """removes personal_toolbar_folder tag. Acts on ParseResults instance in place (ie. a procedure)."""
    folders = top_folders_dict(parseresults)
    tag = pp.Literal('PERSONAL_TOOLBAR_FOLDER="true" ')
    parser = pp.Combine(pp.Optional(pp.SkipTo(tag) + tag.suppress()) + pp.SkipTo(pp.stringEnd))
    for i in folders.values():
        i = i[0]
        parseresults[i][0] = parser.parseString(parseresults[i][0])[0]


def _folder_serialize(parseresults, indent):
    tab = '    '
    indstr = tab * indent
    sresult = indstr + parseresults[0] + '\n'
    sresult += indstr + '<DL><p>' + '\n'
    for item in parseresults[1:]:
        if type(item) == str:
            sresult += indstr + tab + item + '\n'
        elif 'Folder' in item:
            sresult += _folder_serialize(item, indent + 1)

    sresult += indstr + '</DL><p>' + '\n'
    return sresult


def serialize(parseresults):
    """Turns parsed bookmark file back into original string """
    result = ''
    result += ('\n').join((parseresults[0], parseresults[1])) + '\n'
    result += '\n'
    result += '<DL><p>\n'
    for item in parseresults[2:]:
        if type(item) == str:
            result += '    ' + item + '\n'
        else:
            result += _folder_serialize(item, indent=1)

    result += '</DL><p>\n'
    return result


def _folder_serialize_bookmarkDict(bookdict, indent):
    tab = '    '
    indstr = tab * indent
    sresult = indstr + bookdict['Folder'] + '\n'
    sresult += indstr + '<DL><p>' + '\n'
    for key in bookdict:
        if key != 'Folder':
            item = bookdict[key]
            if type(item) == str:
                sresult += indstr + tab + item + '\n'
            elif type(item) == OrderedDict:
                sresult += _folder_serialize_bookmarkDict(item, indent + 1)

    sresult += indstr + '</DL><p>' + '\n'
    return sresult


def serialize_bookmarkDict(bookdict):
    """Turns parsed bookmark file back into original string """
    result = ''
    result += headers[0] + '\n'
    result += '<H1>Bookmarks Menu</H1>' + '\n'
    result += '\n'
    result += '<DL><p>\n'
    for item in bookdict.values():
        if type(item) == str:
            result += '    ' + item + '\n'
        else:
            result += _folder_serialize_bookmarkDict(item, indent=1)

    result += '</DL><p>\n'
    return result


def duplicates(seq):
    uniques = set(seq)
    return [ x for x in seq if x not in uniques or uniques.remove(x) ]


def top_folders_dict(parseresults):
    itemlist = OrderedDict()
    for j, item in enumerate(parseresults):
        if type(item) == str:
            pass
        elif 'Folder' in item:
            try:
                itemlist[item.Folder] += [j]
            except:
                itemlist[item.Folder] = [
                 j]

    return itemlist


def duplicates_dict(seq):
    return [ x for x in seq if len(seq[x]) > 1 ]


def hyperlinks_bookmarkDict(bookdict):
    """returns all hyperlinks from bookmarkDict"""
    itemlist = []
    for item in bookdict:
        if type(bookdict[item]) == OrderedDict:
            foldercontents = hyperlinks_bookmarkDict(bookdict[item])
            itemlist.extend(foldercontents)
        elif item != 'Folder' and type(bookdict[item]) == str:
            itemlist.append(item)
        elif item != 'Folder':
            print_('found an unknown item!: ', item)

    return itemlist


import copy

def merge_bookmarkDict(bookdict1, bookdict2):
    new = copy.deepcopy(bookdict1)
    if new == bookdict2:
        return new
    for key, item in bookdict2.items():
        if key in new:
            if item == new[key]:
                print_()
                print_('##########' + ' found duplicate of ', key)
            elif type(item) == str:
                update = merge_entries(new[key], item)
                new[key] = update
            elif type(item) == OrderedDict:
                print_('|' * 30 + ' merging 2 bookmarkDicts folders named:', key)
                new[key] = merge_bookmarkDict(new[key], item)
            else:
                print_('unexpected item:', item)
        else:
            new[key] = item

    return new


def merge_entries(line1, line2):
    """merges two bookmark entries that should have the same content but different tags"""
    print_('merging 2 tokens strings')
    if line1 == line2:
        print_('Tokens are identical!')
        new = copy.copy(line1)
    else:
        qt = pp.Suppress('"')
        feedurl = 'FEEDURL=' + qt + pp.SkipTo('"')('feedurl') + qt
        href = 'HREF=' + qt + pp.SkipTo('"')('href') + qt
        date = qt + pp.Word(pp.nums).setParseAction(lambda s, l, t: int(t[0])) + qt
        ad = 'ADD_DATE=' + date('ad')
        lv = 'LAST_VISIT=' + date('lv')
        lm = 'LAST_MODIFIED=' + date('lm')
        ID = 'ID=' + qt + pp.SkipTo(qt)('id')
        possible = feedurl | href | ad | lv | lm
        parser = pp.SkipTo(possible | 'ID' | pp.StringEnd()).suppress() + pp.ZeroOrMore(possible) + pp.Optional(pp.SkipTo('ID') + ID)
        l1 = parser.parseString(line1)
        l2 = parser.parseString(line2)
        print_('1) ', line1[:500])
        print_('2) ', line2[:500])
        if l1.feedurl != '':
            print_('Dealing with a smart bookmark')
            print_(l1.feedurl)
            l1.href = l2.href
        if l1.href != l2.href:
            print_("Entries don't share location!")
            raise Exception
        if line1 == line2.replace(l2.id, l1.id):
            print_('strings only differ by ID')
        l1ad, l2ad = l1.ad, l2.ad
        l1recent = l2recent = 0
        for r in ('lv', 'lm'):
            if r in l1:
                l1recent = l1recent * (l1recent > l1[r][0]) or l1[r][0]
            if r in l2:
                l2recent = l2recent * (l2recent > l2[r][0]) or l2[r][0]

        if l1recent > l2recent:
            print_('choosing (1)')
            new = copy.copy(line1)
            if l1ad == '' and l2ad == '':
                pass
            elif l1ad == '' and l2ad != '':
                print_('but using ADD_DATE from 2')
                extra = 'ADD_DATE="' + str(l2ad[0]) + '" '
                if new[0:8] == '<DT><H3 ':
                    new = new[0:8] + extra + new[8:]
                else:
                    inpos = 15 + len(l1.href)
                    new = new[0:inpos] + extra + new[inpos:]
            elif l2ad != '' and l2ad[0] < l1ad[0]:
                print_('but replacing ADD_DATE with that from 2')
                new = new.replace(str(l1ad[0]), str(l2ad[0]))
        else:
            print_('choosing (2)')
            new = copy.copy(line2)
            if l2ad == '' and l1ad == '':
                pass
            elif l2ad == '' and l1ad != '':
                print_('but using ADD_DATE from 1')
                extra = 'ADD_DATE="' + str(l1ad[0]) + '" '
                if new[0:8] == '<DT><H3 ':
                    new = new[0:8] + extra + new[8:]
                else:
                    inpos = 15 + len(l2.href)
                    new = new[0:inpos] + extra + new[inpos:]
            elif l1ad != '' and l1ad[0] < l2ad[0]:
                print_('but replacing ADD_DATE with that from 1')
                new = new.replace(str(l2ad[0]), str(l1ad[0]))
        print_('NEW) ', new[:500])
    print_('')
    return new


def count_folders(bookmarkdict):
    """utility function to count the total number of folders in the collection"""
    count = 0
    for entry in bookmarkdict.values():
        if type(entry) == OrderedDict:
            count += 1
            count += count_folders(entry)

    return count


if __name__ == '__main__':
    pass