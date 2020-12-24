# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bas/dev/django-dmarc/dmarc/views.py
# Compiled at: 2018-06-18 16:39:43
# Size of source mod 2**32: 6545 bytes
"""
DMARC views
http://dmarc.org/resources/specification/
"""
import csv, datetime
from django.contrib.admin.views.decorators import staff_member_required
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db import connection
from django.http import JsonResponse, StreamingHttpResponse
from django.shortcuts import render
from dmarc.models import Report

class Echo(object):
    __doc__ = 'An object that implements just the write method of the file-like\n    interface for csv.writer.\n    '

    @staticmethod
    def write(_, value):
        """Write the value by returning it, instead of storing in a buffer."""
        return value


def _sql_cursor(request_args):
    """Returns a cursor according to users request"""
    sql_where = []
    sql_orderby = []
    sql_params = []
    if 'dmarc_date_from' in request_args:
        val = request_args['dmarc_date_from']
        try:
            val = datetime.datetime.strptime(val, '%Y-%m-%d')
        except:
            val = datetime.date.today()

        sql_where.append('dmarc_report.date_begin >= %s')
        sql_params.append(val)
    if 'dmarc_date_to' in request_args:
        val = request_args['dmarc_date_to']
        try:
            val = datetime.datetime.strptime(val, '%Y-%m-%d')
        except:
            val = datetime.date.today()

        val += datetime.timedelta(days=1)
        sql_where.append('dmarc_report.date_end < %s')
        sql_params.append(val)
    if 'dmarc_disposition' in request_args:
        if request_args['dmarc_disposition']:
            val = request_args['dmarc_disposition']
            sql_where.append('dmarc_record.policyevaluated_disposition = %s')
            sql_params.append(val)
    if 'dmarc_onlyerror' in request_args:
        clause = '('
        clause += "dmarc_record.policyevaluated_dkim = 'fail'"
        clause += ' OR '
        clause += "dmarc_record.policyevaluated_spf = 'fail'"
        clause += ')'
        sql_where.append(clause)
    if 'dmarc_filter' in request_args:
        if request_args['dmarc_filter']:
            val = request_args['dmarc_filter'] + '%'
            clause = '('
            clause += 'lower(dmarc_reporter.org_name) LIKE lower(%s)'
            clause += ' OR '
            clause += 'dmarc_record.source_ip LIKE %s'
            clause += ')'
            sql_where.append(clause)
            sql_params.append(val)
            sql_params.append(val)
    sql = "\nSELECT\n  dmarc_reporter.org_name,\n  dmarc_reporter.email,\n  dmarc_report.date_begin,\n  dmarc_report.date_end,\n  dmarc_report.policy_domain,\n  dmarc_report.policy_adkim,\n  dmarc_report.policy_aspf,\n  dmarc_report.policy_p,\n  dmarc_report.policy_sp,\n  dmarc_report.policy_pct,\n  dmarc_report.report_id,\n  dmarc_record.source_ip,\n  dmarc_record.recordcount,\n  dmarc_record.policyevaluated_disposition,\n  dmarc_record.policyevaluated_dkim,\n  dmarc_record.policyevaluated_spf,\n  dmarc_record.policyevaluated_reasontype,\n  dmarc_record.policyevaluated_reasoncomment,\n  dmarc_record.identifier_headerfrom,\n  spf_dmarc_result.record_type AS spf_record_type,\n  spf_dmarc_result.domain AS spf_domain,\n  spf_dmarc_result.result AS spf_result,\n  dkim_dmarc_result.record_type AS dkim_record_type,\n  dkim_dmarc_result.domain AS dkim_domain,\n  dkim_dmarc_result.result AS dkim_result\nFROM dmarc_reporter\nINNER JOIN dmarc_report\nON dmarc_report.reporter_id = dmarc_reporter.id\nINNER JOIN  dmarc_record\nON dmarc_record.report_id = dmarc_report.id\nLEFT OUTER JOIN dmarc_result AS spf_dmarc_result\nON spf_dmarc_result.record_id = dmarc_record.id\nAND spf_dmarc_result.record_type = 'spf'\nLEFT OUTER JOIN dmarc_result AS dkim_dmarc_result\nON dkim_dmarc_result.record_id = dmarc_record.id\nAND dkim_dmarc_result.record_type = 'dkim'\n    "
    if sql_where:
        sql = sql + ' WHERE ' + '\nAND '.join(sql_where)
    sql_orderby.append('LOWER(dmarc_reporter.org_name)')
    sql_orderby.append('dmarc_report.date_begin')
    sql_orderby.append('dmarc_record.source_ip')
    sql = sql + '\nORDER BY ' + ', '.join(sql_orderby)
    cursor = connection.cursor()
    cursor.execute(sql, sql_params)
    return cursor


@staff_member_required
def dmarc_index(request):
    """Index view"""
    context = {'reports': 'TODO'}
    return render(request, 'dmarc/report.html', context)


@staff_member_required
def dmarc_report(request):
    """Paginated DMARC report list"""
    report_list = Report.objects.select_related('reporter').prefetch_related('records__results').order_by('-date_begin', 'reporter__org_name').all()
    paginator = Paginator(report_list, 2)
    page = request.GET.get('page')
    try:
        reports = paginator.page(page)
    except PageNotAnInteger:
        reports = paginator.page(1)
    except EmptyPage:
        reports = paginator.page(paginator.num_pages)

    context = {'reports': reports}
    return render(request, 'dmarc/report.html', context)


@staff_member_required
def dmarc_csv(request):
    """Export DMARC data as CSV"""

    def stream():
        pseudo_buffer = Echo()
        writer = csv.writer(pseudo_buffer)
        columns = True
        for row in cursor.fetchall():
            data = ''
            if columns:
                columns = [col[0] for col in cursor.description]
                data = writer.writerow(columns)
                columns = False
            data = data + writer.writerow(row)
            yield data

    now = datetime.datetime.now()
    disposition = 'attachment; filename="dmarc-{}.csv"'.format(now.strftime('%Y-%m-%d-%H%M%S'))
    cursor = _sql_cursor(request.GET)
    response = StreamingHttpResponse((stream()), content_type='text/csv')
    response['Content-Disposition'] = disposition
    return response


@staff_member_required
def dmarc_json(request):
    """Export DMARC data as JSON"""
    cursor = _sql_cursor(request.GET)
    data = JsonResponse((cursor.fetchall()), safe=False)
    return data