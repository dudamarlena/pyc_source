# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jhunk/Downloads/pandokia/pandokia/default_config.py
# Compiled at: 2018-05-14 14:25:23
# Size of source mod 2**32: 7615 bytes


def readpass(fn=None):
    f = open(fn, 'r')
    return f.read().strip()


def complex_readpass():
    d = '/ssbwebv1/data2/pandokia/'
    pf = 'mysql_password'
    try:
        f = open(d + pf)
    except:
        try:
            f = open(d + '/alt_password')
        except:
            return
            s = f.read()
            f.close()
            return s.strip()
        except:
            pass
        else:
            f = open(d + pf)

    s = f.read()
    f.close()
    return s.strip()


import pandokia.db_sqlite as dbd, os
db_arg = '/tmp/pdk.db'
pdk_db = dbd.PandokiaDB(db_arg)
user_list = None
admin_user_list = ('sienkiew', 'cslocum', 'Nobody')
pdk_url = 'https://www.example.com/pandokia/pdk.cgi'
exclude_dirs = [
 '.svn',
 '.subversion',
 'CVS',
 '__pycache__',
 'tmp',
 'ref',
 'out',
 'okfile']
runner_glob = [
 ('*.py', 'nose'),
 ('test*.sh', 'shell_runner'),
 ('test*.csh', 'shell_runner'),
 ('*.pytest', 'pytest'),
 ('*.nose', 'nose'),
 ('*.minipyt', 'minipyt'),
 ('*.xml', 'regtest'),
 ('*.shunit2', 'shunit2'),
 ('*.c', 'maker')]
debug = True
server_maintenance = False
cginame = 'https://ssb.stsci.edu/pandokia/pdk.cgi'
statuses = [
 'P', 'F', 'E', 'D', 'M']
status_names = {'P':'pass', 
 'F':'fail', 
 'E':'error', 
 'D':'disable', 
 'M':'missing'}
default_user_email_preferences = [
 ('astrolib', 'n', 100),
 ('axe', 'n', 100),
 ('betadrizzle', 'n', 100),
 ('multidrizzle', 'f', 100),
 ('pydrizzle', 'f', 100),
 ('pyetc', 'n', 100),
 ('stsci_python', 'f', 100),
 ('stsdas', 'f', 100)]
default_qid_expire_days = 30
recurring_prefix = ('daily', 'etc_daily', 'etc_midday', 'etc_hst_daily', 'etc_jwst_daily',
                    'pandeia_nightly', 'jwst', 'pandeia_master_latest')
enable_magic_html_log = False
flagok_file = '/eng/ssb/tests/pdk_updates/%s.ok'