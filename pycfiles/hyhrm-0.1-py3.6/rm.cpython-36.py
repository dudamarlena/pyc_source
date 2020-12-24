# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/hyhrm/rm.py
# Compiled at: 2019-06-19 01:51:54
# Size of source mod 2**32: 1242 bytes
import time, sys, os, shutil, logging
PATH_TRASH = '~/trash'
logging.basicConfig(level=(logging.INFO), format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    """

    myrm file1 file2 file3
    myrm dir1
    argv[0]: myrm
    argv[1]: file1
    argv[2]: file2
    argv[3]: file3
    ...
    os.path: 处理目录相关操作
    time.time(): 获取系统时间
    :return:
    """
    if len(sys.argv) < 2:
        logging.info('this tool like rm')
        logging.info(sys.argv[0], ' file1 ')
    for arg_file in sys.argv[1:]:
        if arg_file in ('/', '.'):
            logging.info("sb, don't rm  filename: {}".format(arg_file))
            return
        filename = str(time.time()).split('.')[0] + arg_file
        logging.debug('newfile:{}'.format(os.path.join(PATH_TRASH, filename)))
        shutil.move(arg_file, os.path.join(PATH_TRASH, filename))


if __name__ == '__main__':
    if not os.path.exists(PATH_TRASH):
        os.mkdir(PATH_TRASH)
    main()