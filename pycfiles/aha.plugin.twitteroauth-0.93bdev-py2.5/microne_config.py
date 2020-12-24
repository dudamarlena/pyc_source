# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/twitteroauth/microne_config.py
# Compiled at: 2011-03-22 05:23:05
"""
    tipfy.ext.auth.microne_config
    ~~~~~~~~~~~~~~~~~~~~~~

    A module for configuration functions for microne plugin.
"""
import logging, aha
config = aha.Config()
__all__ = [
 'initConfig']

def initConfig(app, consumer_key, consumer_secret, oauth_redirect_path='/oauth'):
    """
    A function to make configuration of twitter authentication for microne.
    Arguments :
    :param app             : App object of microne
    :param consumer_key    : Twitter consumer_key
    :param consumer_secret : Twitter consumer_secret
    """
    from plugin.twitteroauth.twitter_auth import TwitterOAuth
    from plugin.twitteroauth.twitteroauth import TwitteroauthController
    config.auth_obj = TwitterOAuth
    config.consumer_key = consumer_key
    config.consumer_secret = consumer_secret

    @app.route(oauth_redirect_path)
    def oauth():
        """
        A function to receive oauth redirection.
        It passes information in url to TwitteroauthController._post_action()
        """
        controller = TwitteroauthController(app.get_handler())
        auth_obj = TwitterOAuth()
        auth_obj.request = app.request
        auth_obj.request.args = app.request.params
        auth_obj.get_authenticated_user(controller._post_action)