# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/max/logintest/location.py
# Compiled at: 2019-04-27 11:19:42
import sys, platform, time
reload(sys)
sys.setdefaultencoding('utf8')
import time, os, unittest, subprocess
from functools import wraps
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from ..tools.loggers import JFMlogging
logger = JFMlogging().getloger()

class Location:

    def __init__(self, driver):
        self.driver = driver

    def location_element(self, location):
        u"""
        解析定位方法
        :param driver:
        :param location:
        :return:
        """
        try:
            method = str(location).split(',')[0]
            value = str(location).split(',')[1]
            if method == 'By.NAME':
                return self.driver.find_element(By.NAME, value)
            if method == 'By.ID':
                return self.driver.find_element(By.ID, value)
            if method == 'By.CLASS_NAME':
                return self.driver.find_element(By.CLASS_NAME, value)
            if method == 'By.XPATH':
                return self.driver.find_element(By.XPATH, value)
            if method == 'By.CSS_SELECTOR':
                return self.driver.find_element(By.CSS_SELECTOR, value)
            if method == 'By.LINK_TEXT':
                return self.driver.find_element(By.LINK_TEXT, value)
            if method == 'By.PARTIAL_LINK_TEXT':
                return self.driver.find_element(By.PARTIAL_LINK_TEXT, value)
            if method == 'By.TAG_NAME':
                return self.driver.find_element(By.TAG_NAME, value)
        except Exception as e:
            fail_detail = ('location_element Exception:{}').format(e)
            logger.error(fail_detail)
            raise Exception

    def create_location(self, location):
        try:
            method = str(location).split(',')[0]
            value = str(location).split(',')[1]
            if method == 'By.NAME':
                return (By.NAME, value)
            if method == 'By.ID':
                return (By.ID, value)
            if method == 'By.CLASS_NAME':
                return (By.CLASS_NAME, value)
            if method == 'By.XPATH':
                return (By.XPATH, value)
            if method == 'By.CSS_SELECTOR':
                return (By.CSS_SELECTOR, value)
            if method == 'By.LINK_TEXT':
                return (By.LINK_TEXT, value)
            if method == 'By.PARTIAL_LINK_TEXT':
                return (By.PARTIAL_LINK_TEXT, value)
            if method == 'By.TAG_NAME':
                return (By.TAG_NAME, value)
        except Exception as e:
            fail_detail = ('create_location Exception:{}').format(location)
            logger.error(fail_detail)
            raise Exception

    def display_wait(self, time, loc):
        u"""
        显示等待
        :param time:
        :param loc:
        :return:
        """
        try:
            element = WebDriverWait(self.driver, time).until(EC.visibility_of_element_located(loc))
            return element
        except Exception as e:
            fail_detail = ('display_wait Exception:{}').format(loc)
            logger.error(fail_detail)

    def when_element_click(self, time, loc):
        u"""
        当元素存在则点击
        :return:
        """
        _loc = self.create_location(loc)
        _el = self.display_wait(time, *_loc)
        if _el != None:
            _el.click()
            logger.info(('存在元素并点击:{}').format(_loc))
        else:
            logger.info(('不存在元素:{}').format(_loc))
        return

    def wait_sleep(self, wait_time):
        time.sleep(int(wait_time))