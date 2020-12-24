# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/deepnlpf/modules/notifications/toast.py
# Compiled at: 2019-07-12 07:52:09
# Size of source mod 2**32: 1495 bytes
"""
    Description: Notificações no desktop.
    Date: 01/11/2018
"""
import pathlib, subprocess as sp
import deepnlpf.config.notification as setting

class Toast(object):
    __doc__ = '\n        List emoticons system linux.\n\n        face-angel.png        face-sad.png         stock_smiley-13.png\n        face-angry.png        face-sick.png        stock_smiley-15.png\n        face-cool.png         face-smile-big.png   stock_smiley-18.png\n        face-crying.png       face-smile.png       stock_smiley-1.png\n        face-devilish.png     face-smirk.png       stock_smiley-22.png\n        face-embarrassed.png  face-surprise.png    stock_smiley-2.png\n        face-glasses.png      face-tired.png       stock_smiley-3.png\n        face-kiss.png         face-uncertain.png   stock_smiley-4.png\n        face-laugh.png        face-wink.png        stock_smiley-5.png\n        face-monkey.png       face-worried.png     stock_smiley-6.png\n        face-plain.png        stock_smiley-10.png  stock_smiley-7.png\n        face-raspberry.png    stock_smiley-11.png  stock_smiley-8.png\n    '

    def send_notification(self, icon, title, mensage):
        """
            Send notification desktop.

            @param 
                icon
                title
                mensage
        """
        if setting.TELEGRAM['SEND_MSG']:
            sp.call(['notify-send', '-i', str(pathlib.Path.cwd()) + '/deepnlpf/modules/notifications/img/' + icon + '.png', title, mensage])