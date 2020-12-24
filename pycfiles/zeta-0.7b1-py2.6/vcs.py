# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/zeta/comp/vcs.py
# Compiled at: 2010-05-06 03:08:26
"""Component to access data base and do data-crunching on vcs tables."""
from __future__ import with_statement
import os
from sqlalchemy import *
from sqlalchemy.orm import *
from authkit.permissions import no_authkit_users_in_environ
from zeta.ccore import Component
import zeta.lib.helpers as h
from zeta.model import meta
from zeta.model.tables import Project, VcsType, Vcs, VcsMount
from zeta.model.schema import t_vcsmount, t_project, t_vcs, at_vcs_projects
from zeta.comp.attach import AttachComponent
from zeta.comp.project import ProjectComponent
from zeta.comp.timeline import TimelineComponent

class VcsComponent(Component):
    """Component Version Control System."""

    def get_vcstype(self, vcs_type=None):
        """Get VcsType instance for the type identified by,
        vcs_type, which can be,
            `id` or `vcs_typename` or `VcsType` instance.

        Return,     
            VcsType instance.
            A list of VcsType instances."""
        msession = meta.Session()
        if isinstance(vcs_type, (int, long)):
            vcs_type = msession.query(VcsType).filter_by(id=vcs_type).first()
        elif isinstance(vcs_type, (str, unicode)):
            vcs_type = msession.query(VcsType).filter_by(vcs_typename=vcs_type).first()
        elif vcs_type == None:
            vcs_type = msession.query(VcsType).all()
        elif isinstance(vcs_type, VcsType):
            pass
        else:
            vcs_type = None
        return vcs_type

    def create_vcstype(self, vcs_typenames, byuser=None):
        """Create vcs_typename  entries for the vcs_typenames specified by,
        `vcs_typenames`
            which can be, a string specifying the vcs_typename name or a list of
            such strings"""
        tlcomp = TimelineComponent(self.compmgr)
        if isinstance(vcs_typenames, (str, unicode)):
            vcs_typenames = [
             vcs_typenames]
        logs = []
        msession = meta.Session()
        with msession.begin(subtransactions=True):
            [ msession.add(VcsType(unicode(t))) for t in vcs_typenames ]
        tlcomp.log(byuser, 'added version control types, `%s`' % (', ').join(vcs_typenames))

    def create_vcs(self, project, vcsdetail, byuser=None):
        """Create a new vcs based on,
        `project` can be,
            `id` or `projectname` or `Project` instance
        `vcsdetail` which is a tuple of,
            ( type, name, rooturl, loginname, password )
            type can be `id` or `vcs_typename`
        Return,
            Vcs instance."""
        config = self.compmgr.config
        userscomp = config['userscomp']
        prjcomp = ProjectComponent(self.compmgr)
        tlcomp = TimelineComponent(self.compmgr)
        project = prjcomp.get_project(project)
        vcs_type = self.get_vcstype(vcsdetail[0])
        msession = meta.Session()
        with msession.begin(subtransactions=True):
            (type, name, rooturl, loginname, password) = vcsdetail
            vcs = Vcs(name, rooturl, loginname, password)
            vcs_type and setattr(vcs, 'type', vcs_type)
            project.vcslist.append(vcs)
            msession.add(vcs)
            msession.flush()
        tlcomp.log(byuser, 'added project repository, `%s`' % vcs.name, vcs=vcs)
        return vcs

    def delete_vcs(self, vcs, byuser=None):
        """Delete the vcs entry identified by,
        `vcs` which can be,
            `id` or `Vcs` instance"""
        config = self.compmgr.config
        userscomp = config['userscomp']
        prjcomp = ProjectComponent(self.compmgr)
        tlcomp = TimelineComponent(self.compmgr)
        vcs = self.get_vcs(vcs)
        project = vcs.project
        name = vcs.name
        msession = meta.Session()
        with msession.begin(subtransactions=True):
            log = 'deleted project repository, `%s`' % vcs.name
            msession.delete(vcs)
        tlcomp.log(byuser, log, project=project)

    def config_vcs(self, vcs, name=None, type=None, rooturl=None, loginname=None, password=None, byuser=None):
        """For the vcs identified by,
        `vcs` which can be,
            `id` or `Vcs` instance
        """
        config = self.compmgr.config
        userscomp = config['userscomp']
        attrs = ['name', 'type', 'rooturl', 'loginname', 'password']
        prjcomp = ProjectComponent(self.compmgr)
        tlcomp = TimelineComponent(self.compmgr)
        vcs = self.get_vcs(vcs, attrload=['project'])
        loglines = [
         (
          'name', vcs.name, name),
         (
          'type', vcs.type.vcs_typename, type),
         (
          'rooturl', vcs.rooturl, rooturl)]
        log = h.logfor(loglines)
        if log:
            log = 'changed attributes,\n%s' % log
        localvars = locals()
        type = type and self.get_vcstype(type) or None
        msession = meta.Session()
        localvars = locals()
        with msession.begin(subtransactions=True):
            [ setattr(vcs, attr, localvars[attr]) for attr in attrs if localvars[attr] ]
        log and tlcomp.log(byuser, log, vcs=vcs)
        return

    def get_vcs(self, vcs=None, attrload=[], attrload_all=[]):
        """Get the Vcs instance corresponding to the vcs entry identified by,
        `vcs` can be,
            `id` or `Vcs` instance

        Return,
            A Vcs instance. or
            List of Vcs instances."""
        msession = meta.Session()
        if isinstance(vcs, Vcs) and attrload == [] and attrload_all == []:
            return vcs
        else:
            if isinstance(vcs, (int, long)):
                q = msession.query(Vcs).filter_by(id=vcs)
            elif isinstance(vcs, Vcs):
                q = msession.query(Vcs).filter_by(id=vcs.id)
            else:
                q = None
            if q != None:
                q = q.options(*[ eagerload_all(e) for e in attrload_all ])
                q = q.options(*[ eagerload(e) for e in attrload ])
                vcs = q.first()
            elif vcs == None:
                q = msession.query(Vcs)
                q = q.options(*[ eagerload_all(e) for e in attrload_all ])
                q = q.options(*[ eagerload(e) for e in attrload ])
                vcs = q.all()
            else:
                vcs = None
            return vcs

    def get_mount(self, mount=None, attrload=[], attrload_all=[]):
        """Get the VcsMount instance corresponding to the mount entry identified
        by,
        `mount` which can be,
            `id` or `VcsMount` instance

        Return,
            A VcsMount instance. or
            List of VcsMount instances."""
        msession = meta.Session()
        if isinstance(mount, VcsMount) and attrload == [] and attrload_all == []:
            return mount
        else:
            if isinstance(mount, (int, long)):
                q = msession.query(VcsMount).filter_by(id=mount)
            elif isinstance(mount, VcsMount):
                q = msession.query(VcsMount).filter_by(id=mount.id)
            else:
                q = None
            if q != None:
                q = q.options(*[ eagerload_all(e) for e in attrload_all ])
                q = q.options(*[ eagerload(e) for e in attrload ])
                mount = q.first()
            elif mount == None:
                q = msession.query(VcsMount)
                q = q.options(*[ eagerload_all(e) for e in attrload_all ])
                q = q.options(*[ eagerload(e) for e in attrload ])
                mount = q.all()
            else:
                mount = None
            return mount

    def create_mount(self, vcs, name, repospath, content='html', byuser=None):
        """Create a mount point for repository directory"""
        tlcomp = TimelineComponent(self.compmgr)
        vcs = self.get_vcs(vcs, attrload=['project'])
        msession = meta.Session()
        with msession.begin(subtransactions=True):
            vmount = VcsMount(name, repospath, content)
            vmount.vcs = vcs
            msession.add(vmount)
            msession.flush()
        tlcomp.log(byuser, 'Mounted directory `%s` onto mount point %s' % (
         repospath, name), project=vcs.project)
        return vmount

    def update_mount(self, mount, name=None, repospath=None, content=None, byuser=None):
        """Update already created mount"""
        tlcomp = TimelineComponent(self.compmgr)
        mount = self.get_mount(mount, attrload_all=['vcs.project'])
        logs = []
        msession = meta.Session()
        with msession.begin(subtransactions=True):
            if name:
                mount.name = name
                logs.append('name : %s' % name)
            if repospath:
                mount.repospath = repospath
                logs.append('repospath : %s' % repospath)
            if content:
                mount.content = content
                logs.append('content : %s' % content)
        if logs and mount:
            logs = [
             'Updated repository mount, %s' % mount.name] + logs
            log = ('\n').join(logs)
            tlcomp.log(byuser, log, project=mount.vcs.project)

    def delete_mount(self, mount, byuser=None):
        """Delete mount point identified by,
        `mount` which can be,
            `id` or `VcsMount` instance"""
        tlcomp = TimelineComponent(self.compmgr)
        mount = self.get_mount(mount, attrload_all=['vcs.project'])
        msession = meta.Session()
        with msession.begin(subtransactions=True):
            if mount:
                project = mount.vcs.project
                name = mount.name
                msession.delete(mount)
        mount and tlcomp.log(byuser, 'Deleted mount point %s' % name, project=project)

    def projmounts(self, project):
        """Collect all the mount definitions for `project`"""
        oj = t_vcsmount.outerjoin(t_vcs).outerjoin(at_vcs_projects, t_vcs.c.id == at_vcs_projects.c.vscid).outerjoin(t_project, t_project.c.id == at_vcs_projects.c.projectid)
        q = select([t_vcsmount.c.id, t_vcsmount.c.name, t_vcsmount.c.content,
         t_vcsmount.c.repospath, t_vcsmount.c.created_on,
         t_vcs.c.id, t_vcs.c.name, t_vcs.c.rooturl], bind=meta.engine).select_from(oj)
        if isinstance(project, (int, long)):
            q = q.where(t_project.c.id == project)
        elif isinstance(project, (str, unicode)):
            q = q.where(t_project.c.projectname == project)
        elif isinstance(project, Project):
            q = q.where(t_project.c.id == project.id)
        res = q.execute().fetchall()
        return res

    def _vcstypenames(self):
        return [ vt.vcs_typename for vt in self.get_vcstype() ]

    vcstypenames = property(_vcstypenames)
    mountcontents = ['html', 'wiki', 'text']