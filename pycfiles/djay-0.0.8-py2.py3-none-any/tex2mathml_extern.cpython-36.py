# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-m_4qh6p6/docutils/docutils/utils/math/tex2mathml_extern.py
# Compiled at: 2019-07-30 18:47:12
# Size of source mod 2**32: 5600 bytes
import subprocess
document_template = '\\documentclass{article}\n\\usepackage{amsmath}\n\\begin{document}\n%s\n\\end{document}\n'

def latexml(math_code, reporter=None):
    """Convert LaTeX math code to MathML with LaTeXML_

    .. _LaTeXML: http://dlmf.nist.gov/LaTeXML/
    """
    p = subprocess.Popen(['latexml',
     '-',
     '--inputencoding=utf8'],
      stdin=(subprocess.PIPE),
      stdout=(subprocess.PIPE),
      stderr=(subprocess.PIPE),
      close_fds=True)
    p.stdin.write((document_template % math_code).encode('utf8'))
    p.stdin.close()
    latexml_code = p.stdout.read()
    latexml_err = p.stderr.read().decode('utf8')
    if reporter:
        if latexml_err.find('Error') >= 0 or not latexml_code:
            reporter.error(latexml_err)
    post_p = subprocess.Popen(['latexmlpost',
     '-',
     '--nonumbersections',
     '--format=xhtml',
     '--'],
      stdin=(subprocess.PIPE),
      stdout=(subprocess.PIPE),
      stderr=(subprocess.PIPE),
      close_fds=True)
    post_p.stdin.write(latexml_code)
    post_p.stdin.close()
    result = post_p.stdout.read().decode('utf8')
    post_p_err = post_p.stderr.read().decode('utf8')
    if reporter:
        if post_p_err.find('Error') >= 0 or not result:
            reporter.error(post_p_err)
    start, end = result.find('<math'), result.find('</math>') + 7
    result = result[start:end]
    if 'class="ltx_ERROR' in result:
        raise SyntaxError(result)
    return result


def ttm(math_code, reporter=None):
    """Convert LaTeX math code to MathML with TtM_

    .. _TtM: http://hutchinson.belmont.ma.us/tth/mml/
    """
    p = subprocess.Popen(['ttm',
     '-u',
     '-r'],
      stdin=(subprocess.PIPE),
      stdout=(subprocess.PIPE),
      stderr=(subprocess.PIPE),
      close_fds=True)
    p.stdin.write((document_template % math_code).encode('utf8'))
    p.stdin.close()
    result = p.stdout.read()
    err = p.stderr.read().decode('utf8')
    if err.find('**** Unknown') >= 0:
        msg = '\n'.join([line for line in err.splitlines() if line.startswith('****')])
        raise SyntaxError('\nMessage from external converter TtM:\n' + msg)
    if reporter and err.find('**** Error') >= 0 or not result:
        reporter.error(err)
    start, end = result.find('<math'), result.find('</math>') + 7
    result = result[start:end]
    return result


def blahtexml(math_code, inline=True, reporter=None):
    """Convert LaTeX math code to MathML with blahtexml_

    .. _blahtexml: http://gva.noekeon.org/blahtexml/
    """
    options = [
     '--mathml',
     '--indented',
     '--spacing', 'moderate',
     '--mathml-encoding', 'raw',
     '--other-encoding', 'raw',
     '--doctype-xhtml+mathml',
     '--annotate-TeX']
    if inline:
        mathmode_arg = ''
    else:
        mathmode_arg = 'mode="display"'
        options.append('--displaymath')
    p = subprocess.Popen((['blahtexml'] + options), stdin=(subprocess.PIPE),
      stdout=(subprocess.PIPE),
      stderr=(subprocess.PIPE),
      close_fds=True)
    p.stdin.write(math_code.encode('utf8'))
    p.stdin.close()
    result = p.stdout.read().decode('utf8')
    err = p.stderr.read().decode('utf8')
    if result.find('<error>') >= 0:
        raise SyntaxError('\nMessage from external converter blahtexml:\n' + result[result.find('<message>') + 9:result.find('</message>')])
    if reporter:
        if err.find('**** Error') >= 0 or not result:
            reporter.error(err)
    start, end = result.find('<markup>') + 9, result.find('</markup>')
    result = '<math xmlns="http://www.w3.org/1998/Math/MathML"%s>\n%s</math>\n' % (
     mathmode_arg, result[start:end])
    return result


if __name__ == '__main__':
    example = '\\frac{\\partial \\sin^2(\\alpha)}{\\partial \\vec r} \\varpi \\, \\text{Grüße}'
    print(blahtexml(example).encode('utf8'))