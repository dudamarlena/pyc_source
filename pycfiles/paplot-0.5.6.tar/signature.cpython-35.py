# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: c:\cygwin\home\okada\github\paplot\scripts\paplot\signature.py
# Compiled at: 2017-11-21 04:12:28
# Size of source mod 2**32: 9443 bytes
"""
Created on Wed Mar 16 15:40:29 2016

@author: okada

$Id: signature.py 205 2017-08-08 06:25:59Z aokada $
"""
js_header = '(function() {\nsig_data = {};\n'
js_footer = '\n})();\nObject.freeze(sig_data);\n'
js_dataset = '\nsig_data.tooltip_format = {{\n    signature_title:{signature_title},\n    signature_partial:{signature_partial},\n    mutation_title:{mutation_title},\n    mutation_partial:{mutation_partial},\n}};\n\nsig_data.signatures = [{signatures}];\nsig_data.sig_colors = [{colors}];\nsig_data.dataset_sig = [{dataset_sig}];\nsig_data.dataset_sig_max = {dataset_sig_max};\nsig_data.route_id = [{route_id}];\nsig_data.substitution = [{substruction}];\n\n// [ID, signature, value]\nsig_data.mutations = [{mutations}];\nsig_data.mutation_count = [{mutation_count}];\nsig_data.Ids = [{Ids}];\n'
js_substruction_template = "{{name: '{name}', color: '{color}', route: [{route}],}},"
html_integral_template = '<table>\n<tr>\n<td style="vertical-align: top;" ><div style="float: left;" id="div_rate"></div></td>\n<td style="vertical-align: top;><!-- legend --> <div style="float: left;" id=\'div_rate_legend_html\'></div><div style="float: left;" id=\'div_rate_legend_svg\'></div></td>\n</tr>\n<tr>\n<td style="vertical-align: top;><div style="float: left;" id="div_integral"></div></td>\n<td style="vertical-align: top;><!-- legend --> <div style="float: left;" id=\'div_integral_legend_html\'></div><div style="float: left;" id=\'div_integral_legend_svg\'></div></td>\n</tr>\n<tr>\n<td colspan=2 style="padding-top: 20px;">\n<p>View mode: <select id="chart_mode"></select></p>\n<p>Sort by: <select id="chart_sort"></select></p>\n</td>\n</tr>\n</table>\n'

def output_html(params, config):
    dataset = convert_tojs(params, config)
    if dataset != None and dataset != {}:
        create_html(dataset, params, config)
    return dataset


def convert_tojs(params, config):
    import os, json, math, itertools, paplot.subcode.tools as tools, paplot.convert as convert, paplot.color as color
    try:
        json_data = json.load(open(params['data']))
    except Exception as e:
        print('failure open data %s, %s' % (params['data'], e.message))
        return

    key_ids = tools.config_getstr(config, 'result_format_signature', 'key_id')
    key_signature = tools.config_getstr(config, 'result_format_signature', 'key_signature')
    key_mutations = tools.config_getstr(config, 'result_format_signature', 'key_mutation')
    key_mutation_count = tools.config_getstr(config, 'result_format_signature', 'key_mutation_count')
    sig_num = len(json_data[key_signature])
    if sig_num == 0:
        print('no data %s' % params['data'])
        return {}
    signature_list = []
    for s in range(sig_num):
        signature_list.append('Signature %d' % (s + 1))

    sig_color_list = color.create_color_array(sig_num, color.r_set2)
    if tools.config_getboolean(config, 'result_format_signature', 'background'):
        signature_list.append('Background ')
        sig_color_list.append(color.r_set2_gray)
    sig_y_max = tools.config_getint(config, 'signature', 'signature_y_max')
    if sig_y_max < 0:
        for sig in json_data[key_signature]:
            for sub in sig:
                m = max(sub)
                if sig_y_max < m:
                    sig_y_max = m

    sub_num = len(json_data[key_signature][0][0])
    log = math.log(sub_num, 4)
    if log % 1 > 0:
        print("substitution's list length is invalid (%d, not number 4^N)" % sub_num)
        return
    route_id = []
    route_list = []
    for p in itertools.product(('A', 'C', 'G', 'T'), repeat=int(log)):
        route_id.append(''.join(p))
        route_list.append(p)

    sub_di = [
     {'name': 'C > A', 'ref': 'C', 'color': tools.config_getstr(config, 'signature', 'alt_color_CtoA')},
     {'name': 'C > G', 'ref': 'C', 'color': tools.config_getstr(config, 'signature', 'alt_color_CtoG')},
     {'name': 'C > T', 'ref': 'C', 'color': tools.config_getstr(config, 'signature', 'alt_color_CtoT')},
     {'name': 'T > A', 'ref': 'T', 'color': tools.config_getstr(config, 'signature', 'alt_color_TtoA')},
     {'name': 'T > C', 'ref': 'T', 'color': tools.config_getstr(config, 'signature', 'alt_color_TtoC')},
     {'name': 'T > G', 'ref': 'T', 'color': tools.config_getstr(config, 'signature', 'alt_color_TtoG')}]
    substruction = ''
    for sub in sub_di:
        route = []
        for r in route_list:
            route.append('p'.join(r[0:int(log / 2)]) + 'p' + sub['ref'] + 'p' + 'p'.join(r[int(log / 2):]))

        substruction += js_substruction_template.format(name=sub['name'], color=sub['color'], route=convert.list_to_text(route))

    id_txt = ''
    if key_ids in json_data:
        id_txt = convert.list_to_text(json_data[key_ids])
    mutations_txt = ''
    if key_mutations in json_data:
        for m in json_data[key_mutations]:
            mutations_txt += '[%d,%d,%f],' % (m[0], m[1], m[2])

    dataset_sig = ''
    for sig in json_data[key_signature]:
        tmp = ''
        for sub in sig:
            tmp += '[' + ','.join(map(str, sub)) + '],'

        dataset_sig += '[' + tmp + '],'

    mutation_count_txt = ''
    if key_mutation_count != '' and key_mutation_count in json_data.keys():
        for v in json_data[key_mutation_count]:
            mutation_count_txt += '%d,' % v

    sig_num_sift = 0
    if tools.config_getboolean(config, 'result_format_signature', 'background'):
        sig_num_sift = 1
    ellipsis = '%s%d' % (params['ellipsis'], sig_num + sig_num_sift)
    js_file = 'data_%s.js' % ellipsis
    html_file = 'graph_%s.html' % ellipsis
    keys_di = {'sig': '', 'route': '', 'id': ''}
    f = open(params['dir'] + '/' + js_file, 'w')
    f.write(js_header + js_dataset.format(Ids=id_txt, signatures=convert.list_to_text(signature_list), colors=convert.list_to_text(sig_color_list), dataset_sig_max=sig_y_max, mutations=mutations_txt, dataset_sig=dataset_sig, route_id=convert.list_to_text(route_id), substruction=substruction, signature_title=convert.pyformat_to_jstooltip_text(keys_di, config, 'signature', '', 'tooltip_format_signature_title'), signature_partial=convert.pyformat_to_jstooltip_text(keys_di, config, 'signature', '', 'tooltip_format_signature_partial'), mutation_title=convert.pyformat_to_jstooltip_text(keys_di, config, 'signature', '', 'tooltip_format_mutation_title'), mutation_partial=convert.pyformat_to_jstooltip_text(keys_di, config, 'signature', '', 'tooltip_format_mutation_partial'), mutation_count=mutation_count_txt))
    f_template = open(os.path.dirname(os.path.abspath(__file__)) + '/templates/data_signature.js')
    js_function = f_template.read()
    f_template.close()
    f.write(js_function)
    f.write(js_footer)
    f.close()
    integral = True
    if key_ids == '' or key_mutations == '' or key_mutation_count == '':
        integral = False
    return {'sig_num': sig_num, 
     'js': js_file, 
     'html': html_file, 
     'intergral': integral}


def create_html(dataset, params, config):
    import os, paplot.subcode.tools as tools, paplot.prep as prep
    html_div_template = "<div style='float: left;' id='div_pm{id}'></div>\n"
    html_add_template = "add_div('div_pm{id}');\n"
    div_text = ''
    add_text = ''
    for i in range(dataset['sig_num']):
        div_text += html_div_template.format(id=i)
        add_text += html_add_template.format(id=i)

    integral_text = ''
    if dataset['intergral'] == True:
        integral_text = html_integral_template
    f_template = open(os.path.dirname(os.path.abspath(__file__)) + '/templates/graph_signature.html')
    html_template = f_template.read()
    f_template.close()
    sig_num_sift = 0
    if tools.config_getboolean(config, 'result_format_signature', 'background'):
        sig_num_sift = 1
    f_html = open(params['dir'] + '/' + dataset['html'], 'w')
    f_html.write(html_template.format(project=params['project'], title='%s(#sig %d)' % (params['title'], dataset['sig_num'] + sig_num_sift), data_js=dataset['js'], version=prep.version_text(), date=tools.now_string(), divs=div_text, add_divs=add_text, integral=integral_text, style='../style/%s' % os.path.basename(tools.config_getpath(config, 'style', 'path', 'default.js'))))
    f_html.close()