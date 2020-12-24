# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ana/dev/dexy-clean/dexy/commands/templates.py
# Compiled at: 2020-03-18 15:12:33
# Size of source mod 2**32: 3356 bytes
from dexy.commands.utils import init_wrapper
from dexy.commands.utils import template_text
from dexy.utils import getdoc
import dexy.templates, os, sys
from dexy.utils import file_exists
DEFAULT_TEMPLATE = 'dexy:default'

def gen_command(plugins='', d=None, t=False, template=DEFAULT_TEMPLATE, **kwargs):
    """
    Generate a new dexy project in the specified directory, using the template.
    """
    wrapper = init_wrapper(locals())
    if t and template == DEFAULT_TEMPLATE:
        template = t
    else:
        if t:
            if template != DEFAULT_TEMPLATE:
                raise dexy.exceptions.UserFeedback('Only specify one of --t or --template, not both.')
    if template not in dexy.template.Template.plugins:
        print("Can't find a template named '%s'. Run 'dexy templates' for a list of templates." % template)
        sys.exit(1)
    template_instance = dexy.template.Template.create_instance(template)
    (template_instance.generate)(d, **kwargs)
    os.chdir(d)
    wrapper.create_dexy_dirs()
    print("Success! Your new dexy project has been created in directory '%s'" % d)
    if file_exists('README'):
        print('\n--------------------------------------------------')
        with open('README', 'r') as (f):
            print(f.read())
        print('\n--------------------------------------------------')
        print("\nThis information is in the 'README' file for future reference.")


def template_command(alias=None):
    print(template_text(alias))


def templates_command(plugins='', simple=False, validate=False, key=False):
    """
    List templates that can be used to generate new projects.
    """
    init_wrapper(locals())
    if not simple:
        FMT = '%-40s %s'
        print(FMT % ('Alias', 'Info'))
    for i, template in enumerate(dexy.template.Template):
        if key:
            if key not in template.alias:
                continue
            else:
                if template.setting('nodoc'):
                    continue
                if simple:
                    print(template.alias)
            first_line_help = template.setting('help').splitlines()[0].strip()
            print((FMT % (template.alias, first_line_help)), end=' ')
            if validate:
                print(' validating...', end=' ')
                print(template.validate() and 'OK' or 'ERROR')
        else:
            print('')

    if i < 5:
        print("Run '[sudo] pip install dexy-templates' to install some more templates.")
    if not simple:
        print("Run 'dexy help -on gen' for help on generating projects from templates.")