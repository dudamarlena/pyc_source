# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Library/Python/2.7/site-packages/src/etl/wpapi.py
# Compiled at: 2012-12-26 15:42:47
"""
    This module defines a class for interfacing with http://www.mediawiki.org/wiki/API:Main_page

    Example: ::

        >>> import libraries.etl.WPAPI
        >>> api = WPAPI.WPAPI()
        >>> api.getDiff(515866670)
        (u'[[Category:People from Palermo]] [[Category:Sportspeople from Sicily|Palermo]] [[Category:Sport in Palermo|People]] [[Category:Sportspeople by city in Italy|Palermo]]', True    )
"""
__author__ = 'Ryan Faulkner and Aaron Halfaker'
__date__ = 'October 3rd, 2012'
__license__ = 'GPL (version 2 or later)'
import sys, logging, types, re, time, urllib, urllib2, json, htmlentitydefs
logging.basicConfig(level=logging.DEBUG, stream=sys.stderr, format='%(asctime)s %(levelname)-8s %(message)s', datefmt='%b-%d %H:%M:%S')

class WPAPI:
    """
        The class itself implements functionality that allows a user to examine revision text.

        The constructor allows the user ot specify the particular api.
    """
    DIFF_ADD_RE = re.compile('<td class="diff-addedline"><div>(.+)</div></td>')

    def __init__(self, uri='http://en.wikipedia.org/w/api.php'):
        self.uri = uri

    def getDiff(self, revId, retries=20):
        attempt = 0
        is_content = False
        while attempt < retries:
            try:
                response = urllib2.urlopen(self.uri, urllib.urlencode({'action': 'query', 
                   'prop': 'revisions', 
                   'revids': revId, 
                   'rvprop': 'ids', 
                   'rvdiffto': 'prev', 
                   'format': 'json'}))
                result = json.load(response)
                diff = result['query']['pages'].values()[0]['revisions'][0]['diff']['*']
                if type(diff) not in types.StringTypes or diff == '':
                    response = urllib2.urlopen(self.uri, urllib.urlencode({'action': 'query', 
                       'prop': 'revisions', 
                       'revids': revId, 
                       'rvprop': 'content', 
                       'format': 'json'}))
                    result = json.load(response)
                    try:
                        diff = result['query']['pages'].values()[0]['revisions'][0]['*']
                    except KeyError:
                        sys.stderr.write('x')
                        diff = ''

                    if type(diff) not in types.StringTypes:
                        diff = ''
                    is_content = True
                return (diff, is_content)
            except urllib2.HTTPError as e:
                time.sleep(2 ** attempt)
                attempt += 1
                logging.error('HTTP Error: %s.  Retry #%s in %s seconds...' % (e, attempt, 2 ** attempt))

    def getAdded(self, revId):
        diff, is_content = self.getDiff(revId)
        if is_content:
            return diff
        else:
            return self.unescape(('\n').join(match.group(1) for match in WPAPI.DIFF_ADD_RE.finditer(diff)))

    def unescape(self, text):

        def fixup(m):
            text = m.group(0)
            if text[:2] == '&#':
                try:
                    if text[:3] == '&#x':
                        return unichr(int(text[3:-1], 16))
                    else:
                        return unichr(int(text[2:-1]))

                except ValueError:
                    pass

            else:
                try:
                    text = unichr(htmlentitydefs.name2codepoint[text[1:-1]])
                except KeyError:
                    pass

            return text

        return re.sub('&#?\\w+;', fixup, text)