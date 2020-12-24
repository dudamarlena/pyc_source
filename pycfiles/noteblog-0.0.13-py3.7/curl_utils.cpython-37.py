# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/noteblog/fzutils/curl_utils.py
# Compiled at: 2019-05-05 05:26:25
# Size of source mod 2**32: 968 bytes
"""
@author = super_fazai
@File    : curl_utils.py
@connect : superonesfazai@gmail.com
"""
import execjs
__all__ = [
 'curl_cmd_2_py_code']

def curl_cmd_2_py_code(curl_cmd: str) -> str:
    """
    curl cmd to py code
        使用前提:
            $ cd ~ && brew install node && npm install npm@latest -g
            # 下面这个旨在创造package.json(一路回车)
            $ npm init
            # 再装包
            $ npm install --save curlconverter
        github: https://github.com/NickCarneiro/curlconverter
        demo url: https://curl.trillworks.com
    :param curl_cmd:
    :return:
    """
    js = "\n    function a(curl_cmd){\n        var curlconverter = require('curlconverter');\n        var tmp = curlconverter.toPython(curl_cmd);\n        \n        return tmp;\n    }\n    "
    js_parser = execjs.compile(js)
    res = js_parser.call('a', curl_cmd)
    return res