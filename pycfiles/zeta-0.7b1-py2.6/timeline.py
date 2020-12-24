# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/zeta/comp/timeline.py
# Compiled at: 2010-05-20 12:53:09
"""Component to access data base and do data-crunching on timeline tables.
"""
from __future__ import with_statement
from sqlalchemy import insert, select
from sqlalchemy.orm import mapper, relation, eagerload
from zwiki.zwparser import ZWParser
import zeta.lib.helpers as h
from zeta.lib.constants import *
from zeta.lib.error import ZetaError
from zeta.ccore import Component
from zeta.model import meta
from zeta.model.schema import t_wikipage, t_timeline, at_user_logs, at_permgroup_logs, at_tag_logs, at_attachment_logs, at_license_logs, at_project_logs, at_ticket_logs, at_review_logs, at_vcs_logs, at_wiki_logs
from zeta.model.tables import Timeline, User, PermissionGroup, Tag, Attachment, License, Project, Ticket, Review, Vcs, Wiki
tbl_mappers = meta.tbl_mappers
metadata = meta.metadata
from zeta.ccore import Component
obj2assctable = {'user': at_user_logs, 
   'permgroup': at_permgroup_logs, 
   'tag': at_tag_logs, 
   'attach': at_attachment_logs, 
   'license': at_license_logs, 
   'project': at_project_logs, 
   'ticket': at_ticket_logs, 
   'review': at_review_logs, 
   'vcs': at_vcs_logs, 
   'wiki': at_wiki_logs}

def url_formodel(name, obj):
    """Compute the href for model object"""
    a_tmpl = name + ' <a href="%s" title="%s">%s</a>'
    if name == 'user':
        username = obj.username
        a = a_tmpl % (h.url_foruser(username), username, username)
    elif name == 'tag':
        tagname = obj.tagname
        a = a_tmpl % (h.url_fortag(tagname), tagname, tagname)
    elif name == 'attach':
        a = a_tmpl % (h.url_forattach(obj.id), obj.filename, obj.filename)
    elif name == 'license':
        a = a_tmpl % (h.url_forlicense(obj.id),
         obj.summary, obj.licensename)
    elif name == 'project':
        a = a_tmpl % (h.url_forproject(obj.projectname),
         obj.summary, obj.projectname)
    elif name == 'ticket':
        a = a_tmpl % (h.url_forticket(obj.project.projectname, obj.id),
         obj.summary, obj.id)
    elif name == 'review':
        a = a_tmpl % (h.url_forreview(obj.project.projectname, obj.id),
         obj.resource_url, obj.resource_url)
    elif name == 'vcs':
        a = a_tmpl % (h.url_forvcs(obj.project.projectname, obj.id),
         obj.name, obj.name)
    elif name == 'wiki':
        a = a_tmpl % (obj.wikiurl, obj.summary, obj.wikiurl)
    elif name == 'staticwiki':
        a = a_tmpl % (obj.path, obj.path, obj.path)
    else:
        raise ZetaError('Unkown model name in timeline reference')
    return a


def url_formodels(**kwargs):
    return (', ').join([ url_formodel(k, kwargs[k]) for k in kwargs if kwargs[k] ])


class TimelineComponent(Component):

    def log(self, user, log, **kwargs):
        """Make an entry and all the timeline as logs to models, specified by
        kwargs, which can be,
            permgroup, tag, attach, license,
            project,
            ticket,
            review,
            wiki"""
        config = self.compmgr.config
        tl = None
        if config['zeta.enabletline']:
            userscomp = config['userscomp']
            c = self.compmgr.config.get('c', None)
            user = user or c and c.authuser
            user = userscomp.get_user(user)
            log = user and '%s' % log.decode('utf8') or log.decode('utf8')
            userhtml = '<a href="%s">%s</a>' % (
             h.url_foruser(user.username), user.username)
            itemhtml = url_formodels(**kwargs)
            if config.get('zeta.fasttline', None):
                msession = meta.Session()
                with msession.begin(subtransactions=True):
                    res = msession.connection().execute(t_timeline.insert().values(log=unicode(log[:LEN_1K]), userhtml=unicode(userhtml), itemhtml=unicode(itemhtml)))
                    tl_id = res.inserted_primary_key[0]
                    msession.connection().execute(at_user_logs.insert().values(timelineid=tl_id, userid=user.id))
                    kwargs.pop('staticwiki', None)
                    for k in kwargs:
                        kw = {'timelineid': tl_id, k + 'id': kwargs[k].id}
                        msession.connection().execute(obj2assctable[k].insert().values(**kw))

            else:
                msession = meta.Session()
                with msession.begin(subtransactions=True):
                    tl = Timeline(unicode(log[:LEN_1K]), unicode(userhtml), unicode(itemhtml))
                    msession.add(tl)
                    user.logs.append(tl)
                    [ kwargs[k].logs.append(tl) for k in kwargs.keys() ]
        return tl

    def fetchlogs(self, assc_tbls, modelobj=None, limit=None, id=None, direction=None):
        """Fetch log entries for associated tables 'assc_tbls',
        if modelobj != None,
            logs associated to modelobj.id
        if limit :
            
        Always return list of Tline instances """
        msession = meta.Session()
        if direction == 'newer':
            q = msession.query(Timeline).order_by(Timeline.id.asc())
            q = id and q.filter(Timeline.id > id)
        elif direction == 'older':
            q = msession.query(Timeline).order_by(Timeline.id.desc())
            q = id and q.filter(Timeline.id < id)
        else:
            q = msession.query(Timeline).order_by(Timeline.id.desc())
        if assc_tbls and isinstance(assc_tbls, list):
            q = q.join(*assc_tbls)
        elif assc_tbls:
            q = q.join(assc_tbls)
        if modelobj:
            q = q.filter_by(id=modelobj.id)
        if limit != None:
            q = q.limit(limit)
        logs = q.all()
        if direction == 'newer' and id:
            logs.reverse()
        return logs

    def fetchprojlogs(self, project, limit=None, id=None, direction=None):
        """Fetch log entries for 'project'"""
        msession = meta.Session()
        if direction == 'newer':
            common_q = msession.query(Timeline).order_by(Timeline.id.asc())
            common_q = id and common_q.filter(Timeline.id > id) or common_q
        elif direction == 'older':
            common_q = msession.query(Timeline).order_by(Timeline.id.desc())
            common_q = id and common_q.filter(Timeline.id < id) or common_q
        else:
            common_q = msession.query(Timeline).order_by(Timeline.id.desc())
        q = common_q.join('project').filter_by(id=project.id)
        q = limit and q.limit(limit) or q
        logs = q.all()
        q = common_q.join('ticket', 'project').filter_by(id=project.id)
        q = limit and q.limit(limit) or q
        logs += q.all()
        q = common_q.join('vcs', 'project').filter_by(id=project.id)
        q = limit and q.limit(limit) or q
        logs += q.all()
        q = common_q.join('review', 'project').filter_by(id=project.id)
        q = limit and q.limit(limit) or q
        logs += q.all()
        q = common_q.join('wiki', 'project').filter_by(id=project.id)
        q = limit and q.limit(limit) or q
        logs += q.all()
        logs = sorted(logs, key=lambda log: log.id, reverse=True)
        return logs

    def get_log(self, fromid, limit):
        """Fetch logs from `fromid` to `toid"""
        msession = meta.Session()
        q = msession.query(Timeline).filter(Timeline.id >= fromid)
        q = limit and q.limit(limit) or q
        logs = q.all()
        return logs