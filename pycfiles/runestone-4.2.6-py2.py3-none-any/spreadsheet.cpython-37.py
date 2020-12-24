# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /srv/RunestoneComponents/runestone/spreadsheet/spreadsheet.py
# Compiled at: 2020-04-16 12:40:55
# Size of source mod 2**32: 7231 bytes
__author__ = 'bmiller'
import csv, io, os, re, urllib.parse
from docutils import nodes
from docutils.parsers.rst import directives
from runestone.common.runestonedirective import RunestoneNode, RunestoneIdDirective, get_node_line
from runestone.server.componentdb import addQuestionToDB, addHTMLToDB

def setup(app):
    app.add_directive('spreadsheet', SpreadSheet)
    app.add_node(SpreadSheetNode, html=(visit_ss_node, depart_ss_node))


class SpreadSheetNode(nodes.General, nodes.Element, RunestoneNode):

    def __init__(self, content, **kwargs):
        (super(SpreadSheetNode, self).__init__)(**kwargs)
        self.ss_options = content


class SpreadSheet(RunestoneIdDirective):
    __doc__ = '\n    .. spreadsheet:: uniqueid\n        :fromcsv: path/to/csv/file\n        :colwidths: list of column widths\n        :coltitles: list of column names\n        :mindimensions: mincols, minrows  -- minDimensions:[10,5]\n\n        A1,B1,C1,D1...\n        A2,B2,C2,D2...\n    '
    required_arguments = 1
    optional_arguments = 5
    has_content = True
    option_spec = RunestoneIdDirective.option_spec.copy()
    option_spec.update({'fromcsv':directives.unchanged, 
     'colwidths':directives.unchanged, 
     'coltitles':directives.unchanged, 
     'mindimensions':directives.unchanged})

    def run(self):
        super(SpreadSheet, self).run()
        env = self.state.document.settings.env
        self.options['divid'] = self.arguments[0].strip()
        if '====' in self.content:
            idx = self.content.index('====')
            suffix = self.content[idx + 1:]
            self.options['asserts'] = suffix
            self.options['autograde'] = 'data-autograde="true"'
        else:
            self.options['asserts'] = '""'
            self.options['autograde'] = ''
        if 'fromcsv' in self.options:
            self.content = self.body_from_csv(env, self.options['fromcsv'])
        else:
            if self.content:
                self.content = self.body_to_csv(self.content)
            else:
                raise ValueError('You must specify either from csv or provide content in the body')
        self.options['data'] = self.content
        if 'coltitles' not in self.options:
            self.options['coltitles'] = ''
        else:
            self.options['coltitles'] = 'data-coltitles=[{}]'.format(','.join([urllib.parse.quote((x.strip()), safe='\'"') for x in self.options['coltitles'].split(',')]))
        if 'mindimensions' not in self.options:
            self.options['mindimensions'] = ''
        else:
            self.options['mindimensions'] = 'data-mindimensions=[{}]'.format(','.join([x.strip() for x in self.options['mindimensions'].split(',')]))
        if 'colwidths' not in self.options:
            self.options['colwidths'] = ''
        else:
            self.options['colwidths'] = 'data-colwidths=[{}]'.format(','.join([x.strip() for x in self.options['colwidths'].split(',')]))
        ssnode = SpreadSheetNode((self.options), rawsource=(self.block_text))
        ssnode.source, ssnode.line = self.state_machine.get_source_and_line(self.lineno)
        self.add_name(ssnode)
        return [
         ssnode]

    def body_to_csv(self, row_list):
        """
        Use the csv reader and writer functionality to better parse the body.

        1. Convert the contents to a StringIO object
        2. Then read and process using a csv reader
        3. Formulas with ,'s in them should be in double quotes, if there are "'s in the
           cell then they should be ""-ed
        """
        csvlist = []
        body_list = []
        for row in row_list:
            if re.match('^\\s*====', row):
                break
            body_list.append(row)

        body_file = io.StringIO('\n'.join(body_list))
        body_reader = csv.reader(body_file)
        for row in body_reader:
            ilist = []
            for item in row:
                item = item.strip()
                if item:
                    if item[0] == '"':
                        if item[(-1)] == '"':
                            item = item[1:-1]
                if is_float(item):
                    ilist.append(as_int_or_float(item))
                elif item.startswith('='):
                    ilist.append('{}'.format(item.upper()))
                else:
                    ilist.append('{}'.format(item))

            csvlist.append(ilist)

        return csvlist

    def body_from_csv(self, env, csvfile):
        ffpath = os.path.dirname(self.srcpath)
        print(self.srcpath, os.getcwd())
        filename = os.path.join(env.srcdir, ffpath, csvfile)
        print('\n\nPATH=', self.srcpath)
        with open(filename, 'r') as (csv):
            content = csv.readlines()
        content = [line[:-1] for line in content]
        return self.body_to_csv(content)


def is_float(s):
    try:
        x = float(s)
        return True
    except:
        return False


def as_int_or_float(s):
    try:
        x = int(s)
        return x
    except:
        x = float(s)
        return x


TEMPLATE = '\n<div id="{divid}" data-component="spreadsheet" class="runestone" {autograde} {mindimensions} {colwidths} {coltitles}>\n    <div id="{divid}_sheet"></div>\n\n    <script>\n        {divid}_data = {data};\n        {divid}_asserts = {asserts};\n    </script>\n</div>\n'

def visit_ss_node(self, node):
    res = (TEMPLATE.format)(**node.ss_options)
    self.body.append(res)


def depart_ss_node(self, node):
    pass