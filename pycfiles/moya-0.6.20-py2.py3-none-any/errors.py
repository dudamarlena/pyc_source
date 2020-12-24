# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/will/projects/moya/moya/template/errors.py
# Compiled at: 2016-12-08 16:29:22
from __future__ import unicode_literals
from __future__ import print_function
from ..compat import implements_to_string, text_type

class MoyaRuntimeError(Exception):

    def __init__(self):
        pass


@implements_to_string
class MissingTemplateError(Exception):
    hide_py_traceback = True
    error_type = b'Missing Template'

    def __init__(self, path, diagnosis=None):
        self.path = path
        self.diagnosis = diagnosis or b"The referenced template doesn't exists in the templates filesystem. Run the following to see what templates are installed:\n\n **$ moya fs templates --tree**"

    def __str__(self):
        return (b'Missing template "{}"').format(self.path)

    __repr__ = __str__


@implements_to_string
class BadTemplateError(MissingTemplateError):
    hide_py_traceback = False
    error_type = b'Bad Template'

    def __str__(self):
        return b'Unable to load template "%s"' % self.path


@implements_to_string
class RecursiveTemplateError(Exception):

    def __init__(self, path):
        self.path = path

    def __str__(self):
        return (b"Template '{}' has already been used in an extends directive").format(self.path)


@implements_to_string
class TemplateError(Exception):
    hide_py_traceback = True

    def __init__(self, msg, path, lineno, diagnosis=None, original=None, trace_frames=None):
        self.msg = msg
        self.path = path
        self.lineno = lineno
        self.diagnosis = diagnosis
        self.original = original
        self.trace_frames = trace_frames or []
        super(TemplateError, self).__init__()

    def __str__(self):
        return self.msg

    def __repr__(self):
        return b'File "%s", line %s: %s' % (self.path, self.lineno, self.msg)

    def get_moya_error(self):
        return b'File "%s", line %s: %s' % (self.path, self.lineno, self.msg)

    def get_moya_frames(self):
        return self.trace_frames[:]


@implements_to_string
class NodeError(Exception):
    hide_py_traceback = True
    error_type = b'Template Node Error'

    def __init__(self, msg, node, lineno, start, end, diagnosis=None):
        self.msg = msg
        self.node = node
        self.lineno = lineno
        self.start = start
        self.end = end
        self.diagnosis = diagnosis

    def __str__(self):
        return self.msg


class UnknownTag(NodeError):
    pass


class UnmatchedTag(NodeError):
    pass


class TagSyntaxError(NodeError):
    pass


class RecursiveExtends(NodeError):
    pass


@implements_to_string
class TokenizerError(Exception):

    def __init__(self, msg, lineno, start, end, diagnosis=None):
        self.msg = msg
        self.lineno = lineno
        self.start = start
        self.end = end
        self.diagnosis = diagnosis

    def __str__(self):
        return self.msg


class UnmatchedComment(TokenizerError):
    pass


@implements_to_string
class TagError(Exception):

    def __init__(self, msg, node, diagnosis=None):
        self.msg = msg
        self.node = node
        self.diagnosis = diagnosis
        super(TagError, self).__init__((b'{} {}').format(msg, text_type(node)))

    def __str__(self):
        return self.msg