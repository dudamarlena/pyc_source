# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ziirish/workspace/burp-ui/burpui/misc/parser/burp2.py
# Compiled at: 2016-11-24 08:46:05
"""
.. module:: burpui.misc.parser.burp2
    :platform: Unix
    :synopsis: Burp-UI configuration file parser for Burp2.
.. moduleauthor:: Ziirish <hi+burpui@ziirish.me>
"""
from .burp1 import Parser as Burp1

def __(string):
    """dummy function to fake the translation"""
    return string


class Parser(Burp1):
    """Extends :class:`burpui.misc.parser.burp1.Parser`"""
    pver = 2
    multi_srv = Burp1.multi_srv + [
     'label']
    string_srv = Burp1.string_srv + [
     'manual_delete']
    boolean_add = [
     'acl',
     'xattr',
     'server_can_override_includes',
     'glob_after_script_pre',
     'cname_fqdn',
     'cname_lowercase']
    boolean_add_cli = [
     'enabled']
    boolean_srv = Burp1.boolean_srv + boolean_add
    boolean_cli = Burp1.boolean_cli + boolean_add + boolean_add_cli
    multi_cli = Burp1.multi_cli + [
     'label']
    integer_cli = Burp1.integer_cli + [
     'randomise']
    fields_cli = Burp1.fields_cli + boolean_add + boolean_add_cli + [
     'randomise',
     'manual_delete',
     'label']
    placeholders = Burp1.placeholders
    placeholders.update({'acl': '0|1', 
       'xattr': '0|1', 
       'randomise': __('max secs'), 
       'manual_delete': __('path'), 
       'label': __('some informations'), 
       'server_can_override_includes': '0|1', 
       'glob_after_script_pre': '0|1', 
       'enabled': '0|1', 
       'cname_fqdn': '0|1', 
       'cname_lowercase': '0|1'})
    defaults = Burp1.defaults
    defaults.update({'acl': True, 
       'xattr': True, 
       'server_can_override_includes': True, 
       'glob_after_script_pre': True, 
       'randomise': 0, 
       'manual_delete': '', 
       'label': '', 
       'enabled': True, 
       'cname_fqdn': True, 
       'cname_lowercase': False})
    doc = Burp1.doc
    doc.update({'acl': __("If acl support is compiled into burp, this allows you to decide whether or not to backup acls at runtime. The default is '1'."), 
       'xattr': __("If xattr support is compiled into burp, this allows you to decide whether or not to backup xattrs at runtime. The default is '1'."), 
       'randomise': __("When running a timed backup, sleep for a random number of seconds (between 0 and the number given) before contacting the server. Alternatively, this can be specified by the '-q' command line option."), 
       'manual_delete': __("This can be overridden by the clientconfdir configuration files in clientconfdir on the server. When the server needs to delete old backups, or rubble left over from generating reverse patches with librsync=1, it will normally delete them in place. If you use the 'manual_delete' option, the files will be moved to the path specified for deletion at a later point. You will then need to configure a cron job, or similar, to delete the files yourself. Do not specify a path that is not on the same filesystem as the client storage directory."), 
       'label': __('You can have multiple labels, and they can be overridden in the client configuration files in clientconfdir on the server. They will appear as an array of strings in the server status monitor JSON output. The idea is to provide a mechanism for arbitrary values to be passed to clients of the server status monitor.'), 
       'server_can_override_includes': __('To prevent the server from being able to override your local include/exclude list, set this to 0. The default is 1.'), 
       'glob_after_script_pre': __('Set this to 0 if you do not want include_glob settings to be evaluated after the pre script is run. The default is 1.'), 
       'enabled': __('Set this to 0 if you want to disable all clients. The default is 1. This option can be overridden per-client in the client configuration files in clientconfdir on the server.'), 
       'cname_fqdn': __("Whether to keep fqdn cname (like 'testclient.example.com') when looking-up in clientconfdir. This also affects the fqdn lookup on the client (see client configuration options for details). The default is 1. When set to 0, the fqdn provided by the client while authenticating will be stripped ('testclient.example.com' becomes 'testclient')."), 
       'cname_lowercase': __('Whether to force lowercase cname when looking-up in clientconfdir. This also affects the fqdn lookup on the client (see client configuration options for details). The default is 0. When set to 1 the name provided by the client while authenticating will be lowercased.')})