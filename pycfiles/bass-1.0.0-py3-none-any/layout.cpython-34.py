# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nico/computer/venv/lib/python3.4/site-packages/bass/layout.py
# Compiled at: 2015-09-06 05:31:13
# Size of source mod 2**32: 2591 bytes
"""
bass.layout
-----
Objects and functions related to the layout of the rendered pages.
Chameleon is the primary template engine. Other template engines can be added.
"""
from . import setting
from os import listdir
from os.path import join, splitext
import logging, sys
template_factory = {}

def add_template_type(suffix, factory):
    """add template factory for given suffix"""
    if suffix in template_factory:
        logging.debug('Cannot redefine template type %s', suffix)
    else:
        logging.debug('Define new template type %s', suffix)
    template_factory[suffix] = factory


def copy_template_type(from_suffix, to_suffix):
    """copy existing template factory to another suffix"""
    if to_suffix in template_factory:
        logging.debug('Cannot redefine template type %s', to_suffix)
    else:
        if from_suffix in template_factory:
            logging.debug('Template type %s copied from %s', to_suffix, from_suffix)
            template_factory[to_suffix] = template_factory[from_suffix]
        else:
            logging.debug('No template type %s', from_suffix)


try:
    from chameleon import PageTemplateFile
    add_template_type('.xml', PageTemplateFile)
    copy_template_type('.xml', '.pt')
except ImportError:
    logging.critical('Chameleon template engine not available')
    sys.exit(1)

def read_templates():
    """read templates from layout directory"""
    template = {}
    template_types = list(template_factory.keys())
    logging.debug('Scanning for templates in {0}'.format(setting.layout))
    logging.debug('Template types: {0}'.format(' '.join(template_types)))
    for filename in listdir(setting.layout):
        name, extension = splitext(filename)
        if extension in template_types:
            try:
                template[name] = template_factory[extension](join(setting.layout, filename))
            except Exception as e:
                logging.debug('Error in template for {0} in file {1}'.format(name, filename))
                logging.debug(str(e))

            continue

    if 'default' in template:
        setting.template = template
    else:
        logging.critical('There is no default template')
        sys.exit(1)