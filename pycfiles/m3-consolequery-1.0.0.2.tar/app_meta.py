# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/khalikov/projects/processing/src/processing/../env/m3_consolequery/app_meta.py
# Compiled at: 2013-09-30 07:59:05
"""
Created on 14.12.2010

@author: Камилла
"""
from django.conf import urls
from m3.ui.actions import ActionController
import actions
from django.conf import settings
from m3.ui.app_ui import DesktopLaunchGroup, DesktopLoader, DesktopLauncher
from m3_users.metaroles import get_metarole
from m3.helpers.users import authenticated_user_required
m3_consolequery_controller = ActionController('/m3-consolequery')

def register_urlpatterns():
    u"""
    Регистрация конфигурации урлов для приложения
    """
    return urls.defaults.patterns('', ('^m3-consolequery/', 'm3_consolequery.app_meta.controller'))


@authenticated_user_required
def controller(request):
    return m3_consolequery_controller.process_request(request)


def register_desktop_menu():
    u"""
    Регистрирует отдельные элементы в меню "Пуск"
    """
    ADMIN_METAROLE = get_metarole('admin')
    try:
        if settings.DATABASES['readonly']:
            admin_root = DesktopLaunchGroup(name='Администрирование', icon='menu-dicts-16')
            admin_root.subitems.append(DesktopLauncher(name='Консоль запросов', url=actions.QyeryConsoleWinAction.absolute_url(), icon='icon-application-xp-terminal'))
            DesktopLoader.add(ADMIN_METAROLE, DesktopLoader.START_MENU, admin_root)
            DesktopLoader.add(ADMIN_METAROLE, DesktopLoader.TOPTOOLBAR, admin_root)
    except:
        None

    return


def register_actions():
    u"""
    Метод регистрации Action'ов для приложения в котором описан
    """
    m3_consolequery_controller.packs.extend([
     actions.QueryConsoleActionsPack,
     actions.CustomQueries_DictPack])