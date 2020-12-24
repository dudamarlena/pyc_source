# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/projex/makotext.py
# Compiled at: 2016-07-03 23:28:12
""" The mako """
import logging, os, projex
logger = logging.getLogger(__name__)
try:
    import mako, mako.template, mako.lookup
except ImportError:
    logger.warning('The projex.makotext package requires mako to be installed.')
    mako = None

from datetime import datetime, date
import projex.text
_macros = {}

def register(macro):
    """
    Registers a macro method for the mako text rendering system.
    
    :param      macro | <method>
    """
    _macros[macro.__name__] = macro


def renderfile(filename, options=None, templatePaths=None, default='', silent=False):
    """
    Renders a file to text using the mako template system.
    
    To learn more about mako and its usage, see [[www.makotemplates.org]]
    
    :return     <str> formatted text
    """
    if not mako:
        logger.debug('mako is not installed')
        return default
    else:
        if not mako:
            logger.debug('mako is not installed.')
            return default
        if templatePaths is None:
            templatePaths = []
        basepath = os.environ.get('MAKO_TEMPLATEPATH', '')
        if basepath:
            basetempls = basepath.split(os.path.pathsep)
        else:
            basetempls = []
        templatePaths += basetempls
        templatePaths.insert(0, os.path.dirname(filename))
        templatePaths = map(lambda x: x.replace('\\', '/'), templatePaths)
        scope = dict(os.environ)
        scope['projex_text'] = projex.text
        scope['date'] = date
        scope['datetime'] = datetime
        scope.update(_macros)
        scope.update(os.environ)
        if options is not None:
            scope.update(options)
        old_env_path = os.environ.get('MAKO_TEMPLATEPATH', '')
        os.environ['MAKO_TEMPLATEPATH'] = os.path.pathsep.join(templatePaths)
        logger.debug('rendering mako file: %s', filename)
        if templatePaths:
            lookup = mako.lookup.TemplateLookup(directories=templatePaths)
            templ = mako.template.Template(filename=filename, lookup=lookup)
        else:
            templ = mako.template.Template(filename=filename)
        try:
            output = templ.render(**scope)
        except StandardError:
            output = default
            if not silent:
                logger.exception('Error rendering mako text')

        os.environ['MAKO_TEMPLATEPATH'] = old_env_path
        return output


def render(text, options=None, templatePaths=None, default=None, silent=False, raiseErrors=False):
    """
    Renders a template text to a resolved text value using the mako template
    system.
    
    Provides a much more robust template option to the projex.text system.  
    While the projex.text method can handle many simple cases with no
    dependencies, the makotext module makes use of the powerful mako template
    language.  This module provides a simple wrapper to the mako code.
    
    To learn more about mako and its usage, see [[www.makotemplates.org]]
    
    :param      text        <str>
    :param      options     <dict> { <str> key: <variant> value, .. }
    
    :return     <str> formatted text
    
    :usage      |import projex.makotext
                |options = { 'key': 10, 'name': 'eric' }
                |template = '${name.lower()}_${key}_${date.today()}.txt'
                |projex.makotext.render( template, options )
    """
    if not mako:
        logger.debug('mako is not installed.')
        if default is None:
            return text
        return default
    if templatePaths is None:
        templatePaths = []
    basepath = os.environ.get('MAKO_TEMPLATEPATH', '')
    if basepath:
        basetempls = basepath.split(os.path.pathsep)
    else:
        basetempls = []
    templatePaths += basetempls
    scope = dict(os.environ)
    scope['projex_text'] = projex.text
    scope['date'] = date
    scope['datetime'] = datetime
    scope.update(_macros)
    if options is not None:
        scope.update(options)
    if templatePaths:
        lookup = mako.lookup.TemplateLookup(directories=templatePaths)
        try:
            templ = mako.template.Template(text, lookup=lookup)
        except StandardError:
            output = text if default is None else default
            if not silent:
                logger.exception('Error compiling mako text')
            return output

    else:
        try:
            templ = mako.template.Template(text)
        except StandardError:
            output = text if default is None else default
            if not silent:
                logger.exception('Error compiling mako text')
            return output

        try:
            output = templ.render(**scope)
        except StandardError:
            if raiseErrors:
                raise
            output = text if default is None else default
            if not silent:
                logger.exception('Error rendering mako text')
            return output

    return output


def unregister(method):
    """
    Unregisters the given macro from the system.
    
    :param      name | <str>
    """
    _macros.pop(method.__name__, None)
    return


def collectfiles(path, filt=None):
    """
    Collects some files based on the given filename.
    
    :param      path | <str>
                filt | <method>
        
    :return     [(<str> name, <str> filepath), ..]
    """
    if not os.path.isdir(path):
        path = os.path.dirname(path)
    output = []
    for name in sorted(os.listdir(path)):
        filepath = os.path.join(path, name)
        if os.path.isfile(filepath):
            if not filt or filt(name):
                output.append((name, filepath))

    return output


register(collectfiles)