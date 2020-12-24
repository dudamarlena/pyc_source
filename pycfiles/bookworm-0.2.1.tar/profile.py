# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/booki/channels/profile.py
# Compiled at: 2012-02-14 23:34:00
from django.db import transaction
from django.conf import settings
try:
    STATUS_URL = settings.STATUS_URL
except AttributeError:
    STATUS_URL = 'http://status.flossmanuals.net/'

def remote_get_status_messages(request, message, profileid):
    """
    Fetches RSS feed from status.net and returns its content. 

    Output:
     - list

    @todo: Not used anymore. Probably should remove it.

    @type request: C{django.http.HttpRequest}
    @param request: Client Request object
    @type message: C{dict}
    @param message: Message object
    @type profileid: C{string}
    @param profile: Unique Profile id
    @rtype: C{dict}
    @return: Returns feed content
    """
    return {}


def remote_group_create(request, message, profileid):
    """
    Creates new Booki Group.

    Input:
     - groupName
     - groupDescription

    Output:
     - list

    @type request: C{django.http.HttpRequest}
    @param request: Client Request object
    @type message: C{dict}
    @param message: Message object
    @type profileid: C{string}
    @param profile: Unique Profile id
    @rtype: C{dict}
    @return: Returns success of the command
    """
    from booki.utils.book import createBookiGroup, BookiGroupExist
    groupName = message.get('groupName', '')
    groupDescription = message.get('groupDescription', '')
    try:
        group = createBookiGroup(groupName, groupDescription, request.user)
        group.members.add(request.user)
    except BookiGroupExist:
        transaction.rollback()
        return {'created': False}

    transaction.commit()
    return {'created': True}


def remote_init_profile(request, message, profileid):
    """
    Initializes data.

    @type request: C{django.http.HttpRequest}
    @param request: Client Request object
    @type message: C{dict}
    @param message: Message object
    @type profileid: C{string}
    @param profile: Unique Profile id
    """
    import sputnik
    try:
        _onlineUsers = sputnik.smembers('sputnik:channel:%s:users' % message['channel'])
    except:
        _onlineUsers = []

    if request.user.username not in _onlineUsers:
        try:
            sputnik.sadd('sputnik:channel:%s:users' % message['channel'], request.user.username)
        except:
            pass

    return {}


def remote_mood_set(request, message, profileid):
    """
    Sets new mood for this profile.

    Input:
     - value

    @type request: C{django.http.HttpRequest}
    @param request: Client Request object
    @type message: C{dict}
    @param message: Message object
    @type profileid: C{string}
    @param profile: Unique Profile id
    """
    from django.utils.html import strip_tags
    moodMessage = strip_tags(message.get('value', ''))[:30]
    import booki.account.signals
    booki.account.signals.account_status_changed.send(sender=request.user, message=message.get('value', ''))
    profile = request.user.get_profile()
    profile.mood = moodMessage
    try:
        profile.save()
    except:
        transaction.rollback()

    transaction.commit()
    import sputnik
    for chnl in sputnik.smembers('sputnik:channels'):
        if sputnik.sismember('sputnik:channel:%s:users' % message['channel'], request.user.username):
            sputnik.addMessageToChannel(request, chnl, {'command': 'user_status_changed', 'from': request.user.username, 
               'message': moodMessage}, myself=True)

    return {}


def remote_hide_book(request, message, profileid):
    from booki.editor import models
    book = models.Book.objects.get(url_title=message['bookID'])
    if message['action'] == 'hide':
        book.hidden = True
    else:
        book.hidden = False
    book.save()
    transaction.commit()
    return {'result': True}


def remote_load_info(request, message, profileid):
    from django.utils.html import escape
    user = request.user
    profile = request.user.get_profile()
    description = escape(profile.description).replace('\r', '')
    lines = description.split('\n')
    import django.template.loader
    from django.template import Context
    c = Context({'user': request.user})
    tmpl = django.template.loader.get_template_from_string('{% load profile %}{% profile_image  user %}')
    html = tmpl.render(c)
    info = {'username': user.username, 'fullname': user.first_name, 
       'description': ('<br/>').join(lines), 
       'image': html}
    return {'result': True, 'info': info}