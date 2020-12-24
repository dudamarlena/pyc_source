# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win-amd64\egg\prboard\settings.py
# Compiled at: 2016-04-23 02:43:52
import os
from utils import parse_pr_filters
PRBOARD_BASE_URL = 'https://api.github.com'
PRBOARD_PR_FILTER = ''
PRBOARD_REPO_FILTER = ''
PRBOARD_ORG_FILTER = ''
PRBOARD_GITHUB_USERNAME = os.environ.get('PRBOARD_GITHUB_USERNAME', '')
PRBOARD_GITHUB_PASSWORD = os.environ.get('PRBOARD_GITHUB_PASSWORD', '')
PRBOARD_DETALED_MODE = True
PRBOARD_REPOS = PRBOARD_PR_FILTER.split(',')
PRBOARD_PR = parse_pr_filters(PRBOARD_PR_FILTER)
PRBOARD_ORG = PRBOARD_ORG_FILTER.split(',')
PRBOARD_SETTINGS_FILE = os.environ.get('PRBOARD_SETTINGS_FILE', os.path.join(os.path.expanduser('~'), 'prboard.cfg'))