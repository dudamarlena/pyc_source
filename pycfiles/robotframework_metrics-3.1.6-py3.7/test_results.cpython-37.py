# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\robotframework_metrics\test_results.py
# Compiled at: 2020-03-14 12:58:26
# Size of source mod 2**32: 1706 bytes
from robot.api import ResultVisitor

class TestResults(ResultVisitor):

    def __init__(self, soup, tbody, logname):
        self.soup = soup
        self.tbody = tbody
        self.log_name = logname

    def visit_test(self, test):
        table_tr = self.soup.new_tag('tr')
        self.tbody.insert(0, table_tr)
        table_td = self.soup.new_tag('td', style='word-wrap: break-word;max-width: 200px; white-space: normal; text-align:left')
        table_td.string = str(test.parent)
        table_tr.insert(0, table_td)
        table_td = self.soup.new_tag('td', style='word-wrap: break-word;max-width: 250px; white-space: normal;cursor: pointer; color:blue; text-align:left')
        table_td.string = str(test)
        table_td['onclick'] = "openInNewTab('%s%s%s','%s%s')" % (self.log_name, '#', test.id, '#', test.id)
        table_td['data-toggle'] = 'tooltip'
        table_td['title'] = "Click to view '%s' logs" % test
        table_tr.insert(1, table_td)
        test_status = str(test.status)
        if test_status == 'PASS':
            table_td = self.soup.new_tag('td', style='color: green')
            table_td.string = test_status
        else:
            table_td = self.soup.new_tag('td', style='color: red')
            table_td.string = test_status
        table_tr.insert(2, table_td)
        table_td = self.soup.new_tag('td')
        table_td.string = str(test.elapsedtime / float(1000))
        table_tr.insert(3, table_td)
        table_td = self.soup.new_tag('td', style='word-wrap: break-word;max-width: 250px; white-space: normal;text-align:left')
        table_td.string = test.message
        table_tr.insert(4, table_td)