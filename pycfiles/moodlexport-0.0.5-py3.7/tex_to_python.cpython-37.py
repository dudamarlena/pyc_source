# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\moodlexport\tex_to_python.py
# Compiled at: 2020-05-04 12:05:19
# Size of source mod 2**32: 4539 bytes
from moodlexport.python_to_moodle import *
from TexSoup import TexSoup
from TexSoup.data import TexNode
from TexSoup.utils import TokenWithPosition

def read_latex_question(latex_question):
    if len(latex_question.args) == 1:
        question = Question(latex_question.args[0].value)
        list_contents = list(latex_question.contents)[1:]
    else:
        question = Question()
        list_contents = list(latex_question.contents)
    text = ''
    for content in list_contents:
        if isinstance(content, TokenWithPosition):
            text = text + content.text

    question.text(cleanstr(text, raw=True))
    return question


def read_latex_category(category_latex):
    if len(category_latex.args) == 1:
        category = Category(category_latex.args[0].value)
        list_contents = list(category_latex.contents)[1:]
    else:
        category = Category()
        list_contents = list(category_latex.contents)
    for content in list_contents:
        if isinstance(content, TexNode):
            field = str(content.name)
            if field == 'name':
                category.name(content.string)
            elif field == 'description':
                category.description(content.string)
            elif field == 'question':
                question = read_latex_question(content)
                question.addto(category)

    return category


def latextopython(file_name):
    with open(file_name, 'r', encoding='utf-8') as (file):
        latex = file.read()
    soup = TexSoup(latex)
    category_list = []
    category_latex_list = list(soup.find_all('category'))
    if len(category_latex_list) > 0:
        for category_latex in category_latex_list:
            category_list.append(read_latex_category(category_latex))

    else:
        category = Category()
        question_latex_list = list(soup.find_all('question'))
        for question_latex in question_latex_list:
            read_latex_question(question_latex).addto(category)

        category_list = [
         category]
    return category_list


def latextomoodle(file_name, save_name=None):
    category_list = latextopython(file_name)
    counter = 1
    for category in category_list:
        if save_name is None:
            category.save()
        else:
            if len(category_list) == 1:
                string = save_name
            else:
                string = save_name + '_' + str(counter)
                counter = counter + 1
            category.save(string)