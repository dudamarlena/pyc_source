# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\pyWebFramework\core\settings.py
# Compiled at: 2019-11-01 23:14:39
# Size of source mod 2**32: 424 bytes


class Settings:
    ROOT = ''
    TAX_INIT_SAMPLE_ROOT = ''
    TEMPLATE_FILE_ROOT = ''

    def load_settings(self, mod):
        for setting in dir(mod):
            if not setting.isupper():
                continue
            setting_value = getattr(mod, setting)
            if setting in dir(self):
                setattr(self, setting, setting_value)


settings = Settings()