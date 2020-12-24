# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-ed191__6/docutils/docutils/transforms/components.py
# Compiled at: 2020-01-10 16:25:35
# Size of source mod 2**32: 1993 bytes
"""
Docutils component-related transforms.
"""
__docformat__ = 'reStructuredText'
import sys, os, re, time
from docutils import nodes, utils
from docutils import ApplicationError, DataError
from docutils.transforms import Transform, TransformError

class Filter(Transform):
    __doc__ = '\n    Include or exclude elements which depend on a specific Docutils component.\n\n    For use with `nodes.pending` elements.  A "pending" element\'s dictionary\n    attribute ``details`` must contain the keys "component" and "format".  The\n    value of ``details[\'component\']`` must match the type name of the\n    component the elements depend on (e.g. "writer").  The value of\n    ``details[\'format\']`` is the name of a specific format or context of that\n    component (e.g. "html").  If the matching Docutils component supports that\n    format or context, the "pending" element is replaced by the contents of\n    ``details[\'nodes\']`` (a list of nodes); otherwise, the "pending" element\n    is removed.\n\n    For example, the reStructuredText "meta" directive creates a "pending"\n    element containing a "meta" element (in ``pending.details[\'nodes\']``).\n    Only writers (``pending.details[\'component\'] == \'writer\'``) supporting the\n    "html" format (``pending.details[\'format\'] == \'html\'``) will include the\n    "meta" element; it will be deleted from the output of all other writers.\n    '
    default_priority = 780

    def apply(self):
        pending = self.startnode
        component_type = pending.details['component']
        format = pending.details['format']
        component = self.document.transformer.components[component_type]
        if component.supports(format):
            pending.replace_self(pending.details['nodes'])
        else:
            pending.parent.remove(pending)