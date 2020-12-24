# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nico/computer/venv/lib/python3.4/site-packages/bass/__init__.py
# Compiled at: 2015-09-06 05:31:09
# Size of source mod 2**32: 1147 bytes
"""
Bass
-----
Bass is a tool for building static web sites.
Wok, Wintersmith, Pelican and StrangeCase served as sources of inspiration.
Markdown, RestructuredText and Textile are used for lightweight page markup.
Chameleon is used for templating, but other template engines can be added.

Functions:
    - parse_cmdline: parse command line, return parsed argument list
    - build_site: build new site from content and layout directories
    - create_project: create new project with default configuration
    - http_server: simple HTTP server, for development and testing
    - add_handler: add event handler
    - copy_handler: copy event handler
    - remove_handler: remove event handler
    - add_template_type: add template type (template factory + extension)
    - copy_template_type: copy template type (existing template factory + new extension)
"""
from .config import parse_cmdline
from .event import add_toc, add_handler, copy_handler, remove_handler, resolve_idref
from .layout import add_template_type, copy_template_type
from .server import http_server
from .setting import version
from .site import build_site, create_project