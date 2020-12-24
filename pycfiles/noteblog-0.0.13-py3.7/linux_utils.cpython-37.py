# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/noteblog/fzutils/linux_utils.py
# Compiled at: 2019-05-05 05:26:25
# Size of source mod 2**32: 6240 bytes
import sys, os, subprocess, socket
from platform import system as platform_system
from .common_utils import delete_list_null_str, get_random_int_number
from .time_utils import get_shanghai_time
__all__ = [
 'daemon_init',
 'restart_program',
 'process_exit',
 'kill_process_by_name',
 'get_os_platform',
 'get_random_free_port',
 'get_str_from_command',
 'get_current_file_path',
 'get_system_type']

def daemon_init(stdin='/dev/null', stdout='/dev/null', stderr='/dev/null'):
    """
    杀掉父进程，独立子进程
    :param stdin:
    :param stdout:
    :param stderr:
    :return:
    """
    sys.stdin = open(stdin, 'r')
    sys.stdout = open(stdout, 'a+')
    sys.stderr = open(stderr, 'a+')
    try:
        pid = os.fork()
        if pid > 0:
            os._exit(0)
    except OSError as e:
        try:
            sys.stderr.write('first fork failed!!' + e.strerror)
            os._exit(1)
        finally:
            e = None
            del e

    os.setsid()
    os.chdir('/')
    os.umask(0)
    try:
        pid = os.fork()
        if pid > 0:
            os._exit(0)
    except OSError as e:
        try:
            sys.stderr.write('second fork failed!!' + e.strerror)
            os._exit(1)
        finally:
            e = None
            del e

    sys.stdout.write('Daemon has been created! with pid: %d\n' % os.getpid())
    sys.stdout.flush()


def restart_program():
    """
    初始化避免异步导致log重复打印
    :return:
    """
    import sys, os
    python = sys.executable
    (os.execl)(python, python, *sys.argv)


def process_exit(process_name) -> int:
    """
    判断进程是否存在
    :param process_name:
    :return: 0 不存在 | >= 1 存在
    """
    process_check_response = os.popen('ps aux | grep "' + process_name + '" | grep -v grep').readlines()
    return len(process_check_response)


def kill_process_by_name(process_name) -> None:
    """
    根据进程名杀掉对应进程(linux/mac测试通过!)
    :param process_name: str
    :return:
    """
    if process_exit(process_name) > 0:
        try:
            process_check_response = os.popen('ps aux | grep ' + process_name).readlines()
            for item in process_check_response:
                tmp = delete_list_null_str(item.split(' '))[1]
                os.system('kill -9 {0}'.format(tmp))
                print('该进程名%s, pid = %s, 进程kill完毕!!' % (process_name, tmp))

        except Exception as e:
            try:
                print(e)
            finally:
                e = None
                del e

    else:
        print('进程[%s]不存在' % process_name)


def get_str_from_command(cmd):
    """
    # 执行成功的命令有正常输出,执行不成功的命令得不到输出,得到输出为"",eg.command=which nihao
    # 判断程序有没有已经安装可eg.get_string_from_command("sqlmap --help")
    :param cmd:
    :return:
    """
    return subprocess.getstatusoutput(cmd)[1]


def get_current_file_path():
    """
    # 得到当前文件的绝对路径
    :return:
    """
    tmp_path = os.path.abspath(__file__)
    module_path = tmp_path[:-len(__file__.split('/')[(-1)])]
    return module_path


def get_os_platform() -> str:
    """
    返回当前是什么系统
    :return: mac是darwin | ...
    """
    if '_PYTHON_HOST_PLATFORM' in os.environ:
        return os.environ['_PYTHON_HOST_PLATFORM']
    if sys.platform.startswith('osf1'):
        return 'osf1'
    return sys.platform


def get_random_free_port() -> int:
    """
    从主机中随机获取一个可用端口
    :return:
    """
    free_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    free_socket.bind(('0.0.0.0', 0))
    free_socket.listen(5)
    port = free_socket.getsockname()[1]
    free_socket.close()
    return port


def _get_simulate_logger(retries=10) -> str:
    """
    print仿生log.info
    :return:
    """
    time_str = lambda x='': str(get_shanghai_time()) + ',' + str(get_random_int_number(100, 999)) + ' [INFO  ] ➞ '
    try:
        time_str = time_str()
    except ValueError:
        if retries > 0:
            return _get_simulate_logger(retries - 1)
        return ''

    return time_str


def get_system_type() -> str:
    """
    获取正在使用的系统的类型
    :return: 'Darwin' mac系统 | 'Linux' | ...
    """
    return platform_system()