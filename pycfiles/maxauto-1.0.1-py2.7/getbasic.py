# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/max/monkey/getbasic.py
# Compiled at: 2019-04-27 11:17:21
"""
@Author  : xinxi
@Time    : 2018/12/5 18:34
@describe: 获取应用基本信息
"""
import sys, os, re
sys.path.append('..')
reload(sys)
sys.setdefaultencoding('utf-8')
from ..tools.loggers import JFMlogging
from ..tools.filetools import write_file
logger = JFMlogging().getloger()
from ..config import all_activity_path

class GetBasic:

    def __init__(self, apkpath, devices):
        self.apkpath = apkpath
        self.devices = devices
        self.appinfo = self.get_app_info()

    def get_app_info(self):
        u"""
        获取app信息
        :return:
        """
        appinfo = ''
        try:
            cmd = ('aapt dupm badging {}').format(self.apkpath)
            appinfo = os.popen(cmd).readlines()
        except Exception as e:
            logger.error(('获取app信息异常!{}').format(e))

        return appinfo

    def get_app_name(self):
        u"""
        获取app名称
        :return:
        """
        appname = ''
        try:
            try:
                for line in self.appinfo:
                    if re.findall('package: name=', line):
                        appname = line.split('package: name=')[1].split()[0].replace("'", '')

            except Exception as e:
                logger.error(('获取app名称异常!{}').format(e))

        finally:
            return appname

    def get_app_activity(self):
        u"""
        获取app的启动activity
        :return:
        """
        appactivity = ''
        try:
            try:
                for line in self.appinfo:
                    if re.findall('launchable-activity: name', line):
                        appactivity = line.split('launchable-activity: name=')[1].split()[0].replace("'", '')

            except Exception as e:
                logger.error(('获取app启动类异常!{}').format(e))

        finally:
            return appactivity

    def get_app_version(self):
        u"""
        获取app版本号
        :return:
        """
        appversion = ''
        try:
            try:
                for line in self.appinfo:
                    if re.findall('package: name=', line):
                        appversion = line.split('versionName=')[(-1)].replace("'", '').replace('\n', '').split()[0]

            except Exception as e:
                logger.error(('获取app版本号异常!{}').format(e))

        finally:
            return appversion

    def get_app_size(self):
        u"""
        获取apk文件大小
        :return:
        """
        appsize = '0MB'
        try:
            try:
                cmd = ('ls -l {}').format(self.apkpath)
                size = float(str(os.popen(cmd).readlines()).split()[4]) / (1024 * 1024)
                appsize = str(round(size, 2)) + 'MB'
            except Exception as e:
                logger.error(('获取获取apk文件大小异常:{}').format(e))

        finally:
            return appsize

    def get_devices_model(self):
        u"""
        获取设备型号
        :return:
        """
        devices_model = 'test phone'
        try:
            try:
                cmd = ('adb -s {} shell getprop ro.product.model').format(self.devices)
                devices_model = os.popen(cmd).readlines()[0].replace('\n', '')
            except Exception as e:
                logger.error(('获取设备型号异常!{}').format(e))

        finally:
            return devices_model

    def get_devices_version(self):
        u"""
        获取设备版本号
        :return:
        """
        devices_version = ''
        try:
            try:
                cmd = ('adb -s {} shell getprop ro.build.version.release').format(self.devices)
                devices_version = os.popen(cmd).readlines()[0].replace('\n', '')
            except Exception as e:
                logger.error(('获取设备版本号异常!{}').format(e))

        finally:
            return devices_version

    def get_all_activitys(self):
        u"""
        获取app中所有activity
        :return:
        """
        activity_list = []
        try:
            cmd = ('aapt dump xmltree {} AndroidManifest.xml').format(self.apkpath)
            result = os.popen(cmd).readlines()
            for line in result:
                if re.findall('Activity', line) and re.findall('Raw', line):
                    activity = line.split('Raw:')[1].strip().replace('"', '').replace(')', '')
                    activity_list.append(activity)

            write_file(all_activity_path, activity_list)
        except Exception as e:
            logger.error(('获取所有activity异常!{}').format(e))

    def get_devices_mem(self):
        u"""
        获取设备内存
        :return:
        """
        mem = {}
        try:
            try:
                cmd = ('adb -s {} shell cat /proc/meminfo | grep MemTotal').format(self.devices)
                total_mem = str(os.popen(cmd).readlines()).split(':')[1].split()[0]
                total_mem = ('{}MB').format(int(total_mem) / 1024)
                logger.info(('手机总内存:{}').format(total_mem))
                mem['total_mem'] = total_mem
                cmd = ('adb -s {} shell cat /proc/meminfo | grep MemFree').format(self.devices)
                free_mem = str(os.popen(cmd).readlines()).split(':')[1].split()[0]
                free_mem = ('{}MB').format(int(free_mem) / 1024)
                logger.info(('手机剩余内存:{}').format(free_mem))
                mem['free_mem'] = free_mem
                mem.update()
            except Exception as e:
                logger.error(('获取设备内存异常!{}').format(e))

        finally:
            return mem