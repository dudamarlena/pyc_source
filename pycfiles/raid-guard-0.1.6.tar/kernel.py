# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/stein/Projekte/eclipse/raid-guard/raid_guard/kernel.py
# Compiled at: 2013-03-13 12:38:09
import os, smtplib
from email.mime.text import MIMEText
import sys, time
from iniparse import INIConfig
from string import lower
import unittest, logging, shutil

def init_logging(test=False):
    if __name__ == '__main__':
        logpath = '%s/raid_guard.log' % os.environ['HOME']
        logging.basicConfig(filename=logpath, format='%(asctime)s %(message)s', filemode='w', level=logging.DEBUG)
        logging.info('Log path for development: home/raid_guard.log')
    elif test:
        pass
    else:
        try:
            logpath = '/var/log/raid_guard.log'
            logging.basicConfig(filename=logpath, format='%(asctime)s %(message)s', level=logging.INFO)
        except IOError as e:
            raise IOError('%s. %s' % (e, 'Run script as root!'))


def run_test():
    suite1 = unittest.TestLoader().loadTestsFromTestCase(TestGuard)
    suite2 = unittest.TestLoader().loadTestsFromTestCase(TestMail)
    unittest.TextTestRunner(verbosity=2).run(suite1)
    unittest.TextTestRunner(verbosity=2).run(suite2)
    sys.exit()


class Guard:

    def __init__(self, mail_dict={}, alerts=[2, 3], ini_path=None, test=False):
        """mail_dict must contain keywords: 
        mail_dict={'value':'just a dict'}
        and should:
        mail_dict={
        'mail_from':'mail@yourdomain.net',
        'host_user':'your_mail_host_username',
        'host_pass':'your_passw',
        'host_smtp':'smtp.domain.net',
        }
        """
        if test:
            init_logging(test)
        else:
            init_logging()
        self.mail = mail_dict
        self.allerts = alerts
        self.initial_mail = False
        self.sleep = 36000
        if not mail_dict:
            if not ini_path:
                ini_file = '/root/.raid_guard.ini'
                if not os.path.isfile(ini_file):
                    shutil.copyfile('/usr/share/raid_guard/raid_guard.ini', ini_file)
            else:
                ini_file = ini_path
            logging.debug('there is no initial mail dict')
            if not os.path.isfile(ini_file):
                m = '%s not found' % ini_file
                logging.error(m)
                raise IOError(m)
            parser = INIConfig(file(ini_file))
            self.sleep = int(parser['daemon']['check_interval'])
            self.allerts = []
            if lower(parser['daemon']['alert_raidstatus_ok']) == lower('YES'):
                self.allerts.append(1)
            if lower(parser['daemon']['alert_raidstatus_malfunction']) == lower('YES'):
                self.allerts.append(2)
            if lower(parser['daemon']['alert_raidstatus_unsure']) == lower('YES'):
                self.allerts.append(3)
            self.mail['host_smtp'] = parser['mail']['host_smtp']
            self.mail['host_user'] = parser['mail']['host_username']
            self.mail['host_pass'] = parser['mail']['host_password']
            self.mail['mail_from'] = parser['mail']['mail_from']
            mailto = parser['mail']['mail_to']
            mailto = mailto.strip(' ').replace(',', '').replace('  ', ' ').split()
            self.mail['recipient_list'] = mailto

    def start_daemon(self, sleep=None):
        logging.debug('daemon was started')
        if not sleep:
            sleep = self.sleep
        self.allert_admin(4)
        while True:
            self.check_raid()
            time.sleep(sleep)

    def _get_status(self, inp):
        """returns status as integer"""
        st = str(inp)
        st = st.replace('\n', '').split(' ')
        logging.debug('Status string to parse: %s' % st)
        if '[U_]' in st:
            logging.info('Raid status: Malfunction')
            return 2
        else:
            if '[UU]' in st:
                logging.info('Raid status: OK')
                return 1
            logging.info('Raid status: Unknown')
            return 3

    def check_raid(self):
        file = '/proc/mdstat'
        o = open(file, 'r')
        data = o.read()
        o.close()
        status = self._get_status(data)
        logging.debug('raid checked! Status: %s' % status)
        if status in self.allerts:
            self.allert_admin(status)

    def allert_admin(self, status):
        subj = 'Raid Guard Disc Status'
        if status == 1:
            text = 'Hard discs OK.'
        elif status == 2:
            text = 'Minimum one hard disc is defect! Check it with: "cat /proc/mdstat"'
        elif status == 3:
            text = "I'am unsure about your disks. Please check your raid and hard discs by your self."
        elif status == 4:
            text = 'Raid Guard demon is active now.'
            subj = 'Raid Guard Status'
        m = Mail(self.mail)
        m.create(subj=subj, message=text, recipients=self.mail['recipient_list'])
        m.send()


class Mail:

    def __init__(self, data_dict):
        """
        data_dict={
        'mail_from':'mail@yourdomain.net',
        'host_user':'your_mail_host_username',
        'host_pass':'your_passw',
        'host_smtp':'smtp.domain.net',
        }
        """
        self.data = data_dict
        self.msg = None
        self.recipients = []
        return

    def create(self, subj, message, recipients):
        if not type(recipients) == list:
            self.recipients = [
             recipients]
        else:
            self.recipients = recipients
        self.msg = MIMEText(message.encode('utf-8'), 'plain', 'UTF-8')
        self.msg['Subject'] = subj
        self.msg['From'] = self.data['mail_from']
        self.msg['To'] = (',').join(self.recipients)
        self.msg['log_message'] = message

    def send(self):
        try:
            s = smtplib.SMTP(self.data['host_smtp'])
            s.login(self.data['host_user'], self.data['host_pass'])
            logging.debug('smtp login ok.')
        except smtplib.socket.error as e:
            m = '%s. %s' % (e, 'Check your raid_guard.ini. May your login data are wrong.')
            logging.error(m)
            raise smtplib.socket.error(m)

        try:
            s.sendmail(self.msg['From'], self.recipients, self.msg.as_string())
            s.quit()
            m = 'mail was send to %s with message: %s' % (self.recipients, self.msg['log_message'])
            logging.info(m)
        except smtplib.SMTPSenderRefused as e:
            if '@' in self.data['host_user']:
                del self.msg['From']
                self.msg['From'] = self.data['host_user']
                s.sendmail(self.msg['From'], self.recipients, self.msg.as_string())
                s.quit()
                logging.warning("\n                                Fall back: Alternate mail sending routine\n                                (changed your sender address) successful executed!\n                                probably your mail host don't allow to send an\n                                email with an unknown mail address\n                            ")
                m = 'mail was send to %s with message: %s' % (self.recipients, self.msg['log_message'])
                logging.info(m)
            else:
                t = "\n                    Probably your mail host don't allow to send an\n                    email with an unknown mail address\n                    "
                m = '%s: %s' % (e, t)
                logging.error(m)
                raise smtplib.SMTPSenderRefused(m, '', '')


class TestMail(unittest.TestCase):

    def setUp(self):
        data_dict = {'mail_from': 'm@yourd.eu', 
           'host_user': 'your_mail_host_username', 
           'host_pass': 'your_passw', 
           'host_smtp': 'smtp.domain.net'}
        self.mail = Mail(data_dict)

    def test_mimetext_instance(self):
        self.mail.create(subj='a subject', message=' a message', recipients=[
         '1@mm.eu', '2@mm.eu'])
        self.assertEqual(self.mail.msg['Subject'], 'a subject')
        self.assertEqual(self.mail.msg['From'], 'm@yourd.eu')
        self.assertEqual(type(self.mail.msg['To']), type(''))
        self.assertEqual(self.mail.msg['To'], '1@mm.eu,2@mm.eu')

    def test_send(self):
        self.assertRaises(smtplib.SMTPAuthenticationError, self.mail.send)


class TestGuard(unittest.TestCase):

    def setUp(self):
        d = {'value': 'some dict'}
        self.g = Guard(mail_dict=d, test=True)
        self.pos = '2096064 blocks [2/2] [UU]\n        active raid1 sdb1[1] sda1[0]'
        self.neg = 'active raid1 sda4[0] sdb4[1](F)\n        1822442815 blocks super 1.2 [2/1] [U_]'
        self.neg2 = '2096064 blocks [2/2] [UU]\n        active raid1 sdb1[1] sda1[0]\n        active raid1 sda4[0] sdb4[1](F)\n        1822442815 blocks super 1.2 [2/1] [U_]'
        self.non = 'Personalities : \n        unused devices: <none>'

    def test_positive(self):
        self.assertEqual(1, self.g._get_status(self.pos))

    def test_negative(self):
        self.assertEqual(2, self.g._get_status(self.neg))
        self.assertEqual(2, self.g._get_status(self.neg2))

    def test_non(self):
        self.assertEqual(3, self.g._get_status(self.non))


if __name__ == '__main__':
    ini_file = '%s/.raid_guard.ini' % os.environ['HOME']
    g = Guard(ini_path=ini_file)
    g.start_daemon()