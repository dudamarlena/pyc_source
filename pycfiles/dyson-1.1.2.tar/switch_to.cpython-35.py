# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dj/workspace/dyson-py/lib/dyson/modules/core/actions/switch_to.py
# Compiled at: 2016-11-15 02:27:13
# Size of source mod 2**32: 2916 bytes
from six import string_types
from dyson.errors import DysonError
from dyson.utils.module import DysonModule
from dyson.utils.selectors import translate_selector

class SwitchToModule(DysonModule):
    ACTIONS = frozenset(['frame', 'default_content', 'window'])

    def run(self, webdriver, params):
        """
        Collection of switch_to actions with selenium.
        Available actions:
        - switch_to
            - frame <selector>
            - alert
                - action
                    - dismiss
                    - accept
                    - send_keys
                    - authenticate
        :param webdriver:
        :param params:
        :return:
        """
        if isinstance(params, dict):
            if 'frame' in params:
                selector, strategy = translate_selector(params['frame'], webdriver)
                return webdriver.switch_to.frame(selector(strategy))
            if 'alert' in params:
                if 'action' in params['alert']:
                    alert_action = params['alert']['action']
                    valid_actions = frozenset(['accept', 'dismiss', 'authenticate', 'send_keys'])
                    if alert_action in valid_actions:
                        if 'accept' is alert_action:
                            return webdriver.switch_to.alert.accept()
                        if 'dismiss' is alert_action:
                            return webdriver.switch_to.alert.dismiss()
                        if 'get_text' is alert_action:
                            return webdriver.switch_to.alert.text
                    else:
                        raise DysonError('Invalid action "%s". Valid actions are %s' % (
                         alert_action, ','.join(valid_actions)))
                else:
                    if 'username' in params['alert']:
                        username = params['alert']['username']
                        password = ''
                        if params['alert']['password']:
                            password = params['alert']['password']
                        return webdriver.switch_to.alert.authenticate(username, password)
                    else:
                        return webdriver.switch_to.alert()
            else:
                if 'window' in params:
                    return webdriver.switch_to.window(params['window'])
                raise DysonError('Unsure how to switch to "%s". Valid options are %s' % (params, ','.join(self.ACTIONS)))
        elif isinstance(params, string_types):
            if 'default_content' == params:
                return webdriver.switch_to.default_content()
            raise DysonError('Unsure how to switch to "%s". Valid options are %s' % (params, ','.join(self.ACTIONS)))