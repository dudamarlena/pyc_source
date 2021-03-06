# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\HuoYan_monitoring\HuoYan_monitoring.py
# Compiled at: 2020-05-11 04:09:04
# Size of source mod 2**32: 15716 bytes
import os, sys, re, numpy as np, pandas as pd
from collections import defaultdict
import json, sqlite3, logging, time, yaml, smtplib, mimetypes
from email.message import EmailMessage
import datetime
from imbox import Imbox
import email.header, shutil, zipfile

class HuoYan_monitoring(object):

    def __init__(self, dbname: str='HuoYan_records.db', configfile: str='config.yaml'):
        if not os.path.exists(dbname):
            self.con = sqlite3.connect(dbname)
            self.creat_table()
        else:
            self.con = sqlite3.connect(dbname)
        if os.path.exists(configfile):
            configfile = os.path.abspath(configfile)
        else:
            raise ValueError('无效的config文件', configfile)
        with open(configfile, 'r', encoding='utf-8') as (f):
            self.config = yaml.load(f.read())

    def creat_table(self):
        """
        test_lifetime:
            id: 样品编号
            name:   姓名
            organization:   组织名称
            sample: 样本信息到达的时间
            test:   灭活组确认进入检测的时间
            extract:    提取组提取时间
            board_index:  PCR版号
            hole_index: PCR孔位
            report: 报告时间
            exception:异常情况
            finnished:样本生命周期是否结束
        
        processed_sample_files:
            sample_file:    文件名称，绝对路径
            modify_time:    最后修改时间

        processed_test_files:
            sample_file:    文件名称，绝对路径
            modify_time:    最后修改时间

        processed_report_files:
            sample_file:    文件名称，绝对路径
            modify_time:    最后修改时间

        processed_mail:
            sample_file:    文件名称，绝对路径
            modify_time:    最后修改时间
        """
        self.con.execute('create table test_lifetime(id,name,organization,sample,test,extract,board_index,hole_index,report,exception,finished)')
        self.con.execute('create table processed_sample_files(sample_file,modify_time)')
        self.con.execute('create table processed_test_files(test_file,modify_time)')
        self.con.execute('create table processed_extract_files(extract_file,modify_time)')
        self.con.execute('create table processed_report_files(report_file,modify_time)')
        self.con.execute('create table processed_mail(mail_uid)')
        self.dbcommit()

    def __del__(self):
        self.con.close()

    def dbcommit(self):
        self.con.commit()

    def fetch_mail(self, imap_server: str='mail.genomics.cn', port: int=143, start_time: datetime.datetime=datetime.datetime.fromtimestamp(time.mktime(datetime.datetime.now().date().timetuple()))):
        user = self.config['mail_user']
        passwd = self.config['mail_passwd']
        out_path = self.config['report_dir']
        imbox = Imbox(imap_server, username=user, password=passwd, ssl=False, starttls=False)
        messages = imbox.messages(date__gt=start_time)
        for _, message in messages:
            subject = message.subject
            if re.findall('新.+冠.+报.+告', subject):
                for attachment in message.attachments:
                    name, _ = email.header.decode_header(attachment['filename'])[0]
                    if re.findall('报.+告', name):
                        if re.findall('z.+i.+p', name):
                            name = re.sub('\\?\\=\\ \\=\\?UTF\\-8\\?Q\\?', '', name)
                            res = self.con.execute(f"select * from processed_mail where mail_uid = '{name}'").fetchone()
                            if res != None:
                                continue
                            filename = os.path.join(out_path, 'tmp', name)
                            content = attachment['content']
                            with open(filename, 'wb') as (w_f):
                                w_f.write(content.getvalue())
                            self.con.execute(f"insert into processed_mail(mail_uid) values ('{name}')")
                            self.dbcommit()
                            target = filename.split('.')[0]
                            if os.path.exists(target):
                                continue
                        myzip = zipfile.ZipFile(filename)
                        myzip.extractall(target)
                        bgmx_path = os.path.join(out_path, '报告明细表')
                        bgcd_path = os.path.join(out_path, '报告存档')
                        _, uuid = re.findall('-(.+?)(\\d+)', os.path.basename(target))[0]
                        for sub in os.listdir(target):
                            sub_path = os.path.join(target, sub)
                            bgmx = os.path.join(sub_path, '报告清单明细.xlsx')
                            bgmx_target = os.path.join(bgmx_path, f"{uuid[0:8]}_{uuid[8:]}_报告清单明细.xlsx")
                            shutil.copy(bgmx, bgmx_target)
                            for sub_sub in os.listdir(sub_path):
                                sub_sub_full = os.path.join(sub_path, sub_sub)
                                if os.path.isdir(sub_sub_full):
                                    bg_path = sub_sub_full
                                    for bg_file in os.listdir(bg_path):
                                        if bg_file.startswith('~'):
                                            continue
                                        if bg_file.endswith('pdf'):
                                            bg_full = os.path.join(bg_path, bg_file)
                                            bg_target = os.path.join(bgcd_path, bg_file)
                                            shutil.copy(bg_full, bg_target)

    def collect_infos(self):
        """采集信息"""
        for file in os.listdir(self.config['sample_dir']):
            if not file.endswith('xlsx'):
                continue
            if file.startswith('~'):
                continue
            file = os.path.join(self.config['sample_dir'], file)
            self.sample_info(file)

        for file in os.listdir(self.config['test_dir']):
            if not file.startswith('20'):
                continue
            if '出库样本明细表' not in file:
                continue
            if file.startswith('~'):
                continue
            file = os.path.join(self.config['test_dir'], file)
            self.test_info(file)

        dir = self.config['extract_dir']
        for sub in os.listdir(self.config['extract_dir']):
            fsub = os.path.join(dir, sub)
            if os.path.isdir(fsub):
                for file in os.listdir(fsub):
                    if file.startswith('~'):
                        continue
                    if not file.endswith('xlsx'):
                        continue
                    ffile = os.path.join(fsub, file)
                    self.extract_info(ffile)

        report_dir = os.path.join(self.config['report_dir'])
        for file in os.listdir(report_dir):
            if not file.endswith('结果反馈表.xlsx'):
                continue
            if file.startswith('~'):
                continue
            file = os.path.join(report_dir, file)
            self.report_info(file)

        self.exception_info(self.config['exception_file'])

    def file_modify_time(self, file: str):
        """文件的最后修改时间"""
        mtime = os.stat(file).st_mtime
        file_modify_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(mtime))
        return file_modify_time

    def sample_info(self, file: str):
        """ sample 表处理"""
        file = os.path.abspath(file)
        res = self.con.execute(f"select modify_time from processed_sample_files where sample_file = '{file}'").fetchone()
        if res == None or self.file_modify_time(file) > res[0]:
            df = pd.read_excel(file, parse_dates=['样品采集日期'], mode='r')
            for id, name, organization, date in zip(df['样品编号'], df['姓名'], df['送检单位'], df['样品采集日期']):
                res = self.con.execute(f"select * from test_lifetime where id ='{id}'").fetchone()
                if res == None:
                    self.con.execute(f"insert into test_lifetime(id,name,organization,sample) values ('{id}','{name}','{organization}','{date}')")
                else:
                    self.con.execute(f"update test_lifetime set name='{name}',organization='{organization}',sample='{date}' where id='{id}'")

        elif res == None:
            self.con.execute(f"insert into processed_sample_files(sample_file,modify_time) values ('{file}','{self.file_modify_time(file)}')")
        else:
            self.con.execute(f"update processed_sample_files set modify_time='{self.file_modify_time(file)}' where sample_file = '{file}'")
        self.dbcommit()

    def test_info(self, file: str):
        file = os.path.abspath(file)
        res = self.con.execute(f"select modify_time from processed_test_files where test_file = '{file}'").fetchone()
        if res == None or self.file_modify_time(file) > res[0]:
            df = pd.read_excel(file, sheet_name='出库样本明细', mode='r')
            sers = []
            for column in df.columns:
                ser = df[column].dropna().astype(str)
                sers.append(ser[ser.str.startswith('20S')])

            total = pd.concat(sers)
            date = os.path.basename(file).split('_')[0]
            if len(date) != 8:
                raise ValueError('检测表格错误的日期格式', file)
            ndf = pd.DataFrame({'id':list(total),  'date':[date for i in range(len(total))]})
            ndf.date = pd.to_datetime((ndf.date), format='%Y%m%d')
            for id, date in zip(ndf['id'], ndf['date']):
                resn = self.con.execute(f"select * from test_lifetime where id ='{id}'").fetchone()
                if resn == None:
                    self.con.execute(f"insert into test_lifetime (id,test) values ('{id}','{date}')")
                else:
                    self.con.execute(f"update test_lifetime set test='{date}' where id='{id}'")

        elif res == None:
            self.con.execute(f"insert into processed_test_files(test_file,modify_time) values ('{file}','{self.file_modify_time(file)}')")
        else:
            self.con.execute(f"update processed_test_files set modify_time='{self.file_modify_time(file)}' where test_file = '{file}'")
        self.dbcommit()

    def extract_info(self, file):
        file = os.path.abspath(file)
        res = self.con.execute(f"select modify_time from processed_extract_files where extract_file = '{file}'").fetchone()
        if res == None or self.file_modify_time(file) > res[0]:
            date = os.path.basename(file).split('-')[0]
            board_index = os.path.basename(file).split('.')[0]
            if len(date) != 8:
                print(file)
                raise ValueError('检测表格错误的日期格式', file)
            df = pd.read_excel(file, mode='r')
            df = df.iloc[:, 12:14]
            df = df.rename(columns={'Unnamed: 12':'hole_index',  '样例编号':'id'})
            df['date'] = date
            df.date = pd.to_datetime((df.date), format='%Y%m%d')
            df['board_index'] = board_index
            df = df[df.id.notnull()]
            for id, date, board_index, hole_index in zip(df['id'], df['date'], df['board_index'], df['hole_index']):
                resn = self.con.execute(f"select * from test_lifetime where id ='{id}'").fetchone()
                if resn == None:
                    continue
                self.con.execute(f"update test_lifetime set extract='{date}', board_index='{board_index}', hole_index='{hole_index}' where id='{id}'")

        self.con.execute(f"insert into processed_extract_files(extract_file,modify_time) values ('{file}','{self.file_modify_time(file)}')")
        self.dbcommit()

    def report_info(self, file):
        file = os.path.abspath(file)
        res = self.con.execute(f"select modify_time from processed_report_files where report_file = '{file}'").fetchone()
        if res == None or self.file_modify_time(file) > res[0]:
            date = os.path.basename(file).split('_')[0]
            if len(date) != 8:
                print(file)
                raise ValueError('检测表格错误的日期格式')
            df = pd.read_excel(file, sheet_name='阴性', mode='r')
            df = df.rename(columns={'结果':'result',  '样本名称':'id'})
            df['date'] = date
            df.date = pd.to_datetime((df.date), format='%Y%m%d')
            df = df[df.id.notnull()]
            for id, result, date in zip(df['id'], df['result'], df['date']):
                if result == '阴性':
                    self.con.execute(f"update test_lifetime set report='{date}',finished=1 where id='{id}'")
                else:
                    self.con.execute(f"update test_lifetime set exception='{result}',finished=1 where id='{id}'")

        self.con.execute(f"insert into processed_report_files(report_file,modify_time) values ('{file}','{self.file_modify_time(file)}')")
        self.dbcommit()

    def exception_info(self, file):
        df = pd.read_excel(file, skiprows=[0, 1], parse_dates=['送样日期'], mode='r')
        for id, date, hege, qksm in zip(df['样本编号'], df['送样日期'], df['实物样本是否合格'], df['情况说明']):
            resn = self.con.execute(f"select * from test_lifetime where id ='{id}'").fetchone()
            if resn == None:
                if hege == '是':
                    self.con.execute(f"insert into test_lifetime (id,exception) values ('{id}','{qksm}') ")
                else:
                    self.con.execute(f"insert into test_lifetime (id,exception,finished) values ('{id}','{qksm}',1) ")
            elif hege == '是':
                self.con.execute(f"update test_lifetime set exception='{qksm}' where id='{id}'")
            else:
                self.con.execute(f"update test_lifetime set exception='{qksm}',test='{date}',finished=1 where id='{id}'")

        self.dbcommit()

    def monitoring(self):
        pass