# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pynestml/visitors/comment_collector_visitor.py
# Compiled at: 2020-03-05 05:49:41
# Size of source mod 2**32: 12304 bytes
from pynestml.generated.PyNestMLParserVisitor import PyNestMLParserVisitor

class CommentCollectorVisitor(PyNestMLParserVisitor):
    __doc__ = '\n    This visitor iterates over a given parse tree and inspects the corresponding stream of tokens in order\n    to update all nodes by their corresponding tokens.\n    Attributes:\n        __tokens (list): A list of all tokens representing the model.\n    '

    def __init__(self, tokens):
        self._CommentCollectorVisitor__tokens = tokens

    def visitBlockWithVariables(self, ctx):
        return (
         get_comments(ctx, self._CommentCollectorVisitor__tokens), get_pre_comment(ctx, self._CommentCollectorVisitor__tokens),
         get_in_comments(ctx, self._CommentCollectorVisitor__tokens), get_post_comments(ctx, self._CommentCollectorVisitor__tokens))

    def visitBlock(self, ctx):
        return (
         get_comments(ctx, self._CommentCollectorVisitor__tokens), get_pre_comment(ctx, self._CommentCollectorVisitor__tokens),
         get_in_comments(ctx, self._CommentCollectorVisitor__tokens), get_post_comments(ctx, self._CommentCollectorVisitor__tokens))

    def visitNeuron(self, ctx):
        return (
         get_comments(ctx, self._CommentCollectorVisitor__tokens), get_pre_comment(ctx, self._CommentCollectorVisitor__tokens),
         get_in_comments(ctx, self._CommentCollectorVisitor__tokens), get_post_comments(ctx, self._CommentCollectorVisitor__tokens))

    def visitOdeEquation(self, ctx):
        return (
         get_comments(ctx, self._CommentCollectorVisitor__tokens), get_pre_comment(ctx, self._CommentCollectorVisitor__tokens),
         get_in_comments(ctx, self._CommentCollectorVisitor__tokens), get_post_comments(ctx, self._CommentCollectorVisitor__tokens))

    def visitOdeFunction(self, ctx):
        return (
         get_comments(ctx, self._CommentCollectorVisitor__tokens), get_pre_comment(ctx, self._CommentCollectorVisitor__tokens),
         get_in_comments(ctx, self._CommentCollectorVisitor__tokens), get_post_comments(ctx, self._CommentCollectorVisitor__tokens))

    def visitOdeShape(self, ctx):
        return (
         get_comments(ctx, self._CommentCollectorVisitor__tokens), get_pre_comment(ctx, self._CommentCollectorVisitor__tokens),
         get_in_comments(ctx, self._CommentCollectorVisitor__tokens), get_post_comments(ctx, self._CommentCollectorVisitor__tokens))

    def visitStmt(self, ctx):
        return (
         get_comments(ctx, self._CommentCollectorVisitor__tokens), get_pre_comment(ctx, self._CommentCollectorVisitor__tokens),
         get_in_comments(ctx, self._CommentCollectorVisitor__tokens), get_post_comments(ctx, self._CommentCollectorVisitor__tokens))

    def visitSmallStmt(self, ctx):
        return (
         get_comments(ctx, self._CommentCollectorVisitor__tokens), get_pre_comment(ctx, self._CommentCollectorVisitor__tokens),
         get_in_comments(ctx, self._CommentCollectorVisitor__tokens), get_post_comments(ctx, self._CommentCollectorVisitor__tokens))

    def visitCompoundStmt(self, ctx):
        return (
         get_comments(ctx, self._CommentCollectorVisitor__tokens), get_pre_comment(ctx, self._CommentCollectorVisitor__tokens),
         get_in_comments(ctx, self._CommentCollectorVisitor__tokens), get_post_comments(ctx, self._CommentCollectorVisitor__tokens))

    def visitInputPort(self, ctx):
        return (
         get_comments(ctx, self._CommentCollectorVisitor__tokens), get_pre_comment(ctx, self._CommentCollectorVisitor__tokens),
         get_in_comments(ctx, self._CommentCollectorVisitor__tokens), get_post_comments(ctx, self._CommentCollectorVisitor__tokens))

    def visitDeclaration(self, ctx):
        return (
         get_comments(ctx, self._CommentCollectorVisitor__tokens), get_pre_comment(ctx, self._CommentCollectorVisitor__tokens),
         get_in_comments(ctx, self._CommentCollectorVisitor__tokens), get_post_comments(ctx, self._CommentCollectorVisitor__tokens))

    def visitAssignment(self, ctx):
        return (
         get_comments(ctx, self._CommentCollectorVisitor__tokens), get_pre_comment(ctx, self._CommentCollectorVisitor__tokens),
         get_in_comments(ctx, self._CommentCollectorVisitor__tokens), get_post_comments(ctx, self._CommentCollectorVisitor__tokens))

    def visitUpdateBlock(self, ctx):
        return (
         get_comments(ctx, self._CommentCollectorVisitor__tokens), get_pre_comment(ctx, self._CommentCollectorVisitor__tokens),
         get_in_comments(ctx, self._CommentCollectorVisitor__tokens), get_post_comments(ctx, self._CommentCollectorVisitor__tokens))

    def visitEquationsBlock(self, ctx):
        return (
         get_comments(ctx, self._CommentCollectorVisitor__tokens), get_pre_comment(ctx, self._CommentCollectorVisitor__tokens),
         get_in_comments(ctx, self._CommentCollectorVisitor__tokens), get_post_comments(ctx, self._CommentCollectorVisitor__tokens))

    def visitInputBlock(self, ctx):
        return (
         get_comments(ctx, self._CommentCollectorVisitor__tokens), get_pre_comment(ctx, self._CommentCollectorVisitor__tokens),
         get_in_comments(ctx, self._CommentCollectorVisitor__tokens), get_post_comments(ctx, self._CommentCollectorVisitor__tokens))

    def visitOutputBlock(self, ctx):
        return (
         get_comments(ctx, self._CommentCollectorVisitor__tokens), get_pre_comment(ctx, self._CommentCollectorVisitor__tokens),
         get_in_comments(ctx, self._CommentCollectorVisitor__tokens), get_post_comments(ctx, self._CommentCollectorVisitor__tokens))

    def visitFunctionCall(self, ctx):
        return (
         get_comments(ctx, self._CommentCollectorVisitor__tokens), get_pre_comment(ctx, self._CommentCollectorVisitor__tokens),
         get_in_comments(ctx, self._CommentCollectorVisitor__tokens), get_post_comments(ctx, self._CommentCollectorVisitor__tokens))

    def visitFunction(self, ctx):
        return (
         get_comments(ctx, self._CommentCollectorVisitor__tokens), get_pre_comment(ctx, self._CommentCollectorVisitor__tokens),
         get_in_comments(ctx, self._CommentCollectorVisitor__tokens), get_post_comments(ctx, self._CommentCollectorVisitor__tokens))

    def visitForStmt(self, ctx):
        return (
         get_comments(ctx, self._CommentCollectorVisitor__tokens), get_pre_comment(ctx, self._CommentCollectorVisitor__tokens),
         get_in_comments(ctx, self._CommentCollectorVisitor__tokens), get_post_comments(ctx, self._CommentCollectorVisitor__tokens))

    def visitWhileStmt(self, ctx):
        return (
         get_comments(ctx, self._CommentCollectorVisitor__tokens), get_pre_comment(ctx, self._CommentCollectorVisitor__tokens),
         get_in_comments(ctx, self._CommentCollectorVisitor__tokens), get_post_comments(ctx, self._CommentCollectorVisitor__tokens))

    def visitIfClause(self, ctx):
        temp = list()
        temp.extend(get_pre_comment(ctx, self._CommentCollectorVisitor__tokens))
        temp.append(get_in_comments(ctx, self._CommentCollectorVisitor__tokens))
        return (
         temp, get_pre_comment(ctx, self._CommentCollectorVisitor__tokens),
         get_in_comments(ctx, self._CommentCollectorVisitor__tokens), list())

    def visitElifClause(self, ctx):
        temp = get_in_comments(ctx, self._CommentCollectorVisitor__tokens)
        if temp is None:
            temp = list()
        else:
            temp = list(temp)
        return (temp, list(), get_in_comments(ctx, self._CommentCollectorVisitor__tokens),
         list())

    def visitElseClause(self, ctx):
        temp = get_in_comments(ctx, self._CommentCollectorVisitor__tokens)
        if temp is None:
            temp = list()
        else:
            temp = list(temp)
        return (
         temp, list(), get_in_comments(ctx, self._CommentCollectorVisitor__tokens),
         get_post_comments(ctx, self._CommentCollectorVisitor__tokens))


def get_comments(ctx, tokens):
    """
    Returns all previously, in-line and pos comments.
    :param ctx: a context
    :type ctx: ctx
    :param tokens: list of token objects
    :type tokens: list(Tokens)
    :return: a list of comments
    :rtype: list(str)
    """
    ret = list()
    pre_comments = get_pre_comment(ctx, tokens)
    in_comment = get_in_comments(ctx, tokens)
    post_comments = get_post_comments(ctx, tokens)
    if pre_comments is not None:
        ret.extend(pre_comments)
    if in_comment is not None:
        ret.append(in_comment)
    if post_comments is not None:
        ret.extend(post_comments)
    return ret


def get_pre_comment(ctx, tokens):
    """
    Returns the comment which has been stated before this element but also before the next previous token.
    :param ctx: a context
    :type ctx: ctx
    :param tokens: list of token objects
    :type tokens: list(Tokens)
    :return: the corresponding comment or None
    :rtype: str
    """
    comments = list()
    empty_before = __no_definitions_before(ctx, tokens)
    eol = False
    temp = None
    for possibleCommentToken in reversed(tokens[0:tokens.index(ctx.start)]):
        if possibleCommentToken.channel == 0:
            break
        if possibleCommentToken.channel == 2:
            temp = replace_delimiters(possibleCommentToken.text)
            eol = False
        if possibleCommentToken.channel == 1:
            continue
        elif eol and not empty_before:
            break
        if possibleCommentToken.channel == 3:
            if temp is not None:
                comments.append(temp)
            eol = True
            continue

    if empty_before and temp is not None and temp not in comments:
        comments.append(temp)
    if len(comments) > 0:
        return list(reversed(comments))
    return list()


def __no_definitions_before(ctx, tokens):
    """
    This method indicates whether before the start of ctx, something has been defined, e.g. a different neuron.
    This method is used to identify the start of a model.
    :param ctx: a context
    :type ctx: ctx
    :param tokens: list of token objects
    :type tokens: list(Tokens)
    :return: True if nothing defined before, otherwise False.
    :rtype: bool
    """
    for token in tokens[0:tokens.index(ctx.start)]:
        if token.channel == 0:
            return False

    return True


def get_in_comments(ctx, tokens):
    """
    Returns the sole comment if one is defined in the same line, e.g. function a mV = 10mV # comment
    :param ctx: a context
    :type ctx: ctx
    :param tokens: list of token objects
    :type tokens: list(Tokens)
    :return: a comment
    :rtype: str
    """
    for possibleComment in tokens[tokens.index(ctx.start):]:
        if possibleComment.channel == 2:
            return replace_delimiters(possibleComment.text)
        if possibleComment.channel == 3:
            break


def get_post_comments(ctx, tokens):
    """
    Returns the comment which has been stated after the current token but in the same line.
    :param ctx: a context
    :type ctx: ctx
    :param tokens: list of token objects
    :type tokens: list(Tokens)
    :return: the corresponding comment or None
    :rtype: str
    """
    comments = list()
    next_line_start_index = -1
    for possibleToken in tokens[tokens.index(ctx.stop) + 1:]:
        if possibleToken.channel == 3:
            next_line_start_index = tokens.index(possibleToken)
            break

    first_line = False
    for possibleCommentToken in tokens[next_line_start_index:]:
        if possibleCommentToken.channel == 2:
            comments.append(replace_delimiters(possibleCommentToken.text))
            first_line = False
        if possibleCommentToken.channel == 3 and first_line:
            break
        elif possibleCommentToken.channel == 3:
            first_line = True
        if possibleCommentToken.channel == 0:
            break

    if len(comments) > 0:
        return comments
    return list()


def replace_delimiters(comment):
    '''
    Returns the raw comment, i.e., without the comment-tags /* ..*/, """ """ and #
    '''
    ret = comment
    ret = ret.replace('/*', '').replace('*/', '')
    ret = ret.replace('"""', '')
    return ret.replace('#', '')