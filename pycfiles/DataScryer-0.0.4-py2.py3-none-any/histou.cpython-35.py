# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\Programmieren\dataScryer\datascryer\histou\histou.py
# Compiled at: 2016-09-01 04:37:42
# Size of source mod 2**32: 4116 bytes
import json, logging, os, subprocess, requests
from datascryer.config import Config
from datascryer.helper.python import python_3
if python_3():
    from urllib.error import URLError
else:
    from urllib2 import URLError

class Histou:
    POST_HEADER = {'User-Agent': "It's me, wget!", 
     'Content-Type': 'application/json'}

    def __init__(self, protocol, address):
        self.protocol = protocol
        self.address = address
        self.schema = json.loads(self.get_json_schema())
        requests.packages.urllib3.disable_warnings()

    def get_config(self, hosts_services):
        json_config = json.dumps(hosts_services)
        if self.protocol == 'http':
            r = requests.post(url=self.address, data=json_config, auth=(
             Config.data['histou']['user'], Config.data['histou']['password']), verify=False, headers=Histou.POST_HEADER)
            if r.status_code != 200:
                raise URLError('Returncode is not 200: ' + str(r.status_code))
            out = r.text
        else:
            if self.protocol == 'file':
                current_dir = os.path.dirname(os.path.realpath(os.getcwd()))
                folder = os.path.split(self.address)[0:-1][0]
                cmd = ['php', os.path.basename(self.address), '--request=' + json_config]
                os.chdir(folder)
                out = subprocess.check_output(cmd).decode('utf8')
                os.chdir(current_dir)
            else:
                logging.getLogger(__name__).error('Undefined Protocol: ' + self.protocol)
                return
        json_object = json.loads(out)
        for o in json_object:
            if o and not self.check_json_object(o[0]):
                return

        return json_object

    @staticmethod
    def get_json_schema():
        return '\n{\n  "$schema": "http://json-schema.org/draft-04/schema#",\n  "type": "array",\n  "items": {\n    "type": "object",\n    "properties": {\n      "label": {\n        "type": "string",\n        "description": "Performancelabel"\n      },\n      "method": {\n        "type": "string",\n        "description": "Method to calc forecast"\n      },\n      "methodSpecificOptions": {\n      },\n      "lookback_range": {\n        "type": "string",\n        "description": "Timebase for forecast",\n        "pattern": "^[0-9]+[smhd]$"\n      },\n      "forecast_range": {\n        "type": "string",\n        "description": "Time to predict",\n        "pattern": "^[0-9]+[smhd]$"\n      },\n      "forecast_interval": {\n        "type": "string",\n        "description": "Time between predicted points.",\n        "pattern": "^[0-9]+[smhd]$"\n      },\n      "update_rate": {\n        "type": "string",\n        "description": "Time between calculations.",\n        "pattern": "^[0-9]+[smhd]$"\n      }\n    },\n    "required": [\n      "label",\n      "method",\n      "methodSpecificOptions",\n      "lookback_range",\n      "forecast_range",\n      "forecast_interval",\n      "update_rate"\n    ]\n  }\n}\n'

    @staticmethod
    def check_json_object(obj):
        required_keys = ['label', 'method', 'methodSpecificOptions', 'lookback_range', 'forecast_range',
         'forecast_interval', 'update_rate']
        for key in required_keys:
            if key not in obj.keys():
                logging.getLogger(__name__).error('JSON Config received from Histou is not valid: ' + str(obj), exc_info=True)
                return False

        return True