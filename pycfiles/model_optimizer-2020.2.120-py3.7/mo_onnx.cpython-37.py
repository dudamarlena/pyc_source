# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mo/mo_onnx.py
# Compiled at: 2020-05-04 09:28:53
# Size of source mod 2**32: 950 bytes
"""
 Copyright (C) 2018-2020 Intel Corporation

 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at

      http://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.
"""
import sys
from mo.utils.versions_checker import check_python_version

def main():
    ret_code = check_python_version()
    if ret_code:
        sys.exit(ret_code)
    import mo.main as main
    from mo.utils.cli_parser import get_onnx_cli_parser
    sys.exit(main(get_onnx_cli_parser(), 'onnx'))


if __name__ == '__main__':
    main()