# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-intel/egg/snipsmanager/utils/intent_class_generator.py
# Compiled at: 2017-11-11 03:08:58
""" Tools to automatically generate intent classes from an assistant
    definition.
"""
import os, re, json, zipfile
from jinja2 import Environment, PackageLoader
from .os_helpers import create_dir

def camel_case_to_underscore(text):
    """ Convert camel-case to underscore.

    :param text: a text, potentially in camel-case format.
    :return: the text, converted to underscore format.
    """
    underscored = re.sub('(.)([A-Z][a-z]+)', '\\1_\\2', text)
    return re.sub('([a-z0-9])([A-Z])', '\\1_\\2', underscored).lower()


def to_camelcase_capitalized(text):
    """ Convert to camel-case and capitalize.

    :param text: a text, potentially with dashes and underscores.
    :return: the text, converted to cancel-case format, and capitalized.
    """
    hyphens = re.sub('(?!^)-([a-zA-Z])', lambda m: m.group(1).upper(), text)
    underscores = re.sub('(?!^)_([a-zA-Z])', lambda m: m.group(1).upper(), hyphens)
    return underscores[:1].upper() + underscores[1:]


def save_intent_file(output_dir, filename, text):
    """ Save a text string to a given file.

    :param filename: a file name.
    :param text: a text to save.
    """
    create_dir(output_dir)
    create_dir(('{}/intents').format(output_dir))
    output_filename = ('{}/intents/{}').format(output_dir, filename)
    with open(output_filename, 'w') as (output_file):
        output_file.write(text)


class IntentClassGenerator:
    """ Tools to automatically generate intent classes from an assistant
        definition.
    """

    def __init__(self):
        """ Initialisation. """
        self.jinja_env = Environment(loader=PackageLoader('snipsmanager', 'templates'))

    def generate_intent_file(self, intent, output_dir):
        """ Given a JSON intent, generate the corresponding Python intent class
            file.

        :param intent: a JSON intent.
        """
        template = self.jinja_env.get_template('intent_template.py')
        file_content = template.render(intent=intent)
        filename = camel_case_to_underscore(to_camelcase_capitalized(intent['name'])) + '_intent.py'
        save_intent_file(output_dir, filename, file_content)

    def generate_intent_registry_file(self, intents, output_dir):
        """ Given a list of intents, generate an intents registry, which is
            a list of intent classes.

        :param intents: a list of intents.
        """
        template = self.jinja_env.get_template('intent_registry_template.py')
        file_content = template.render(intents=intents)
        with open(('{}/intent_registry.py').format(output_dir), 'w') as (output_file):
            output_file.write(file_content)

    def generate(self, assistant_filename, output_dir):
        """ Generate intent classes from assistant.json specification.

        :param assistant_filename: path to the assistant zip file
        :param output_dir: directory to which the intents and registry should be
                           written.
        """
        self.jinja_env.globals.update(camel_case_to_underscore=camel_case_to_underscore)
        self.jinja_env.globals.update(to_camelcase_capitalized=to_camelcase_capitalized)
        intents = []
        content = zipfile.ZipFile(assistant_filename).read('assistant/assistant.json')
        data = json.loads(content.decode('utf-8'))
        for intent in data['intents']:
            self.generate_intent_file(intent, output_dir)
            intents.append(intent)

        self.generate_intent_registry_file(intents, output_dir)
        with open(('{}/__init__.py').format(output_dir), 'w') as (output_file):
            output_file.write('')
        with open(('{}/intents/__init__.py').format(output_dir), 'w') as (output_file):
            output_file.write('')