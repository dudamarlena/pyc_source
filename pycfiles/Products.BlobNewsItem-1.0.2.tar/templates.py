# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/plone-production-nbf-1/zeocluster/src/Products.BlobNewsItem/PasteScript-1.7.5-py2.6.egg/paste/script/templates.py
# Compiled at: 2012-02-27 07:41:53
import sys, os, inspect, copydir, command
from paste.util.template import paste_script_template_renderer

class Template(object):
    vars = []
    egg_plugins = []
    required_templates = []
    use_cheetah = False
    read_vars_from_templates = False
    template_renderer = None

    def __init__(self, name):
        self.name = name
        self._read_vars = None
        return

    def module_dir(self):
        """Returns the module directory of this template."""
        mod = sys.modules[self.__class__.__module__]
        return os.path.dirname(mod.__file__)

    def template_dir(self):
        assert self._template_dir is not None, "Template %r didn't set _template_dir" % self
        if isinstance(self._template_dir, tuple):
            return self._template_dir
        else:
            return os.path.join(self.module_dir(), self._template_dir)
            return

    def run(self, command, output_dir, vars):
        self.pre(command, output_dir, vars)
        self.write_files(command, output_dir, vars)
        self.post(command, output_dir, vars)

    def check_vars(self, vars, cmd):
        expect_vars = self.read_vars(cmd)
        if not expect_vars:
            return vars
        converted_vars = {}
        unused_vars = vars.copy()
        errors = []
        for var in expect_vars:
            if var.name not in unused_vars:
                if cmd.interactive:
                    prompt = 'Enter %s' % var.full_description()
                    response = cmd.challenge(prompt, var.default, var.should_echo)
                    converted_vars[var.name] = response
                elif var.default is command.NoDefault:
                    errors.append('Required variable missing: %s' % var.full_description())
                else:
                    converted_vars[var.name] = var.default
            else:
                converted_vars[var.name] = unused_vars.pop(var.name)

        if errors:
            raise command.BadCommand('Errors in variables:\n%s' % ('\n').join(errors))
        converted_vars.update(unused_vars)
        vars.update(converted_vars)
        return converted_vars

    def read_vars(self, command=None):
        if self._read_vars is not None:
            return self._read_vars
        else:
            assert not self.read_vars_from_templates or self.use_cheetah, 'You can only read variables from templates if using Cheetah'
            if not self.read_vars_from_templates:
                self._read_vars = self.vars
                return self.vars
            vars = self.vars[:]
            var_names = [ var.name for var in self.vars ]
            read_vars = find_args_in_dir(self.template_dir(), verbose=command and command.verbose > 1).items()
            read_vars.sort()
            for (var_name, var) in read_vars:
                if var_name not in var_names:
                    vars.append(var)

            self._read_vars = vars
            return vars

    def write_files(self, command, output_dir, vars):
        template_dir = self.template_dir()
        if not os.path.exists(output_dir):
            print 'Creating directory %s' % output_dir
            if not command.simulate:
                os.makedirs(output_dir)
        copydir.copy_dir(template_dir, output_dir, vars, verbosity=command.verbose, simulate=command.options.simulate, interactive=command.interactive, overwrite=command.options.overwrite, indent=1, use_cheetah=self.use_cheetah, template_renderer=self.template_renderer)

    def print_vars(self, indent=0):
        vars = self.read_vars()
        var.print_vars(vars)

    def pre(self, command, output_dir, vars):
        """
        Called before template is applied.
        """
        pass

    def post(self, command, output_dir, vars):
        """
        Called after template is applied.
        """
        pass


NoDefault = command.NoDefault

class var(object):

    def __init__(self, name, description, default='', should_echo=True):
        self.name = name
        self.description = description
        self.default = default
        self.should_echo = should_echo

    def __repr__(self):
        return '<%s %s default=%r should_echo=%s>' % (
         self.__class__.__name__,
         self.name, self.default, self.should_echo)

    def full_description(self):
        if self.description:
            return '%s (%s)' % (self.name, self.description)
        else:
            return self.name

    def print_vars(cls, vars, indent=0):
        max_name = max([ len(v.name) for v in vars ])
        for var in vars:
            if var.description:
                print '%s%s%s  %s' % (
                 ' ' * indent,
                 var.name,
                 ' ' * (max_name - len(var.name)),
                 var.description)
            else:
                print '  %s' % var.name
            if var.default is not command.NoDefault:
                print '      default: %r' % var.default
            if var.should_echo is True:
                print '      should_echo: %s' % var.should_echo

        print

    print_vars = classmethod(print_vars)


class BasicPackage(Template):
    _template_dir = 'paster-templates/basic_package'
    summary = 'A basic setuptools-enabled package'
    vars = [
     var('version', 'Version (like 0.1)'),
     var('description', 'One-line description of the package'),
     var('long_description', 'Multi-line description (in reST)'),
     var('keywords', 'Space-separated keywords/tags'),
     var('author', 'Author name'),
     var('author_email', 'Author email'),
     var('url', 'URL of homepage'),
     var('license_name', 'License name'),
     var('zip_safe', 'True/False: if the package can be distributed as a .zip file', default=False)]
    template_renderer = staticmethod(paste_script_template_renderer)


_skip_variables = [
 'VFN', 'currentTime', 'self', 'VFFSL', 'dummyTrans',
 'getmtime', 'trans']

def find_args_in_template(template):
    if isinstance(template, (str, unicode)):
        import Cheetah.Template
        template = Cheetah.Template.Template(file=template)
    if not hasattr(template, 'body'):
        return
    else:
        method = template.body
        (args, varargs, varkw, defaults) = inspect.getargspec(method)
        defaults = list(defaults or [])
        vars = []
        while args:
            if len(args) == len(defaults):
                default = defaults.pop(0)
            else:
                default = command.NoDefault
            arg = args.pop(0)
            if arg in _skip_variables:
                continue
            vars.append(var(arg, description=None, default=default))

        return vars


def find_args_in_dir(dir, verbose=False):
    all_vars = {}
    for fn in os.listdir(dir):
        if fn.startswith('.') or fn == 'CVS' or fn == '_darcs':
            continue
        full = os.path.join(dir, fn)
        if os.path.isdir(full):
            inner_vars = find_args_in_dir(full)
        elif full.endswith('_tmpl'):
            inner_vars = {}
            found = find_args_in_template(full)
            if found is None:
                if verbose:
                    print 'Template %s has no parseable variables' % full
                continue
            for var in found:
                inner_vars[var.name] = var

        else:
            continue
        if verbose:
            print 'Found variable(s) %s in Template %s' % (
             (', ').join(inner_vars.keys()), full)
        for (var_name, var) in inner_vars.items():
            if var_name not in all_vars:
                all_vars[var_name] = var
                continue
            cur_var = all_vars[var_name]
            if not cur_var.description:
                cur_var.description = var.description
            elif cur_var.description and var.description and var.description != cur_var.description:
                print >> sys.stderr, 'Variable descriptions do not match: %s: %s and %s' % (
                 var_name, cur_var.description, var.description)
            if cur_var.default is not command.NoDefault and var.default is not command.NoDefault and cur_var.default != var.default:
                print >> sys.stderr, 'Variable defaults do not match: %s: %r and %r' % (
                 var_name, cur_var.default, var.default)

    return all_vars