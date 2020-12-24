# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/jupyterlab_twitter/__init__.py
# Compiled at: 2018-07-06 02:45:54
# Size of source mod 2**32: 1204 bytes
"""
Python module to initialize Server Extension & Notebook Extension
"""
import os
from jupyterlab_twitter.handlers import setup_handlers
from jupyterlab_twitter.twitter import Twitter

def _jupyter_server_extension_paths():
    """
    Function to declare Jupyter Server Extension Paths.
    """
    return [
     {'module': 'jupyterlab_twitter'}]


def _jupyter_nbextension_paths():
    """
    Function to declare Jupyter Notebook Extension Paths.
    """
    return [
     {'section':'notebook', 
      'dest':'jupyterlab_twitter'}]


def load_jupyter_server_extension(nbapp):
    """
    Function to load Jupyter Server Extension.
    """
    twitter = Twitter()
    nbapp.web_app.settings['twitter'] = twitter
    nbapp.web_app.settings['xsrf_cookies'] = False
    nbapp.web_app.settings['twitter_consumer_key'] = os.environ['DATALAYER_TWITTER_CONSUMER_KEY']
    nbapp.web_app.settings['twitter_consumer_secret'] = os.environ['DATALAYER_TWITTER_CONSUMER_SECRET']
    nbapp.web_app.settings['cookie_secret'] = '32oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo='
    nbapp.web_app.settings['login_url'] = '/twitter/auth/popup'
    nbapp.web_app.settings['debug'] = True
    setup_handlers(nbapp.web_app)