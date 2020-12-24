# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/sampedro/Documents/Dev/oide-project/dev-env/local/lib/python2.7/site-packages/oide_slurm_assist-0.0.dev1-py2.7.egg/oideslurm/config_utils.py
# Compiled at: 2015-11-02 17:14:55
import oideslurm.settings as app_settings, copy, json
from jsonschema import Draft4Validator

class ConfigLoader:

    @staticmethod
    def getFormConfigs():
        base_schema = app_settings.BASE_CONFIG
        Draft4Validator.check_schema(base_schema)
        form_configs = app_settings.FORM_CONFIGS
        applied = {}
        for k, v in form_configs.iteritems():
            temp = copy.deepcopy(base_schema)
            try:
                temp['required'] = v['required']
            except KeyError:
                pass

            for pk, pv in v['properties'].iteritems():
                temp['properties'][pk].update(pv)

            applied[k] = temp

        return applied