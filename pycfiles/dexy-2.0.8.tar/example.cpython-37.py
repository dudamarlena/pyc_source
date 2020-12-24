# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ana/dev/dexy-clean/dexy/filters/example.py
# Compiled at: 2020-03-18 15:12:33
# Size of source mod 2**32: 4373 bytes
"""
DexyFilters written to be examples of how to write filters.
"""
from dexy.doc import Doc
from dexy.filter import DexyFilter
import os

class Example(DexyFilter):
    __doc__ = '\n    Examples of how to write filters.\n    '
    aliases = []
    NODOC = True


class KeyValueExample(Example):
    __doc__ = '\n    Example of storing key value data.\n    '
    aliases = ['keyvalueexample']
    _settings = {'data-type':'keyvalue', 
     'output-extensions':[
      '.sqlite3', '.json']}

    def process(self):
        assert self.output_data.state == 'ready'
        self.output_data.append('foo', 'bar')
        self.output_data.save()


class AccessOtherDocuments(Example):
    __doc__ = '\n    Example of accessing other documents.\n    '
    aliases = ['others']

    def process_text(self, input_text):
        info = []
        info.append('Here is a list of previous docs in this tree (not including %s).' % self.key)
        for doc in self.doc.walk_input_docs():
            if not isinstance(doc, Doc):
                raise AssertionError
            else:
                n_children = len(doc.children)
                n_inputs = len(doc.inputs)
                if doc.output_data().has_data():
                    length = len(doc.output_data().data())
                else:
                    length = len(doc.output_data().ordered_dict())
            info.append('%s (%s children, %s inputs, length %s)' % (doc.key, n_children, n_inputs, length))

        s = '%s        ' % os.linesep
        return s.join(info)


class AddNewDocument(Example):
    __doc__ = '\n    A filter which adds an extra document to the tree.\n    '
    aliases = ['newdoc']

    def process_text(self, input_text):
        self.add_doc('newfile.txt|processtext', 'newfile')
        return 'we added a new file'


class ConvertDict(Example):
    __doc__ = '\n    Returns an ordered dict with a single element.\n    '
    aliases = ['dict']

    def process(self, input_text):
        self.output_data['1'] = str(self.input_data)
        self.output_data.save()


class ExampleProcessTextMethod(Example):
    __doc__ = '\n    Uses process_text method\n    '
    aliases = ['processtext']

    def process_text(self, input_text):
        return "Dexy processed the text '%s'" % input_text


class ExampleProcessMethod(Example):
    __doc__ = '\n    Calls `set_data` method to store output.\n    '
    aliases = ['process']

    def process(self):
        output = "Dexy processed the text '%s'" % self.input_data
        self.output_data.set_data(output)


class ExampleProcessMethodManualWrite(Example):
    __doc__ = '\n    Writes output directly to output file.\n    '
    aliases = ['processmanual']

    def process(self):
        input_data = self.input_data
        output = "Dexy processed the text '%s'" % input_data
        with open(self.output_filepath(), 'w') as (f):
            f.write(output)


class ExampleProcessWithDictMethod(Example):
    __doc__ = '\n    Stores sectional data using `process` method.\n    '
    aliases = ['processwithdict']
    _settings = {'data-type': 'sectioned'}

    def process(self):
        self.output_data['1'] = "Dexy processed the text '%s'" % self.input_data
        self.output_data.save()


class AbcExtension(Example):
    __doc__ = '\n    Only outputs extension .abc\n    '
    aliases = ['outputabc']
    _settings = {'output-extensions': ['.abc']}

    def process_text(self, input_text):
        return "Dexy processed the text '%s'" % input_text


class ExampleFilterArgs(Example):
    __doc__ = '\n    Prints out the args it receives.\n    '
    aliases = ['filterargs']
    _settings = {'abc':('The abc setting.', None), 
     'foo':('The foo setting.', None)}

    def process_text(self, input_text):
        result = [
         'Here are the filter settings:']
        for k in sorted(self.setting_values()):
            v = self.setting_values()[k]
            result.append('  %s: %s' % (k, v))

        result.append('Here are the document args:')
        for k in sorted(self.doc.args):
            v = self.doc.args[k]
            result.append('  %s: %s' % (k, v))

        return os.linesep.join(result)