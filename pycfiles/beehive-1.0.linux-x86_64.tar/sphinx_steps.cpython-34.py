# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python3.4/site-packages/beehive/formatter/sphinx_steps.py
# Compiled at: 2014-11-03 05:47:13
# Size of source mod 2**32: 12963 bytes
"""
Provides a formatter that generates Sphinx-based documentation
of available step definitions (step implementations).

TODO:
  * Post-processor for step docstrings.
  * Solution for requires: table, text
  * i18n keywords

.. seealso::
    http://sphinx-doc.org/
"""
from beehive.formatter.steps import AbstractStepsFormatter
from beehive.formatter import sphinx_util
from beehive.model import Table
import inspect, os.path, sys

class StepsModule(object):
    __doc__ = '\n    Value object to keep track of step definitions that belong to same module.\n    '

    def __init__(self, module_name, step_definitions=None):
        self.module_name = module_name
        self.step_definitions = step_definitions or []
        self._name = None
        self._filename = None

    @property
    def name(self):
        if self._name is None:
            module = self.module
            if module:
                module_name = self.module.__name__
            else:
                module_name = self.module_name
            self._name = module_name
        return self._name

    @property
    def filename(self):
        if not self._filename:
            if self.step_definitions:
                filename = inspect.getfile(self.step_definitions[0].func)
                self._filename = os.path.relpath(filename)
            return self._filename

    @property
    def module(self):
        if self.step_definitions:
            return inspect.getmodule(self.step_definitions[0].func)
        return sys.modules.get(self.module_name)

    @property
    def module_doc(self):
        module = self.module
        if module:
            return inspect.getdoc(module)

    def append(self, step_definition):
        self.step_definitions.append(step_definition)


class SphinxStepsDocumentGenerator(object):
    __doc__ = '\n    Provides document generator class that generates Sphinx-based\n    documentation for step definitions. The primary purpose is to:\n\n      * help the step-library provider/writer\n      * simplify self-documentation of step-libraries\n\n    EXAMPLE:\n        step_definitions = ...  # Collect from step_registry\n        doc_generator = SphinxStepsDocumentGenerator(step_definitions, "output")\n        doc_generator.write_docs()\n\n    .. seealso:: http://sphinx-doc.org/\n    '
    default_step_definition_doc = '.. todo::\n    Step definition description is missing.\n'
    shows_step_module_info = True
    shows_step_module_overview = True
    make_step_index_entries = True
    document_separator = '# -- DOCUMENT-END ' + '-' * 60
    step_document_prefix = 'step_module.'
    step_heading_prefix = '**Step:** '

    def __init__(self, step_definitions, destdir=None, stream=None):
        self.step_definitions = step_definitions
        self.destdir = destdir
        self.stream = stream
        self.document = None

    @property
    def stdout_mode(self):
        """
        Indicates that output towards stdout should be used.
        """
        return self.stream is not None

    @staticmethod
    def describe_step_definition(step_definition, step_type=None):
        if not step_type:
            step_type = step_definition.step_type or 'step'
        if step_type == 'step':
            step_type_text = 'Given/When/Then'
        else:
            step_type_text = step_type.capitalize()
        step_text = step_definition.string
        if '`' in step_text:
            step_text = step_text.replace('`', '\\`')
        return '%s %s' % (step_type_text, step_text)

    def ensure_destdir_exists(self):
        assert self.destdir
        if os.path.isfile(self.destdir):
            print('OOPS: remove %s' % self.destdir)
            os.remove(self.destdir)
        if not os.path.exists(self.destdir):
            os.makedirs(self.destdir)

    def ensure_document_is_closed(self):
        if self.document:
            if not self.stdout_mode:
                self.document.close()
                self.document = None

    def discover_step_modules(self):
        step_modules_map = {}
        for step_definition in self.step_definitions:
            assert step_definition.step_type is not None
            step_filename = step_definition.location.filename
            step_module = step_modules_map.get(step_filename, None)
            if not step_module:
                filename = inspect.getfile(step_definition.func)
                module_name = inspect.getmodulename(filename)
                assert module_name, 'step_definition: %s' % step_definition.location
                step_module = StepsModule(module_name)
                step_modules_map[step_filename] = step_module
            step_module.append(step_definition)

        step_modules = sorted(step_modules_map.values(), key=lambda x: x.name)
        for module in step_modules:
            step_definitions = sorted(module.step_definitions, key=lambda x: x.location)
            module.step_definitions = step_definitions

        return step_modules

    def create_document(self, filename):
        if not (filename.endswith('.rst') or filename.endswith('.txt')):
            filename += '.rst'
        if self.stdout_mode:
            stream = self.stream
            document = sphinx_util.DocumentWriter(stream, should_close=False)
        else:
            self.ensure_destdir_exists()
            filename = os.path.join(self.destdir, filename)
            document = sphinx_util.DocumentWriter.open(filename)
        return document

    def write_docs(self):
        step_modules = self.discover_step_modules()
        self.write_step_module_index(step_modules)
        for step_module in step_modules:
            self.write_step_module(step_module)

        return len(step_modules)

    def write_step_module_index(self, step_modules, filename='index.rst'):
        document = self.create_document(filename)
        document.write('.. _docid.steps:\n\n')
        document.write_heading('Step Definitions')
        document.write('The following step definitions are provided here.\n\n----\n\n')
        entries = sorted([self.step_document_prefix + module.name for module in step_modules])
        document.write_toctree(entries, maxdepth=1)
        document.close()
        if self.stdout_mode:
            sys.stdout.write('\n%s\n' % self.document_separator)

    def write_step_module(self, step_module):
        self.ensure_document_is_closed()
        document_name = self.step_document_prefix + step_module.name
        self.document = self.create_document(document_name)
        self.document.write('.. _docid.steps.%s:\n' % step_module.name)
        self.document.write_heading(step_module.name, index_id=step_module.name)
        if self.shows_step_module_info:
            self.document.write(':Module:   %s\n' % step_module.name)
            self.document.write(':Filename: %s\n' % step_module.filename)
            self.document.write('\n')
        if step_module.module_doc:
            module_doc = step_module.module_doc.strip()
            self.document.write('%s\n\n' % module_doc)
        if self.shows_step_module_overview:
            self.document.write_heading('Step Overview', level=1)
            self.write_step_module_overview(step_module.step_definitions)
        self.document.write_heading('Step Definitions', level=1)
        for step_definition in step_module.step_definitions:
            self.write_step_definition(step_definition)

        self.document.close()
        self.document = None
        if self.stdout_mode:
            sys.stdout.write('\n%s\n' % self.document_separator)

    def write_step_module_overview(self, step_definitions):
        assert self.document
        headings = ['Step Definition', 'Given', 'When', 'Then', 'Step']
        table = Table(headings)
        step_type_cols = {'given': [
                   '  x', '  ', '  ', '  '], 
         'when': [
                  '  ', '  x', '  ', '  '], 
         'then': [
                  '  ', '  ', '  x', '  '], 
         'step': [
                  '  x', '  x', '  x', '  x']}
        for step_definition in step_definitions:
            row = [self.describe_step_definition(step_definition)]
            row.extend(step_type_cols[step_definition.step_type])
            table.add_row(row)

        self.document.write_table(table)

    @staticmethod
    def make_step_definition_index_id(step_definition):
        if step_definition.step_type == 'step':
            index_kinds = ('Given', 'When', 'Then', 'Step')
        else:
            keyword = step_definition.step_type.capitalize()
            index_kinds = (keyword,)
        schema = 'single: %s%s; %s %s'
        index_parts = []
        for index_kind in index_kinds:
            keyword = index_kind
            word = ' step'
            if index_kind == 'Step':
                keyword = 'Given/When/Then'
                word = ''
            part = schema % (index_kind, word, keyword, step_definition.string)
            index_parts.append(part)

        joiner = '\n    '
        return joiner + joiner.join(index_parts)

    def make_step_definition_doc(self, step_definition):
        doc = inspect.getdoc(step_definition.func)
        if not doc:
            doc = self.default_step_definition_doc
        doc = doc.strip()
        return doc

    def write_step_definition(self, step_definition):
        assert self.document
        step_text = self.describe_step_definition(step_definition)
        if step_text.startswith('* '):
            step_text = step_text[2:]
        index_id = None
        if self.make_step_index_entries:
            index_id = self.make_step_definition_index_id(step_definition)
        heading = step_text
        if self.step_heading_prefix:
            heading = self.step_heading_prefix + step_text
        self.document.write_heading(heading, level=2, index_id=index_id)
        step_definition_doc = self.make_step_definition_doc(step_definition)
        self.document.write('%s\n' % step_definition_doc)
        self.document.write('\n')


class SphinxStepsFormatter(AbstractStepsFormatter):
    __doc__ = '\n    Provides formatter class that generates Sphinx-based documentation\n    for all registered step definitions. The primary purpose is to:\n\n      * help the step-library provider/writer\n      * simplify self-documentation of step-libraries\n\n    .. note::\n        Supports dry-run mode.\n        Supports destination directory mode to write multiple documents.\n    '
    name = 'sphinx.steps'
    description = 'Generate sphinx-based documentation for step definitions.'
    doc_generator_class = SphinxStepsDocumentGenerator

    def __init__(self, stream_opener, config):
        super(SphinxStepsFormatter, self).__init__(stream_opener, config)
        self.destdir = stream_opener.name

    @property
    def step_definitions(self):
        """
        Derive step definitions from step-registry.
        """
        steps = []
        for step_type, step_definitions in self.step_registry.steps.items():
            for step_definition in step_definitions:
                step_definition.step_type = step_type
                steps.append(step_definition)

        return steps

    def close(self):
        """Called at end of test run."""
        if not self.step_registry:
            self.discover_step_definitions()
        self.report()

    def create_document_generator(self):
        generator_class = self.doc_generator_class
        if self.stdout_mode:
            return generator_class(self.step_definitions, stream=self.stream)
        else:
            return generator_class(self.step_definitions, destdir=self.destdir)

    def report(self):
        document_generator = self.create_document_generator()
        document_counts = document_generator.write_docs()
        if not self.stdout_mode:
            msg = "%s: Written %s document(s) into directory '%s'.\n"
            sys.stdout.write(msg % (self.name, document_counts, self.destdir))