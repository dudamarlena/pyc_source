# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/tezign_zjj/PycharmProjects/autox/autox/model/report.py
# Compiled at: 2019-12-15 03:05:01
# Size of source mod 2**32: 4790 bytes
import os, json, shutil, time, traceback
import autox.core.mylog as log
from autox.model.htmlparser import MyHTMLParser
from shutil import copyfile
import autox
logging = log.track_log()
result = {'testPass':1, 
 'testResult':[
  {'serviceName':'com.test.testcase.TestDemo1', 
   'serviceUrl':'http://test', 
   'methodName':'post', 
   'description':'测试DEMO', 
   'spendTime':'11ms', 
   'status':'成功', 
   'log':[
    'this is demo!']},
  {'serviceName':'com.test.testcase.TestDemo1', 
   'serviceUrl':'http://test', 
   'methodName':'post', 
   'description':'测试DEMO', 
   'spendTime':'11ms', 
   'status':'失败', 
   'log':[
    'this is demo!']}], 
 'testName':'20171109132744898', 
 'testAll':1, 
 'testFail':0, 
 'beginTime':'2017-11-09 13:27:44.917', 
 'totalTime':'11ms', 
 'testSkip':0}

class Report:
    testResultList = []

    def __init__(self):
        self.testResultList = []

    def sum_result(self, scenario, serviceName, methodName, description, spendTime, status, requestlog, resulttlog):
        request_log = []
        result_log = []
        testResultDict = {}
        request_log.append(requestlog)
        result_log.append(resulttlog)
        testResultDict['requestLog'] = request_log
        testResultDict['resultLog'] = result_log
        testResultDict['scenario'] = scenario
        testResultDict['serviceName'] = serviceName
        testResultDict['methodName'] = methodName
        testResultDict['description'] = description
        testResultDict['spendTime'] = spendTime
        testResultDict['status'] = status
        self.testResultList.append(testResultDict)
        return self.testResultList

    def build_report(self, testResult, testName, testAll, testPass, testFail, testSkip, totalTime):
        try:
            reportResult = {}
            reportResult['testPass'] = testPass
            reportResult['testResult'] = testResult
            reportResult['testName'] = testName
            reportResult['testAll'] = testAll
            reportResult['testFail'] = testFail
            reportResult['beginTime'] = time.strftime('%Y-%m-%d %H:%M:%S')
            reportResult['totalTime'] = totalTime
            reportResult['testSkip'] = testAll - testPass - testFail
            reportResult['testCoverage'] = str(round(float(testPass) / float(testAll) * 100, 2)) + '%'
            self.write_report(reportResult, testName)
            htmlparser = MyHTMLParser()
            htmltrs = htmlparser.reporthtmlparser(testResult, '')
            report = htmlparser.report_html.replace('${case_list}', htmltrs).replace('${filterAll}', str(testAll)).replace('${filterOk}', str(testPass)).replace('${filterFail}', str(testFail)).replace('${filterSkip}', str(testAll - testPass - testFail)).replace('${filterCoverage}', str(round(float(testPass) / float(testAll) * 100, 2)) + '%')
            return report
        except Exception as e:
            try:
                logging.error('请求失败%s' % e)
                traceback.print_exc(file=(open(os.getcwd() + '/log/error.log', 'a+')))
            finally:
                e = None
                del e

    def write_report(self, reportResult, testName):
        reportHtmlFileName = testName + '.html'
        reportDirPath = os.path.dirname(os.path.realpath('report')) + '/report/'
        template = open((os.path.dirname(autox.__file__) + '/model/template'), 'r', encoding='UTF-8')
        reportHtml = open(reportHtmlFileName, 'w', encoding='UTF-8')
        for s in template:
            reportHtml.write(s.replace('${resultData}', json.dumps(reportResult)))

        reportHtml.close()
        template.close()
        if os.path.exists(reportDirPath):
            self.move_report(reportHtmlFileName, reportDirPath)
        else:
            os.makedirs(reportDirPath)
            self.move_report(reportHtmlFileName, reportDirPath)

    def move_report(self, fileName, dirPath):
        oldFilePath = os.path.realpath(fileName)
        newFilePath = dirPath + fileName
        shutil.move(oldFilePath, newFilePath)