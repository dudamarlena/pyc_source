# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-intel/egg/onlinelinguisticdatabase/lib/bibtex.py
# Compiled at: 2016-09-19 13:27:02
r"""bibtex.py encodes and describes the BibTeX specification (see Kopka & Daly,
2004 for details).  Useful for validating OLD source input since the data
structure for OLD sources is the BibTeX data structure.

Use Pybtex (http://pybtex.sourceforge.net/manual.html) to parse BibTeX files if
need be:

from io import StringIO
from pybtex.database.input.bibtex import Parser

e1 = '''
@BOOK{knuth:86a,
  AUTHOR = "Donald E. Knuth",
  TITLE = {The \TeX{}book},
  EDITION = "third",
  PUBLISHER = "Addison--Wesley",
  ADDRESS = {Reading, Massachusetts},
  YEAR = 1986
}
'''.strip()

parser = Parser()
bib_data = parser.parse_stream(StringIO(e1))
knuth86a = parser.data.entries['knuth:86a']
unicode(knuth86a.persons['author'][0])
u'Knuth, Donald E.'

"""
entry_types = {'article': {'description': 'An article from a journal or magazine.', 
               'required': ('author', 'title', 'journal', 'year'), 
               'optional': ('volume', 'number', 'pages', 'month', 'note')}, 
   'book': {'description': 'A book with an explicit publisher.', 
            'required': (('author', 'editor'), 'title', 'publisher', 'year'), 
            'optional': (('volume', 'number'), 'series', 'address', 'edition', 'month', 'note')}, 
   'booklet': {'description': 'A work that is printed and bound, but without a named publisher or sponsoring institution.', 
               'required': ('title', ), 
               'optional': ('author', 'howpublished', 'address', 'month', 'year', 'note')}, 
   'conference': {'description': 'The same as inproceedings, included for Scribe compatibility.', 
                  'required': ('author', 'title', 'booktitle', 'year'), 
                  'optional': (
                             'editor', ('volume', 'number'), 'series', 'pages',
                             'address', 'month', 'organization', 'publisher', 'note')}, 
   'inbook': {'description': 'A part of a book, usually untitled. May be a chapter (or section or whatever) and/or a range of pages.', 
              'required': (
                         ('author', 'editor'), 'title', ('chapter', 'pages'),
                         'publisher', 'year'), 
              'optional': (('volume', 'number'), 'series', 'type', 'address', 'edition', 'month', 'note')}, 
   'incollection': {'description': 'A part of a book having its own title.', 
                    'required': ('author', 'title', 'booktitle', 'publisher', 'year'), 
                    'optional': (
                               'editor', ('volume', 'number'), 'series', 'type', 'chapter',
                               'pages', 'address', 'edition', 'month', 'note')}, 
   'inproceedings': {'description': 'An article in a conference proceedings.', 
                     'required': ('author', 'title', 'booktitle', 'year'), 
                     'optional': (
                                'editor', ('volume', 'number'), 'series', 'pages',
                                'address', 'month', 'organization', 'publisher', 'note')}, 
   'manual': {'description': 'Technical documentation.', 
              'required': ('title', ), 
              'optional': ('author', 'organization', 'address', 'edition', 'month', 'year', 'note')}, 
   'mastersthesis': {'description': "A Master's thesis.", 
                     'required': ('author', 'title', 'school', 'year'), 
                     'optional': ('type', 'address', 'month', 'note')}, 
   'misc': {'description': 'For use when nothing else fits.', 
            'required': (), 
            'optional': ('author', 'title', 'howpublished', 'month', 'year', 'note')}, 
   'phdthesis': {'description': 'A Ph.D. thesis.', 
                 'required': ('author', 'title', 'school', 'year'), 
                 'optional': ('type', 'address', 'month', 'note')}, 
   'proceedings': {'description': 'The proceedings of a conference.', 
                   'required': ('title', 'year'), 
                   'optional': (
                              'editor', ('volume', 'number'), 'series', 'address',
                              'month', 'publisher', 'organization', 'note')}, 
   'techreport': {'description': 'A report published by a school or other institution, usually numbered within a series.', 
                  'required': ('author', 'title', 'institution', 'year'), 
                  'optional': ('type', 'number', 'address', 'month', 'note')}, 
   'unpublished': {'description': 'A document having an author and title, but not formally published.', 
                   'required': ('author', 'title', 'note'), 
                   'optional': ('month', 'year')}}
other_entry_types = ('collection', 'patent')
universally_optional_field_names = ('key', 'crossrefurl', 'crossref')
field_names = ('address', 'annote', 'author', 'booktitle', 'chapter', 'crossref', 'edition',
               'editor', 'howpublished', 'institution', 'journal', 'key', 'month',
               'note', 'number', 'organization', 'pages', 'publisher', 'school',
               'series', 'title', 'type', 'url', 'volume', 'year')
other_field_names = ('affiliation', 'abstract', 'contents', 'copyright', 'ISBN', 'ISSN',
                     'keywords', 'language', 'location', 'LCCN', 'mrnumber', 'price',
                     'size')