# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tex.py
# Compiled at: 2012-01-06 10:42:33
r'''Convert LaTeX or TeX source to PDF or DVI, and escape strings for LaTeX.

**The python-tex project is obsolete!** Please have a look at Texcaller_.

.. _Texcaller: http://www.profv.de/texcaller/

Python-tex is a convenient interface
to the TeX command line tools
that handles all kinds of errors without much fuzz.

Temporary files are always cleaned up.
The TeX interpreter is automatically re-run as often as necessary,
and an exception is thrown
in case the output fails to stabilize soon enough.
The TeX interpreter is always run in batch mode,
so it won't ever get in your way by stopping your application
when there are issues with your TeX source.
Instead, an exception is thrown
that contains all information of the TeX log.

This enables you to debug TeX related issues
directly within your application
or within an interactive Python interpreter session.

Example:

>>> from tex import latex2pdf
>>> document = ur"""
... \documentclass{article}
... \begin{document}
... Hello, World!
... \end{document}
... """
>>> pdf = latex2pdf(document)

>>> type(pdf)
<type 'str'>
>>> print "PDF size: %.1f KB" % (len(pdf) / 1024.0)
PDF size: 5.6 KB
>>> pdf[:5]
'%PDF-'
>>> pdf[-6:]
'%%EOF\n'
'''
__version__ = '1.8'
__author__ = 'Volker Grabsch'
__author_email__ = 'vog@notjusthosting.com'
__url__ = 'http://www.profv.de/python-tex/'
__classifiers__ = '\n                   Development Status :: 5 - Production/Stable\n                   Development Status :: 6 - Mature\n                   Development Status :: 7 - Inactive\n                   Intended Audience :: Developers\n                   License :: OSI Approved :: MIT License\n                   Operating System :: OS Independent\n                   Programming Language :: Python\n                   Topic :: Documentation\n                   Topic :: Office/Business\n                   Topic :: Printing\n                   Topic :: Software Development :: Libraries :: Python Modules\n                   Topic :: Text Processing :: Markup :: LaTeX\n                   '
__license__ = '\nPermission is hereby granted, free of charge, to any person obtaining\na copy of this software and associated documentation files (the\n"Software"), to deal in the Software without restriction, including\nwithout limitation the rights to use, copy, modify, merge, publish,\ndistribute, sublicense, and/or sell copies of the Software, and to\npermit persons to whom the Software is furnished to do so, subject\nto the following conditions:\n\nThe above copyright notice and this permission notice shall be\nincluded in all copies or substantial portions of the Software.\n\nTHE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,\nEXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF\nMERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.\nIN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY\nCLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,\nTORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE\nSOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.\n'
import os, os.path, random, shutil, string, subprocess, tempfile

def _file_read(filename):
    """Read the content of a file and close it properly."""
    f = file(filename, 'rb')
    content = f.read()
    f.close()
    return content


def _file_write(filename, content):
    """Write into a file and close it properly."""
    f = file(filename, 'wb')
    f.write(content)
    f.close()


def convert(tex_source, input_format, output_format, max_runs=5):
    """Convert LaTeX or TeX source to PDF or DVI."""
    assert isinstance(tex_source, unicode)
    try:
        tex_cmd, output_suffix = {('tex', 'dvi'): ('tex', '.dvi'), ('latex', 'dvi'): ('latex', '.dvi'), 
           ('tex', 'pdf'): ('pdftex', '.pdf'), 
           ('latex', 'pdf'): ('pdflatex', '.pdf')}[(
         input_format, output_format)]
    except KeyError:
        raise ValueError('Unable to handle conversion: %s -> %s' % (
         input_format, output_format))

    if max_runs < 2:
        raise ValueError('max_runs must be at least 2.')
    tex_dir = tempfile.mkdtemp(suffix='', prefix='tex-temp-')
    try:
        tex_filename = os.path.join(tex_dir, 'texput.tex')
        _file_write(tex_filename, tex_source.encode('UTF-8'))
        aux_old = None
        for i in xrange(max_runs):
            tex_process = subprocess.Popen([
             tex_cmd,
             '-interaction=batchmode',
             '-halt-on-error',
             '-no-shell-escape',
             tex_filename], stdin=file(os.devnull, 'r'), stdout=file(os.devnull, 'w'), stderr=subprocess.STDOUT, close_fds=True, shell=False, cwd=tex_dir, env={'PATH': os.getenv('PATH')})
            tex_process.wait()
            if tex_process.returncode != 0:
                log = _file_read(os.path.join(tex_dir, 'texput.log'))
                raise ValueError(log)
            aux = _file_read(os.path.join(tex_dir, 'texput.aux'))
            if aux == aux_old:
                try:
                    return _file_read(os.path.join(tex_dir, 'texput' + output_suffix))
                except:
                    raise ValueError('No output file was produced.')

            aux_old = aux

        raise ValueError("%s didn't stabilize after %i runs" % (
         'texput.aux', max_runs))
    finally:
        shutil.rmtree(tex_dir)

    return


def tex2dvi(tex_source, **kwargs):
    """Convert TeX source to DVI."""
    return convert(tex_source, 'tex', 'dvi', **kwargs)


def latex2dvi(tex_source, **kwargs):
    """Convert LaTeX source to DVI."""
    return convert(tex_source, 'latex', 'dvi', **kwargs)


def tex2pdf(tex_source, **kwargs):
    """Convert TeX source to PDF."""
    return convert(tex_source, 'tex', 'pdf', **kwargs)


def latex2pdf(tex_source, **kwargs):
    """Convert LaTeX source to PDF."""
    return convert(tex_source, 'latex', 'pdf', **kwargs)


_latex_special_chars = {'$': '\\$', 
   '%': '\\%', 
   '&': '\\&', 
   '#': '\\#', 
   '_': '\\_', 
   '{': '\\{', 
   '}': '\\}', 
   '[': '{[}', 
   ']': '{]}', 
   '"': "{''}", 
   '\\': '\\textbackslash{}', 
   '~': '\\textasciitilde{}', 
   '<': '\\textless{}', 
   '>': '\\textgreater{}', 
   '^': '\\textasciicircum{}', 
   '`': '{}`', 
   '\n': '\\\\'}

def escape_latex(s):
    r"""Escape a unicode string for LaTeX.

    :Warning:
        The source string must not contain empty lines such as:
            - u'\n...' -- empty first line
            - u'...\n\n...' -- empty line in between
            - u'...\n' -- empty last line

    :Parameters:
        - `s`: unicode object to escape for LaTeX

    >>> s = u'\\"{}_&%a$b#\nc[]"~<>^`\\'
    >>> escape_latex(s)
    u"\\textbackslash{}{''}\\{\\}\\_\\&\\%a\\$b\\#\\\\c{[}{]}{''}\\textasciitilde{}\\textless{}\\textgreater{}\\textasciicircum{}{}`\\textbackslash{}"
    >>> print s
    \"{}_&%a$b#
    c[]"~<>^`\
    >>> print escape_latex(s)
    \textbackslash{}{''}\{\}\_\&\%a\$b\#\\c{[}{]}{''}\textasciitilde{}\textless{}\textgreater{}\textasciicircum{}{}`\textbackslash{}
    """
    return ('').join(_latex_special_chars.get(c, c) for c in s)


def _test():
    """Run all doc tests of this module."""
    import doctest, tex
    return doctest.testmod(tex)


if __name__ == '__main__':
    _test()