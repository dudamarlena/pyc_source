# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/big/ENV2/lib/python2.7/site-packages/cloudmesh_piazza/piazza.py
# Compiled at: 2016-09-12 11:27:15
"""Usage:
   piazza [--file] get FOLDER
   piazza convert FOLDER [--html|--latex]

Process FILE and optionally apply correction to either left-hand side or
right-hand side.

Arguments:
  FOLDER     optional input file

Options:
  -h --help

"""
from __future__ import print_function
from docopt import docopt
import yaml, os, json
from cm_piazza_api import PiazzaExtractor

def main():
    arguments = docopt(__doc__)
    print(arguments)
    if arguments['--file']:
        with open('.piazza', 'r') as (stream):
            try:
                config = yaml.load(stream)
            except yaml.YAMLError as exc:
                print(exc)

        print(config)
        password = config['piazza']['password']
        email = config['piazza']['email']
        print(email, password)
    else:
        password = None
        email = None
    if arguments['get']:
        folder = arguments['FOLDER']
        print(folder)
        piazza = PiazzaExtractor()
        email, password = piazza.get_login()
        piazza.login(email=email, password=password)
        piazza.save_folder_posts(folder)
    elif arguments['convert']:
        html = arguments['--html']
        latex = arguments['--latex']
        folder = arguments['FOLDER']
        json_data = open(folder + '.json').read()
        data = json.loads(json_data)
        if html:
            html_file = open(folder + '.html', 'w+')
            for post in data['feed']:
                html_file.write(('\n\n<h1> {subject} </h1>\n').format(**post))
                html_file.write(('Uid: {uid}<br>\n').format(**post))
                html_file.write(('Created: {created}<br>\n').format(**post))
                html_file.write('\n')
                content = post['content'].encode('utf-8')
                html_file.write(content)

            html_file.close()
    return


if __name__ == '__main__':
    main()