# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/linseed/format.py
# Compiled at: 2011-01-16 05:29:27


def format(snapshot, fmt):
    """Fill in a format string with values taken from a Snapshot.

    Essentially, this calls::

      fmt.format(
        source_name1 = snapshot["source_name1"].display(),
        source_name2 = snapshot["source_name2"].display(),
        ...
        source_nameN = snapshot["source_nameN"].display())

    Where the various "source_nameXXX" values are taken from the keys
    of `snapshot`.

    In other words, if `fmt` was:
    
      {linseed_cpus}, {linseed_batteries}

    then this would do standard string formatting and replace the
    {...} placeholders with values taken from the snapshot, resulting
    in something like:

      CPU: 10%, Batt: 76%-

    Args:
      * snapshot: A Snapshot object whose values will be used to
          process the format string.
      * fmt: The format string to interpolate.

    Returns:
      The format string with its values filled in.
    """
    args = (',').join([ ('{0} = snapshot["{0}"].display()').format(k) for k in snapshot ])
    cmd = 'fmt.format(' + args + ')'
    return eval(cmd, globals(), locals())