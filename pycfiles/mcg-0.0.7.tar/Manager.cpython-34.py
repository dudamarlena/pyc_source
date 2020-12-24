# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/jlopes/PycharmProjects/mcg/core/Manager.py
# Compiled at: 2017-01-24 01:10:58
# Size of source mod 2**32: 1902 bytes
import os
from core.GeneratorFactory import GeneratorFactory
from core.db.MongoDB import MongoDB

class Manager:

    def __init__(self, args):
        self.project = args['project']
        self.api = args['api']

    def begin(self):
        generator = GeneratorFactory()
        db = self._Manager__connect_to_database
        if self.project:
            if db.projects.find_one({'project_id': self.project}):
                if self.api:
                    if db.forms.find_one({'name': self.api}):
                        data = db.forms.find_one({'name': self.api})
                        if os.path.exists('.meteor'):
                            os.chdir('imports/api/')
                        else:
                            os.chdir(self.project + '/imports/api/')
                        os.mkdir(data['name'])
                        os.chdir(data['name'])
                        args = {'project': self.project,  'api': self.api,  'data': data}
                        generator.generate_file('ModelGenerator', args)
                        generator.generate_file('ModelTestsGenerator', args)
                        generator.generate_file('MethodsGenerator', args)
                        generator.generate_file('MethodsTestsGenerator', args)
                        generator.generate_file('PublicationGenerator', args)
                        generator.generate_file('PublicationTestsGenerator', args)
                    else:
                        print('Form not found')
                else:
                    args = {'project': self.project}
                    generator.generate_file('ProjectGenerator', args)
            else:
                print('Project not found')
        else:
            print('Project [-p, --project] argument is necessary')

    @property
    def __connect_to_database(self):
        mongodb = MongoDB()
        return mongodb.get_database()