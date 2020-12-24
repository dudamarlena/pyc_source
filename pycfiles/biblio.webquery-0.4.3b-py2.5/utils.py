# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/biblio/webquery/utils.py
# Compiled at: 2009-05-06 14:40:43
"""
Various utilities.

"""
__docformat__ = 'restructuredtext en'
import re
from bibrecord import PersonalName
EDITOR_PATS = [ re.compile(x, flags=re.IGNORECASE + re.UNICODE) for x in [
 '^edited by\\s+',
 '\\s*, editors\\.?$',
 '^editors,?\\s*']
              ]
STRIP_PATS = [ re.compile(x, flags=re.IGNORECASE + re.UNICODE) for x in [
 '^by\\s+',
 '\\s*;\\s+with an introduction by .*$',
 '^\\[\\s*',
 '\\s*\\]$',
 '\\.{3,}',
 'et[\\. ]al\\.',
 '\\[',
 '\\]',
 '\\([^\\)]+\\)',
 '\\s*;.*$']
             ]
AND_PAT = re.compile('\\s+and\\s+')
COLLAPSE_SPACE_RE = re.compile('\\s+')
PUBLISHER_RES = [ re.compile(p, flags=re.IGNORECASE + re.UNICODE) for p in [
 '^(?P<city>.*)\\s*:\\s*(?P<pub>.*)\\s*,\\s*c?(?P<year>\\d{4})\\.?$',
 '^(?P<pub>.*)\\.?$']
                ]

def normalize_isbn(isbn):
    """
        Remove formatting from an ISBN, making it suitable for web-queries.
        """
    return isbn.replace(' ', '').replace('-', '').lower().strip()


def parse_single_name(name_str):
    """
        Clean up an indivdual name into a more consistent format.
        """
    family = given = other = ''
    name_str = COLLAPSE_SPACE_RE.sub(' ', name_str.strip())
    if ', ' in name_str:
        name_parts = name_str.split(', ', 1)
        family = name_parts[0].strip()
        given_other = name_parts[1].split(' ', 1)
        given = given_other[0]
        other = given_other[1:]
    else:
        name_parts = name_str.split(' ')
        given = name_parts[0]
        other_family = name_parts[1:]
        if other_family:
            family = other_family[(-1)]
            other = (' ').join(other_family[:-1])
    if family.endswith('.'):
        family = family[:-1]
    name = PersonalName(given)
    name.family = family or ''
    name.other = other or ''
    return name


def parse_names(name_str):
    """
        Clean up a list of names into a more consistent format.

        :Parameters:
                name_str : string
                        The "author" attribute from a Xisbn record in XML.
        
        :Returns:
                A list of the authors in "reverse" format, e.g. "['Smith, A. B.',
                'Jones, X. Y.']"

        Xisbn data can be irregularly formatted, unpredictably including
        ancillary information. This function attempts to cleans up the author field
        into a list of consistent author names.
        
        For example::

                >>> n = parse_names ("Leonard Richardson and Sam Ruby.")
                >>> print (n[0].family == 'Richardson')
                True
                >>> print (n[0].given == 'Leonard')
                True
                >>> print (not n[0].other)
                True
                >>> n = parse_names ("Stephen P. Schoenberger, Bali Pulendran")
                >>> print (n[0].family == 'Schoenberger')
                True
                >>> print (n[0].given == 'Stephen')
                True
                >>> print (n[0].other == 'P.')
                True
                >>> n = parse_names ("Madonna")
                >>> print (not n[0].family)
                True
                >>> print (n[0].given == 'Madonna')
                True
                >>> print (not n[0].other)
                True
                
        """
    name_str = name_str.strip()
    if not name_str:
        return []
    for pat in STRIP_PATS:
        name_str = pat.sub('', name_str)

    name_str = AND_PAT.sub(', ', name_str)
    auth_list = name_str.split(', ')
    name_list = [ parse_single_name(x) for x in auth_list ]
    return name_list


def parse_editing_info(name_str):
    """
        Detect whethers names are editors and returns
        
        Returns:
                Whether editing information was recognised and the name with that
                editing information removed.
                
        For example::

                >>> parse_editing_info ("Leonard Richardson and Sam Ruby.")
                (False, 'Leonard Richardson and Sam Ruby.')
                >>> parse_editing_info ("Ann Thomson.")
                (False, 'Ann Thomson.')
                >>> parse_editing_info ("Stephen P. Schoenberger, Bali Pulendran, editors.")
                (True, 'Stephen P. Schoenberger, Bali Pulendran')
                >>> print parse_editing_info ("Madonna")
                (False, 'Madonna')
        
        """
    name_str = name_str.strip()
    if not name_str:
        return (
         False, '')
    for pat in EDITOR_PATS:
        match = pat.search(name_str)
        if match:
            return (
             True, pat.sub('', name_str))

    return (False, name_str)


def parse_publisher(pub_str):
    """
        Parse a string of publisher information.

        :Parameters:
                pub_str : string
                        text giving publisher details.
                
        :Returns:
                A tuple of strings, being (<publisher>, <city of publication>,
                <year of publication>). If no value is available, an empty string
                returned.
                
        As with author names, publication details are often inconsistently set out,
        even in bibliographic data. This function attempts to parse out and
        normalise the details.
        
        For example::
        
                >>> parse_publisher ('New York: Asia Pub. House, c1979.')
                ('Asia Pub. House', 'New York', '1979')
                >>> parse_publisher ('New York : LearningExpress, 1999.')
                ('LearningExpress', 'New York', '1999')
                >>> parse_publisher ('HarperTorch')
                ('HarperTorch', '', '')
                >>> parse_publisher ('Berkeley Heights, NJ: Enslow Publishers, c2000.')
                ('Enslow Publishers', 'Berkeley Heights, NJ', '2000')
                
        """
    for re in PUBLISHER_RES:
        match = re.search(pub_str)
        if match:
            fields = [
             'pub', 'city', 'year']
            match_vals = match.groupdict(None)
            return tuple([ match_vals.get(f, '').strip() for f in fields ])

    return ('', '', '')


def _doctest():
    import doctest
    doctest.testmod()


if __name__ == '__main__':
    _doctest()