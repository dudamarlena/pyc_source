# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/virtualenv/python3.6.3/lib/python3.6/site-packages/create/cli.py
# Compiled at: 2019-06-02 12:21:47
# Size of source mod 2**32: 1451 bytes
"""Console script for create."""
import sys, click
from github import Github
import subprocess, os, configparser
cp = configparser.ConfigParser()
txtpath = os.path.dirname(os.path.abspath(__file__)) + '/config.txt'
token = ''
try:
    with open(txtpath) as (f):
        cp.read_file(f)
        token = cp.get('Config', 'password')
        print(token)
except:
    cfgfile = open(txtpath, 'w')
    cp.add_section('Config')
    token = str(input('There are no saved Github access tokens saved.\nPlease enter your Github token: '))
    cp.set('Config', 'password', token)
    cp.write(cfgfile)
    cfgfile.close()

def subrun(string):
    subprocess.run(string.split())


@click.command()
@click.argument('project')
def main(project):
    """Console script for create."""
    path = 'D:/Google Drive/Works/'
    print(token)
    g = Github(token).get_user()
    try:
        os.makedirs(path + project)
    except:
        print('Cannot create folder')
        return
    else:
        os.chdir(path + project)
        subrun('git init')
        g.create_repo(project, private=True)
        subrun('git remote add origin https://github.com/MatyiFKBT/{}.git'.format(project))
        subrun('touch README.md')
        subrun('git add .')
        subprocess.run(['git', 'commit', '-m', '"Initial commit"'])
        subrun('git push -u origin master')
        os.system('code .')


if __name__ == '__main__':
    main()