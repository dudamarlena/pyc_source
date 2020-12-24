# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/gazest/controllers/wiki.py
# Compiled at: 2007-10-26 12:27:12
import logging
from gazest.lib.base import *
from gazest.lib import markup
from gazest.lib.wiki_util import *
from gazest.lib.formutil import IntListValidator
from gazest.lib import dag
from tempfile import NamedTemporaryFile
from datetime import datetime
import formencode, os
log = logging.getLogger(__name__)
MERGE_CMD = "diff3 -m -L 'your version' %s -L original %s -L 'concurrent version' %s"
CONFLICT_MSG = "Some conflict were detected and you'll have to merge them manually.  Good luck!"
MARKERS = [
 '<<<<<<<', '|||||||', '=======', '>>>>>>>']

class WikiPageForm(formencode.Schema):
    __module__ = __name__
    allow_extra_fields = True
    parent_ids = IntListValidator()
    body = formencode.validators.UnicodeString()
    comment = formencode.validators.UnicodeString(strip=True)


class AbuseReportForm(formencode.Schema):
    __module__ = __name__
    allow_extra_fields = True
    comment = formencode.validators.OneOf(model.ABUSE_TYPES)
    comment = formencode.validators.UnicodeString(strip=True)


def merge_revs(a, b):
    """ 3-way merge with GNU diff3 """
    lca = dag.get_lca(a, b)
    temps = []
    for rev in (a, lca, b):
        temps.append(NamedTemporaryFile())
        temps[(-1)].write(rev.body.encode('utf-8'))
        temps[(-1)].file.flush()

    names = tuple([ f.name for f in temps ])
    pipe = os.popen(MERGE_CMD % names)
    merge = unicode(pipe.read(), 'utf-8')
    error = pipe.close()
    if error == 127:
        raise Exception('diff3 is not installed')
    return (
     error, merge)


def has_conflict(body):
    for mrk in MARKERS:
        if body.find(mrk) != -1:
            return True

    return False


def get_rev(slug, for_edit=False):
    page = model.Page.query.selectfirst_by(slug=slug)
    if page:
        rev = page.rev
    else:
        ns_slug = get_namespace(slug)
        namespace = model.Namespace.query.selectfirst_by(slug=ns_slug)
        if not namespace:
            log.info("no page found for '%s'" % slug)
            abort(404)
        if for_edit:
            rev = namespace.stub_rev
        else:
            rev = namespace.not_found_rev
    return (
     page, rev)


class WikiController(BaseController):
    __module__ = __name__

    def __before__(self):
        actions = [('Page', 'wiki', 'view'), ('Edit', 'wiki', 'edit_form'), ('History', 'wiki', 'diff_form')]
        c.nav3_actions += actions

    def _get_method_args(self):
        args = BaseController._get_method_args(self)
        if args.has_key('slug'):
            args['slug'] = normalize_slug(args['slug'])
        return args

    def index(self):
        slug = config['wiki_index']
        c.routes_dict['slug'] = slug
        return self.view(slug)

    def about(self):
        slug = config['wiki_about']
        c.routes_dict['slug'] = slug
        return self.view(slug)

    def random_page(self):
        slug_col = model.RevNode.c.slug
        page = model.RevNode.query.selectfirst(slug_col != '', order_by=model.func.random())
        c.routes_dict['slug'] = page.slug
        return self.view(page.slug)

    def view(self, slug):
        (page, rev) = get_rev(slug)
        delay = config['wiki_indexing_delay']
        if rev.creat_date + delay > datetime.utcnow():
            c.noindex = True
        (page, c.body) = markup.render_page(rev.body, slug)
        c.title = page.title
        return render('/wiki_view.mako')

    def edit_form(self, slug):
        (page, rev) = get_rev(slug, True)
        c.body = rev.body
        if page:
            c.parent_ids = [
             rev.id]
        else:
            c.comment = 'Page creation'
        return render('/wiki_edit_form.mako')

    @validate(schema=WikiPageForm(), form='edit_form')
    def edit_action(self, slug):
        c.title = 'Editing %s' % slug
        msgs = []
        conflict = has_conflict(self.form_result['body'])
        page = model.Page.query.selectfirst_by(slug=slug)
        rev = model.RevNode(body=self.form_result['body'], comment=self.form_result['comment'], slug=slug, user=h.get_remote_user())
        if not page:
            ns_slug = get_namespace(slug)
            ns = model.Namespace.query.selectfirst_by(slug=ns_slug)
            page = model.Page(slug=slug, namespace=ns)
        pre_rev = page.rev
        c.parent_ids = self.form_result['parent_ids']
        for rev_id in c.parent_ids:
            rev.add_parent(model.RevNode.query.get(rev_id))

        if not c.parent_ids:
            if pre_rev:
                log.debug('concurent creation of %s' % slug)
                rev.add_parent(pre_rev)
                msgs.append('This page was created by someone else while you were editing.  Your version takes precedence but you can acces the other version from this history tab.')
        elif conflict:
            pass
        elif pre_rev.id in c.parent_ids:
            pass
        else:
            (conflict, merge) = merge_revs(rev, pre_rev)
            msgs.append('Someone modified this page while you were editing.')
            if not conflict:
                msgs.append('The changes were merged without conflicts but keep an eye open for possible errors.')
            rev.body = merge
            c.body = merge
            if len(c.parent_ids) > 1:
                rev.del_parent(rev.parents()[(-1)])
            rev.add_parent(pre_rev)
            c.parent_ids = [ r.id for r in rev.parents() ]
        page.rev = rev
        if conflict:
            h.m_warn(CONFLICT_MSG)
            c.body = rev.body
            c.comment = rev.comment
            c.m_warn += msgs
            return render('/wiki_edit_form.mako')
        elif self.form_result.has_key('save'):
            model.full_commit()
            map(h.q_info, msgs)
            return h.redirect_to(action='view')
        elif self.form_result.has_key('preview'):
            c.m_info.append("This is only a preview; don't forget to save.")
            (page, c.preview) = markup.render_page(rev.body, slug)
            c.title = 'Edit preview'
            c.body = rev.body
            c.comment = rev.comment
            c.m_info += msgs
            return render('/wiki_edit_form.mako')
        else:
            raise ValueError('No action specified.')

    def diff_form(self, slug):
        c.noindex = True
        (page, rev) = get_rev(slug)
        c.rows = dag.html_layout(rev)
        return render('/wiki_diff_form.mako')

    def revision_diff(self, slug, to_id, from_id):
        c.noindex = True
        c.title = 'Revision diff'
        to_rev = model.RevNode.query.get(to_id)
        if from_id:
            from_rev = model.RevNode.query.get(from_id)
        else:
            from_rev = to_rev.parents()[(-1)]
        c.from_rev = from_rev
        c.to_rev = to_rev
        return render('/wiki_revision_diff.mako')

    def past_revision(self, slug, rev_id):
        c.noindex = True
        c.m_info.append('This is a past revision; it might differ from the current page.')
        rev = model.RevNode.query.get(rev_id)
        (page, c.body) = markup.render_page(rev.body, slug)
        c.title = page.title
        return render('/wiki_view.mako')

    def recent_changes(self):
        c.noindex = True
        c.title = 'Recent changes'
        c.nav3_actions = []
        slug_col = model.RevNode.c.slug
        date_col = model.desc(model.RevNode.c.creat_date)
        c.revs = model.RevNode.query.select(slug_col != '', order_by=date_col, limit=50)

        def group(elems, key_funct):
            """ Return a list of [key, elems] pairs """
            groups = {}
            keys = []
            last_elem = None
            for elem in elems:
                key = key_funct(elem)
                if not groups.has_key(key):
                    keys.append(key)
                    groups[key] = []
                groups[key].append(elem)

            return [ [key, groups[key]] for key in keys ]

        c.groups = [ (date, group(revs, lambda r: r.slug)) for (date, revs) in group(c.revs, lambda r: r.creat_date.date())
                   ]
        return render('/wiki_recent_changes.mako')

    def undo_revision(self, slug, rev_id):
        c.noindex = True
        page = model.Page.query.selectfirst_by(slug=slug)
        badrev = model.RevNode.query.get(rev_id)
        oldtip = badrev.parents()[(-1)]
        conflict = False
        c.comment = 'Revert'
        editrev = model.RevNode(body=oldtip.body, comment=c.comment, user=h.get_remote_user())
        editrev.add_parent(badrev)
        if page.rev.id == badrev.id:
            pass
        else:
            (conflict, merge) = merge_revs(editrev, page.rev)
            editrev.add_parent(page.rev)
            editrev.body = merge
            if conflict:
                h.m_warn(CONFLICT_MSG)
        c.show_diff_highlight = not conflict
        h.m_info('You are about to undo an edit. Please review the changes before you save.')
        c.parent_ids = [ r.id for r in editrev.parents() ]
        c.body = editrev.body
        c.editrev = editrev
        c.page = page
        return render('/wiki_edit_form.mako')

    def page_atom(self, slug):
        c.page = model.Page.query.selectfirst_by(slug=slug)
        slug_col = model.RevNode.c.slug
        date_col = model.desc(model.RevNode.c.creat_date)
        c.revs = model.RevNode.query.select(slug_col == slug, order_by=date_col, limit=50)
        ctype = 'application/atom+xml; charset=utf-8'
        response.headers['Content-Type'] = ctype
        return render('/wiki_page_atom.mako')

    def site_atom(self):
        slug_col = model.RevNode.c.slug
        date_col = model.desc(model.RevNode.c.creat_date)
        c.revs = model.RevNode.query.select(slug_col != '', order_by=date_col, limit=50)
        ctype = 'application/atom+xml; charset=utf-8'
        response.headers['Content-Type'] = ctype
        return render('/wiki_site_atom.mako')

    def abuse_report_form(self, slug, rev_id):
        c.rev = model.RevNode.get(rev_id)
        return render('/wiki_abuse_report_form.mako')

    @validate(schema=AbuseReportForm(), form='abuse_report_form')
    def abuse_report_action(self, slug, rev_id):
        rev = model.RevNode.get(rev_id)
        report = model.AbuseReport(rev=rev, reporter=h.get_remote_user(), comment=self.form_result['comment'], problem=self.form_result['problem'])
        model.full_commit()
        h.q_info("Thank you for brining this to our attention. We'll review your report and take due actions shortly. In the mean time, feel free to undo offensive edits by yourself.")
        return h.redirect_to(action='view')