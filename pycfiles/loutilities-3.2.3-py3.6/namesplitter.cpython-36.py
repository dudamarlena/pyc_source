# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\loutilities\namesplitter.py
# Compiled at: 2019-11-20 12:25:23
# Size of source mod 2**32: 8990 bytes
"""
namesplitter - name splitting method
=========================================

name splitting, adapted from the following

* https:#code.google.com/p/php-name-parser/source/browse/trunk/parser.php

also reviewed

* https:#github.com/pahanix/full-name-splitter

see http:#www.w3.org/International/questions/qa-personal-names for more information on international name formats

"""
import re
SALUTATIONS = 'mr master mister mrs miss ms dr rev fr'.split()
PREFIXES = 'de da la du di del dei pietro vda. dello della degli delle van vanden vere von der den heer ten ter vande vanden vander voor ver aan mc ben st. st'.split()
SUFFIXES = 'I II III IV V Senior Junior Jr Sr PhD APR RPh PE MD MA DMD CME'.split()

def split_full_name(full_name):
    full_name = full_name.strip()
    unfiltered_name_parts = full_name.split(' ')
    name_parts = []
    for word in unfiltered_name_parts:
        if word == '':
            pass
        else:
            if word[0] != '(':
                name_parts.append(word)

    num_words = len(name_parts)
    salutation = is_salutation(name_parts[0])
    suffix = is_suffix(name_parts[(len(name_parts) - 1)])
    start = 1 if salutation else 0
    end = num_words - 1 if suffix else num_words
    fname = ''
    initials = ''
    lname = ''
    i = start
    while i < end - 1:
        word = name_parts[i]
        if is_compound_lname(word):
            if i != start:
                break
        if is_initial(word):
            if i == start:
                fname += ' ' + word.upper()
            else:
                initials += ' ' + word.upper()
        else:
            fname += ' ' + fix_case(word)
        i += 1

    if end - start > 1:
        while i < end:
            lname += ' ' + fix_case(name_parts[i])
            i += 1

    else:
        fname = fix_case(name_parts[i])
    name = {}
    name['salutation'] = salutation
    name['fname'] = fname.strip()
    name['initials'] = initials.strip()
    name['lname'] = lname.strip()
    name['suffix'] = suffix
    return name


def is_salutation(word):
    word = word.replace('.', '').lower()
    if word in ('mr', 'master', 'mister'):
        return 'Mr.'
    if word == 'mrs':
        return 'Mrs.'
    if word in ('miss', 'ms'):
        return 'Ms.'
    if word == 'dr':
        return 'Dr.'
    if word == 'rev':
        return 'Rev.'
    else:
        if word == 'fr':
            return 'Fr.'
        return False


def is_suffix(word):
    word = word.replace('.', '')
    suffix_array = SUFFIXES
    for suffix in suffix_array:
        if suffix.lower() == word.lower():
            return suffix

    return False


def is_compound_lname(word):
    return word.lower() in PREFIXES


def is_initial(word):
    return len(word) == 1 or len(word) == 2 and word[1] == '.'


def is_camel_case(word):
    if re.match("([A-Z]*[a-z'][a-z']*[A-Z']|[a-z']*[A-Z'][A-Z']*[a-z'])[A-Za-z]*", word):
        return True
    else:
        return False


def fix_case(word):
    word = safe_ucfirst('-', word)
    word = safe_ucfirst('.', word)
    return word


def safe_ucfirst(separator, word):
    parts = word.split(separator)
    words = []
    for word in parts:
        words.append(word if is_camel_case(word) else word.lower().capitalize())

    return separator.join(words)


def main():
    """
    test name splitting function
    """
    import argparse, csv
    from . import version
    parser = argparse.ArgumentParser(version=('{0} {1}'.format('loutilities', version.__version__)))
    parser.add_argument('filename', help='csv file containing "name" column')
    args = parser.parse_args()
    filename = args.filename
    outfile = '.'.join(filename.split('.')[:-1]) + '-annotated.csv'
    _IN = open(filename, 'rb')
    IN = csv.DictReader(_IN)
    outfields = []
    for field in IN.fieldnames:
        outfields.append(field)
        if field == 'name':
            outfields += ['fname', 'lname', 'names']

    _OUT = open(outfile, 'wb')
    OUT = csv.DictWriter(_OUT, outfields)
    OUT.writeheader()
    try:
        for rec in IN:
            names = split_full_name(rec['name'])
            rec['fname'] = ' '.join([names['fname'], names['initials']]).strip()
            rec['lname'] = names['lname']
            if names['suffix']:
                rec['lname'] += ' ' + names['suffix']
            rec['lname'] = rec['lname'].strip()
            rec['names'] = names
            OUT.writerow(rec)

    finally:
        _IN.close()
        _OUT.close()


if __name__ == '__main__':
    main()