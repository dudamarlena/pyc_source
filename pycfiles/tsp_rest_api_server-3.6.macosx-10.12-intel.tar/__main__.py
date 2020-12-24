# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Volumes/containers/caputo.marcos/Projects/logistic/env/lib/python2.7/site-packages/tsp_api/__main__.py
# Compiled at: 2017-10-01 21:21:03
from optparse import OptionParser
CONFIG_TEMPLATE = '\nDOMAIN = {\n    \'maps\': {\n        \'additional_lookup\': {\n            \'url\': \'regex("[\\w]+")\',\n            \'field\': \'title\',\n        },\n        \'schema\': {\n            \'title\': {\n                \'type\':\'string\'\n            },\n            \'routes\': {\n                \'type\':\'list\',\n                \'schema\': {\n                    \'type\':\'dict\',\n                    \'schema\': {\n                        \'origin\': {\'type\':\'string\'},\n                        \'destiny\': {\'type\':\'string\'},\n                        \'distance\': {\'type\':\'float\'}\n                    }\n                }\n            }\n        }\n    }\n\n}\n\nMONGO_HOST = %(default_key)r\nMONGO_PORT = 27017\nMONGO_DBNAME = \'tsp_rest_api_server\'\n\nRESOURCE_METHODS = [\'GET\', \'POST\']\nXML = False\n\n'

def generate_settings(parser, options, args):
    output = CONFIG_TEMPLATE % dict(default_key='0.0.0.0')
    with open('settings.py', 'a+') as (a_file):
        a_file.write(output)
        a_file.close()


def runserver(parser, options, args):
    from api import app
    app.debug = True
    app.run()


COMMANDS = {'runserver': runserver, 
   'settings': generate_settings}

def main():
    parser = OptionParser(usage='Usage: %prog runserver')
    options, args = parser.parse_args()
    try:
        command = args[0]
    except IndexError:
        parser.print_help()
        return

    if COMMANDS:
        if command in COMMANDS:
            COMMANDS[command](parser, options, args)
        else:
            parser.error('Unrecognised command: ' + command)


if __name__ == '__main__':
    main()