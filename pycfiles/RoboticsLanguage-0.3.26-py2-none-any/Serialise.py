# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/roboticslanguage/RoboticsLanguage/RoboticsLanguage/Tools/Serialise.py
# Compiled at: 2019-09-27 03:30:17
from RoboticsLanguage.Base import Utilities
from jinja2 import Template, TemplateError
default_template_engine_filters = {'tag': Utilities.tag, 
   'text': Utilities.text, 
   'dpath': Utilities.path, 
   'xpath': Utilities.xpath, 
   'dpaths': Utilities.paths, 
   'xpaths': Utilities.xpaths, 
   'parent': Utilities.parent, 
   'unique': Utilities.unique, 
   'dashes': Utilities.dashes, 
   'option': Utilities.option, 
   'children': Utilities.children, 
   'initials': Utilities.initials, 
   'fullCaps': Utilities.fullCaps, 
   'isDefined': Utilities.isDefined, 
   'camelCase': Utilities.camelCase, 
   'attribute': Utilities.attribute, 
   'todaysDate': Utilities.todaysDate, 
   'ensureList': Utilities.ensureList, 
   'attributes': Utilities.attributes, 
   'underscore': Utilities.underscore, 
   'optionalArguments': Utilities.optionalArguments, 
   'underscoreFullCaps': Utilities.underscoreFullCaps, 
   'sortListCodeByAttribute': Utilities.sortListCodeByAttribute}

def serialise(code, parameters, keywords, language, filters=default_template_engine_filters):
    snippet = ''
    try:
        keyword = keywords[code.tag]['output'][language]
        try:
            template = Template(keyword)
            for key, value in filters.iteritems():
                template.globals[key] = value

            children_elements = code.xpath('*[not(self::option)]')
            snippet = template.render(children=map(lambda x: serialise(x, parameters, keywords, language, filters), children_elements), childrenTags=map(lambda x: x.tag, children_elements), options=dict(zip(code.xpath('option/@name'), map(lambda x: serialise(x, parameters, keywords, language, filters), code.xpath('option')))), attributes=code.attrib, parentAttributes=code.getparent().attrib, parentTag=code.getparent().tag, text=Utilities.text(code), tag=code.tag, parameters=parameters, code=code, language=language)
            code.attrib[language] = snippet
        except TemplateError as e:
            Utilities.logErrors(Utilities.formatJinjaErrorMessage(e), parameters)

    except KeyError:
        if 'p' in code.keys():
            line_number, column_number, line = Utilities.positionToLineColumn(int(code.attrib['p']), parameters['text'])
        else:
            line_number = 0
            column_number = 0
            line = ''
        Utilities.logErrors(Utilities.errorMessage('Language semantic', "Keyword '" + code.tag + "' not defined", line_number=line_number, column_number=column_number, line=line), parameters)

    return snippet