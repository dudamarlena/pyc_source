# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/unidist/stack.py
# Compiled at: 2010-10-14 14:04:22
"""
Print out a one-line version of the stack.
"""
import traceback, os

def Mini(depth=0, start_back_offset=0):
    """Returns a miniaturized string of the stack, useful for debugging.
  
  Args:
    depth: int (optional), depth to look into stack
    start_back_offset: int (optional), depth to go back before reporting the
        stack, to avoid reporting the end of the stack, if it only the calling
        functions are useful.
  """
    depth += 2
    start_back = -1
    start_back -= start_back_offset
    stack = traceback.extract_stack()
    items = []
    for item in stack[len(stack) - depth:start_back]:
        msg = '%s:%s:%s' % (os.path.basename(item[0]), item[1], item[2])
        items.append(msg)

    return (' -> ').join(items)


if __name__ == '__main__':
    pass