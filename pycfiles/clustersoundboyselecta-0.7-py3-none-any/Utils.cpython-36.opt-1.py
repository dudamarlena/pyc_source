# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /ClusterShell/CLI/Utils.py
# Compiled at: 2019-12-07 15:34:33
# Size of source mod 2**32: 1731 bytes
__doc__ = '\nCLI utility functions\n'
KIBI, MEBI, GIBI, TEBI = (1024.0, 1048576.0, 1073741824.0, 1099511627776.0)

def human_bi_bytes_unit(value):
    """
    Format numerical `value` to display it using human readable unit with
    binary prefix like (KiB, MiB, GiB, ...).
    """
    if value >= TEBI:
        fmt = '%.2f TiB' % (value / TEBI)
    else:
        if value >= GIBI:
            fmt = '%.2f GiB' % (value / GIBI)
        else:
            if value >= MEBI:
                fmt = '%.2f MiB' % (value / MEBI)
            else:
                if value >= KIBI:
                    fmt = '%.2f KiB' % (value / KIBI)
                else:
                    fmt = '%d B' % value
    return fmt


def nodeset_cmpkey(nodeset):
    """We want larger nodeset first, then sorted by first node index."""
    return (
     -len(nodeset), nodeset[0])


def bufnodeset_cmpkey(buf):
    """Helper to get nodeset compare key from a buffer (buf, nodeset)"""
    return nodeset_cmpkey(buf[1])