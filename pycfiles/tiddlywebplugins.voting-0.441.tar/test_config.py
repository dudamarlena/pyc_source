# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Jon/Documents/TiddlyWiki/Trunk/contributors/JonRobson/TiddlyWeb/plugins/voting/test/test_config.py
# Compiled at: 2010-04-17 06:32:23
votebag = 'tiddlyvoting'
from tiddlyweb.config import config
from tiddlywebplugins import voting
from tiddlyweb.model.tiddler import Tiddler
from tiddlyweb.model.bag import Bag
from tiddlyweb.model.user import User
from tiddlyweb.model.policy import Policy
from tiddlyweb.store import Store, NoTiddlerError, NoBagError, NoRecipeError

def setup(store):
    try:
        store.delete(Bag(votebag))
    except NoBagError:
        pass

    snowwhitebag = Bag('snow white')
    snowwhitebag.policy = Policy('jon', [], ['admin'], ['admin'], ['admin'])
    mrmenbag = Bag('mr_and_mrs')
    mrmenbag.policy = Policy('jon', ['jon', 'andrew', 'martin'], ['admin'], ['admin'], ['admin'])
    films = Bag('films')
    films.policy = Policy(accept=['NONE'])
    try:
        store.delete(mrmenbag)
    except NoBagError:
        pass

    try:
        store.delete(snowwhitebag)
    except NoBagError:
        pass

    try:
        store.delete(films)
    except NoBagError:
        pass

    voting.setup_store(config)
    users = ['jon', 'FND', 'andrew', 'martin']
    for user in users:
        store.put(User(user))

    mrmendata = [{'title': 'mr clumbsy', 'tags': ['kitty', 'pet', 'cat'], 'fields': {}}, {'title': 'mr thin', 'tags': ['dog', 'pet'], 'fields': {}}, {'title': 'mr tickle', 'tags': ['cat', 'animal', 'bogof'], 'fields': {'%s.total' % votebag: '2'}}, {'title': 'mr messy', 'tags': ['lion'], 'fields': {}}, {'title': 'mr strong', 'tags': ['monkey', 'lolcat'], 'fields': {'%s.total' % votebag: '923'}}, {'title': 'mr tall', 'tags': ['dinosaur', 'kitty', 'tiger'], 'fields': {}}, {'title': 'little miss naughty', 'tags': ['cAt', 'pet'], 'fields': {}}, {'title': 'mr small', 'tags': ['pet', 'animal', 'kitty'], 'fields': {}}]
    snowwhitedata = [{'title': 'snow white', 'tags': [], 'fields': {}}, {'title': 'grumpy', 'tags': [], 'fields': {}}]
    filmdata = [{'title': 'Kill Bill', 'modifier': 'Ben'}, {'title': 'Kill Bill 2', 'modifier': 'Ben'}, {'title': 'Pulp Fiction', 'modifier': 'Ben'}, {'title': 'Jackie Brown', 'modifier': 'Ben'}]
    configSnowWhite = Tiddler('config::snow white', votebag)
    configSnowWhite.text = '\nincrement.range::-5,30\nincrement.limit::2\n'
    store.put(configSnowWhite)
    store.put(snowwhitebag)
    store.put(mrmenbag)
    store.put(films)
    tiddlers = []
    for tid in mrmendata:
        tiddler = Tiddler(tid['title'], 'mr_and_mrs')
        tiddler.fields = tid['fields']
        tiddler.tags = tid['tags']
        tiddlers.append(tiddler)
        store.put(tiddler)

    for tid in filmdata:
        tiddler = Tiddler(tid['title'], 'films')
        if 'modifier' in tid:
            tiddler.modifier = tid['modifier']
        tiddlers.append(tiddler)
        store.put(tiddler)

    for tid in snowwhitedata:
        tiddler = Tiddler(tid['title'], 'snow white')
        tiddler.fields = tid['fields']
        tiddler.tags = tid['tags']
        tiddlers.append(tiddler)
        store.put(tiddler)

    return tiddlers