# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ajdiaz/env/mico/lib/python2.7/site-packages/mico/lib/core/ulimit.py
# Compiled at: 2013-05-20 13:32:09
"""The ulimit core submodule provide a useful way to manage system
ulimits."""

def ulimit_ensure(limits):
    """Ensure user limits.

    Example::

        ulimit_ensure("@root hard nproc 1024")
        ulimit_ensure([
            "@root hard nproc 1024",
            "@root soft nproc 1024"
        ])
    """
    if isinstance(limits, str):
        limits = limits.split('\n')
    limits = map(lambda x: (' ').join(x.split()), limits)
    for limit in limits:
        _x = run("sed 's:[ \\t][ \\t]*: :g' /etc/security/limits.conf " + "| grep '%s' || ( echo '%s' >> /etc/security/limits.conf; )" % (limit, limit))