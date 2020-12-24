# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/typtop/dbutils.py
# Compiled at: 2017-03-01 16:34:15
import struct
from typtop.pw_pkcrypto import decrypt, hash256, urlsafe_b64encode
import logging
from typtop.config import DB_NAME, GROUP
import pwd, grp, uuid, os

def is_user(u):
    try:
        pwd.getpwnam(u)
        return True
    except KeyError:
        return False


logger = logging.getLogger(DB_NAME)

def change_db_ownership(fl):
    try:
        g_id = grp.getgrnam(GROUP).gr_gid
        f_stat = os.stat(fl)
        f_uid, f_gid, mode = f_stat.st_uid, f_stat.st_gid, f_stat.st_mode
        if f_uid != 0 or f_gid != g_id or mode & 511 != 432:
            os.chown(fl, f_uid, g_id)
            os.chmod(fl, 432)
    except (KeyError, OSError) as e:
        logger.exception(e)


def setup_logger(logfile_path, debug_mode, user):
    log_level = logging.DEBUG if debug_mode else logging.INFO
    logger.setLevel(log_level)
    if not logger.handlers:
        handler = logging.FileHandler(logfile_path)
        formatter = logging.Formatter(('%(asctime)s:%(levelname)s:<{}>:[%(filename)s:%(lineno)s(%(funcName)s)>> %(message)s').format(user))
        handler.setFormatter(formatter)
        logger.addHandler(handler)


def is_in_top5_fixes(orig_pw, typo):
    return orig_pw in (
     typo.capitalize(), typo.swapcase(), typo.lower(),
     typo.upper(), typo[1:], typo[:-1])


def increment_val(dbh, tabname, key, keyf='desc', valuef='data'):
    """
    Increments the value of the key in tabname purely using sql query.
    final value of key in tabname will be tabname[keyf=key] + 1
    """
    q = ('update {tabname} set {valuef}=(select {valuef}+1 from {tabnme} where desc="{key}") where {keyf}="{key}"').format(tabname=tabname, keyf=keyf, key=key, valuef=valuef)
    dbh.query(q)


def get_machine_id():
    """Unique machine id tied to the machine, does not change easily"""
    return urlsafe_b64encode(hash256(bytes(uuid.getnode()))[:6])


def find_one(table, key, apply_type=str):
    """Finds a key from the table with column name 'desc', and value in
    'data'. It is faster than traditional find_one of 'dataset'.

    """
    return apply_type(table.get(key, ''))


def decode_decrypt_sym_count(key, ctx):
    """
    Receives the count ctx, decrypts it, decode it from base64
    and than from bytes to int
    """
    count_in_bytes = decrypt(key, ctx)
    return struct.unpack('<i', count_in_bytes)[0]