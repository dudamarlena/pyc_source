# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/springheel/genrss.py
# Compiled at: 2019-12-16 01:43:37
# Size of source mod 2**32: 2386 bytes
from feedgen.feed import FeedGenerator
import datetime, os
from datetime import timezone

def generateFeed(base_url, rssmeta, comics):
    """
    Generate an RSS feed for a comic site.

    Parameters
    ----------
    base_url : str
        The URL of the base site.
    rssmeta : dict
        Metadata needed by the RSS feed.
    comics : list
        All comic strips on the site.
    Returns
    -------
    rssfeed : str
        The generated RSS feed.
    """
    from feedgen.feed import FeedGenerator
    fg = FeedGenerator()
    fg.id(base_url)
    fg.title(rssmeta['title'])
    fg.author({'name':rssmeta['author'],  'email':rssmeta['email']})
    fg.link(href=(rssmeta['link']), rel='self')
    fg.language(rssmeta['language'])
    fg.description(rssmeta['desc'])
    for i in comics:
        fe = fg.add_entry()
        full_url = str(base_url + i.html_filename)
        link = {'href':full_url,  'rel':'alternate',  'type':'image',  'hreflang':i.lang, 
         'title':i.title}
        fe.id(full_url)
        fe.link(link)
        authord = {'name':i.author,  'email':i.author_email}
        fe.author(authord)
        utc = timezone.utc
        adate = i.date.replace(tzinfo=utc)
        fe.published(adate)
        fe.title(i.title)
        page = str(i.page_int)
        fe.description(str(i.category + ' #' + page))
    else:
        rssfeed = fg.rss_str(pretty=True)
        o_path = os.path.join('.', 'output', 'feed.xml')
        fg.rss_file(o_path)
        return rssfeed