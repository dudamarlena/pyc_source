# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/parallel_run/base_motor.py
# Compiled at: 2014-01-24 00:14:03
from optparse import OptionParser
import os, multiprocessing, signal, sys, traceback
from tools import config2dict, load_module
from base_manager import BaseManager
WILL_RECV = True
SUBPROCESS2MESSAGE = {}

def hook_signal():

    def on_ignore_sig(sn, fo):
        u"""忽略信号处理函数"""
        pass

    def on_sigusr1(sn, fo):
        u"""sigusr1信号处理函数"""
        global WILL_RECV
        WILL_RECV = False

    def on_sigusr2(sn, fo):
        u"""sigusr2信号处理函数"""
        sys.exit(1)

    signal.signal(signal.SIGINT, on_ignore_sig)
    signal.signal(signal.SIGTERM, on_ignore_sig)
    signal.signal(signal.SIGQUIT, on_ignore_sig)
    signal.signal(signal.SIGUSR1, on_sigusr1)
    signal.signal(signal.SIGUSR2, on_sigusr2)


def arg_parse():
    u"""解析命令行参数"""
    options = OptionParser()
    options.add_option('-f', '--config_file', dest='config_file', help='path of config file')
    options, _ = options.parse_args()
    return options


def sync_process(processes):
    global SUBPROCESS2MESSAGE
    for process in processes:
        try:
            print 'process is', process
            print 'message is', SUBPROCESS2MESSAGE[process]
            returns = process.get()
            print 'result is', returns
            print
        except Exception as e:
            traceback.print_exc()


def start():
    u"""启动器"""
    hook_signal()
    options = arg_parse()
    options.logger = multiprocessing.get_logger()
    common_config = config2dict(options.config_file, 'common')
    options.config_file = os.path.abspath(options.config_file)
    main_work_dir = common_config['main_work_dir'].strip('\' "') if 'main_work_dir' in common_config else None
    if main_work_dir is not None and os.path.isdir(main_work_dir):
        os.chdir(main_work_dir)
    sys.path.extend(filter(os.path.isdir, map(lambda p: os.path.abspath(p.strip('" \'')), common_config['main_sys_path'].split(','))) if 'main_sys_path' in common_config else [])
    cur_dir = os.path.abspath(os.curdir)
    if cur_dir not in sys.path:
        sys.path.append(cur_dir)
    manager_path = [common_config['manager_path'].strip('\' "')] if 'manager_path' in common_config else None
    manager_module = common_config['manager_module'].strip('\' "')
    manager_app = common_config['manager_app'].strip('\' "')
    manager = getattr(load_module(manager_module, manager_path), manager_app)
    if not isinstance(manager, BaseManager):
        raise Exception('manager_app should be subclass of BaseManager')
    receiver_path = [common_config['receiver_path'].strip('\' "')] if 'receiver_path' in common_config else None
    receiver_module = common_config['receiver_module'].strip('\' "')
    receiver_app = common_config['receiver_app'].strip('\' "')
    receiver_app_args = common_config['receiver_app_args'].strip('\' "')
    receiver = getattr(load_module(receiver_module, receiver_path), receiver_app)
    receiver_args = getattr(load_module(receiver_module, receiver_path), receiver_app_args)
    assert hasattr(receiver_args, 'args') and hasattr(receiver_args, 'kwargs'), 'receiver_args must have attribute : args and kwargs'
    print 'pid of main process is', os.getpid()
    with open(common_config['pid_file'], 'wb') as (fd):
        fd.write(str(os.getpid()))
    process_pool = multiprocessing.Pool(int(common_config['pool_size']))
    will_sync = int(common_config['will_sync'].strip('\' "'))
    assert will_sync > 0, 'will_sync should be a positive integer'
    processes = []
    while WILL_RECV:
        try:
            messages = receiver(*receiver_args.args, **receiver_args.kwargs)
        except Exception as e:
            print 'error accurs while getting messages :', e
        else:
            for msg in messages:
                options.message = msg
                process = process_pool.apply_async(manager, (options,))
                SUBPROCESS2MESSAGE[process] = msg
                processes.append(process)

            if len(processes) == will_sync:
                sync_process(processes)
                processes = []

    sync_process(processes)
    process_pool.close()
    process_pool.join()
    return


if __name__ == '__main__':
    start()