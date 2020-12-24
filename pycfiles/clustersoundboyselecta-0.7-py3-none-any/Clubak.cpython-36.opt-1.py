# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /ClusterShell/CLI/Clubak.py
# Compiled at: 2019-12-07 15:34:33
# Size of source mod 2**32: 6857 bytes
__doc__ = '\nformat dsh/pdsh-like output for humans and more\n\nFor help, type::\n    $ clubak --help\n'
from __future__ import print_function
import sys
from ClusterShell.MsgTree import MsgTree, MODE_DEFER, MODE_TRACE
from ClusterShell.NodeSet import NodeSet, NodeSetParseError, std_group_resolver
from ClusterShell.NodeSet import set_std_group_resolver_config
from ClusterShell.CLI.Display import Display, THREE_CHOICES
from ClusterShell.CLI.Display import sys_stdin, sys_stdout
from ClusterShell.CLI.Error import GENERIC_ERRORS, handle_generic_error
from ClusterShell.CLI.OptionParser import OptionParser
from ClusterShell.CLI.Utils import nodeset_cmpkey

def display_tree(tree, disp, out):
    """display sub-routine for clubak -T (msgtree trace mode)"""
    togh = True
    offset = 2
    reldepth = -offset
    reldepths = {}
    line_mode = disp.line_mode
    for msgline, keys, depth, nchildren in tree.walk_trace():
        if togh:
            if depth in reldepths:
                reldepth = reldepths[depth]
            else:
                reldepth = reldepths[depth] = reldepth + offset
            nodeset = NodeSet.fromlist(keys)
            if line_mode:
                out.write(str(nodeset).encode() + ':\n')
            else:
                out.write(disp.format_header(nodeset, reldepth))
        out.write(' ' * reldepth + msgline + '\n')
        togh = nchildren != 1


def display(tree, disp, gather, trace_mode, enable_nodeset_key):
    """nicely display MsgTree instance `tree' content according to
    `disp' Display object and `gather' boolean flag"""
    out = sys_stdout()
    try:
        if trace_mode:
            display_tree(tree, disp, out)
        else:
            if gather:
                if enable_nodeset_key:
                    ns_getter = lambda x: NodeSet.fromlist(x[1])
                    for nodeset in sorted((ns_getter(item) for item in tree.walk()), key=nodeset_cmpkey):
                        disp.print_gather(nodeset, tree[nodeset[0]])

                else:
                    for msg, key in tree.walk():
                        disp.print_gather_keys(key, msg)

            else:
                if enable_nodeset_key:
                    for node in NodeSet.fromlist(tree.keys()).nsiter():
                        disp.print_gather(node, tree[str(node)])

                else:
                    for key in tree.keys():
                        disp.print_gather_keys([key], tree[key])

    finally:
        out.flush()


def clubak():
    """script subroutine"""
    parser = OptionParser('%prog [options]')
    parser.install_groupsconf_option()
    parser.install_display_options(verbose_options=True, separator_option=True,
      dshbak_compat=True,
      msgtree_mode=True)
    options = parser.parse_args()[0]
    set_std_group_resolver_config(options.groupsconf)
    if options.interpret_keys == THREE_CHOICES[(-1)]:
        enable_nodeset_key = None
    else:
        enable_nodeset_key = options.interpret_keys == THREE_CHOICES[1]
    if options.trace_mode:
        tree_mode = MODE_TRACE
    else:
        tree_mode = MODE_DEFER
    tree = MsgTree(mode=tree_mode)
    fast_mode = options.fast_mode
    if fast_mode:
        if tree_mode != MODE_DEFER or options.line_mode:
            parser.error('incompatible tree options')
        preload_msgs = {}
    separator = options.separator.encode()
    for line in sys_stdin():
        try:
            linestripped = line.rstrip('\r\n')
            if options.verbose or options.debug:
                sys_stdout().write('INPUT ' + linestripped + '\n')
            key, content = linestripped.split(separator, 1)
            key = key.strip().decode()
            if not key:
                raise ValueError('no node found')
            if enable_nodeset_key is False:
                keyset = [
                 key]
            else:
                try:
                    keyset = NodeSet(key)
                except NodeSetParseError:
                    if enable_nodeset_key:
                        raise
                    enable_nodeset_key = False
                    keyset = [key]

                if fast_mode:
                    for node in keyset:
                        preload_msgs.setdefault(node, []).append(content)

                else:
                    for node in keyset:
                        tree.add(node, content)

        except ValueError as ex:
            raise ValueError('%s: "%s"' % (ex, linestripped.decode()))

    if fast_mode:
        for key, wholemsg in preload_msgs.items():
            tree.add(key, '\n'.join(wholemsg))

    try:
        disp = Display(options)
    except ValueError as exc:
        parser.error('option mismatch (%s)' % exc)
        return

    if options.debug:
        std_group_resolver().set_verbosity(1)
        print(('clubak: line_mode=%s gather=%s tree_depth=%d' % (
         bool(options.line_mode), bool(disp.gather), tree._depth())),
          file=(sys.stderr))
    display(tree, disp, disp.gather or disp.regroup, options.trace_mode, enable_nodeset_key is not False)


def main():
    """main script function"""
    try:
        clubak()
    except GENERIC_ERRORS as ex:
        sys.exit(handle_generic_error(ex))
    except ValueError as ex:
        print(('%s:' % sys.argv[0]), ex, file=(sys.stderr))
        sys.exit(1)

    sys.exit(0)


if __name__ == '__main__':
    main()