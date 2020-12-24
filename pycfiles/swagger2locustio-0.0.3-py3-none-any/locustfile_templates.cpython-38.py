# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dpoliuha/work/opensource/swagger2locustio/swagger2locustio/templates/locustfile_templates.py
# Compiled at: 2020-05-08 14:29:31
# Size of source mod 2**32: 2160 bytes
"""Module: locustfile templates"""
from jinja2 import Template
MAIN_LOCUSTFILE = Template('from locust import HttpLocust, between\n\nfrom tasksets.generated_taskset import GeneratedTaskSet\n\n\nclass TestUser(HttpLocust):\n    task_set = GeneratedTaskSet\n    wait_time = between(5.0, 9.0)\n    host = "{{ host }}"\n\n')
BASE_TASKSET_FILE = Template('import os\nfrom base64 import b64encode\nfrom locust import TaskSet as LocustTaskSet\n\nfrom tasksets.helper import Helper\n\n\nclass TaskSet(LocustTaskSet):\n\n    def on_start(self):\n        self.login()\n\n    def on_stop(self):\n        pass\n\n    def login(self):{% if not security_cases %}\n        pass{% else %}{{ security_cases }}{% endif %}\n\n    def url(self, _url: str, **kwargs):\n        return _url.format(**kwargs)\n\n    def get_generic_name(self, file):\n        return (\n            "-".join(os.path.realpath(file).split("/")[-3:])\n            .replace("_", "-")\n            .replace(".py", "")\n        )\n\n')
GENERATED_TASKSET_FILE = Template('from tasksets.base import TaskSet\nfrom tasksets.helper import Helper\nfrom constants.base_constants import API_PREFIX\n{% for class_import in test_classes_imports %}{{ class_import }}\n{% endfor %}\n\nclass GeneratedTaskSet(\n    {% for test_class in test_classes_names %}{{ test_class }},\n    {% endfor %}TaskSet\n):\n    pass\n\n')
TEST_CLASS_FILE = Template('from locust import task\n\nfrom tasksets.base import TaskSet\nfrom tasksets.helper import Helper\nfrom constants.base_constants import API_PREFIX\n{% if constants %}from constants.{{ file_name }} import {{ constants }}{% endif %}\n\n\nclass {{ class_name }}(TaskSet):\n{{ test_methods }}\n')
FUNC = Template('\n    @task(1)\n    def {{ func_name }}(self):\n        self.client.{{ method }}(\n            name=self.get_generic_name(__file__),\n            url=self.url("{api_prefix}{{ path }}".format(api_prefix=API_PREFIX{{ path_params }})),\n            params={{ query_params }},\n            headers={{ header_params }},\n            cookies={{ cookie_params }},\n        )\n\n')
PATH_PARAM_PAIR = Template('{{ key }}={{ val }}')
DICT_PARAM_PAIR = Template('"{{ key }}": {{ val }}')