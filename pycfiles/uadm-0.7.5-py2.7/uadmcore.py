# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/uadm/uadmcore.py
# Compiled at: 2012-07-05 09:09:45
__author__ = 'Pierre-Yves Langlois'
__copyright__ = 'https://github.com/pylanglois/uadm/blob/master/LICENCE'
__credits__ = ['Pierre-Yves Langlois']
__license__ = 'BSD'
__version__ = '1.0'
__maintainer__ = 'Pierre-Yves Langlois'
__status__ = 'Production'
import sys, os
from os import path
import socket, subprocess, shlex, logging

def mod_conf(params, override=True):
    """
    This method will modify configuration in the CONF_MAP dictionarie
    """
    for p in params.keys():
        if p in CONF_MAP and override or p not in CONF_MAP:
            CONF_MAP[p] = params[p]


def init_logger():
    """
    This method create a logger with an output to a file
    """
    log_name = '%s.log' % CONF_MAP['UADM_TOOL_NAME'].split('.')[0]
    logger = logging.getLogger(CONF_MAP['UADM_TOOL_NAME'])
    logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler('%s/%s' % (CONF_MAP['UADM_LOG_PATH'], log_name), mode='a+')
    fh.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    fh = logging.StreamHandler(sys.stdout)
    fh.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    return logger


def get_host_info():
    """
    This method tries to get the IP and the hostname of the computer
    """
    hostname = socket.getfqdn()
    ip = None
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('www.google.ca', 0))
        ip = s.getsockname()[0]
    except:
        pass

    return {'hostname': unicode(hostname), 'ip': unicode(ip)}


def mail(subject, message, image_list=[], smtp_server=None, from_add=None, to_add=None):
    """
    Code from activestate, slightly modified, allowing to send mail
    """
    smtp_server = smtp_server if smtp_server else CONF_MAP['UADM_SMTP_SERVER']
    from_add = from_add if from_add else CONF_MAP['UADM_SRC_EMAIL']
    to_add = to_addd if to_add else CONF_MAP['UADM_SRC_EMAIL']
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    from email.mime.image import MIMEImage
    strFrom = from_add
    strTo = to_add
    msgRoot = MIMEMultipart('related')
    msgRoot.set_charset('UTF-8')
    msgRoot['Subject'] = subject
    msgRoot['From'] = strFrom
    msgRoot['To'] = strTo
    msgRoot.preamble = 'This is a multi-part message in MIME format.'
    msgAlternative = MIMEMultipart('alternative')
    msgAlternative.set_charset('UTF-8')
    msgRoot.attach(msgAlternative)
    msgText = MIMEText('This is the alternative plain text message.')
    msgAlternative.attach(msgText)
    img_iter = 0
    for image in image_list:
        if image is not None:
            message += '<img src="cid:image%d">' % img_iter
            img_iter += 1

    msgText = MIMEText(unicode(message), 'html', 'UTF-8')
    msgAlternative.attach(msgText)
    img_iter = 0
    for image in image_list:
        if image is not None:
            fp = open(image, 'rb')
            msgImage = MIMEImage(fp.read())
            msgImage.add_header('Content-ID', '<image%d>' % img_iter)
            msgRoot.attach(msgImage)
            img_iter += 1
            fp.close()

    import smtplib
    smtp = smtplib.SMTP(smtp_server)
    smtp.sendmail(strFrom, strTo, msgRoot.as_string())
    smtp.quit()
    return


def send_report(message, subject_prefix=None):
    """
    This method will send an email to the administrator.
    """
    subject_prefix = subject_prefix if subject_prefix else CONF_MAP['UADM_SUCCESS_SUBJECT']
    subject = '[%s] %s sur %s (%s)' % (CONF_MAP['UADM_TOOL_NAME'],
     subject_prefix,
     HOST_INFO['hostname'],
     HOST_INFO['ip'])
    if not CONF_MAP['UADM_DISABLE_MAIL']:
        mail(subject, message)


def send_error_report(message, subject_prefix=None):
    subject_prefix = subject_prefix if subject_prefix else CONF_MAP['UADM_ERROR_SUBJECT']
    send_report(message, subject_prefix)


def debug_pinfo(pinfo, command, newline='<br>'):
    """
    This method build a readable version of the process output
    """
    msg = unicode('command: %(command)s%(newline)sreturn code: %(return_code)s%(newline)sstderr: %(stderr)sstdout: %(stdout)s' % {'newline': newline, 
       'command': command, 
       'return_code': pinfo['return_code'], 
       'stderr': split_output(pinfo['stderr'], newline=newline), 
       'stdout': split_output(pinfo['stdout'], newline=newline)})
    return msg


def split_output(output, newline='<br>'):
    """
    Format each line with the proper newline definition
    """
    output = unicode(output, 'UTF-8')
    out = ''
    for line in output.split('\n'):
        out += line + newline

    return out


def run_cmd(command):
    """
    This method runs a single command with Popen and return a map of the output
    """
    proc = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    ret = proc.wait()
    out, err = proc.communicate()
    return {'process': proc, 'return_code': ret, 'stdout': out, 'stderr': err}


def cfb(string_to_clean):
    """
    This method format a multiple line command into a single line command
    """
    return (' ').join(string_to_clean.strip('\n').split())


def exec_cmd_list(cmd_list):
    """
    This method take a list of command and execute them with Popen. If a command fails
    a report is send by mail to the administrator
    """
    output = ''
    completed = True
    for command in cmd_list:
        pinfo = run_cmd(command)
        output += debug_pinfo(pinfo, command)
        if pinfo['return_code'] == 0:
            l().info('%s' % debug_pinfo(pinfo, command, newline='\n'))
        else:
            completed = False
            l().error('%s' % debug_pinfo(pinfo, command, newline='\n'))
            send_error_report(output)
            break

    if completed and CONF_MAP['UADM_REPORT_ON_SUCCESS']:
        send_report('%s' % output)
    return (completed, pinfo)


def l(init=None):
    if init:
        l_instance['l'] = init
    return l_instance['l']


def get_rel_path(filename):
    fn = os.path.join(os.path.dirname(__file__), filename)
    return fn


HOST_INFO = get_host_info()
CONF_MAP = {'UADM_TOOL_NAME': unicode(path.basename(sys.modules['__main__'].__file__)), 
   'UADM_LOG_PATH': '/var/log/uadm', 
   'UADM_SCRIPT_PATH': '/etc/uadm/scripts', 
   'UADM_SMTP_SERVER': 'smtp.example.com', 
   'UADM_SRC_EMAIL': 'tech@example.com', 
   'UADM_SUCCESS_SUBJECT': 'Success', 
   'UADM_ERROR_SUBJECT': 'Error', 
   'UADM_REPORT_ON_SUCCESS': False, 
   'UADM_DISABLE_MAIL': False, 
   'UADM_ENABLED': True, 
   'UADM_DOCROOT': '/var/www', 
   'UADM_APACHE_VHOST_DIR': '/etc/apache2/sites-available', 
   'UADM_LOGROTATE_DIR': '/etc/logrotate.d', 
   'UADM_AUTO_MOUNT_DIR': '/usr/local/bin/auto_mount_www', 
   'UADM_USE_CENTRIFY': False}
l_instance = {'l': ''}
if __name__ == 'uadm.uadmcore':
    conf_path = '/etc/uadm/uadm.conf'
    if path.exists(conf_path):
        import imp
        conf = imp.load_source('uadm.conf', conf_path)
        mod_conf(conf.CONF_MAP)
    l(init_logger())
    if not CONF_MAP['UADM_ENABLED']:
        l().info('UADM scripts are not enabled. Change your conf file with "UADM_ENABLED" : True, EXITING!!! ')
        exit(1)