# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/max/report/predata.py
# Compiled at: 2019-04-27 11:20:12
"""
@Author  : xinxi
@Time    : 2018/12/5 18:34
@describe: 获取报告数据
"""
import os, re, time, subprocess, sys
sys.path.append('..')
from ..tools.loggers import JFMlogging
logger = JFMlogging().getloger()
from ..config import *

def read_cpu():
    u"""
    读取cpu文件的数据
    :return:
    """
    time = []
    info = []
    activity = []
    with open(cpu_path, 'r') as (f):
        for index in f.readlines():
            time.append(index.split(',')[0].replace('\n', ''))
            info.append(index.split(',')[1].replace('+', '').replace('\n', ''))
            activity.append(index.split(',')[2].replace('\n', ''))

    return (
     time, info, activity)


def read_mem():
    u"""
    读取mem文件的数据
    :return:
    """
    time = []
    info = []
    activity = []
    with open(mem_path, 'r') as (f):
        for index in f.readlines():
            time.append(index.split(',')[0].replace('\n', ''))
            info.append(index.split(',')[1].replace('\n', ''))
            activity.append(index.split(',')[2].replace('\n', ''))

    return (
     time, info, activity)


def read_fps():
    u"""
    读取fps文件的数据
    :return:
    """
    time = []
    info = []
    activity = []
    with open(fps_path, 'r') as (f):
        for index in f.readlines():
            time.append(index.split(',')[0].replace('\n', ''))
            info.append(index.split(',')[1].replace('\n', ''))
            activity.append(index.split(',')[2].replace('\n', ''))

    return (
     time, info, activity)


def read_network():
    u"""
    读取network文件的数据
    :return:
    """
    time = []
    info = []
    activity = []
    with open(network_path, 'r') as (f):
        for index in f.readlines():
            time.append(index.split(',')[0].replace('\n', ''))
            info.append(index.split(',')[1].replace('\n', ''))
            activity.append(index.split(',')[2].replace('\n', ''))

    return (
     time, info, activity)


def get_page():
    u"""
    获取页面数据
    :return:
    """
    try:
        try:
            time_list = []
            page_list = []
            page_time_list = []
            with open(page_path, 'r') as (f_r):
                result = f_r.readlines()
            for line in set(result):
                time = line.split()[0] + ' ' + line.split()[1]
                page = line.split('/')[1].split(':')[0]
                page_time = line.split('/')[1].split(':')[1].replace('+', '').replace('\n', '').strip()
                time_list.append(time)
                page_list.append(page)
                page_time_list.append(format_time(page_time))

        except Exception as e:
            logger.error(('获取页面数据异常!{}').format(e))

    finally:
        return (
         time_list, page_time_list, page_list)


def format_time(time_str):
    u"""
    格式化时间
    :param time_str:
    :return:
    """
    try:
        try:
            if re.findall('total', time_str):
                time_str = time_str.replace('ms', '')
                time_str = time_str.split('(')[0].strip()
                if re.findall('s', time_str):
                    new_time_m = str(time_str).split('s')[0]
                    new_time_s = str(time_str).split('s')[1]
                    new_time = int(new_time_m) * 1000 + int(new_time_s)
                else:
                    new_time = time_str
            else:
                time_str = time_str.replace('ms', '')
                if re.findall('s', time_str):
                    new_time_m = str(time_str).split('s')[0]
                    new_time_s = str(time_str).split('s')[1]
                    new_time = int(new_time_m) * 1000 + int(new_time_s)
                else:
                    new_time = time_str
        except Exception as e:
            logger.error(('格式化时间异常!{}').format(e))
            new_time = 0

    finally:
        return new_time