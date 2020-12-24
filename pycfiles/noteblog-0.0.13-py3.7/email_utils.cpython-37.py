# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/noteblog/fzutils/email_utils.py
# Compiled at: 2019-05-05 05:26:25
# Size of source mod 2**32: 1857 bytes
import smtplib
from gc import collect
from email.mime.text import MIMEText
__all__ = [
 'FZEmail']

class FZEmail(object):
    __doc__ = "\n    邮件obj\n        目前支持: qq邮箱 [qq邮箱设置开启smtp, 并获得授权码]\n        用法: eg:\n            _ = FZEmail(user='2939161681@qq.com', passwd='smtp授权码or密码')\n            _.send_email(to=['superonesfazai@gmail.com',])\n    "

    def __init__(self, user, passwd, host='smtp.qq.com', port=465):
        self.host = host
        self.port = port
        self.user = user
        self.passwd = passwd
        self._init_connect()

    def _init_connect(self):
        """
        初始化连接
        :return:
        """
        self.server = smtplib.SMTP_SSL(self.host, self.port)
        self.server.login(user=(self.user), password=(self.passwd))

    def send_email(self, to, subject='邮件主题', text='邮件正文'):
        """
        发送email
        :param to: a list eg: ["superonesfazai@gmail.com", ...]
        :param subject:
        :param text:
        :return:
        """
        if not isinstance(to, list):
            raise ValueError('to类型为list, 格式eg: ["superonesfazai@gmail.com", ...]')
        msg = MIMEText(text)
        msg['Subject'] = subject
        msg['From'] = self.user
        msg['To'] = to
        try:
            self.server.sendmail(self.user, to, msg.as_string())
            print('邮件发送成功!')
        except Exception as e:
            try:
                print(e)
                print('邮件发送失败!')
            finally:
                e = None
                del e

    def __del__(self):
        try:
            self.server.quit()
        except:
            pass

        collect()