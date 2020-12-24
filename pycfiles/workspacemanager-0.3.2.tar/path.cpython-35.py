# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hayj/Workspace/Python/Organization/WorkspaceManager/workspacemanager/path.py
# Compiled at: 2018-08-09 14:56:23
# Size of source mod 2**32: 3676 bytes
import os, sh
from workspacemanager.utils import *
from workspacemanager.path import *
import sys
path = '\n/home/hayj/Workspace/Python/Octopeek/HumanDriver\n/home/hayj/Workspace/Python/Octopeek/PrivaliaCrawler\n/home/hayj/Workspace/Python/Octopeek/ProxyBench\n/home/hayj/Workspace/Python/Octopeek/MailStat\n/home/hayj/Workspace/Python/Datasets/SparkBasics\n/home/hayj/Workspace/Python/Datasets/TwitterArchiveOrg\n/home/hayj/Workspace/Python/Crawling/NewsTools\n/home/hayj/Workspace/Python/Crawling/TwitterCrawler\n/home/hayj/Workspace/Python/Crawling/DomainDuplicate\n/home/hayj/Workspace/Python/Crawling/WebWatcher\n/home/hayj/Workspace/Python/Crawling/WebCrawler\n/home/hayj/Workspace/Python/Crawling/Unshortener\n/home/hayj/Workspace/Python/Crawling/Scroller\n/home/hayj/Workspace/Python/Crawling/Error404Detector\n/home/hayj/Workspace/Python/Crawling/HoneypotDetector\n/home/hayj/Workspace/Python/Crawling/WebBrowser\n/home/hayj/Workspace/Python/Crawling/NewsCrawler\n/home/hayj/Workspace/Python/Utils/DataStructureTools\n/home/hayj/Workspace/Python/Utils/NLPTools\n/home/hayj/Workspace/Python/Utils/MachineLearning\n/home/hayj/Workspace/Python/Utils/DataTools\n/home/hayj/Workspace/Python/Utils/SystemTools\n/home/hayj/Workspace/Python/Utils/DatabaseTools\n/home/hayj/Workspace/Python/Utils/DeviceTools\n/home/hayj/Workspace/Python/Utils/NetworkTools\n/home/hayj/Workspace/Python/Renewal/NewsSourceAggregator\n/home/hayj/.local/share/virtualenvs/st-venv/lib/python35.zip\n/home/hayj/.local/share/virtualenvs/st-venv/lib/python3.5\n/home/hayj/.local/share/virtualenvs/st-venv/lib/python3.5/plat-linux\n/home/hayj/.local/share/virtualenvs/st-venv/lib/python3.5/lib-dynload\n/home/hayj/Programs/python-3.5.4/lib/python3.5\n/home/hayj/Programs/python-3.5.4/lib/python3.5/plat-linux\n/home/hayj/.local/share/virtualenvs/st-venv/lib/python3.5/site-packages\n'
print()
sys.path = []
for current in path.split('\n'):
    if len(current) > 2:
        sys.path.append(current)

for current in sys.path:
    print(current)

exit()

def generatePythonpath():
    venvName = 'st-venv'
    workspacePath = '/home/' + getUser() + '/Workspace'
    venvPath = '/home/' + getUser() + '/.virtualenvs/' + venvName
    projects = getAllProjects(workspacePath)
    pewPythonpathPath = venvPath + '/lib/python3.5/site-packages/_virtualenv_path_extensions.pth'
    removeFile(pewPythonpathPath)
    print('Installing all projects in the python path of ' + venvName + '...')
    for current in projects.keys():
        sh.pew('in', venvName, 'pew', 'add', current)
        print(current)


if __name__ == '__main__':
    generatePythonpath()