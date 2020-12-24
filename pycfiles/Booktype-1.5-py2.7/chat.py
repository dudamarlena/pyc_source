# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/booki/channels/chat.py
# Compiled at: 2012-02-14 23:34:00


def remote_message_send(request, message, bookid):
    """
    Called when user is sending message to chat channel L{bookid}.

    @type request: C{django.http.HttpRequest}
    @param request: Client Request object
    @type message: C{dict}
    @param message: Message object
    @type bookid: C{string}
    @param bookid: Unique Book id
    """
    import sputnik
    sputnik.addMessageToChannel(request, '/chat/%s/' % bookid, {'command': 'message_received', 'from': request.user.username, 'message': message['message']})
    return {}