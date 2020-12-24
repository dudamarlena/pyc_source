# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\moodlexport\python_to_latex.py
# Compiled at: 2020-05-05 14:22:16
# Size of source mod 2**32: 2977 bytes
from moodlexport.python_to_moodle import Category, Question, latex_protect, alias, savestr
import requests, os.path
LATEX_PACKAGE_URL = 'https://raw.githubusercontent.com/Guillaume-Garrigos/moodlexport/master/latex/latextomoodle.sty'
LATEX_PACKAGE_NAME = 'latextomoodle'

def latexfile_preamble(list_of_packages=[]):
    string = '\\documentclass{article}\n'
    string += '\\usepackage{amsmath}\n'
    for package in list_of_packages:
        string += latex_protect('\\usepackage{') + package + '}\n'

    return string


def latexfile_begin(env_name, option=None):
    string = latex_protect('\x08egin{' + env_name + '}')
    if option is not None:
        string += '[' + str(option) + ']'
    return string + '\n'


def latexfile_end(env_name):
    return latex_protect('\\end{' + env_name + '}') + '\n'


def latexfile_command(cmd_name, value, option=None):
    string = latex_protect('\\' + cmd_name)
    if option is not None:
        string += '[' + str(option) + ']'
    string += '{' + latex_protect(str(value)) + '}\n'
    return string


def latexfile_environement(env_name, value, option=None):
    string = latexfile_begin(env_name, option)
    string += value + '\n'
    string += latexfile_end(env_name)
    return string


def latexfile_append_question(question):
    content = ''
    for field in question.structure:
        if field not in ('@type', 'questiontext', 'answer') and question.structure[field]['isset']:
            content += latexfile_command(alias(field), question.structure[field]['value'])

    content += latex_protect(question.structure['questiontext']['value'])
    option = question.structure['@type']['value']
    if option == 'multichoice':
        if question.structure['answer']['isset']:
            content += '\n'
            for answer in question.structure['answer']['value']:
                content += latexfile_command('answer', answer['text'], str(answer['grade']))

    return latexfile_environement('question', content, option)


def latexfile_append_category(category):
    content = ''
    description = category.getdescription()
    if description != '':
        content += latexfile_command('description', description)
    for question in category.question_objects:
        content += latexfile_append_question(question)

    return latexfile_environement('category', content, category.getname())


def latexfile_document(category, custom_package=True):
    if custom_package:
        content = latexfile_preamble([LATEX_PACKAGE_NAME])
        req = os.path.isfile(LATEX_PACKAGE_NAME + '.sty') or requests.get(LATEX_PACKAGE_URL)
        savestr(req.text, LATEX_PACKAGE_NAME + '.sty')
    else:
        content = latexfile_preamble()
    content += latexfile_environement('document', latexfile_append_category(category))
    return content