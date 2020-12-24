# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.8-x86_64/egg/vint/vint.py
# Compiled at: 2013-04-19 06:08:34
from __future__ import unicode_literals
import logging, os
from cerf_api import Cerf
from file_util import Template, FileUtil
from misc import calc_time_spent
__author__ = b'tchen'
logger = logging.getLogger(__name__)

class InterviewManager(object):

    def __init__(self, id=None):
        self.id = id
        if self.id:
            self.exam_path = b'exam%s' % self.id
        else:
            self.exam_path = None
        self.code = None
        self.interview = None
        self.exam_id = None
        self.cerf_api = None
        return

    def generate_environment(self):
        os.mkdir(self.exam_path)
        Template.create_exam_config(os.path.join(os.getcwd(), self.exam_path), self.interview)
        exam = self.cerf_api.exam.retrieve(self.exam_id)
        if len(exam) == 0:
            print b'Can not retrieve proper exam by id %s. Please contact your hiring manager.' % self.exam_id
            exit(-1)
        Template.create_exam_instruction(self.exam_path, self.interview, exam)
        for case in exam[b'cases']:
            self.generate_case(case)

    def generate_case(self, case):
        os.mkdir(b'%s/case%s' % (self.exam_path, case[b'position']))
        path = os.path.join(os.getcwd(), self.exam_path, b'case%s' % str(case[b'position']))
        Template.create_case_config(path, case)
        Template.create_case_instruction(path, case)
        Template.create_case_code(path, case)

    def start(self):
        code = raw_input(b'Please provide your authentication code:')
        self.code = code
        self.cerf_api = Cerf(self.id, code)
        data = self.cerf_api.interview.start()
        if len(data) == 0:
            print b'Can not retrieve proper interview by id %s. Please contact your hiring manager.' % self.id
            exit(-1)
        if calc_time_spent(data[b'started']) > 1 or os.path.exists(self.exam_path):
            print b'This interview has been started already!'
            exit(-1)
        self.interview = data
        self.exam_id = self.interview[b'exam']
        print b'Nice to meet you, %s! Thanks for your interest in Juniper China R&D.' % data[b'applicant']
        print b'Creating the exam environment...',
        self.generate_environment()
        print b'Done!\nYou can "cd %s" to start your exam now.' % self.exam_path

    def load_data(self, interview):
        self.id = interview[b'id']
        self.code = interview[b'authcode']
        self.interview = interview
        self.exam_id = interview[b'exam']
        self.exam_path = b'exam%d' % self.exam_id

    def submit_case(self, case):
        path = os.path.join(os.getcwd(), b'case%s' % case[b'position'])
        print b'\tSubmit case%s...' % case[b'position'],
        extentions = [ ext.strip() for ext in case[b'extentions'].split(b',') ]
        first_list, second_list = FileUtil.get_valid_files(path, extentions)
        content = b''
        for name in first_list + second_list:
            s = b'/* %s */\n\n%s' % (name, FileUtil.read_content(os.path.join(path, name)))
            content += s

        data = {b'interview': self.id, 
           b'applicant': self.interview[b'applicant_id'], 
           b'case': case[b'cid'], 
           b'content': content}
        if not self.cerf_api.answer.create(data):
            print b'Cannot submit case%s, please contact your hiring manager.' % case[b'position']
        else:
            print b'Done!'

    def submit_cases(self):
        path = os.getcwd()
        for root, dirs, files in os.walk(b'.'):
            for d in dirs:
                if d.startswith(b'case'):
                    config = FileUtil.read_case(os.path.join(path, d))
                    self.submit_case(config)

    def finish_interview(self):
        data = self.cerf_api.interview.finish()
        if len(data) == 0:
            print b'Can not finish interview by id %s. Please contact your hiring manager.' % self.id
            exit(-1)

    def finish(self):
        if not FileUtil.interview_exists():
            print b'Please change to the root of the exam directory, then execute this command again.'
            exit(-1)
        interview = FileUtil.read_interview(b'.')
        self.cerf_api = Cerf(interview[b'id'], interview[b'authcode'])
        interview = self.cerf_api.interview.retrieve(interview[b'id'])
        self.load_data(interview)
        if interview[b'time_spent']:
            print b'Your exam is over. Please stay tuned.'
            exit(-1)
        spent = calc_time_spent(interview[b'started'])
        print b'Thank you! Your exam is done! Total time spent: %d minutes.' % spent
        print b'Submitting your code to generate report...'
        self.submit_cases()
        print b'Done!'
        print b'Notifying the hiring manager...',
        self.finish_interview()
        print b'Done!'
        print b'Please wait for a short moment. If no one comes in 5m, please inform frontdesk.'


def main(arguments):
    is_finish = arguments[b'finish']
    is_start = arguments[b'start']
    if is_finish:
        InterviewManager().finish()
    elif is_start:
        try:
            id = int(arguments[b'<id>'])
        except:
            print b'Interview id is not valid. Please contact your hiring manager.'
            exit(-1)

        InterviewManager(id).start()
    else:
        print b'Please specify a correct command.'