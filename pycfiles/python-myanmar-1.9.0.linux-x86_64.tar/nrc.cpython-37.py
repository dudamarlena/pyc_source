# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/trhura/Code/pythonenv/lib/python3.7/site-packages/myanmar/nrc.py
# Compiled at: 2019-10-01 11:34:23
# Size of source mod 2**32: 3586 bytes
import re, json, pkgutil
township_names = json.loads(pkgutil.get_data('myanmar', 'data/nrc_townships.json').decode('utf-8'))
ccode = range(1, 14)
nation_dict = {'naing':'n', 
 'pyu':'p', 
 'ae':'e', 
 'n':'n', 
 'p':'p', 
 'e':'e'}
city_code_re = '(\\d{1,2}?)\\s*'
township_name_re = '\\s*(\\b\\w.*\\s*\\w.*\\s*\\b)\\s*'
nation_re = '(\\b\\w.*\\b)'
number_re = '\\s*(\\b[0-9][0-9]{5}\\b)'
nrc_format = re.compile(city_code_re + '[/ .,]' + township_name_re + '[( .,]' + nation_re + '[,. )]' + number_re)

def is_valid_nrc(nrc):
    """
    Check whether the given string is
    valid Myanmar national registration ID or not

    >>> is_valid_nrc('12/LMN (N) 144144')
    True
    >>> is_valid_nrc('5/PMN (N) 123456')
    False
    """
    nrc = nrc.lower()
    match = nrc_format.search(nrc)
    if not match:
        return False
    city_code = int(match.group(1))
    township_name = match.group(2)
    nation = match.group(3)
    cname_no_space = township_name.replace(' ', '')
    cname_no_vowel = re.sub('[aeiou]', '', cname_no_space)
    if city_code not in ccode:
        return False
    if cname_no_vowel not in township_names[str(city_code)]:
        return False
    if nation not in nation_dict:
        return False
    return True


def normalize_nrc(nrc):
    """
    Check the given string is valid myanmar nrc or not and
    normalize the string to simplest form if the string is valid

    >>> normalize_nrc('9/pmn(n)123456')
    '9 pamana n 123456'
    >>> normalize_nrc('1/bkn(n)123456')
    '1 bakana n 123456'
    """
    nrc = nrc.lower()
    search = is_valid_nrc(nrc)
    if not search:
        raise RuntimeError('%s is not a valid Myanmar nrc number.' % nrc)
    match = nrc_format.search(nrc)
    city_code = int(match.group(1))
    township_name = match.group(2)
    nation = match.group(3)
    number = match.group(4)
    cname_no_space = township_name.replace(' ', '')
    cname_no_vowel = re.sub('[aeiou]', '', cname_no_space)
    nation_no_space = nation.replace(' ', '')
    nrc_normalize = str(city_code) + ' ' + township_names[str(city_code)][cname_no_vowel] + ' ' + nation_dict[nation_no_space] + ' ' + number
    return nrc_normalize