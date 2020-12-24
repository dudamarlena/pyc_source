# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-intel/egg/elaphe/utils.py
# Compiled at: 2013-06-16 19:17:06
from os.path import abspath, dirname, join as pathjoin
import re
__all__ = [
 'DEFAULT_PS_CODE_PATH', 'DEFAULT_DISTILL_RE',
 'to_ps', 'dict_to_optstring', 'distill_ps_code',
 'DEFAULT_EPSF_DSC_TEMPLATE', 'DEFAULT_RENDER_COMMAND_TEMPLATE',
 'init_ps_code_template', 'BARCODE_PS_CODE_PATH', 'PS_CODE_TEMPLATE']
DEFAULT_PS_CODE_PATH = pathjoin(dirname(abspath(__file__)), 'postscriptbarcode', 'barcode.ps')
DEFAULT_DISTILL_RE = re.compile('% --BEGIN TEMPLATE--(.+)% --END TEMPLATE--', re.S)

def to_ps(obj, parlen=False):
    """Converts object into postscript literal"""
    if isinstance(obj, str) and parlen:
        return '(%s)' % obj
    else:
        if isinstance(obj, bool):
            return {True: 'true', False: 'false'}[obj]
        return str(obj)


def dict_to_optstring(d, none=lambda x: ' () ', empty=lambda x: ' () '):
    """Converts dictionary into ps string in barcode.ps specific format.

    >>> dict_to_optstring(dict(purpose='seekagrail', color='yellow', spam=True, egg=False))
    ' (color=yellow purpose=seekagrail spam) '
    >>> dict_to_optstring(dict())
    ' () '
    >>> dict_to_optstring(None)
    ' () '
    """
    if d is None:
        return none(d)
    else:
        if d:
            return ' ' + to_ps((' ').join(key + {True: '', False: '=%s' % to_ps(value)}[(value is True)] for key, value in d.items() if value is not False), parlen=True) + ' '
        else:
            return empty(d)

        return


def distill_ps_code(path_to_ps_code=DEFAULT_PS_CODE_PATH, distill_regexp=DEFAULT_DISTILL_RE):
    """
    Distills barcode procedure code blocks with given path and regexp.

    >>> print distill_ps_code() # doctest: +ELLIPSIS
    <BLANKLINE>
    <BLANKLINE>
    %% --BEGIN ENCODER ean13--
    %% --DESC: EAN-13
    %% --EXAM: 977147396801
    %% --EXOP: includetext guardwhitespace
    %% --RNDR: renlinear
    ...
    /barcode load 0 1 dict put
    %% --END DISPATCHER--
    <BLANKLINE>
    <BLANKLINE>
    """
    return distill_regexp.findall(open(path_to_ps_code, 'rb').read())[0].replace('%', '%%')


DEFAULT_EPSF_DSC_TEMPLATE = '%%!PS-Adobe-2.0\n%%%%Pages: (attend)\n%%%%Creator: Elaphe powered by barcode.ps\n%%%%BoundingBox: %(bbox)s\n%%%%LanguageLevel: 2\n%%%%EndComments\n'
DEFAULT_RENDER_COMMAND_TEMPLATE = '\ngsave\n0 0 moveto\n%(xscale)f %(yscale)f scale\n%(codestring)s%(options)s%(codetype)s barcode\ngrestore\nshowpage\n'

def init_ps_code_template(epsf_dsc_template=DEFAULT_EPSF_DSC_TEMPLATE, render_command_template=DEFAULT_RENDER_COMMAND_TEMPLATE, ps_code_distiller=distill_ps_code):
    """Initializes postscript code template.
    """
    return ('\n').join([epsf_dsc_template, ps_code_distiller(), render_command_template])


BARCODE_PS_CODE_PATH = distill_ps_code()
PS_CODE_TEMPLATE = init_ps_code_template()
if __name__ == '__main__':
    from doctest import testmod
    testmod()