# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mendeley2biblatex/bib_entry.py
# Compiled at: 2016-07-20 04:49:35
# Size of source mod 2**32: 3608 bytes


class BibEntry:
    TEMPLATES = {'JournalArticle': '\n@article{{{entry[citationKey]},\n    author    = "{entry[authors]}",\n    title     = "{entry[title]}",\n    journal   = "{entry[publication]}",\n    number    = "{entry[issue]}",\n    volume    = "{entry[volume]}",\n    pages     = "{entry[pages]}",\n    year      = "{entry[year]}",\n    doi       = "{entry[doi]}",\n}}', 
     'ConferenceProceedings': '\n@proceedings{{{entry[citationKey]},\n    author    = "{entry[authors]}",\n    title     = "{entry[title]}",\n    publisher = "{entry[publisher]}",\n    pages     = "{entry[pages]}",\n    year      = "{entry[year]}",\n    doi       = "{entry[doi]}",\n}}', 
     'WebPage': '\n@online{{{entry[citationKey]},\n    author    = "{entry[authors]}",\n    title     = "{entry[title]}",\n    year      = "{entry[year]}",\n    url       = "{entry[url]}",\n    urldate   = "{entry[urldate]}"\n}}', 
     'Book': '\n@book{{{entry[citationKey]},\n    author    = "{entry[authors]}",\n    title     = "{entry[title]}",\n    publisher = "{entry[publisher]}",\n    year      = "{entry[year]}",\n    pages     = "{entry[pages]}",\n    volume    = "{entry[volume]}",\n    doi       = "{entry[doi]}",\n}}', 
     'BookSection': '\n@inbook{{{entry[citationKey]},\n    author    = "{entry[authors]}",\n    title     = "{entry[title]}",\n    booktitle = "{entry[publication]}",\n    publisher = "{entry[publisher]}",\n    year      = "{entry[year]}",\n    volume    = "{entry[volume]}",\n    pages     = "{entry[pages]}",\n    doi       = "{entry[doi]}",\n    url       = "{entry[url]}",\n    urldate   = "{entry[urldate]}"\n}}', 
     'Patent': '\n@thesis{{{entry[citationKey]},\n    author    = "{entry[authors]}",\n    title     = "{entry[title]}",\n    number    = "{entry[number]}",\n    year      = "{entry[year]}",\n    type      = "{entry[sourceType]}",\n    doi       = "{entry[doi]}",\n    url       = "{entry[url]}",\n    urldate   = "{entry[urldate]}"\n}}', 
     'Report': '\n@inbook{{{entry[citationKey]},\n    author    = "{entry[authors]}",\n    title     = "{entry[title]}",\n    type = "{entry[publication]}",\n    institution = "{entry[institution]}",\n    year      = "{entry[year]}",\n    type      = "{entry[sourceType]}",\n    doi       = "{entry[doi]}",\n    pages     = "{entry[pages]}",\n    url       = "{entry[url]}",\n    urldate   = "{entry[urldate]}"\n}}', 
     'Thesis': '\n@thesis{{{entry[citationKey]},\n    author    = "{entry[authors]}",\n    title     = "{entry[title]}",\n    institution = "{entry[institution]}",\n    year      = "{entry[year]}",\n    type      = "{entry[sourceType]}",\n    doi       = "{entry[doi]}",\n    pages     = "{entry[pages]}",\n    url       = "{entry[url]}",\n    urldate   = "{entry[urldate]}"\n}}'}

    @staticmethod
    def clean_characters(entry):
        """A helper function to convert special characters to LaTeX characters"""
        char_to_replace = {'&': '\\&', 
         '#': '\\#', 
         '–': '--', 
         '—': '--', 
         '∕': '/', 
         'κ': 'k', 
         '×': 'x', 
         '"': "'"}
        entry_key = [
         'publisher', 'publication', 'title']
        for k in entry_key:
            for char, repl_char in char_to_replace.items():
                entry[k] = entry[k].replace(char, repl_char)