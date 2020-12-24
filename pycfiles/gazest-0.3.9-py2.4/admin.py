# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/gazest/controllers/admin.py
# Compiled at: 2007-10-25 12:41:27
import logging
from gazest.lib.base import *
from authkit.pylons_adaptors import authorize
from gazest.lib.auth_util import HasRank
from gazest.lib.formutil import CIDRValidator
from datetime import datetime, timedelta
import formencode
log = logging.getLogger(__name__)

class BoycottForm(formencode.Schema):
    __module__ = __name__
    allow_extra_fields = True
    range_cidr = CIDRValidator()
    nb_days = formencode.validators.Number()
    reason = formencode.validators.UnicodeString(strip=True)


class AdminController(BaseController):
    __module__ = __name__

    def __before__(self, action, **kw):
        c.noindex = True

    @authorize(HasRank('thaumaturge'))
    def abuse_log(self):
        date_col = model.AbuseReport.c.creat_date
        reports = model.AbuseReport.query.select(order_by=date_col, limit=200)
        abuse_h = {}
        revs = []
        for report in reports:
            rev_id = report.rev.id
            if not abuse_h.has_key(rev_id):
                abuse_h[rev_id] = 0
                revs.append(report.rev)
            abuse_h[rev_id] += 1

        revs.sort(lambda a, b: a.creat_date < b.creat_date)
        c.rev_rep_pairs = [ (r, abuse_h[r.id]) for r in revs ]
        return render('/wiki_abuse_log.mako')

    @authorize(HasRank('thaumaturge'))
    def boycott_form(self, addr=None):
        if addr:
            c.range_cidr = '%s/32' % addr
        c.nb_days = 2
        return render('/admin_boycott_form.mako')

    @authorize(HasRank('thaumaturge'))
    @validate(schema=BoycottForm(), form='boycott_form')
    def boycott_action(self):
        cidr = self.form_result['range_cidr']
        days = self.form_result['nb_days']
        now = datetime.utcnow()
        delay = timedelta(days=days)
        boycott = model.Boycott(reason=self.form_result['reason'], range_cidr=str(cidr), range_start=int(cidr.first_ip.get_dec()), range_stop=int(cidr.last_ip.get_dec()), expiration_date=now + delay, instigator=h.get_remote_user())
        model.full_commit()
        h.q_info('Boycotting %s IP addresses for %s days' % (len(cidr), days))
        return h.redirect_to(action='abuse_log')