# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/githsearch/githsearch.py
# Compiled at: 2016-02-21 13:06:13
# Size of source mod 2**32: 3789 bytes
"""
Usage for githsearch :
options :
    -h or --help : display instructions
    -r or --repo [args] : search for args in github repos
    -u or --user [args] : search for args in github users
    -l or --limit : know your rate limit
example :
    githsearch -r python tetris
"""
from urllib.request import build_opener
from urllib.parse import urlencode
import json, sys
__all__ = [
 'GithSearch', 'get_repo', 'get_user', 'get_limit']
PURPLE = '\x1b[1;35m'
NO_COLOUR = '\x1b[0m'

class GithSearch:
    __doc__ = "\n    Usage :\n    Instantiate the class\n    >>> g=GithSearch()\n    Search for a repo :\n    >>> g.get_repo('python tetris pygame')\n    Search for a user :\n    >>> g.get_user('toto')\n    Know the rate_limit :\n    >>> g.get_limit\n    "

    def __init__(self):
        self.opener = build_opener()
        self.opener.addheaders.append(('User-agent', 'GithSearch - search Github from the CLI in Python, the quick and dirty way (github.com/bayang)'))

    def fetch_url(self, url, query):
        params = urlencode({'q': query})
        final = url.format(params)
        response = self.opener.open(final).read().decode('utf-8')
        dict_response = json.loads(response)
        return dict_response

    def get_repo(self, query):
        """Results are sorted by best match. Default sort order is desc
        """
        base_url = 'https://api.github.com/search/repositories?{}&per_page=50'
        res = self.fetch_url(base_url, query)
        resp = []
        for item in res['items']:
            resp.append((item['html_url'], item['description']))

        return resp

    def get_user(self, query):
        """Results are sorted by best match. Default sort order is desc
        """
        base_url = 'https://api.github.com/search/users?{}&per_page=50'
        res = self.fetch_url(base_url, query)
        respo = []
        for item in res['items']:
            respo.append((item['login'], item['html_url']))

        return respo

    @property
    def get_limit(self):
        """get your rate limit (e.g. the number of free requests remaining)
        """
        response = self.opener.open('https://api.github.com/rate_limit').read().decode('utf-8')
        txt = json.loads(response)
        return txt['resources']['search']

    @staticmethod
    def print_results(results):
        print('****** Query returned : ******')
        for item in results:
            print(PURPLE, '-->', item[0], NO_COLOUR)
            print('    --', item[1])


def main():
    g = GithSearch()
    rep = ['-r', '--repo', '--repository']
    usr_kw = ['-u', '--user']
    hlp = ['-h', '--help', '--please', '--what']
    lim = ['-l', '--limit']
    if len(sys.argv) == 1 or sys.argv[1].lower() in hlp:
        print(__doc__)
    else:
        if sys.argv[1].lower() in rep:
            res = g.get_repo(sys.argv[2:])
            g.print_results(res)
        else:
            if sys.argv[1].lower() in usr_kw:
                res = g.get_user(' '.join(sys.argv[2:]))
                g.print_results(res)
            else:
                if sys.argv[1].lower() in lim:
                    print(g.get_limit)
                else:
                    print(__doc__)


if __name__ == '__main__':
    main()