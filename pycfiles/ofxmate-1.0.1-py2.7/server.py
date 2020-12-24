# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.8-intel/egg/ofxmate/server.py
# Compiled at: 2013-03-26 18:51:05
import cherrypy, webapp, webbrowser, threading, getopt, sys

def browser(url):
    webbrowser.open(url, new=1, autoraise=True)


def server(host='127.0.0.1', port='8899', verbose=False, open_browser=True, quiet=False):
    mode = 'development' if verbose else ''
    l2s = True if verbose else False
    config = {'global': {'server.environment': mode, 
                  'server.socket_host': host, 
                  'server.socket_port': int(port), 
                  'server.log_to_screen': l2s, 
                  'log.screen': l2s}, 
       '/': {'tools.staticdir.root': webapp.html_dir}, 
       '/favicon.ico': {'tools.staticfile.on': True, 
                        'tools.staticfile.filename': webapp.html_dir + '/favicon.ico'}, 
       '/static': {'tools.staticdir.on': True, 
                   'tools.staticdir.dir': 'static'}}
    url = 'http://%s:%s%s' % (host, port, '/')
    if not quiet:
        print 'Visit this url in your browser to use the app'
        print url
    if open_browser:
        browser_open = threading.Timer(1.0, browser, args=[url])
        browser_open.start()
    cherrypy.quickstart(webapp.Root(), config=config)


def cmdline():
    args = sys.argv[1:]
    host = '127.0.0.1'
    port = '8899'
    open_browser = True
    verbose = False
    optlist, args = getopt.getopt(args, 'vbh:p:')
    for opt in optlist:
        if opt[0] == '-p':
            port = opt[1]
        if opt[0] == '-h':
            host = opt[1]
        if opt[0] == '-v':
            verbose = True
        if opt[0] == '-b':
            open_browser = False

    server(host=host, port=port, verbose=verbose, open_browser=open_browser)


if __name__ == '__main__':
    cmdline()