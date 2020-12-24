# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/archipelagentiphonenotification/notifications.py
# Compiled at: 2013-03-20 13:50:16
__doc__ = "Client for the iPhone/iPod Touch `Notifications' app.\n\nThis  module helps  scripts to  use  the HTTP  REST API  of the  `Notifications'\napplication, which is  available for the iPhone and the  iPod Touch. It supports\nfinding  the  user's credentials  token,  and  then  sending notification  in  a\nsynchronous or asynchronous way. This modules provides three functions:\n\nget_credentials() -- Get the user's credentials token\nsend() -- Send a notification, waiting for it to be sent.\nsend_async() -- Send a  notification, returning immediately, without waiting for\nthe message to be sent.\n\n"
__author__ = 'Thomas Jost <thomas.jost@gmail.com>'
__version__ = '0.1'
import thread, urllib, xml.dom.minidom
CREDENTIALS_URL = 'https://www.appnotifications.com/user_session.xml'
SEND_URL = 'https://www.appnotifications.com/account/notifications.xml'

def get_credentials(email, password):
    """Get the user's credentials token."""
    data = {'user_session[email]': email, 
       'user_session[password]': password}
    data = urllib.urlencode(data)
    u = urllib.urlopen(SEND_URL, data)
    success = u.getcode() == 200
    if not success:
        return False
    response = u.read()
    u.close()
    doc = xml.dom.minidom.parseString(response)
    token = doc.getElementsByTagName('single-access-token')
    if len(token) == 0:
        return False
    return token[0].firstChild.data


def send(credentials, message, title=None, long_message=None, subtitle=None, long_message_preview=None, message_level=0, silent=False, action_loc_key=None, run_command=None, sound=1, icon_url=None, debug=False):
    """Send a notification, waiting for the message to be sent.

    The first two arguments (credentials  and message) are mandatory, all of the
    others are optional. They are  the same as the various identifiers described
    in    the   documentation    of    the   Notifications    HTTP   REST    API
    (http://appnotifications.com/account/rest_api).

    When  `debug` is  set  to `True`,  the XML  result  of the  HTTP request  is
    displayed on `sys.stderr`.

    This  function  returns  a  boolean  indicating  if  the  message  was  sent
    successfuly.

    """
    try:
        data = {}
        if credentials is None or credentials == '':
            raise ValueError('Invalid user credentials')
        if message is None or message == '':
            raise ValueError('Invalid message')
        data['user_credentials'] = credentials
        data['notification[message]'] = message
        for key in ('title', 'long_message', 'long_message_preview', 'message_level',
                    'action_loc_key', 'run_command', 'icon_url', 'subtitle'):
            value = locals()[key]
            if value is not None:
                data['notification[%s]' % key] = value

        if silent:
            data['notification[silent]'] = 1
        else:
            data['notification[silent]'] = 0
            if not 1 <= sound <= 7:
                raise ValueError('sound must be an integer between 1 and 7')
            data['notification[sound]'] = '%d.caf' % sound
        data = urllib.urlencode(data)
        u = urllib.urlopen(SEND_URL, data)
        success = u.getcode() == 200
        if debug:
            print >> sys.stderr, u.read()
        u.close()
        return success
    except:
        pass

    return


def send_async(*args, **kwargs):
    """Send  a  notification, returning  immediately,  without  waiting for  the
    message to be sent.

    This function does return the ID of the thread that does the HTTP request.

    """
    return thread.start_new_thread(send, args, kwargs)


if __name__ == '__main__':
    import sys, time
    if len(sys.argv) != 3:
        print >> sys.stderr, 'Syntax: %s credentials message' % sys.argv[0]
    else:
        send_async(sys.argv[1], sys.argv[2], title='MyTITLE', debug=True)
        time.sleep(5)