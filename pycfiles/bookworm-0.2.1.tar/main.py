# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/booki/channels/main.py
# Compiled at: 2012-02-14 23:34:00
import time, re, decimal

def remote_ping(request, message):
    """
    Sends ping to the server. Just so we know client is still alive. It also removes old locks. This is not the place to do it at all, 
    but once we have normal scheduled calls, will put it there.

    @type request: C{django.http.HttpRequest}
    @param request: Client Request object
    @type message: C{dict}
    @param message: Message object
    """
    import sputnik
    sputnik.addMessageToChannel(request, '/booki/', {})
    _now = time.time()
    try:
        locks = sputnik.rkeys('booki:*:locks:*')
    except:
        return

    for key in locks:
        lastAccess = sputnik.get(key)
        if type(lastAccess) in [type(' '), type(' ')]:
            try:
                lastAccess = decimal.Decimal(lastAccess)
            except:
                continue

        if lastAccess and decimal.Decimal('%f' % _now) - lastAccess > 30:
            sputnik.rdelete(key)
            m = re.match('booki:(\\d+):locks:(\\d+):(\\w+)', key)
            if m:
                sputnik.addMessageToChannel(request, '/booki/book/%s/' % m.group(1), {'command': 'chapter_status', 'chapterID': m.group(2), 
                   'status': 'normal', 
                   'username': m.group(3)}, myself=True)


def remote_disconnect(request, message):
    pass


def remote_subscribe(request, message):
    """
    Subscribes client to specific channels.

    Input:
     - chanels

    @type request: C{django.http.HttpRequest}
    @param request: Client Request object
    @type message: C{dict}
    @param message: Message object
    """
    import sputnik
    for chnl in message['channels']:
        if not sputnik.hasChannel(chnl):
            sputnik.createChannel(chnl)
        sputnik.addClientToChannel(chnl, request.sputnikID)


def remote_connect(request, message):
    """
    Initializes sputnik connection for this client. Creates clientID for this connection. 

    Input:
     - chanels

    @type request: C{django.http.HttpRequest}
    @param request: Client Request object
    @type message: C{dict}
    @param message: Message object
    @rtype: C{string}
    @return: Returns unique Client ID for this connection
    """
    import sputnik
    ret = {}
    try:
        clientID = sputnik.incr('sputnik:client_id')
    except:
        sputnik.rcon.connect()
        clientID = sputnik.incr('sputnik:client_id')

    ret['clientID'] = clientID
    request.sputnikID = '%s:%s' % (request.session.session_key, clientID)
    if not clientID:
        return
    for chnl in message['channels']:
        if not sputnik.hasChannel(chnl):
            sputnik.createChannel(chnl)
        sputnik.addClientToChannel(chnl, request.sputnikID)

    if request.user and request.user.username.strip() != '' and request.sputnikID and request.sputnikID.find(' ') == -1:
        sputnik.set('ses:%s:username' % request.sputnikID, request.user.username)
    if request.sputnikID and request.sputnikID.strip() != '' and request.sputnikID and request.sputnikID.find(' ') == -1:
        sputnik.set('ses:%s:last_access' % request.sputnikID, time.time())
    return ret