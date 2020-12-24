# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./dploy/__init__.py
# Compiled at: 2017-03-16 01:16:27
"""
dploy script is an attempt at creating a clone of GNU stow that will work on
Windows as well as *nix
"""
import sys
assert sys.version_info >= (3, 3), 'Requires Python 3.3 or Greater'
import dploy.linkcmd as linkcmd, dploy.stowcmd as stowcmd

def stow(sources, dest, is_silent=True, is_dry_run=False, ignore_patterns=None):
    """
    sub command stow
    """
    stowcmd.Stow(sources, dest, is_silent, is_dry_run, ignore_patterns)


def unstow(sources, dest, is_silent=True, is_dry_run=False, ignore_patterns=None):
    """
    sub command unstow
    """
    stowcmd.UnStow(sources, dest, is_silent, is_dry_run, ignore_patterns)


def link(source, dest, is_silent=True, is_dry_run=False, ignore_patterns=None):
    """
    sub command link
    """
    linkcmd.Link(source, dest, is_silent, is_dry_run, ignore_patterns)