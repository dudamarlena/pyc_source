# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/lishengangTools/simpleEmail.py
# Compiled at: 2017-10-19 00:15:25
# Size of source mod 2**32: 4333 bytes
from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.utils import parseaddr, formataddr, formatdate
import smtplib, mimetypes, os, time

def help():
    print("\n\t\n\t支持两种参数调用方式：\n\n1.关键字参数调用：\n\nif __name__=='__main__':\n    From='xxxx@qq.com'\n    To=['xx@xx.com','xx@xxa.com']\n    Pwd='xxxx'\n    Screen='测试'\n    Content='test'\n    Serve='smtp.qq.com'\n    Subject='这是一个测试'\n    BCC=['test@mmeitech.com']\n    CC=['cszy2013@163.com']\n    SSL=True\n    Port=465\n    mail=SimpleEmail(From=From,To=To,Pwd=Pwd,Screen=Screen,Content=Content,Serve=Serve,Subject=Subject,BCC=BCC,CC=CC,SSL=SSL,Port=Port)\n    result=mail.send()\n    if result:\n        print('send success!')\n    else:\n        print('send failed!')\n2.tuple参数调用\n\nif __name__=='__main__':\n    data={\n    'From':'xx@163.com','Pwd':'xxxx','To':['xx@qq.com'],\n    'Screen':'测试2','Subject':'啊哈哈',\n    'Serve':'smtp@163.com','Attachment':['E://1.png','C://tm//1.txt'],\n    'Content':'111222'\n    }\n    mail=SimpleEmail(data)\n    result=mail.send()\n    if result:\n        print('send success!')\n    else:\n        print('send failed!')\n本类中：\n1.使用QQ邮箱的时候，密码是授权码，SSL=True，Port=465\n2.使用Gmail的时候，设置TLS=True,Port=587\n3.使用163，阿里云等企业邮箱的时候，无需设置端口和其他，已经默认。\n\t\n\t\n\t")


class SimpleEmail(object):

    def __init__(self, *kw, From='', Screen='', Pwd='', To='', CC=[], BCC=[], Subject='', Content='', Port=25, Serve='', Attachment=[], Emailtype='HTML', SSL=False, TLS=False):
        kw1 = {'From': From, 'Screen': Screen, 'CC': CC, 'Pwd': Pwd, 'To': To, 'BCC': BCC, 'Subject': Subject, 'Content': Content, 'Port': Port, 'Serve': Serve, 'Attachment': Attachment, 'Emailtype': Emailtype, 'SSL': SSL, 'TLS': TLS}
        if len(kw) == 0:
            kw = kw1
        else:
            kw = kw[0]
            for k in kw1:
                if k not in kw:
                    kw[k] = kw1[k]

        self.From, self.Pwd, self.Serve, self.Port, self.SSL, self.To, self.BCC, self.CC, self.TLS = (
         kw['From'], kw['Pwd'], kw['Serve'], kw['Port'], kw['SSL'], kw['To'], kw['BCC'], kw['CC'], kw['TLS'])
        MIMEmain = MIMEMultipart()
        MIMEmain['Date'] = formatdate()
        MIMEmain['X-Mailer'] = 'By Python'
        MIMEmain['Message-ID'] = '<%s%s>' % (int(time.time() * 10000000), kw['From'])
        MIMEmain['From'] = formataddr((Header(kw['Screen'], 'utf-8').encode(), kw['From']))
        MIMEmain['To'] = ', '.join(kw['To'])
        MIMEmain['Cc'] = ', '.join(kw['CC'])
        MIMEmain['Subject'] = Header(kw['Subject'], 'utf-8').encode()
        MIMEmain.attach(MIMEText(kw['Content'], kw['Emailtype'], 'utf-8'))
        if isinstance(kw['Attachment'], list) and len(kw['Attachment']) > 0:
            count = 0
            for i in kw['Attachment']:
                with open(i, 'rb') as (f):
                    ext1, ext2 = mimetypes.guess_type(i)
                    if ext1 == None or not ext2 == None:
                        ext1 = 'application/octet-stream'
                    ext3, ext4 = ext1.split('/', 1)
                    mimefile = MIMEBase(ext3, ext4, filename=os.path.split(i)[1])
                    mimefile.add_header('Content-Disposition', 'attachment', filename=os.path.split(i)[1])
                    mimefile.add_header('Content-ID', '<%s>' % count)
                    mimefile.add_header('X-Attachment-ID', '%s' % count)
                    count += 1
                    mimefile.set_payload(f.read())
                    encoders.encode_base64(mimefile)
                    MIMEmain.attach(mimefile)

        self.MIMEmain = MIMEmain

    def multistyle_args():
        pass

    def send(self):
        if self.SSL:
            mail = smtplib.SMTP_SSL(self.Serve, self.Port)
        else:
            mail = smtplib.SMTP(self.Serve, self.Port)
        if self.TLS:
            mail.starttls()
        mail.login(self.From, self.Pwd)
        try:
            try:
                mail.sendmail(self.From, self.To + self.CC + self.BCC, self.MIMEmain.as_string())
                mail.quit()
            except:
                return False

        finally:
            return True