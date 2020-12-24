# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/zeta/lib/analytics.py
# Compiled at: 2010-06-16 04:31:38
"""Analytics library, to do data crunching and save them in disk-cache"""
import zeta.lib.helpers as h
cache_namespace = 'zeta_analytics_store'

class Analytics(object):
    """Analytics object"""
    cache_key = ''

    def __init__(self):
        pass

    def analyse(self, *args, **kwargs):
        """Compute the analytics. To be implemented by the deriving class"""
        pass

    def cacheme(self):
        """Cache `self` object. Remove the cache object on disk and store it
        once again"""
        dofunc = lambda : self
        cachemgr = h.fromconfig('cachemgr')
        cachenm = cachemgr.get_cache(cache_namespace)
        cachenm.remove_value(key=self.cache_key)
        return cachenm.get(key=self.cache_key, createfunc=dofunc)


class TagAnalytics(Analytics):
    cache_key = 'tags'

    def do_chart1(self, tags):
        """Compute data for chart1
        chart1_data,
            { tagname : [ [ 'attachments', count ],
                          [ 'licenses', count ],
                        ],
              ...
            }
        chart1_rtags,
            { tagname : [ [ reltagname, percent-related ],
                          ....,
                        ],
              ...
            }
        """
        attrs = [
         'attachments', 'licenses', 'projects', 'tickets', 'reviews',
         'wikipages']
        chart1_data = dict([ (tag.tagname, [ [attr, len(getattr(tag, attr, []))] for attr in attrs ]) for tag in tags
                           ])
        chart1_rtags = {}
        for tag in tags:
            reltags = []
            [ reltags.extend(i.tags) for a in attrs for i in getattr(tag, a) ]
            dtags = h.computecount(reltags, lambda x: x.tagname)
            vals = dtags.values()
            maxt = float(vals and max(vals) or 1)
            perct = sorted([ [tagname, int(count / maxt * 100)] for (tagname, count) in dtags.iteritems() if tagname != tag.tagname
                           ], key=lambda x: x[0])
            chart1_rtags.setdefault(tag.tagname, perct)

        return (
         chart1_data, chart1_rtags)

    def do_chart4(self, tags):
        """Compute chart for attachment Vs tags
        chart4_data,
            [ tagname, [ [ attach.id, attach.filename ], ... ] ... ],
        """
        chart4_data = sorted([ [tag.tagname, [ [a.id, a.filename] for a in tag.attachments ]] for tag in tags if tag.attachments
                             ], key=lambda x: x[0])
        chart4_tags = map(lambda x: x[0], chart4_data)
        return (chart4_data, chart4_tags)

    def do_chart7(self, tags):
        """Compute chart for license Vs tags
        chart7_data,
            [ tagname, [ [ license.id, license.licensename ], ... ] ... ],
        """
        chart7_data = sorted([ [tag.tagname, [ [l.id, l.licensename] for l in tag.licenses ]] for tag in tags if tag.licenses
                             ], key=lambda x: x[0])
        chart7_tags = map(lambda x: x[0], chart7_data)
        return (chart7_data, chart7_tags)

    def do_chart20(self, tags):
        """Compute chart for wiki Vs tags
        chart20_data,
        { project: [ tagname, [ [ wiki.id, wiki.wikiurl ], ... ] ... ],
          ...
        }
        chart20_tags,
        { project: [ tagname, ...],
          ...
        }
        """
        data = {}
        for tag in tags:
            for w in tag.wikipages:
                data.setdefault(w.project.id, {}).setdefault(tag.tagname, []).append([
                 w.id, h.wiki_parseurl(w.wikiurl), w.wikiurl])

        data = dict([ (p,
         sorted([ [k, v] for (k, v) in data[p].iteritems() ], key=lambda x: x[0]))
         for p in data
                    ])
        chart20_data = data
        chart20_tags = {}
        for (p, tlist) in chart20_data.iteritems():
            chart20_tags[p] = sorted(map(lambda x: x[0], tlist))

        return (
         chart20_data, chart20_tags)

    def analyse(self):
        from zeta.comp.tag import TagComponent
        compmgr = h.fromconfig('compmgr')
        tagcomp = TagComponent(compmgr)
        tags = tagcomp.get_tag(attrload=[
         'attachments', 'licenses', 'projects',
         'tickets', 'reviews', 'wikipages'])
        (self.chart1_data, self.chart1_rtags) = self.do_chart1(tags)
        (self.chart4_data, self.chart4_tags) = self.do_chart4(tags)
        (self.chart7_data, self.chart7_tags) = self.do_chart7(tags)
        (self.chart20_data, self.chart20_tags) = self.do_chart20(tags)


class AttachAnalytics(Analytics):
    cache_key = 'attachs'

    def _asscanalytics(self, attcomp):
        """Compute attachments to user, license, project, ticket, wiki,
        review, etc ... and save the association"""
        return attcomp.attachassc()

    def do_chart2(self, attachs):
        """Compute chart relating files and its uploaders
        chart2_data,
            [ [ username, totalfiles, totalpayload ],
              ...
            ]
        chart2_fcnt
            Integer - no. of attachments
        chart2_payld
            Integet - Total payload 
        """
        filelen = lambda a: a.content and len(a.content) or 0
        userfiles = []
        userpayld = {}
        chart2_payld = 0
        for a in attachs:
            uploader = a.uploader.username
            userfiles.append(uploader)
            userpayld.setdefault(uploader, []).append(filelen(a))
            chart2_payld += filelen(a)

        userfiles = h.computecount(userfiles, lambda x: x)
        chart2_data = sorted([ [u, userfiles.get(u, 0), sum(userpayld.get(u, []))] for u in userfiles
                             ], key=lambda x: x[0])
        chart2_fcnt = len(attachs)
        return (chart2_data, chart2_fcnt, chart2_payld)

    def do_chart3(self, attachs):
        """Compute chart tracking file's download count
        chart3_data,
            [ [ attach.id attach.filename, downloads ],
              ...
            ]
        """
        chart3_data = sorted([ [a.id, a.filename, a.download_count] for a in attachs ], key=lambda x: x[1])
        return chart3_data

    def do_chart5(self, attachs):
        """Compute the 
        chart5_data,
            [ [ [ attach.id attach.filename, attach.created_on.ctime(),
                  attach.created_on ], ...
              ],
              ...
            ]
        """
        uploadtline = [ [a.id, a.filename, a.created_on] for a in attachs ]
        uploadtline = sorted(uploadtline, key=lambda x: x[2])
        maxdays = (uploadtline[(-1)][2] - uploadtline[0][2]).days
        data = [ [] for i in range(maxdays + 1) ]
        for v in uploadtline:
            data[(v[2] - uploadtline[0][2]).days].append([
             v[0], v[1], v[2].ctime(), v[2]])

        chart5_data = [ map(lambda x: x[:4], logs) for logs in data if logs ]
        return chart5_data

    def analyse(self):
        from zeta.comp.attach import AttachComponent
        compmgr = h.fromconfig('compmgr')
        attcomp = AttachComponent(compmgr)
        attachs = attcomp.get_attach(attrload=['uploader', 'tags'])
        self.attachassc = self._asscanalytics(attcomp)
        (self.chart2_data, self.chart2_fcnt, self.chart2_payld) = self.do_chart2(attachs)
        self.chart3_data = self.do_chart3(attachs)
        self.chart5_data = self.do_chart5(attachs)


class UserAnalytics(Analytics):
    cache_key = 'users'

    def do_chart8(self, users):
        """Compute user activity for all registered users,
        chart8_data,
        [ [ user.id, user.username, updatecount ],
          ...
        ]
        """
        chart8_data = sorted([ [u.id, u.username, len(u.logs)] for u in users ], key=lambda x: x[1])
        return chart8_data

    def do_chart9(self, userscomp, users):
        """Compute site permissions for registered users,
        chart9_data,
        [ [ user.id, user.username, permname-list, permnames_x-list ],
          ...
        ]"""
        pmap = userscomp.mapfor_usersite()
        pnames = userscomp.site_permnames
        pmap['admin'] = pnames
        chart9_data = sorted([ [u.id, u.username, list(set(pnames).intersection(pmap.get(u.username, []))), list(set(pnames).difference(pmap.get(u.username, [])))] for u in users
                             ], key=lambda x: x[1])
        return chart9_data

    def do_chart10(self, users):
        """Compute projects administered by registered users,
        chart10_data,
        [ [ user.id, user.username, project-list ],
          ...
        ]"""
        data = [ [u.id, u.username, sorted([ p.projectname for p in u.adminprojects ])] for u in users
               ]
        chart10_data = sorted(filter(lambda x: x[2], data), key=lambda x: x[2])
        return chart10_data

    def do_chart11(self, users, projcomp):
        """Compute components owned by users,
        chart11_data,
        [ [ user.id, user.username, component-list ],
          ...
        ] """
        data = [ [u.id, u.username, sorted([ comp.componentname for comp in u.owncomponents ])] for u in users
               ]
        chart11_data = sorted(filter(lambda x: x[2], data), key=lambda x: x[2])
        chart11_ccnt = len(projcomp.get_component())
        return (chart11_data, chart11_ccnt)

    def do_chart12(self, users):
        """Computer user activity across functions,
        chart12_data,
        { user.id : [ user.id, user.username,
                      [ [ 'fnname', count ], ... ] ],
          ...
        }"""
        chart12_data = {}
        for u in users:
            byfn = []
            byprj = []
            for l in u.logs:
                if getattr(l, 'ticket', None):
                    byfn.append('ticket')
                    byprj.append(l.ticket.project.projectname)
                elif getattr(l, 'review', None):
                    byfn.append('review')
                    byprj.append(l.review.project.projectname)
                elif getattr(l, 'vcs', None):
                    byfn.append('vcs')
                    byprj.append(l.vcs.project.projectname)
                elif getattr(l, 'wiki', None):
                    byfn.append('wiki')
                    byprj.append(l.wiki.project.projectname)
                elif getattr(l, 'project', None):
                    byfn.append('project')
                    byprj.append(l.project.projectname)
                else:
                    byfn.append('others')

            chart12_data.setdefault(u.id, [
             u.id, u.username,
             [ [k, v] for (k, v) in h.computecount(byfn, lambda x: x).iteritems()
             ]])

        return chart12_data

    def analyse(self):
        from zeta.comp.project import ProjectComponent
        compmgr = h.fromconfig('compmgr')
        userscomp = h.fromconfig('userscomp')
        projcomp = ProjectComponent(compmgr)
        users = userscomp.get_user(attrload=[
         'adminprojects', 'owncomponents'])
        self.id2name = dict([ (u.id, u.username) for u in users ])
        self.name2id = dict([ (u.username, u.id) for u in users ])
        self.chart8_data = self.do_chart8(users)
        self.chart9_data = self.do_chart9(userscomp, users)
        self.chart10_data = self.do_chart10(users)
        (self.chart11_data, self.chart11_ccnt) = self.do_chart11(users, projcomp)
        self.chart12_data = self.do_chart12(users)


class LicenseAnalytics(Analytics):
    cache_key = 'license'

    def do_chart6(self, license):
        """Compute projects under license"""
        chart6_data = [ [l.id, l.licensename, [ p.projectname for p in l.projects ]] for l in license
                      ]
        return chart6_data

    def analyse(self):
        from zeta.comp.license import LicenseComponent
        compmgr = h.fromconfig('compmgr')
        liccomp = LicenseComponent(compmgr)
        license = liccomp.get_license(attrload=['projects'])
        self.id2name = dict([ (l.id, l.licensename) for l in license ])
        self.name2id = dict([ (l.licensename, l.id) for l in license ])
        self.chart6_data = self.do_chart6(license)


class ProjectAnalytics(Analytics):
    cache_key = 'projects'

    def do_chart14(self, projects):
        """Compute project activity based on functions,
        chart14_data,
        { projectname : { review:count, wiki:count, ticket:count,
                          vcs:count, admin:count },
          ...
        }"""
        from zeta.comp.project import ProjectComponent
        from zeta.comp.ticket import TicketComponent
        from zeta.comp.vcs import VcsComponent
        from zeta.comp.review import ReviewComponent
        from zeta.comp.wiki import WikiComponent
        compmgr = h.fromconfig('compmgr')
        projcomp = ProjectComponent(compmgr)
        tckcomp = TicketComponent(compmgr)
        vcscomp = VcsComponent(compmgr)
        revcomp = ReviewComponent(compmgr)
        wikicomp = WikiComponent(compmgr)
        chart14_data = dict([ (p.projectname, {'ticket': 0, 'vcs': 0, 'review': 0, 'wiki': 0, 'admin': 0}) for p in projcomp.get_project()
                            ])
        for t in tckcomp.get_ticket(attrload=['project']):
            d = chart14_data[t.project.projectname]
            d['ticket'] += len(t.logs)

        for v in vcscomp.get_vcs(attrload=['project']):
            d = chart14_data[v.project.projectname]
            d['vcs'] += len(v.logs)

        for r in revcomp.get_review(attrload=['project']):
            d = chart14_data[r.project.projectname]
            d['review'] += len(r.logs)

        for w in wikicomp.get_wiki(attrload=['project']):
            d = chart14_data[w.project.projectname]
            d['wiki'] += len(w.logs)

        for p in projcomp.get_project():
            d = chart14_data[p.projectname]
            d['admin'] += len(p.logs)

        return chart14_data

    def analyse(self):
        from zeta.comp.project import ProjectComponent
        compmgr = h.fromconfig('compmgr')
        projcomp = ProjectComponent(compmgr)
        projects = projcomp.get_project()
        self.id2name = dict([ (p.id, p.projectname) for p in projects ])
        self.name2id = dict([ (p.projectname, p.id) for p in projects ])
        self.chart14_data = self.do_chart14(projects)


class TicketAnalytics(Analytics):
    cache_key = 'tickets'

    def do_chart21(self, tickets, tstatus):
        """Compute pie charts for ticket types, ticket severity and ticket
        status, project wise,
        chart21_data,
        { projectname : [ 
                            [ [ type1, count ], [ type2, count ] .... ],
                            [ [ severity1, count ], [ severity2, count ] .... ],
                            [ [ status1, count ], [ status2, count ] .... ],
                        ],
          ...
        }"""
        data = {}
        for t in tickets:
            ts = tstatus.get(t.tsh_id)
            data.setdefault(t.project.id, []).append([
             t.type.tck_typename, t.severity.tck_severityname,
             ts.status.tck_statusname])

        chart21_data = {}
        for (p, vals) in data.iteritems():
            chart21_data[p] = [
             sorted(list(h.computecount(vals, lambda x: x[0]).items()), key=lambda x: x[0]),
             sorted(list(h.computecount(vals, lambda x: x[1]).items()), key=lambda x: x[0]),
             sorted(list(h.computecount(vals, lambda x: x[2]).items()), key=lambda x: x[0])]

        return chart21_data

    def do_chart22(self, tickets):
        """Compute pie charts for project user's
            ticket types, ticket severity and ticket status
        chart22_data,
        { projectname : [ [ username,
                            [ [ type1, count ], [ type2, count ] .... ],
                            [ [ severity1, count ], [ severity2, count ] .... ],
                            [ [ status1, count ], [ status2, count ] .... ],
                          ],
                          ...
                        ],
          ...
        }"""
        data = {}
        for t in tickets:
            ts = t.statushistory[(-1)]
            data.setdefault(t.project.id, {}).setdefault(ts.owner.username, []).append([
             t.type.tck_typename, t.severity.tck_severityname,
             ts.status.tck_statusname])

        chart22_data = {}
        for (p, udict) in data.iteritems():
            chart22_data[p] = []
            for (u, vals) in udict.iteritems():
                chart22_data[p].append([
                 u,
                 sorted(list(h.computecount(vals, lambda x: x[0]).items()), key=lambda x: x[0]),
                 sorted(list(h.computecount(vals, lambda x: x[1]).items()), key=lambda x: x[0]),
                 sorted(list(h.computecount(vals, lambda x: x[2]).items()), key=lambda x: x[0])])

        chart22_usrs = dict([ (p,
         [ [u, h.url_foruser(u)] for u in map(lambda x: x[0], vals)
         ])
         for (p, vals) in chart22_data.iteritems()
                            ])
        return (chart22_data, chart22_usrs)

    def do_chart23(self, tickets):
        """Compute pie charts for components, 
                ticket types, ticket severity and ticket status
        chart23_data,
        { projectname : [ [ componentname,
                            [ [ type1, count ], [ type2, count ] .... ],
                            [ [ severity1, count ], [ severity2, count ] .... ],
                            [ [ status1, count ], [ status2, count ] .... ],
                          ],
                          ...
                        ],
          ...
        }"""
        data = {}
        for t in tickets:
            if not t.components:
                continue
            ts = t.statushistory[(-1)]
            data.setdefault(t.project.id, {}).setdefault(t.components[0].componentname, []).append([
             t.type.tck_typename, t.severity.tck_severityname,
             ts.status.tck_statusname])

        chart23_data = {}
        for (p, cdict) in data.iteritems():
            chart23_data[p] = []
            for (comp, vals) in cdict.iteritems():
                chart23_data[p].append([
                 comp,
                 sorted(list(h.computecount(vals, lambda x: x[0]).items()), key=lambda x: x[0]),
                 sorted(list(h.computecount(vals, lambda x: x[1]).items()), key=lambda x: x[0]),
                 sorted(list(h.computecount(vals, lambda x: x[2]).items()), key=lambda x: x[0])])

        return chart23_data

    def do_chart24(self, tickets):
        """Compute pie charts for milestones, 
                ticket types, ticket severity and ticket status
        chart24_data,
        { projectname : [ [ milestone_name,
                            [ [ type1, count ], [ type2, count ] .... ],
                            [ [ severity1, count ], [ severity2, count ] .... ],
                            [ [ status1, count ], [ status2, count ] .... ],
                          ],
                          ...
                        ],
          ...
        }"""
        data = {}
        for t in tickets:
            if not t.milestones:
                continue
            ts = t.statushistory[(-1)]
            data.setdefault(t.project.id, {}).setdefault(t.milestones[0].milestone_name, []).append([
             t.type.tck_typename, t.severity.tck_severityname,
             ts.status.tck_statusname])

        chart24_data = {}
        for (p, mdict) in data.iteritems():
            chart24_data[p] = []
            for (mstn, vals) in mdict.iteritems():
                chart24_data[p].append([
                 mstn,
                 sorted(list(h.computecount(vals, lambda x: x[0]).items()), key=lambda x: x[0]),
                 sorted(list(h.computecount(vals, lambda x: x[1]).items()), key=lambda x: x[0]),
                 sorted(list(h.computecount(vals, lambda x: x[2]).items()), key=lambda x: x[0])])

        return chart24_data

    def do_chart25(self, tickets):
        """Compute pie charts for versions, 
                ticket types, ticket severity and ticket status
        chart25_data,
        { projectname : [ [ version_name,
                            [ [ type1, count ], [ type2, count ] .... ],
                            [ [ severity1, count ], [ severity2, count ] .... ],
                            [ [ status1, count ], [ status2, count ] .... ],
                          ],
                          ...
                        ],
          ...
        }"""
        data = {}
        for t in tickets:
            ts = t.statushistory[(-1)]
            if not t.versions:
                continue
            data.setdefault(t.project.id, {}).setdefault(t.versions[0].version_name, []).append([
             t.type.tck_typename, t.severity.tck_severityname,
             ts.status.tck_statusname])

        chart25_data = {}
        for (p, vdict) in data.iteritems():
            chart25_data[p] = []
            for (ver, vals) in vdict.iteritems():
                chart25_data[p].append([
                 ver,
                 sorted(h.computecount(vals, lambda x: x[0]).items(), key=lambda x: x[0]),
                 sorted(h.computecount(vals, lambda x: x[1]).items(), key=lambda x: x[0]),
                 sorted(h.computecount(vals, lambda x: x[2]).items(), key=lambda x: x[0])])

        return chart25_data

    def do_chart26(self, tickets):
        """Compute wiki commentors, projectwise
        chart26_data,
        { project.id : [ [ t.id, [ [commentor, count], ... ] ]
                         ...
                       ],
          ...
        }
        """
        tdets = []
        allcmtrs = {}
        for t in tickets:
            cmtrs = h.computecount(t.comments, lambda x: x.commentby.username)
            allcmtrs.setdefault(t.project.id, []).extend(cmtrs.keys())
            tdets.append([t.project.id, t.id, cmtrs])

        allcmtrs = dict([ (p, sorted(set(allcmtrs[p]))) for p in allcmtrs ])
        for t in tdets:
            pid = t[0]
            cmtrs = t[2]
            t[2] = [ [u, cmtrs.get(u, 0)] for u in allcmtrs[pid] ]

        chart26_usrs = dict([ (pid, [ [u, h.url_foruser(u)] for u in users ]) for (pid, users) in allcmtrs.iteritems()
                            ])
        chart26_data = {}
        [ chart26_data.setdefault(t[0], []).append(t[1:]) for t in tdets ]
        return (chart26_data, chart26_usrs)

    def do_tdets(self, tickets):
        tdets = dict([ (t.id, [t.project.projectname, t.id]) for t in tickets
                     ])
        return tdets

    def analyse(self):
        from zeta.comp.ticket import TicketComponent
        from zeta.comp.project import ProjectComponent
        compmgr = h.fromconfig('compmgr')
        tckcomp = TicketComponent(compmgr)
        projcomp = ProjectComponent(compmgr)
        tickets = tckcomp.get_ticket(attrload=[
         'statushistory', 'type', 'severity',
         'comments'])
        tstatus = dict([ (ts.id, ts) for ts in tckcomp.get_ticket_status(attrload=[
         'status', 'owner'])
                       ])
        self.tdets = self.do_tdets(tickets)
        self.chart21_data = self.do_chart21(tickets, tstatus)
        (self.chart22_data, self.chart22_usrs) = self.do_chart22(tickets)
        self.chart23_data = self.do_chart23(tickets)
        self.chart24_data = self.do_chart24(tickets)
        self.chart25_data = self.do_chart25(tickets)
        (self.chart26_data, self.chart26_usrs) = self.do_chart26(tickets)


class ReviewAnalytics(Analytics):
    cache_key = 'reviews'

    def do_rdets(self, reviews):
        rdets = dict([ (r.id, [r.project.projectname, r.id]) for r in reviews
                     ])
        return rdets

    def do_chart27(self, reviews):
        """Compute wiki commentors, projectwise
        chart26_data,
        { project.id : [ [ [author1, count], ... ],
                         [ [moderator1, count], ... ],
                         [ [participant1, count], ... ],
                       ],
          ...
        }
        """
        data = {}
        usrs = {}
        for r in reviews:
            data.setdefault(r.project.id, {}).setdefault('author', []).append(r.author.username)
            data.setdefault(r.project.id, {}).setdefault('moderator', []).append(r.moderator.username)
            data.setdefault(r.project.id, {}).setdefault('participant', []).extend([ partc.username for partc in r.participants ])
            usrs.setdefault(r.project.id, []).append(r.author.username)
            usrs.setdefault(r.project.id, []).append(r.moderator.username)
            usrs.setdefault(r.project.id, []).extend([ partc.username for partc in r.participants ])

        chart27_data = {}
        [ chart27_data.setdefault(p, [
         sorted(h.computecount(data[p]['author'], lambda x: x).items(), key=lambda x: x[0]),
         sorted(h.computecount(data[p]['moderator'], lambda x: x).items(), key=lambda x: x[0]),
         sorted(h.computecount(data[p]['participant'], lambda x: x).items(), key=lambda x: x[0])])
         for p in data
        ]
        chart27_usrs = dict([ (p, [ [u, h.url_foruser(u)] for u in set(vals) ]) for (p, vals) in usrs.iteritems()
                            ])
        return (
         chart27_data, chart27_usrs)

    def analyse(self):
        from zeta.comp.review import ReviewComponent
        compmgr = h.fromconfig('compmgr')
        revcomp = ReviewComponent(compmgr)
        reviews = revcomp.get_review()
        self.rdets = self.do_rdets(reviews)
        (self.chart27_data, self.chart27_usrs) = self.do_chart27(reviews)


class WikiAnalytics(Analytics):
    cache_key = 'wiki'

    def do_wdets(self, wikis):
        wdets = dict([ (w.id, [w.project.projectname, h.wiki_parseurl(w.wikiurl)]) for w in wikis
                     ])
        return wdets

    def do_chart16(self, wikis):
        """Compute wiki edits and comments, projectwise
        chart16_data,
        { project.id : [ [ wikipath, versioncount, commentscount ]
                         ...
                       ],
          ...
        }
        """
        wdets = sorted([ [w.project.id, w.wikiurl, h.wiki_parseurl(w.wikiurl), w.latest_version, len(w.comments)] for w in wikis
                       ], key=lambda x: x[2])
        chart16_wiki = {}
        chart16_data = {}
        [ chart16_data.setdefault(w[0], []).append(w[2:]) for w in wdets ]
        [ chart16_wiki.setdefault(w[0], []).append([w[1], w[2]]) for w in wdets ]
        return (
         chart16_data, chart16_wiki)

    def do_chart17(self, wikis):
        """Compute wiki votes, projectwise
        chart1y_data,
        { project.id : [ [ wikipath, upvotes, downvotes ]
                         ...
                       ],
          ...
        }
        """
        wdets = sorted([ [w.project.id, w.wikiurl, h.wiki_parseurl(w.wikiurl), sum([ 1 for v in w.votes if v.votedas == 'up' ]), sum([ 1 for v in w.votes if v.votedas == 'down' ])] for w in wikis
                       ], key=lambda x: x[2])
        chart17_data = {}
        [ chart17_data.setdefault(w[0], []).append(w[2:]) for w in wdets ]
        return chart17_data

    def do_chart18(self, wikicomp, wikis):
        """Compute wiki authors, projectwise
        chart18_data,
        { project.id : [ [ wikipath, [ [author, edits], ... ] ]
                         ...
                       ],
          ...
        }
        """
        wdets = []
        allauthors = {}
        for w in wikis:
            wcnts = wikicomp.get_content(w, all=True)
            authors = h.computecount(wcnts, lambda x: x.author)
            allauthors.setdefault(w.project.id, []).extend(authors.keys())
            wdets.append([w.project.id, h.wiki_parseurl(w.wikiurl), authors])

        allauthors = dict([ (p, sorted(set(allauthors[p]))) for p in allauthors ])
        for w in wdets:
            pid = w[0]
            authors = w[2]
            w[2] = [ [u, authors.get(u, 0)] for u in allauthors[pid] ]

        chart18_usrs = dict([ (pid, [ [u, h.url_foruser(u)] for u in users ]) for (pid, users) in allauthors.iteritems()
                            ])
        chart18_data = {}
        [ chart18_data.setdefault(w[0], []).append(w[1:]) for w in wdets ]
        return (chart18_data, chart18_usrs)

    def do_chart19(self, wikis):
        """Compute wiki commentors, projectwise
        chart19_data,
        { project.id : [ [ wikipath, [ [commentor, count], ... ] ]
                         ...
                       ],
          ...
        }
        """
        wdets = []
        allcmtrs = {}
        for w in wikis:
            cmtrs = h.computecount(w.comments, lambda x: x.commentby.username)
            allcmtrs.setdefault(w.project.id, []).extend(cmtrs.keys())
            wdets.append([w.project.id, h.wiki_parseurl(w.wikiurl), cmtrs])

        allcmtrs = dict([ (p, sorted(set(allcmtrs[p]))) for p in allcmtrs ])
        for w in wdets:
            pid = w[0]
            cmtrs = w[2]
            w[2] = [ [u, cmtrs.get(u, 0)] for u in allcmtrs[pid] ]

        chart19_usrs = dict([ (pid, [ [u, h.url_foruser(u)] for u in users ]) for (pid, users) in allcmtrs.iteritems()
                            ])
        chart19_data = {}
        [ chart19_data.setdefault(w[0], []).append(w[1:]) for w in wdets ]
        return (chart19_data, chart19_usrs)

    def analyse(self):
        from zeta.comp.wiki import WikiComponent
        compmgr = h.fromconfig('compmgr')
        wikicomp = WikiComponent(compmgr)
        wikis = wikicomp.get_wiki(attrload=[
         'project', 'comments', 'votes', 'tags'])
        self.id2url = dict([ (w.id, w.wikiurl) for w in wikis ])
        self.url2id = dict([ (w.wikiurl, w.id) for w in wikis ])
        self.wdets = self.do_wdets(wikis)
        (self.chart16_data, self.chart16_wiki) = self.do_chart16(wikis)
        self.chart17_data = self.do_chart17(wikis)
        (self.chart18_data, self.chart18_usrs) = self.do_chart18(wikicomp, wikis)
        (self.chart19_data, self.chart19_usrs) = self.do_chart19(wikis)


class TimelineAnalytics(Analytics):
    cache_key = 'timeline'

    def _sitetimeline(self, tlcomp):
        """Compute the full timeline for the site"""
        alllogs = tlcomp.fetchlogs([])
        s_vs_c = [ [l.id, l.userhtml, l.itemhtml, l.created_on] for l in alllogs
                 ]
        s_vs_c = sorted(s_vs_c, key=lambda x: x[3])
        maxdays = (s_vs_c[(-1)][3] - s_vs_c[0][3]).days
        data = [ [] for i in range(maxdays + 1) ]
        for l in s_vs_c:
            data[(l[3] - s_vs_c[0][3]).days].append([
             l[0], l[1], l[2], l[3].ctime(), l[3]])

        s_vs_c = data
        return s_vs_c

    def _lictimeline(self, tlcomp):
        """Compute the full timeline for the site"""
        pass

    def _projecttimeline(self, tlcomp):
        """Compute the full timeline for the site"""
        pass

    def analyse(self):
        from zeta.comp.timeline import TimelineComponent
        compmgr = h.fromconfig('compmgr')
        tlcomp = TimelineComponent(compmgr)
        self.s_vs_c = self._sitetimeline(tlcomp)


AnalyticClasses = [
 TagAnalytics, AttachAnalytics, UserAnalytics,
 LicenseAnalytics, ProjectAnalytics, TicketAnalytics,
 ReviewAnalytics, WikiAnalytics, TimelineAnalytics]

def get_analyticobj(key):
    """Get the analytics object of interest"""
    analcls = [ cls for cls in AnalyticClasses if cls.cache_key == key ]
    analcls = analcls and analcls[0] or None
    dofunc = lambda : analcls and analcls()
    cachemgr = h.fromconfig('cachemgr')
    cachenm = cachemgr.get_cache(cache_namespace)
    return cachenm.get(key=key, createfunc=dofunc)