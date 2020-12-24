# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\xh\Documents\github-xh\crawl_image\crawl_image\model\model.py
# Compiled at: 2019-06-12 03:32:16
# Size of source mod 2**32: 650 bytes
from crawl_image.config.setting import *

class ImgCrawlModel:

    @staticmethod
    def build(url, img_save_path=IMG_SAVE_PATH):
        if str(url).strip() == '':
            raise SystemExit('url 不能为空')
        img_crawl_model = ImgCrawlModel()
        img_crawl_model.url = url
        img_crawl_model.img_save_path = img_save_path
        return img_crawl_model

    url = URL
    img_save_path = IMG_SAVE_PATH
    do_multi = DO_MULTI
    default_img_suffix = DEFAULT_IMG_SUFFIX
    img_include_suffix = IMG_INCLUDE_SUFFIX
    img_exclude_suffix = IMG_EXCLUDE_SUFFIX