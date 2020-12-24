# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/jqb/projects/boilerplate/boilerplate/cmdline.py
# Compiled at: 2018-08-06 09:41:19
from __future__ import unicode_literals
import sys, optparse, os, os.path as ospath
from . import template, conf, filematchers, VERSION

def handle(argv):
    handler = Handler()
    return handler.handle(argv)


class HandlerException(Exception):
    pass


completion = dict(bash=b'\n# boilerplate bash completion start\n_boilerplate_completion()\n{\n    COMPREPLY=( $( COMP_WORDS="${COMP_WORDS[*]}"                    COMP_CWORD=$COMP_CWORD                    BOILERPLATE_AUTO_COMPLETE=1 $1 ) )\n}\ncomplete -o default -F _boilerplate_completion boil\n# boilerplate bash completion end\n')

class OptionParser(optparse.OptionParser):

    def get_matches(self, comp_word):
        """
        Returns list of options that mathes given ``comp_word``
        """
        result = []
        for opt in self.option_list:
            for opt_str in opt._short_opts + opt._long_opts:
                if opt_str.startswith(comp_word):
                    result.append(opt_str)

        return result


class Handler(object):
    completion = completion

    def __init__(self, stdout=sys.stdout, stderr=sys.stderr):
        self.stdout = stdout
        self.stderr = stderr

    def parse_cmdline(self, argv):
        parser = OptionParser(usage=b'usage: %prog <template-name> <project-name>', description=b'Project structure generation tool')
        parser.add_option(b'-l', b'--list', action=b'store_true', dest=b'list', default=False)
        parser.add_option(b'-v', b'--version', action=b'store_true', dest=b'version', default=False)
        parser.add_option(b'--bash-completion', action=b'store_true', dest=b'bash_completion', default=False)
        return parser

    def get_templates_places(self):
        return conf.templates_places()

    def is_template(self, dirpath):
        return all([
         ospath.isdir(dirpath),
         not filematchers.git_directory.match(dirpath),
         not filematchers.svn_directory.match(dirpath)])

    def get_templates_list(self):
        result = template.TemplateList()
        for tmpl_place in self.get_templates_places():
            if not ospath.exists(tmpl_place):
                if not self.completion_request():
                    self.stdout.write(b'WARNING Directory: %s, does not exists, omitting.\n' % tmpl_place)
                continue
            for dirname in os.listdir(tmpl_place):
                dirpath = ospath.join(tmpl_place, dirname)
                if self.is_template(dirpath):
                    result.append(template.Template(place=tmpl_place, name=dirname))

        return result

    def completion_request(self):
        return os.environ.get(b'BOILERPLATE_AUTO_COMPLETE') == b'1'

    def can_do_completion(self):
        return len(self.get_complete_words()) <= 1

    def get_complete_words(self):
        return os.environ.get(b'COMP_WORDS', b'').split(b' ')[1:]

    def concat(self, words, delimiter=b' '):
        return delimiter.join(words)

    def handle_completion(self, parser):
        if self.can_do_completion():
            first = self.get_complete_words()[0]
            self.stdout.write(self.concat([ t.name for t in self.get_templates_list() if t.name.startswith(first)
                                          ]))
            if first.startswith(b'-'):
                self.stdout.write(self.concat(parser.get_matches(first)))
            self.stdout.write(b'')

    def handle(self, argv):
        parser = self.parse_cmdline(argv)
        options, args = parser.parse_args(argv)
        templates_list = self.get_templates_list()
        if self.completion_request():
            self.handle_completion(parser)
            return 0
        if options.version:
            self.stdout.write(b'%s\n' % VERSION)
            return 0
        if options.list:
            for tmpl in templates_list:
                self.stdout.write(b'%s\n' % tmpl.name)

            return 0
        if options.bash_completion:
            self.stdout.write(self.completion[b'bash'])
            return 0
        if len(args) == 0:
            self.stderr.write(b"There's no enough arguments. Exact two args should be passed.\n")
            parser.print_usage(file=self.stderr)
            return 1
        template_name = args[0]
        if len(args) == 1:
            self.stderr.write(b'Please add project name\n')
            parser.print_usage(file=self.stderr)
            return 1
        if not templates_list.has_item_with(name=template_name):
            self.stderr.write(b"No such template: '%s'\n" % template_name)
            self.stderr.write(b'Following places has been searched:\n')
            for tmpl_dir in self.get_templates_places():
                self.stderr.write(b'   %s\n' % tmpl_dir)

            return 1
        template = templates_list.get_item_with(name=template_name)
        project_name = args[1]
        if not template.exists():
            self.stderr.write(b'No such template directory: %s\n' % template.get_full_path())
            return 2
        destination_path = ospath.join(os.getcwd())
        template.create(destination_path, project_name)
        return 0