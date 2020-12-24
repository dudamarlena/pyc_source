# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\xh\Documents\PyCharmProjects\page_screenshot\page_screenshot\index.py
# Compiled at: 2019-06-25 23:07:34
# Size of source mod 2**32: 9052 bytes
"""
@project: page screenshot
@author: xiaohong
@time: 2019-06-07
@feature: a complete capture from a web page
"""
import time, os
from PIL import Image
from selenium import webdriver
from page_screenshot.model.model import *

def make_unique_folder(path):
    """
    创建时间戳文件夹

    :param path: 文件路径
    :return: 文件夹路径
    """
    t = ''
    folder = path + t
    if not os.path.isdir(folder):
        os.makedirs(folder)
    return folder


class PageScreenshot:

    def __init__(self):
        """
        init
        """
        self.model = None
        self.driver = self.take_driver()

    def print_w_h(self):
        """
        print

        :return: void
        """
        width = self.driver.execute_script(JS_MAX_WIDTH)
        height = self.driver.execute_script(JS_MAX_HEIGHT)
        driver_width = self.driver.get_window_size()['width']
        driver_height = self.driver.get_window_size()['height']
        window_height = self.driver.execute_script(JS_WINDOW_HEIGHT)
        logging.info('外宽(set_window_size) %s, %s; 外宽截图 %s, %s; 内宽(JS_MAX_WIDTH/HEIGHT) %s %s; 内宽截图 %s, %s' % (
         driver_width, driver_height,
         driver_width * self.model.scale_window, driver_height * self.model.scale_window,
         width, height,
         width * self.model.scale_window, window_height))

    def calc_right_step_scroll(self):
        """
        计算滚动大小

        :return: 滚动次数，滚动高度
        """
        times_shot = 1
        inner_height = height = float(self.driver.execute_script(JS_MAX_HEIGHT))
        while True:
            if inner_height <= self.model.base_height:
                break
            times_shot = times_shot + 1
            inner_height = height / times_shot

        driver_height = self.driver.get_window_size()['height']
        window_height = self.driver.execute_script(JS_WINDOW_HEIGHT)
        if 0 == window_height:
            window_height = 1
        self.driver.set_window_size(self.driver.get_window_size()['width'], inner_height * driver_height / window_height)
        logging.info('times_shot : %s' % times_shot)
        self.print_w_h()
        return (times_shot, self.driver.execute_script(JS_WINDOW_HEIGHT))

    def scroll_to_capture(self):
        """
        滚动并截图

        :return: 截图次数
        """
        self.model.img_save_path = make_unique_folder(self.model.img_save_path)
        times_shot, step_scroll = self.calc_right_step_scroll()
        for i in range(times_shot):
            self.driver.execute_script(JS_SCROLL % (i * step_scroll, self.model.time_ms_scroll_fast))
            time.sleep(self.model.time_ms_scroll_fast * 0.002)
            self.driver.execute_script(JS_SCROLL % (0, self.model.time_ms_scroll_fast))

        times_shot, step_scroll = self.calc_right_step_scroll()
        for i in range(times_shot):
            self.driver.execute_script(JS_SCROLL % (i * step_scroll, self.model.time_ms_scroll_slow))
            time.sleep(self.model.time_ms_scroll_slow * 0.002)
            self.driver.save_screenshot(self.model.img_save_path + '/' + str(i) + DEFAULT_IMG_SUFFIX)

        time.sleep(3)
        return times_shot

    def take_driver(self):
        """
        生成driver

        :return: WebDriver
        """
        options = webdriver.ChromeOptions()
        options.add_argument('--dns-prefetch-disable')
        options.add_argument('--no-referrers')
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-audio')
        options.add_argument('--no-sandbox')
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--allow-insecure-localhost')
        options.add_argument('disable-infobars')
        driver = webdriver.Chrome(options=options, executable_path=CHROME_DRIVER_PATH)
        return driver

    def take_url(self):
        self.driver.get(url=(self.model.url))
        time.sleep(0.5)
        self.driver.set_window_position(self.model.init_window_position_x, self.model.init_window_position_y)
        self.driver.execute_script('document.body.parentNode.style.overflowX = "hidden";')
        self.driver.execute_script('document.body.parentNode.style.overflowY = "hidden";')
        self.driver.set_window_size(self.model.outer_width / self.model.scale_window, self.model.init_height)

    def check(self):
        template_file_name = self.model.default_img_save_path + '/%s' + DEFAULT_IMG_SUFFIX
        return os.path.exists(template_file_name % self.model.file_name)

    def capture(self, page_screenshot_model: PageScreenshotModel):
        """
        生成网页截图文件

        :param page_screenshot_model: PageScreenshotModel
        :return: void
        """
        self.model = page_screenshot_model
        self.take_url()
        try:
            self.model.file_name = self.driver.execute_script(self.model.js_file_name)
        except Exception:
            try:
                self.model.file_name = self.driver.execute_script(JS_MD5_URL)
            except Exception:
                self.model.file_name = str(int(time.time()))

        self.model.file_name = self.filter_file_name(self.model.file_name)
        if self.check():
            logging.info('图片已存在 %s' % self.model.file_name)
            return
        logging.info('开始捕获截图的url %s' % page_screenshot_model.url)
        self.model.count_image = self.scroll_to_capture()
        logging.info('merge image ...')
        self.merge()
        logging.info('remove_temp_file ...')
        self.remove_temp_file()

    def close(self):
        """
        close

        :return: void
        """
        self.driver.quit()

    def remove_temp_file(self):
        """
        删除每次滚动截图文件

        :return: void
        """
        template_file_name = self.model.img_save_path + '/%s' + DEFAULT_IMG_SUFFIX
        for i in range(self.model.count_image):
            try:
                os.remove(template_file_name % i)
            except Exception:
                print('no image file, go on')

    @staticmethod
    def filter_file_name(file_name: str):
        """
        过滤非法文件名称的字符
        :param file_name: 文件名
        :return: 正确的文件名
        """
        illegal_char = [
         '\\', '/', ':', '*', '?', '"', '<', '>', '|']
        for i in illegal_char:
            file_name = file_name.replace(i, '')

        return file_name

    def merge(self):
        """
        拼接滚动截图文件

        :return: void
        """
        template_file_name = self.model.img_save_path + '/%s' + DEFAULT_IMG_SUFFIX
        f = Image.open(template_file_name % 0)
        w, h = f.size
        merge_image = Image.new('RGBA', (w, h * self.model.count_image))
        for i in range(self.model.count_image):
            merge_image.paste(Image.open(template_file_name % i), (0, i * h))

        try:
            merge_image.save(template_file_name % self.model.file_name)
        except Exception:
            merge_image.save(template_file_name % str(int(time.time())))
            logging.info('文件名称不合符 %s' % self.model.url)

        time.sleep(1)