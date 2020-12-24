# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/breno/Envs/djangoplus/lib/python3.7/site-packages/djangoplus/admin/management/commands/make_apk.py
# Compiled at: 2019-03-28 13:52:11
# Size of source mod 2**32: 4920 bytes
import os, shutil, tempfile, urllib.request, zipfile
from PIL import Image
from django.conf import settings
from resizeimage import resizeimage
from djangoplus.tools.browser import Browser
from django.core.management.base import BaseCommand
ANDROID_HOME = '/Users/breno/Library/Android'
KEY_STORE_FILE_PATH = '/tmp/djangoplus.keystore'
TEMPLATE_FILE_PATH = '/tmp/template.apk'
LANDSCAPE_IMAGE_PATH = '/tmp/landscape.png'
PORTRAIT_IMAGE_PATH = '/tmp/portrait.png'

class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('url')

    def handle(self, *args, **options):
        url = options['url']
        if not os.path.exists(KEY_STORE_FILE_PATH):
            urllib.request.urlretrieve('http://djangoplus.net/djangoplus.keystore', KEY_STORE_FILE_PATH)
        if not os.path.exists(TEMPLATE_FILE_PATH):
            urllib.request.urlretrieve('http://djangoplus.net/template.apk', TEMPLATE_FILE_PATH)
        unsigned_file_path = os.path.join(settings.BASE_DIR, 'unsigned.apk')
        signed_file_path = os.path.join(settings.BASE_DIR, 'signed.apk')
        shutil.copy(TEMPLATE_FILE_PATH, unsigned_file_path)
        new_files = []
        old_files = []
        if not os.path.exists(LANDSCAPE_IMAGE_PATH):
            browser = Browser(url, headless=True)
            browser.set_window_size(1920, 1280)
            browser.open('/')
            browser.wait(3)
            browser.save_screenshot(LANDSCAPE_IMAGE_PATH)
            browser.set_window_size(1280, 1920)
            browser.open('/')
            browser.wait(3)
            browser.save_screenshot(PORTRAIT_IMAGE_PATH)
        replacements = dict(ID=(url.replace('http://', '')), NAME='Educ', DESCRIPTION=url, EMAIL='brenokcc@yahoo.com.br')
        for file_name in ('assets/www/home-home-module.js', 'assets/www/home-home-module.js.map'):
            with zipfile.ZipFile(TEMPLATE_FILE_PATH) as (myzip):
                with myzip.open(file_name) as (myfile):
                    s = myfile.read().decode()
                s = s.replace('http://google.com', url)
                temp_file_name = '/tmp/{}'.format(file_name.split('/')[(-1)])
                open(temp_file_name, 'w').write(s)
                new_files.append((file_name, temp_file_name))
                old_files.append(file_name)

        with zipfile.ZipFile(TEMPLATE_FILE_PATH, 'r') as (zipread):
            for item in zipread.infolist():
                for file_name in ('icon.png', 'screen.png'):
                    if item.filename.endswith(file_name):
                        with zipread.open(item.filename) as (myfile):
                            with Image.open(myfile) as (my_image_file):
                                width, height = my_image_file.size
                                base_image_name = width > height and LANDSCAPE_IMAGE_PATH or PORTRAIT_IMAGE_PATH
                                with Image.open(base_image_name) as (base_image):
                                    temp_file_name = '/tmp/{}x{}.png'.format(width, height)
                                    resized_image = resizeimage.resize_cover(base_image, my_image_file.size)
                                    resized_image.save(temp_file_name)
                                    new_files.append((item.filename, temp_file_name))
                                    old_files.append(item.filename)

        tempdir = tempfile.mkdtemp()
        try:
            tempname = os.path.join(tempdir, 'new.zip')
            with zipfile.ZipFile(unsigned_file_path, 'r') as (zipread):
                with zipfile.ZipFile(tempname, 'w') as (zipwrite):
                    for item in zipread.infolist():
                        if item.filename not in old_files:
                            data = zipread.read(item.filename)
                            zipwrite.writestr(item, data)

            shutil.move(tempname, unsigned_file_path)
        finally:
            shutil.rmtree(tempdir)

        with zipfile.ZipFile(unsigned_file_path, 'a') as (myzip2):
            for file_name, temp_file_name in new_files:
                myzip2.write(temp_file_name, file_name)
                os.unlink(temp_file_name)

        jarsigner = 'jarsigner -keystore /tmp/djangoplus.keystore -storepass 1793ifrn. {} djangoplus > /dev/null 2>&1'
        zipalign = '{}/sdk/build-tools/28.0.3/zipalign -v 4 {} {} > /dev/null 2>&1'
        os.system(jarsigner.format(unsigned_file_path))
        os.system(zipalign.format(ANDROID_HOME, unsigned_file_path, signed_file_path))
        os.unlink(unsigned_file_path)
        print('File {} successfully generated'.format(signed_file_path))