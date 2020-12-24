# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_mysqladmin.py
# Compiled at: 2019-11-14 13:57:46
import pytest, doctest
from insights.parsers import ParseException, SkipException, mysqladmin
from insights.parsers.mysqladmin import MysqladminVars, MysqladminStatus
from insights.tests import context_wrap
OUTPUT_MYSQLADMIN_STATUS = ('\nUptime: 1103965 Threads: 1820 Questions: 44778091 Slow queries: 0 Opens: 1919 Flush tables: 1 Open tables: 592 Queries per second avg: 40.561\n').strip()
BLANK_SAMPLE = ('\n').strip()
BAD_INPUT_SAMPLE = ('\nThreads: 1820 Questions: 44778091 Slow queries: 0 Opens: 1919 Flush tables: 1 Open tables: 592 Queries per second avg: 40.561\n').strip()

def test_mysqladmin_status():
    parser_result = MysqladminStatus(context_wrap(OUTPUT_MYSQLADMIN_STATUS))
    mysqlstat = parser_result.status
    assert parser_result is not None
    assert mysqlstat['Threads'] == '1820'
    assert mysqlstat['Queries per second avg'] == '40.561'
    assert mysqlstat['Uptime'] == '1103965'
    assert mysqlstat['Opens'] == '1919'
    assert mysqlstat['Slow queries'] == '0'
    return


def test_mysqlstat_blank_input():
    with pytest.raises(SkipException) as (sc):
        MysqladminStatus(context_wrap(BLANK_SAMPLE))
    assert 'Content is empty.' in str(sc.value)


def test_mysqlstat_bad_input():
    with pytest.raises(ParseException) as (exc):
        MysqladminStatus(context_wrap(BAD_INPUT_SAMPLE))
    assert 'Unable to parse the output.' in str(exc)


INPUT_NORMAL = ('\n+---------------------------------------------------+-------------------\n| Variable_name                                     | Value            |\n+---------------------------------------------------+------------------+\n| aria_block_size                                   | 8192             |\n| aria_checkpoint_interval                          | 30               |\n| auto_increment_increment                          | 1                |\n| auto_increment_offset                             | 1                |\n| binlog_stmt_cache_size                            | 32768            |\n| character_set_filesystem                          | binary           |\n| datadir                                           | /var/lib/mysql/  |\n| init_file                                         |                  |\n| innodb_autoinc_lock_mode                          | 1                |\n| version                                           | 5.5.56-MariaDB   |\n| version_comment                                   | MariaDB Server   |\n| version_compile_machine                           | x86_64           |\n| version_compile_os                                | Linux            |\n| wait_timeout                                      | 28800            |\n+---------------------------------------------------+------------------+\n').strip()

def test_mysqladmin_vars():
    res = MysqladminVars(context_wrap(INPUT_NORMAL))
    d = res.data
    assert len(list(d)) == 14
    assert d['version_comment'] == 'MariaDB Server'
    assert d['datadir'] == '/var/lib/mysql/'
    assert d['auto_increment_increment'] == '1'
    assert d.get('abc') is None
    assert res.get('abc', '233') == '233'
    assert res.get('init_file') == ''
    assert res.get('wait_what') is None
    assert res.get('wait_timeout') == '28800'
    assert res.getint('wait_timeout') == 28800
    assert res.getint('version_compile_machine') is None
    assert res.get('binlog_stmt_cache_size', '666') == '32768'
    with pytest.raises(TypeError) as (e_info):
        res.getint('binlog_stmt_cache_size', '666')
    assert 'Default value should be int type.' in str(e_info.value)
    return


INPUT_EMPTY = ('\n+-------------------------------------------------+------------------+\n| Variable_name                                   | Value            |\n+-------------------------------------------------+------------------+\n+-------------------------------------------------+------------------+\n').strip()
INPUT_FORAMT_WRONG = ('\n+-------------------------------------------------+------------------+\n| Variable_name                                   | Value            |\n+-------------------------------------------------+------------------+\n| aria_block_size                                 | 1                |\n| version_compile_machine                          x86_64           |\n| version_compile_machine                         | x86_64           |x\n| old_password********                                     ********\n| version_compile_machine                           | x86_64           |\n+-------------------------------------------------+------------------+\n').strip()

def test_empty_mysqladmin_var():
    with pytest.raises(SkipException) as (e_info):
        MysqladminVars(context_wrap(''))
    assert 'Empty content.' in str(e_info.value)


def test_wrong_mysqladmin_var():
    with pytest.raises(ParseException) as (e_info):
        MysqladminVars(context_wrap(INPUT_EMPTY))
    assert 'Variable_name' in str(e_info.value)


INPUT_STILL_PARSABLE_1 = ('\n+-------------------------------------------------+------------------+\n| Variable_name                                   | Value            |\n+-------------------------------------------------+------------------+\n| aria_block_size                                 | 1                |\n| aria_checkpoint_interval                        | 30   |    23     |\n+-------------------------------------------------+------------------+\n').strip()
INPUT_STILL_PARSABLE_2 = ('\n+---------------------------------------------------+-------------------\n| Variable_name                                     | Value            |\n+---------------------------------------------------+------------------+\n| aria_block_size                                   | 8192             |\n| aria_checkpoint_interval                          | 30               |\n| ft_boolean_syntax                                 | + -><()~*:""&|   |\n| version_compile_machine                           | x86_64           |\n| version_compile_os                                | Linux            |\n+---------------------------------------------------+------------------+\n').strip()
INPUT_FORAMT_WRONG = ('\n+-------------------------------------------------+------------------+\n| Variable_name                                   | Value            |\n+-------------------------------------------------+------------------+\n| aria_block_size                                 | 1                |\n| version_compile_machine                          x86_64           |\n| version_compile_machine                         | x86_64           |x\n| old_password********                                     ********\n| version_compile_machine                           | x86_64           |\n+-------------------------------------------------+------------------+\n').strip()

def test_mysqladmin_still_parsable():
    res = MysqladminVars(context_wrap(INPUT_STILL_PARSABLE_1))
    d = res.data
    assert d['aria_checkpoint_interval'] == '30   |    23'
    res = MysqladminVars(context_wrap(INPUT_STILL_PARSABLE_2))
    d = res.data
    assert d['ft_boolean_syntax'] == '+ -><()~*:""&|'
    res = MysqladminVars(context_wrap(INPUT_FORAMT_WRONG))
    assert len(res.bad_lines) == 3
    assert res.bad_lines[1] == '| version_compile_machine                         | x86_64           |x'


def test_doc():
    env = {'MysqladminStatus': MysqladminStatus, 
       'result': MysqladminStatus(context_wrap(OUTPUT_MYSQLADMIN_STATUS, path='/bin/mysqladmin status')), 
       'MysqladminVars': MysqladminVars, 
       'output': MysqladminVars(context_wrap(INPUT_NORMAL, '/bin/mysqladmin variables'))}
    failed, total = doctest.testmod(mysqladmin, globs=env)
    assert failed == 0