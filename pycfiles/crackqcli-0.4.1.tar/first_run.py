# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/byt3bl33d3r/.virtualenvs/CME_old/lib/python2.7/site-packages/cme/first_run.py
# Compiled at: 2016-12-29 01:51:56
import os, sqlite3, shutil, cme
from subprocess import check_output, PIPE
from sys import exit
CME_PATH = os.path.expanduser('~/.cme')
DB_PATH = os.path.join(CME_PATH, 'cme.db')
CERT_PATH = os.path.join(CME_PATH, 'cme.pem')
CONFIG_PATH = os.path.join(CME_PATH, 'cme.conf')

def first_run_setup(logger):
    if not os.path.exists(CME_PATH):
        logger.info('First time use detected')
        logger.info('Creating home directory structure')
        os.mkdir(CME_PATH)
        folders = ['logs', 'modules']
        for folder in folders:
            os.mkdir(os.path.join(CME_PATH, folder))

    if not os.path.exists(DB_PATH):
        logger.info('Initializing the database')
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('PRAGMA journal_mode = OFF')
        c.execute('CREATE TABLE "hosts" (\n            "id" integer PRIMARY KEY,\n            "ip" text,\n            "hostname" text,\n            "domain" test,\n            "os" text\n            )')
        c.execute('CREATE TABLE "links" (\n            "id" integer PRIMARY KEY,\n            "credid" integer,\n            "hostid" integer\n            )')
        c.execute('CREATE TABLE "credentials" (\n            "id" integer PRIMARY KEY,\n            "credtype" text,\n            "domain" text,\n            "username" text,\n            "password" text,\n            "pillagedfrom" integer\n            )')
        conn.commit()
        conn.close()
    if not os.path.exists(CONFIG_PATH):
        logger.info('Copying default configuration file')
        default_path = os.path.join(os.path.dirname(cme.__file__), 'data', 'cme.conf')
        shutil.copy(default_path, CME_PATH)
    if not os.path.exists(CERT_PATH):
        logger.info('Generating SSL certificate')
        try:
            out = check_output(['openssl', 'help'], stderr=PIPE)
        except OSError as e:
            if e.errno == os.errno.ENOENT:
                logger.error('OpenSSL command line utility is not installed, could not generate certificate')
                exit(1)
            else:
                logger.error(('Error while generating SSL certificate: {}').format(e))
                exit(1)

        os.system(('openssl req -new -x509 -keyout {path} -out {path} -days 365 -nodes -subj "/C=US" > /dev/null 2>&1').format(path=CERT_PATH))