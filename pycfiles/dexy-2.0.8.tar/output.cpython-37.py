# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ana/dev/dexy-clean/dexy/reporters/output.py
# Compiled at: 2020-03-18 15:12:33
# Size of source mod 2**32: 2425 bytes
from dexy.reporter import Reporter
import os

class Output(Reporter):
    __doc__ = '\n    Creates canonical dexy output with files given short filenames.\n    '
    aliases = ['output']
    _settings = {'dir': 'output'}

    def write_canonical_data(self, doc):
        output_name = doc.output_data().output_name()
        if output_name:
            fp = os.path.join(self.setting('dir'), output_name)
            if fp in self.locations:
                self.log_warn('WARNING overwriting file %s' % fp)
            else:
                self.locations[fp] = []
            self.locations[fp].append(doc.key)
            parent_dir = os.path.dirname(fp)
            try:
                os.makedirs(parent_dir)
            except os.error:
                pass

            self.log_debug('  writing %s to %s' % (doc.key, fp))
            doc.output_data().output_to_file(fp)

    def run(self, wrapper):
        self.wrapper = wrapper
        self.locations = {}
        self.remove_reports_dir((self.wrapper), keep_empty_dir=True)
        self.create_reports_dir()
        for doc in list(wrapper.nodes.values()):
            if doc.key_with_class() not in wrapper.batch.docs:
                continue
            if doc.state not in ('ran', 'consolidated'):
                continue
            if not hasattr(doc, 'output_data'):
                continue
            if doc.output_data().is_canonical_output():
                self.write_canonical_data(doc)


class LongOutput(Reporter):
    __doc__ = '\n    Creates complete dexy output with files given long, unique filenames.\n    '
    aliases = ['long']
    _settings = {'default':False, 
     'dir':'output-long'}

    def run(self, wrapper):
        self.wrapper = wrapper
        self.create_reports_dir()
        for doc in list(wrapper.nodes.values()):
            if doc.key_with_class() not in wrapper.batch.docs:
                continue
            elif doc.state not in ('ran', 'consolidated'):
                continue
            else:
                if not hasattr(doc, 'output_data'):
                    continue
                fp = os.path.join(self.setting('dir'), doc.output_data().long_name())
                try:
                    os.makedirs(os.path.dirname(fp))
                except os.error:
                    pass

            self.log_debug('  writing %s to %s' % (doc.key, fp))
            doc.output_data().output_to_file(fp)