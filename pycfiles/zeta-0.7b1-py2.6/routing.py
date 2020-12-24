# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/zeta/config/routing.py
# Compiled at: 2010-05-28 03:49:44
"""Routes configuration

The more specific and detailed routes should be defined first so they
may take precedent over the more generic routes. For more information
refer to the routes manual at http://routes.groovie.org/docs/
"""
from routes import Mapper
r_home = 'home'
r_aboutus = 'aboutus'
r_tos = 'tos'
r_accounts = 'accounts'
r_siteadmin = 'siteadmin'
r_sitecharts = 'sitecharts'
r_sitelogo = 'sitelogo'
r_sitefeeds = 'sitefeed'
r_sitetline = 'sitetimeline'
r_attachments = 'attachments'
r_attachfeeds = 'attachfeeds'
r_attachtimeline = 'attachtimeline'
r_attachcharts = 'attachcharts'
r_addattchments = 'addattachments'
r_attachment = 'attachment'
r_attachdownl = 'attachdownl'
r_tags = 'tags'
r_tag = 'tagname'
r_tagstline = 'tagstline'
r_tagtline = 'tagtline'
r_tagsfeed = 'tagsfeed'
r_tagfeed = 'tagfeed'
r_liccreate = 'liccreate'
r_liccharts = 'liccharts'
r_lictimelines = 'lictimelines'
r_lictimeline = 'lictimeline'
r_licfeeds = 'licfeeds'
r_licfeed = 'licfeed'
r_licattachs = 'licattachs'
r_license = 'license'
r_licenseid = 'licenseid'
r_userhome = 'userhome'
r_usertickets = 'usertickets'
r_userpref = 'userpref'
r_usercharts = 'usercharts'
r_userstline = 'userstimeline'
r_usertline = 'usertimeline'
r_usersfeed = 'usersfeed'
r_userfeed = 'userfeed'
r_usershome = 'users'
r_usersgmap = 'usersgmap'
r_usersinvite = 'usersinvite'
r_userscharts = 'userscharts'
r_projects = 'projects'
r_projcreate = 'projcreate'
r_projecthome = 'projecthome'
r_projroadmap = 'projectroadmap'
r_projmstns = 'projectmilestones'
r_projmstn = 'projectmilestone'
r_projtline = 'projtimeline'
r_projadmtline = 'projadmtimeline'
r_projfeed = 'projfeed'
r_projadmfeed = 'projadmfeed'
r_projattachs = 'projattachs'
r_projdownlds = 'projdownloads'
r_projcharts = 'projectcharts'
r_projadmin = 'projadmin'
r_project = 'project'
r_projtickets = 'tickets'
r_projticketid = 'ticket'
r_projtidgraph = 'ticketgraph'
r_projtckcreate = 'ticketcreate'
r_projtckstline = 'ticketstimeline'
r_projtcktline = 'tickettimeline'
r_projtcksfeed = 'ticketsfeed'
r_projtckfeed = 'ticketfeed'
r_projtckcharts = 'ticketcharts'
r_projtckattachs = 'ticketattachs'
r_projvcs = 'vcsindex'
r_projvcscreate = 'createvcs'
r_projvcsbrowse = 'vcsbrowse'
r_projvcsfile = 'vcsfile'
r_projvcsrevlist = 'vcsrevlist'
r_projvcsrev = 'vcsrev'
r_projvcsdiff = 'vcsdiff'
r_projvcsdiffdown = 'vcsdiffdown'
r_projvcsfiledown = 'vcsfiledown'
r_projvcstlines = 'vcstlines'
r_projvcstline = 'vcstline'
r_projvcsfeeds = 'vcsfeeds'
r_projvcsfeed = 'vcsfeed'
r_projmounts = 'projmounts'
r_projmount = 'projmount'
r_projwikis = 'wikis'
r_projwtindex = 'wikititleindex'
r_projwTIndex = 'wikiTitleIndex'
r_projwikistline = 'wikistline'
r_projwikitline = 'wikitline'
r_projwikisfeed = 'wikisfeed'
r_projwikifeed = 'wikifeed'
r_projwikicharts = 'wikicharts'
r_projwikiattachs = 'wikiattachs'
r_projwiki = 'wiki'
r_projrevw = 'revwindex'
r_projrevwsets = 'revwsets'
r_projrevwset = 'revwset'
r_projrevwcreate = 'revwcreate'
r_projrevwid = 'revwid'
r_projrevwtlines = 'revwtlines'
r_projrevwtline = 'revwtline'
r_projrevwfeeds = 'revwfeeds'
r_projrevwfeed = 'revwfeed'
r_projrevwcharts = 'revwcharts'
r_projrevwattachs = 'revwattachs'
r_pasteradmin = 'pasteradmin'
r_titleindex = 'titleindex'
r_TitleIndex = 'TitleIndex'
r_searchpage = 'searchpage'
r_xmlrpc = 'xmlrpc'
r_staticwiki = 'staticwiki'

def make_map(config):
    """Create, configure and return the routes Mapper"""
    map = Mapper(directory=config['pylons.paths']['controllers'], always_scan=config['debug'])
    map.minimization = False
    map.connect('/error/{action}', controller='error')
    map.connect('/error/{action}/{id}', controller='error')
    map.connect('/debug', controller='debug', action='index')
    map.connect(r_accounts, '/accounts/{action}', controller='accounts')
    map.connect(r_siteadmin, '/siteadmin', controller='siteadmin', action='index')
    map.connect(r_sitecharts, '/sitecharts', controller='siteadmin', action='charts')
    map.connect(r_sitetline, '/sitetline', controller='siteadmin', action='timeline')
    map.connect(r_sitefeeds, '/sitefeed', controller='siteadmin', action='feed')
    map.connect(r_sitelogo, '/uploadlogo', controller='siteadmin', action='uploadlogo')
    map.connect(r_attachments, '/attachment', controller='attachment', action='index')
    map.connect(r_attachtimeline, '/attachment/timeline', controller='attachment', action='timeline')
    map.connect(r_attachfeeds, '/attachment/feed', controller='attachment', action='feed')
    map.connect(r_addattchments, '/attachment/add', controller='attachment', action='add')
    map.connect(r_attachcharts, '/attachment/charts', controller='attachment', action='charts')
    map.connect(r_attachment, '/attachment/{id}', controller='attachment', action='attach')
    map.connect(r_attachdownl, '/attachment/download/{id}', controller='attachment', action='download')
    map.connect(r_tags, '/tags', controller='tag', action='index')
    map.connect(r_tag, '/tag/{tagname}', controller='tag', action='tagname')
    map.connect(r_tagstline, '/tags/timeline', controller='tag', action='timeline')
    map.connect(r_tagtline, '/tags/timeline/{tagname}', controller='tag', action='timeline')
    map.connect(r_tagsfeed, '/tags/feed', controller='tag', action='feed')
    map.connect(r_tagfeed, '/tags/feed/{tagname}', controller='tag', action='feed')
    map.connect(r_liccreate, '/license/create', controller='license', action='liccreate')
    map.connect(r_liccharts, '/license/charts', controller='license', action='charts')
    map.connect(r_lictimelines, '/license/timeline', controller='license', action='timeline')
    map.connect(r_lictimeline, '/license/timeline/{id}', controller='license', action='timeline')
    map.connect(r_licfeeds, '/license/feed', controller='license', action='feed')
    map.connect(r_licfeed, '/license/feed/{id}', controller='license', action='feed')
    map.connect(r_licattachs, '/license/attachs', controller='license', action='attachs')
    map.connect(r_license, '/license', controller='license', action='license')
    map.connect(r_licenseid, '/license/{id}', controller='license', action='license')
    map.connect(r_userstline, '/u/timeline', controller='userpage', action='timeline')
    map.connect(r_usertline, '/u/timeline/{username}', controller='userpage', action='timeline')
    map.connect(r_usersfeed, '/u/feed', controller='userpage', action='feed')
    map.connect(r_userfeed, '/u/feed/{username}', controller='userpage', action='feed')
    map.connect(r_usershome, '/u', controller='userpage', action='index')
    map.connect(r_usersgmap, '/u/gmap', controller='userpage', action='gmap')
    map.connect(r_usersinvite, '/u/inviteuser', controller='userpage', action='inviteuser')
    map.connect(r_userscharts, '/u/charts', controller='userpage', action='charts')
    map.connect(r_userhome, '/u/{username}', controller='userpage', action='userhome')
    map.connect(r_usertickets, '/u/{username}/t', controller='userpage', action='tickets')
    map.connect(r_userpref, '/u/{username}/preference', controller='userpage', action='preference')
    map.connect(r_usercharts, '/u/{username}/charts', controller='userpage', action='usercharts')
    map.connect(r_projects, '/p', controller='projects', action='index')
    map.connect(r_projcreate, '/p/newproject', controller='projects', action='create')
    map.connect(r_projecthome, '/p/{projectname}', controller='projects', action='projecthome')
    map.connect(r_projroadmap, '/p/{projectname}/roadmap', controller='projects', action='roadmap')
    map.connect(r_projtline, '/p/{projectname}/timeline', controller='projects', action='timeline')
    map.connect(r_projadmtline, '/p/{projectname}/timeline/admin', controller='projects', action='timelineadmin')
    map.connect(r_projfeed, '/p/{projectname}/feed', controller='projects', action='feed')
    map.connect(r_projadmfeed, '/p/{projectname}/feed/admin', controller='projects', action='feedadmin')
    map.connect(r_projattachs, '/p/{projectname}/attachs', controller='projects', action='attachs')
    map.connect(r_projdownlds, '/p/{projectname}/downloads', controller='projects', action='downloads')
    map.connect(r_projcharts, '/p/{projectname}/charts', controller='projects', action='charts')
    map.connect(r_projadmin, '/p/{projectname}/admin', controller='projects', action='admin')
    map.connect(r_projmstns, '/p/{projectname}/m', controller='projects', action='milestone', id='')
    map.connect(r_projmstn, '/p/{projectname}/m/{id}', controller='projects', action='milestone')
    map.connect(r_projwikis, '/p/{projectname}/wiki', controller='projwiki', action='wikiindex')
    map.connect(r_projwtindex, '/p/{projectname}/wiki/titleindex', controller='projwiki', action='titleindex')
    map.connect(r_projwTIndex, '/p/{projectname}/wiki/TitleIndex', controller='projwiki', action='titleindex')
    map.connect(r_projwikistline, '/p/{projectname}/wiki/timeline', controller='projwiki', action='timeline')
    map.connect(r_projwikitline, '/p/{projectname}/wiki/timeline/*(url)', controller='projwiki', action='timeline')
    map.connect(r_projwikisfeed, '/p/{projectname}/wiki/feed', controller='projwiki', action='feed')
    map.connect(r_projwikifeed, '/p/{projectname}/wiki/feed/*(url)', controller='projwiki', action='feed')
    map.connect(r_projwikicharts, '/p/{projectname}/wiki/charts', controller='projwiki', action='charts')
    map.connect(r_projwikiattachs, '/p/{projectname}/wiki/attachs', controller='projwiki', action='attachs')
    map.connect(r_projwiki, '/p/{projectname}/wiki/*(url)', controller='projwiki', action='wiki')
    map.connect(r_projtickets, '/p/{projectname}/t', controller='projticket', action='ticketindex')
    map.connect(r_projtckcreate, '/p/{projectname}/t/createticket', controller='projticket', action='createticket')
    map.connect(r_projtckstline, '/p/{projectname}/t/timeline', controller='projticket', action='timeline')
    map.connect(r_projtcktline, '/p/{projectname}/t/timeline/{id}', controller='projticket', action='timeline')
    map.connect(r_projtcksfeed, '/p/{projectname}/t/feed', controller='projticket', action='feed')
    map.connect(r_projtckfeed, '/p/{projectname}/t/feed/{id}', controller='projticket', action='feed')
    map.connect(r_projtckcharts, '/p/{projectname}/t/charts', controller='projticket', action='charts')
    map.connect(r_projtckattachs, '/p/{projectname}/t/attachs', controller='projticket', action='attachs')
    map.connect(r_projticketid, '/p/{projectname}/t/{id}', controller='projticket', action='ticket', id='')
    map.connect(r_projtidgraph, '/p/{projectname}/t/{id}/{file}', controller='projticket', action='ticketgraph')
    map.connect(r_projvcs, '/p/{projectname}/s', controller='projvcs', action='vcsindex')
    map.connect(r_projvcscreate, '/p/{projectname}/s/createvcs', controller='projvcs', action='createvcs')
    map.connect(r_projvcstlines, '/p/{projectname}/s/timeline', controller='projvcs', action='timeline')
    map.connect(r_projvcstline, '/p/{projectname}/s/timeline/{id}', controller='projvcs', action='timeline')
    map.connect(r_projvcsfeeds, '/p/{projectname}/s/feed', controller='projvcs', action='feed')
    map.connect(r_projvcsfeed, '/p/{projectname}/s/feed/{id}', controller='projvcs', action='feed')
    map.connect(r_projvcsbrowse, '/p/{projectname}/s/{id}/browse', controller='projvcs', action='vcs_browse')
    map.connect(r_projvcsrevlist, '/p/{projectname}/s/{id}/revlist', controller='projvcs', action='vcs_revlist')
    map.connect(r_projvcsrev, '/p/{projectname}/s/{id}/revision', controller='projvcs', action='vcs_revision')
    map.connect(r_projvcsdiff, '/p/{projectname}/s/{id}/diff', controller='projvcs', action='vcs_diff')
    map.connect(r_projvcsdiffdown, '/p/{projectname}/s/{id}/diffdownl', controller='projvcs', action='diffdownload')
    map.connect(r_projvcsfiledown, '/p/{projectname}/s/{id}/filedownl', controller='projvcs', action='filedownload')
    map.connect(r_projvcsfile, '/p/{projectname}/s/{id}/*(filepath)', controller='projvcs', action='vcs_file')
    map.connect(r_projmounts, '/p/{projectname}/mnt', controller='projmount', action='mounts')
    map.connect(r_projmount, '/p/{projectname}/mnt/{id}/*(murl)', controller='projmount', action='mount')
    map.connect(r_projrevw, '/p/{projectname}/r', controller='projreview', action='index')
    map.connect(r_projrevwsets, '/p/{projectname}/rset', controller='projreview', action='reviewset')
    map.connect(r_projrevwset, '/p/{projectname}/rset/{id}', controller='projreview', action='reviewset')
    map.connect(r_projrevwcreate, '/p/{projectname}/r/createrevw', controller='projreview', action='create')
    map.connect(r_projrevwtlines, '/p/{projectname}/r/timeline', controller='projreview', action='timeline')
    map.connect(r_projrevwtline, '/p/{projectname}/r/timeline/{id}', controller='projreview', action='timeline')
    map.connect(r_projrevwfeeds, '/p/{projectname}/r/feed', controller='projreview', action='feed')
    map.connect(r_projrevwfeed, '/p/{projectname}/r/feed/{id}', controller='projreview', action='feed')
    map.connect(r_projrevwcharts, '/p/{projectname}/r/charts', controller='projreview', action='charts')
    map.connect(r_projrevwattachs, '/p/{projectname}/r/attachs', controller='projreview', action='attachs')
    map.connect(r_projrevwid, '/p/{projectname}/r/{id}', controller='projreview', action='review')
    map.connect(r_project, '/p/{projectname}/{action}', controller='projects')
    map.connect(r_pasteradmin, '/pasteradmin/{action}', controller='pasteradmin')
    map.connect(r_tos, '/tos', controller='home', action='tos')
    map.connect(r_home, '/', controller='home', action='index')
    map.connect(r_searchpage, '/search', controller='search', action='index')
    map.connect(r_xmlrpc, '/xmlrpc', controller='xmlrpc', action='index')
    map.connect(r_titleindex, '/titleindex', controller='home', action='titleindex')
    map.connect(r_TitleIndex, '/TitleIndex', controller='home', action='titleindex')
    map.connect(r_staticwiki, '/*(url)', controller='home', action='staticwiki')
    return map