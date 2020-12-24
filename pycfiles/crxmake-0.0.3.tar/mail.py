# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/crwy/utils/mail.py
# Compiled at: 2020-02-03 23:11:43
from __future__ import print_function, unicode_literals
import email, re, traceback, imaplib
from imapclient import IMAPClient
from email.header import decode_header
imaplib._MAXLINE = 10000000
SEEN = b'\\Seen'

class MailReceiver(IMAPClient):

    def __init__(self, host, timeout=60, **kwargs):
        super(MailReceiver, self).__init__(host, timeout=timeout, **kwargs)

    def get_folder_list(self):
        u"""
        获取邮箱文件夹
        :return: list
        """
        folders = self.list_folders()
        res_list = []
        for folder in folders:
            if folder:
                res_list.append(folder[2])

        return res_list

    def get_message_id_list(self, mailbox=b'INBOX', search_=b'all'):
        u"""
        获取邮件ID列表
        :param mailbox: 邮箱文件夹
        :param search_: 搜索规则
        :return: list
        """
        self.select_folder(mailbox)
        message_list = self.search(search_)
        return message_list

    def get_message_list(self, message_id_list):
        u"""
        获取邮件列表
        :param message_id_list: 邮件ID列表
        :return: dict   id:email
        """
        message_list = self.fetch(message_id_list, [b'INTERNALDATE', b'FLAGS', b'BODY.PEEK[]'])
        if not message_list:
            return
        return message_list

    @staticmethod
    def parse_email(m, flag=None):
        u"""
        解析邮件header内容
        :param m: 原内容
        :param flag: 解析类型标识
        :return: 编码转换后内容
        """
        res = []
        try:
            for s, c in decode_header(m):
                if c:
                    res.append(s.decode(c, b'ignore'))
                else:
                    res.append(s.decode(b'utf-8') if isinstance(s, bytes) else s)

            if not res:
                return
            if flag == b'from':
                res = re.findall(b'[0-9a-zA-Z_\\.]{0,19}@[0-9a-zA-Z\\.]{1,100}', res[1])
                return res[0]
            if flag == b'to':
                new_res = []
                for e in res[0].split(b','):
                    em = re.findall(b'[0-9a-zA-Z_\\.]{0,19}@[0-9a-zA-Z\\.]{1,100}', e)
                    if em:
                        new_res.append(em[0])

                return new_res
            return res[0]
        except Exception as e:
            traceback.print_exc()
            return res

    def get_message_content(self, message):
        u"""
        获取邮件内容
        :param message:
        :return:
        """
        try:
            while True:
                res = {}
                msg = email.message_from_bytes(message[b'BODY[]'])
                res[b'subject'] = self.parse_email(msg[b'Subject'])
                res[b'from'] = self.parse_email(msg[b'From'], flag=b'from')
                res[b'to'] = self.parse_email(msg[b'To'], flag=b'to')
                res[b'date'] = self.parse_email(msg[b'Date'])
                for par in msg.walk():
                    if not par.is_multipart():
                        name = par.get_param(b'name')
                        if name:
                            pass
                        else:
                            body = par.get_payload(decode=True)
                            if not body:
                                continue
                            try:
                                code = par.get_content_charset()
                                res[b'body'] = body.decode(code, b'ignore')
                            except TypeError:
                                res[b'body'] = body

                return res

        except Exception as e:
            traceback.print_exc()
            return

    def delete_message(self, messages, deleted_folder=b'Deleted Messages'):
        u"""
        删除邮件
        :param messages:
        :param deleted_folder:
        :return:
        """
        try:
            self.add_flags(messages, SEEN)
            if deleted_folder:
                self.copy(messages, deleted_folder)
            self.delete_messages(messages)
            self.expunge()
            return True
        except Exception as e:
            traceback.print_exc(e)
            return False