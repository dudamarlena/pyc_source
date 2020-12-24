# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsr/examples/tests/test_httpd.py
# Compiled at: 2019-11-14 13:57:46
from insights.parsr.examples.httpd_conf import loads
from insights.parsr.query import ieq
DATA = '\n<IfModule log_config_module>\n    #\n    # The following directives define some format nicknames for use with\n    # a CustomLog directive (see below).\n    #\n    LogFormat "%h %l %u %t \\"%r\\" %>s %b \\"%{Referer}i\\" \\"%{User-Agent}i\\"" combined\n    LogFormat "%h %l %u %t \\"%r\\" %>s %b" common\n</IfModule>\n    <IfModule logio_module>\n      # You need to enable mod_logio.c to use %I and %O\n      LogFormat "%h %l %u %t \\"%r\\" %>s %b \\"%{Referer}i\\" \\"%{User-Agent}i\\" %I %O" combinedio\n    </IfModule>\n\n    #\n    # The location and format of the access logfile (Common Logfile Format).\n    # If you do not define any access logfiles within a <VirtualHost>\n    # container, they will be logged here.  Contrariwise, if you *do*\n    # define per-<VirtualHost> access logfiles, transactions will be\n    # logged therein and *not* in this file.\n    #\n    #CustomLog "logs/access_log" common\n    CustomLog logs/ssl_request_log \\\n    "%t %h %{SSL_PROTOCOL}x %{SSL_CIPHER}x "%r" %b"\n\n    #\n    # If you prefer a logfile with access, agent, and referer information\n    # (Combined Logfile Format) you can use the following directive.\n    #\n    CustomLog "logs/access_log" combined\n'
HTTPD_CONF_NEST_1 = ('\n<VirtualHost 128.39.140.28>\n    <Directory /var/www/example>\n        Options FollowSymLinks\n        AllowOverride None\n    </Directory>\n    <IfModule mod_php4.c>\n        php_admin_flag safe_mode Off\n        php_admin_value register_globals    0\n    </IfModule>\n    DirectoryIndex index.php\n    <IfModule mod_rewrite.c>\n        RewriteEngine On\n        RewriteRule .* /index.php\n    </IfModule>\n    <IfModule mod_rewrite.c>\n        RewriteEngine Off\n    </IfModule>\n    <IfModule !php5_module>\n        <IfModule !php4_module>\n            <FilesMatch ".php[45]?$">\n                Order allow,deny\n                Deny from all\n            </FilesMatch>\n            <FilesMatch ".php[45]?$">\n                Order deny,allow\n            </FilesMatch>\n        </IfModule>\n    </IfModule>\n    DocumentRoot /var/www/example\n    ServerName www.example.com\n    ServerAlias admin.example.com\n</VirtualHost>\n<IfModule !php5_module>\n  <IfModule !php4_module>\n    <Location />\n        <FilesMatch ".php[45]">\n            Order allow,deny\n            Deny from all\n        </FilesMatch>\n    </Location>\n  </IfModule>\n</IfModule>\n<IfModule mod_rewrite.c>\n    RewriteEngine Off\n</IfModule>\nLogLevel warn\nDocumentRoot "/var/www/html_cgi"\nIncludeOptional conf.d/*.conf\nEnableSendfile on\nSSLProtocol -ALL +TLSv1.2  # SSLv3\n').strip()
HTTPD_CONF_NEST_2 = ('\nDocumentRoot "/var/www/html"\n<VirtualHost 128.39.140.30>\n    <IfModule !php5_module>\n        <IfModule !php4_module>\n            <FilesMatch ".php[45]?$">\n                Order allow,deny\n                Deny from all\n            </FilesMatch>\n            <FilesMatch ".php[45]?$">\n                Order deny,allow\n            </FilesMatch>\n        </IfModule>\n    </IfModule>\n    DocumentRoot /var/www/example1\n    ServerName www.example1.com\n    ServerAlias admin.example1.com\n</VirtualHost>\n<IfModule !php5_module>\n  <IfModule !php4_module>\n    <Location />\n        <FilesMatch test>\n            Order deny,allow\n            Allow from all\n        </FilesMatch>\n        <FilesMatch ".php[45]">\n            Order deny,allow\n        </FilesMatch>\n    </Location>\n  </IfModule>\n</IfModule>\n<IfModule mod_rewrite.c>\n    RewriteEngine On\n</IfModule>\nEnableSendfile off\n').strip()
HTTPD_CONF_NEST_3 = ('\n<VirtualHost 128.39.140.28>\n    <IfModule !php5_module>\n        Testphp php5_v3_1\n        <IfModule !php4_module>\n            Testphp php4_v3_1\n        </IfModule>\n        Testphp php5_v3_2\n    </IfModule>\n</VirtualHost>\n<IfModule !php5_module>\n  Testphp php5_3_a\n  <IfModule !php4_module>\n    Testphp php4_3_a\n  </IfModule>\n</IfModule>\n').strip()
HTTPD_CONF_NEST_4 = ('\n<VirtualHost 128.39.140.30>\n    <IfModule !php5_module>\n        Testphp php5_v4_1\n        <IfModule !php4_module>\n            Testphp php4_v4_1\n        </IfModule>\n        Testphp php5_v4_2\n    </IfModule>\n</VirtualHost>\n<IfModule !php5_module>\n  Testphp php5_4_b\n  <IfModule !php4_module>\n    Testphp php4_4_b\n  </IfModule>\n</IfModule>\n').strip()

def test_if_module():
    val = loads(DATA)
    assert len(val) == 4


def test_httpd_conf_nest_one():
    val = loads(HTTPD_CONF_NEST_1)
    assert len(val['IfModule']) == 2
    assert len(val[('IfModule', 'mod_rewrite.c')]) == 1
    assert len(val[('IfModule', '!php5_module')]) == 1
    assert val[('IfModule', 'mod_rewrite.c')][0].lineno == 43
    assert val['LogLevel'].value == 'warn'
    assert val['LogLevel'][0].lineno == 46
    assert val[ieq('loglevel')].value == 'warn'
    assert val['SSLProtocol'][0].attrs == ['-ALL', '+TLSv1.2', '#', 'SSLv3']