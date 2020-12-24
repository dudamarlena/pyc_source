# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/autobahntestsuite/report.py
# Compiled at: 2018-12-17 11:51:20
import jinja2, os, sys
__all__ = ('CSS_COMMON', 'CSS_MASTER_REPORT', 'CSS_DETAIL_REPORT', 'JS_MASTER_REPORT',
           'HtmlReport')
CSS_COMMON = '\nbody {\n   background-color: #F4F4F4;\n   color: #333;\n   font-family: Segoe UI,Tahoma,Arial,Verdana,sans-serif;\n}\n\np#intro {\n   font-family: Cambria,serif;\n   font-size: 1.1em;\n   color: #444;\n}\n\np#intro a {\n   color: #444;\n}\n\np#intro a:visited {\n   color: #444;\n}\n\n.block {\n   background-color: #e0e0e0;\n   padding: 16px;\n   margin: 20px;\n}\n\np.case_text_block {\n   border-radius: 10px;\n   border: 1px solid #aaa;\n   padding: 16px;\n   margin: 4px 20px;\n   color: #444;\n}\n\np.case_desc {\n}\n\np.case_expect {\n}\n\np.case_outcome {\n}\n\np.case_closing_beh {\n}\n\npre.http_dump {\n   font-family: Consolas, "Courier New", monospace;\n   font-size: 0.8em;\n   color: #333;\n   border-radius: 10px;\n   border: 1px solid #aaa;\n   padding: 16px;\n   margin: 4px 20px;\n}\n\nspan.case_pickle {\n   font-family: Consolas, "Courier New", monospace;\n   font-size: 0.7em;\n   color: #000;\n}\n\np#case_result,p#close_result {\n   border-radius: 10px;\n   background-color: #e8e2d1;\n   padding: 20px;\n   margin: 20px;\n}\n\nh1 {\n   margin-left: 60px;\n}\n\nh2 {\n   margin-left: 30px;\n}\n\nh3 {\n   margin-left: 50px;\n}\n\na.up {\n   float: right;\n   border-radius: 16px;\n   margin-top: 16px;\n   margin-bottom: 10px;\n\n   margin-right: 30px;\n   padding-left: 10px;\n   padding-right: 10px;\n   padding-bottom: 2px;\n   padding-top: 2px;\n   background-color: #666;\n   color: #fff;\n   text-decoration: none;\n   font-size: 0.8em;\n}\n\na.up:visited {\n}\n\na.up:hover {\n   background-color: #028ec9;\n}\n'
CSS_MASTER_REPORT = '\ntable {\n   border-collapse: collapse;\n   border-spacing: 0px;\n}\n\ntd {\n   margin: 0;\n   border: 1px solid #fff;\n   padding-top: 6px;\n   padding-bottom: 6px;\n   padding-left: 16px;\n   padding-right: 16px;\n   font-size: 0.9em;\n   color: #fff;\n}\n\ntable#agent_case_results {\n   border-collapse: collapse;\n   border-spacing: 0px;\n   border-radius: 10px;\n   margin-left: 20px;\n   margin-right: 20px;\n   margin-bottom: 40px;\n}\n\ntd.outcome_desc {\n   width: 100%;\n   color: #333;\n   font-size: 0.8em;\n}\n\ntr.agent_case_result_row a {\n   color: #eee;\n}\n\ntd.agent {\n   color: #fff;\n   font-size: 1.0em;\n   text-align: center;\n   background-color: #048;\n   font-size: 0.8em;\n   word-wrap: break-word;\n   padding: 4px;\n   width: 140px;\n}\n\ntd.case {\n   background-color: #666;\n   text-align: left;\n   padding-left: 40px;\n   font-size: 0.9em;\n}\n\ntd.case_category {\n   color: #fff;\n   background-color: #000;\n   text-align: left;\n   padding-left: 20px;\n   font-size: 1.0em;\n}\n\ntd.case_subcategory {\n   color: #fff;\n   background-color: #333;\n   text-align: left;\n   padding-left: 30px;\n   font-size: 0.9em;\n}\n\ntd.close {\n   width: 15px;\n   padding: 6px;\n   font-size: 0.7em;\n   color: #fff;\n   min-width: 0px;\n}\n\ntd.case_ok {\n   background-color: #0a0;\n   text-align: center;\n}\n\ntd.case_almost {\n   background-color: #6d6;\n   text-align: center;\n}\n\ntd.case_non_strict, td.case_no_close {\n   background-color: #9a0;\n   text-align: center;\n}\n\ntd.case_info {\n   background-color: #4095BF;\n   text-align: center;\n}\n\ntd.case_unimplemented {\n   background-color: #800080;\n   text-align: center;\n}\n\ntd.case_failed {\n   background-color: #900;\n   text-align: center;\n}\n\ntd.case_missing {\n   color: #fff;\n   background-color: #a05a2c;\n   text-align: center;\n}\n\nspan.case_duration {\n   font-size: 0.7em;\n   color: #fff;\n}\n\n*.unselectable {\n   user-select: none;\n   -moz-user-select: -moz-none;\n   -webkit-user-select: none;\n   -khtml-user-select: none;\n}\n\ndiv#toggle_button {\n   position: fixed;\n   bottom: 10px;\n   right: 10px;\n   background-color: rgba(60, 60, 60, 0.5);\n   border-radius: 12px;\n   color: #fff;\n   font-size: 0.7em;\n   padding: 5px 10px;\n}\n\ndiv#toggle_button:hover {\n   background-color: #028ec9;\n}\n'
CSS_DETAIL_REPORT = '\np.case {\n   color: #fff;\n   border-radius: 10px;\n   padding: 20px;\n   margin: 12px 20px;\n   font-size: 1.2em;\n}\n\np.case_ok {\n   background-color: #0a0;\n}\n\np.case_non_strict, p.case_no_close {\n   background-color: #9a0;\n}\n\np.case_info {\n   background-color: #4095BF;\n}\n\np.case_failed {\n   background-color: #900;\n}\n\ntable {\n   border-collapse: collapse;\n   border-spacing: 0px;\n   margin-left: 80px;\n   margin-bottom: 12px;\n   margin-top: 0px;\n}\n\ntd\n{\n   margin: 0;\n   font-size: 0.8em;\n   border: 1px #fff solid;\n   padding-top: 6px;\n   padding-bottom: 6px;\n   padding-left: 16px;\n   padding-right: 16px;\n   text-align: right;\n}\n\ntd.right {\n   text-align: right;\n}\n\ntd.left {\n   text-align: left;\n}\n\ntr.stats_header {\n   color: #eee;\n   background-color: #000;\n}\n\ntr.stats_row {\n   color: #000;\n   background-color: #fc3;\n}\n\ntr.stats_total {\n   color: #fff;\n   background-color: #888;\n}\n\ndiv#wirelog {\n   margin-top: 20px;\n   margin-bottom: 80px;\n}\n\npre.wirelog_rx_octets {color: #aaa; margin: 0; background-color: #060; padding: 2px;}\npre.wirelog_tx_octets {color: #aaa; margin: 0; background-color: #600; padding: 2px;}\npre.wirelog_tx_octets_sync {color: #aaa; margin: 0; background-color: #606; padding: 2px;}\n\npre.wirelog_rx_frame {color: #fff; margin: 0; background-color: #0a0; padding: 2px;}\npre.wirelog_tx_frame {color: #fff; margin: 0; background-color: #a00; padding: 2px;}\npre.wirelog_tx_frame_sync {color: #fff; margin: 0; background-color: #a0a; padding: 2px;}\n\npre.wirelog_delay {color: #fff; margin: 0; background-color: #000; padding: 2px;}\npre.wirelog_kill_after {color: #fff; margin: 0; background-color: #000; padding: 2px;}\n\npre.wirelog_tcp_closed_by_me {color: #fff; margin: 0; background-color: #008; padding: 2px;}\npre.wirelog_tcp_closed_by_peer {color: #fff; margin: 0; background-color: #000; padding: 2px;}\n'
JS_MASTER_REPORT = '\nvar isClosed = false;\n\nfunction closeHelper(display,colspan) {\n   // hide all close codes\n   var a = document.getElementsByClassName("close_hide");\n   for (var i in a) {\n      if (a[i].style) {\n         a[i].style.display = display;\n      }\n   }\n\n   // set colspans\n   var a = document.getElementsByClassName("close_flex");\n   for (var i in a) {\n      a[i].colSpan = colspan;\n   }\n\n   var a = document.getElementsByClassName("case_subcategory");\n   for (var i in a) {\n      a[i].colSpan = %(agents_cnt)d * colspan + 1;\n   }\n}\n\nfunction toggleClose() {\n   if (window.isClosed == false) {\n      closeHelper("none",1);\n      window.isClosed = true;\n   } else {\n      closeHelper("table-cell",2);\n      window.isClosed = false;\n   }\n}\n'
REPORT_DIR_PERMISSIONS = 504
from zope.interface import implementer
from interfaces import IReportGenerator

@implementer(IReportGenerator)
class HtmlReportGenerator(object):

    def __init__(self, test_db, report_dirname):
        self.test_db = test_db
        self.report_dirname = report_dirname
        env = jinja2.Environment(loader=jinja2.PackageLoader('autobahntestsuite', 'templates'), line_statement_prefix='#', line_comment_prefix='##')
        self.wamp_details_tpl = env.get_template('wamp_details.html')
        self.wamp_index_tpl = env.get_template('wamp_overview.html')
        if not os.path.isdir(report_dirname):
            self.createReportDirectory()

    def writeReportIndexFile(self, runId, file=None):
        raise Exception('implement me')

    def writeReportFile(self, resultId, file=None):
        raise Exception('implement me')

    def createReportDirectory(self):
        """
       Create the directory for storing the reports. If this is not possible,
       terminate the script.
       """
        try:
            os.makedirs(self.report_dirname, REPORT_DIR_PERMISSIONS)
        except OSError as exc:
            print 'Could not create directory: %s' % exc
            sys.exit(1)

    def createReport(self, res, report_filename, readable_test_name, agent, description):
        """
       Create an HTML file called `report_filename` in the
       `report_dirname` directory with details about the test case.
       """
        report_path = os.path.join(self.report_dirname, report_filename)
        try:
            f = open(report_path, 'w')
        except IOError as ex:
            print 'Could not create file %s: %s.' % (report_path, ex)
            return

        try:
            f.write(self.formatResultAsHtml(res, readable_test_name, agent, description))
        except Exception as ex:
            print 'Could not write report: %s.' % ex

        f.close()

    def formatResultAsHtml(self, res, readable_test_name, agent, description):
        """
       Create an HTML document with a table containing information about
       the test outcome.
       """
        html = self.wamp_details_tpl.render(record_list=res[3], test_name=readable_test_name, expected=res[1], observed=res[2], outcome='Pass' if res[0] else 'Fail', agent=agent, description=description)
        return html

    def createIndex(self, reports):
        """
        Create an HTML document with a table containing an overview of all
        tests and links to the detailed documents.
        """
        try:
            with open(os.path.join(self.report_dirname, 'index.html'), 'w') as (f):
                html = self.wamp_index_tpl.render(categories=reports)
                f.write(html)
        except Exception as ex:
            print 'Could not create index file: %s' % ex