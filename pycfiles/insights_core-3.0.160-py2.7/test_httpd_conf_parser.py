# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/combiners/tests/test_httpd_conf_parser.py
# Compiled at: 2019-11-14 13:57:46
from insights.parsr.query import first, last
from insights.combiners.httpd_conf import _HttpdConf
from insights.tests import context_wrap
HTTPD_CONF_PATH = '/etc/httpd/conf/httpd.conf'
HTTPD_CONF_D_PATH = '/etc/httpd/conf.d/default.conf'
HTTPD_CONF_1 = ('\nServerRoot "/etc/httpd"\n<Directory />\n    Options FollowSymLinks\n    AllowOverride None\n</Directory>\n\nSSLProtocol -ALL +SSLv3\n#SSLProtocol all -SSLv2\n\nNSSProtocol SSLV3 TLSV1.0\n#NSSProtocol ALL\n\n# prefork MPM\n <IfModule prefork.c>\nStartServers       8\nMinSpareServers    5\nMaxSpareServers   20\nServerLimit      256\nMaxClients       256\nMaxRequestsPerChild  200\n </IfModule>\n\n# worker MPM\n<IfModule worker.c>\nStartServers         4\nMaxClients         300\nMinSpareThreads     25\nMaxSpareThreads     75\nThreadsPerChild     25\nMaxRequestsPerChild  0\n</IfModule>\nLoadModule auth_basic_module modules/mod_auth_basic.so\nLoadModule auth_digest_module modules/mod_auth_digest.so\n').strip()
HTTPD_CONF_D_1 = ('\nSSLProtocol -ALL +SSLv3\n#SSLProtocol all -SSLv2\n\n#SSLCipherSuite ALL:!ADH:!EXPORT:!SSLv2:RC4+RSA:+HIGH:+MEDIUM:+LOW\nSSLCipherSuite ALL:!ADH:!EXPORT:!SSLv2:RC4+RSA:+HIGH:+MEDIUM:+LOW\n\n# MaxClients: maximum number of server processes allowed to start\n   MaxClients\n').strip()
HTTPD_CONF_SPLIT = ('\nLogLevel warn\nIncludeOptional conf.d/*.conf\nEnableSendfile on\n').strip()
HTTPD_CONF_MORE = ('\nUserDir disable\nUserDir enable bob\n').strip()
HTTPD_CONF_NEST_1 = ('\n<VirtualHost 192.0.2.1>\n    <Directory /var/www/example>\n        Options FollowSymLinks\n        AllowOverride None\n    </Directory>\n    <IfModule mod_php4.c>\n        php_admin_flag safe_mode Off\n        php_admin_value register_globals    0\n        php_value magic_quotes_gpc  0\n        php_value magic_quotes_runtime  0\n        php_value allow_call_time_pass_reference 0\n    </IfModule>\n    DirectoryIndex index.php\n    <IfModule mod_rewrite.c>\n        RewriteEngine On\n        RewriteRule .* /index.php\n    </IfModule>\n    <IfModule mod_rewrite.c>\n        RewriteEngine Off\n    </IfModule>\n    DocumentRoot /var/www/example\n    ServerName www.example.com\n    ServerAlias admin.example.com\n</VirtualHost>\n').strip()
HTTPD_CONF_NEST_2 = ('\n<IfModule !php5_module>\n  Testphp php5_1\n  <IfModule !php4_module>\n    Testphp php4_1\n    <Location />\n        <FilesMatch ".php[45]?$">\n            Order allow,deny\n            Deny from all\n        </FilesMatch>\n        <FilesMatch ".php[45]?$">\n            Order deny,allow\n        </FilesMatch>\n    </Location>\n    Testphp php4_2\n  </IfModule>\n  Testphp php5_2\n</IfModule>\n<IfModule !php5_module>\n    Testphp php5_3\n    JustATest on\n</IfModule>\n').strip()
HTTPD_CONF_NO_NAME_SEC = ('\n<RequireAll>\n    AuthName "NAME Access"\n    Require valid-user\n</RequireAll>\n').strip()
HTTPD_CONF_DOC = ('\nServerRoot "/etc/httpd"\nLoadModule auth_basic_module modules/mod_auth_basic.so\nLoadModule auth_digest_module modules/mod_auth_digest.so\n\n<Directory />\n    Options FollowSymLinks\n    AllowOverride None\n</Directory>\n\n<IfModule mod_mime_magic.c>\n#   MIMEMagicFile /usr/share/magic.mime\n    MIMEMagicFile conf/magic\n</IfModule>\n\nErrorLog "|/usr/sbin/httplog -z /var/log/httpd/error_log.%Y-%m-%d"\n\nSSLProtocol -ALL +SSLv3\n#SSLProtocol all -SSLv2\n\nNSSProtocol SSLV3 TLSV1.0\n#NSSProtocol ALL\n\n# prefork MPM\n <IfModule prefork.c>\nStartServers       8\nMinSpareServers    5\nMaxSpareServers   20\nServerLimit      256\nMaxClients       256\nMaxRequestsPerChild  200\n </IfModule>\n\n# worker MPM\n<IfModule worker.c>\nStartServers         4\nMaxClients         300\nMinSpareThreads     25\nMaxSpareThreads     75\nThreadsPerChild     25\nMaxRequestsPerChild  0\n</IfModule>\n').strip()

def test_get_httpd_conf_nest_1():
    context = context_wrap(HTTPD_CONF_NEST_1, path=HTTPD_CONF_PATH)
    result = _HttpdConf(context)
    assert result[('VirtualHost', '192.0.2.1')][('IfModule', 'mod_php4.c')]['php_admin_flag'][last].value == 'safe_mode Off'
    assert result[('VirtualHost', '192.0.2.1')][('IfModule', 'mod_rewrite.c')]['RewriteEngine'][last].value is False
    assert result[('VirtualHost', '192.0.2.1')][('IfModule', 'mod_rewrite.c')]['RewriteRule'][last].value == '.* /index.php'
    assert result[('VirtualHost', '192.0.2.1')]['ServerName'][last].value == 'www.example.com'


def test_get_httpd_conf_1():
    context = context_wrap(HTTPD_CONF_1, path=HTTPD_CONF_PATH)
    result = _HttpdConf(context)
    assert 'SSLCipherSuite' not in result
    assert result['ServerRoot'][first].value == '/etc/httpd'
    assert result['NSSProtocol'][first].value == 'SSLV3 TLSV1.0'
    assert result[('IfModule', 'prefork.c')]['MaxClients'][last].value == 256
    assert result[('IfModule', 'worker.c')]['MaxClients'][last].value == 300
    assert result.file_path == HTTPD_CONF_PATH
    assert 'ThreadsPerChild' not in result[('IfModule', 'prefork.c')]
    assert result[('IfModule', 'prefork.c')]['MaxRequestsPerChild'][last].value == 200
    assert result.file_name == 'httpd.conf'
    assert result['LoadModule'][first].value == 'auth_basic_module modules/mod_auth_basic.so'
    assert result['LoadModule'][last].value == 'auth_digest_module modules/mod_auth_digest.so'
    assert result[('Directory', '/')]['Options'][last].value == 'FollowSymLinks'


def test_get_httpd_conf_2():
    context = context_wrap(HTTPD_CONF_D_1, path=HTTPD_CONF_D_PATH)
    result = _HttpdConf(context)
    except_SSLC = 'ALL:!ADH:!EXPORT:!SSLv2:RC4+RSA:+HIGH:+MEDIUM:+LOW'
    assert result['SSLCipherSuite'][last].value == except_SSLC
    assert 'NSSProtocol' not in result
    assert result.file_path == HTTPD_CONF_D_PATH
    assert result.file_name == 'default.conf'
    assert result['SSLProtocol'][last].value == '-ALL +SSLv3'
    assert result['SSLProtocol'][last].line == 'SSLProtocol -ALL +SSLv3'


def test_multiple_values_for_directive():
    context = context_wrap(HTTPD_CONF_MORE, path=HTTPD_CONF_PATH)
    result = _HttpdConf(context)
    assert result.file_path == HTTPD_CONF_PATH
    assert result.file_name == 'httpd.conf'
    assert len(result['UserDir']) == 2
    assert result['UserDir'][0].value == 'disable'
    assert result['UserDir'][1].value == 'enable bob'


def test_no_name_section():
    context = context_wrap(HTTPD_CONF_NO_NAME_SEC, path=HTTPD_CONF_PATH)
    result = _HttpdConf(context)
    assert result['RequireAll']['AuthName'][last].value == 'NAME Access'
    assert result['RequireAll']['Require'][last].value == 'valid-user'