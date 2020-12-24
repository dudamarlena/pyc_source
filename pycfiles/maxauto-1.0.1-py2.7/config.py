# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/max/config.py
# Compiled at: 2019-04-27 22:50:06
import os, shutil, time
from tools.loggers import JFMlogging
logger = JFMlogging().getloger()
project_path = os.path.abspath(os.path.dirname(__file__))
android_tmp = os.path.join(project_path, 'report/tmp/')
install_app_log = os.path.join(project_path, 'report/tmp/install_app.log')
lanuch_app_log = os.path.join(project_path, 'report/tmp/lanuch_app.log')
logintest_app_log = os.path.join(project_path, 'report/tmp/login_app.log')
uninstall_app_log = os.path.join(project_path, 'report/tmp/uninstall_app.log')
appium_log = os.path.join(project_path, 'report/tmp/appium.log')
sdcard_path = '/sdcard/'
crash_savepath = os.path.join(project_path, 'report/tmp/crash.log')
monkey_log = os.path.join(project_path, 'report/tmp/monkey.log')
monkey_jar = os.path.join(project_path, 'monkey/libs/monkey.jar')
framework_jar = os.path.join(project_path, 'monkey/libs/framework.jar')
device_crash_path = '/sdcard/crash-dump.log'
get_performance_path = os.path.join(project_path, 'monkey/getper.sh')
report = os.path.join(project_path, 'report')
performance_out = os.path.join(project_path, 'report/tmp/')
performance_folder = os.path.join(project_path, 'report/tmp/')
max_path = os.path.join(project_path, 'monkey/config/max.config')
device_crash_image = '/sdcard/Crash_*'
image_key = '*Crash_*'
local_images_path = os.path.join(project_path, 'monkey/images')
images_zip = os.path.join(project_path, 'monkey/images.zip')
run_activity_path = os.path.join(project_path, 'report/tmp/runactivity.log')
run_activity_path_back = os.path.join(project_path, 'report/tmp/runactivity_back.log')
cpu_path = os.path.join(project_path, 'report/tmp/cpu.log')
mem_path = os.path.join(project_path, 'report/tmp/mem.log')
page_path = os.path.join(project_path, 'report/tmp/page.log')
network_path = os.path.join(project_path, 'report/tmp/network.log')
fps_path = os.path.join(project_path, 'report/tmp/fps.log')
all_activity_path = os.path.join(project_path, 'report/tmp/allactivity.log')
run_model = 'uiautomatordfs'
throttle = 200
sleep_time = 3
gunicorn_port = '3031'
gunicorn_address = '127.0.0.1:' + gunicorn_port
host = '127.0.0.1'
port = '3031'
api = ('http://{}:{}/getreport').format(host, gunicorn_port)