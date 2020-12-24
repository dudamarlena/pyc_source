# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/cookiecutter/{{cookiecutter.project_name}}/travis_pypi_setup.py
# Compiled at: 2017-01-01 18:58:14
# Size of source mod 2**32: 3786 bytes
"""Update encrypted deploy password in Travis config file
"""
from __future__ import print_function
import base64, json, os
from getpass import getpass
import yaml
from cryptography.hazmat.primitives.serialization import load_pem_public_key
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric.padding import PKCS1v15
try:
    from urllib import urlopen
except:
    from urllib.request import urlopen
else:
    GITHUB_REPO = '{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}'
    TRAVIS_CONFIG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.travis.yml')

    def load_key--- This code section failed: ---

 L.  36         0  SETUP_FINALLY        20  'to 20'

 L.  37         2  LOAD_GLOBAL              load_pem_public_key
                4  LOAD_FAST                'pubkey'
                6  LOAD_METHOD              encode
                8  CALL_METHOD_0         0  ''
               10  LOAD_GLOBAL              default_backend
               12  CALL_FUNCTION_0       0  ''
               14  CALL_FUNCTION_2       2  ''
               16  POP_BLOCK        
               18  RETURN_VALUE     
             20_0  COME_FROM_FINALLY     0  '0'

 L.  38        20  DUP_TOP          
               22  LOAD_GLOBAL              ValueError
               24  COMPARE_OP               exception-match
               26  POP_JUMP_IF_FALSE    74  'to 74'
               28  POP_TOP          
               30  POP_TOP          
               32  POP_TOP          

 L.  40        34  LOAD_FAST                'pubkey'
               36  LOAD_METHOD              replace
               38  LOAD_STR                 'BEGIN RSA'
               40  LOAD_STR                 'BEGIN'
               42  CALL_METHOD_2         2  ''
               44  LOAD_METHOD              replace
               46  LOAD_STR                 'END RSA'
               48  LOAD_STR                 'END'
               50  CALL_METHOD_2         2  ''
               52  STORE_FAST               'pubkey'

 L.  41        54  LOAD_GLOBAL              load_pem_public_key
               56  LOAD_FAST                'pubkey'
               58  LOAD_METHOD              encode
               60  CALL_METHOD_0         0  ''
               62  LOAD_GLOBAL              default_backend
               64  CALL_FUNCTION_0       0  ''
               66  CALL_FUNCTION_2       2  ''
               68  ROT_FOUR         
               70  POP_EXCEPT       
               72  RETURN_VALUE     
             74_0  COME_FROM            26  '26'
               74  END_FINALLY      

Parse error at or near `POP_TOP' instruction at offset 30


    def encrypt(pubkey, password):
        """Encrypt password using given RSA public key and encode it with base64.

    The encrypted password can only be decrypted by someone with the
    private key (in this case, only Travis).
    """
        key = load_key(pubkey)
        encrypted_password = key.encrypt(password, PKCS1v15)
        return base64.b64encode(encrypted_password)


    def fetch_public_key(repo):
        """Download RSA public key Travis will use for this repo.

    Travis API docs: http://docs.travis-ci.com/api/#repository-keys
    """
        keyurl = 'https://api.travis-ci.org/repos/{0}/key'.format(repo)
        data = json.loads(urlopen(keyurl).read())
        if 'key' not in data:
            errmsg = 'Could not find public key for repo: {}.\n'.format(repo)
            errmsg += 'Have you already added your GitHub repo to Travis?'
            raise ValueError(errmsg)
        return data['key']


    def prepend_line(filepath, line):
        """Rewrite a file adding a line to its beginning.
    """
        with open(filepath) as (f):
            lines = f.readlines()
        lines.insert(0, line)
        with openfilepath'w' as (f):
            f.writelines(lines)


    def load_yaml_config--- This code section failed: ---

 L.  82         0  LOAD_GLOBAL              open
                2  LOAD_FAST                'filepath'
                4  CALL_FUNCTION_1       1  ''
                6  SETUP_WITH           32  'to 32'
                8  STORE_FAST               'f'

 L.  83        10  LOAD_GLOBAL              yaml
               12  LOAD_METHOD              load
               14  LOAD_FAST                'f'
               16  CALL_METHOD_1         1  ''
               18  POP_BLOCK        
               20  ROT_TWO          
               22  BEGIN_FINALLY    
               24  WITH_CLEANUP_START
               26  WITH_CLEANUP_FINISH
               28  POP_FINALLY           0  ''
               30  RETURN_VALUE     
             32_0  COME_FROM_WITH        6  '6'
               32  WITH_CLEANUP_START
               34  WITH_CLEANUP_FINISH
               36  END_FINALLY      

Parse error at or near `ROT_TWO' instruction at offset 20


    def save_yaml_config(filepath, config):
        with openfilepath'w' as (f):
            yaml.dump(config, f, default_flow_style=False)


    def update_travis_deploy_password(encrypted_password):
        """Update the deploy section of the .travis.yml file
    to use the given encrypted password.
    """
        config = load_yaml_config(TRAVIS_CONFIG_FILE)
        config['deploy']['password'] = dict(secure=encrypted_password)
        save_yaml_configTRAVIS_CONFIG_FILEconfig
        line = '# This file was autogenerated and will overwrite each time you run travis_pypi_setup.py\n'
        prepend_lineTRAVIS_CONFIG_FILEline


    def main(args):
        public_key = fetch_public_key(args.repo)
        password = args.password or getpass('PyPI password: ')
        update_travis_deploy_password(encryptpublic_keypassword)
        print("Wrote encrypted password to .travis.yml -- you're ready to deploy")


    if '__main__' == __name__:
        import argparse
        parser = argparse.ArgumentParser(description=__doc__)
        parser.add_argument('--repo', default=GITHUB_REPO, help=('GitHub repo (default: %s)' % GITHUB_REPO))
        parser.add_argument('--password', help='PyPI password (will prompt if not provided)')
        args = parser.parse_args()
        main(args)