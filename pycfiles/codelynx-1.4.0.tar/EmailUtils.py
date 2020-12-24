# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: D:\PythonCode\CodeLib\src\Network\EmailUtils.py
# Compiled at: 2016-09-28 23:08:22
__doc__ = '\nPackage: EmailUtils, Send email toolkit.\nAuthor: Benjamin Zhou\n'
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class EmailUtils:
    u"""
    发送Email工具包
    """

    def __init__(self):
        pass

    @staticmethod
    def _send_email(to_list, fromaddress, mailtype, subject, content):
        """
        sss
        :param to_list:
        :param fromaddress:
        :param mailtype:
        :param subject:
        :param content:
        :return:
        """
        msg = MIMEText(content, _subtype=mailtype, _charset='utf8')
        msg['Subject'] = subject
        msg['From'] = fromaddress
        msg['To'] = (';').join(to_list)
        try:
            mail_host = 'internalmail.morningstar.com'
            server = smtplib.SMTP()
            server.connect(mail_host)
            server.sendmail(fromaddress, to_list, msg.as_string())
            server.close()
            return True
        except Exception as e:
            print str(e)
            return False

    @staticmethod
    def send_plainmail(to_list, fromaddress, subject, content):
        u"""
        在公司内部发送PlainText格式的消息邮件
        :param to_list:
        :param fromaddress:
        :param subject:
        :param content:
        :return:
        """
        mailtype = 'plain'
        return EmailUtils._send_email(to_list, fromaddress, mailtype, subject, content)

    @staticmethod
    def send_htmlmail(to_list, fromaddress, subject, content):
        u"""
        在公司内部发送HTML格式的消息邮件
        :param to_list:
        :param fromaddress:
        :param subject:
        :param content:
        :return:
        """
        mailtype = 'html'
        return EmailUtils._send_email(to_list, fromaddress, mailtype, subject, content)

    @staticmethod
    def send_attachemail(to_list, fromaddress, subject, content, attachmentfiles):
        """

        :param to_list:
        :param fromaddress:
        :param subject:
        :param content:
        :param attachmentfiles:
        :return:
        """
        msg = MIMEMultipart()
        att0 = MIMEText(content, _subtype='html', _charset='utf8')
        msg.attach(att0)
        for filepath in attachmentfiles:
            att1 = MIMEText(open(filepath, 'rb').read(), 'base64', 'utf8')
            att1['Content-Type'] = 'application/octet-stream'
            filename = filepath.split('\\')[(-1)]
            att1['Content-Disposition'] = 'attachment; filename="' + filename + '"'
            msg.attach(att1)

        msg['to'] = to_list
        msg['from'] = fromaddress
        msg['subject'] = subject
        try:
            mail_host = 'internalmail.morningstar.com'
            server = smtplib.SMTP()
            server.connect(mail_host)
            server.sendmail(msg['from'], msg['to'], msg.as_string())
            server.quit()
            print '发送成功'
            return True
        except Exception as e:
            print '发送失败,详细信息为：' + str(e)
            return False


if __name__ == '__main__':
    EmailUtils.send_attachemail('Benjamin.Zhou@morningstar.com', 'Benjamin.Zhou@morningstar.com', 'test', '<b>hello 你好，world!</b><table><tr><td>aaaaaaa</td></tr></table>', [
     'D:\\piplist.txt', 'D:\\PythonTestAbc.zip'])