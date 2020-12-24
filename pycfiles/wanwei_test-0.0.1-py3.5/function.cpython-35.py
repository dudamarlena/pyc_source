# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\test1\function.py
# Compiled at: 2019-01-14 07:53:28
# Size of source mod 2**32: 452 bytes
from selenium import webdriver
import os

def insert_img(driver, file_name):
    base_dir = os.path.dirname(os.path.dirname(__file__))
    base_dir = str(base_dir)
    base_dir = base_dir.replace('\\', '/')
    file_path = base_dir + file_name
    driver.get_screenshot_as_file(file_path)


if __name__ == '__main__':
    driver = webdriver.Chrome()
    driver.get('https://www.baidu.com')
    insert_img(driver, 'baidu.jpg')
    driver.quit()