# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/rfc2xml/rfc2xml.py
# Compiled at: 2019-09-08 12:19:27
# Size of source mod 2**32: 4739 bytes
import parsley, string, os, sys, itertools
from typing import List as TypingList, Tuple, Union
from .elements import Rfc, Date, Author, Organization, Workgroup, Xref, T, TocItem, Section, List, Figure, Artwork

class Rfc2Xml:

    @staticmethod
    def get_parser_file(filename):
        with open(filename) as (fp):
            grammar = fp.read()
        return Rfc2Xml.get_parser(grammar)

    @staticmethod
    def get_parser(grammar):
        return parsley.makeGrammar(grammar, {'punctuation':string.punctuation, 
         'ascii_uppercase':string.ascii_uppercase, 
         'ascii_lowercase':string.ascii_lowercase, 
         'itertools':itertools, 
         'ExtendedDiagrams':Rfc2Xml, 
         'rfc':Rfc(compliant=True), 
         'Date':Date, 
         'Xref':Xref, 
         'TocItem':TocItem, 
         'Section':Section, 
         'List':List, 
         'Figure':Figure, 
         'Artwork':Artwork, 
         'T':T, 
         'rfc_title_docname':Rfc2Xml.rfc_title_docname, 
         'rfc_title_abbrev':Rfc2Xml.rfc_title_abbrev, 
         'front_names':Rfc2Xml.front_names, 
         'text_paragraph':Rfc2Xml.text_paragraph, 
         'sections':Rfc2Xml.sections, 
         'printr':Rfc2Xml.printr})

    @staticmethod
    def parse(string: str) -> Rfc:
        string += '\n\n'
        parser = Rfc2Xml.get_parser_file(filename=(os.path.dirname(os.path.realpath(__file__)) + '/grammar.txt'))
        return parser(string).rfc()

    @staticmethod
    def rfc_title_docname(rfc: 'Rfc', title: str, docname: str):
        if not docname:
            docname = None
        rfc.docname = docname
        rfc.front.set_title(title)

    @staticmethod
    def rfc_title_abbrev(rfc: 'Rfc', abbrev: str):
        if rfc.front.title.abbrev is None:
            rfc.front.title.abbrev = abbrev

    @staticmethod
    def front_names(rfc: 'Rfc', data: TypingList[Tuple]):
        left, right = zip(*data)
        names = []
        for item in right:
            if item is None:
                continue
            if item['type'] == 'name':
                names.append(item)
            elif item['type'] == 'organization':
                organization = Organization(item['name'])
                for name in names:
                    author = Author(initials=(name['initials']),
                      surname=(name['surname']),
                      organization=organization,
                      role=(Rfc2Xml.suffix_to_role(name['role'])))
                    rfc.front.authors.append(author)

                names = []
            else:
                raise Exception('Invalid item type ', item['type'])

        rfc.front.workgroup = Workgroup(left[0])

    @staticmethod
    def suffix_to_role(suffix: str):
        if suffix is None:
            return
        suffix = suffix.lower()
        if suffix == 'ed':
            return 'editor'
        print('Warning: Found unknown author suffix ', suffix, file=(sys.stderr))
        return suffix

    @staticmethod
    def text_paragraph(arr: TypingList[Union[(str, Xref)]], hang_text: str=None):
        o = [
         arr[0]]
        for a in arr[1:]:
            if isinstance(a, str):
                if isinstance(o[(-1)], str):
                    o[(-1)] += a
                else:
                    o.append(a)
            else:
                o.append(a)

        return T(children=o, hang_text=hang_text)

    @staticmethod
    def sections(arr: TypingList[Section]):
        out = []
        current = []
        current_level = None
        for a in reversed(arr):
            split = a.number.split('.')
            level = len(split) - 1
            if current_level is None:
                current_level = level
            else:
                if level > current_level:
                    out = current + out
                    current = []
                    current_level = level
                if level == current_level:
                    current.insert(0, a)
            if level < current_level:
                a.children += current
                current = [a]
                current_level = level

        return current + out

    @staticmethod
    def printr(x, v=None):
        print(str(x))
        if v is None:
            return x
        return v