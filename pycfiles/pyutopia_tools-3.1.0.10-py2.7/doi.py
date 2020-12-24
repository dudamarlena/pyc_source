# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/utopia/tools/doi.py
# Compiled at: 2017-06-20 22:46:59
import re
_inner_regex = '(10\\.\\d+/[^%"\\#\\s]+)'
_strip_regex = '[^\\d\\w]+'

def search(text):
    """Look for first DOI in some text"""
    match = re.search(_inner_regex, text)
    if match is not None:
        return re.sub(('(^{0}|{0}$)').format(_strip_regex), '', match.group(0))
    else:
        return


def findall(text):
    """Look for all DOIs in some text"""
    matches = re.findall(_inner_regex, text)
    return [ re.sub(('(^{0}|{0}$)').format(_strip_regex), '', match) for match in matches ]


__all__ = [
 'search', 'findall']
try:
    import spineapi
    _regex = '(?:(?:doi|digital\\s+object\\s+id(?:entifier)?)\\s*\\S?\\s*)?' + _inner_regex

    def scrape(document):
        """Look for a DOI in the document"""
        margin = 90
        dois = []
        for match in document.search(_regex, spineapi.IgnoreCase + spineapi.RegExp):
            page, _, (_, _), (width, height) = pageArea = match.begin().pageArea()
            _, orientation, (left, top), (right, bottom) = lineArea = match.begin().lineArea()
            if page > 2:
                break
            if page == 2 and len(dois) > 0:
                break
            if orientation > 0:
                dois[0:0] = [
                 match.text()]
            elif top > height - margin:
                dois[0:0] = [
                 match.text()]
            else:
                dois.append(match.text())

        if len(dois) > 0:
            doi = dois[0]
            doi = re.search(_inner_regex, doi).group(0)
            doi = re.sub(('(^{0}|{0}$)').format(_strip_regex), '', doi)
            doi = re.sub('[-\xad‐‑–-―⸺⸻]', '-', doi)
            return doi


    __all__[:] = ['scrape']
except ImportError:
    logger.info('spineapi not imported: document scraping of DOIs will be unavailable')
    spineapi = None