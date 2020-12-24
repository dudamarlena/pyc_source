# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/combiners/tests/test_httpd_conf_tree.py
# Compiled at: 2019-11-14 13:57:46
from insights.combiners.httpd_conf import _HttpdConf, HttpdConfTree, _HttpdConfSclHttpd24, HttpdConfSclHttpd24Tree, _HttpdConfSclJbcsHttpd24, HttpdConfSclJbcsHttpd24Tree
from insights.tests import context_wrap
from insights.parsers import SkipException
import pytest
HTTPD_CONF_MIXED = ('\nJustFotTest_NoSec "/var/www/cgi"\n# prefork MPM\n<IfModule prefork.c>\nServerLimit      256\nThreadsPerChild  16\nJustForTest      "AB"\nMaxClients       256\n</IfMoDuLe>\n\nIncludeOptional conf.d/*.conf\n').strip()
HTTPD_CONF_CONTINUATION = ('\nJustFotTest_NoSec "/var/www/cgi"\nCustomLog logs/ssl_request_log \\\n"%t %h %{SSL_PROTOCOL}x %{SSL_CIPHER}x \\"%r\\" %b"\n# prefork MPM\n<IfModule prefork.c>\nServerLimit      256\nThreadsPerChild  16\nJustForTest      "AB"\nMaxClients       256\n</IfModule>\n\nIncludeOptional conf.d/*.conf\n').strip()
HTTPD_CONF_1 = ('\nJustFotTest_NoSec "/var/www/cgi"\n# prefork MPM\n<IfModule prefork.c>\nServerLimit      256\nThreadsPerChild  16\nJustForTest      "AB"\nMaxClients       256\n</IfModule>\n\nIncludeOptional conf.d/*.conf\n').strip()
HTTPD_CONF_2 = ('\nJustForTest_NoSec "/var/www/cgi"\n# prefork MPM\n<IfModule prefork.c>\nServerLimit      1024\nJustForTest      "ABC"\nMaxClients       1024\n</IfModule>\n').strip()
HTTPD_CONF_3 = ('\n# prefork MPM\n<IfModule prefork.c>\nServerLimit      256\nMaxClients       512\n</IfModule>\n').strip()
HTTPD_CONF_SHADOWTEST_1 = ('\nFoo 1A\nFoo 1B\nFoo 1C\n<IfModule prefork.c>\nFoo 1xA\nFoo 1xB\nFoo 1xC\nBar 1A\nBar 1B\nBar 1C\n</IfModule>\n\nIncludeOptional conf.d/*.conf\n').strip()
HTTPD_CONF_SHADOWTEST_2 = ('\nFoo 2A\nFoo 2B\nFoo 2C\n<IfModule ASDF.prefork.c.ASDF>\nFoo 2xA\nFoo 2xB\nFoo 2xC\nBar 2A\nBar 2B\nBar 2C\n</IfModule>\n').strip()
HTTPD_CONF_SHADOWTEST_3 = ('\nFoo 3A\nFoo 3B\nFoo 3C\n<IfModule prefork.c>\nFoo 3xA\nFoo 3xB\nFoo 3xC\nBar 3A\nBar 3B\nBar 3C\n</IfModule>\n').strip()
HTTPD_CONF_MAIN_1 = ('\nServerRoot "/etc/httpd"\nListen 80\n\n# Load config files in the "/etc/httpd/conf.d" directory, if any.\nIncludeOptional conf.d/*.conf\nSSLProtocol -ALL +TLSv1.2  # SSLv3\n').strip()
HTTPD_CONF_MAIN_2 = ('\n# Load config files in the "/etc/httpd/conf.d" directory, if any.\nIncludeOptional conf.d/*.conf\n\nServerRoot "/etc/httpd"\nListen 80\n').strip()
HTTPD_CONF_MAIN_3 = ('\nServerRoot "/etc/httpd"\n\n# Load config files in the "/etc/httpd/conf.d" directory, if any.\nIncludeOptional conf.d/*.conf\nIncludeOptional conf.d/*/*.conf\n\nListen 80\n').strip()
HTTPD_CONF_MAIN_4 = ('\nIncludeOptional conf.d/*.conf\nIncludeOptional conf.modules.d/*.conf\nListen 80\n').strip()
HTTPD_CONF_FILE_1 = ('\nServerRoot "/home/skontar/httpd"\nListen 8080\n').strip()
HTTPD_CONF_FILE_2 = ('\nServerRoot "/home/skontar/www"\n').strip()
HTTPD_CONF_FILE_3 = ('\nLoadModule access_compat_module modules/mod_access_compat.so\nLoadModule actions_module modules/mod_actions.so\nLoadModule alias_module modules/mod_alias.so\nLoadModule mpm_prefork_module modules/mod_mpm_prefork.so\n').strip()
HTTPD_CONF_MORE = ('\nUserDir disable\nUserDir enable bob\n').strip()
HTTPD_EMPTY_LAST = ('\n#\n# Directives controlling the display of server-generated directory listings.\n#\n# Required modules: mod_authz_core, mod_authz_host,\n#                   mod_autoindex, mod_alias\n#\n# To see the listing of a directory, the Options directive for the\n# directory must include "Indexes", and the directory must not contain\n# a file matching those listed in the DirectoryIndex directive.\n#\n\n#\n# IndexOptions: Controls the appearance of server-generated directory\n# listings.\n#\nIndexOptions FancyIndexing HTMLTable VersionSort\n\n# We include the /icons/ alias for FancyIndexed directory listings.  If\n# you do not use FancyIndexing, you may comment this out.\n#\nAlias /icons/ "/usr/share/httpd/icons/"\n\n<Directory "/usr/share/httpd/icons">\n    Options Indexes MultiViews FollowSymlinks\n    AllowOverride None\n    Require all granted\n</Directory>\n\n#\n# AddIcon* directives tell the server which icon to show for different\n# files or filename extensions.  These are only displayed for\n# FancyIndexed directories.\n#\nAddIconByEncoding (CMP,/icons/compressed.gif) x-compress x-gzip\n\nAddIconByType (TXT,/icons/text.gif) text/*\nAddIconByType (IMG,/icons/image2.gif) image/*\nAddIconByType (SND,/icons/sound2.gif) audio/*\nAddIconByType (VID,/icons/movie.gif) video/*\n\nAddIcon /icons/binary.gif .bin .exe\nAddIcon /icons/binhex.gif .hqx\nAddIcon /icons/tar.gif .tar\nAddIcon /icons/world2.gif .wrl .wrl.gz .vrml .vrm .iv\nAddIcon /icons/compressed.gif .Z .z .tgz .gz .zip\nAddIcon /icons/a.gif .ps .ai .eps\nAddIcon /icons/layout.gif .html .shtml .htm .pdf\nAddIcon /icons/text.gif .txt\nAddIcon /icons/c.gif .c\nAddIcon /icons/p.gif .pl .py\nAddIcon /icons/f.gif .for\nAddIcon /icons/dvi.gif .dvi\nAddIcon /icons/uuencoded.gif .uu\nAddIcon /icons/script.gif .conf .sh .shar .csh .ksh .tcl\nAddIcon /icons/tex.gif .tex\nAddIcon /icons/bomb.gif core.\n\nAddIcon /icons/back.gif ..\nAddIcon /icons/hand.right.gif README\nAddIcon /icons/folder.gif ^^DIRECTORY^^\nAddIcon /icons/blank.gif ^^BLANKICON^^\n\n#\n# DefaultIcon is which icon to show for files which do not have an icon\n# explicitly set.\n#\nDefaultIcon /icons/unknown.gif\n\n#\n# AddDescription allows you to place a short description after a file in\n# server-generated indexes.  These are only displayed for FancyIndexed\n# directories.\n# Format: AddDescription "description" filename\n#\n#AddDescription "GZIP compressed document" .gz\n#AddDescription "tar archive" .tar\n#AddDescription "GZIP compressed tar archive" .tgz\n\n#\n# ReadmeName is the name of the README file the server will look for by\n# default, and append to directory listings.\n#\n# HeaderName is the name of a file which should be prepended to\n# directory indexes.\nReadmeName README.html\nHeaderName HEADER.html\n\n#\n# IndexIgnore is a set of filenames which directory indexing should ignore\n# and not include in the listing.  Shell-style wildcarding is permitted.\n#\nIndexIgnore .??* *~ *# HEADER* README* RCS CVS *,v *,t\n\n').lstrip()
HTTPD_CONF_NEST_1 = ('\n<VirtualHost 128.39.140.28>\n    <Directory /var/www/example>\n        Options FollowSymLinks\n        AllowOverride None\n    </Directory>\n    <IfModule mod_php4.c>\n        php_admin_flag safe_mode Off\n        php_admin_value register_globals    0\n    </IfModule>\n    DirectoryIndex index.php\n    <IfModule mod_rewrite.c>\n        RewriteEngine On\n        RewriteRule .* /index.php\n    </IfModule>\n    <IfModule mod_rewrite.c>\n        RewriteEngine Off\n    </IfModule>\n    <IfModule !php5_module>\n        <IfModule !php4_module>\n            <FilesMatch ".php[45]?$">\n                Order allow,deny\n                Deny from all\n            </FilesMatch>\n            <FilesMatch ".php[45]?$">\n                Order deny,allow\n            </FilesMatch>\n        </IfModule>\n    </IfModule>\n    DocumentRoot /var/www/example\n    ServerName www.example.com\n    ServerAlias admin.example.com\n</VirtualHost>\n<IfModule !php5_module>\n  <IfModule !php4_module>\n    <Location />\n        <FilesMatch ".php[45]">\n            Order allow,deny\n            Deny from all\n        </FilesMatch>\n    </Location>\n  </IfModule>\n</IfModule>\n<IfModule mod_rewrite.c>\n    RewriteEngine Off\n</IfModule>\nLogLevel warn\nDocumentRoot "/var/www/html_cgi"\nIncludeOptional conf.d/*.conf\nEnableSendfile on\n').strip()
HTTPD_CONF_NEST_2 = ('\nDocumentRoot "/var/www/html"\n<VirtualHost 128.39.140.30>\n    <IfModule !php5_module>\n        <IfModule !php4_module>\n            <FilesMatch ".php[45]?$">\n                Order allow,deny\n                Deny from all\n            </FilesMatch>\n            <FilesMatch ".php[45]?$">\n                Order deny,allow\n            </FilesMatch>\n        </IfModule>\n    </IfModule>\n    DocumentRoot /var/www/example1\n    ServerName www.example1.com\n    ServerAlias admin.example1.com\n</VirtualHost>\n<IfModule !php5_module>\n  <IfModule !php4_module>\n    <Location />\n        <FilesMatch test>\n            Order deny,allow\n            Allow from all\n        </FilesMatch>\n        <FilesMatch ".php[45]">\n            Order deny,allow\n        </FilesMatch>\n    </Location>\n  </IfModule>\n</IfModule>\n<IfModule mod_rewrite.c>\n    RewriteEngine On\n</IfModule>\nEnableSendfile off\n').strip()
HTTPD_CONF_NEST_3 = ('\n<VirtualHost 128.39.140.28>\n    <IfModule !php5_module>\n        Testphp php5_v3_1\n        <IfModule !php4_module>\n            Testphp php4_v3_1\n        </IfModule>\n        Testphp php5_v3_2\n    </IfModule>\n</VirtualHost>\n<IfModule !php5_module>\n  Testphp php5_3_a\n  <IfModule !php4_module>\n    Testphp php4_3_a\n  </IfModule>\n</IfModule>\n').strip()
HTTPD_CONF_NEST_4 = ('\n<VirtualHost 128.39.140.30>\n    <IfModule !php5_module>\n        Testphp php5_v4_1\n        <IfModule !php4_module>\n            Testphp php4_v4_1\n        </IfModule>\n        Testphp php5_v4_2\n    </IfModule>\n</VirtualHost>\n<IfModule !php5_module>\n  Testphp php5_4_b\n  <IfModule !php4_module>\n    Testphp php4_4_b\n  </IfModule>\n</IfModule>\n').strip()
HTTPD_REGEX_AND_OP_ATTRS = ('\nRewriteCond %{HTTP:Accept-Encoding} \\b(x-)?gzip\\b\nRedirectMatch ^\\/?pulp_puppet\\/forge\\/[^\\/]+\\/[^\\/]+\\/(?!api\\/v1\\/releases\\.json)(.*)$ /$1\nRewriteCond %1%2 (^|&|;)([^(&|;)].*|$)\nRewriteCond %{HTTP:Accept-Encoding} \\b(x-)?gzip\\b\n<IfVersion < 2.4>\n    Allow from all\n  </IfVersion>\n').strip()
HTTPD_EMBEDDED_QUOTES = ('\n# DirectoryIndex: sets the file that Apache will serve if a directory\n# is requested.\n#\n<IfModule dir_module>\n    DirectoryIndex index.html\n</IfModule>\n\n#\n# The following lines prevent .htaccess and .htpasswd files from being\n# viewed by Web clients.\n#\n<Files ".ht*">\n    Require all denied\n</Files>\n\n#\n# ErrorLog: The location of the error log file.\n# If you do not specify an ErrorLog directive within a <VirtualHost>\n# container, error messages relating to that virtual host will be\n# logged here.  If you *do* define an error logfile for a <VirtualHost>\n# container, that host\'s errors will be logged there and not here.\n#\nErrorLog "logs/error_log"\n\n  RequestHeader   whatever # last value is taken\n  \n  \n  RequestHeader   unset   Proxy\n\n#\n# LogLevel: Control the number of messages logged to the error_log.\n# Possible values include: debug, info, notice, warn, error, crit,\n# alert, emerg.\n#\nLogLevel warn\n\n<IfModule log_config_module>\n    #\n    # The following directives define some format nicknames for use with\n    # a CustomLog directive (see below).\n    #\n    LogFormat "%h %l %u %t \\"%r\\" %>s %b \\"%{Referer}i\\" \\"%{User-Agent}i\\"" combined\n    LogFormat "%h %l %u %t \\"%r\\" %>s %b" common\n\n    <IfModule logio_module>\n      # You need to enable mod_logio.c to use %I and %O\n      LogFormat "%h %l %u %t \\"%r\\" %>s %b \\"%{Referer}i\\" \\"%{User-Agent}i\\" %I %O" combinedio\n    </IfModule>\n\n    #\n    # The location and format of the access logfile (Common Logfile Format).\n    # logged therein and *not* in this file.\n    #\n    #CustomLog "logs/access_log" common\n\n    #\n    # If you prefer a logfile with access, agent, and referer information\n    # (Combined Logfile Format) you can use the following directive.\n    #\n    CustomLog "logs/access_log" combined\n</IfModule>\n\n\nDNSSDEnable on\n#DNSSDAutoRegisterVHosts on\n#DNSSDAutoRegisterUserDir on\n').strip()
UNICODE_COMMENTS = '\n#Alterações realizadas por issue no Insights\nDNSSDEnable on\n#DNSSDAutoRegisterVHosts on\n#DNSSDAutoRegisterUserDir on\n'
MULTIPLE_INCLUDES = '\n<IfVersion < 2.4>\n  Include /etc/httpd/conf.d/05-foreman.d/*.conf\n</IfVersion>\n<IfVersion >= 2.4>\n  IncludeOptional /etc/httpd/conf.d/05-foreman.d/*.conf\n</IfVersion>\n'

def test_mixed_case_tags():
    httpd = _HttpdConf(context_wrap(HTTPD_CONF_MIXED, path='/etc/httpd/conf/httpd.conf'))
    assert httpd.find('ServerLimit').value == 256


def test_line_continuation():
    httpd = _HttpdConf(context_wrap(HTTPD_CONF_CONTINUATION, path='/etc/httpd/conf/httpd.conf'))
    val = httpd.find('CustomLog')[0].attrs
    assert val == ['logs/ssl_request_log', '%t %h %{SSL_PROTOCOL}x %{SSL_CIPHER}x "%r" %b'], val


def test_nopath():
    httpd2 = _HttpdConf(context_wrap(HTTPD_CONF_2))
    try:
        result = HttpdConfTree([httpd2])
        exception_happened = False
    except:
        exception_happened = True

    assert exception_happened
    httpd2 = _HttpdConf(context_wrap(HTTPD_CONF_2, path='/etc/httpd/conf.d/00-z.conf'))
    try:
        result = HttpdConfTree([httpd2])
        exception_happened = False
    except:
        exception_happened = True

    assert exception_happened
    httpd2 = _HttpdConf(context_wrap(HTTPD_CONF_2, path='/etc/httpd/conf/httpd.conf'))
    result = HttpdConfTree([httpd2])
    assert result[('IfModule', 'prefork.c')]['ServerLimit'][(-1)].value == 1024
    httpd2 = _HttpdConf(context_wrap(HTTPD_CONF_2, path='/laaalalalala/blablabla/httpd.conf'))
    result = HttpdConfTree([httpd2])
    assert result[('IfModule', 'prefork.c')]['ServerLimit'][(-1)].value == 1024
    httpd2 = _HttpdConf(context_wrap(HTTPD_CONF_2, path='/etc/httpd/conf/httpd.conf'))
    httpd3 = _HttpdConf(context_wrap(HTTPD_CONF_3, path='/etc/httpd/conf.d/z-z.conf'))
    result = HttpdConfTree([httpd2, httpd3])
    assert result[('IfModule', 'prefork.c')]['ServerLimit'][(-1)].value == 1024
    httpd2 = _HttpdConf(context_wrap(HTTPD_CONF_2, path='/etc/httpd/conf/httpd.conf'))
    httpd3 = _HttpdConf(context_wrap(HTTPD_CONF_3, path='/etc/httpd/conf.d/aaa.conf'))
    result = HttpdConfTree([httpd3, httpd2])
    assert len(result[('IfModule', 'prefork.c')]['ServerLimit']) == 1
    assert result[('IfModule', 'prefork.c')]['ServerLimit'][0].value == 1024
    assert result[('IfModule', 'prefork.c')]['ServerLimit'][(-1)].value == 1024
    httpd1 = _HttpdConf(context_wrap(HTTPD_CONF_1, path='/etc/httpd/conf/httpd.conf'))
    httpd2 = _HttpdConf(context_wrap(HTTPD_CONF_2, path='/etc/httpd/conf.d/00-z.conf'))
    result = HttpdConfTree([httpd1, httpd2])
    assert len(result[('IfModule', 'prefork.c')]['ServerLimit']) == 2
    assert result[('IfModule', 'prefork.c')]['ServerLimit'][0].value == 256
    assert result[('IfModule', 'prefork.c')]['ServerLimit'][(-1)].value == 1024
    httpd1 = _HttpdConf(context_wrap(HTTPD_CONF_1, path='/etc/httpd/conf/httpd.conf'))
    httpd2 = _HttpdConf(context_wrap(HTTPD_CONF_2, path='/etc/httpd/conf.d/00-z.conf'))
    httpd3 = _HttpdConf(context_wrap(HTTPD_CONF_3, path='/etc/httpd/conf.d/00-z.conf'))
    result = HttpdConfTree([httpd1, httpd2, httpd3])
    assert len(result[('IfModule', 'prefork.c')]['ServerLimit']) == 3
    assert result[('IfModule', 'prefork.c')]['ServerLimit'][0].value == 256
    assert result[('IfModule', 'prefork.c')]['ServerLimit'][1].value == 1024
    assert result[('IfModule', 'prefork.c')]['ServerLimit'][(-1)].value == 256
    assert len(result[('IfModule', 'prefork.c')]['MaxClients']) == 3
    assert result[('IfModule', 'prefork.c')]['MaxClients'][0].value == 256
    assert result[('IfModule', 'prefork.c')]['MaxClients'][1].value == 1024
    assert result[('IfModule', 'prefork.c')]['MaxClients'][(-1)].value == 512
    assert result[('IfModule', 'prefork.c')]['MaxClients'][0].value == 256
    assert result[('IfModule', 'prefork.c')]['MaxClients'][2].value == 512
    assert result[('IfModule', 'prefork.c')]['MaxClients'][(-1)].value == 512


def test_active_httpd():
    httpd1 = _HttpdConf(context_wrap(HTTPD_CONF_1, path='/etc/httpd/conf/httpd.conf'))
    httpd2 = _HttpdConf(context_wrap(HTTPD_CONF_2, path='/etc/httpd/conf.d/00-z.conf'))
    httpd3 = _HttpdConf(context_wrap(HTTPD_CONF_3, path='/etc/httpd/conf.d/z-z.conf'))
    result = HttpdConfTree([httpd1, httpd2, httpd3])
    assert result[('IfModule', 'prefork.c')]['MaxClients'][(-1)].value == 512
    assert result[('IfModule', 'prefork.c')]['MaxClients'][(-1)].file_path == '/etc/httpd/conf.d/z-z.conf'
    assert result[('IfModule', 'prefork.c')]['ThreadsPerChild'][(-1)].value == 16
    assert result[('IfModule', 'prefork.c')]['ServerLimit'][(-1)].value == 256
    assert result[('IfModule', 'prefork.c')]['JustForTest'][(-1)].file_name == '00-z.conf'
    assert result['JustForTest_NoSec'][0].line == 'JustForTest_NoSec "/var/www/cgi"'


def test_shadowing():
    httpd1 = _HttpdConf(context_wrap(HTTPD_CONF_SHADOWTEST_1, path='/etc/httpd/conf/httpd.conf'))
    httpd2 = _HttpdConf(context_wrap(HTTPD_CONF_SHADOWTEST_2, path='/etc/httpd/conf.d/00-z.conf'))
    httpd3 = _HttpdConf(context_wrap(HTTPD_CONF_SHADOWTEST_3, path='/etc/httpd/conf.d/z-z.conf'))
    result = HttpdConfTree([httpd1, httpd2, httpd3])
    assert len(result['Foo']) == 9
    assert len(result['IfModule']) == 3
    assert len(result['IfModule']['Foo']) == 9
    assert len(result['IfModule']['Bar']) == 9
    assert len(result[('IfModule', 'prefork.c')]) == 2
    assert len(result[('IfModule', 'prefork.c')]['Foo']) == 6
    assert len(result[('IfModule', 'prefork.c')]['Bar']) == 6
    assert len(result[('IfModule', 'prefork.c')][0]['Foo']) == 3
    assert len(result[('IfModule', 'prefork.c')][1]['Foo']) == 3
    assert len(result[('IfModule', 'prefork.c')][0]['Bar']) == 3
    assert len(result[('IfModule', 'prefork.c')][1]['Bar']) == 3


def test_splits():
    httpd1 = _HttpdConf(context_wrap(HTTPD_CONF_MAIN_1, path='/etc/httpd/conf/httpd.conf'))
    httpd2 = _HttpdConf(context_wrap(HTTPD_CONF_FILE_1, path='/etc/httpd/conf.d/00-a.conf'))
    httpd3 = _HttpdConf(context_wrap(HTTPD_CONF_FILE_2, path='/etc/httpd/conf.d/01-b.conf'))
    result = HttpdConfTree([httpd1, httpd2, httpd3])
    server_root = result['ServerRoot'][(-1)]
    assert server_root.value == '/home/skontar/www'
    assert server_root.line == 'ServerRoot "/home/skontar/www"'
    assert server_root.file_name == '01-b.conf'
    assert server_root.file_path == '/etc/httpd/conf.d/01-b.conf'
    listen = result['Listen'][(-1)]
    assert listen.value == 8080
    assert listen.line == 'Listen 8080'
    assert listen.file_name == '00-a.conf'
    assert listen.file_path == '/etc/httpd/conf.d/00-a.conf'
    ssl_proto = result['SSLProtocol'][(-1)]
    assert ssl_proto.attrs == ['-ALL', '+TLSv1.2', '#', 'SSLv3']
    httpd1 = _HttpdConf(context_wrap(HTTPD_CONF_MAIN_2, path='/etc/httpd/conf/httpd.conf'))
    httpd2 = _HttpdConf(context_wrap(HTTPD_CONF_FILE_1, path='/etc/httpd/conf.d/00-a.conf'))
    httpd3 = _HttpdConf(context_wrap(HTTPD_CONF_FILE_2, path='/etc/httpd/conf.d/01-b.conf'))
    result = HttpdConfTree([httpd1, httpd2, httpd3])
    server_root = result['ServerRoot'][(-1)]
    assert server_root.value == '/etc/httpd'
    assert server_root.line == 'ServerRoot "/etc/httpd"'
    assert server_root.file_name == 'httpd.conf'
    assert server_root.file_path == '/etc/httpd/conf/httpd.conf'
    listen = result['Listen'][(-1)]
    assert listen.value == 80
    assert listen.line == 'Listen 80'
    assert listen.file_name == 'httpd.conf'
    assert listen.file_path == '/etc/httpd/conf/httpd.conf'
    httpd1 = _HttpdConf(context_wrap(HTTPD_CONF_MAIN_3, path='/etc/httpd/conf/httpd.conf'))
    httpd2 = _HttpdConf(context_wrap(HTTPD_CONF_FILE_1, path='/etc/httpd/conf.d/00-a.conf'))
    httpd3 = _HttpdConf(context_wrap(HTTPD_CONF_FILE_2, path='/etc/httpd/conf.d/01-b.conf'))
    result = HttpdConfTree([httpd1, httpd2, httpd3])
    server_root = result['ServerRoot'][(-1)]
    assert server_root.value == '/home/skontar/www'
    assert server_root.line == 'ServerRoot "/home/skontar/www"'
    assert server_root.file_name == '01-b.conf'
    assert server_root.file_path == '/etc/httpd/conf.d/01-b.conf'
    assert listen.value == 80
    assert listen.line == 'Listen 80'
    assert listen.file_name == 'httpd.conf'
    assert listen.file_path == '/etc/httpd/conf/httpd.conf'


def test_httpd_one_file_overwrites():
    httpd = _HttpdConf(context_wrap(HTTPD_CONF_MORE, path='/etc/httpd/conf/httpd.conf'))
    result = HttpdConfTree([httpd])
    active_setting = result['UserDir'][(-1)]
    assert active_setting.value == 'enable bob'
    assert active_setting.file_path == '/etc/httpd/conf/httpd.conf'
    assert active_setting.file_name == 'httpd.conf'
    assert active_setting.line == 'UserDir enable bob', active_setting.line
    setting_list = result['UserDir']
    assert len(setting_list) == 2
    assert setting_list[0].value == 'disable'
    assert setting_list[0].line == 'UserDir disable'
    assert setting_list[0].file_path == '/etc/httpd/conf/httpd.conf'
    assert setting_list[0].file_name == 'httpd.conf'
    assert setting_list[0].section is None
    assert setting_list[1].value == 'enable bob'
    assert setting_list[1].line == 'UserDir enable bob'
    assert setting_list[1].file_path == '/etc/httpd/conf/httpd.conf'
    assert setting_list[1].file_name == 'httpd.conf'
    assert setting_list[1].section_name is None
    return


def test_httpd_conf_empty():
    with pytest.raises(SkipException):
        assert _HttpdConf(context_wrap('', path='/etc/httpd/httpd.conf')) is None
    return


def test_httpd_conf_tree_with_load_modules():
    httpd1 = _HttpdConfSclHttpd24(context_wrap(HTTPD_CONF_MAIN_4, path='/etc/httpd/conf/httpd.conf'))
    httpd2 = _HttpdConfSclHttpd24(context_wrap(HTTPD_CONF_MORE, path='/etc/httpd/conf.d/01-b.conf'))
    httpd3 = _HttpdConfSclHttpd24(context_wrap(HTTPD_CONF_FILE_3, path='/etc/httpd/conf.modules.d/02-c.conf'))
    result = HttpdConfTree([httpd1, httpd2, httpd3])
    userdirs = result['UserDir']
    assert len(userdirs) == 2
    assert userdirs[(-1)].value == 'enable bob'
    load_module_list = result['LoadModule']
    assert len(load_module_list) == 4
    assert result['LoadModule'][3].value == 'mpm_prefork_module modules/mod_mpm_prefork.so'
    assert result['LoadModule'][3].file_path == '/etc/httpd/conf.modules.d/02-c.conf'


def test_httpd_conf_scl_httpd24_tree():
    httpd1 = _HttpdConfSclHttpd24(context_wrap(HTTPD_CONF_MAIN_4, path='/opt/rh/httpd24/root/etc/httpd/conf/httpd.conf'))
    httpd2 = _HttpdConfSclHttpd24(context_wrap(HTTPD_CONF_MORE, path='/opt/rh/httpd24/root/etc/httpd/conf.d/01-b.conf'))
    httpd3 = _HttpdConfSclHttpd24(context_wrap(HTTPD_CONF_FILE_3, path='/opt/rh/httpd24/root/etc/httpd/conf.modules.d/02-c.conf'))
    result = HttpdConfSclHttpd24Tree([httpd1, httpd2, httpd3])
    userdirs = result['UserDir']
    assert len(userdirs) == 2
    assert userdirs[(-1)].value == 'enable bob'
    load_module_list = result['LoadModule']
    assert len(load_module_list) == 4
    assert result['LoadModule'][3].value == 'mpm_prefork_module modules/mod_mpm_prefork.so'
    assert result['LoadModule'][3].file_path == '/opt/rh/httpd24/root/etc/httpd/conf.modules.d/02-c.conf'


def test_httpd_conf_jbcs_httpd24_tree():
    httpd1 = _HttpdConfSclJbcsHttpd24(context_wrap(HTTPD_CONF_MAIN_4, path='/opt/rh/jbcs-httpd24/root/etc/httpd/conf/httpd.conf'))
    httpd2 = _HttpdConfSclJbcsHttpd24(context_wrap(HTTPD_CONF_MORE, path='/opt/rh/jbcs-httpd24/root/etc/httpd/conf.d/01-b.conf'))
    httpd3 = _HttpdConfSclJbcsHttpd24(context_wrap(HTTPD_CONF_FILE_3, path='/opt/rh/jbcs-httpd24/root/etc/httpd/conf.modules.d/02-c.conf'))
    result = HttpdConfSclJbcsHttpd24Tree([httpd1, httpd2, httpd3])
    userdirs = result['UserDir']
    assert len(userdirs) == 2
    assert userdirs[(-1)].value == 'enable bob'
    load_module_list = result['LoadModule']
    assert len(load_module_list) == 4
    assert result['LoadModule'][3].value == 'mpm_prefork_module modules/mod_mpm_prefork.so'
    assert result['LoadModule'][3].file_path == '/opt/rh/jbcs-httpd24/root/etc/httpd/conf.modules.d/02-c.conf'


def test_httpd_nested_conf_file():
    httpd1 = _HttpdConf(context_wrap(HTTPD_CONF_MAIN_3, path='/etc/httpd/conf/httpd.conf'))
    httpd2 = _HttpdConf(context_wrap(HTTPD_CONF_FILE_1, path='/etc/httpd/conf.d/00-a.conf'))
    httpd3 = _HttpdConf(context_wrap(HTTPD_CONF_FILE_2, path='/etc/httpd/conf.d/d1/hello.conf'))
    result = HttpdConfTree([httpd1, httpd2, httpd3])
    server_root = result['ServerRoot'][(-1)]
    assert server_root.value == '/home/skontar/www'
    assert server_root.line == 'ServerRoot "/home/skontar/www"'
    assert server_root.file_name == 'hello.conf'
    assert server_root.file_path == '/etc/httpd/conf.d/d1/hello.conf'


def test_empty_last_line():
    httpd = _HttpdConf(context_wrap(HTTPD_EMPTY_LAST, path='/etc/httpd/conf/httpd.conf'))
    result = HttpdConfTree([httpd])
    index_options = result['IndexOptions'][(-1)]
    assert index_options.value == 'FancyIndexing HTMLTable VersionSort'


def test_indented_lines_and_comments():
    httpd = _HttpdConf(context_wrap(HTTPD_EMBEDDED_QUOTES, path='/etc/httpd/conf/httpd.conf'))
    result = HttpdConfTree([httpd])
    request_headers = result['RequestHeader']
    assert len(request_headers) == 2


def test_regex_and_op_attrs():
    httpd = _HttpdConf(context_wrap(HTTPD_REGEX_AND_OP_ATTRS, path='/etc/httpd/conf/httpd.conf'))
    result = HttpdConfTree([httpd])
    rewrite_cond = result['RewriteCond']
    assert len(rewrite_cond) == 3
    if_version = result['IfVersion']
    assert len(if_version) == 1


def test_unicode_comments():
    httpd = _HttpdConf(context_wrap(UNICODE_COMMENTS, path='/etc/httpd/conf/httpd.conf'))
    result = HttpdConfTree([httpd])
    rewrite_cond = result['DNSSDEnable']
    assert len(rewrite_cond) == 1


def test_multiple_includes():
    httpd1 = _HttpdConf(context_wrap(MULTIPLE_INCLUDES, path='/etc/httpd/conf/httpd.conf'))
    httpd2 = _HttpdConf(context_wrap(UNICODE_COMMENTS, path='/etc/httpd/conf.d/05-foreman.d/hello.conf'))
    result = HttpdConfTree([httpd1, httpd2])
    assert len(result['IfVersion']['DNSSDEnable']) == 2


def test_recursive_includes():
    with pytest.raises(Exception):
        httpd1 = _HttpdConf(context_wrap(MULTIPLE_INCLUDES, path='/etc/httpd/conf/httpd.conf'))
        httpd2 = _HttpdConf(context_wrap(MULTIPLE_INCLUDES, path='/etc/httpd/conf.d/05-foreman.d/hello.conf'))
        HttpdConfTree([httpd1, httpd2])