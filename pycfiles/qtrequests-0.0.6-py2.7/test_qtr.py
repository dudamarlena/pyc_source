# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tests/test_qtr.py
# Compiled at: 2014-06-17 00:39:58
import nose
from qtrequests import qtr
from . import utils

def test_get():
    client = qtr.QClient()
    client.addstep_seturl('http://127.0.0.1:8080')
    client.addstep_setrequest('get')
    client.do()
    nose.tools.eq_(client.status(), 200)


def test_get_hostnotfound():
    client = qtr.QClient()
    client.addstep_seturl('http://asdhasbd')
    client.addstep_setrequest('get')
    client.do()
    nose.tools.eq_(client.error(), 3)


def test_get_scrap():
    client = qtr.QClient()
    client.addstep_seturl('http://127.0.0.1:8080/tests/www/')
    client.addstep_setrequest('get')
    client.addstep_setscraper(utils.scrap_scrapme)
    client.do()
    nose.tools.eq_(client.getinternaldata(), 'Hello world!')


def test_get_gotoanotherlink():
    client = qtr.QClient()
    client.addstep_seturl('http://127.0.0.1:8080/tests/www/')
    client.addstep_setrequest('get')
    client.addstep_setscraper(utils.scrap_url)
    client.addstep_seturl(None)
    client.addstep_setrequest('get')
    client.addstep_setscraper(utils.scrap_scrapme)
    client.do()
    nose.tools.eq_(client.getinternaldata(), 'scrap me, page 2')
    return


def test_get_gotoanotherlink_withqueries():
    client = qtr.QClient()
    client.addstep_seturl('http://127.0.0.1:8080/tests/www/')
    client.addstep_setrequest('get')
    client.addstep_setscraper(utils.scrap_url)
    client.addstep_seturl(None, query={'name': 'jorge'})
    client.addstep_setrequest('get')
    client.addstep_setscraper(utils.scrap_scrapme)
    client.do()
    nose.tools.eq_(client.getinternaldata(), 'scrap me, page 2')
    return


def test_thisshouldabort():
    client = qtr.QClient()
    client.addstep_setrequest('ksdhajsdhasdh')
    client.do()


def test_scrapallpages():
    client = qtr.QClient()
    client.addstep_seturl('http://127.0.0.1:8080/tests/www/test2.html')
    client.addstep_setrequest('get')
    client.addstep_setscraperpageurls(utils.scrap_allurl, utils.scrap_scrapmepages)
    client.do()
    nose.tools.eq_(client.getinternaldata(accumulated=True), ['scrap me, page 2',
     'scrap me, page 2',
     'scrap me, page 2',
     'scrap me, page 2'])