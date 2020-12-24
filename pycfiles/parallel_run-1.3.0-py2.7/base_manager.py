# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/parallel_run/base_manager.py
# Compiled at: 2014-01-14 01:27:26
import os, sys
from ConfigParser import ConfigParser
import logging
from tools import config2dict, load_module

class BaseManager(object):

    def gen_kwd(self, options):
        u"""利用options.message获得关键字
        继承BaseManager的子类应该实现gen_pwd方法"""
        err_msg = 'gen_kwd should be implemented in subclass of BaseManager'
        raise NotImplementedError(err_msg)

    def gen_kwd2opt(self, kwd2opt_cfg):
        u"""
        关键字keyword与其处理方法的对应关系
        path -list -函数所在的模块所在的路径
        module -basestring -函数所在的模块的模块名
        function -basestring -要调用的函数的函数名
        """
        cf = ConfigParser()
        cf.read(kwd2opt_cfg)
        ret = {}
        for section in cf.sections():
            d = ret.setdefault(section, {})
            d['module'] = cf.get(section, 'module').strip('" \'')
            d['function'] = cf.get(section, 'function').strip('" \'')
            try:
                d['path'] = [
                 cf.get(section, 'path').strip('" \'')]
            except Exception:
                d['path'] = None

        return ret

    def __call__(self, options):
        common_config = config2dict(options.config_file, 'common')
        work_dir = common_config['work_dir'].strip('" \'') if 'work_dir' in common_config else None
        if work_dir is not None and os.path.isdir(work_dir):
            os.chdir(work_dir)
        handler = logging.FileHandler(common_config['log_file'].strip('" \''))
        log_fmt = common_config['log_formatter'].strip('" \'') if 'log_formatter' in common_config else logging.BASIC_FORMAT
        handler.setFormatter(logging.Formatter(log_fmt))
        options.logger.addHandler(handler)
        try:
            log_level = int(common_config['log_level'].strip('" \''))
        except Exception:
            log_level = logging.DEBUG

        options.logger.setLevel(log_level)
        sys.path.extend(filter(os.path.isdir, map(lambda p: os.path.abspath(p.strip('" \'')), common_config['sys_path'].split(','))) if 'sys_path' in common_config else [])
        cur_dir = os.path.abspath(os.curdir)
        if cur_dir not in sys.path:
            sys.path.append(cur_dir)
        if 'kwd2opt' not in common_config:
            raise Exception('item kwd2opt must be supported')
        if not os.path.isfile(common_config['kwd2opt']):
            raise Exception('kwd2opt must be a config file')
        kwd2opt = self.gen_kwd2opt(common_config['kwd2opt'])
        kwd = self.gen_kwd(options)
        if kwd not in kwd2opt:
            return '%s not in type' % kwd
        else:
            return getattr(load_module(kwd2opt[kwd]['module'], kwd2opt[kwd]['path'] if 'path' in kwd2opt[kwd] else None), kwd2opt[kwd]['function'])(options)