# uncompyle6 version 3.6.7
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/pycommunity/glossary.py
# Compiled at: 2007-02-15 14:01:36
__doc__ = ' Glossary reader and render\n'
import os, logging
from Cheetah.Template import Template
from generator import BaseTask
from generator import registerTask

class GlossaryReader(list):
    """reads glossary entries"""

    def __init__(self, filename):

        def _clean(element):
            element = element.lower()
            return element.strip()

        self.filename = filename
        words = []
        for line in open(filename):
            line = line.strip()
            if line.startswith('#'):
                continue
            elements = line.split(':')
            if len(elements) != 2:
                continue
            word = _clean(elements[0])
            if word in words:
                continue
            self.append((word, _clean(elements[1])))
            words.append(word)

    def getDefinition(self, word):
        """returns a definition"""
        word = word.lower()
        for (word_, definition) in self:
            if word_ == word:
                return definition

        raise KeyError('%s not found' % word)


class GlossaryView(object):
    """renders a view using a cheetah template"""

    def __init__(self, templatefile, glossary):
        self._glossary = glossary
        self._template = Template(open(templatefile).read(), searchList=[{'glossary': glossary}])

    def render(self):
        """renders the html"""
        return str(self._template)

    __call__ = render


class GlossaryTask(BaseTask):
    """creates the glossary file"""

    def _getName(self):
        """returns the task name"""
        return 'glossary'

    def _run(self, configuration):
        """reads the glossary file, and generate
        the html file"""
        targets = configuration.targets.values()
        glossary = GlossaryReader(configuration.glossary)
        view = GlossaryView(configuration.templates['glossary'], glossary)
        result = view()
        for target in targets:
            path = os.path.join(target, 'glossary.html')
            path = os.path.realpath(path)
            logging.info('writing %s' % path)
            glossary_file = open(path, 'w')
            try:
                glossary_file.write(result)
            finally:
                glossary_file.close()


registerTask(GlossaryTask)