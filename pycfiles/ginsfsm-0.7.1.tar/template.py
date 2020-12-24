# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/gines/midesarrollo/hg-projects/ginsfsm/ginsfsm/scaffolds/template.py
# Compiled at: 2012-07-11 15:59:09
import re, sys, os
from ginsfsm.compat import native_, bytes_
from ginsfsm.scaffolds import copydir
fsenc = sys.getfilesystemencoding()

class Template(object):
    """ Inherit from this base class and override methods to use the Pyramid
    scaffolding system."""
    copydir = copydir
    _template_dir = None

    def __init__(self, name):
        self.name = name

    def render_template(self, content, vars, filename=None):
        """ Return a bytestring representing a templated file based on the
        input (content) and the variable names defined (vars).  ``filename``
        is used for exception reporting."""
        content = native_(content, fsenc)
        try:
            return bytes_(substitute_double_braces(content, TypeMapper(vars)), fsenc)
        except Exception as e:
            _add_except(e, ' in file %s' % filename)
            raise

    def module_dir(self):
        mod = sys.modules[self.__class__.__module__]
        return os.path.dirname(mod.__file__)

    def template_dir(self):
        """ Return the template directory of the scaffold.  By default, it
        returns the value of ``os.path.join(self.module_dir(),
        self._template_dir)`` (``self.module_dir()`` returns the module in
        which your subclass has been defined).  If ``self._template_dir`` is
        a tuple this method just returns the value instead of trying to
        construct a path.  If _template_dir is a tuple, it should be a
        2-element tuple: ``(package_name, package_relative_path)``."""
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

    def write_files(self, command, output_dir, vars):
        template_dir = self.template_dir()
        if not self.exists(output_dir):
            self.out('Creating directory %s' % output_dir)
            if not command.options.simulate:
                self.makedirs(output_dir)
        self.copydir.copy_dir(template_dir, output_dir, vars, verbosity=command.verbosity, simulate=command.options.simulate, interactive=command.options.interactive, overwrite=command.options.overwrite, indent=1, template_renderer=self.render_template)

    def makedirs(self, dir):
        return os.makedirs(dir)

    def exists(self, path):
        return os.path.exists(path)

    def out(self, msg):
        print msg

    required_templates = ()

    def check_vars(self, vars, other):
        raise RuntimeError('Under ginsFSM, you should use the "gcreate" command rather than "paster create"')


class TypeMapper(dict):

    def __getitem__(self, item):
        options = item.split('|')
        for op in options[:-1]:
            try:
                value = eval_with_catch(op, dict(self.items()))
                break
            except (NameError, KeyError):
                pass

        else:
            value = eval(options[(-1)], dict(self.items()))

        if value is None:
            return ''
        else:
            return str(value)
            return


def eval_with_catch(expr, vars):
    try:
        return eval(expr, vars)
    except Exception as e:
        _add_except(e, 'in expression %r' % expr)
        raise


double_brace_pattern = re.compile('{{(?P<braced>.*?)}}')

def substitute_double_braces(content, values):

    def double_bracerepl(match):
        value = match.group('braced').strip()
        return values[value]

    return double_brace_pattern.sub(double_bracerepl, content)


def _add_except(exc, info):
    if not hasattr(exc, 'args') or exc.args is None:
        return
    args = list(exc.args)
    if args:
        args[0] += ' ' + info
    else:
        args = [
         info]
    exc.args = tuple(args)
    return