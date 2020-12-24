# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\jld\api\delicious_objects.py
# Compiled at: 2009-01-13 14:40:53
""" Delicious objects
    @author: Jean-Lou Dupont
"""
__author__ = 'Jean-Lou Dupont'
__version__ = '$Id: delicious_objects.py 795 2009-01-13 19:42:53Z JeanLou.Dupont $'
from xml.dom import minidom
import jld.api as api
__sample__tags = '\n<?xml version="1.0" encoding="UTF-8"?>\n<tags>\n  <tag count="1" tag=".net"/>\n  <tag count="19" tag="AI"/>\n  <tag count="2" tag="AOP"/>\n  <tag count="1" tag="AmazonWebServices"/>\n  <tag count="1" tag="BT"/>\n  <tag count="1" tag="Brain"/>\n<tags>\n'

def Tags(raw):
    """ Response Processor for B{Tags} objects
    """
    try:
        e = minidom.parseString(raw).documentElement
        liste = []
        ts = e.getElementsByTagName('tag')
        for t in ts:
            count = t.getAttribute('count')
            tag = t.getAttribute('tag')
            liste.append((tag, count))

    except Exception, e:
        raise api.ErrorProtocol('msg:expecting', {'param': 'tag'})

    return liste


__sample_recent = '\n<?xml version="1.0" encoding="UTF-8"?>\n<posts user="jldupont" tag="">\n  <post    href="http://www.gliffy.com/publish/1553434/" \n            hash="94bd15480886834d104b24178dcc3e48" \n            description="BasicInterfaces" \n            tag="my-diagrams" \n            time="2008-12-01T20:36:01Z" \n            extended=""/>\n  <post href="http://dev.chromium.org/developers/design-documents/extensions" hash="b02e129cdaa64cbbb54252cfbfebeeee" description="Extensions " tag="chromium, google" time="2008-12-01T19:31:46Z" extended=""/>\n</posts>\n'
_posts_fields = [
 'href', 'hash', 'description', 'tag', 'time', 'extended']

def Posts(raw):
    """ Response Processor for B{Posts} objects
    """
    try:
        e = minidom.parseString(raw).documentElement
        liste = []
        ps = e.getElementsByTagName('post')
        for p in ps:
            entry = {}
            for key in _posts_fields:
                value = p.getAttribute(key)
                entry[key] = value

            liste.append(entry)

    except Exception, e:
        raise api.ErrorProtocol('msg:expecting', {'param': 'post'})

    return liste


__sample_recent2 = '\nhttps://api.del.icio.us/v1/posts/recent?count=100&tag=business333\n<?xml version="1.0" encoding="UTF-8"?>\n<posts user="jldupont" tag="business333"/>\n'
__sample_update = '\n<?xml version="1.0" encoding="UTF-8"?>\n<update time="2008-12-01T20:36:01Z" inboxnew="0"/>\n'

def Update(raw):
    """ Response Processor for B{Update} objects
    """
    try:
        e = minidom.parseString(raw).documentElement
        time = e.getAttribute('time')
        inbox = e.getAttribute('inboxnew')
    except Exception, e:
        raise api.ErrorProtocol('msg:expecting', {'param': 'update'})

    return (time, inbox)


__sample_bundle = '\n<?xml version="1.0" encoding="UTF-8"?>\n<bundles>\n  <bundle name="my-stuff" tags="my-diagrams my-mindmaps"/>\n</bundles>\n'

def Bundle(raw):
    """ Response processor for B{Bundle} object
    """
    try:
        e = minidom.parseString(raw).documentElement
        b = e.getElementsByTagName('bundle')[0]
        name = b.getAttribute('name')
        tags = b.getAttribute('tags')
    except Exception, e:
        raise api.ErrorProtocol('msg:expecting', {'param': 'bundle'})

    return (name, tags)


__sample_bundles = '\n<?xml version="1.0" encoding="UTF-8"?>\n<bundles>\n  <bundle name="my-stuff" tags="my-diagrams my-mindmaps"/>\n  <bundle name="php" tags="php pear PHING phpdoc PHPUnit PEAR-CHANNEL"/>\n  <bundle name="programming" tags="gae GWT python programming"/>\n  <bundle name="software" tags="ajax jquery eclipse subversion programming"/>\n  <bundle name="telecomm" tags="IP ITU atca fcoe utca ITU-T ethernet companies semiconductor"/>\n</bundles>\n'

def Bundles(raw):
    """ Response processor for B{Bundles} objects
    """
    try:
        e = minidom.parseString(raw).documentElement
        liste = []
        bs = e.getElementsByTagName('bundle')
        for b in bs:
            name = b.getAttribute('name')
            tags = b.getAttribute('tags')
            liste.append((name, tags))

    except Exception, e:
        raise api.ErrorProtocol('msg:expecting', {'param': 'bundle'})

    return liste


__sample_hashes = '\n<posts>\n    <post meta="957d3e3b5e04fbe250f995cb663ad271" url="94bd15480886834d104b24178dcc3e48"/>\n    <post meta="cf811c206b21654979dc1db885647381" url="b02e129cdaa64cbbb54252cfbfebeeee"/>\n</posts>\n'

def Hashes(raw):
    """ Response processor B{Hashes} objects
    """
    try:
        e = minidom.parseString(raw).documentElement
        liste = []
        ps = e.getElementsByTagName('post')
        for p in ps:
            meta = p.getAttribute('meta')
            url = p.getAttribute('url')
            liste.append((url, meta))

    except Exception, e:
        raise api.ErrorProtocol('msg:expecting', {'param': 'post'})

    return liste