# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dbop/dbop.py
# Compiled at: 2018-08-24 01:28:57
import fileinput
from scipy import misc
import sys, os, argparse, numpy as np, random
from time import sleep
import time, datetime, scipy.misc, hashlib, urllib2, json
from DBUtils.PooledDB import PooledDB
import traceback, cv2
from PIL import Image
import imageio, shutil
from skimage import io
import os.path, MySQLdb, sys
from zprint import *

class dbop:

    def __init__(self, hostName='127.0.0.1', usrName='root', passWord='123456', charset='utf8'):
        self.db = MySQLdb.connect('%s' % hostName, '%s' % usrName, '%s' % passWord, charset='utf8')

    def po(self, message):
        zprint(message)

    def epo(self, message):
        eprint(message)

    def turple2list(self, turple_val):
        rlist = lambda t, self=lambda t, self: [ self(tt, self) for tt in t ] if isinstance(t, tuple) else t: self(t, self)
        rl = rlist(turple_val)
        return rl

    def run(self, sqlstr):
        cursor = self.db.cursor()
        content = None
        try:
            cursor.execute(sqlstr)
            content = cursor.fetchall()
        except Exception as e:
            self.epo(sqlstr)
            self.epo(e)

        self.db.commit()
        return self.turple2list(content)

    def help(self, name='sql'):
        if name == 'sql':
            self.po("SELECT ziduan FROM %sxml WHERE image_name = '%s'")
            self.po("INSERT INTO %sxml (image_name, xml_content) VALUES ('%s','%s')")
            self.po("UPDATE %sxml SET xml_content = '%s' WHERE image_name = '%s'")
            self.po("select count(*) from %s_task  where status='finished' and teacher_id=%d")
            self.po("insert into  audio_flvs(online_class_id,info,created_at,updated_at) values(%d,'%s',now(),now())")
            self.po('delete from video_flvs where online_class_id=%d')
            self.po("insert into  video_flvs(online_class_id,info,created_at,updated_at) values(%d,'%s',now(),now())")

    def getnum(self, rr):
        num = 0
        if rr is None:
            num += 0
        else:
            num += rr[0][0]
        return num

    def get_task_num(projectname, host_id, status):
        sqlstr = "select count(*) from %s_task  where status='%s' and host_id=%d" % (project_name, status, host_id)
        rr = self.run(sqlstr)
        return self.getnum(rr)

    def get_finished_num_by_teacher_id(self, project_name, teacher_id, host_id):
        task_sql = "select count(*) from %s_task  where status='finished' and teacher_id=%d" % (project_name, teacher_id)
        rr = self.run(sqlstr)
        return self.getnum(rr)

    def get_task_list_from_db(self, project_name, host_id, pre_log_str):
        sqlstr = "select online_class_id,supplier_code,student_id,teacher_id,class_room as classroom,scheduled_date_time,course_id,student_id,birthday,english_name,teacher_1_avatar_url,teacher_2_avatar_url,teacher_3_avatar_url,teacher_4_avatar_url from %s_task  where status in ('insert') and host_id=%d  order by id limit 1" % (project_name, host_id)
        rr = self.run(sqlstr)
        tl = self.tasklist2dict(rr)
        return tl

    def update_finished_num(self, project_name, teacher_id, finished_num):
        sqlstr = 'update %_task set finished_num=%d,updated_at=now() where teacher_id=%d ' % (project_name, finished_num, teacher_id)
        rr = self.run(sqlstr)
        return self.getnum(rr)

    def update_finished_teacher_id_status_as_repeate(self, project_name, teacher_id, pre_log_str):
        sqlstr = "update %s_task set status='repeate',updated_at=now() where teacher_id=%d and status='new'" % (project_name, teacher_id)
        rr = self.run(sqlstr)
        return rr

    def connect(self, project_name):
        pool = PooledDB(MySQLdb, 1, host='127.0.0.1', user='root', passwd='MyNewPass4!', db='%s_task' % project_name, port=3306, charset='utf8')
        return pool

    def get_task_list_by_hand(pre_log_str):
        pre_log_str += sys._getframe().f_code.co_name + ':'
        log2(pre_log_str + '[start]')
        task_list = []
        task_dict = {}
        task_dict['online_class_id'] = 93363743
        task_dict['supplier_code'] = 8
        task_dict['student_id'] = 1896711
        task_dict['teacher_id'] = 7832201
        task_dict['classroom'] = 'jz721ee6b1cff04559a597a6572d9f00d1'
        task_dict['scheduled_date_time'] = '2018-04-26 18:00:00'
        task_list.append(task_dict)
        log2(pre_log_str + '[  end]')
        return task_list

    def tasklist2dict(self, rr):
        task_list = []
        for rrr in rr:
            task = rrr
            online_class_id = task[0]
            task_dict = {}
            task_dict['online_class_id'] = int(task[0])
            task_dict['supplier_code'] = int(task[1])
            task_dict['student_id'] = int(task[2])
            task_dict['teacher_id'] = int(task[3])
            task_dict['course_id'] = int(task[6])
            task_dict['classroom'] = str(task[4])
            task_dict['scheduled_date_time'] = str(task[5])
            task_dict['student_id'] = int(task[7])
            task_dict['birthday'] = str(task[8])
            task_dict['english_name'] = str(task[9])
            task_dict['teacher_1_avatar_url'] = str(task[10])
            task_dict['teacher_2_avatar_url'] = str(task[11])
            task_dict['teacher_3_avatar_url'] = str(task[12])
            task_dict['teacher_4_avatar_url'] = str(task[13])
            task_list.append(task_dict)

        return task_list


if __name__ == '__main__':
    dbb = dbop('172.23.250.51', 'root', '20180712')
    dbl = dbb.run('show databases;')
    xml_num = 0
    jpg_num = 0
    for dbname in dbl:
        if 'fourgesture_detection_train' not in dbname[0]:
            continue
        sqlstr = 'use %s;' % dbname[0]
        dbb.run(sqlstr)
        sqlstr = 'select count(*) from %sxml;' % dbname[0]
        rr = dbb.run(sqlstr)
        xml_num += dbb.getnum(rr)
        xml_numtmp = dbb.getnum(rr)
        sqlstr = 'select count(*) from %simg' % dbname[0]
        rr = dbb.run(sqlstr)
        jpg_num += dbb.getnum(rr)
        jpg_numtmp = dbb.getnum(rr)
        if xml_numtmp > 0:
            print dbname[0]
            print 'xmltmp:%d,jpgtmp:%s' % (xml_numtmp, jpg_numtmp)
            print 'xml:%d,jpg:%s' % (xml_num, jpg_num)

    print dbb.help('sql')