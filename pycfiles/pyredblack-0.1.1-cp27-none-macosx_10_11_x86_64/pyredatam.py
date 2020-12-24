# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyredatam/pyredatam.py
# Compiled at: 2015-09-21 12:56:27
__doc__ = b'\npyredatam.py\n\nRedatam object created from a .dic file that generate queries.\n'
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import with_statement

def arealist_query(area_level, variables, area_filter=None, universe_filter=None, title=None):
    """Generate an Area List REDATAM query.

    Args:
        area_level (str): Level of geographical area of the list.
        variables (str or list): Variable/s that will be asked for their data.
        area_filter (str or list): Geographical area/s where results are asked.
        universe_filter (str): REDATAM filter exrpession.
        title (str): Title of the results table.

    Returns:
        str: REDATAM query ready to paste in a processor.

    >>> print(arealist_query("FRAC", "PERSONA.CONDACT",
    ...                      {"PROV": ["02", "03"]}))
    RUNDEF Job
        SELECTION INLINE,
         PROV 02, 03
    <BLANKLINE>
    TABLE TABLE1
        AS AREALIST
        OF FRAC, PERSONA.CONDACT
    """
    lines = [
     b'RUNDEF Job']
    if area_filter:
        lines.append(b'    SELECTION INLINE,')
        area_type = area_filter.keys()[0]
        areas = area_filter.values()[0]
        if type(areas) != list:
            areas = [
             areas]
        lines.append((b'     {} {}').format(area_type, (b', ').join(areas)))
    if universe_filter:
        lines.append(b'    UNIVERSE ' + universe_filter)
    lines.append(b'')
    lines.append(b'TABLE TABLE1')
    if title:
        lines.append(b'    TITLE "' + title + b'"')
    lines.append(b'    AS AREALIST')
    if type(variables) != list:
        variables = [
         variables]
    lines.append((b'    OF {}, {}').format(area_level, (b', ').join(variables)))
    return (b'\n').join(lines)


if __name__ == b'__main__':
    import doctest
    doctest.testmod()