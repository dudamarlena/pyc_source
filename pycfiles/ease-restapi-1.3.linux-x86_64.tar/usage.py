# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/site-packages/ease_restapi/simplify/usage.py
# Compiled at: 2015-01-25 06:16:18
import six
from ease_restapi import join_easemob_local, passwd_easemob_user, change_easemob_nickname

def login(request):
    u"""登录
    """
    profile = None
    username = None
    password = None
    join_easemob_local(profile, username, password, True)
    return


def user_joining(request):
    u"""用户注册
    """
    profile = None
    username = None
    password = None
    join_easemob_local(profile, username, password, True)
    return


def user_passwd_reset(request):
    u"""重置密码
    """
    user = None
    profile = None
    username = None
    password = None
    is_flag = True
    if profile.ring_join:
        is_flag = passwd_easemob_user(username, password)
    try:
        if is_flag:
            user.save()
        else:
            six.print_('环信密码更新失败.')
    except Exception as e:
        is_flag = False
        six.print_((e, '本地数据密码保存失败.'))

    if not is_flag:
        return {'error': 1010}
    else:
        return


def user_profile(request):
    u"""修改会员信息
    """
    profile = None
    username = None
    nickname = None
    password = None
    if profile.ring_join:
        change_easemob_nickname(username, nickname)
    passwd_easemob_user(username, password)
    return


def user_nickname(request):
    u"""从环信端用户名获取本地用户昵称.

        环信好友列表, 会话列表, username值传入该接口, 以本地昵称形式显示客户端.

        本地业务如有调整, 启用并修改下面注释代码, 增修字段.
    """
    if request.method != 'POST':
        return {'error': 9999}
    else:
        user_name_list = None if 'usernames' not in request.POST else request.POST['usernames']
        if not user_name_list:
            return {'error': 8888}
        void_list = []
        is_error = False
        user_nick_list = []
        for user_name in user_name_list.split(','):
            try:
                char_ind = user_name.rindex('_')
                user_name = ('@').join((user_name[:char_ind], user_name[char_ind + 1:]))
                user_nick_list.append(user_name)
            except (ValueError, Exception):
                void_list.append({'name': user_name})
                if is_error:
                    return {'error': 8888}

        user_info_list = None
        user_info_list = list(user_info_list)
        user_info_list.extend(void_list)
        return {'error': 0, 'array': user_info_list}