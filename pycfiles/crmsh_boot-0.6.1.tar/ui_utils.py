# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/lib/python2.7/site-packages/crmsh/ui_utils.py
# Compiled at: 2016-05-04 07:56:27
import re, inspect
from .msg import bad_usage, common_err
from . import utils

def _get_attr_cmd(attr_ext_commands, subcmd):
    try:
        attr_cmd = attr_ext_commands[subcmd]
        if attr_cmd:
            return attr_cmd
    except KeyError as msg:
        raise ValueError(msg)

    raise ValueError('Bad attr_cmd ' + repr(attr_ext_commands))


def _dispatch_attr_cmd(cmd, attr_cmd, rsc, subcmd, attr, value):

    def sanity_check(arg):
        if not utils.is_name_sane(arg):
            raise ValueError("Expected valid name, got '%s'" % arg)

    if subcmd == 'set':
        if value is None:
            raise ValueError('Missing value argument to set')
        sanity_check(rsc)
        sanity_check(attr)
        sanity_check(value)
        return utils.ext_cmd(attr_cmd % (rsc, attr, value)) == 0
    else:
        if subcmd in ('delete', 'show') or cmd == 'secret' and subcmd in ('stash',
                                                                          'unstash',
                                                                          'check'):
            if value is not None:
                raise ValueError('Too many arguments to %s' % subcmd)
            sanity_check(rsc)
            sanity_check(attr)
            return utils.ext_cmd(attr_cmd % (rsc, attr)) == 0
        raise ValueError('Unknown command ' + repr(subcmd))
        return


def manage_attr(cmd, attr_ext_commands, rsc, subcmd, attr, value):
    """
    TODO: describe.
    """
    try:
        attr_cmd = _get_attr_cmd(attr_ext_commands, subcmd)
        return _dispatch_attr_cmd(cmd, attr_cmd, rsc, subcmd, attr, value)
    except ValueError as msg:
        cmdline = [
         rsc, subcmd, attr]
        if value is not None:
            cmdline.append(value)
        bad_usage(cmd, (' ').join(cmdline), msg)
        return False

    return


def ptestlike(simfun, def_verb, cmd, args):
    verbosity = def_verb
    nograph = False
    scores = False
    utilization = False
    actions = False
    for p in args:
        if p == 'nograph':
            nograph = True
        elif p == 'scores':
            scores = True
        elif p == 'utilization':
            utilization = True
        elif p == 'actions':
            actions = True
        elif re.match('^vv*$', p):
            verbosity = p
        else:
            bad_usage(cmd, (' ').join(args))
            return False

    return simfun(nograph, scores, utilization, actions, verbosity)


def graph_args(args):
    """
    Common parameters for two graph commands:
        configure graph [<gtype> [<file> [<img_format>]]]
        history graph <pe> [<gtype> [<file> [<img_format>]]]
    """
    from .crm_gv import gv_types
    gtype, outf, ftype = (None, None, None)
    try:
        gtype = args[0]
        if gtype not in gv_types:
            common_err('graph type %s is not supported' % gtype)
            return (
             False, gtype, outf, ftype)
    except:
        gtype = 'dot'

    try:
        outf = args[1]
        if not utils.is_path_sane(outf):
            return (False, gtype, outf, ftype)
    except:
        outf = None

    try:
        ftype = args[2]
    except:
        ftype = gtype

    return (True, gtype, outf, ftype)


def pretty_arguments(f, nskip=0):
    """
    Returns a prettified representation
    of the command arguments
    """
    specs = inspect.getargspec(f)
    named_args = []
    if specs.defaults is None:
        named_args += specs.args
    else:
        named_args += specs.args[:-len(specs.defaults)]
        named_args += [ '[%s]' % a for a in specs.args[-len(specs.defaults):] ]
    if specs.varargs:
        named_args += ['[%s ...]' % specs.varargs]
    if nskip:
        named_args = named_args[nskip:]
    return (' ').join(named_args)


def validate_arguments(f, args, nskip=0):
    """
    Compares the declared arguments of f to
    the given arguments in args, and raises
    ValueError if the arguments don't match.

    nskip: When reporting an error, skip these
    many initial arguments when counting.
    For example, pass 1 to not count self on a
    method.

    Note: Does not support keyword arguments.
    """
    specs = inspect.getargspec(f)
    min_args = len(specs.args)
    if specs.defaults is not None:
        min_args -= len(specs.defaults)
    max_args = len(specs.args)
    if specs.varargs:
        max_args = -1

    def mknamed():
        return pretty_arguments(f, nskip=nskip)

    if min_args == max_args and len(args) != min_args:
        raise ValueError('Expected (%s), takes exactly %d arguments (%d given)' % (
         mknamed(), min_args - nskip, len(args) - nskip))
    elif len(args) < min_args:
        raise ValueError('Expected (%s), takes at least %d arguments (%d given)' % (
         mknamed(), min_args - nskip, len(args) - nskip))
    if max_args >= 0 and len(args) > max_args:
        raise ValueError('Expected (%s), takes at most %d arguments (%d given)' % (
         mknamed(), max_args - nskip, len(args) - nskip))
    return