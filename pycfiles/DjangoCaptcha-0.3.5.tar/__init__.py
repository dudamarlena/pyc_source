# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/tianyu/Dev/DjangoCaptcha/demo/main/DjangoCaptcha/__init__.py
# Compiled at: 2017-04-13 23:50:59
"""
Copyright 2013 TY<tianyu0915@gmail.com>

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

"""
import os, random
from math import ceil
from six import BytesIO
from django.http import HttpResponse
from PIL import Image, ImageDraw, ImageFont
__version__ = '0.3.3'
current_path = os.path.normpath(os.path.dirname(__file__))

class Captcha(object):

    def __init__(self, request):
        """ something init
        """
        self.django_request = request
        self.session_key = '_django_captcha_key'
        self.words = []
        self.img_width = 150
        self.img_height = 30
        self.type = 'number'
        self.mode = 'number'

    def _get_font_size(self):
        u"""  将图片高度的80%作为字体大小
        """
        s1 = int(self.img_height * 0.8)
        s2 = int(self.img_width / len(self.code))
        return int(min((s1, s2)) + max((s1, s2)) * 0.05)

    def _get_words(self):
        """ The words list
        """
        if self.words:
            return set(self.words)
        file_path = os.path.join(current_path, 'words.list')
        f = open(file_path, 'r')
        return set([ line.replace('\n', '') for line in f.readlines() ])

    def _set_answer(self, answer):
        u"""  设置答案
        
        """
        self.django_request.session[self.session_key] = str(answer)

    def _yield_code(self):
        u"""  生成验证码文字,以及答案
        
        """

        def word():
            code = random.sample(self._get_words(), 1)[0]
            self._set_answer(code)
            return code

        def number():
            m, n = (1, 50)
            x = random.randrange(m, n)
            y = random.randrange(m, n)
            r = random.randrange(0, 2)
            if r == 0:
                code = '%s - %s = ?' % (x, y)
                z = x - y
            else:
                code = '%s + %s = ?' % (x, y)
                z = x + y
            self._set_answer(z)
            return code

        fun = eval(self.mode.lower())
        return fun()

    def display(self):
        """  The captch image output using Django response object
        """
        self.font_color = [
         'black', 'darkblue', 'darkred']
        self.background = (
         random.randrange(230, 255), random.randrange(230, 255), random.randrange(230, 255))
        self.font_path = os.path.join(current_path, 'timesbi.ttf')
        self.django_request.session[self.session_key] = ''
        im = Image.new('RGB', (self.img_width, self.img_height), self.background)
        self.code = self._yield_code()
        self.font_size = self._get_font_size()
        draw = ImageDraw.Draw(im)
        if self.mode == 'word':
            c = int(8 / len(self.code) * 3) or 3
        else:
            if self.mode == 'number':
                c = 4
            for i in range(random.randrange(c - 2, c)):
                line_color = (
                 random.randrange(0, 255), random.randrange(0, 255), random.randrange(0, 255))
                xy = (
                 random.randrange(0, int(self.img_width * 0.2)),
                 random.randrange(0, self.img_height),
                 random.randrange(int(3 * self.img_width / 4), self.img_width),
                 random.randrange(0, self.img_height))
                draw.line(xy, fill=line_color, width=int(self.font_size * 0.1))

            j = int(self.font_size * 0.3)
            k = int(self.font_size * 0.5)
            x = random.randrange(j, k)
            for i in self.code:
                m = int(len(self.code))
                y = random.randrange(1, 3)
                if i in ('+', '=', '?'):
                    m = ceil(self.font_size * 0.8)
                else:
                    m = random.randrange(0, int(45 / self.font_size) + int(self.font_size / 5))
                self.font = ImageFont.truetype(self.font_path.replace('\\', '/'), self.font_size + int(ceil(m)))
                draw.text((x, y), i, font=self.font, fill=random.choice(self.font_color))
                x += self.font_size * 0.9

        del x
        del draw
        buf = BytesIO()
        im.save(buf, 'gif')
        buf.closed
        return HttpResponse(buf.getvalue(), 'image/gif')

    def validate(self, code):
        """ 
        validate user's input
        """
        if not code:
            return False
        code = code.strip()
        _code = self.django_request.session.get(self.session_key) or ''
        self.django_request.session[self.session_key] = ''
        return _code.lower() == str(code).lower()

    def check(self, code):
        """
        This function will no longer be supported after  version  0.4
        """
        return self.validate(code)


class Code(Captcha):
    """
    compatibility for less than v2.0.6 
    """
    pass


if __name__ == '__main__':
    import mock
    request = mock.Mock()
    c = Captcha(request)