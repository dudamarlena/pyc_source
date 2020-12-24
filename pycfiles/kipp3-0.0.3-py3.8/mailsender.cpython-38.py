# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/kipp3/utils/mailsender.py
# Compiled at: 2019-12-16 21:55:05
# Size of source mod 2**32: 5778 bytes
"""
------------
Email Sender
------------

Usage
::
    from kipp3.utils import EmailSender

    sender = EmailSender(opt.SMTP_HOST)  # SMTP_HOST is different between NOVA and PRD
    receivers = ','.join([xxx, xxx, xxx])

    sender.send_email(
        mail_from='data@movoto.com',
        mail_to=receivers,
        subject='Email Title',
        content='Email content'
    )

"""
from __future__ import unicode_literals
import smtplib
from textwrap import dedent
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from .logger import get_logger as get_kipp_logger
HOST = 'smtp.internal.ng.movoto.net'
FROM_ADDRESS = 'mls-normalizer-ng@movoto.com'

class EmailSender(object):

    def __init__(self, host=HOST, port=None, username=None, passwd=None, logger=None, use_tls=True):
        """Initiallize EmailSender

        Args:
            host (str, default movoto): SMTP server host
            port (int, default=None): SMTP server port
            logger (logging.logger, default=kipp_internal_logger):
            use_tls (bool, default=True)
        """
        self._host = host
        self._port = port
        self._user = username
        self._passwd = passwd
        self._logger = logger
        self._use_tls = use_tls

    def set_smtp_host(self, host):
        assert host, 'smtp host should not be empty'
        assert isinstance(host, str), 'smtp host should be string'
        self._host = host

    def set_smtp_port(self, port):
        assert port, 'smtp port should not be empty'
        assert isinstance(port, int), 'smtp port should be string'
        self._port = port

    def get_logger(self):
        return self._logger or get_kipp_logger().getChild('email')

    def parse_content(self, content):
        return '<font face="Microsoft YaHei, Helvetica Neue, Helvetica">{}</font>'.format('<p>{}</p>'.format('</p><p>'.join(content.splitlines())))

    def get_html(self, body):
        return '\n            <head>\n            <meta http-equiv="Content-Type" content="text/html; charset=utf-8">\n            <title>html title</title>\n            <style type="text/css" media="screen">\n                table{{\n                    background-color: #f9f9f9;\n                    empty-cells: hide;\n                }}\n            </style>\n            </head>\n            <body>\n                {body}\n            </body>\n            '.format(body=body)

    def _filter_mail_to(self, mail_to):
        return ','.join(set(mail_to.split(',')))

    def send_email--- This code section failed: ---

 L. 127         0  LOAD_GLOBAL              MIMEMultipart
                2  LOAD_STR                 'alternative'
                4  CALL_FUNCTION_1       1  ''
                6  STORE_FAST               'msg'

 L. 128         8  LOAD_FAST                'msg'
               10  LOAD_METHOD              set_charset
               12  LOAD_STR                 'utf-8'
               14  CALL_METHOD_1         1  ''
               16  POP_TOP          

 L. 129        18  LOAD_FAST                'content'
               20  POP_JUMP_IF_FALSE    44  'to 44'

 L. 130        22  LOAD_FAST                'msg'
               24  LOAD_METHOD              attach
               26  LOAD_GLOBAL              MIMEText
               28  LOAD_FAST                'self'
               30  LOAD_METHOD              parse_content
               32  LOAD_FAST                'content'
               34  CALL_METHOD_1         1  ''
               36  LOAD_STR                 'html'
               38  CALL_FUNCTION_2       2  ''
               40  CALL_METHOD_1         1  ''
               42  POP_TOP          
             44_0  COME_FROM            20  '20'

 L. 132        44  LOAD_FAST                'html'
               46  POP_JUMP_IF_FALSE    70  'to 70'

 L. 133        48  LOAD_FAST                'msg'
               50  LOAD_METHOD              attach
               52  LOAD_GLOBAL              MIMEText
               54  LOAD_FAST                'self'
               56  LOAD_METHOD              get_html
               58  LOAD_FAST                'html'
               60  CALL_METHOD_1         1  ''
               62  LOAD_STR                 'html'
               64  CALL_FUNCTION_2       2  ''
               66  CALL_METHOD_1         1  ''
               68  POP_TOP          
             70_0  COME_FROM            46  '46'

 L. 135        70  LOAD_FAST                'subject'
               72  LOAD_FAST                'msg'
               74  LOAD_STR                 'Subject'
               76  STORE_SUBSCR     

 L. 136        78  LOAD_FAST                'mail_from'
               80  LOAD_FAST                'msg'
               82  LOAD_STR                 'From'
               84  STORE_SUBSCR     

 L. 137        86  LOAD_FAST                'self'
               88  LOAD_METHOD              _filter_mail_to
               90  LOAD_FAST                'mail_to'
               92  CALL_METHOD_1         1  ''
               94  LOAD_FAST                'msg'
               96  LOAD_STR                 'To'
               98  STORE_SUBSCR     

 L. 139       100  SETUP_FINALLY       220  'to 220'

 L. 140       102  LOAD_GLOBAL              smtplib
              104  LOAD_METHOD              SMTP
              106  LOAD_FAST                'self'
              108  LOAD_ATTR                _host
              110  LOAD_FAST                'self'
              112  LOAD_ATTR                _port
              114  CALL_METHOD_2         2  ''
              116  STORE_FAST               's'

 L. 141       118  LOAD_FAST                'self'
              120  LOAD_ATTR                _use_tls
              122  POP_JUMP_IF_FALSE   132  'to 132'

 L. 142       124  LOAD_FAST                's'
              126  LOAD_METHOD              starttls
              128  CALL_METHOD_0         0  ''
              130  POP_TOP          
            132_0  COME_FROM           122  '122'

 L. 144       132  LOAD_FAST                'self'
              134  LOAD_ATTR                _user
              136  POP_JUMP_IF_FALSE   160  'to 160'
              138  LOAD_FAST                'self'
              140  LOAD_ATTR                _passwd
              142  POP_JUMP_IF_FALSE   160  'to 160'

 L. 145       144  LOAD_FAST                's'
              146  LOAD_METHOD              login
              148  LOAD_FAST                'self'
              150  LOAD_ATTR                _user
              152  LOAD_FAST                'self'
              154  LOAD_ATTR                _passwd
              156  CALL_METHOD_2         2  ''
              158  POP_TOP          
            160_0  COME_FROM           142  '142'
            160_1  COME_FROM           136  '136'

 L. 147       160  LOAD_FAST                's'
              162  LOAD_METHOD              sendmail
              164  LOAD_FAST                'mail_from'
              166  LOAD_FAST                'mail_to'
              168  LOAD_METHOD              split
              170  LOAD_STR                 ','
              172  CALL_METHOD_1         1  ''
              174  LOAD_FAST                'msg'
              176  LOAD_METHOD              as_string
              178  CALL_METHOD_0         0  ''
              180  CALL_METHOD_3         3  ''
              182  POP_TOP          

 L. 148       184  LOAD_FAST                's'
              186  LOAD_METHOD              quit
              188  CALL_METHOD_0         0  ''
              190  POP_TOP          

 L. 149       192  LOAD_FAST                'self'
              194  LOAD_METHOD              get_logger
              196  CALL_METHOD_0         0  ''
              198  LOAD_METHOD              info

 L. 150       200  LOAD_STR                 'send email successfully to {} with subject {}'
              202  LOAD_METHOD              format
              204  LOAD_FAST                'mail_to'
              206  LOAD_FAST                'subject'
              208  CALL_METHOD_2         2  ''

 L. 149       210  CALL_METHOD_1         1  ''
              212  POP_TOP          

 L. 152       214  POP_BLOCK        
              216  LOAD_CONST               True
              218  RETURN_VALUE     
            220_0  COME_FROM_FINALLY   100  '100'

 L. 153       220  DUP_TOP          
              222  LOAD_GLOBAL              Exception
              224  COMPARE_OP               exception-match
          226_228  POP_JUMP_IF_FALSE   264  'to 264'
              230  POP_TOP          
              232  POP_TOP          
              234  POP_TOP          

 L. 154       236  LOAD_FAST                'self'
              238  LOAD_METHOD              get_logger
              240  CALL_METHOD_0         0  ''
              242  LOAD_METHOD              exception

 L. 155       244  LOAD_STR                 'fail to send email to {} with subject {} for error:'
              246  LOAD_METHOD              format

 L. 156       248  LOAD_FAST                'mail_to'

 L. 156       250  LOAD_FAST                'subject'

 L. 155       252  CALL_METHOD_2         2  ''

 L. 154       254  CALL_METHOD_1         1  ''
              256  POP_TOP          

 L. 159       258  POP_EXCEPT       
              260  LOAD_CONST               False
              262  RETURN_VALUE     
            264_0  COME_FROM           226  '226'
              264  END_FINALLY      

Parse error at or near `RETURN_VALUE' instruction at offset 218

    def generate_table(self, heads, contents):
        """Generate the html of table in email

        Args:
            heads (list): Table head
            contents (list of lists): Table contents

        Returns:
            str:

        Examples:
        ::
            heads = ('head 1', 'head 2', 'head 3')
            contents = (
                ('cell 1-1', 'cell 1-2', 'cell 1-3'),
                ('cell 2-1', 'cell 2-2', 'cell 2-3')
            )

            table_html = sender.generate_table(heads, contents)
        """
        thead = ''.join(['<th><p>{}</p></th>\n'.format(str(h)) for h in heads])
        tbody = ''
        for cnt in contents:
            tbody += '<tr>{}</tr>\n'.format(''.join(['<td><p>{}</p></td>'.format(str(h)) for h in cnt]))
        else:
            return dedent('\n            <table style="table-layout:fixed;" cellspacing="0" cellpadding="10">\n                <thead><tr>{thead}</tr></thead>\n                <tbody>{tbody}</tbody>\n            </table>\n            ').format(thead=thead,
              tbody=tbody)


if __name__ == '__main__':
    sender = EmailSender()
    assert sender.send_email(mail_to='lcai@movoto.com,lcai@movoto.com',
      subject='test: kipp.utils.EmailSender',
      content='fake-content\n\nline 2',
      mail_from='kipp@movoto.com')