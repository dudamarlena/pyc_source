# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/unidist/error_info.py
# Compiled at: 2010-10-14 14:04:23
"""
Error Information: Prints detailed stack information

TODO(g): Move out of unidist package.  It doesnt belong here.  Does it?
"""
import traceback, sys

def GetExceptionDetails(long=False, webify=True):
    """Print the usual traceback information, followed by a listing of all the
  local variables in each frame.
  """
    output = '\n-----START-----\n'
    tb = sys.exc_info()[2]
    while 1:
        if not tb.tb_next:
            break
        tb = tb.tb_next

    stack = []
    f = tb.tb_frame
    while f:
        stack.append(f)
        f = f.f_back

    stack.reverse()
    output += traceback.format_exc()
    if long:
        output += 'Locals by frame, innermost last\n'
        for frame in stack:
            output += '\nFrame %s in %s at line %s\n' % (frame.f_code.co_name,
             frame.f_code.co_filename,
             frame.f_lineno)
            for (key, value) in frame.f_locals.items():
                output += '\t%20s = ' % key
                try:
                    output += str(value) + '\n'
                except:
                    output += '<ERROR WHILE PRINTING VALUE>\n'

    output += '-----END-----'
    if webify:
        output = output.replace('\n', '<br>\n')
        output = output.replace('-----START-----', '<b>-----START-----</b>')
        output = output.replace('-----END-----', '<b>-----END-----</b>')
    return output