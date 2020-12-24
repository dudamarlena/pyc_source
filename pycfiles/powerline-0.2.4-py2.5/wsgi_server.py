# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/powerline/tools/wsgi_server.py
# Compiled at: 2008-04-11 15:13:57
CONFIGURATION_FILES = [
 '/opt/powerline/etc/powerline.conf']
if __name__ == '__main__':
    import sys
    sys.stdout = sys.stderr
    import atexit, cherrypy
    from powerline.main import root
    for config_file in CONFIGURATION_FILES:
        cherrypy.config.update(config_file)

    cherrypy.config.update({'environment': 'embedded'})
    if cherrypy.engine.state == 0:
        cherrypy.engine.start(blocking=False)
        atexit.register(cherrypy.engine.stop)
    application = cherrypy.Application(root(), None)