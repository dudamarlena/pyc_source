# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/nushell/examples/pokemon/nu_plugin_pokemon.py
# Compiled at: 2019-10-24 11:59:16
# Size of source mod 2**32: 3232 bytes
from nushell.sink import SinkPlugin
from pokemon.master import get_pokemon, catch_em_all
from pokemon.skills import get_ascii, get_avatar

def list_pokemon(do_sort=False):
    """print list of all names of pokemon in database

       Parameters
       ==========
       do_sort: return list of sorted pokemon (ABC)
    """
    names = catch_em_all(return_names=True)
    if do_sort:
        names.sort()
    for name in names:
        try:
            print(name)
        except:
            pass


def catch_pokemon():
    """use the get_pokemon function to catch a random pokemon, return it
       (along with stats!) as a single string
    """
    catch = get_pokemon()
    for pokemon_id, meta in catch.items():
        response = meta['ascii']
        response = '%s\n%s %s' % (response, meta['name'], meta['link'])
        print(response)


def sink(plugin, params):
    """sink will be executed by the calling SinkPlugin when method is "sink"
       and should be able to parse the dictionary of params and respond
       appropriately. Since this is a sink, whatever you print to stdout
       will show for the user. Useful functions:

       plugin.logger.<level>
    """
    if params.get('catch', False):
        plugin.logger.info('We want to catch a random pokemon!')
        catch_pokemon()
    else:
        if params.get('list', False):
            plugin.logger.info('We want to list Pokemon names.')
            list_pokemon()
        else:
            if params.get('list-sorted', False):
                plugin.logger.info('We want to list sorted Pokemon names.')
                list_pokemon(do_sort=True)
            else:
                if params.get('avatar', '') != '':
                    plugin.logger.info('We want a pokemon avatar!')
                    catch = get_avatar(params['avatar'])
                else:
                    if params.get('pokemon', '') != '':
                        get_ascii(name=(params['pokemon']))
                    else:
                        print(plugin.get_help())


def main():
    plugin = SinkPlugin(name='pokemon', usage='Catch an asciinema pokemon on demand.')
    plugin.add_named_argument('catch', 'Switch', usage='catch a random pokemon')
    plugin.add_named_argument('list', 'Switch', usage='list pokemon names')
    plugin.add_named_argument('list-sorted', 'Switch', usage='list sorted names')
    plugin.add_named_argument('avatar', 'Optional', 'String', 'generate avatar')
    plugin.add_named_argument('pokemon', 'Optional', 'String', 'get pokemon')
    plugin.run(sink)


if __name__ == __main__:
    main()