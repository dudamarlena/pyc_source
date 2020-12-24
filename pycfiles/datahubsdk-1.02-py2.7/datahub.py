# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sdktool/datahub.py
# Compiled at: 2020-04-07 04:46:20
from util.utils import *
from upload import *
from checkout import *
from optparse import OptionParser
import json, pprint, traceback, sys, ConfigParser, fcntl, logging
logging.basicConfig(level=logging.ERROR, format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
reload(sys)
sys.setdefaultencoding('utf8')

def getusage():
    usage1 = 'usage: %prog [Options] arg1 [Options] arg2 ...'


def demoArgs():
    parser = OptionParser(usage=getusage())
    parser.add_option('-c', '--checkout', action='store', dest='version', help='根据version来checkout')
    parser.add_option('--project', action='store', dest='project', help='project_id,checkout时必须')
    parser.add_option('-s', '--softlink', action='store_true', dest='softlink', help='checkout需要创建软链')
    parser.add_option('--mnt', action='store', dest='mnt', help='挂载路径，创建软链必须')
    parser.add_option('--dst', action='store', dest='dst', help='checkout 路径')
    parser.add_option('--command', action='store', dest='command', help='命令行参数配置')
    parser.add_option('--add', action='store', dest='add', help='同git add，添加文件以逗号,分割')
    parser.add_option('--rm', action='store', dest='rm', help='同git rm，删除文件以逗号,分割')
    parser.add_option('--commit', action='store_true', dest='commit', help='同git commit')
    parser.add_option('-m', '--message', action='store', dest='message', help='同git message')
    parser.add_option('--config', action='store_true', dest='config', help='global config配置')
    parser.add_option('--dataunit', action='store', dest='dataunit', help='设置dataunit')
    parser.add_option('--partition', action='store', dest='partition', help='设置partition')
    parser.add_option('--erp', action='store', dest='erp', help='所有涉及到DataOps的操作，erp是必须的！')
    parser.add_option('--projectpath', action='store', dest='projectpath', help='项目路径prefix')
    ori, args = parser.parse_args()
    if ori.config:
        if ori.dataunit:
            FileConfig.globalconfig('dataunit', ori.dataunit)
        if ori.partition:
            FileConfig.globalconfig('partition', ori.partition)
        if ori.erp:
            FileConfig.globalconfig('erp', ori.erp)
        if ori.projectpath:
            FileConfig.globalconfig('projectpath', ori.projectpath)
        return
    if ori.add or ori.rm:
        if ori.add:
            FileConfig.operationconfig(ori.add, 'add')
        if ori.rm:
            FileConfig.operationconfig(ori.rm, 'rm')
        return
    if ori.commit:
        if not ori.message:
            logging.error('请提交commit message')
            return
        try:
            fp_global = open(os.getcwd() + '/.store/global.json', 'r+')
            fp_basic = open(os.getcwd() + '/.store/basic.json', 'r+')
            fp_list = json.load(fp_basic).get('fp_list')
            gconfig = json.load(fp_global)
            a = Upload(gconfig=gconfig, fp_list=fp_list, message=ori.message)
            a.commit()
        except Exception as e:
            logging.error(str(traceback.print_exc()) + '请保证制定了正确的config信息和文件')
            return

    if ori.command:
        config = ConfigParser.ConfigParser()
        config.read(ori.command)
        tmp = config.items('command')
        o = {}
        for item in tmp:
            o[item[0]] = item[1]

    else:
        o = vars(ori)
    if o.get('version'):
        if not o.get('project') or not o.get('erp'):
            logging.error('提示：checkout版本时，project和erp是必须的')
            return
        if o.get('softlink'):
            if not o.get('mnt'):
                logging.error('提示：创建软链时，挂载路径prefix是必须的')
            else:
                c = Checkout(version=o.get('version'), erp=o.get('erp'), id=str(o.get('project')), mnt_path=o.get('mnt'), dst=o.get('dst'))
                c.checkout_sl()
        else:
            c = Checkout(version=o.get('version'), erp=o.get('erp'), id=str(o.get('project')), mnt_path='', dst='')
            c.checkout()
        return
    if o.get('get'):
        a = Upload()
        a.get_objects(o.get('keyword'))
        return


demoArgs()