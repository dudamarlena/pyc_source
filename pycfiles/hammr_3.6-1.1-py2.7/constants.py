# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/hammr/utils/constants.py
# Compiled at: 2016-12-16 11:09:34
__author__ = 'UShareSoft'
import os, tempfile
VERSION = '1.1'
TMP_WORKING_DIR = tempfile.gettempdir() + os.sep + 'hammr-' + str(os.getpid())
HTTP_TIMEOUT = 30
TEMPLATE_JSON_FILE_NAME = 'template.json'
TEMPLATE_JSON_NEW_FILE_NAME = 'template.json'
FOLDER_BUNDLES = 'bundles'
FOLDER_CONFIGS = 'config'
FOLDER_DEPLOYMENT_SCENARIO = 'deploymentScenario'
FOLDER_LOGO = 'logo'
URI_SCAN_BINARY = '/resources/uforge-scan.bin'
SCAN_BINARY_NAME = 'uforge-scan.bin'
QUOTAS_SCAN = 'scan'
QUOTAS_TEMPLATE = 'appliance'
QUOTAS_GENERATION = 'generation'
QUOTAS_DISK_USAGE = 'diskusage'