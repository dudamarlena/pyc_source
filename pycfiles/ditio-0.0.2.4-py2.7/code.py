# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ditio/notebook/code.py
# Compiled at: 2018-01-30 12:44:26
import re
from .. import log, trace
from .. import utils
from ..utils import apply_commands, commands_update

def export(context, indexed_cells):
    context['file-handles'] = {}
    for index, cell in indexed_cells:
        if cell['cell_type'] != 'code':
            continue
        trace('(notebook-export) - pos=%s,type=%s' % (index, cell['cell_type']))
        commands = get_cell_commands(cell)
        cell = apply_commands(context, code_cell_executor, commands, cell)
        trace('(notebook-export) - commands: %s  ' % str(commands))

    for k in context['file-handles']:
        f_handle = context['file-handles'][k]
        f_handle.close()

    trace('(notebook-code-export): properties=%s ' % str(context['properties']))


def code_cell_executor(context, cell, command, params):
    properties = context['properties']
    trace('(execute):  cmd=%s,params=%s' % (command, params))
    if command == 'FILE':
        if params not in context['file-handles']:
            if params == '__init__.py':
                file_name = '%s/%s' % (context['package-folder'], params)
            else:
                file_name = '%s/%s' % (context['project-folder'], params)
            context['file-handles'][params] = open(file_name, 'w')
            context['file-handles'][params].write(('\n').join([ l.strip() for l in cell['source'] ]))
    else:
        log('(directives-code): Unknown Command: %s, %s ' % (command, params))


def get_cell_commands(cell):
    directive_matcher = re.compile('^#([A-Z]+)\\:')
    directives = [
     ('FILE', '__init__.py')]
    for l in cell['source']:
        matches = directive_matcher.findall(l)
        if matches == []:
            break
        directive = matches[0]
        params = l.split(':', 1)[1].strip()
        if params == '':
            params = str(True)
        if directive == 'DIST':
            directive = 'FILE'
            params = 'setup.py'
        commands_update(directives, directive, params)

    return directives