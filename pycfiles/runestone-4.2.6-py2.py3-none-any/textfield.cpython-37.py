# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/bmiller/Runestone/RunestoneComponents/runestone/activecode/textfield.py
# Compiled at: 2019-11-02 08:12:59
# Size of source mod 2**32: 1988 bytes
__author__ = 'bmiller'
from docutils import nodes
from docutils.parsers.rst import directives
from docutils.parsers.rst import Directive
import json, random

def textfield_role(name, rawtext, text, lineno, inliner, options={}, content=[]):
    """
    Usage:
    In your document you can write :textfield:`myid:myvalue:width`
    This will translate to:
        <input type='text' id='myid' class="form-control input-small" style="display:inline; width:width;" value='myvalue'></input>

    where width can be specified in pixels or percentage of page width (standard CSS syntax).
    Width can also be specified using relative sizes:
        mini, small, medium, large, xlarge, and xxlarge
    """
    iid, value, width = text.split(':')
    if 'mini' in width:
        width = '60px'
    else:
        if 'small' in width:
            width = '90px'
        else:
            if 'medium' in width:
                width = '150px'
            else:
                if 'large' in width:
                    width = '210px'
                else:
                    if 'xlarge' in width:
                        width = '270px'
                    else:
                        if 'xxlarge' in width:
                            width = '530px'
    res = '<input type=\'text\' id=\'%s\' class="form-control" style="display:inline; width: %s;" value="%s"></input>' % (
     iid, width, value)
    return (
     [
      nodes.raw('', res, format='html')], [])