# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\dartmouthbanner\Banner.py
# Compiled at: 2015-06-09 14:15:19
__author__ = 'Alex Beals'
import requests, re
requests.packages.urllib3.disable_warnings()
landingPage = 'https://login.dartmouth.edu/cas/login?service=https://banner.dartmouth.edu/banner/groucho/twbkwbis.P_WWWLoginWEBAUTH'
login = 'https://websso.dartmouth.edu:443/oam/server/auth_cred_submit'
finalLogin = 'https://banner.dartmouth.edu/banner/groucho/twbkwbis.P_ValLoginWEBAUTH'
cookie = {'domain': 'banner.dartmouth.edu', 'name': 'TESTID', 'value': 'TESTID', 'path': '/banner/groucho', 'secure': False}
redirect = {'Referer': 'https://banner.dartmouth.edu/banner/groucho/twbkwbis.P_GenMenu?name=bmenu.Z_UGSMainMenu'}

class BannerConnection:

    def __init__(self):
        with requests.Session() as (c):
            init = c.get(landingPage, verify=False)
            self.session = c
            self.loggedin = False

    def login(self, username, password):
        if not self.loggedin:
            payload = {'username': username, 'password': password, 'aSubmit': 'Continue'}
            request = self.session.post(login, data=payload, verify=False)
            if 'ticket' in request.url:
                self.loggedin = True
                self.session.cookies.set(**cookie)
                finalRequest = self.session.get(finalLogin, verify=False)
            else:
                self.loggedin = False

    def logout(self):
        if self.loggedin:
            self.__init__()

    def gpa(self):
        if self.loggedin:
            page = self.session.get('https://banner.dartmouth.edu/banner/groucho/zwskogru.P_ViewTermGrde', headers=redirect)
            year = re.search('VALUE="(.*?)" SELECTED', page.text).group(1)
            page2 = self.session.post('https://banner.dartmouth.edu/banner/groucho/zwskogru.P_ViewGrde', data={'term': year}, headers=redirect)
            return float(re.search('(?s).*<p class="rightaligntext">\\s*(.*?)</p>', page2.text).group(1))
        else:
            return False

    def dba(self):
        if self.loggedin:
            page = self.session.get('https://banner.dartmouth.edu/banner/groucho/kap_ar_dash.entry_point', headers=redirect)
            return float(re.search('Dining DBA[\\s\\S]*?<TD>(.*?)</TD>', page.text).group(1))
        else:
            return False

    def addCourse(self, courseID):
        timetable = 'https://banner.dartmouth.edu/banner/groucho/zp_web_add_drop.pz_timetable'
        if self.loggedin:
            page = self.session.get(timetable, headers=redirect)
            term = re.search('<INPUT TYPE = "radio".*?ID="(.*?)".*?CHECKED', page.text).group(1)
            page2 = self.session.post(timetable, headers=redirect, data={'term': term})
            classData = 'term_in=' + term + '&RSTS_IN=DUMMY&assoc_term_in=DUMMY&CRN_IN=DUMMY&start_date_in=DUMMY&end_date_in=DUMMY&SUBJ=DUMMY&CRSE=DUMMY&SEC=DUMMY&LEVL=DUMMY&CRED=DUMMY&GMOD=DUMMY&TITLE=DUMMY&MESG=DUMMY&REG_BTN=DUMMY&RSTS_IN=RW&CRN_IN=' + str(courseID) + '&assoc_term_in=&start_date_in=&end_date_in=&regs_row=0&wait_row=0&add_row=1&REG_BTN=Submit+Changes'
            submit = self.session.post('https://banner.dartmouth.edu/banner/groucho/bwckcoms.P_Regs', data=classData, headers=redirect)
            if 'Maximum number of courses exceeded' in submit.text:
                return 2
            if 'Error occurred while processing registration changes' in submit.text:
                return 3
            if 'Prerequisite not met' in submit.text:
                return 4
            if 'Enrollment Limit Reached' in submit.text:
                return 5
            if 'DUPLICATE ' in submit.text:
                return 6
            if 'Registration Add Errors' in submit.text:
                return 7
            return 1
        else:
            return 0

    def dropCourse(self, courseID):
        timetable = 'https://banner.dartmouth.edu/banner/groucho/zp_web_add_drop.pz_timetable'
        if self.loggedin:
            page = self.session.get(timetable, headers=redirect)
            term = re.search('<INPUT TYPE = "radio".*?ID="(.*?)".*?CHECKED', page.text).group(1)
            page2 = self.session.post(timetable, headers=redirect, data={'term': term})
            classData = 'term_in=' + term + '&RSTS_IN=DUMMY&assoc_term_in=DUMMY&CRN_IN=DUMMY&start_date_in=DUMMY&end_date_in=DUMMY&SUBJ=DUMMY&CRSE=DUMMY&SEC=DUMMY&LEVL=DUMMY&CRED=DUMMY&GMOD=DUMMY&TITLE=DUMMY&MESG=DUMMY&REG_BTN=DUMMY&MESG=DUMMY&RSTS_IN=DW&assoc_term_in=' + term + '&CRN_IN=' + str(courseID) + '&regs_row=1&wait_row=0&add_row=0&REG_BTN=Submit+Changes'
            submit = self.session.post('https://banner.dartmouth.edu/banner/groucho/bwckcoms.P_Regs', data=classData, headers=redirect)
            if 'Can not drop a course which has not been registered' in submit.text:
                return 2
            if 'Registration Add Errors' in submit.text:
                return 3
            return 1
        else:
            return 0