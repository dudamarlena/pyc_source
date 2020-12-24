# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.8-x86_64/egg/vint/file_util.py
# Compiled at: 2013-04-19 06:08:22
from __future__ import unicode_literals
import json, logging, os, codecs
__author__ = b'tchen'
logger = logging.getLogger(__name__)
FIRST_EXTENSIONS = [
 b'.h']
INSTRUCTION_FILE = b'README'
EXAM_CONFIG_FILE = b'.interview.json'
CASE_CONFIG_FILE = b'.case.json'
EXAM_INSTRUCTION_TEMPLATE = b'\nHello %(applicant)s, Welcome to exam %(name)s\n\n%(description)s\n\nInstructions:\n\n1. Write the code as fast as you can. Optimize when you have further time.\n2. Verify the correctness and robustness of your code with proper output.\n3. When you finish the exam, please go back to this directory (where you see this file), and execute "vint finish".\n    This is very important to do so since we will time your exam and submit your result back to the hiring manager.\n\nStart your journey now, pal!\n\n'
CASE_INSTRUCTION_TEMPLATE = b"\n\nCase%(position)d: %(name)s\n\n%(description)s\n\nInstructions:\n\n1. You need to code in %(lang)s, with acceptable extentisons: %(extentions)s.\n2. You'd better to write down the code inside one file unless you find it is not readable.\n"

def write_file(filename, content):
    f = codecs.open(filename, b'w+', encoding=b'utf8')
    f.write(content)
    f.close()


class Template(object):

    @staticmethod
    def create_exam_config(exam_path, interview):
        filename = os.path.join(os.getcwd(), exam_path, EXAM_CONFIG_FILE)
        content = json.dumps(interview)
        write_file(filename, content)

    @staticmethod
    def create_exam_instruction(exam_path, interview, exam):
        filename = os.path.join(os.getcwd(), exam_path, INSTRUCTION_FILE)
        content = EXAM_INSTRUCTION_TEMPLATE % {b'applicant': interview[b'applicant'], 
           b'name': exam[b'name'], 
           b'description': exam[b'description']}
        write_file(filename, content)

    @staticmethod
    def create_case_config(case_path, case):
        filename = os.path.join(case_path, CASE_CONFIG_FILE)
        content = json.dumps(case)
        write_file(filename, content)

    @staticmethod
    def create_case_instruction(case_path, case):
        instruction = os.path.join(case_path, INSTRUCTION_FILE)
        content = CASE_INSTRUCTION_TEMPLATE % {b'position': case[b'position'], 
           b'name': case[b'name'], 
           b'description': case[b'description'], 
           b'lang': case[b'lang'], 
           b'extentions': case[b'extentions']}
        write_file(instruction, content)

    @staticmethod
    def create_case_code(case_path, case):
        ext = case[b'extentions'].split(b',')[0].strip()
        filename = os.path.join(case_path, b'main%s' % ext)
        write_file(filename, case[b'code'])


class FileUtil(object):

    @staticmethod
    def read_content(filename):
        return codecs.open(filename, b'r', encoding=b'utf8').read()

    @staticmethod
    def get_valid_files(path, extentions):
        first_list = []
        second_list = []
        normal_list = []
        for root, dirs, files in os.walk(path):
            for f in files:
                for ext in extentions:
                    if f.endswith(ext):
                        normal_list.append(f)
                        break

        for f in normal_list:
            for ext in FIRST_EXTENSIONS:
                if f.endswith(ext):
                    first_list.append(f)
                    break
            else:
                second_list.append(f)

        return (
         first_list, second_list)

    @staticmethod
    def read_case(path):
        return FileUtil.read_json(path, CASE_CONFIG_FILE)

    @staticmethod
    def read_json(path, name):
        filename = os.path.join(path, name)
        return json.load(codecs.open(filename, b'r', encoding=b'utf8'))

    @staticmethod
    def read_interview(path):
        return FileUtil.read_json(path, EXAM_CONFIG_FILE)

    @staticmethod
    def interview_exists():
        return os.path.exists(EXAM_CONFIG_FILE)