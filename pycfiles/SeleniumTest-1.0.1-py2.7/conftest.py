# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/sr/conftest.py
# Compiled at: 2019-03-23 05:47:02
"""
@Author  : xinxi
@Time    : 2018/12/5 18:34
@describe: 创建driver
"""
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import os, sys, subprocess, pytest, time, allure, base64
from allure.constants import AttachmentType
from config import screen_folder
from wdriver import WDriver
sys.path.append('..')
from logger import init_logger
logger = init_logger()

@pytest.fixture()
def driver_setup(request):
    logger.info('自动化测试开始!')
    request.instance.driver = WDriver().init_driver()
    logger.info('driver初始化')

    def driver_teardown():
        logger.info('自动化测试结束!')
        request.instance.driver.quit()

    request.addfinalizer(driver_teardown)


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    u"""
    hook pytest失败
    :param item:
    :param call:
    :return:
    """
    outcome = yield
    rep = outcome.get_result()
    if rep.when == 'call' and rep.failed:
        mode = 'a' if os.path.exists('failures') else 'w'
        with open('failures', mode) as (f):
            if 'tmpdir' in item.fixturenames:
                extra = ' (%s)' % item.funcargs['tmpdir']
            else:
                extra = ''
            f.write(rep.nodeid + extra + '\n')
        logger.info('测试失败了')
        with allure.step('添加失败截图...'):
            allure.attach(rep.nodeid, WDriver().get_driver().get_screenshot_as_png(), type=AttachmentType.PNG)