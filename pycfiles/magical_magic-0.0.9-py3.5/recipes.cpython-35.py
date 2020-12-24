# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/magical/recipes.py
# Compiled at: 2016-09-07 10:58:39
# Size of source mod 2**32: 1300 bytes
from magical.magic import magical
from toolz.curried import compose, partial
from jinja2 import Environment, Template
import IPython
from mistune import markdown
import yaml
__all__ = [
 'register_jinja2_magic', 'register_mistune_magic', 'register_yaml_magic']

def _render_jinja2_with_globals(template):
    return template.render(**IPython.get_ipython().user_ns)


def register_jinja2_magic(env=Environment(), display='Markdown'):
    """Display reusable jinja2 templates.  Returns a jinja2 template.
    """
    magical('jinja2', lang='jinja2', display=compose(IPython.display.display, IPython.display.Markdown, lambda x: x.render(**IPython.get_ipython().user_ns)))(env.from_string)
    return env


def register_mistune_magic(**kwargs):
    magical('mistune', display='HTML', lang='markdown')(compose(partial(markdown, **kwargs), _render_jinja2_with_globals, Template))


def register_yaml_magic(loader=yaml.SafeLoader):
    magical('yaml', display=print, lang='yaml')(compose(partial(yaml.load, Loader=loader), _render_jinja2_with_globals, Template))


register_yaml_magic()