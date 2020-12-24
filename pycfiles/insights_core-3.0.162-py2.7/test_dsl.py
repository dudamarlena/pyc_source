# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/configtree/tests/test_dsl.py
# Compiled at: 2019-05-16 13:41:33
from insights.configtree import startswith, istartswith
from insights.configtree import endswith, iendswith
from insights.configtree import contains, icontains
from insights.configtree import eq, ieq, le, ile, lt, ilt, ge, ige, gt, igt
from insights.configtree import first, last
from insights.combiners.httpd_conf import _HttpdConf, HttpdConfTree
from insights.combiners.httpd_conf import in_network, is_private
from insights.tests import context_wrap
HTTPD_CONF_1 = ('\nJustFotTest_NoSec "/var/www/cgi"\n# prefork MPM\n<IfModule prefork.c>\nServerLimit      256\nThreadsPerChild  16\nJustForTest      "AB"\nMaxClients       256\n</IfModule>\n\nIncludeOptional conf.d/*.conf\n').strip()
HTTPD_CONF_2 = ('\nJustForTest_NoSec "/var/www/cgi"\n# prefork MPM\n<IfModule prefork.c>\nServerLimit      1024\nJustForTest      "ABC"\nMaxClients       1024\n</IfModule>\n').strip()
HTTPD_CONF_3 = ('\n# prefork MPM\n<IfModule prefork.c>\nServerLimit      256\nMaxClients       512\n</IfModule>\n').strip()
HTTPD_CONF_SHADOWTEST_1 = ('\nFoo 1A\nFoo 1B\nFoo 1C\n<IfModule prefork.c>\nFoo 1xA\nFoo 1xB\nFoo 1xC\nBar 1A\nBar 1B\nBar 1C\n</IfModule>\n\nIncludeOptional conf.d/*.conf\n').strip()
HTTPD_CONF_SHADOWTEST_2 = ('\nFoo 2A\nFoo 2B\nFoo 2C\n<IfModule ASDF.prefork.c.ASDF>\nFoo 2xA\nFoo 2xB\nFoo 2xC\nBar 2A\nBar 2B\nBar 2C\n</IfModule>\n').strip()
HTTPD_CONF_SHADOWTEST_3 = ('\nFoo 3A\nFoo 3B\nFoo 3C\n<IfModule prefork.c>\nFoo 3xA\nFoo 3xB\nFoo 3xC\nBar 3A\nBar 3B\nBar 3C\n</IfModule>\n').strip()
HTTPD_CONF_MAIN_1 = ('\nServerRoot "/etc/httpd"\nListen 80\n\n# Load config files in the "/etc/httpd/conf.d" directory, if any.\nIncludeOptional conf.d/*.conf\n').strip()
HTTPD_CONF_MAIN_2 = ('\n# Load config files in the "/etc/httpd/conf.d" directory, if any.\nIncludeOptional conf.d/*.conf\n\nServerRoot "/etc/httpd"\nListen 80\n').strip()
HTTPD_CONF_MAIN_3 = ('\nServerRoot "/etc/httpd"\n\n# Load config files in the "/etc/httpd/conf.d" directory, if any.\nIncludeOptional conf.d/*.conf\n\nListen 80\n').strip()
HTTPD_CONF_FILE_1 = ('\nServerRoot "/home/skontar/httpd"\nListen 8080\n').strip()
HTTPD_CONF_FILE_2 = ('\nServerRoot "/home/skontar/www"\n').strip()
HTTPD_CONF_MORE = ('\nUserDir disable\nUserDir enable bob\n').strip()
HTTPD_CONF_NEST_1 = ('\n<VirtualHost 128.39.140.28>\n    <Directory /var/www/example>\n        Options FollowSymLinks\n        AllowOverride None\n    </Directory>\n    <IfModule mod_php4.c>\n        php_admin_flag safe_mode Off\n        php_admin_value register_globals    0\n    </IfModule>\n    DirectoryIndex index.php\n    <IfModule mod_rewrite.c>\n        RewriteEngine On\n        RewriteRule .* /index.php\n    </IfModule>\n    <IfModule mod_rewrite.c>\n        RewriteEngine Off\n    </IfModule>\n    <IfModule !php5_module>\n        <IfModule !php4_module>\n            <FilesMatch ".php[45]?$">\n                Order allow,deny\n                Deny from all\n            </FilesMatch>\n            <FilesMatch ".php[45]?$">\n                Order deny,allow\n            </FilesMatch>\n        </IfModule>\n    </IfModule>\n    DocumentRoot /var/www/example\n    ServerName www.example.com\n    ServerAlias admin.example.com\n</VirtualHost>\n<IfModule !php5_module>\n  <IfModule !php4_module>\n    <Location />\n        <FilesMatch ".php[45]">\n            Order allow,deny\n            Deny from all\n        </FilesMatch>\n    </Location>\n  </IfModule>\n</IfModule>\n<IfModule mod_rewrite.c>\n    RewriteEngine Off\n</IfModule>\nLogLevel warn\nDocumentRoot "/var/www/html_cgi"\nIncludeOptional conf.d/*.conf\nEnableSendfile on\n').strip()
HTTPD_CONF_NEST_2 = ('\nDocumentRoot "/var/www/html"\n<VirtualHost 128.39.140.30>\n    <IfModule !php5_module>\n        <IfModule !php4_module>\n            <FilesMatch ".php[45]?$">\n                Order allow,deny\n                Deny from all\n            </FilesMatch>\n            <FilesMatch ".php[45]?$">\n                Order deny,allow\n            </FilesMatch>\n        </IfModule>\n    </IfModule>\n    DocumentRoot /var/www/example1\n    ServerName www.example1.com\n    ServerAlias admin.example1.com\n</VirtualHost>\n<IfModule !php5_module>\n  <IfModule !php4_module>\n    <Location />\n        <FilesMatch test>\n            Order deny,allow\n            Allow from all\n        </FilesMatch>\n        <FilesMatch ".php[45]">\n            Order deny,allow\n        </FilesMatch>\n    </Location>\n  </IfModule>\n</IfModule>\n<IfModule mod_rewrite.c>\n    RewriteEngine On\n</IfModule>\nEnableSendfile off\n').strip()
HTTPD_CONF_NEST_3 = ('\n<VirtualHost 128.39.140.28>\n    <IfModule !php5_module>\n        Testphp php5_v3_1\n        <IfModule !php4_module>\n            Testphp php4_v3_1\n        </IfModule>\n        Testphp php5_v3_2\n    </IfModule>\n</VirtualHost>\n<IfModule !php5_module>\n  Testphp php5_3_a\n  <IfModule !php4_module>\n    Testphp php4_3_a\n  </IfModule>\n</IfModule>\n').strip()
HTTPD_CONF_NEST_4 = ('\n<VirtualHost 128.39.140.30>\n    <IfModule !php5_module>\n        Testphp php5_v4_1\n        <IfModule !php4_module>\n            Testphp php4_v4_1\n        </IfModule>\n        Testphp php5_v4_2\n    </IfModule>\n</VirtualHost>\n<IfModule !php5_module>\n  Testphp php5_4_b\n  <IfModule !php4_module>\n    Testphp php4_4_b\n  </IfModule>\n</IfModule>\n').strip()

def test_startswith():
    data = [
     'abc', 'abrd', 'ed']
    assert startswith('ab')(data)
    assert istartswith('AB')(data)
    assert startswith('ab')('abcde')
    assert not startswith('de')(data)


def test_endswith():
    data = [
     'abc', 'abrd', 'ed']
    assert endswith('d')(data)
    assert iendswith('D')(data)
    assert endswith('d')('end')
    assert not endswith('re')(data)


def test_contains():
    data = [
     'abc', 'abrd', 'ed']
    assert contains('b')(data)
    assert icontains('B')(data)
    assert contains('b')('abc')
    assert not contains('x')(data)


def test_equals():
    data = [
     'abc', 'abrd', 'ed']
    assert eq('abc')(data)
    assert ieq('ABC')(data)
    assert eq('b')('b')
    assert eq(10)([1, 2, 10])
    assert eq(10.0)([1, 2, 10.0])
    assert eq(10)(10)
    assert eq(10.1)(10.1)


def test_less_than():
    data = [
     'abc', 'abrd', 'ed']
    assert lt('abd')(data)
    assert ilt('ABD')(data)
    assert lt('b')('a')
    assert lt(10)([1, 2, 10])
    assert lt(10)(9)
    assert lt(10.2)([1, 2, 10.1])
    assert lt(10.2)(9.3)


def test_less_than_equals():
    data = [
     'abc', 'abrd', 'ed']
    assert le('abd')(data)
    assert ile('ABD')(data)
    assert le('abc')(data)
    assert le('b')('b')
    assert le('b')('a')
    assert le(1)([1, 2, 10])
    assert le(10)(9.9)
    assert le(10.0)(10)
    assert le(10.1)([1, 2, 10.01])
    assert le(2.3)([1, 2.3, 10.1])
    assert le(10.2)(9.3)
    assert le(9.3)(9.3)


def test_greater_than():
    data = [
     'abc', 'abrd', 'ed']
    assert gt('abb')(data)
    assert igt('ABB')(data)
    assert gt('b')('c')
    assert gt(10)([1, 2, 11])
    assert gt(10)(11)
    assert gt(10.4)([1, 2, 11.5])
    assert gt(10.9)(11.02)


def test_greater_than_equals():
    data = [
     'abc', 'abrd', 'ed']
    assert ge('abb')(data)
    assert ige('ABB')(data)
    assert ge('abc')(data)
    assert ge('b')('c')
    assert ge('c')('c')
    assert ge(10)([1, 2, 11])
    assert ge(11)([1, 2, 11])
    assert ge(10)(11)
    assert ge(11)(11)
    assert ge(10.4)([1, 2, 11.5])
    assert ge(11.5)([1, 2, 11.5])
    assert ge(10.9)(11.02)
    assert ge(11.02)(11.02)


def test_simple_queries():
    httpd1 = _HttpdConf(context_wrap(HTTPD_CONF_NEST_1, path='/etc/httpd/conf/httpd.conf'))
    result = HttpdConfTree([httpd1])
    assert result['EnableSendfile'][first].value
    assert len(result['VirtualHost']) == 1
    assert len(result['VirtualHost']['Directory']) == 1
    assert len(result['VirtualHost']['IfModule']) == 4
    assert len(result['VirtualHost']['IfModule']['RewriteEngine']) == 2
    assert len(result['VirtualHost'][('IfModule', 'mod_rewrite.c')]) == 2


def test_complex_queries():
    httpd1 = _HttpdConf(context_wrap(HTTPD_CONF_NEST_1, path='/etc/httpd/conf/httpd.conf'))
    httpd2 = _HttpdConf(context_wrap(HTTPD_CONF_NEST_3, path='/etc/httpd/conf.d/00-a.conf'))
    httpd3 = _HttpdConf(context_wrap(HTTPD_CONF_NEST_4, path='/etc/httpd/conf.d/01-b.conf'))
    result = HttpdConfTree([httpd1, httpd2, httpd3])
    assert len(result.select('VirtualHost')) == 3
    assert len(result.select(('VirtualHost', '128.39.140.28'))) == 2
    assert len(result.select(('VirtualHost', '128.39.140.30'))) == 1
    assert len(result.select(('VirtualHost', startswith('128.39.140')))) == 3
    assert len(result.select(('VirtualHost', ~startswith('128.39.140')))) == 0
    assert len(result.select(('VirtualHost', endswith('140.30')))) == 1
    assert len(result.select(('VirtualHost', ~endswith('140.30')))) == 2
    assert len(result.select((startswith('Virtual'), ~endswith('140.30')))) == 2
    assert len(result.select('FilesMatch', deep=True, roots=False)) == 3
    assert len(result.select(('IfModule', '!php5_module'), deep=True, roots=False)) == 6
    assert len(result.select('VirtualHost', ('IfModule', '!php5_module'), roots=False)) == 3
    res = result.select('VirtualHost').select(('IfModule', '!php4_module'), deep=True, roots=False)
    assert len(res) == 3
    assert len(result.select(('VirtualHost', ~is_private))) == 3
    res = result.select(('VirtualHost', in_network('128.39.0.0/16')))
    assert len(res) == 3
    res = result.select(('VirtualHost', ~is_private & in_network('128.39.0.0/16')))
    assert len(res) == 3


def test_directives_and_sections():
    httpd1 = _HttpdConf(context_wrap(HTTPD_CONF_NEST_1, path='/etc/httpd/conf/httpd.conf'))
    httpd2 = _HttpdConf(context_wrap(HTTPD_CONF_NEST_3, path='/etc/httpd/conf.d/00-a.conf'))
    httpd3 = _HttpdConf(context_wrap(HTTPD_CONF_NEST_4, path='/etc/httpd/conf.d/01-b.conf'))
    result = HttpdConfTree([httpd1, httpd2, httpd3])
    assert len(result.directives) == 3
    assert len(result.sections) == 7
    assert len(result.find_all(startswith('Dir')).directives) == 1
    assert len(result.find_all(startswith('Dir')).sections) == 1