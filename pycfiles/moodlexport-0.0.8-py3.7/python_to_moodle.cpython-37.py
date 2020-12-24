# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\moodlexport\python_to_moodle.py
# Compiled at: 2020-05-05 13:46:20
# Size of source mod 2**32: 12116 bytes
from xml.dom.minidom import parseString
from xml.sax.saxutils import unescape
import xmltodict, io, numpy as np, os
DICT_DEFAULT_QUESTION_MOODLE = {'@type':{'default':'essay', 
  'alias':'type'}, 
 'name':{'default':'Default question title', 
  'attribute':{'@format': 'txt'}, 
  'alias':'title'}, 
 'questiontext':{'default':'Default question text', 
  'attribute':{'@format': 'html'}, 
  'alias':'text'}, 
 'generalfeedback':{'default':'', 
  'attribute':{'@format': 'html'}}, 
 'defaultgrade':{'default':1.0, 
  'alias':'grade'}, 
 'penalty':{'default': 0.0}, 
 'hidden':{'default': 0}, 
 'idnumber':{'default': ''}, 
 'responseformat':{'default': 'editorfilepicker'}, 
 'responserequired':{'default': 0}, 
 'responsefieldlines':{'default': 10}, 
 'attachments':{'default': -1}, 
 'attachmentsrequired':{'default': 0}, 
 'graderinfo':{'default':'', 
  'attribute':{'@format': 'html'}, 
  'alias':'infocorrecteur'}, 
 'responsetemplate':{'default':'', 
  'attribute':{'@format': 'html'}}, 
 'single':{'default': 'true'}, 
 'shuffleanswers':{'default': 'true'}, 
 'answernumbering':{'default': 'none'}, 
 'correctfeedback':{'default':'Votre réponse est correcte.', 
  'attribute':{'@format': 'html'}}, 
 'partiallycorrectfeedback':{'default':'Votre réponse est partiellement correcte.', 
  'attribute':{'@format': 'html'}}, 
 'incorrectfeedback':{'default':'Votre réponse est incorrecte.', 
  'attribute':{'@format': 'html'}}, 
 'shownumcorrect':{'default': ''}, 
 'answer':{'default': ''}}
UNESCAPE_LATEX = {'\x07':'\\a', 
 '\x0c':'\\f',  '\x0b':'\\v',  '\x08':'\\b',  '\n':'\\n',  '\r':'\\r',  '\t':'\\t'}

def alias(field):
    if 'alias' in DICT_DEFAULT_QUESTION_MOODLE[field]:
        return DICT_DEFAULT_QUESTION_MOODLE[field]['alias']
    return field


def isfield(string):
    for key in DICT_DEFAULT_QUESTION_MOODLE.keys():
        if string in [key, alias(key)]:
            return True

    return False


def cleanstr(string, raw=False):
    if raw:
        string = string.replace('\t', '')
        string = string.replace('\n', '')
    else:
        string = string.replace('\t', '  ')
    return string


def savestr(string, filename='new.txt', raw=False):
    string = cleanstr(string, raw)
    text_file = io.open(filename, 'w', encoding='utf8')
    text_file.write(string)
    text_file.close()


def latex_protect(string):
    return unescape(string, UNESCAPE_LATEX)


def html(string):
    if string is '':
        return string
    return '<![CDATA[<p>\\(\\)' + latex_protect(string) + '</p>]]>'


def set_oparg(name, default_value, **opargs):
    if name in opargs:
        return opargs.get(name)
    return default_value


class Category:
    __doc__ = ' \n        Object collecting Questions under the form of a category, ready to export to Moodle.\n        Methods:\n        _set(name, description) : e.g. _set("my_category", "list of questions about ... ")\n        append(question) : adds a Question to the Category\n        save(file_name) : save the Category into Moodle-XML\n    '

    def __init__(self, name='Default category name', description=''):
        self.dict = {'quiz': {'question': [{}]}}
        self.questions = self.dict['quiz']['question']
        self._set(name, description)
        self.question_objects = []

    def _set(self, name='Default category name', description=''):
        qcat = {'@type':'category', 
         'category':{'text': '$module$/top/' + name}, 
         'info':{'@format':'html', 
          'text':html(description)}}
        self.questions[0] = qcat

    def name(self, string='Default category name'):
        self.questions[0]['category']['text'] = '$module$/top/' + string

    def description(self, string=''):
        self.questions[0]['info']['text'] = html(string)

    def getname(self):
        return self.questions[0]['category']['text'][len('$module$/top/'):]

    def getdescription(self):
        return self.questions[0]['info']['text']

    def append(self, question):
        self.questions.append(question.dict)
        self.question_objects.append(question)

    def save(self, file_name=None):
        """ Save a category under the format Moodle XML """
        if file_name is None:
            file_name = self.getname()
        category_xml = xmltodict.unparse((self.dict), pretty=True)
        savestr(unescape(category_xml), file_name + '.xml')

    def savetex(self, file_name=None):
        """ Save a category under the format TEX """
        import moodlexport.python_to_latex
        if file_name is None:
            file_name = self.getname()
        savestr(moodlexport.python_to_latex.latexfile_document(self), file_name + '.tex')

    def savepdf(self, file_name=None):
        """ Save a category under the format PDF """
        if file_name is None:
            file_name = self.getname()
        if not os.path.isfile(file_name + '.tex'):
            self.savetex(file_name)
        os.system('latexmk -pdf ' + file_name + '.tex')
        os.system('latexmk -c ' + file_name + '.tex')


class Question:
    __doc__ = ' \n        Object collecting the parameters of a question under the form of a dictionary.\n        Methods:\n        _set(field, value) : e.g. _set("questiontext", "What is $2+2$?")\n    '

    def __init__(self, question_type='essay'):
        self.structure = DICT_DEFAULT_QUESTION_MOODLE
        self.dict = {}
        for field in self.structure:
            self._set(field, self.structure[field]['default'])

        self._set('@type', question_type)
        self.answer_objects = []
        self.structure['answer']['value'] = []

    def _set(self, field, value=''):
        """ Assigns a value to a field of a Question """
        field_structure = self.structure[field]
        field_structure['value'] = value
        field_structure['isset'] = value != self.structure[field]['default']
        if 'attribute' not in field_structure:
            self.dict[field] = value
        else:
            if 'html' in field_structure['attribute'].values():
                value = html(value)
            self.dict[field] = {**(field_structure['attribute']), **{'text': value}}

    def multi_answer(self):
        self.dict['single'] = 'false'

    def addto(self, category):
        category.append(self)

    def save(self, optional_name='Default category name'):
        cat = Category(optional_name)
        cat.append(self)
        cat.save()

    def answer(self, answer_text='This is a default answer', grade=0):
        ans = Answer(answer_text, grade)
        ans.addto(self)
        self.structure['answer']['isset'] = True
        self.structure['answer']['value'].append({'text':answer_text,  'grade':ans.dict['@fraction']})


for key in DICT_DEFAULT_QUESTION_MOODLE.keys():
    if key is not 'answer':
        setattr(Question, alias(key), lambda self, value, key=key: self._set(key, value))
        setattr(Question, key, lambda self, value, key=key: self._set(key, value))

class Answer:
    __doc__ = ' \n        Object collecting an answer to a multichoice Question\n    '

    def __init__(self, answer_text='This is a default answer', grade=0):
        if isinstance(grade, bool) or isinstance(grade, np.bool):
            if grade:
                grade = 100
        else:
            grade = 0
        self.dict = {'@fraction':grade, 
         '@format':'html', 
         'text':html(answer_text), 
         'feedback':{'@format':'html', 
          'text':''}}

    def text(self, text):
        self.dict['text'] = html(text)

    def feedback(self, text):
        self.dict['feedback']['text'] = html(text)

    def relativegrade(self, answer_fraction):
        self.dict['@fraction'] = answer_fraction

    def istrue(self):
        self.relativegrade(100)

    def isfalse(self):
        self.relativegrade(0)

    def addto(self, question):
        """"""
        if question.dict['@type'] == 'multichoice':
            if question.dict['answer'] == '':
                question.dict['answer'] = []
            question.dict['answer'].append(self.dict)
            question.answer_objects.append(self)
        else:
            print('Error : answers can only be added to multichoice questions')