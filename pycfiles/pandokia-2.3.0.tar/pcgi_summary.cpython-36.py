# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jhunk/Downloads/pandokia/pandokia/pcgi_summary.py
# Compiled at: 2018-05-14 14:25:23
# Size of source mod 2**32: 27771 bytes
import sys, cgi, re, copy, time, pandokia.lib as lib, pandokia.text_table as text_table
try:
    from urllib.parse import quote
except ImportError:
    from urllib import quote

import pandokia.pcgi
from . import common
import pandokia
pdk_db = pandokia.cfg.pdk_db
output = sys.stdout

def qid_block(qid):
    c = pdk_db.execute('SELECT expires, username, notes FROM query_id WHERE qid = :1', (qid,))
    x = c.fetchone()
    if x is not None:
        expires = x[0]
        claimant = x[1]
        if claimant == '':
            claimant = None
        notes = x[2]
    else:
        expires = None
        claimant = None
        notes = ''
    output.write('<h3>QID = %d</h3>' % int(qid))
    if expires == pandokia.never_expires:
        output.write('<b>never expires</b>')
    else:
        if expires is not None:
            expires = float(expires)
            e = time.localtime(expires)
            output.write('expires %4d-%02d-%02d' % (
             e.tm_year, e.tm_mon, e.tm_mday))
        else:
            output.write('expires someday')
        qdict = {'qid':qid,  'valuable_qid':1}
        output.write(" ( <a href='" + common.selflink(qdict, linkmode='action') + "'>")
        output.write('never expire</a> )')
    qdict = {'qid':qid,  'valuable_qid':0}
    output.write(" ( <a href='" + common.selflink(qdict, linkmode='action') + "'>")
    output.write('normal expire</a> )')
    output.write(', ')
    qdict = {'qid':qid,  'claim_qid':1}
    if claimant is not None:
        output.write('owner %s\n' % claimant)
    else:
        output.write(" ( <a href='" + common.selflink(qdict, linkmode='action') + "'>")
        output.write('Claim this qid</a> ) <br>')
    if notes is None:
        notes = 'None'
    qdict = {'qid':qid,  'edit_comment':1}
    output.write("<br><a href='" + common.selflink(qdict, linkmode='action') + "'>")
    output.write('Comment:</a><br><pre>%s</pre>\n' % cgi.escape(notes))


def run():
    global any_attr
    any_attr = {}
    input_query = pandokia.pcgi.form_to_dict(pandokia.pcgi.form)
    qid = int(input_query['qid'][0])
    for x in ('x', ):
        if x in input_query:
            del input_query[x]

    if 'cmp_run' in input_query:
        cmp_run = input_query['cmp_run'][0]
        if cmp_run == '':
            cmp_run = 'daily_yesterday'
        cmp_run = common.find_test_run(cmp_run)
    else:
        cmp_run = ''
    cmptype = 'c'
    if 'x_submit' in input_query:
        x = input_query['x_submit'][0]
        if x == 'same':
            cmptype = 's'
        elif x == 'different':
            cmptype = 'd'
    else:
        show_attr = 0
        if 'show_attr' in input_query:
            show_attr = int(input_query['show_attr'][0])
            if show_attr == 2:
                return column_selector(input_query)
        sort_query = {}
        for x in input_query:
            if x != 'sort' and x != 'query':
                sort_query[x] = input_query[x]

        sort_link = common.selflink(sort_query, 'summary') + '&sort='
        result_table, all_test_run, all_project, all_host, all_context, rowcount, different = get_table(qid, sort_link, cmp_run, cmptype, show_attr)
        if 'S' in input_query:
            column_select_values = input_query['S']
            column_select_values = set(column_select_values)
            for x in result_table.colmap:
                if x in ('line #', 'checkbox'):
                    continue
                if x not in column_select_values:
                    result_table.suppress(x)

        else:
            column_select_values = set([x for x in result_table.colmap])
    if pandokia.pcgi.output_format == 'html':
        print('content-type: text/html\n\n')
        print(common.page_header())
        output.write('<h1>Test summary</h1>')
        output.write("\n    Compare to:\n    <form action=%s id=compare_form name=compare_form>\n    <input type=hidden name=qid value='%d'>\n    <input type=hidden name=show_attr value='%d'>\n    <input type=hidden name=query value='summary'>\n    <input type=text name=cmp_run value='%s'>\n    <br>\n    <input type=submit name=x_submit value='compare'>\n    <input type=submit name=x_submit value='same'>\n    <input type=submit name=x_submit value='different'>\n    </form>\n    " % (pandokia.pcgi.cginame, qid, show_attr, cgi.escape(cmp_run)))
        output.write("\n    <form action=%s id=attribute_form name=attribute_form>\n    <input type=hidden name=qid value=%d>\n    <input type=hidden name=show_attr value=1>\n    <input type=hidden name=query value=summary>\n    <input type=hidden name=cmp_run value='%s'>\n    <input type=submit name=x_submit value='Add Attributes'>\n    </form>\n    " % (pandokia.pcgi.cginame, qid, cgi.escape(cmp_run)))
        qid_block(qid)
        qdict = {'qid': qid}
        output.write("<a href='%s'>Tree walk this QID </a>, " % common.selflink(qdict, linkmode='treewalk'))
        qdict = {'qid': qid}
        output.write("<a href='%s'>Edit this QID </a>, " % common.selflink(qdict,
          linkmode='qid_op'))
        qdict = input_query.copy()
        qdict['show_attr'] = 2
        del qdict['query']
        output.write('<a href="%s">Column Selector</a>' % common.selflink(qdict,
          linkmode='summary'))
        output.write('<br>Other formats: ')
        qdict = input_query.copy()
        del qdict['query']
        qdict['format'] = 'csv'
        output.write("<a href='%s'>CSV</a> " % common.selflink(qdict,
          linkmode='summary'))
        qdict['format'] = 'rst'
        output.write("<a href='%s'>RST</a> " % common.selflink(qdict,
          linkmode='summary'))
        qdict['format'] = 'awk'
        output.write("<a href='%s'>TAB</a> " % common.selflink(qdict,
          linkmode='summary'))
        output.write('<br>\n')
        if len(all_test_run) == 1:
            result_table.suppress('test_run')
            output.write('<h3>test_run: ' + cgi.escape([tmp for tmp in all_test_run][0]) + '</h3>')
        if len(all_project) == 1:
            result_table.suppress('project')
            output.write('<h3>project: ' + cgi.escape([tmp for tmp in all_project][0]) + '</h3>')
        if len(all_host) == 1:
            result_table.suppress('host')
            output.write('<h3>host: ' + cgi.escape([tmp for tmp in all_host][0]) + '</h3>')
        if len(all_context) == 1:
            result_table.suppress('context')
            output.write('<h3>context: ' + cgi.escape([tmp for tmp in all_context][0]) + '</h3>')
        same_table = suppress_attr_all_same(result_table, column_select_values)
        if same_table.get_row_count() > 0:
            output.write('<ul><b>attributes same for all rows:</b>')
            output.write(same_table.get_html())
            output.write('</ul><br>')
        if 'sort' in input_query:
            sort_order = input_query['sort'][0]
        else:
            sort_order = 'Utest_name'
        reverse_val = sort_order.startswith('D')
        result_table.set_sort_key(sort_order[1:], float)
        result_table.sort([sort_order[1:]], reverse=reverse_val)
        rows = len(result_table.rows)
        for i in range(0, rows):
            result_table.set_value(i, 'line #', i + 1)

        output.write('\n    <script language=javascript type=\'text/javascript\'>\n\n        var flag_ok_clicked=false;\n\n        function validate_flag_ok()\n        {\n            var comment = document.forms["testform"]["ok_comment"].value;\n\n            if (flag_ok_clicked == true)\n            {\n                if (comment == "")\n                {\n                    alert("Doh!  You forgot to comment!");\n                    flag_ok_clicked = false;\n                    return false;\n                }\n            }\n            return true;\n        }\n\n        function set_all(value)\n            {\n            len = document.testform.elements.length;\n            ele = document.testform.elements;\n            for (n=0; n<len; n++)\n                ele[n].checked=value;\n            }\n        function set_range(value)\n            {\n            begin=document.getElementById("begin").value-1;\n            end=document.getElementById("end").value-0;\n            ele=document.testform.elements;\n            for(n=begin; n<end; n++)\n                ele[n].checked=value;\n            }\n        function toggle(value)\n            {\n            len = document.testform.elements.length;\n            ele = document.testform.elements;\n            for (n=0; n<len; n++)\n                ele[n].checked= ! ele[n].checked;\n            }\n        function condclear(name)\n            {\n            n = document.getElementById(name);\n            if ( n.value.substr(0,1) == \'*\' )\n                n.value=\'\';\n            }\n    </script>\n    ')
        output.write('\n        <form action=%s method=post name=testform onsubmit="return validate_flag_ok();">\n        ' % (pandokia.pcgi.cginame,))
        output.write(result_table.get_html(color_rows=5))
        output.write("\n        <input type=hidden name=query value='action'>\n        <input type=hidden name=qid value=%d>\n        " % (qid,))
        output.write('Actions:<br>')
        output.write('<input type=text name=begin id=begin value="*Begin line" onfocus=\'condclear("begin")\'size=10> ')
        output.write('<input type=text name=end id=end value="*End line" onfocus=\'condclear("end")\' size=10> ')
        output.write('<input type=button name="setrange" value="Set Range" onclick="set_range(true)">')
        output.write('<br>')
        output.write('<input type=button name="setall"   value="Select All"   onclick="set_all(true)">')
        output.write('<input type=button name="clearall" value="Clear All" onclick="set_all(false)">')
        output.write('<input type=button name="clearall" value="Toggle"    onclick="toggle()">')
        output.write('<br>')
        output.write('<input type=submit name="action_remove" value="Remove">')
        output.write('<input type=submit name="action_keep"   value="Keep">')
        output.write(' on this report page<br>')
        output.write('<input type=submit name="action_flagok" value="Flag OK" onclick="flag_ok_clicked = true;">')
        output.write('<input type=submit name="action_flagok_rem" value="Flag OK + Remove">')
        output.write(' with comment: <input type=text name=ok_comment value="" size=30><br>')
        output.write('<input type=submit name="action_cattn" value="Clear Attn">')
        output.write('<input type=submit name="action_sattn" value="Set Attn"><br>')
        output.write('<input type=submit name="not_expected" value="Not Expected"> in <input type=text name=arg1 value="%" size=10> test runs')
        output.write('</form>')
        output.write('<br>rows: %d <br>' % rowcount)
        if cmp_run != '':
            output.write('different: %d <br>' % different)
        qdict = {'qid': qid}
        output.write("<a href='" + common.selflink(qdict, linkmode='detail') + "'>")
        output.write('detail of all</a>')
        return
    if pandokia.pcgi.output_format == 'csv':
        result_table.suppress('checkbox')
        result_table.suppress('line #')
        print('content-type: text/plain\n\n')
        print(result_table.get_csv(headings=1))
    else:
        if pandokia.pcgi.output_format == 'rst':
            result_table.suppress('checkbox')
            result_table.suppress('line #')
            print('content-type: text/plain\n\n')
            print(result_table.get_rst(headings=1))
        elif pandokia.pcgi.output_format == 'awk':
            result_table.suppress('checkbox')
            result_table.suppress('line #')
            print('content-type: text/plain\n\n')
            print(result_table.get_awk(headings=1))


def load_in_table(tt, row, cursor, prefix, sort_link):
    for x in cursor:
        name, value = x
        name = prefix + name
        tt.define_column(name, link=(sort_link + 'U' + name))
        tt.set_value(row, name, value)
        any_attr[name] = 1


def get_table(qid, sort_link, cmp_run, cmptype, show_attr):
    result_table = text_table.text_table()
    result_table.set_html_table_attributes('border=1')
    tda_table = text_table.text_table()
    tda_table.set_html_table_attributes('border=1')
    tra_table = text_table.text_table()
    tra_table.set_html_table_attributes('border=1')
    now = time.time()
    pdk_db.execute('UPDATE query_id SET time = :1 WHERE qid = :2', (now, qid))
    expires = now + pandokia.cfg.default_qid_expire_days * 86400
    pdk_db.execute('UPDATE query_id SET expires = :1 WHERE qid = :2 AND :1 > query_id.expires', (
     expires,
     qid))
    pdk_db.commit()
    c = pdk_db.execute('SELECT key_id FROM query WHERE qid = :1', (qid,))
    result_table.define_column('line #', showname='&nbsp;')
    result_table.define_column('runner')
    result_table.define_column('checkbox', showname='&nbsp;')
    result_table.define_column('attn', link=(sort_link + 'Uattn'))
    result_table.define_column('test_run', link=(sort_link + 'Utest_run'))
    result_table.define_column('project', link=(sort_link + 'Uproject'))
    result_table.define_column('host', link=(sort_link + 'Uhost'))
    result_table.define_column('context', link=(sort_link + 'Ucontext'))
    result_table.define_column('test_name', link=(sort_link + 'Utest_name'))
    result_table.define_column('contact', link=(sort_link + 'Ucontact'))
    result_table.define_column('duration', link=(sort_link + 'Uduration'))
    if cmp_run != '':
        result_table.define_column('diff', link=(sort_link + 'Udiff'))
        result_table.define_column('other', link=(sort_link + 'Uother'))
    result_table.define_column('stat', link=(sort_link + 'Ustat'))
    all_test_run = {}
    all_project = {}
    all_host = {}
    all_context = {}
    different = 0
    rowcount = 0
    for x in c:
        key_id, = x
        c1 = pdk_db.execute('SELECT test_run, project, host, context, test_name, status, attn, test_runner, start_time, end_time FROM result_scalar WHERE key_id = :1 ', (
         key_id,))
        y = c1.fetchone()
        if y is None:
            continue
        test_run, project, host, context, test_name, status, attn, runner, start_time, end_time = y
        if cmp_run != '':
            c2 = pdk_db.execute('SELECT status, key_id FROM result_scalar WHERE test_run = :1 AND project = :2 AND host = :3 AND test_name = :4 AND context = :5', (
             cmp_run,
             project,
             host,
             test_name,
             context))
            other_status = c2.fetchone()
            if other_status is None:
                pass
            else:
                other_status, other_key_id = other_status
                if other_status == status:
                    if cmptype == 'd':
                        continue
                else:
                    if cmptype == 's':
                        continue
                    result_table.set_value(rowcount, 'diff', text='>')
                other_link = common.selflink({'key_id': other_key_id},
                  linkmode='detail')
                if other_status == 'P':
                    result_table.set_value(rowcount,
                      'other', other_status, link=other_link)
                else:
                    result_table.set_value(rowcount,
                      'other',
                      other_status,
                      html=('<font color=red>' + str(other_status) + '</font>'),
                      link=other_link)
                result_table.set_html_cell_attributes(rowcount, 'other', 'bgcolor=lightgray')
                if other_status != status:
                    different = different + 1
        all_test_run[test_run] = 1
        all_project[project] = 1
        all_host[host] = 1
        all_context[context] = 1
        detail_query = {'key_id': key_id}
        result_table.set_value(rowcount, 'runner', runner)
        result_table.set_value(rowcount,
          'checkbox',
          '',
          html=('<input type=checkbox name=%s>' % key_id))
        result_table.set_value(rowcount, 'attn', attn)
        result_table.set_value(rowcount, 'test_run', test_run)
        result_table.set_value(rowcount, 'project', project)
        result_table.set_value(rowcount, 'host', host)
        result_table.set_value(rowcount, 'context', context)
        this_link = common.selflink(detail_query, linkmode='detail')
        result_table.set_value(rowcount,
          'test_name',
          text=test_name,
          link=this_link)
        result_table.set_value(rowcount, 'contact', common.get_contact(project, test_name, 'str'))
        start_time = lib.decode_time_float(start_time)
        end_time = lib.decode_time_float(end_time)
        if start_time is not None:
            if end_time is not None:
                result_table.set_value(rowcount, 'duration', '%.3f' % (end_time - start_time))
        if status == 'P':
            result_table.set_value(rowcount, 'stat', status, link=this_link)
        else:
            result_table.set_value(rowcount,
              'stat',
              status,
              html=('<font color=red>' + str(status) + '</font>'),
              link=this_link)
        if show_attr:
            c3 = pdk_db.execute('SELECT name, value FROM result_tda WHERE key_id = :1 ORDER BY name ASC', (
             key_id,))
            load_in_table(tda_table, rowcount, c3, 'tda_', sort_link)
            del c3
            c3 = pdk_db.execute('SELECT name, value FROM result_tra WHERE key_id = :1 ORDER BY name ASC', (
             key_id,))
            load_in_table(tra_table, rowcount, c3, 'tra_', sort_link)
            del c3
        rowcount += 1
        del c1

    if show_attr:
        result_table.join(tda_table)
        result_table.join(tra_table)
    return (result_table, all_test_run, all_project, all_host, all_context, rowcount, different)


def suppress_attr_all_same(result_table, column_select_values=set({})):
    global any_attr
    any_attr = sorted(any_attr)
    same_table = text_table.text_table()
    same_table.set_html_table_attributes('border=1')
    same_row = 0
    rowcount = result_table.get_row_count()
    for x in any_attr:
        if x not in column_select_values:
            pass
        else:
            all_same = 1
            txt = result_table._row_col_cell(0, x).text
            for y in range(1, rowcount):
                ntxt = result_table._row_col_cell(y, x).text
                if txt != ntxt:
                    all_same = 0
                    break

            if all_same:
                same_table.set_value(same_row, 0, x)
                same_table.set_value(same_row, 1, txt)
                same_row = same_row + 1
                result_table.suppress(x)

    return same_table


column_selector_buttons = '\n        <input type=button name="x" value="All" onclick="vis_all(1)">\n        <input type=button name="x" value="None" onclick="vis_all(0)">\n        <input type=button name="x" value="tda" onclick="vis_some(\'tda_\')">\n        <input type=button name="x" value="tra" onclick="vis_some(\'tra_\')">\n        <input type=button name="x" value="core" onclick="vis_some(\'\')">\n        <input type=button name="x" value="Toggle" onclick="vis_toggle()">\n        &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;\n        <button type=submit name="format" value="html">Display</button>\n        <button type=submit name="format" value="csv">CSV</button>\n        <button type=submit name="format" value="rst">RST</button>\n        <button type=submit name="format" value="awk">TAB</button>\n        <br>\n'
exclude_cgi_params_from_selector = set(('S', 'show_attr', 'format'))

def column_selector(input_query):
    qid = int(input_query['qid'][0])
    print('content-type: text/html\n\n')
    print(common.page_header())
    print('<h1>Column Selector</h1>')
    qid_block(qid)
    l0 = [
     'runner',
     'attn',
     'test_run',
     'project',
     'host',
     'context',
     'test_name',
     'contact',
     'diff',
     'other',
     'stat',
     'start',
     'duration']
    c = pdk_db.execute('SELECT DISTINCT result_tda.name FROM result_tda, query WHERE query.qid = :1 AND query.key_id = result_tda.key_id', {'1': qid})
    l1 = ['tda_' + x for x, in c]
    c = pdk_db.execute('SELECT DISTINCT result_tra.name FROM result_tra, query WHERE query.qid = :1 AND query.key_id = result_tra.key_id', {'1': qid})
    l2 = ['tra_' + x for x, in c]
    col_list = l0 + sorted(l1) + sorted(l2)
    column_select_values = [
     'test_name', 'stat']
    if 'S' in input_query:
        column_select_values += input_query['S']
    column_select_values = set(column_select_values)
    output.write('<form action=%s method=get name=colselectform id=colselectform>' % pandokia.pcgi.cginame)
    output.write(column_selector_buttons)
    for t in col_list:
        if t in column_select_values:
            checked = ' checked '
        else:
            checked = ''
        output.write('<label><input type=checkbox name=S %s value=%s>%s</label><br>' % (
         checked, quote(t), quote(t)))

    for x in input_query:
        if x not in exclude_cgi_params_from_selector:
            for y in input_query[x]:
                output.write('<input type=hidden name=%s value=%s>' % (
                 x, quote(y)))

    output.write('<input type=hidden name=show_attr value=1>')
    output.write(column_selector_buttons)
    output.write('</form>')
    output.write('\n<script type="text/javascript">\n\n    function vis_toggle()\n        {\n        len = document.colselectform.S.length;\n        ele = document.colselectform.S;\n        for (n=0; n<len; n++)\n            ele[n].checked= ! ele[n].checked;\n        }\n\n    function vis_all(value)\n        {\n        len = document.colselectform.S.length;\n        ele = document.colselectform.S;\n        for (n=0; n<len; n++)\n            ele[n].checked= value;\n        ele[6].checked=1;   // test_name\n        }\n\n    function vis_some(value)\n        {\n        len = document.colselectform.S.length;\n        ele = document.colselectform.S;\n        if ( value == \'\' ) {\n            for (n=0; n<len; n++) {\n                if ( ele[n].value.search(\'t.a_\') == 0 )\n                    return;\n                ele[n].checked= 1\n                }\n            return;\n            }\n        for (n=0; n<len; n++)\n            if ( ele[n].value.search(value) == 0 )\n                ele[n].checked= 1\n        }\n\n</script>\n')