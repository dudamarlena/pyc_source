# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/jlopes/PycharmProjects/mcg/core/PublicationGenerator.py
# Compiled at: 2017-01-24 01:10:58
# Size of source mod 2**32: 877 bytes
from core.Generator import Generator
import os

class PublicationGenerator(Generator):

    def __init__(self, args):
        self.project = args['project']
        self.api = args['api']
        self.data = args['data']

    def insert_into_file(self):
        pass

    def generate(self):
        os.mkdir('server')
        os.chdir('server')
        publications = open('publications.js', 'a')
        publications.write("import { Meteor } from 'meteor/meteor';\n")
        publications.write('import { ' + self.data['name'] + " } from '../" + self.data['name'] + ".js';\n\n")
        for pub in self.data['publications']:
            publications.write("Meteor.publish('" + pub['name'] + "', () => {\n")
            publications.write('\treturn ' + self.data['name'] + '.' + pub['return'] + ';\n')
            publications.write('});\n\n')

        publications.close()