# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/evax/bitten/tools/lcov.py
# Compiled at: 2010-07-27 02:21:05
__docformat__ = 'restructuredtext en'
from bitten.build import CommandLine
from bitten.util import xmlio
import os

def lcov(ctxt, directory=None):
    """ Use lcov to extract code coverage information

    :param ctxt: the build context
    :type ctxt: `Context`
    :param directory: the directory where to look for gcov files
    """
    assert directory, 'Missing required attribute "directory"'
    options = ['--directory', directory, '--capture', '--output-file', '-']
    cmd = CommandLine('lcov', options, cwd=ctxt.basedir)
    coverage = xmlio.Fragment()
    cur_elem = cur_lines = full_path = None
    instrumented_lines = {}
    for (out, err) in cmd.execute():
        if err or out is None:
            continue
        if out.startswith('SF:'):
            path = out[3:]
            if not path.startswith(ctxt.basedir):
                continue
            full_path = path
            basename = os.path.basename(path)
            fname = os.path.join(directory, basename)
            cur_elem = xmlio.Element('coverage', name=fname, file=fname, lines=0, percentage=0)
            continue
        if out == 'end_of_record':
            if cur_elem:
                sfile = open(full_path, 'r')
                lines = []
                for i in range(1, len(sfile.readlines())):
                    if instrumented_lines.has_key(i):
                        lines.append(instrumented_lines[i])
                    else:
                        lines.append('-')

                sfile.close()
                cur_elem.append(xmlio.Element('line_hits')[(' ').join(lines)])
                instrumented_lines.clear()
                coverage.append(cur_elem)
                cur_elem = None
                full_path = None
            continue
        if out.startswith('LF:'):
            if cur_elem:
                cur_elem.attr['lines'] = cur_lines = out[3:]
            continue
        if out.startswith('DA:'):
            if cur_elem:
                (linenum, count) = out[3:].split(',')
                instrumented_lines[int(linenum)] = count
            continue
        if out.startswith('LH:'):
            if cur_elem and cur_lines:
                percent = int(round(int(out[3:]) * 100.0 / int(cur_lines)))
                cur_elem.attr['percentage'] = percent
                cur_lines = None
            continue

    ctxt.report('coverage', coverage)
    return