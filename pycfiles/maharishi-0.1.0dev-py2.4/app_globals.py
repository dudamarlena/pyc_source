# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/maharishi/lib/app_globals.py
# Compiled at: 2006-08-30 12:30:23


class Globals(object):
    __module__ = __name__

    def __init__(self, global_conf, app_conf, **extra):
        """
        You can put any objects which need to be initialised only once
        here as class attributes and they will be available as globals
        everywhere in your application and will be intialised only once,
        not on every request.
        
        ``global_conf``
            The same as variable used throughout ``config/middleware.py``
            namely, the variables from the ``[DEFAULT]`` section of the
            configuration file.
            
        ``app_conf``
            The same as the ``kw`` dictionary used throughout 
            ``config/middleware.py`` namely, the variables the section 
            in the config file for your application.
            
        ``extra``
            The configuration returned from ``load_config`` in 
            ``config/middleware.py`` which may be of use in the setup of 
            your global variables.
            
        """
        pass

    def __del__(self):
        """
        Put any cleanup code to be run when the application finally exits 
        here.
        """
        pass