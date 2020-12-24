# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/git2gitee/util.py
# Compiled at: 2020-05-04 01:42:24
# Size of source mod 2**32: 1251 bytes
"""
encrypt by public key
"""
import re
from base64 import b64encode
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5

def encrypt_pwd(password, public_key):
    """
    :params public_key:
        -----BEGIN PUBLIC KEY----
keys
-----END ...-----
    :params password: csrf-token + '$gitee$' + password
    """
    rsa_key = RSA.import_key(public_key)
    encryptor = PKCS1_v1_5.new(rsa_key)
    cipher = b64encode(encryptor.encrypt(password.encode('utf-8')))
    return cipher.decode('utf-8')


def parse_token(response):
    """parse csrf token form gitee"""
    result = re.search('<meta content="(.*?)" name="csrf-token"', response.text)
    return result.group(1)


def valib_github_repo_url(repo):
    """return repo url"""
    github_base_url = 'https://github.com/'
    if repo.startswith(github_base_url):
        return repo
    else:
        return github_base_url + repo


def parse_repo_name(repo):
    """parse repo name"""
    return repo.split('/')[-1:][0]


def to_gitee_repo_url(username, repo_name):
    """
    :params username: gitee username
    :params repo_name:  import repo name
    return gitee repo url
    """
    return 'https://gitee.com/{}/{}'.format(username, repo_name)