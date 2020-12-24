# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/commonslib/network.py
# Compiled at: 2015-04-04 05:19:06
__doc__ = '\nCreated on 2011-8-28\n\n@author: huwei\n'
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_html_mail(sender, to, subject, message):
    u"""发送html邮件.
    ::
        send_html_mail(
            '爱玩儿<aiwanr.com@gmail.com>',
            'hu77wei@gmail.com',
            'hi, xiaohu xiaohu love you',
            '<html><body>hi, Im huwei </body></html>')
    :param sender: 发送者email 爱玩儿<aiwanr.com@gmail.com>.
    :param to: 接收者email.
    :param subject: 标题.
    :param message: 正文.
    :return: bool 成功发送返回true.
    """
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = to
    msg.attach(MIMEText(message, 'html', 'utf-8'))
    server = smtplib.SMTP('localhost')
    server.sendmail(sender, to, msg.as_string())
    server.quit()


def send_text_mail(sender, to, subject, message):
    u"""发送纯文本邮件.

    :param sender: string  发送者email 爱玩儿<aiwanr.com@gmail.com>.
    :param to: string 接收者email.
    :param subject: string 标题.
    :param message: string 正文.
    :return: bool 成功发送返回true.
    """
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = to
    msg.attach(MIMEText(message, 'plain', 'utf-8'))
    server = smtplib.SMTP('localhost')
    server.sendmail(sender, to, msg.as_string())
    server.quit()


if __name__ == '__main__':
    send_html_mail('爱玩儿<aiwanr.com@gmail.com>', '876213774@qq.com', 'hi, xiaohu xiaohu love you', '<html><body>hi, Im huwei </body></html>')