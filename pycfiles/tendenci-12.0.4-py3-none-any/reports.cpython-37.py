# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jennyq/.pyenv/versions/venv_t12/lib/python3.7/site-packages/tendenci/apps/memberships/reports.py
# Compiled at: 2020-02-26 14:47:58
# Size of source mod 2**32: 5396 bytes
from geraldo import Report, ReportBand, ObjectValue, Label, landscape
from reportlab.lib.units import cm
from reportlab.lib.pagesizes import A5
from django.urls import reverse
from django.utils.safestring import mark_safe
import django.utils.translation as _
from tendenci.libs.model_report.report import reports, ReportAdmin
from tendenci.libs.model_report.utils import us_date_format
from tendenci.apps.memberships.models import MembershipDefault, MembershipType
MEMBERSHIPTYPE_DICT = None

class ReportBandNewMems(ReportBand):

    def __init__(self, *args, **kwargs):
        kwargs.pop('days_ago')
        (super(ReportBandNewMems, self).__init__)(*args, **kwargs)


class ReportNewMems(Report):
    title = _('New Memberships')
    author = _('John Smith  Corporation')
    page_size = landscape(A5)

    def __init__(self, *args, **kwargs):
        (super(ReportNewMems, self).__init__)(*args, **kwargs)

    class band_page_header(ReportBand):
        height = 1.2 * cm
        elements = [
         Label(text=(_('Name')), top=(0.8 * cm), left=(0 * cm)),
         Label(text=(_('Email')), top=(0.8 * cm), left=(2.5 * cm)),
         Label(text=(_('Type')), top=(0.8 * cm), left=(5.5 * cm)),
         Label(text=(_('Price Paid')), top=(0.8 * cm), left=(11.5 * cm)),
         Label(text=(_('Start Date')), top=(0.8 * cm), left=(14.5 * cm)),
         Label(text=(_('End Date')), top=(0.8 * cm), left=(17.5 * cm))]

    class band_detail(ReportBand):
        height = 0.5 * cm
        elements = (
         ObjectValue(attribute_name='user', left=(0 * cm), get_value=(lambda instance: instance.user.last_name + ', ' + instance.user.first_name)),
         ObjectValue(attribute_name='user', left=(2.5 * cm), get_value=(lambda instance: instance.user.email)),
         ObjectValue(attribute_name='membership_type', left=(5.5 * cm)),
         ObjectValue(attribute_name='invoice', left=(11.5 * cm), get_value=(lambda instance:          if instance.get_invoice():
instance.get_invoice().total # Avoid dead code: '')),
         ObjectValue(attribute_name='join_dt', left=(14.5 * cm), get_value=(lambda instance: instance.join_dt.strftime('%b %d, %Y'))),
         ObjectValue(attribute_name='expire_dt', left=(17.5 * cm), get_value=(lambda instance:          if instance.expire_dt:
instance.expire_dt.strftime('%b %d, %Y') # Avoid dead code: '')))


def id_format(value, instance):
    link = reverse('membership.details', args=[value])
    html = '<a href="%s">%s</a>' % (link, value)
    return mark_safe(html)


def membership_type_format(value, instance=None):
    global MEMBERSHIPTYPE_DICT
    if not MEMBERSHIPTYPE_DICT:
        MEMBERSHIPTYPE_DICT = dict(((m.id, m.name) for m in MembershipType.objects.all()))
    return MEMBERSHIPTYPE_DICT.get(value, value)


class MembershipReport(ReportAdmin):
    title = _('Membership Report')
    model = MembershipDefault
    fields = [
     'id',
     'user__first_name',
     'user__last_name',
     'user__email',
     'expire_dt',
     'membership_type',
     'status_detail']
    list_filter = ('status_detail', 'membership_type')
    list_order_by = ('create_dt', )
    list_group_by = ('membership_type', 'status_detail')
    exports = ('excel', 'pdf')
    type = 'chart'
    chart_types = ('pie', 'column')
    list_serie_fields = ('id', )
    list_serie_ops = ('len', )
    hide_show_only_totals = True
    override_group_value = {'membership_type': membership_type_format}
    override_field_formats = {'membership_type':membership_type_format, 
     'expire_dt':us_date_format, 
     'id':id_format}
    base_template_name = ''


reports.register('memberships', MembershipReport)