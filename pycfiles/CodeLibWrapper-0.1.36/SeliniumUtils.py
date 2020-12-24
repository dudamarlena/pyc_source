# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Python27\Lib\site-packages\CodeLibWrapper\Src\UIAction\SeliniumUtils.py
# Compiled at: 2016-11-28 20:22:14
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

def open_firefox_with_gecko_driver(firefox_exe_path='C:\\Program Files (x86)\\Mozilla Firefox\\firefox.exe'):
    binary = FirefoxBinary(firefox_exe_path)
    return webdriver.Firefox(firefox_binary=binary)


def open_chrome():
    return webdriver.Chrome()


def open_ie():
    return webdriver.Ie()


def main():
    print 'Do something.'


if __name__ == '__main__':
    main()