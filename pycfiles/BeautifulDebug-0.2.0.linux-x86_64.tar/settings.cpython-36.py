# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cufrancis/Develop/BeautifulDebug/.env/lib/python3.6/site-packages/BeautifulDebug/settings.py
# Compiled at: 2017-10-23 07:31:23
# Size of source mod 2**32: 1836 bytes


class Setting(object):

    def __init__(self, debug=True, date='%Y-%m-%d %H:%M:%S', separator='\n================', show_function=True, content=True):
        self._debug = debug
        self._date = date
        self._separator = separator
        self._show_function = show_function
        self._content = content

    def update(self, *args, **kw):
        """更新配置"""
        for key, value in kw.items():
            if hasattr(self, key):
                setattr(self, key, value)

    @property
    def debug(self):
        return self._debug

    @debug.setter
    def debug(self, value):
        self._debug = bool(value)

    @property
    def date(self):
        """显示时间"""
        return self._date

    @date.setter
    def date(self, value):
        self._date = value

    @property
    def separator(self):
        """
        每条记录之间分隔符,
        如果e设置为 None, 则没有分割符,
        支持字符串, 转义字符
        """
        return self._separator

    @separator.setter
    def separator(self, value):
        self._separator = value

    @property
    def show_function(self):
        """
        每条记录之间分隔符,
        如果e设置为 None, 则没有分割符,
        支持字符串, 转义字符
        """
        return self._show_function

    @show_function.setter
    def show_function(self, value):
        self._show_function = value

    @property
    def content(self):
        """是否显示变量内容"""
        return self._content


if __name__ == '__main__':
    pass