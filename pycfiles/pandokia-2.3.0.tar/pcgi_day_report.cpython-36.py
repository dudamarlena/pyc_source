# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jhunk/Downloads/pandokia/pandokia/pcgi_day_report.py
# Compiled at: 2018-06-04 12:38:26
# Size of source mod 2**32: 21412 bytes
import sys, cgi, re, copy, time, pandokia.text_table as text_table, pandokia.lib as lib, pandokia
pdk_db = pandokia.cfg.pdk_db
import pandokia.common as common, pandokia.pcgi

def rpt1():
    form = pandokia.pcgi.form
    if 'test_run' in form:
        test_run = form.getvalue('test_run')
    else:
        test_run = '*'
    if test_run == '-me':
        test_run = 'user_' + common.current_user() + '_*'
    my_run_prefix = 'user_' + common.current_user()
    admin = common.current_user() in common.cfg.admin_user_list
    where_str, where_dict = pdk_db.where_dict([('test_run', test_run)])
    sql = 'SELECT test_run, valuable, record_count, note, min_time, max_time FROM distinct_test_run %s ORDER BY test_run DESC ' % where_str
    c = pdk_db.execute(sql, where_dict)
    table = text_table.text_table()
    table.set_html_table_attributes('border=1')
    table.define_column('addval', showname='')
    table.define_column('run', showname='test_run')
    table.define_column('tree', showname='')
    table.define_column('del', showname='')
    table.define_column('min', showname='start')
    table.define_column('max', showname='end')
    table.define_column('tdiff', showname='duration')
    table.define_column('count', showname='records')
    table.define_column('note', showname='note')
    tquery = {'project':'*', 
     'host':'*'}
    vquery = {'valuable_run': 1}
    cquery = {}
    row = 0
    for x, val, record_count, note, min_time, max_time in c:
        if x is None:
            continue
        else:
            tquery['test_run'] = x
            vquery['test_run'] = x
            cquery['count_run'] = x
            table.set_value(row,
              'addval',
              html=('<a href="%s">!</a>&nbsp;&nbsp;&nbsp;' % common.selflink(vquery, 'action')))
            table.set_value(row,
              'run', text=x, link=(common.selflink(tquery, 'day_report.2')))
            table.set_value(row,
              'tree',
              text='(tree display)',
              link=(common.selflink(tquery, 'treewalk')))
            if val == '0':
                if x.startswith(my_run_prefix):
                    table.set_value(row,
                      'del', text='(delete)', link=(common.selflink(tquery, 'delete_run.ays')))
                else:
                    table.set_value(row,
                      'del',
                      text='(delete)',
                      html='<font color=gray>(delete)</font>',
                      link=(common.selflink(tquery, 'delete_run.ays')))
            else:
                table.set_value(row, 'del', text='(valuable)')
            if note is None:
                table.set_value(row, 'note', text='')
            else:
                table.set_value(row, 'note', text=note)
            if min_time is not None:
                if max_time is not None:
                    table.set_value(row, 'tdiff', str(lib.time_diff(max_time, min_time)))
                    min_time = str(min_time).split('.')[0]
                    max_time = str(max_time).split('.')[0]
                    t1 = min_time.split()
                    t2 = max_time.split()
                    if len(t2) > 1:
                        if len(t1) > 1:
                            if t1[0] == t2[0]:
                                if len(t2) > 1:
                                    max_time = t2[1]
                    table.set_value(row, 'min', text=min_time)
                    table.set_value(row, 'max', text=max_time)
                elif min_time is not None:
                    min_time = str(min_time).split('.')[0]
                    table.set_value(row, 'min', text=min_time)
            else:
                if max_time is not None:
                    max_time = str(max_time).split('.')[0]
                    table.set_value(row, 'max', text=max_time)
                table.set_value(row, 'tdiff', '')
            update_count = common.selflink(cquery, 'action')
            if record_count is None or record_count <= 0:
                record_count = '&nbsp;'
        table.set_value(row,
          'count',
          html=(str(record_count)),
          link=update_count)
        row = row + 1

    if pandokia.pcgi.output_format == 'html':
        sys.stdout.write(common.cgi_header_html)
        sys.stdout.write(common.page_header())
        sys.stdout.write('<h2>%s</h2>' % cgi.escape(test_run))
        sys.stdout.write(table.get_html(headings=1))
        sys.stdout.write('<br>Click on the ! to mark a test run as too valuable to delete\n')
        sys.stdout.write('<br>Click on record count to check the count and update it\n')
        sys.stdout.write('<style>\ntable {\n    border-collapse: collapse;\n}\ntable, th, td {\n    border: 2px solid black;\n    padding: 3px;\n}\n</style>\n')
    else:
        if pandokia.pcgi.output_format == 'csv':
            sys.stdout.write(common.cgi_header_csv)
            sys.stdout.write(table.get_csv())
    sys.stdout.flush()


def rpt2():
    form = pandokia.pcgi.form
    if 'test_run' in form:
        test_run = form.getvalue('test_run')
    else:
        rpt1()
        return
        test_run = common.find_test_run(test_run)
        projects = None
        host = None
        context = None
        chronic = '0'
        if 'project' in form:
            projects = form.getlist('project')
        if 'host' in form:
            host = form.getlist('host')
        if 'context' in form:
            context = form.getlist('context')
        if 'chronic' in form:
            chronic = form.getlist('chronic')[0]
        c = pdk_db.execute('SELECT note, valuable FROM distinct_test_run WHERE test_run = :1', (test_run,))
        x = c.fetchone()
        if x is None:
            sys.stdout.write(common.cgi_header_html)
            sys.stdout.write(common.page_header())
            sys.stdout.write('No such test run')
            return
        test_run_note, test_run_valuable = x
        if test_run_note is None:
            test_run_note = ''
        if test_run_valuable is None:
            test_run_valuable = 0
        else:
            test_run_valuable = int(test_run_valuable)
        table, projects = gen_daily_table(test_run, projects, context, host,
          valuable=test_run_valuable, chronic=(chronic == '1'))
        if pandokia.pcgi.output_format == 'html':
            header = '<big><big><b>' + cgi.escape(test_run) + '</b></big></big>\n'
            t = common.looks_like_a_date(test_run)
            try:
                import datetime
                t = t.group(1).split('-')
                year, month, day = int(t[0]), int(t[1]), int(t[2])
                t = datetime.date(year, month, day)
                t = t.strftime('%A')
                header = header + '<big>(' + str(t) + ')</big>'
            except:
                pass

            header = header + '<p>'
            recurring_prefix = common.recurring_test_run(test_run)
            if recurring_prefix:
                l = []
                prev = common.run_previous(recurring_prefix, test_run)
                if prev:
                    l.append(common.self_href(query_dict={'test_run': prev},
                      linkmode='day_report.2',
                      text=prev))
                next = common.run_next(recurring_prefix, test_run)
                if next:
                    l.append(common.self_href(query_dict={'test_run': next},
                      linkmode='day_report.2',
                      text=next))
                latest = common.run_latest(recurring_prefix)
                if latest:
                    if latest != next:
                        if latest != test_run:
                            l.append(common.self_href(query_dict={'test_run': latest},
                              linkmode='day_report.2',
                              text=latest))
                header = header + '( %s )' % ' / '.join(l)
            if test_run_note.startswith('*'):
                header = header + '<p>\nNote: %s</p>' % cgi.escape(test_run_note)
            else:
                header = header + '<p><form action=%s>\nNote: <input type=text name=note value="%s" size=%d>\n<input type=hidden name=test_run value="%s">\n<input type=hidden name=query value=action></form></p>' % (
                 common.get_cgi_name(), cgi.escape(test_run_note), len(test_run_note) + 20, test_run)
            if test_run_valuable:
                header = header + '<p>valuable '
            else:
                header = header + '<p>not valuable '
            header = header + '(<a href=%s>change</a>)' % common.selflink({'test_run':test_run, 
             'valuable_run':int(not test_run_valuable)},
              linkmode='action')
            sys.stdout.write(common.cgi_header_html)
            sys.stdout.write(common.page_header())
            sys.stdout.write(header)
            sys.stdout.write('<p>\n')
            for p in projects:
                p = cgi.escape(p)
                sys.stdout.write('<a href="#%s">%s</a>&nbsp;&nbsp; ' % (p, p))

            sys.stdout.write('</p>\n')
            sys.stdout.write(table.get_html(headings=0))
        elif pandokia.pcgi.output_format == 'csv':
            sys.stdout.write(common.cgi_header_csv)
            sys.stdout.write(table.get_csv())


def gen_daily_table(test_run, projects, query_context, query_host, valuable=0, chronic=False):
    test_run = common.find_test_run(test_run)
    show_delete = not valuable
    if show_delete:
        my_run_prefix = 'user_' + common.current_user()
        if test_run.startswith(my_run_prefix):
            del_text = '(del)'
        else:
            if common.current_user() in common.cfg.admin_user_list:
                del_text = '<font color=gray>(del)</font>'
            else:
                show_delete = False
    else:
        query = {'test_run': test_run}
        table = text_table.text_table()
        table.set_html_table_attributes('cellpadding=2 ')
        status_types = common.cfg.statuses
        row = 0
        table.define_column('host')
        table.define_column('context')
        table.define_column('os')
        table.define_column('total')
        for x in status_types:
            table.define_column(x)

        if chronic:
            table.define_column('chronic')
        table.define_column('del')
        table.define_column('note')
        n_cols = 3 + len(status_types) + 2
        prev_project = None
        all_sum = {'total':0, 
         'chronic':0}
        for status in status_types:
            all_sum[status] = 0

        hc_where, hc_where_dict = pdk_db.where_dict([
         (
          'test_run', test_run), ('project', projects), ('context', query_context), ('host', query_host)])
        c = pdk_db.execute('SELECT DISTINCT project, host, context FROM result_scalar %s ORDER BY project, host, context ' % hc_where, hc_where_dict)
        if chronic:
            chronic_str = "AND ( chronic = '0' or chronic IS NULL )"
        else:
            chronic_str = ''
    projects = []
    for project, host, context in c:
        if project != prev_project:
            projects.append(project)
            table.set_value(row, 0, '')
            prev_project = project
            query['project'] = project
            query['host'] = '%'
            link = common.selflink(query_dict=query, linkmode='treewalk')
            project_text = cgi.escape(project)
            project_text = '<hr><big><strong><b><a name="%s" href="%s">%s</a></b></strong></big>' % (
             project_text, link, project_text)
            table.set_value(row, 0, text=project, html=project_text)
            table.set_html_cell_attributes(row, 0, 'colspan=%d' % n_cols)
            row += 1
            insert_col_headings(table, row, link, chronic)
            row += 1
            project_sum = {'total':0, 
             'chronic':0}
            for status in status_types:
                project_sum[status] = 0

            project_sum_row = row
            if show_delete:
                table.set_value(row, 'del', html=del_text, link=(delete_link({'test_run':test_run, 
                 'project':project}, show_delete)))
            row += 1
            prev_host = None
        else:
            query['host'] = host
            link = common.selflink(query_dict=query, linkmode='treewalk')
            if host != prev_host:
                table.set_value(row, 0, text=host, link=link)
                prev_host = host
            query['context'] = context
            link = common.selflink(query_dict=query, linkmode='treewalk')
            del query['context']
            table.set_value(row, 1, text=context, link=link)
            if show_delete:
                table.set_value(row, 'del',
                  html=del_text,
                  link=(delete_link({'test_run':test_run,  'project':project, 
                 'host':host, 
                 'context':context}, show_delete)))
            hinfo = pandokia.common.hostinfo(host)
            table.set_value(row,
              2,
              text=(hinfo[1]),
              link=common.selflink(query_dict={'host': host},
              linkmode='hostinfo'))
            total_results = 0
            missing_count = 0
            for status in status_types:
                c1 = pdk_db.execute('SELECT COUNT(*) FROM result_scalar WHERE  test_run = :1 AND project = :2 AND host = :3 AND status = :4 AND context = :5 %s' % (
                 chronic_str,), (test_run, project, host, status, context))
                x, = c1.fetchone()
                total_results += x
                project_sum[status] += x
                all_sum[status] += x
                if x == 0:
                    table.set_value(row, status, text='0')
                else:
                    table.set_value(row,
                      status,
                      text=(str(x)),
                      link=(link + '&status=' + status))
                table.set_html_cell_attributes(row, status, 'align="right"')
                if status == 'M':
                    missing_count = x

            if chronic:
                c1 = pdk_db.execute("SELECT COUNT(*) FROM result_scalar WHERE  test_run = :1 AND project = :2 AND host = :3 AND context = :5 AND chronic = '1'", (
                 test_run,
                 project,
                 host,
                 status,
                 context))
                x, = c1.fetchone()
                total_results += x
                project_sum['chronic'] += x
                all_sum['chronic'] += x
                table.set_value(row,
                  'chronic',
                  text=(str(x)),
                  link=(link + '&chronic=1'))
                table.set_html_cell_attributes(row, 'chronic', 'align="right"')
            project_sum['total'] += total_results
            all_sum['total'] += total_results
            if 0:
                if 'M' in status_types:
                    if missing_count != 0:
                        if missing_count == total_results:
                            table.set_value(row, 'note', 'all missing')
                        else:
                            table.set_value(row, 'note', 'some missing')
        table.set_value(row, 'total', text=(str(total_results)), link=link)
        table.set_html_cell_attributes(row, 'total', 'align="right"')
        row = row + 1
        for status in status_types:
            table.set_value(project_sum_row, status, project_sum[status])
            table.set_html_cell_attributes(project_sum_row, status, 'align="right" style="font-weight:bold"')

        table.set_value(project_sum_row, 'total', project_sum['total'])
        table.set_html_cell_attributes(project_sum_row, 'total', 'align="right" style="font-weight:bold"')
        table.set_value(row, 0, '')

    table.set_value(row, 0, html='<hr>')
    table.set_html_cell_attributes(row, 0, 'colspan=%d' % n_cols)
    row = row + 1
    insert_col_headings(table, row, None, chronic)
    row = row + 1
    total_row = row
    query['host'] = '*'
    query['project'] = projects
    query['host'] = query_host
    query['context'] = query_context
    table.set_value(total_row, 'total', text=(str(all_sum['total'])), link=common.selflink(query_dict=query, linkmode='treewalk'))
    table.set_html_cell_attributes(row, 'total', 'align="right"')
    for status in status_types:
        query['status'] = status
        table.set_value(total_row,
          status,
          (all_sum[status]),
          link=common.selflink(query_dict=query,
          linkmode='treewalk'))
        table.set_html_cell_attributes(total_row, status, 'align="right"')

    return (table, projects)


def insert_col_headings(table, row, link, chronic):
    table.set_value(row, 'total', text='total', link=link)
    table.set_html_cell_attributes(row, 'total', 'align="right"')
    xl = None
    for x in common.cfg.statuses:
        xn = common.cfg.status_names[x]
        if link:
            xl = link + '&status=' + x
        table.set_value(row, x, text=xn, link=xl)
        table.set_html_cell_attributes(row, x, 'align="right"')

    if chronic:
        table.set_value(row, 'chronic', 'chronic')
        table.set_html_cell_attributes(row, 'chronic', 'align="right"')


def delete_link(argdict, mode):
    l = common.selflink(argdict, 'delete_run.ays')
    return l