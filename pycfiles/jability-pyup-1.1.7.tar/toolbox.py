# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/fabrom/workspace/jability-python-package/jabilitypyup/toolbox.py
# Compiled at: 2013-05-25 04:38:30
""" Module d'outils divers
"""
__author__ = 'Fabrice Romand'
__copyright__ = 'Copyleft 2008, Fabrice Romand'
__credits__ = ['Fabrice Romand']
__license__ = 'GPL'
__version__ = '1.1'
__maintainer__ = 'Fabrice Romand'
__email__ = 'fabrom@jability.org'
__status__ = 'Development'
import locale, logging, os.path, re, sys, time

def encstr(x, srccoding=None, tgtcoding=None):
    u"""Encodage d'une chaine unicode,str et de tous objets
        renvoyant une chaine de représentation en chaine encodée.

    >>> a = u'ésséîïàç'
    >>> a1 = encstr(a)
    >>> a1 == 'ésséîïàç'
    True

    >>> b = 'ésséîïàç'
    >>> b1 = encstr(b)
    >>> b1 == 'ésséîïàç'
    True

    >>> c = 3
    >>> encstr(c)
    '3'
    """
    if srccoding == None:
        srccoding = locale.getdefaultlocale()[1]
    if tgtcoding == None:
        tgtcoding = locale.getdefaultlocale()[1]
    if isinstance(x, unicode):
        y = x
    elif isinstance(x, str):
        y = unicode(x, srccoding)
    else:
        y = unicode(str(x))
    return y.encode(tgtcoding)


def convert_template(template, opener='{', closer='}'):
    """Doctests for templates with bracketed placeholders

    >>> s = 'People of {planet}, take us to your leader.'
    >>> d = dict(planet='Earth')
    >>> print convert_template(s) % d
    People of Earth, take us to your leader.

    >>> s = 'People of <planet>, take us to your leader.'
    >>> print convert_template(s, '<', '>') % d
    People of Earth, take us to your leader.

    """
    opener = re.escape(opener)
    closer = re.escape(closer)
    pattern = re.compile(opener + '([_A-Za-z][_A-Za-z0-9]*)' + closer)
    return re.sub(pattern, '%(\\1)s', template.replace('%', '%%'))


def get_stream_encoding(stream):
    """Renvoie l'encodage pour le stream"""
    encoding = stream.encoding
    if encoding == None:
        encoding = locale.getpreferredencoding()
    return encoding


def printu(unicodemsg, streamhdl=sys.stdout, encoding=None):
    u"""Affichage d'un message en unicode sur un stream
        encodé (par défaut, stdout)
    """
    if encoding == None:
        encoding = get_stream_encoding(streamhdl)
    if isinstance(unicodemsg, unicode):
        print >> streamhdl, unicodemsg.encode(encoding)
    else:
        print >> streamhdl, unicodemsg
    return


def timedfilename(prefix='', timefmt='%Y%m%d%H%M%S', ext='.tmp'):
    u"""Renvoi un nom de fichier composé avec
        ''prefix'' + <date/heure au format ''timefmt''> + ''ext''
    """
    return prefix + time.strftime(timefmt) + ext


def ensure_listindex(listobj, index_expression, default=''):
    u"""Permet d'éviter les IndexError déclenchés par l'absence d'un indice
        dans une expression représentant l'appel d'un élèment de liste/tuple.
        Si l'indice existe, la valeur correspondante est renvoyée.
        Si l'indice n'existe pas, la fonction renvoie la valeur par défaut.
    """
    mylocallist = listobj
    try:
        res = eval('mylocallist' + index_expression)
    except (IndexError, TypeError):
        return default

    return res


def logger_force_rollover(loggerobj):
    u"""Force la rotation de tous les handlers de type RotatingFileHandler ou
        TimedRotatingFileHandler pour le ''loggerobj'' fourni
        Renvoie le nombre de rollover effectué ou -1 si erreur
    """
    count = 0
    if isinstance(loggerobj, logging.Logger):
        for loginst in loggerobj.handlers:
            if isinstance(loginst, logging.handlers.RotatingFileHandler) or isinstance(loginst, logging.handlers.TimedRotatingFileHandler):
                loginst.doRollover()
                count += 1

        return count
    return -1