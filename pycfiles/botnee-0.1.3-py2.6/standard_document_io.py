# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/botnee/standard_document_io.py
# Compiled at: 2012-08-16 08:16:39
"""
Reading of standard document files
"""
import os, io, re, dateutil.parser, logging
from botnee import debug
from botnee.standard_document import StandardDocument
regular_expressions = {'header': re.compile('([^:]*) ?: ?(.*)'), 
   'guid': re.compile('[A-Za-z0-9:.\\-/_]*')}
std_doc_logger = logging.getLogger(__name__)

def count_files(collector_directory='/home/tdiethe/BMJ/journal-collector-output/', suffix='txt', verbose=False, recursive=True):
    """
    Simply counts how many standard document files are in the directory
    (and subdirectories if recursive=True)
    """
    count = 0
    if recursive:
        for (root, subs, allfiles) in os.walk(collector_directory):
            for fname in allfiles:
                if fname.endswith(suffix):
                    count += 1

    for name in os.listdir(collector_directory):
        if name.endswith(suffix):
            count += 1

    return count


def read_directory(collector_directory='/home/tdiethe/BMJ/journal-collector-output/', suffix='txt', verbose=False, recursive=True):
    """
    Reads a directory - only processes files with the suffix given. 
    Returns a list of dictionary objects
    """
    docs = []
    if recursive:
        for (root, subs, allfiles) in os.walk(collector_directory):
            for fname in allfiles:
                if fname.endswith(suffix):
                    doc = load_document(os.path.join(root, fname), verbose)
                    if doc:
                        yield doc

    for name in os.listdir(collector_directory):
        if name.endswith(suffix):
            doc = load_document(os.path.join(collector_directory, name), verbose)
            if doc:
                yield doc


def load_document(fname, verbose=False):
    """Loads a single file in standard document format"""
    with io.open(fname, 'rU', encoding='utf-8') as (f):
        doc = parse_document(f, fname, verbose)
        f.close()
        if doc:
            doc['filename'] = fname
    return doc


def parse_document(input_doc, fname='web request', verbose=False):
    """
    Parses a single document using iterator functionality.
    doc could be a file or a list with a line on each row
    
    required_fields = ['guid', 'url', 'publication-date', 'title']
    
    publication-date must pass through dateutil.parser.parse()
    """
    in_body = False
    if type(input_doc) in [str, unicode]:
        input_doc = input_doc.split('\n')
    elif type(input_doc) is io.TextIOWrapper:
        pass
    else:
        debug.debug_here()
        str_error = 'Unexpected input_doc type: ' + str(type(input_doc)) + ' - can handle text or files'
        debug.print_verbose(str_error, verbose, std_doc_logger)
        return
    doc = StandardDocument()
    for (line_num, line) in enumerate(input_doc):
        line = line.strip()
        if line == '':
            in_body = True
            continue
        if not in_body:
            s = regular_expressions['header'].split(line)
            try:
                if s[1] == 'publication-date':
                    try:
                        doc[s[1]] = dateutil.parser.parse(s[2])
                    except ValueError, e:
                        debug.print_verbose('Unknown date format ' + s[2], verbose, std_doc_logger)
                        debug.debug_here()
                        doc['failed'] = {'reason': 'date', 'extra': s[2]}
                        return doc

                elif s[1] == 'guid':
                    guid = regular_expressions['guid'].match(s[2]).group()
                    if ' ' in guid or guid is not s[2]:
                        debug.print_verbose('Error in parsing ' + fname + ': invalid guid ' + guid, verbose, std_doc_logger)
                        doc['failed'] = {'reason': 'guid', 'extra': guid}
                        return doc
                    doc[s[1]] = guid
                else:
                    doc[s[1]] = s[2]
            except IndexError, e:
                debug.print_verbose('Error in parsing %s at line %d' % (
                 fname, line_num), verbose, std_doc_logger)
                try:
                    debug.print_verbose(line, verbose, std_doc_logger)
                except UnicodeEncodeError, e:
                    debug.print_verbose(e, verbose, std_doc_logger)

                doc['failed'] = {'reason': 'bad_line', 'extra': (line_num, line)}
                return doc

        else:
            doc['body'] += ' ' + line

    result = doc.check_for_failures()
    if result is not None:
        debug.print_verbose('Error in parsing ' + fname + ': missing ' + result, verbose, std_doc_logger)
    return doc