# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ana/dev/dexy-clean/dexy/filters/ipynb.py
# Compiled at: 2020-03-18 15:12:33
# Size of source mod 2**32: 7730 bytes
from dexy.filter import DexyFilter
import base64, dexy.exceptions, json, urllib
try:
    import IPython.nbformat.current
    AVAILABLE = True
except ImportError:
    AVAILABLE = False

class IPythonBase(DexyFilter):
    __doc__ = '\n    Base class for IPython filters which work by loading notebooks into memory.\n    '
    aliases = []

    def is_active(self):
        return AVAILABLE

    def load_notebook(self):
        nb = None
        with open(self.input_data.storage.data_file(), 'r') as (f):
            nb_fmt = self.input_data.ext.replace('.', '')
            nb = IPython.nbformat.current.read(f, nb_fmt)
        return nb

    def enumerate_cells(self, nb=None):
        if not nb:
            nb = self.load_notebook()
        worksheet = nb['worksheets'][0]
        for j, cell in enumerate(worksheet['cells']):
            yield (
             j, cell)


class IPythonExport(IPythonBase):
    __doc__ = '\n    Generates a static file based on an IPython notebook.\n    '
    aliases = ['ipynbx']
    _settings = {'added-in-version':'0.9.9.6', 
     'input-extensions':[
      '.ipynb'], 
     'output':True, 
     'output-extensions':[
      '.md', '.html']}

    def process_html(self):
        nb = self.load_notebook()

    def process_md(self):
        output = ''
        for j, cell in self.enumerate_cells():
            cell_type = cell['cell_type']
            if cell_type == 'heading':
                output += '## %s\n' % cell['source']
            elif cell_type == 'markdown':
                output += '\n%s\n' % cell['source']
            elif cell_type == 'code':
                for k, cell_output in enumerate(cell['outputs']):
                    cell_output_type = cell_output['output_type']
                    del cell_output['output_type']
                    if cell_output_type == 'stream':
                        output += cell_output['text']
                    else:
                        if cell_output_type in ('pyout', 'pyerr'):
                            continue
                        if cell_output_type == 'display_data':
                            for fmt, contents in cell_output.items():
                                if fmt == 'png':
                                    cell_output_image_file = 'cell-%s-output-%s.%s' % (j, k, fmt)
                                    d = self.add_doc(cell_output_image_file, base64.decodestring(contents))
                                    output += '\n![Description](%s)\n' % urllib.quote(cell_output_image_file)
                                else:
                                    if fmt in ('metadata', 'text'):
                                        continue
                                    raise dexy.exceptions.InternalDexyProblem(fmt)

                        else:
                            raise dexy.exceptions.InternalDexyProblem('unexpected cell output type %s' % cell_output_type)

            else:
                raise dexy.exceptions.InternalDexyProblem('Unexpected cell type %s' % cell_type)

        return output

    def process(self):
        if self.ext == '.html':
            output = self.process_html()
        else:
            if self.ext == '.md':
                output = self.process_md()
            else:
                raise dexy.exceptions.InternalDexyProblem("Shouldn't get ext %s" % self.ext)
        self.output_data.set_data(output)


class IPythonNotebook(IPythonBase):
    __doc__ = '\n    Get data out of an IPython notebook.\n    '
    aliases = ['ipynb']
    _settings = {'added-in-version':'0.9.9.6', 
     'examples':[
      'ipynb'], 
     'input-extensions':[
      '.ipynb', '.json', '.py'], 
     'output-extensions':[
      '.json']}

    def process(self):
        output = {}
        nb = self.load_notebook()
        nb_fmt_string = '%s.%s' % (nb['nbformat'], nb['nbformat_minor'])
        output['nbformat'] = nb_fmt_string
        cells = []
        documents = []
        for j, cell in self.enumerate_cells(nb):
            cell_key = '%s--%s' % (self.input_data.rootname(), j)
            cell_type = cell['cell_type']
            if cell_type == 'heading':
                pass
            elif cell_type == 'markdown':
                d = self.add_doc('%s.md' % cell_key, cell['source'], {'output': False})
                documents.append(d.key)
                d = self.add_doc('%s.md|pyg|h' % cell_key, cell['source'])
                d = self.add_doc('%s.md|pyg|l' % cell_key, cell['source'])
            else:
                if cell_type == 'code':
                    file_extensions = {'python': '.py'}
                    ext = file_extensions[cell['language']]
                    d = self.add_doc('%s-input%s' % (cell_key, ext), cell['input'], {'output': False})
                    documents.append(d.key)
                    self.add_doc('%s-input%s|pyg|h' % (cell_key, ext), cell['input'], {'output': False})
                    self.add_doc('%s-input%s|pyg|l' % (cell_key, ext), cell['input'], {'output': False})
                    for k, cell_output in enumerate(cell['outputs']):
                        cell_output_type = cell_output['output_type']
                        del cell_output['output_type']
                        if cell_output_type == 'stream':
                            assert sorted(cell_output.keys()) == ['stream', 'text'], 'stream output keys'
                            d = self.add_doc('%s-output-%s.txt' % (cell_key, k), cell_output['text'], {'output': False})
                            documents.append(d.key)
                        else:
                            if cell_output_type == 'pyout':
                                continue
                            if cell_output_type == 'pyerr':
                                continue
                            if cell_output_type == 'display_data':
                                for fmt, contents in cell_output.items():
                                    if fmt == 'png':
                                        d = self.add_doc('%s-output-%s.%s' % (cell_key, k, fmt), base64.decodestring(contents))
                                        documents.append(d.key)
                                        cell.outputs[k]['png'] = d.key
                                    else:
                                        if fmt == 'text':
                                            continue
                                        if fmt == 'metadata':
                                            continue
                                        if fmt == 'latex':
                                            continue
                                        raise Exception('unexpected format in display_data %s' % fmt)

                            else:
                                raise Exception('unexpected output type %s' % cell_output_type)

                else:
                    raise Exception("unexpected cell type '%s'" % cell_type)
            cells.append((cell_type, cell))

        output['nbformat'] = nb_fmt_string
        output['cells'] = cells
        output['documents'] = documents
        for k, v in nb['metadata'].items():
            output[k] = v

        self.output_data.set_data(json.dumps(output))