# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-m_4qh6p6/Pygments/pygments/lexers/configs.py
# Compiled at: 2019-07-30 18:47:12
# Size of source mod 2**32: 31855 bytes
"""
    pygments.lexers.configs
    ~~~~~~~~~~~~~~~~~~~~~~~

    Lexers for configuration file formats.

    :copyright: Copyright 2006-2019 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""
import re
from pygments.lexer import RegexLexer, default, words, bygroups, include, using
from pygments.token import Text, Comment, Operator, Keyword, Name, String, Number, Punctuation, Whitespace, Literal
from pygments.lexers.shell import BashLexer
from pygments.lexers.data import JsonLexer
__all__ = [
 'IniLexer', 'RegeditLexer', 'PropertiesLexer', 'KconfigLexer',
 'Cfengine3Lexer', 'ApacheConfLexer', 'SquidConfLexer',
 'NginxConfLexer', 'LighttpdConfLexer', 'DockerLexer',
 'TerraformLexer', 'TermcapLexer', 'TerminfoLexer',
 'PkgConfigLexer', 'PacmanConfLexer', 'AugeasLexer', 'TOMLLexer']

class IniLexer(RegexLexer):
    __doc__ = '\n    Lexer for configuration files in INI style.\n    '
    name = 'INI'
    aliases = ['ini', 'cfg', 'dosini']
    filenames = ['*.ini', '*.cfg', '*.inf']
    mimetypes = ['text/x-ini', 'text/inf']
    tokens = {'root': [
              (
               '\\s+', Text),
              (
               '[;#].*', Comment.Single),
              (
               '\\[.*?\\]$', Keyword),
              (
               '(.*?)([ \\t]*)(=)([ \\t]*)(.*(?:\\n[ \\t].+)*)',
               bygroups(Name.Attribute, Text, Operator, Text, String)),
              (
               '(.+?)$', Name.Attribute)]}

    def analyse_text(text):
        npos = text.find('\n')
        if npos < 3:
            return False
        else:
            return text[0] == '[' and text[(npos - 1)] == ']'


class RegeditLexer(RegexLexer):
    __doc__ = '\n    Lexer for `Windows Registry\n    <http://en.wikipedia.org/wiki/Windows_Registry#.REG_files>`_ files produced\n    by regedit.\n\n    .. versionadded:: 1.6\n    '
    name = 'reg'
    aliases = ['registry']
    filenames = ['*.reg']
    mimetypes = ['text/x-windows-registry']
    tokens = {'root':[
      (
       'Windows Registry Editor.*', Text),
      (
       '\\s+', Text),
      (
       '[;#].*', Comment.Single),
      (
       '(\\[)(-?)(HKEY_[A-Z_]+)(.*?\\])$',
       bygroups(Keyword, Operator, Name.Builtin, Keyword)),
      (
       '("(?:\\\\"|\\\\\\\\|[^"])+")([ \\t]*)(=)([ \\t]*)',
       bygroups(Name.Attribute, Text, Operator, Text),
       'value'),
      (
       '(.*?)([ \\t]*)(=)([ \\t]*)',
       bygroups(Name.Attribute, Text, Operator, Text),
       'value')], 
     'value':[
      (
       '-', Operator, '#pop'),
      (
       '(dword|hex(?:\\([0-9a-fA-F]\\))?)(:)([0-9a-fA-F,]+)',
       bygroups(Name.Variable, Punctuation, Number), '#pop'),
      (
       '.+', String, '#pop'),
      default('#pop')]}

    def analyse_text(text):
        return text.startswith('Windows Registry Editor')


class PropertiesLexer(RegexLexer):
    __doc__ = "\n    Lexer for configuration files in Java's properties format.\n\n    Note: trailing whitespace counts as part of the value as per spec\n\n    .. versionadded:: 1.4\n    "
    name = 'Properties'
    aliases = ['properties', 'jproperties']
    filenames = ['*.properties']
    mimetypes = ['text/x-java-properties']
    tokens = {'root': [
              (
               '^(\\w+)([ \\t])(\\w+\\s*)$', bygroups(Name.Attribute, Text, String)),
              (
               '^\\w+(\\\\[ \\t]\\w*)*$', Name.Attribute),
              (
               '(^ *)([#!].*)', bygroups(Text, Comment)),
              (
               '(^ *)((?:;|//).*)', bygroups(Text, Comment)),
              (
               '(.*?)([ \\t]*)([=:])([ \\t]*)(.*(?:(?<=\\\\)\\n.*)*)',
               bygroups(Name.Attribute, Text, Operator, Text, String)),
              (
               '\\s', Text)]}


def _rx_indent(level):
    tab_width = 8
    if tab_width == 2:
        space_repeat = '+'
    else:
        space_repeat = '{1,%d}' % (tab_width - 1)
    if level == 1:
        level_repeat = ''
    else:
        level_repeat = '{%s}' % level
    return '(?:\\t| %s\\t| {%s})%s.*\\n' % (space_repeat, tab_width, level_repeat)


class KconfigLexer(RegexLexer):
    __doc__ = '\n    For Linux-style Kconfig files.\n\n    .. versionadded:: 1.6\n    '
    name = 'Kconfig'
    aliases = ['kconfig', 'menuconfig', 'linux-config', 'kernel-config']
    filenames = [
     'Kconfig', '*Config.in*', 'external.in*',
     'standard-modules.in']
    mimetypes = ['text/x-kconfig']
    flags = 0

    def call_indent(level):
        return (
         _rx_indent(level), String.Doc, 'indent%s' % level)

    def do_indent(level):
        return [
         (
          _rx_indent(level), String.Doc),
         (
          '\\s*\\n', Text),
         default('#pop:2')]

    tokens = {'root':[
      (
       '\\s+', Text),
      (
       '#.*?\\n', Comment.Single),
      (
       words(('mainmenu', 'config', 'menuconfig', 'choice', 'endchoice', 'comment', 'menu',
       'endmenu', 'visible if', 'if', 'endif', 'source', 'prompt', 'select', 'depends on',
       'default', 'range', 'option'),
         suffix='\\b'),
       Keyword),
      (
       '(---help---|help)[\\t ]*\\n', Keyword, 'help'),
      (
       '(bool|tristate|string|hex|int|defconfig_list|modules|env)\\b',
       Name.Builtin),
      (
       '[!=&|]', Operator),
      (
       '[()]', Punctuation),
      (
       '[0-9]+', Number.Integer),
      (
       "'(''|[^'])*'", String.Single),
      (
       '"(""|[^"])*"', String.Double),
      (
       '\\S+', Text)], 
     'help':[
      (
       '\\s*\\n', Text),
      call_indent(7),
      call_indent(6),
      call_indent(5),
      call_indent(4),
      call_indent(3),
      call_indent(2),
      call_indent(1),
      default('#pop')], 
     'indent7':do_indent(7), 
     'indent6':do_indent(6), 
     'indent5':do_indent(5), 
     'indent4':do_indent(4), 
     'indent3':do_indent(3), 
     'indent2':do_indent(2), 
     'indent1':do_indent(1)}


class Cfengine3Lexer(RegexLexer):
    __doc__ = '\n    Lexer for `CFEngine3 <http://cfengine.org>`_ policy files.\n\n    .. versionadded:: 1.5\n    '
    name = 'CFEngine3'
    aliases = ['cfengine3', 'cf3']
    filenames = ['*.cf']
    mimetypes = []
    tokens = {'root':[
      (
       '#.*?\\n', Comment),
      (
       '(body)(\\s+)(\\S+)(\\s+)(control)',
       bygroups(Keyword, Text, Keyword, Text, Keyword)),
      (
       '(body|bundle)(\\s+)(\\S+)(\\s+)(\\w+)(\\()',
       bygroups(Keyword, Text, Keyword, Text, Name.Function, Punctuation),
       'arglist'),
      (
       '(body|bundle)(\\s+)(\\S+)(\\s+)(\\w+)',
       bygroups(Keyword, Text, Keyword, Text, Name.Function)),
      (
       '(")([^"]+)(")(\\s+)(string|slist|int|real)(\\s*)(=>)(\\s*)',
       bygroups(Punctuation, Name.Variable, Punctuation, Text, Keyword.Type, Text, Operator, Text)),
      (
       '(\\S+)(\\s*)(=>)(\\s*)',
       bygroups(Keyword.Reserved, Text, Operator, Text)),
      (
       '"', String, 'string'),
      (
       '(\\w+)(\\()', bygroups(Name.Function, Punctuation)),
      (
       '([\\w.!&|()]+)(::)', bygroups(Name.Class, Punctuation)),
      (
       '(\\w+)(:)', bygroups(Keyword.Declaration, Punctuation)),
      (
       '@[{(][^)}]+[})]', Name.Variable),
      (
       '[(){},;]', Punctuation),
      (
       '=>', Operator),
      (
       '->', Operator),
      (
       '\\d+\\.\\d+', Number.Float),
      (
       '\\d+', Number.Integer),
      (
       '\\w+', Name.Function),
      (
       '\\s+', Text)], 
     'string':[
      (
       '\\$[{(]', String.Interpol, 'interpol'),
      (
       '\\\\.', String.Escape),
      (
       '"', String, '#pop'),
      (
       '\\n', String),
      (
       '.', String)], 
     'interpol':[
      (
       '\\$[{(]', String.Interpol, '#push'),
      (
       '[})]', String.Interpol, '#pop'),
      (
       '[^${()}]+', String.Interpol)], 
     'arglist':[
      (
       '\\)', Punctuation, '#pop'),
      (
       ',', Punctuation),
      (
       '\\w+', Name.Variable),
      (
       '\\s+', Text)]}


class ApacheConfLexer(RegexLexer):
    __doc__ = '\n    Lexer for configuration files following the Apache config file\n    format.\n\n    .. versionadded:: 0.6\n    '
    name = 'ApacheConf'
    aliases = ['apacheconf', 'aconf', 'apache']
    filenames = ['.htaccess', 'apache.conf', 'apache2.conf']
    mimetypes = ['text/x-apacheconf']
    flags = re.MULTILINE | re.IGNORECASE
    tokens = {'root':[
      (
       '\\s+', Text),
      (
       '(#.*?)$', Comment),
      (
       '(<[^\\s>]+)(?:(\\s+)(.*))?(>)',
       bygroups(Name.Tag, Text, String, Name.Tag)),
      (
       '([a-z]\\w*)(\\s+)',
       bygroups(Name.Builtin, Text), 'value'),
      (
       '\\.+', Text)], 
     'value':[
      (
       '\\\\\\n', Text),
      (
       '$', Text, '#pop'),
      (
       '\\\\', Text),
      (
       '[^\\S\\n]+', Text),
      (
       '\\d+\\.\\d+\\.\\d+\\.\\d+(?:/\\d+)?', Number),
      (
       '\\d+', Number),
      (
       '/([a-z0-9][\\w./-]+)', String.Other),
      (
       '(on|off|none|any|all|double|email|dns|min|minimal|os|productonly|full|emerg|alert|crit|error|warn|notice|info|debug|registry|script|inetd|standalone|user|group)\\b',
       Keyword),
      (
       '"([^"\\\\]*(?:\\\\.[^"\\\\]*)*)"', String.Double),
      (
       '[^\\s"\\\\]+', Text)]}


class SquidConfLexer(RegexLexer):
    __doc__ = '\n    Lexer for `squid <http://www.squid-cache.org/>`_ configuration files.\n\n    .. versionadded:: 0.9\n    '
    name = 'SquidConf'
    aliases = ['squidconf', 'squid.conf', 'squid']
    filenames = ['squid.conf']
    mimetypes = ['text/x-squidconf']
    flags = re.IGNORECASE
    keywords = ('access_log', 'acl', 'always_direct', 'announce_host', 'announce_period',
                'announce_port', 'announce_to', 'anonymize_headers', 'append_domain',
                'as_whois_server', 'auth_param_basic', 'authenticate_children', 'authenticate_program',
                'authenticate_ttl', 'broken_posts', 'buffered_logs', 'cache_access_log',
                'cache_announce', 'cache_dir', 'cache_dns_program', 'cache_effective_group',
                'cache_effective_user', 'cache_host', 'cache_host_acl', 'cache_host_domain',
                'cache_log', 'cache_mem', 'cache_mem_high', 'cache_mem_low', 'cache_mgr',
                'cachemgr_passwd', 'cache_peer', 'cache_peer_access', 'cahce_replacement_policy',
                'cache_stoplist', 'cache_stoplist_pattern', 'cache_store_log', 'cache_swap',
                'cache_swap_high', 'cache_swap_log', 'cache_swap_low', 'client_db',
                'client_lifetime', 'client_netmask', 'connect_timeout', 'coredump_dir',
                'dead_peer_timeout', 'debug_options', 'delay_access', 'delay_class',
                'delay_initial_bucket_level', 'delay_parameters', 'delay_pools',
                'deny_info', 'dns_children', 'dns_defnames', 'dns_nameservers', 'dns_testnames',
                'emulate_httpd_log', 'err_html_text', 'fake_user_agent', 'firewall_ip',
                'forwarded_for', 'forward_snmpd_port', 'fqdncache_size', 'ftpget_options',
                'ftpget_program', 'ftp_list_width', 'ftp_passive', 'ftp_user', 'half_closed_clients',
                'header_access', 'header_replace', 'hierarchy_stoplist', 'high_response_time_warning',
                'high_page_fault_warning', 'hosts_file', 'htcp_port', 'http_access',
                'http_anonymizer', 'httpd_accel', 'httpd_accel_host', 'httpd_accel_port',
                'httpd_accel_uses_host_header', 'httpd_accel_with_proxy', 'http_port',
                'http_reply_access', 'icp_access', 'icp_hit_stale', 'icp_port', 'icp_query_timeout',
                'ident_lookup', 'ident_lookup_access', 'ident_timeout', 'incoming_http_average',
                'incoming_icp_average', 'inside_firewall', 'ipcache_high', 'ipcache_low',
                'ipcache_size', 'local_domain', 'local_ip', 'logfile_rotate', 'log_fqdn',
                'log_icp_queries', 'log_mime_hdrs', 'maximum_object_size', 'maximum_single_addr_tries',
                'mcast_groups', 'mcast_icp_query_timeout', 'mcast_miss_addr', 'mcast_miss_encode_key',
                'mcast_miss_port', 'memory_pools', 'memory_pools_limit', 'memory_replacement_policy',
                'mime_table', 'min_http_poll_cnt', 'min_icp_poll_cnt', 'minimum_direct_hops',
                'minimum_object_size', 'minimum_retry_timeout', 'miss_access', 'negative_dns_ttl',
                'negative_ttl', 'neighbor_timeout', 'neighbor_type_domain', 'netdb_high',
                'netdb_low', 'netdb_ping_period', 'netdb_ping_rate', 'never_direct',
                'no_cache', 'passthrough_proxy', 'pconn_timeout', 'pid_filename',
                'pinger_program', 'positive_dns_ttl', 'prefer_direct', 'proxy_auth',
                'proxy_auth_realm', 'query_icmp', 'quick_abort', 'quick_abort_max',
                'quick_abort_min', 'quick_abort_pct', 'range_offset_limit', 'read_timeout',
                'redirect_children', 'redirect_program', 'redirect_rewrites_host_header',
                'reference_age', 'refresh_pattern', 'reload_into_ims', 'request_body_max_size',
                'request_size', 'request_timeout', 'shutdown_lifetime', 'single_parent_bypass',
                'siteselect_timeout', 'snmp_access', 'snmp_incoming_address', 'snmp_port',
                'source_ping', 'ssl_proxy', 'store_avg_object_size', 'store_objects_per_bucket',
                'strip_query_terms', 'swap_level1_dirs', 'swap_level2_dirs', 'tcp_incoming_address',
                'tcp_outgoing_address', 'tcp_recv_bufsize', 'test_reachability',
                'udp_hit_obj', 'udp_hit_obj_size', 'udp_incoming_address', 'udp_outgoing_address',
                'unique_hostname', 'unlinkd_program', 'uri_whitespace', 'useragent_log',
                'visible_hostname', 'wais_relay', 'wais_relay_host', 'wais_relay_port')
    opts = ('proxy-only', 'weight', 'ttl', 'no-query', 'default', 'round-robin', 'multicast-responder',
            'on', 'off', 'all', 'deny', 'allow', 'via', 'parent', 'no-digest', 'heap',
            'lru', 'realm', 'children', 'q1', 'q2', 'credentialsttl', 'none', 'disable',
            'offline_toggle', 'diskd')
    actions = ('shutdown', 'info', 'parameter', 'server_list', 'client_list', 'squid.conf')
    actions_stats = ('objects', 'vm_objects', 'utilization', 'ipcache', 'fqdncache',
                     'dns', 'redirector', 'io', 'reply_headers', 'filedescriptors',
                     'netdb')
    actions_log = ('status', 'enable', 'disable', 'clear')
    acls = ('url_regex', 'urlpath_regex', 'referer_regex', 'port', 'proto', 'req_mime_type',
            'rep_mime_type', 'method', 'browser', 'user', 'src', 'dst', 'time', 'dstdomain',
            'ident', 'snmp_community')
    ip_re = '(?:(?:(?:[3-9]\\d?|2(?:5[0-5]|[0-4]?\\d)?|1\\d{0,2}|0x0*[0-9a-f]{1,2}|0+[1-3]?[0-7]{0,2})(?:\\.(?:[3-9]\\d?|2(?:5[0-5]|[0-4]?\\d)?|1\\d{0,2}|0x0*[0-9a-f]{1,2}|0+[1-3]?[0-7]{0,2})){3})|(?!.*::.*::)(?:(?!:)|:(?=:))(?:[0-9a-f]{0,4}(?:(?<=::)|(?<!::):)){6}(?:[0-9a-f]{0,4}(?:(?<=::)|(?<!::):)[0-9a-f]{0,4}(?:(?<=::)|(?<!:)|(?<=:)(?<!::):)|(?:25[0-4]|2[0-4]\\d|1\\d\\d|[1-9]?\\d)(?:\\.(?:25[0-4]|2[0-4]\\d|1\\d\\d|[1-9]?\\d)){3}))'
    tokens = {'root':[
      (
       '\\s+', Whitespace),
      (
       '#', Comment, 'comment'),
      (
       words(keywords, prefix='\\b', suffix='\\b'), Keyword),
      (
       words(opts, prefix='\\b', suffix='\\b'), Name.Constant),
      (
       words(actions, prefix='\\b', suffix='\\b'), String),
      (
       words(actions_stats, prefix='stats/', suffix='\\b'), String),
      (
       words(actions_log, prefix='log/', suffix='='), String),
      (
       words(acls, prefix='\\b', suffix='\\b'), Keyword),
      (
       ip_re + '(?:/(?:' + ip_re + '|\\b\\d+\\b))?', Number.Float),
      (
       '(?:\\b\\d+\\b(?:-\\b\\d+|%)?)', Number),
      (
       '\\S+', Text)], 
     'comment':[
      (
       '\\s*TAG:.*', String.Escape, '#pop'),
      (
       '.+', Comment, '#pop'),
      default('#pop')]}


class NginxConfLexer(RegexLexer):
    __doc__ = '\n    Lexer for `Nginx <http://nginx.net/>`_ configuration files.\n\n    .. versionadded:: 0.11\n    '
    name = 'Nginx configuration file'
    aliases = ['nginx']
    filenames = ['nginx.conf']
    mimetypes = ['text/x-nginx-conf']
    tokens = {'root':[
      (
       '(include)(\\s+)([^\\s;]+)', bygroups(Keyword, Text, Name)),
      (
       '[^\\s;#]+', Keyword, 'stmt'),
      include('base')], 
     'block':[
      (
       '\\}', Punctuation, '#pop:2'),
      (
       '[^\\s;#]+', Keyword.Namespace, 'stmt'),
      include('base')], 
     'stmt':[
      (
       '\\{', Punctuation, 'block'),
      (
       ';', Punctuation, '#pop'),
      include('base')], 
     'base':[
      (
       '#.*\\n', Comment.Single),
      (
       'on|off', Name.Constant),
      (
       '\\$[^\\s;#()]+', Name.Variable),
      (
       '([a-z0-9.-]+)(:)([0-9]+)',
       bygroups(Name, Punctuation, Number.Integer)),
      (
       '[a-z-]+/[a-z-+]+', String),
      (
       '[0-9]+[km]?\\b', Number.Integer),
      (
       '(~)(\\s*)([^\\s{]+)', bygroups(Punctuation, Text, String.Regex)),
      (
       '[:=~]', Punctuation),
      (
       '[^\\s;#{}$]+', String),
      (
       '/[^\\s;#]*', Name),
      (
       '\\s+', Text),
      (
       '[$;]', Text)]}


class LighttpdConfLexer(RegexLexer):
    __doc__ = '\n    Lexer for `Lighttpd <http://lighttpd.net/>`_ configuration files.\n\n    .. versionadded:: 0.11\n    '
    name = 'Lighttpd configuration file'
    aliases = ['lighty', 'lighttpd']
    filenames = []
    mimetypes = ['text/x-lighttpd-conf']
    tokens = {'root': [
              (
               '#.*\\n', Comment.Single),
              (
               '/\\S*', Name),
              (
               '[a-zA-Z._-]+', Keyword),
              (
               '\\d+\\.\\d+\\.\\d+\\.\\d+(?:/\\d+)?', Number),
              (
               '[0-9]+', Number),
              (
               '=>|=~|\\+=|==|=|\\+', Operator),
              (
               '\\$[A-Z]+', Name.Builtin),
              (
               '[(){}\\[\\],]', Punctuation),
              (
               '"([^"\\\\]*(?:\\\\.[^"\\\\]*)*)"', String.Double),
              (
               '\\s+', Text)]}


class DockerLexer(RegexLexer):
    __doc__ = '\n    Lexer for `Docker <http://docker.io>`_ configuration files.\n\n    .. versionadded:: 2.0\n    '
    name = 'Docker'
    aliases = ['docker', 'dockerfile']
    filenames = ['Dockerfile', '*.docker']
    mimetypes = ['text/x-dockerfile-config']
    _keywords = '(?:FROM|MAINTAINER|EXPOSE|WORKDIR|USER|STOPSIGNAL)'
    _bash_keywords = '(?:RUN|CMD|ENTRYPOINT|ENV|ARG|LABEL|ADD|COPY)'
    _lb = '(?:\\s*\\\\?\\s*)'
    flags = re.IGNORECASE | re.MULTILINE
    tokens = {'root': [
              (
               '#.*', Comment),
              (
               '(ONBUILD)(%s)' % (_lb,), bygroups(Keyword, using(BashLexer))),
              (
               '(HEALTHCHECK)((%s--\\w+=\\w+%s)*)' % (_lb, _lb),
               bygroups(Keyword, using(BashLexer))),
              (
               '(VOLUME|ENTRYPOINT|CMD|SHELL)(%s)(\\[.*?\\])' % (_lb,),
               bygroups(Keyword, using(BashLexer), using(JsonLexer))),
              (
               '(LABEL|ENV|ARG)((%s\\w+=\\w+%s)*)' % (_lb, _lb),
               bygroups(Keyword, using(BashLexer))),
              (
               '(%s|VOLUME)\\b(.*)' % _keywords, bygroups(Keyword, String)),
              (
               '(%s)' % (_bash_keywords,), Keyword),
              (
               '(.*\\\\\\n)*.+', using(BashLexer))]}


class TerraformLexer(RegexLexer):
    __doc__ = '\n    Lexer for `terraformi .tf files <https://www.terraform.io/>`_.\n\n    .. versionadded:: 2.1\n    '
    name = 'Terraform'
    aliases = ['terraform', 'tf']
    filenames = ['*.tf']
    mimetypes = ['application/x-tf', 'application/x-terraform']
    embedded_keywords = ('ingress', 'egress', 'listener', 'default', 'connection',
                         'alias', 'tags', 'lifecycle', 'timeouts')
    tokens = {'root':[
      include('string'),
      include('punctuation'),
      include('curly'),
      include('basic'),
      include('whitespace'),
      (
       '[0-9]+', Number)], 
     'basic':[
      (
       words(('true', 'false'), prefix='\\b', suffix='\\b'), Keyword.Type),
      (
       '\\s*/\\*', Comment.Multiline, 'comment'),
      (
       '\\s*#.*\\n', Comment.Single),
      (
       '(.*?)(\\s*)(=)', bygroups(Name.Attribute, Text, Operator)),
      (
       words(('variable', 'resource', 'provider', 'provisioner', 'module'), prefix='\\b',
         suffix='\\b'), Keyword.Reserved, 'function'),
      (
       words(embedded_keywords, prefix='\\b', suffix='\\b'), Keyword.Declaration),
      (
       '\\$\\{', String.Interpol, 'var_builtin')], 
     'function':[
      (
       '(\\s+)(".*")(\\s+)', bygroups(Text, String, Text)),
      include('punctuation'),
      include('curly')], 
     'var_builtin':[
      (
       '\\$\\{', String.Interpol, '#push'),
      (
       words(('concat', 'file', 'join', 'lookup', 'element'), prefix='\\b',
         suffix='\\b'), Name.Builtin),
      include('string'),
      include('punctuation'),
      (
       '\\s+', Text),
      (
       '\\}', String.Interpol, '#pop')], 
     'string':[
      (
       '(".*")', bygroups(String.Double))], 
     'punctuation':[
      (
       '[\\[\\](),.]', Punctuation)], 
     'curly':[
      (
       '\\{', Text.Punctuation),
      (
       '\\}', Text.Punctuation)], 
     'comment':[
      (
       '[^*/]', Comment.Multiline),
      (
       '/\\*', Comment.Multiline, '#push'),
      (
       '\\*/', Comment.Multiline, '#pop'),
      (
       '[*/]', Comment.Multiline)], 
     'whitespace':[
      (
       '\\n', Text),
      (
       '\\s+', Text),
      (
       '\\\\\\n', Text)]}


class TermcapLexer(RegexLexer):
    __doc__ = '\n    Lexer for termcap database source.\n\n    This is very simple and minimal.\n\n    .. versionadded:: 2.1\n    '
    name = 'Termcap'
    aliases = ['termcap']
    filenames = ['termcap', 'termcap.src']
    mimetypes = []
    tokens = {'root':[
      (
       '^#.*$', Comment),
      (
       '^[^\\s#:|]+', Name.Tag, 'names')], 
     'names':[
      (
       '\\n', Text, '#pop'),
      (
       ':', Punctuation, 'defs'),
      (
       '\\|', Punctuation),
      (
       '[^:|]+', Name.Attribute)], 
     'defs':[
      (
       '\\\\\\n[ \\t]*', Text),
      (
       '\\n[ \\t]*', Text, '#pop:2'),
      (
       '(#)([0-9]+)', bygroups(Operator, Number)),
      (
       '=', Operator, 'data'),
      (
       ':', Punctuation),
      (
       '[^\\s:=#]+', Name.Class)], 
     'data':[
      (
       '\\\\072', Literal),
      (
       ':', Punctuation, '#pop'),
      (
       '[^:\\\\]+', Literal),
      (
       '.', Literal)]}


class TerminfoLexer(RegexLexer):
    __doc__ = '\n    Lexer for terminfo database source.\n\n    This is very simple and minimal.\n\n    .. versionadded:: 2.1\n    '
    name = 'Terminfo'
    aliases = ['terminfo']
    filenames = ['terminfo', 'terminfo.src']
    mimetypes = []
    tokens = {'root':[
      (
       '^#.*$', Comment),
      (
       '^[^\\s#,|]+', Name.Tag, 'names')], 
     'names':[
      (
       '\\n', Text, '#pop'),
      (
       '(,)([ \\t]*)', bygroups(Punctuation, Text), 'defs'),
      (
       '\\|', Punctuation),
      (
       '[^,|]+', Name.Attribute)], 
     'defs':[
      (
       '\\n[ \\t]+', Text),
      (
       '\\n', Text, '#pop:2'),
      (
       '(#)([0-9]+)', bygroups(Operator, Number)),
      (
       '=', Operator, 'data'),
      (
       '(,)([ \\t]*)', bygroups(Punctuation, Text)),
      (
       '[^\\s,=#]+', Name.Class)], 
     'data':[
      (
       '\\\\[,\\\\]', Literal),
      (
       '(,)([ \\t]*)', bygroups(Punctuation, Text), '#pop'),
      (
       '[^\\\\,]+', Literal),
      (
       '.', Literal)]}


class PkgConfigLexer(RegexLexer):
    __doc__ = '\n    Lexer for `pkg-config\n    <http://www.freedesktop.org/wiki/Software/pkg-config/>`_\n    (see also `manual page <http://linux.die.net/man/1/pkg-config>`_).\n\n    .. versionadded:: 2.1\n    '
    name = 'PkgConfig'
    aliases = ['pkgconfig']
    filenames = ['*.pc']
    mimetypes = []
    tokens = {'root':[
      (
       '#.*$', Comment.Single),
      (
       '^(\\w+)(=)', bygroups(Name.Attribute, Operator)),
      (
       '^([\\w.]+)(:)',
       bygroups(Name.Tag, Punctuation), 'spvalue'),
      include('interp'),
      (
       '[^${}#=:\\n.]+', Text),
      (
       '.', Text)], 
     'interp':[
      (
       '\\$\\$', Text),
      (
       '\\$\\{', String.Interpol, 'curly')], 
     'curly':[
      (
       '\\}', String.Interpol, '#pop'),
      (
       '\\w+', Name.Attribute)], 
     'spvalue':[
      include('interp'),
      (
       '#.*$', Comment.Single, '#pop'),
      (
       '\\n', Text, '#pop'),
      (
       '[^${}#\\n]+', Text),
      (
       '.', Text)]}


class PacmanConfLexer(RegexLexer):
    __doc__ = '\n    Lexer for `pacman.conf\n    <https://www.archlinux.org/pacman/pacman.conf.5.html>`_.\n\n    Actually, IniLexer works almost fine for this format,\n    but it yield error token. It is because pacman.conf has\n    a form without assignment like:\n\n        UseSyslog\n        Color\n        TotalDownload\n        CheckSpace\n        VerbosePkgLists\n\n    These are flags to switch on.\n\n    .. versionadded:: 2.1\n    '
    name = 'PacmanConf'
    aliases = ['pacmanconf']
    filenames = ['pacman.conf']
    mimetypes = []
    tokens = {'root': [
              (
               '#.*$', Comment.Single),
              (
               '^\\s*\\[.*?\\]\\s*$', Keyword),
              (
               '(\\w+)(\\s*)(=)',
               bygroups(Name.Attribute, Text, Operator)),
              (
               '^(\\s*)(\\w+)(\\s*)$',
               bygroups(Text, Name.Attribute, Text)),
              (
               words(('$repo', '$arch', '%o', '%u'),
                 suffix='\\b'),
               Name.Variable),
              (
               '.', Text)]}


class AugeasLexer(RegexLexer):
    __doc__ = '\n    Lexer for `Augeas <http://augeas.net>`_.\n\n    .. versionadded:: 2.4\n    '
    name = 'Augeas'
    aliases = ['augeas']
    filenames = ['*.aug']
    tokens = {'root':[
      (
       '(module)(\\s*)([^\\s=]+)', bygroups(Keyword.Namespace, Text, Name.Namespace)),
      (
       '(let)(\\s*)([^\\s=]+)', bygroups(Keyword.Declaration, Text, Name.Variable)),
      (
       '(del|store|value|counter|seq|key|label|autoload|incl|excl|transform|test|get|put)(\\s+)', bygroups(Name.Builtin, Text)),
      (
       '(\\()([^:]+)(\\:)(unit|string|regexp|lens|tree|filter)(\\))', bygroups(Punctuation, Name.Variable, Punctuation, Keyword.Type, Punctuation)),
      (
       '\\(\\*', Comment.Multiline, 'comment'),
      (
       '[*+\\-.;=?|]', Operator),
      (
       '[()\\[\\]{}]', Operator),
      (
       '"', String.Double, 'string'),
      (
       '\\/', String.Regex, 'regex'),
      (
       '([A-Z]\\w*)(\\.)(\\w+)', bygroups(Name.Namespace, Punctuation, Name.Variable)),
      (
       '.', Name.Variable),
      (
       '\\s', Text)], 
     'string':[
      (
       '\\\\.', String.Escape),
      (
       '[^"]', String.Double),
      (
       '"', String.Double, '#pop')], 
     'regex':[
      (
       '\\\\.', String.Escape),
      (
       '[^/]', String.Regex),
      (
       '\\/', String.Regex, '#pop')], 
     'comment':[
      (
       '[^*)]', Comment.Multiline),
      (
       '\\(\\*', Comment.Multiline, '#push'),
      (
       '\\*\\)', Comment.Multiline, '#pop'),
      (
       '[)*]', Comment.Multiline)]}


class TOMLLexer(RegexLexer):
    __doc__ = '\n    Lexer for `TOML <https://github.com/toml-lang/toml>`_, a simple language\n    for config files.\n\n    .. versionadded:: 2.4\n    '
    name = 'TOML'
    aliases = ['toml']
    filenames = ['*.toml']
    tokens = {'root': [
              (
               '\\s+', Text),
              (
               '#.*?$', Comment.Single),
              (
               '"(\\\\\\\\|\\\\"|[^"])*"', String),
              (
               "\\'\\'\\'(.*)\\'\\'\\'", String),
              (
               "\\'[^\\']*\\'", String),
              (
               '(true|false)$', Keyword.Constant),
              (
               '[a-zA-Z_][\\w\\-]*', Name),
              (
               '\\[.*?\\]$', Keyword),
              (
               '\\d{4}-\\d{2}-\\d{2}(?:T| )\\d{2}:\\d{2}:\\d{2}(?:Z|[-+]\\d{2}:\\d{2})', Number.Integer),
              (
               '(\\d+\\.\\d*|\\d*\\.\\d+)([eE][+-]?[0-9]+)?j?', Number.Float),
              (
               '\\d+[eE][+-]?[0-9]+j?', Number.Float),
              (
               '[+-]?(?:(inf(?:inity)?)|nan)', Number.Float),
              (
               '[+-]?\\d+', Number.Integer),
              (
               '[]{}:(),;[]', Punctuation),
              (
               '\\.', Punctuation),
              (
               '=', Operator)]}