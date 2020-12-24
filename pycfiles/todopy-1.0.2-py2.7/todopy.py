# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\todopy\todopy.py
# Compiled at: 2011-12-15 09:18:19
import os.path
from model import Model
from reader import FileReader
from writer import FileWriter
from formatter import ConsoleFormatter
from filter import StringFilter
from munger import ContextRemover
from munger import ProjectRemover
from options import Options

def main():
    o = Options('todo.txt manager', config_file='~/.todopy.ini')
    o.add_flag('color', help='Turn on colored output')
    o.add_option('todofile', help='Todo file path')
    o.add_option('tododir', help='Directory for all todo.py data', default=os.path.expanduser('~'))
    o.add_subcommand('add', help='Add a todo')
    o.add_argument('todo', dest='todos', group='add', count='+')
    o.add_subcommand('ls', help='List todos')
    o.add_argument('word', dest='words', group='ls', count='*', help='List only todos containing these words')
    o.add_flag('contexts', group='ls', default=True, help="Don't show @contexts when listing todos")
    o.add_flag('projects', group='ls', default=True, help="Don't show +projects when listing todos")
    o.add_subcommand('lsc', help='List contexts')
    o.add_subcommand('lsp', help='List projects')
    o.add_subcommand('do', help='Mark todo as done')
    o.add_argument('id', dest='ids', count='+', type=int, help='IDs of todos to mark as done', group='do')
    o.add_subcommand('undo', help='Mark todo as undone')
    o.add_argument('id', dest='ids', count='+', type=int, help='IDs of todos to mark as undone', group='undo')
    o.add_subcommand('app', help='Append text to todo')
    o.add_argument('id', help='ID if todo to append text to', type=int, group='app')
    o.add_argument('text', help='Text to append', group='app')
    o.add_subcommand('pre', help='Prepend text to todo')
    o.add_argument('id', help='ID if todo to prepend text to', type=int, group='pre')
    o.add_argument('text', help='Text to prepend', group='pre')
    o.add_subcommand('pri', help='Give priority to todo item')
    o.add_argument('id', type=int, help='ID of todo item to prioritize', group='pri')
    o.add_argument('priority', help='New priority for todo item', group='pri')
    o.add_subcommand('dp', help='Remove priority from todo item')
    o.add_argument('id', dest='ids', count='+', type=int, group='dp', help='IDs of todo items to deprioritize')
    o.parse(config_file=os.path.expanduser('~/.todopy.ini'))
    if o.main.todofile:
        model = Model.from_store(FileReader(o.main.todofile))
    else:
        model = Model.from_store(FileReader(os.path.join(o.main.tododir, 'todo.txt')))
    if o.command == 'ls':
        for word in o.ls.words:
            model = StringFilter(word, model)

        if not o.ls.contexts:
            model = ContextRemover(model)
        if not o.ls.projects:
            model = ProjectRemover(model)
        print ConsoleFormatter(o.main.color).format(model)
    elif o.command == 'add':
        for todo in o.add.todos:
            model.add(todo)

        FileWriter(o.main.todofile).write(model)
    elif o.command == 'do':
        for id in o.do.ids:
            model.set_done(id)

        FileWriter(o.main.todofile).write(model)
    elif o.command == 'undo':
        for id in o.undo.ids:
            model.set_done(id, False)

        FileWriter(o.main.todofile).write(model)
    elif o.command == 'app':
        model.append(o.app.id, o.app.text)
        FileWriter(o.main.todofile).write(model)
    elif o.command == 'pre':
        model.prepend(o.pre.id, o.pre.text)
        FileWriter(o.main.todofile).write(model)
    elif o.command == 'pri':
        model.set_priority(o.pri.id, o.pri.priority)
        FileWriter(o.main.todofile).write(model)
    elif o.command == 'dp':
        for id in o.dp.ids:
            model.set_priority(id, None)

        FileWriter(o.main.todofile).write(model)
    return


if __name__ == '__main__':
    main()