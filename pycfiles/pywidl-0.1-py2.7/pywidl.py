# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/pywidl/pywidl.py
# Compiled at: 2012-03-31 09:53:42
from grammar import parse
from mako.template import Template
import sys
name = 'pywidl'
version = '0.1'

def printUsage():
    print 'USAGE: pywidl <options> source [-- <userargs>]\n\n  Options:\n    -v, --version\n    -n, --native\n    -m, --mako\n    -o, --output=FILE\n    -t, --template=FILE\n\n  User arguments:\n    --foo\n    --foo=bar\n'


def printVersion():
    print '%s %s' % (name, version)


class App(object):
    NATIVE_TEMPLATE = 0
    MAKO_TEMPLATE = 1

    def __init__(self, source, output, template, template_type=NATIVE_TEMPLATE, user_args=None):
        if user_args is None:
            user_args = {}
        self._source = source
        self._output = output
        self._template = template
        self._template_type = template_type
        self._user_args = user_args
        return

    def _parse(self):
        with open(self._source, 'r') as (f):
            return parse(f.read())

    def _emitNative(self, definitions):
        exec 'import %s as template' % self._template
        template.render(definitions=definitions, source=self._source, output=self._output, template=self._template, template_type=self._template_type, **self._user_args)

    def _emitMako(self, definitions):
        template = Template(filename=self._template)
        with open(self._output, 'w') as (f):
            f.write(template.render(definitions=definitions, source=self._source, output=self._output, template=self._template, template_type=self._template_type, **self._user_args))

    def _emit(self, definitions):
        if self._template_type == self.NATIVE_TEMPLATE:
            self._emitNative(definitions)
        elif self._template_type == self.MAKO_TEMPLATE:
            self._emitMako(definitions)
        else:
            raise ValueError('Unknown template type: %d' % self._template_type)

    def run(self):
        definitions = self._parse()
        self._emit(definitions)


def options(argv):
    args = {}
    for i in range(1, len(argv)):
        arg = argv[i]
        if arg == '--':
            break
        elif arg == '--version' or arg == '-v':
            key = 'version'
            value = None
        elif arg == '--mako' or arg == '-m':
            key = 'template_type'
            value = App.MAKO_TEMPLATE
        elif arg == '--native' or arg == '-n':
            key = 'template_type'
            value = App.NATIVE_TEMPLATE
        elif arg.startswith('--output='):
            key = 'output'
            value = arg.split('=', 1)[1]
        elif arg == '-o' and i < len(argv) - 1:
            i += 1
            key = 'output'
            value = argv[i]
        elif arg.startswith('--template='):
            key = 'template'
            value = arg.split('=', 1)[1]
        elif arg == '-t' and i < len(argv) - 1:
            i += 1
            key = 'template'
            value = argv[i]
        else:
            key = 'source'
            value = arg
        args[key] = value

    return args


def userArgs(argv):
    args = {}
    user_flag = False
    for i in range(1, len(argv)):
        arg = argv[i]
        if not user_flag and arg == '--':
            user_flag = True
            continue
        if not user_flag:
            continue
        if arg.startswith('--'):
            arg = arg[2:]
            keyvalue = arg.split('=', 1)
            if len(keyvalue) == 2:
                key, value = keyvalue
            else:
                key = keyvalue[0]
                value = None
            args[key] = value

    return args


def main():
    app_args = options(sys.argv)
    user_args = userArgs(sys.argv)
    if 'version' in app_args:
        printVersion()
        return
    else:
        source = app_args.get('source', None)
        output = app_args.get('output', None)
        template = app_args.get('template', None)
        template_type = app_args.get('template_type', App.NATIVE_TEMPLATE)
        if source is None or output is None or template is None or template_type is None:
            printUsage()
            exit(1)
        app = App(source, output, template, template_type, user_args)
        return app.run()


if __name__ == '__main__':
    main()