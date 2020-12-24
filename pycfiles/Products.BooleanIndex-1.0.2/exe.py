# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/plone-production-nbf-1/zeocluster/src/Products.BlobNewsItem/PasteScript-1.7.5-py2.6.egg/paste/script/exe.py
# Compiled at: 2012-02-27 07:41:53
import re, os, sys, shlex, pkg_resources, command

class ExeCommand(command.Command):
    parser = command.Command.standard_parser(verbose=False)
    summary = 'Run #! executable files'
    description = 'Use this at the top of files like:\n\n  #!/usr/bin/env /path/to/paster exe subcommand <command options>\n\nThe rest of the file will be used as a config file for the given\ncommand, if it wants a config file.\n\nYou can also include an [exe] section in the file, which looks\nlike:\n\n  [exe]\n  command = serve\n  log_file = /path/to/log\n  add = /path/to/other/config.ini\n\nWhich translates to:\n\n  paster serve --log-file=/path/to/log /path/to/other/config.ini\n'
    hidden = True
    _exe_section_re = re.compile('^\\s*\\[\\s*exe\\s*\\]\\s*$')
    _section_re = re.compile('^\\s*\\[')

    def run(self, argv):
        if argv and argv[0] in ('-h', '--help'):
            print self.description
            return
        if os.environ.get('REQUEST_METHOD'):
            sys.stdout = sys.stderr
            os.environ['PASTE_DEFAULT_QUIET'] = 'true'
        if '_' not in os.environ:
            print 'Warning: this command is intended to be run with a #! like:'
            print '  #!/usr/bin/env paster exe'
            print 'It only works with /usr/bin/env, and only as a #! line.'
            filename = argv[(-1)]
            args = argv[:-1]
            extra_args = []
        filename = os.environ['_']
        extra_args = argv[:]
        args = []
        while extra_args:
            if extra_args[0] == filename:
                extra_args.pop(0)
                break
            args.append(extra_args.pop(0))

        vars = {'here': os.path.dirname(filename), '__file__': filename}
        f = open(filename)
        lines = f.readlines()
        f.close()
        options = {}
        lineno = 1
        while lines:
            if self._exe_section_re.search(lines[0]):
                lines.pop(0)
                break
            lines.pop(0)
            lineno += 1

        pre_options = []
        options = args
        for line in lines:
            lineno += 1
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            if self._section_re.search(line):
                break
            if '=' not in line:
                raise command.BadCommand('Missing = in %s at %s: %r' % (
                 filename, lineno, line))
            (name, value) = line.split('=', 1)
            name = name.strip()
            value = value.strip()
            if name == 'require':
                pkg_resources.require(value)
            elif name == 'command' or name == 'add':
                options.extend(shlex.split(value))
            elif name == 'plugin':
                options[:0] = [
                 '--plugin', value]
            else:
                value = value % vars
                options.append('--%s=%s' % (name.replace('_', '-'), value))

        os.environ['PASTE_CONFIG_FILE'] = filename
        options.extend(extra_args)
        command.run(options)