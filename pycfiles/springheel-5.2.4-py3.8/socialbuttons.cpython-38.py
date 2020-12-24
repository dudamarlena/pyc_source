# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/springheel/socialbuttons.py
# Compiled at: 2019-12-16 02:46:10
# Size of source mod 2**32: 3424 bytes
from springheel.__init__ import *

def getButtons(site, rss_s):
    """
    Show social media icons on the site as desired.

    Parameters
    ----------
    site : Site
        The site for which icons are being generated.
    rss_s : str
        The string to use as alt text for RSS in the current language.
    Returns
    -------
    social_links : list
        Dictionaries with metadata about other sites.
    icons : str
        HTML img elements that hyperlink to other sites.
    """
    twitter_handle = site.config.twitter_handle
    tumblr_handle = site.config.tumblr_handle
    patreon_handle = site.config.patreon_handle
    pump_url = site.config.pump_url
    diaspora_url = site.config.diaspora_url
    liberapay_handle = site.config.liberapay_handle
    social_links = []
    if site.config.social_icons == 'False':
        rss_link = {'url':'feed.xml', 
         'site':'',  'title':rss_s,  'image':'rss.png'}
        social_links.append(rss_link)
    if twitter_handle != 'False':
        twitter_url = 'http://twitter.com/' + twitter_handle
        twitter = {'url':twitter_url,  'site':'twitter',  'title':'Twitter',  'image':'twitter.png'}
        social_links.append(twitter)
    if tumblr_handle != 'False':
        tumblr_url = 'http://' + tumblr_handle + '.tumblr.com'
        tumblr = {'url':tumblr_url,  'site':'tumblr',  'title':'tumblr.',  'image':'tumblr.png'}
        social_links.append(tumblr)
    if patreon_handle != 'False':
        patreon_url = 'https://www.patreon.com/' + patreon_handle
        patreon = {'url':patreon_url,  'site':'Patreon',  'title':'Patreon',  'image':'patreon.png'}
        social_links.append(patreon)
    if liberapay_handle != 'False':
        liberapay_url = 'https://liberapay.com/' + liberapay_handle
        liberapay = {'url':liberapay_url,  'site':'Liberapay',  'title':'Liberapay',  'image':'liberapay.png'}
        social_links.append(liberapay)
    if pump_url != 'False':
        pump = {'url':pump_url, 
         'site':'pump',  'title':'Pump.io',  'image':'pump.png'}
        social_links.append(pump)
    if diaspora_url != 'False':
        diaspora = {'url':diaspora_url, 
         'site':'diaspora',  'title':'diaspora*',  'image':'diaspora.png'}
        social_links.append(diaspora)
    social_icons = []
    for i in social_links:
        icon = springheel.__init__.wrapImage(i['url'], i['title'], i['image'])
        social_icons.append(icon)
    else:
        icons = ' '.join(social_icons)
        return (
         social_links, icons)