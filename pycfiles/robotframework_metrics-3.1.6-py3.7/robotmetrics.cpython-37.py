# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\robotframework_metrics\robotmetrics.py
# Compiled at: 2020-03-14 13:13:17
# Size of source mod 2**32: 36236 bytes
import os, math, smtplib, time, logging
from bs4 import BeautifulSoup
from datetime import datetime
from datetime import timedelta
from robot.api import ExecutionResult
from .test_stats import TestStats
from .keyword_stats import KeywordStats
from .suite_results import SuiteResults
from .test_results import TestResults
from .keyword_results import KeywordResults
try:
    from gevent.pool import Group
    FAILED_IMPORT = False
except ImportError:
    FAILED_IMPORT = True

IGNORE_LIBRARIES = ['BuiltIn', 'SeleniumLibrary', 'String', 'Collections', 'DateTime']
IGNORE_TYPES = ['foritem', 'for']

def generate_report(opts):
    logging.basicConfig(format='%(levelname)s:%(message)s', level=(logging.INFO))
    group = Group() if not FAILED_IMPORT else ''
    logo = opts.logo
    ignore_library = IGNORE_LIBRARIES
    if opts.ignore:
        ignore_library.extend(opts.ignore)
    else:
        ignore_type = IGNORE_TYPES
        if opts.ignoretype:
            ignore_type.extend(opts.ignoretype)
        else:
            path = os.path.abspath(os.path.expanduser(opts.path))
            output_names = []
            if opts.output == '*.xml':
                for item in os.listdir(path):
                    if os.path.isfile(item) and item.endswith('.xml'):
                        output_names.append(item)

            else:
                for curr_name in opts.output.split(','):
                    curr_path = os.path.join(path, curr_name)
                    output_names.append(curr_path)

            log_name = opts.log_name
            required_files = list(output_names)
            missing_files = [filename for filename in required_files if not os.path.exists(filename)]
            if missing_files:
                exit('output.xml file is missing: {}'.format(', '.join(missing_files)))
            else:
                mt_time = datetime.now().strftime('%Y%m%d-%H%M%S')
                if opts.metrics_report_name:
                    result_file_name = opts.metrics_report_name
                else:
                    result_file_name = 'metrics-' + mt_time + '.html'
                result_file = os.path.join(path, result_file_name)
                result = ExecutionResult(*output_names)
                result.configure(stat_config={'suite_stat_level':2,  'tag_stat_combine':'tagANDanother'})
                logging.info('Converting .xml to .html file. This may take few minutes...')
                head_content = '\n    <!DOCTYPE doctype html>\n    <html lang="en">\n\n    <head>\n        <link href="https://png.icons8.com/windows/50/000000/bot.png" rel="shortcut icon" type="image/x-icon" />\n        <title>RF Metrics</title>\n        <meta charset="utf-8" />\n        <meta content="width=device-width, initial-scale=1" name="viewport" />\n        <link href="https://cdn.datatables.net/1.10.19/css/jquery.dataTables.min.css" rel="stylesheet" />\n        <link href="https://cdn.datatables.net/buttons/1.5.2/css/buttons.dataTables.min.css" rel="stylesheet" />\n        <link href="https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/4.1.3/css/bootstrap.min.css" rel="stylesheet" />\n        <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css" rel="stylesheet" />\n        <script src="https://code.jquery.com/jquery-3.3.1.js" type="text/javascript"/>\n        <!-- Bootstrap core Googleccharts -->\n        <script src="https://www.gstatic.com/charts/loader.js" type="text/javascript"/>\n        <script type="text/javascript">\n            google.charts.load(\'current\', {\n                packages: [\'corechart\']\n            });\n        </script>\n        <!-- Bootstrap core Datatable-->\n        <script src="https://cdn.datatables.net/1.10.19/js/jquery.dataTables.min.js" type="text/javascript"></script>\n        <script src="https://cdn.datatables.net/buttons/1.5.2/js/dataTables.buttons.min.js" type="text/javascript"></script>\n        <script src="https://cdnjs.cloudflare.com/ajax/libs/jszip/3.1.3/jszip.min.js" type="text/javascript"></script>\n        <script src="https://cdn.datatables.net/buttons/1.5.2/js/buttons.html5.min.js" type="text/javascript"></script>\n        <script src="https://cdn.datatables.net/buttons/1.5.2/js/buttons.print.min.js" type="text/javascript"></script>\n        <script src="https://cdn.datatables.net/buttons/1.6.1/js/buttons.colVis.min.js" type="text/javascript"></script>\n\n        <style>\n            body {\n                font-family: -apple-system, sans-serif;\n                background-color: #eeeeee;\n            }\n\n            .sidenav {\n                height: 100%;\n                width: 240px;\n                position: fixed;\n                z-index: 1;\n                top: 0;\n                left: 0;\n                background-color: white;\n                overflow-x: hidden;\n            }\n\n            .sidenav a {\n                padding: 12px 10px 8px 12px;\n                text-decoration: none;\n                font-size: 18px;\n                color: Black;\n                display: block;\n            }\n\n            .main {\n                padding-top: 10px;\n            }\n\n            @media screen and (max-height: 450px) {\n                .sidenav {\n                    padding-top: 15px;\n                }\n                .sidenav a {\n                    font-size: 18px;\n                }\n            }\n\n            .wrimagecard {\n                margin-top: 0;\n                margin-bottom: 0.6rem;\n                border-radius: 10px;\n                transition: all 0.3s ease;\n                background-color: #f8f9fa;\n            }\n\n            .rowcard {\n                padding-top: 10px;\n                box-shadow: 12px 15px 20px 0px rgba(46, 61, 73, 0.15);\n                border-radius: 15px;\n                transition: all 0.3s ease;\n                background-color: white;\n            }\n\n            .tablecard {\n                background-color: white;\n                font-size: 15px;\n            }\n\n            tr {\n                height: 40px;\n            }\n\n            .dt-buttons {\n                margin-left: 5px;\n            }\n\n            th, td, tr {\n                text-align:center;\n                vertical-align: middle;\n            }\n\n            .loader {\n                position: fixed;\n                left: 0px;\n                top: 0px;\n                width: 100%;\n                height: 100%;\n                z-index: 9999;\n                background: url(\'https://i.ibb.co/cXnKsNR/Cube-1s-200px.gif\') 50% 50% no-repeat rgb(249, 249, 249);\n            }\n        </style>\n    </head>\n    '
                if opts.ignorekeywords == 'True':
                    hide_keyword = 'hidden'
                else:
                    hide_keyword = ''
                soup = BeautifulSoup(head_content, 'html.parser')
                body = soup.new_tag('body')
                soup.insert(20, body)
                icons_txt = '\n    <div class="loader"></div>\n    <div class="sidenav">\n        <a> <img class="wrimagecard" src="%s" style="height:20vh;max-width:98%%;"/> </a>\n        <a class="tablink" href="#" id="defaultOpen" onclick="openPage(\'dashboard\', this, \'#fc6666\')"><i class="fa fa-dashboard" style="color:CORNFLOWERBLUE"></i> Dashboard</a>\n        <a class="tablink" href="#" onclick="openPage(\'suiteMetrics\', this, \'#fc6666\'); executeDataTable(\'#sm\',5)"><i class="fa fa-th-large" style="color:CADETBLUE"></i> Suite Metrics</a>\n        <a class="tablink" href="#" onclick="openPage(\'testMetrics\', this, \'#fc6666\'); executeDataTable(\'#tm\',3)"><i class="fa fa-list-alt" style="color:PALEVIOLETRED"></i> Test Metrics</a>\n        <a %s class="tablink" href="#" onclick="openPage(\'keywordMetrics\', this, \'#fc6666\'); executeDataTable(\'#km\',3)"><i class="fa fa-table" style="color:STEELBLUE"></i> Keyword Metrics</a>\n        <a class="tablink" href="#" onclick="openPage(\'log\', this, \'#fc6666\');"><i class="fa fa-wpforms" style="color:CHOCOLATE"></i> Logs</a>\n    </div>\n    ' % (logo, hide_keyword)
                body.append(BeautifulSoup(icons_txt, 'html.parser'))
                page_content_div = soup.new_tag('div')
                page_content_div['class'] = 'main col-md-9 ml-sm-auto col-lg-10 px-4'
                body.insert(50, page_content_div)
                logging.info('1 of 4: Capturing dashboard content...')
                test_stats = TestStats()
                result.visit(test_stats)
                total_suite = test_stats.total_suite
                passed_suite = test_stats.passed_suite
                failed_suite = test_stats.failed_suite
                elapsedtime = datetime(1970, 1, 1) + timedelta(milliseconds=(result.suite.elapsedtime))
                elapsedtime = elapsedtime.strftime('%X')
                my_results = result.generated_by_robot
                if my_results:
                    generator = 'Robot'
                else:
                    generator = 'Rebot'
                stats = result.statistics
                total = stats.total.all.total
                passed = stats.total.all.passed
                failed = stats.total.all.failed
                kw_stats = KeywordStats(ignore_library, ignore_type)
                result.visit(kw_stats)
                total_keywords = kw_stats.total_keywords
                passed_keywords = kw_stats.passed_keywords
                failed_keywords = kw_stats.failed_keywords
                dashboard_content = '\n    <div class="tabcontent" id="dashboard">\n        <div id="stats_screenshot_area">\n        <div class="d-flex flex-column flex-md-row align-items-center p-1 mb-3 bg-light border-bottom shadow-sm rowcard">\n            <h5 class="my-0 mr-md-auto font-weight-normal"><i class="fa fa-dashboard"></i> Dashboard</h5>\n            <nav class="my-2 my-md-0 mr-md-3" style="color:#fc6666">\n            <a class="p-2"><b style="color:black;">Execution Time: </b>__TIME__ h</a>\n            <a class="p-2"><b style="color:black;cursor: pointer;" data-toggle="tooltip" title=".xml file is created by">Generated By: </b>__GENERATED-BY__</a>\n            </nav>\n        </div>\n\n        <div class="row rowcard">\n\n            <div class="col-md-4 border-right" onclick="openPage(\'suiteMetrics\', this, \'\')" data-toggle="tooltip" \n                title="Click to view Suite metrics" style="cursor: pointer;">\n                <span style="font-weight:bold; padding-left:5px;color:gray">Suite Statistics:</span>\n                <table style="width:100%;height:200px;text-align: center;">\n                    <tbody>\n                        <tr style="height:60%">\n                            <td>\n                                <table style="width:100%">\n                                    <tbody>\n                                        <tr style="height:100%">\n                                            <td style="font-size:60px; color:#2ecc71">__SPASS__</td>\n                                        </tr>\n                                        <tr>\n                                            <td><span style="color: #999999;font-size:12px">Pass</span></td>\n                                        </tr>\n                                    </tbody>\n                                </table>\n                            </td>\n                        </tr>\n\n                        <tr style="height:25%">\n                            <td>\n                                <table style="width:100%">\n                                    <tbody>\n                                        <tr style="height:70%;font-size:25px" align="center" valign="middle">\n                                            <td style="width: 33%; color:brown">__STOTAL__</td>\n                                            <td style="width: 33%; color:#fc6666">__SFAIL__</td>\n                                        </tr>\n                                        <tr style="height:30%" align="center" valign="top">\n                                            <td style="width: 33%"><span style="color: #999999;font-size:10px">Total</span></td>\n                                            <td style="width: 33%"><span style="color: #999999;font-size:10px">Fail</span></td>\n                                        </tr>\n                                    </tbody>\n                                </table>\n                            </td>\n                        </tr>\n                    </tbody>\n                </table>\n            </div>\n            <div class="col-md-4 borders" onclick="openPage(\'testMetrics\', this, \'\')" data-toggle="tooltip" \n                            title="Click to view Test metrics" style="cursor: pointer;">\n                <span style="font-weight:bold; padding-left:5px;color:gray">Test Statistics:</span>\n                <table style="width:100%;height:200px;text-align: center;">\n                    <tbody>\n                        <tr style="height:60%">\n                            <td>\n                                <table style="width:100%">\n                                    <tbody>\n                                        <tr style="height:100%">\n                                            <td style="font-size:60px; color:#2ecc71">__TPASS__</td>\n                                        </tr>\n                                        <tr>\n                                            <td><span style="color: #999999;font-size:12px">Pass</span></td>\n                                        </tr>\n                                    </tbody>\n                                </table>\n                            </td>\n                        </tr>\n\n                        <tr style="height:25%">\n                            <td>\n                                <table style="width:100%">\n                                    <tbody>\n                                        <tr style="height:70%;font-size:25px" align="center" valign="middle">\n                                            <td style="width: 33%; color:brown">__TTOTAL__</td>\n                                            <td style="width: 33%; color:#fc6666">__TFAIL__</td>\n                                        </tr>\n                                        <tr style="height:30%" align="center" valign="top">\n                                            <td style="width: 33%"><span style="color: #999999;font-size:10px">Total</span></td>\n                                            <td style="width: 33%"><span style="color: #999999;font-size:10px">Fail</span></td>\n                                        </tr>\n                                    </tbody>\n                                </table>\n                            </td>\n                        </tr>\n                    </tbody>\n                </table>\n            </div>\n            <div class="col-md-4 border-left" onclick="openPage(\'keywordMetrics\', this, \'\')" data-toggle="tooltip" \n                            title="Click to view Keyword metrics" style="cursor: pointer;">\n                <span style="font-weight:bold; padding-left:5px;color:gray">Keyword Statistics:</span>\n                <table style="width:100%;height:200px;text-align: center;">\n                    <tbody>\n                        <tr style="height:60%">\n                            <td>\n                                <table style="width:100%">\n                                    <tbody>\n                                        <tr style="height:100%">\n                                            <td style="font-size:60px; color:#2ecc71">__KPASS__</td>\n                                        </tr>\n                                        <tr>\n                                            <td><span style="color: #999999;font-size:12px">Pass</span></td>\n                                        </tr>\n                                    </tbody>\n                                </table>\n                            </td>\n                        </tr>\n\n                        <tr style="height:25%">\n                            <td>\n                                <table style="width:100%">\n                                    <tbody>\n                                        <tr style="height:70%;font-size:25px" align="center" valign="middle">\n                                            <td style="width: 33%; color:brown">__KTOTAL__</td>\n                                            <td style="width: 33%; color:#fc6666">__KFAIL__</td>\n                                        </tr>\n                                        <tr style="height:30%" align="center" valign="top">\n                                            <td style="width: 33%"><span style="color: #999999;font-size:10px">Total</span></td>\n                                            <td style="width: 33%"><span style="color: #999999;font-size:10px">Fail</span></td>\n                                        </tr>\n                                    </tbody>\n                                </table>\n                            </td>\n                        </tr>\n                    </tbody>\n                </table>\n            </div>\n\n        </div>\n        <hr/>\n        <div class="row rowcard">\n            <div class="col-md-4" style="height:280px;width:auto;">\n                <span style="font-weight:bold;color:gray">Suite Status:</span>\n                <div id="suiteChartID" style="height:250px;width:auto;"></div>\n            </div>\n            <div class="col-md-4" style="height:280px;width:auto;">\n                <span style="font-weight:bold;color:gray">Test Status:</span>\n                <div id="testChartID" style="height:250px;width:auto;"></div>\n            </div>\n            <div class="col-md-4" style="height:280px;width:auto;">\n                <span style="font-weight:bold;color:gray">Keyword Status:</span>\n                <div id="keywordChartID" style="height:250px;width:auto;"></div>\n            </div>\n        </div>\n        <hr/>\n        <div class="row rowcard">\n            <div class="col-md-12" style="height:450px;width:auto;">\n                <span style="font-weight:bold;color:gray">Top 10 Suite Performance(sec):</span>\n                <div id="suiteBarID" style="height:400px;width:auto;"></div>\n            </div>\n        </div>\n        <hr/>\n        <div class="row rowcard">\n            <div class="col-md-12" style="height:450px;width:auto;">\n                <span style="font-weight:bold;color:gray">Top 10 Test Performance(sec):</span>\n                <div id="testsBarID" style="height:400px;width:auto;"> </div>\n            </div>\n        </div>\n        <hr/>\n        <div class="row rowcard" __KHIDE__>\n            <div class="col-md-12" style="height:450px;width:auto;">\n                <span style="font-weight:bold;color:gray">Top 10 Keywords Performance(sec):</span>\n                <div id="keywordsBarID" style="height:400px;width:auto;"></div>\n            </div>\n        </div>\n        <div class="row">\n            <div class="col-md-12" style="height:25px;width:auto;">\n                <p class="text-muted" style="text-align:center;font-size:9px">\n                    <a href="https://github.com/adiralashiva8/robotframework-metrics" target="_blank" style="color:gray">robotframework-metrics</a>\n                </p>\n            </div>\n        </div>\n\n       <script>\n            window.onload = function(){\n                executeDataTable(\'#sm\',5);\n                executeDataTable(\'#tm\',3);\n                executeDataTable(\'#km\',3);\n                createPieChart(__SPASS__,__SFAIL__,\'suiteChartID\',\'Suite Status:\');\n                createBarGraph(\'#sm\',0,5,10,\'suiteBarID\',\'Elapsed Time (s) \',\'Suite\');\n                createPieChart(__TPASS__,__TFAIL__,\'testChartID\',\'Tests Status:\');\n                createBarGraph(\'#tm\',1,3,10,\'testsBarID\',\'Elapsed Time (s) \',\'Test\');\n                createPieChart(__KPASS__,__KFAIL__,\'keywordChartID\',\'Keywords Status:\');\n                createBarGraph(\'#km\',1,3,10,\'keywordsBarID\',\'Elapsed Time (s) \',\'Keyword\');\n            };\n       </script>\n       <script>\n            function openInNewTab(url,element_id) {\n                var element_id= element_id;\n                var win = window.open(url, \'_blank\');\n                win.focus();\n                $(\'body\').scrollTo(element_id);\n            }\n        </script>\n    </div>\n    '
                dashboard_content = dashboard_content.replace('__TIME__', str(elapsedtime))
                dashboard_content = dashboard_content.replace('__GENERATED-BY__', str(generator))
                dashboard_content = dashboard_content.replace('__STOTAL__', str(total_suite))
                dashboard_content = dashboard_content.replace('__SPASS__', str(passed_suite))
                dashboard_content = dashboard_content.replace('__SFAIL__', str(failed_suite))
                dashboard_content = dashboard_content.replace('__TTOTAL__', str(total))
                dashboard_content = dashboard_content.replace('__TPASS__', str(passed))
                dashboard_content = dashboard_content.replace('__TFAIL__', str(failed))
                dashboard_content = dashboard_content.replace('__KTOTAL__', str(total_keywords))
                dashboard_content = dashboard_content.replace('__KPASS__', str(passed_keywords))
                dashboard_content = dashboard_content.replace('__KFAIL__', str(failed_keywords))
                dashboard_content = dashboard_content.replace('__KHIDE__', str(hide_keyword))
                page_content_div.append(BeautifulSoup(dashboard_content, 'html.parser'))
                logging.info('2 of 4: Capturing suite metrics...')
                suite_div = soup.new_tag('div')
                suite_div['id'] = 'suiteMetrics'
                suite_div['class'] = 'tabcontent'
                page_content_div.insert(50, suite_div)
                test_icon_txt = '\n                    <h4><b><i class="fa fa-table"></i> Suite Metrics</b></h4>\n                    <hr></hr>\n                    '
                suite_div.append(BeautifulSoup(test_icon_txt, 'html.parser'))
                table = soup.new_tag('table')
                table['id'] = 'sm'
                table['class'] = 'table row-border tablecard'
                suite_div.insert(10, table)
                thead = soup.new_tag('thead')
                table.insert(0, thead)
                tr = soup.new_tag('tr')
                thead.insert(0, tr)
                th = soup.new_tag('th')
                th.string = 'Suite Name'
                tr.insert(0, th)
                th = soup.new_tag('th')
                th.string = 'Status'
                tr.insert(1, th)
                th = soup.new_tag('th')
                th.string = 'Total'
                tr.insert(2, th)
                th = soup.new_tag('th')
                th.string = 'Pass'
                tr.insert(3, th)
                th = soup.new_tag('th')
                th.string = 'Fail'
                tr.insert(4, th)
                th = soup.new_tag('th')
                th.string = 'Time (s)'
                tr.insert(5, th)
                suite_tbody = soup.new_tag('tbody')
                table.insert(11, suite_tbody)
                if group:
                    group.spawn(result.visit, SuiteResults(soup, suite_tbody, log_name))
                else:
                    result.visit(SuiteResults(soup, suite_tbody, log_name))
                test_icon_txt = '\n    <div class="row">\n        <div class="col-md-12" style="height:25px;width:auto;"></div>\n    </div>\n    '
                suite_div.append(BeautifulSoup(test_icon_txt, 'html.parser'))
                logging.info('3 of 4: Capturing test metrics...')
                tm_div = soup.new_tag('div')
                tm_div['id'] = 'testMetrics'
                tm_div['class'] = 'tabcontent'
                page_content_div.insert(100, tm_div)
                test_icon_txt = '\n    <h4><b><i class="fa fa-table"></i> Test Metrics</b></h4>\n    <hr></hr>\n    '
                tm_div.append(BeautifulSoup(test_icon_txt, 'html.parser'))
                table = soup.new_tag('table')
                table['id'] = 'tm'
                table['class'] = 'table row-border tablecard'
                tm_div.insert(10, table)
                thead = soup.new_tag('thead')
                table.insert(0, thead)
                tr = soup.new_tag('tr')
                thead.insert(0, tr)
                th = soup.new_tag('th')
                th.string = 'Suite Name'
                tr.insert(0, th)
                th = soup.new_tag('th')
                th.string = 'Test Case'
                tr.insert(1, th)
                th = soup.new_tag('th')
                th.string = 'Status'
                tr.insert(2, th)
                th = soup.new_tag('th')
                th.string = 'Time (s)'
                tr.insert(3, th)
                th = soup.new_tag('th')
                th.string = 'Error Message'
                tr.insert(4, th)
                test_tbody = soup.new_tag('tbody')
                table.insert(11, test_tbody)
                if group:
                    group.spawn(result.visit, TestResults(soup, test_tbody, log_name))
                else:
                    result.visit(TestResults(soup, test_tbody, log_name))
            test_icon_txt = '\n    <div class="row">\n        <div class="col-md-12" style="height:25px;width:auto;"></div>\n    </div>\n    '
            tm_div.append(BeautifulSoup(test_icon_txt, 'html.parser'))
            logging.info('4 of 4: Capturing keyword metrics...')
            km_div = soup.new_tag('div')
            km_div['id'] = 'keywordMetrics'
            km_div['class'] = 'tabcontent'
            page_content_div.insert(150, km_div)
            keyword_icon_txt = '\n    <h4><b><i class="fa fa-table"></i> Keyword Metrics</b></h4>\n      <hr></hr>\n    '
            km_div.append(BeautifulSoup(keyword_icon_txt, 'html.parser'))
            table = soup.new_tag('table')
            table['id'] = 'km'
            table['class'] = 'table row-border tablecard'
            km_div.insert(10, table)
            thead = soup.new_tag('thead')
            table.insert(0, thead)
            tr = soup.new_tag('tr')
            thead.insert(0, tr)
            th = soup.new_tag('th')
            th.string = 'Test Case'
            tr.insert(1, th)
            th = soup.new_tag('th')
            th.string = 'Keyword'
            tr.insert(1, th)
            th = soup.new_tag('th')
            th.string = 'Status'
            tr.insert(2, th)
            th = soup.new_tag('th')
            th.string = 'Time (s)'
            tr.insert(3, th)
            kw_tbody = soup.new_tag('tbody')
            table.insert(1, kw_tbody)
            if opts.ignorekeywords == 'True':
                pass
            elif group:
                group.spawn(result.visit, KeywordResults(soup, kw_tbody, ignore_library, ignore_type))
                group.join()
            else:
                result.visit(KeywordResults(soup, kw_tbody, ignore_library, ignore_type))
    test_icon_txt = '\n    <div class="row">\n        <div class="col-md-12" style="height:25px;width:auto;"></div>\n    </div>\n    '
    km_div.append(BeautifulSoup(test_icon_txt, 'html.parser'))
    log_div = soup.new_tag('div')
    log_div['id'] = 'log'
    log_div['class'] = 'tabcontent'
    page_content_div.insert(200, log_div)
    test_icon_txt = '\n        <p style="text-align:right">** <b>Report.html</b> and <b>Log.html</b> need to be in current folder in \n        order to display here</p>\n      <div class="embed-responsive embed-responsive-4by3">\n        <iframe class="embed-responsive-item" src=%s></iframe>\n      </div>\n    ' % log_name
    log_div.append(BeautifulSoup(test_icon_txt, 'html.parser'))
    script_text = '\n        <script>\n            function createPieChart(passed_count,failed_count,ChartID,ChartName){\n            var status = [];\n            status.push([\'Status\', \'Percentage\']);\n            status.push([\'PASS\',parseInt(passed_count)],[\'FAIL\',parseInt(failed_count)]);\n            var data = google.visualization.arrayToDataTable(status);\n\n            var options = {\n            pieHole: 0.6,\n            legend: \'none\',\n            chartArea: {width: "95%",height: "90%"},\n            colors: [\'#2ecc71\', \'#fc6666\'],\n            };\n\n            var chart = new google.visualization.PieChart(document.getElementById(ChartID));\n            chart.draw(data, options);\n        }\n        </script>\n        <script>\n           function createBarGraph(tableID,keyword_column,time_column,limit,ChartID,Label,type){\n            var status = [];\n            css_selector_locator = tableID + \' tbody >tr\'\n            var rows = $(css_selector_locator);\n            var columns;\n            var myColors = [\n                \'#4F81BC\',\n                \'#C0504E\',\n                \'#9BBB58\',\n                \'#24BEAA\',\n                \'#8064A1\',\n                \'#4AACC5\',\n                \'#F79647\',\n                \'#815E86\',\n                \'#76A032\',\n                \'#34558B\'\n            ];\n            status.push([type, Label,{ role: \'annotation\'}, {role: \'style\'}]);\n            for (var i = 0; i < rows.length; i++) {\n                if (i == Number(limit)){\n                    break;\n                }\n                //status = [];\n                name_value = $(rows[i]).find(\'td\');\n\n                time=($(name_value[Number(time_column)]).html()).trim();\n                keyword=($(name_value[Number(keyword_column)]).html()).trim();\n                status.push([keyword,parseFloat(time),parseFloat(time),myColors[i]]);\n              }\n              var data = google.visualization.arrayToDataTable(status);\n\n              var options = {\n                legend: \'none\',\n                chartArea: {width: "92%",height: "75%"},\n                bar: {\n                    groupWidth: \'90%\'\n                },\n                annotations: {\n                    alwaysOutside: true,\n                    textStyle: {\n                    fontName: \'Comic Sans MS\',\n                    fontSize: 12,\n                    //bold: true,\n                    italic: true,\n                    color: "black",     // The color of the text.\n                    },\n                },\n                hAxis: {\n                    textStyle: {\n                        //fontName: \'Arial\',\n                        fontName: \'Comic Sans MS\',\n                        fontSize: 10,\n                    }\n                },\n                vAxis: {\n                    gridlines: { count: 10 },\n                    textStyle: {\n                        fontName: \'Comic Sans MS\',\n                        fontSize: 10,\n                    }\n                },\n              };\n\n                // Instantiate and draw the chart.\n                var chart = new google.visualization.ColumnChart(document.getElementById(ChartID));\n                chart.draw(data, options);\n             }\n\n        </script>\n\n     <script>\n      function executeDataTable(tabname,sortCol) {\n        var fileTitle;\n        switch(tabname) {\n            case "#sm":\n                fileTitle = "SuiteMetrics";\n                break;\n            case "#tm":\n                fileTitle =  "TestMetrics";\n                break;\n            case "#km":\n                fileTitle =  "KeywordMetrics";\n                break;\n            default:\n                fileTitle =  "metrics";\n        }\n\n        $(tabname).DataTable(\n            {\n                retrieve: true,\n                "order": [[ Number(sortCol), "desc" ]],\n                dom: \'l<".margin" B>frtip\',\n                buttons: [\n                    {\n                        extend:    \'copyHtml5\',\n                        text:      \'<i class="fa fa-files-o"></i>\',\n                        filename: function() {\n                            return fileTitle + \'-\' + new Date().toLocaleString();\n                        },\n                        titleAttr: \'Copy\',\n                        exportOptions: {\n                            columns: \':visible\'\n                        }\n\t\t\t\t\t},\n\n                    {\n                        extend:    \'csvHtml5\',\n                        text:      \'<i class="fa fa-file-text-o"></i>\',\n                        titleAttr: \'CSV\',\n                        filename: function() {\n                            return fileTitle + \'-\' + new Date().toLocaleString();\n                        },\n                        exportOptions: {\n                            columns: \':visible\'\n                        }\n                    },\n\n                    {\n                        extend:    \'excelHtml5\',\n                        text:      \'<i class="fa fa-file-excel-o"></i>\',\n                        titleAttr: \'Excel\',\n                        filename: function() {\n                            return fileTitle + \'-\' + new Date().toLocaleString();\n                        },\n                        exportOptions: {\n                            columns: \':visible\'\n                        }\n                    },\n                    {\n                        extend:    \'print\',\n                        text:      \'<i class="fa fa-print"></i>\',\n                        titleAttr: \'Print\',\n                        exportOptions: {\n                            columns: \':visible\',\n                            alignment: \'left\',\n                        }\n                    },\n                    {\n                        extend:    \'colvis\',\n                        collectionLayout: \'fixed two-column\',\n                        text:      \'<i class="fa fa-low-vision"></i>\',\n                        titleAttr: \'Hide Column\',\n                        exportOptions: {\n                            columns: \':visible\'\n                        },\n                        postfixButtons: [ \'colvisRestore\' ]\n                    },\n                ],\n                columnDefs: [ {\n                    visible: false,\n                } ]\n            }\n        );\n    }\n     </script>\n    <script>\n      function openPage(pageName,elmnt,color) {\n        var i, tabcontent, tablinks;\n        tabcontent = document.getElementsByClassName("tabcontent");\n        for (i = 0; i < tabcontent.length; i++) {\n            tabcontent[i].style.display = "none";\n        }\n        tablinks = document.getElementsByClassName("tablink");\n        for (i = 0; i < tablinks.length; i++) {\n            tablinks[i].style.color = "";\n        }\n        document.getElementById(pageName).style.display = "block";\n        elmnt.style.color = color;\n\n    }\n    // Get the element with id="defaultOpen" and click on it\n    document.getElementById("defaultOpen").click();\n     </script>\n     <script>\n     // Get the element with id="defaultOpen" and click on it\n    document.getElementById("defaultOpen").click();\n    </script>\n    <script>\n        $(window).on(\'load\',function(){$(\'.loader\').fadeOut();});\n    </script>\n    '
    body.append(BeautifulSoup(script_text, 'html.parser'))
    with open(result_file, 'w') as (outfile):
        outfile.write(soup.prettify())
    logging.info('Results file created successfully and can be found at {}'.format(result_file))