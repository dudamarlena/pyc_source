# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/src/__init__.py
# Compiled at: 2017-01-03 17:39:52
# Size of source mod 2**32: 1357 bytes
from time import sleep
import pystray, psutil
from PIL import Image, ImageDraw
WIDTH, HEIGHT = (16, 16)
ICON_IMAGE_SIZE = (WIDTH, HEIGHT)
COLOR1, COLOR2 = ('#FF1493', '#ADFF2F')
ICON_IMAGE_COLORS = (COLOR1, COLOR2)

def is_emacs_up():
    return [True for p in psutil.process_iter() if p.name() == 'emacs'] != []


def create_raw_icon():
    return pystray.Icon('test name')


def generate_image(size, colors, is_emacs_up=is_emacs_up):
    width, height = size
    color1, color2 = colors
    image = Image.new('RGB', (width, height), color1)
    dc = ImageDraw.Draw(image)
    if is_emacs_up():
        dc.rectangle((0, 0, width, height), fill=color2)
    else:
        dc.rectangle((0, 0, width, height), fill=color1)
    return image


def set_image(icon, image):
    icon.icon = image


def update_icon(icon, icon_image_size=ICON_IMAGE_SIZE, icon_image_colors=ICON_IMAGE_COLORS):
    while True:
        image = generate_image(icon_image_size, icon_image_colors)
        set_image(icon, image)
        icon.visible = True
        sleep(5)


def create_icon(icon_image_size, icon_image_colors):
    icon = create_raw_icon()
    return icon


def run(icon, function=update_icon):
    icon.run(function)


def main(size=ICON_IMAGE_SIZE, colors=ICON_IMAGE_COLORS):
    icon = create_icon(size, colors)
    run(icon)


if __name__ == '__main__':
    main()