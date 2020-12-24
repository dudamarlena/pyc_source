# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/noval/plugins/update.py
# Compiled at: 2019-10-17 01:45:10
# Size of source mod 2**32: 8255 bytes
from noval import GetApp, _
import os, noval.util.utils as utils, noval.util.apputils as apputils, time
from dummy.userdb import UserDataDb
from tkinter import messagebox
import noval.util.urlutils as urlutils, sys, noval.iface as iface, noval.plugin as plugin, noval.constants as constants, noval.consts as consts, noval.util.downutils as downutils, noval.python.parser.utils as parserutils, threading, shutil

def check_plugins(ignore_error=False):
    """
        检查插件更新信息
    """

    def pop_error(data):
        if data is None:
            if not ignore_error:
                messagebox.showerror(GetApp().GetAppName(), _('could not connect to server'))

    def after_update_download(egg_path):
        """
            插件更新下载后回调函数
        """
        plugin_path = os.path.dirname(dist.location)
        try:
            os.remove(dist.location)
            utils.get_logger().info('remove plugin %s old version %s file %s success', plugin_name, plugin_version, dist.location)
            dest_egg_path = os.path.join(plugin_path, plugin_data['path'])
            if os.path.exists(dest_egg_path):
                logger.error('plugin %s version %s dist egg path is exist when update it', plugin_name, plugin_data['version'], dest_egg_path)
                os.remove(dest_egg_path)
        except:
            messagebox.showerror(GetApp().GetAppName(), _('Remove faile:%s fail') % dist.location)
            return

        shutil.move(egg_path, plugin_path)
        GetApp().GetPluginManager().LoadPluginByName(plugin_name)
        messagebox.showinfo(GetApp().GetAppName(), _("Update plugin '%s' success") % plugin_name)

    user_id = UserDataDb().GetUserId()
    check_plugin_update = utils.profile_get_int('CheckPluginUpdate', True)
    for plugin_class, dist in GetApp().GetPluginManager().GetPluginDistros().items():
        plugin_version = dist.version
        plugin_name = dist.key
        api_addr = '%s/member/get_plugin' % UserDataDb.HOST_SERVER_ADDR
        plugin_data = utils.RequestData(api_addr, method='get', arg={'name': plugin_name})
        if not plugin_data:
            pop_error(plugin_data)
            return
        if 'id' not in plugin_data:
            logger.warn('could not find plugin %s on server', plugin_name)
            continue
            plugin_name = plugin_data['name']
            plugin_id = plugin_data['id']
            free = int(plugin_data['free'])
            if GetApp().GetDebug():
                log = utils.get_logger().debug
            else:
                log = utils.get_logger().info
            log('plugin %s version is %s latest verison is %s', plugin_name, plugin_version, plugin_data['version'])
            if not free:
                api_addr = '%s/member/get_payment' % UserDataDb.HOST_SERVER_ADDR
                data = urlutils.RequestData(api_addr, arg={'member_id': user_id, 'plugin_id': plugin_id})
                if not data:
                    pop_error(data)
                    return
                payed = int(data['payed'])
                if not payed:
                    check_plugin_update = True
                price = plugin_data.get('price', None)
                if not payed and price:
                    pass
                if check_plugin_update and parserutils.CompareCommonVersion(plugin_data['version'], plugin_version):
                    ret = messagebox.askyesno(_('Plugin Update Available'), _("Plugin '%s' latest version '%s' is available,do you want to download and update it?") % (plugin_name, plugin_data['version']))
                    if ret:
                        new_version = plugin_data['version']
                        download_url = '%s/member/download_plugin' % UserDataDb.HOST_SERVER_ADDR
                        payload = dict(app_version=apputils.get_app_version(), lang=GetApp().locale.GetLanguageCanonicalName(), os_name=sys.platform, plugin_id=plugin_id)
                        downutils.download_file(download_url, call_back=after_update_download, **payload)
                    break


def CheckAppUpdate(ignore_error=False):
    api_addr = '%s/member/get_update' % UserDataDb.HOST_SERVER_ADDR
    lang = GetApp().locale.GetLanguageCanonicalName()
    app_version = apputils.get_app_version()
    data = urlutils.RequestData(api_addr, arg={'app_version': app_version, 'lang': lang})
    if data is None:
        if not ignore_error:
            messagebox.showerror(GetApp().GetAppName(), _('could not connect to server'))
        return
    if data['code'] == 0:
        if not ignore_error:
            messagebox.showinfo(GetApp().GetAppName(), data['message'])
    else:
        if data['code'] == 1:
            ret = messagebox.askyesno(_('Update Available'), data['message'])
            if ret:
                new_version = data['new_version']
                download_url = '%s/member/download_app' % UserDataDb.HOST_SERVER_ADDR
                payload = dict(new_version=new_version, lang=lang, os_name=sys.platform)
                downutils.download_file(download_url, call_back=Install, **payload)
        elif not ignore_error:
            messagebox.showerror(GetApp().GetAppName(), data['message'])


def Install(app_path):
    if utils.is_windows():
        os.startfile(app_path)
    else:
        path = os.path.dirname(sys.executable)
        pip_path = os.path.join(path, 'pip')
        cmd = '%s  -c "from distutils.sysconfig import get_python_lib; print get_python_lib()"' % (sys.executable,)
        python_lib_path = utils.GetCommandOutput(cmd).strip()
        user = getpass.getuser()
        should_root = not fileutils.is_writable(python_lib_path, user)
        if should_root:
            cmd = 'pkexec ' + '%s install %s' % (pip_path, app_path)
        else:
            cmd = '%s install %s' % (pip_path, app_path)
        subprocess.call(cmd, shell=True)
        app_startup_path = whichpath.GuessPath('NovalIDE')
        subprocess.Popen('/bin/sleep 2;%s' % app_startup_path, shell=True)
    GetApp().Quit()


def CheckForceupdate():
    """
        某些版本太老了,需要强制更新
    """
    app_version = apputils.get_app_version()
    check_url = '%s/member/check_force_update' % UserDataDb.HOST_SERVER_ADDR
    try:
        req = urlutils.RequestData(check_url, arg={'app_version': app_version})
        return req.get('force_update', False)
    except:
        return False


class UpdateLoader(plugin.Plugin):
    plugin.Implements(iface.CommonPluginI)

    def Load(self):
        force_update = CheckForceupdate()
        GetApp().InsertCommand(constants.ID_GOTO_OFFICIAL_WEB, constants.ID_CHECK_UPDATE, _('&Help'), _('&Check for Updates'), handler=lambda : self.CheckUpdate(ignore_error=False, check_plugin_update=False), pos='before')
        if utils.profile_get_int(consts.CHECK_UPDATE_ATSTARTUP_KEY, True) or force_update:
            self.CheckUpdateAfter()

    @utils.call_after
    def CheckUpdateAfter(self, ignore_error=True, check_plugin_update=True):
        t = threading.Thread(target=self.CheckUpdate, args=(ignore_error, check_plugin_update))
        t.start()

    def CheckUpdate(self, ignore_error=True, check_plugin_update=True):
        CheckAppUpdate(ignore_error)
        if check_plugin_update:
            check_plugins(ignore_error)