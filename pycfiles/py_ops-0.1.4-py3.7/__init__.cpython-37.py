# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\pyops\__init__.py
# Compiled at: 2020-04-17 12:21:38
# Size of source mod 2**32: 5106 bytes
import os, json, jinja2, optparse, subprocess
from logging.config import dictConfig
__version__ = '0.1.4'
dictConfig({'version':1, 
 'formatters':{'default': {'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'}}, 
 'handlers':{'console':{'class':'logging.StreamHandler', 
   'level':'INFO', 
   'formatter':'default'}, 
  'file':{'class':'logging.FileHandler', 
   'filename':os.path.join(os.getcwd(), './std.log'), 
   'level':'DEBUG', 
   'formatter':'default', 
   'encoding':'utf-8'}}, 
 'root':{'level':'DEBUG', 
  'handlers':[
   'console', 'file']}})
__TMPL__ = '# -*- coding: utf-8 -*- \nimport pytest\nimport logging\nfrom pyops.main import *\n\nlogger = logging.getLogger()\n\n# 打全局标签，比如功能模块标签\npytestmark = pytest.mark.{{ tag }}\n\n\nclass {{ class }}:{% for case in cases %}\n    def {{ case }}(self, class_init, class_dest, init, dest, test_data, test_flow, test_check):\n        pass\n{% endfor %}\n\nif __name__ == "__main__":\n    pytest.main(["-s", "{{ module }}.py", "--pytest_report", "report.html"])\n\n'
__INI_TMPL__ = '[pytest]\nmarkers = {% for tag in tags %}\n    {{ tag }}\n{% endfor %}\n'
__JSON_TMPL__ = '{\n    "name": "TestDemo",\n    "desc": ".....background......",\n    "tag": "smoking_test",\n    "setup_class": [],\n    "teardown_class": [],\n    "setup": [],\n    "teardown": [],\n    "cases": {\n        "test_add": {\n            "desc": "",\n            "tags": [],\n            "data": {\n                "x": 2,\n                "y": 3,\n                "expect": 5\n            },\n            "flow": ["调用add"],\n            "check": ["检查add"]\n        }\n    }\n}\n'
__INIT_TMPL__ = 'import logging\nfrom pyops.decorator import (make_check, make_flow, alias)\n\nlogger = logging.getLogger()\n\ndef add(x, y):\n    print(\'add\')\n    return x + y\n\n@alias(\'调用add\')\n@make_flow\ndef call_add(data):\n    """\n        data: 即json配置文件中的case节点下对应data字典对象\n    """\n    data[\'actual\'] = add(data[\'x\'], data[\'y\'])\n\n@alias(\'检查add\')\n@make_check\ndef check_add(data):\n    """\n        data: 即json配置文件中的case节点下对应data字典对象\n    """\n    return data[\'actual\'] == data[\'expect\']\n'

def run(args):
    case_files = make(args)
    args = ['pytest'] + case_files + ['-s', '-v--pytest_report', 'report.html']
    subprocess.call(args)


def force_run(args):
    case_files = make(args)
    args = ['pytest'] + case_files + ['-s', '-v', '--force_run', '--pytest_report', 'report.html']
    subprocess.call(args)


def make(args):
    files = args[1:] if len(args) > 1 else get_files()
    all_tags = []
    case_files = []
    for file in files:
        with open((os.path.join(os.getcwd(), file)), 'r', encoding='utf8') as (fr):
            json_data = json.load(fr)
            all_tags.append(json_data['tag'])
            content = gen_template_file({'module':file.replace('.json', ''), 
             'class':json_data['name'], 
             'tag':json_data['tag'], 
             'cases':[case for case in json_data['cases']]}, __TMPL__)
            case_file = file.replace('.json', '.py')
            case_files.append(case_file)
            with open((os.path.join(os.getcwd(), case_file)), 'w', encoding='utf8') as (fw):
                fw.write(content)

    with open((os.path.join(os.getcwd(), 'pytest.ini')), 'w', encoding='utf8') as (fw):
        content = gen_template_file({'tags': set(all_tags)}, __INI_TMPL__)
        fw.write(content)
    return case_files


def start_project(args):
    project_name = args[1]
    os.makedirs(project_name)
    os.makedirs(os.path.join(project_name, 'ah_ext'))
    with open((os.path.join(project_name, 'ah_ext', '__init__.py')), 'w', encoding='utf-8') as (f):
        f.write(__INIT_TMPL__)
    with open((os.path.join(project_name, 'demo.json')), 'w', encoding='utf-8') as (f):
        f.write(__JSON_TMPL__)
    print(f"创建项目 {project_name} 成功!")


def get_files():
    sub_files = os.listdir(os.getcwd())
    return [sub_file for sub_file in sub_files if sub_file.endswith('json')]


def gen_template_file(data, temp_str):
    template = jinja2.Template(temp_str)
    return template.render(data)


def main():
    usage = 'USAGE: pyops run|make|forcerun|startproject projectname'
    op = optparse.OptionParser(usage=usage)
    option, args = op.parse_args()
    if len(args) < 1:
        op.print_help()
        exit(1)
    else:
        action = args[0]
        if action == 'run':
            run(args)
        else:
            if action == 'make':
                make(args)
            else:
                if action == 'forcerun':
                    force_run(args)
                else:
                    if action == 'startproject':
                        if len(args) < 2:
                            print('[ERROR] startproject common must have a arg')
                            op.print_help()
                        else:
                            start_project(args)
                    else:
                        op.print_help()


if __name__ == '__main__':
    main()