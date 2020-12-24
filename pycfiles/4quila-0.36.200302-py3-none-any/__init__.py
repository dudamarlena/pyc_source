# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/zed/venvs/4ch/lib/python2.7/site-packages/fourch/__init__.py
# Compiled at: 2014-09-20 11:39:24
__doc__ = " fourch (stylised as 4ch) is an easy-to-implement Python wrapper for\n    4chan's JSON API, as provided by moot.\n\n    It uses the documentation of the 4chan API located at:\n        https://github.com/4chan/4chan-API\n\n    This is based off of the API last updated Aug 12, 2014.\n    (4chan-API commit: 1b2bc7858afc555127b8911b4d760480769872a9)\n"
from ._version import __version__
from .fourch import urls
from .thread import Thread
from .board import Board
from .reply import Reply
import requests

def boards(https=False):
    """ Get a list of all boards on 4chan, in :class:`fourch.board.Board`
        objects.

        :param https: Should we use HTTPS or HTTP?
        :type https: bool
    """
    s = requests.Session()
    s.headers.update({'User-Agent': ('fourch/{0} (@https://github.com/sysr-q/4ch)').format(__version__)})
    proto = 'https://' if https else 'http://'
    url = proto + urls['api'] + urls['api_boards']
    r = s.get(url)
    if r.status_code != requests.codes.ok:
        r.raise_for_status()
    boards = []
    for json_board in r.json()['boards']:
        boards.append(Board(json_board['board'], https=https))

    return boards