# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /local_home/weigl/.virtualenvs/msml_env/lib/python2.7/site-packages/clictk/argparseutil.py
# Compiled at: 2015-06-12 16:52:08
from __future__ import absolute_import
from argparse import ArgumentParser

def prettify(elem):
    """Return a pretty-printed XML string for the Element.
    """
    from xml.etree import ElementTree
    return ElementTree.tostring(elem, 'utf-8')


def build_argument_parser(executable):
    """creates an argument parser from the given `executable` model.

    An argument '__xml__' for "--xml" is added independently.

    :param executable: CLI Model
    :type executable: clictk.model.Executable
    :return:
    """
    a = ArgumentParser()
    a.add_argument('--xml', action='store_true', dest='__xml__', help='show cli xml')
    for p in executable:
        o = []
        if p.flag:
            o.append('-%s' % p.flag)
        if p.longflag:
            o.append('--%s' % p.longflag)
        a.add_argument(metavar=p.type.upper(), dest=p.name, action='store', help=(p.description.strip() or 'parameter %s' % p.name), *o)

    return a


def cmdline(executable):
    """Generates a valid command line call for the executable given by call arguments in `kwargs`
    :param kwargs: values to call the executable
    :return: the command line
    :rtype: list
    """
    args = [
     executable.executable]
    indexed_args = []
    for parameter in executable:
        optional = parameter.type == 'boolean' or parameter.default
        has_value = parameter.type != 'boolean'
        if parameter.longflag:
            flag = '--%s' % parameter.longflag
        elif parameter.flag:
            flag = '-%s VALUE' % parameter.flag
        elif parameter.index:
            flag = parameter.name
            optional = False
        if has_value:
            flag += ' VALUE'
        if optional:
            flag = '[' + flag + ']'
        if parameter.index:
            indexed_args.insert(int(parameter.index), flag)
        else:
            args.append(flag)

    return args + indexed_args


def build_docopt(executable, header=''):
    help = header
    help += '\nUsage:\n  '
    help += (' ').join(map(str, cmdline(executable)))
    help += '\n'
    help += '\nOptions:\n'
    for group in executable.parameter_groups:
        help += group.label + '\n'
        dirty = False
        for parameter in group:
            if parameter.flag:
                help += '-%s' % parameter.flag
                dirty = True
            if parameter.longflag:
                if dirty:
                    help += ', '
                help += '--%s' % parameter.longflag
            help += '\t\t %s\n' % parameter.description

        help += '\n\n'

    return help