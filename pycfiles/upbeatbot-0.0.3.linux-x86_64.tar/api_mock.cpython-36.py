# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ndibari/development/UpBeatBot/venv/lib/python3.6/site-packages/upbeatbot/libs/api_mock.py
# Compiled at: 2020-03-08 17:39:03
# Size of source mod 2**32: 2524 bytes
import random

class Dummy(object):
    __doc__ = '\n    Dummy data object to hold arbitrary data. Good for mocking out various\n    classes and data structures used in program execution.\n    '

    def __init__(self):
        pass


class TwitterAPIMock(object):
    __doc__ = "\n    Class that mimics the endpoints used in the program. Doesn't actually call\n    the endpoints but instead returns fixture data similar to that of the\n    actual Twitter API\n    "

    def GetMentions(self, mentions=5):
        """
        Return data on user mentions
        return: List of Dummy objects that mimic the objects used in the
        Twitter API
        """
        mentions_list = []
        for i in range(mentions):
            mention = Dummy()
            mention.user = Dummy()
            mention.user.screen_name = 'Dummy'
            mention.text = 'Hey @UpBeatBot!'
            mention.favorited = True
            if random.randint(0, 10) % 2 == 0:
                mention.favorited = False
                mention.text += ' Send me a a picture of a {animal}'.format(animal=(random.choice([
                 'dog', 'bunny', 'kitten', 'pug', 'squirrel'])))
            mentions_list.append(mention)

        return mentions_list

    def PostUpdate(self, text, img):
        """
        Sends tweet to be posted. Doesn't actually return anything, so can
        be a simple `pass` method.
        """
        pass

    def CreateFavorite(self, status):
        """
        Favorites a specified tweet. Like with PostUpdate doesn't return
        anything in the real version so can be easily mocked
        """
        pass


class RequestsMock(object):
    __doc__ = '\n    Class to mock out the requests library. This negates the dependency on\n    cutestpaws.com to complete the tweet preparation process\n    '

    def get(self, url):

        def dummy_raise_for_status():
            pass

        resp = Dummy()
        resp.raise_for_status = dummy_raise_for_status
        resp.text = "<div id=photos><a href='foo'>Here is a div!</a></div>\n        <div id=single-cute-wrap><img src='bar'>Here is another!</img></div>"
        return resp

    class exceptions(object):
        __doc__ = '\n        Mock for requests.exceptions\n        Needed to circumvent import of ConnectionError exception\n        '

        class ConnectionError(object):
            pass