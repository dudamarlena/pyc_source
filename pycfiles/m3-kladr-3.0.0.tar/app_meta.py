# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/pirogov/.virtualenvs/paid/local/lib/python2.7/site-packages/kladr/app_meta.py
# Compiled at: 2014-05-26 05:22:26
from django.conf import urls
from actions import kladr_controller, KLADRPack
from m3 import authenticated_user_required

def register_actions():
    kladr_controller.packs.append(KLADRPack())


def register_urlpatterns():
    u"""
    Регистрация конфигурации урлов для приложения kladr
    """
    return urls.patterns('', ('^m3-kladr', 'kladr.app_meta.kladr_view'))


@authenticated_user_required
def kladr_view(request):
    return kladr_controller.process_request(request)