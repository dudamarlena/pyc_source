# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\nekos\nekos.py
# Compiled at: 2020-03-05 10:24:48
# Size of source mod 2**32: 2381 bytes
import urllib
from . import http, dict, errors
noresponse = "Couldn't contact the API right now..."

def eightball():
    r = http.get('/8ball')
    return dict.JsonDict({'text':r['response'], 
     'image':r['url']})


def img(target: str):
    possible = [
     'feet', 'yuri', 'trap', 'futanari', 'hololewd', 'lewdkemo',
     'solog', 'feetg', 'cum', 'erokemo', 'les', 'wallpaper', 'lewdk',
     'ngif', 'tickle', 'lewd', 'feed', 'gecg', 'eroyuri', 'eron',
     'cum_jpg', 'bj', 'nsfw_neko_gif', 'solo', 'kemonomimi', 'nsfw_avatar',
     'gasm', 'poke', 'anal', 'slap', 'hentai', 'avatar', 'erofeet', 'holo',
     'keta', 'blowjob', 'pussy', 'tits', 'holoero', 'lizard', 'pussy_jpg',
     'pwankg', 'classic', 'kuni', 'waifu', 'pat', '8ball', 'kiss', 'femdom',
     'neko', 'spank', 'cuddle', 'erok', 'fox_girl', 'boobs', 'random_hentai_gif',
     'smallboobs', 'hug', 'ero', 'smug', 'goose', 'baka', 'woof']
    if target is None:
        raise errors.EmptyArgument('You have to at least define an argument in string format\nArguments: {}'.format(possible))
    if target.lower() not in possible:
        raise errors.InvalidArgument("You haven't added any valid arguments\nArguments: {}".format(possible))
    try:
        if target.lower() == 'random_hentai_gif':
            r = http.get('/img/Random_hentai_gif')
        else:
            r = http.get('/img/' + target.lower())
    except Exception as e:
        try:
            raise errors.NothingFound(noresponse)
        finally:
            e = None
            del e

    return r['url']


def owoify(text: str):
    if text is None:
        raise errors.EmptyArgument('You have to enter a string you want to enter to API')
    r = http.get('/owoify?text=' + urllib.parse.quote(text))
    return r['owo']


def cat():
    try:
        return http.get('/img/meow')['url']
    except Exception as e:
        try:
            raise errors.NothingFound(noresponse)
        finally:
            e = None
            del e


def textcat():
    try:
        return http.get('/cat')['cat']
    except Exception as e:
        try:
            raise errors.NothingFound(noresponse)
        finally:
            e = None
            del e


def why():
    try:
        return http.get('/why')['why']
    except Exception as e:
        try:
            raise errors.NothingFound(noresponse)
        finally:
            e = None
            del e


def fact():
    try:
        return http.get('/fact')['fact']
    except Exception as e:
        try:
            raise errors.NothingFound(noresponse)
        finally:
            e = None
            del e