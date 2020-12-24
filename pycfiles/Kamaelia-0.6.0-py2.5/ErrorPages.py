# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/Kamaelia/Protocol/HTTP/ErrorPages.py
# Compiled at: 2008-10-19 12:19:52


def getErrorPage(errorcode, msg=''):
    """    Get the HTML associated with an (integer) error code.
    """
    if errorcode == 400:
        return {'statuscode': '400', 'data': "<html>\n<title>400 Bad Request</title>\n<body style='background-color: black; color: white;'>\n<h2>400 Bad Request</h2>\n<p>" + msg + '</p></body>\n</html>\n\n', 
           'content-type': 'text/html'}
    elif errorcode == 404:
        return {'statuscode': '404', 'data': "<html>\n<title>404 Not Found</title>\n<body style='background-color: black; color: white;'>\n<h2>404 Not Found</h2>\n<p>" + msg + '</p></body>\n</html>\n\n', 
           'content-type': 'text/html'}
    elif errorcode == 500:
        return {'statuscode': '500', 'data': "<html>\n<title>500 Internal Server Error</title>\n<body style='background-color: black; color: white;'>\n<h2>500 Internal Server Error</h2>\n<p>" + msg + '</p></body>\n</html>\n\n', 
           'content-type': 'text/html'}
    elif errorcode == 501:
        return {'statuscode': '501', 'data': "<html>\n<title>501 Not Implemented</title>\n<body style='background-color: black; color: white;'>\n<h2>501 Not Implemented</h2>\n<p>" + msg + '</p></body>\n</html>\n\n', 
           'content-type': 'text/html'}
    else:
        return {'statuscode': str(errorcode), 
           'data': '', 
           'content-type': 'text/html'}