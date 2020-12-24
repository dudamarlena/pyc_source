# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/sshtail/utils.py
# Compiled at: 2011-08-10 07:21:19
import os, paramiko

def prepend_home_dir(filename):
    """
    Prepends the home directory to the given filename if it doesn't
    already contain some kind of directory path.
    """
    if '/' not in filename:
        return os.path.join(os.environ['HOME'], '.ssh', filename)
    return filename


def load_rsa_key(filename):
    """
    Function to get an RSA key from the specified file for Paramiko.
    """
    return paramiko.RSAKey.from_private_key_file(prepend_home_dir(filename))


def load_dss_key(filename):
    """
    Function to get a DSS key from the specified file for Paramiko.
    """
    return paramiko.DSSKey.from_private_key_file(prepend_home_dir(filename))