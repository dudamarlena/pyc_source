# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/zk_rn_lib_maker/__main__.py
# Compiled at: 2020-01-07 03:45:34
# Size of source mod 2**32: 2242 bytes
import sys, re, os, ezutils.files
lib_name_re = re.compile('^[a-z][a-z0-9|\\-]*[a-z|0-9]$')

def brother_path(file_name):
    return os.path.join(os.path.abspath(os.path.dirname(__file__)), file_name)


def check_lib_name(lib_name):
    return lib_name_re.match(lib_name)


def print_lib_name():
    print('组件名称要求:\n        1. 非数字开头\n        2. 小写字母或数字\n        3. 以中横线作为单词间的分割。\n    ')


def print_using():
    print('\n    zk-rn-lib-maker lib-name\n    lib-name:\n    1. 非数字开头\n    2. 小写字母或数字\n    3. 以中横线(-)作为单词间的分割。\n\n    例如:\n    "zk-rn-lib-maker protocal-view"\n    将会在当前目录下创建名为protocal-view的lib库工程.\n    ')


def print_version():
    version_str = ezutils.files.readstr(brother_path('version.cfg'))
    print(f"zk-rn-lib-maker:{version_str}")


def result_of_cmd(cmd):
    r = os.popen(cmd)
    text = r.read()
    r.close()
    return text


def is_rn_create_lib_installed():
    result = result_of_cmd('npm ls react-native-create-library -g|grep empty')
    return len(result) == 0


def print_install_rn_create_lib():
    print('请先安装react-native-create-library：\n\n    npm install -g react-native-create-library\n    ')


def main():
    if not is_rn_create_lib_installed():
        print_install_rn_create_lib()
        return
    else:
        arg_count = len(sys.argv)
        if arg_count < 2:
            print_using()
            return
        lib_name = sys.argv[1]
        if lib_name == '-h':
            print_using()
            return
        if lib_name == '-v':
            print_version()
            return
        check_lib_name(lib_name) or print_lib_name()
        return
    android_id = f"com.smartstudy.{lib_name.replace('-', '')}"
    cmd = f'react-native-create-library {lib_name} --module-prefix "@zhike-private/rn" --package-identifier "{android_id}" && rm -rf ./{lib_name}/windows'
    os.system(cmd)


if __name__ == '__main__':
    main()