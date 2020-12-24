# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/jlopes/PycharmProjects/mcg/core/MethodsTestsGenerator.py
# Compiled at: 2017-01-24 01:10:58
# Size of source mod 2**32: 1941 bytes
from core.Generator import Generator
from core.TestsGenerator import TestsGenerator
from faker import Factory

class MethodsTestsGenerator(Generator, TestsGenerator):

    def __init__(self, args):
        self.project = args['project']
        self.api = args['api']
        self.data = args['data']

    def insert_into_file(self):
        pass

    def generate(self):
        fake = Factory.create()
        methods_tests = open('methods.tests.js', 'a')
        methods_tests.write("import { Meteor } from 'meteor/meteor';")
        methods_tests.write("\nimport { assert } from 'meteor/practicalmeteor:chai';")
        methods_tests.write('\nimport { ' + self.api + " } from './" + self.api + ".js';")
        methods_tests.write("\nimport './methods.js';")
        methods_tests.write('\n')
        methods_tests.write('\nif (Meteor.isServer) {')
        methods_tests.write("\n\tdescribe('" + self.api + " methods', () => {")
        methods_tests.write('\n\t\tbeforeEach(() => {')
        methods_tests.write('\n\t\t\t' + self.api + '.remove({});')
        methods_tests.write('\n\t\t});')
        for method in self.data['methods']:
            methods_tests.write("\n\t\tit('can " + method['name'] + "', () => {")
            methods_tests.write("\n\t\t\tconst handler = Meteor.server.method_handlers['" + self.api + '.' + method['name'] + "'];")
            methods_tests.write('\n\t\t\thandler.apply({}, [')
            for field in self.data['fields']:
                super(MethodsTestsGenerator, self).fetch_type(methods_tests, field)
                methods_tests.write(', ')

            methods_tests.write(']);')
            methods_tests.write('\n\t\t\tassert.equal(' + self.api + '.find().count(), 1);')
            methods_tests.write('\n\t\t});')

        methods_tests.write('\n\t});')
        methods_tests.write('\n}')