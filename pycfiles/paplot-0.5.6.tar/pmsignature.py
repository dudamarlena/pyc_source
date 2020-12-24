# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/Okada/github/paplot/scripts/paplot/pmsignature.py
# Compiled at: 2017-11-21 04:12:28
"""
Created on Wed Mar 16 15:40:29 2016

@author: okada

$Id: pmsignature.py 205 2017-08-08 06:25:59Z aokada $
"""
js_header = '(function() {\nmsig_data = {};\n'
js_footer = '\n})();\nObject.freeze(msig_data);\n'
js_dataset = "\nmsig_data.tooltip_format = {{\n    {tooltip_ref}\n    alt:{tooltip_alt},\n    strand:{tooltip_strand},\n    mutation_title:{mutation_title},\n    mutation_partial:{mutation_partial},\n}};\n\nmsig_data.ref_reduce_rate = [1,1,1,1,1];\nmsig_data.label_colors = {{'A': '{color_A}', 'C': '{color_C}', 'G': '{color_G}', 'T': '{color_T}', 'plus': '{color_plus}', 'minus': '{color_minus}'}};\nmsig_data.signatures = [{signatures}];\nmsig_data.sig_colors = [{colors}];\n\nmsig_data.dataset_ref = [{dataset_ref}];\nmsig_data.dataset_alt = [{dataset_alt}];\nmsig_data.dataset_strand = [{dataset_strand}];\n\n// [ID, signature, value]\nmsig_data.mutations = [{mutations}];\nmsig_data.mutation_count = [{mutation_count}];\nmsig_data.Ids = [{Ids}];\n"
js_tooltip_ref_template = 'ref{index}:{tooltip_format},'
html_integral_template = '<table>\n<tr>\n<td style="vertical-align: top;" ><div style="float: left;" id="div_rate"></div></td>\n<td style="vertical-align: top;><!-- legend --> <div style="float: left;" id=\'div_rate_legend_html\'></div><div style="float: left;" id=\'div_rate_legend_svg\'></div></td>\n</tr>\n<tr>\n<td style="vertical-align: top;><div style="float: left;" id="div_integral"></div></td>\n<td style="vertical-align: top;><!-- legend --> <div style="float: left;" id=\'div_integral_legend_html\'></div><div style="float: left;" id=\'div_integral_legend_svg\'></div></td>\n</tr>\n<tr>\n<td colspan=2 style="padding-top: 20px;">\n<p>View mode: <select id="chart_mode"></select></p>\n<p>Sort by: <select id="chart_sort"></select></p>\n</td>\n</tr>\n</table>\n'

def output_html(params, config):
    dataset = convert_tojs(params, config)
    if dataset != None and dataset != {}:
        create_html(dataset, params, config)
    return dataset


def convert_tojs(params, config):
    import os, json, paplot.subcode.tools as tools, paplot.convert as convert, paplot.color as color
    try:
        json_data = json.load(open(params['data']))
    except Exception as e:
        print 'failure open data %s, %s' % (params['data'], e.message)
        return

    key_id_list = tools.config_getstr(config, 'result_format_pmsignature', 'key_id')
    key_ref = tools.config_getstr(config, 'result_format_pmsignature', 'key_ref')
    key_alt = tools.config_getstr(config, 'result_format_pmsignature', 'key_alt')
    key_strand = tools.config_getstr(config, 'result_format_pmsignature', 'key_strand')
    key_mutations = tools.config_getstr(config, 'result_format_pmsignature', 'key_mutation')
    key_mutation_count = tools.config_getstr(config, 'result_format_pmsignature', 'key_mutation_count')
    sig_num = len(json_data[key_ref])
    if sig_num == 0:
        print 'no data %s' % params['data']
        return {}
    else:
        signature_list = []
        for s in range(sig_num):
            signature_list.append('Signature %d' % (s + 1))

        sig_color_list = color.create_color_array(sig_num, color.r_set2)
        if tools.config_getboolean(config, 'result_format_pmsignature', 'background'):
            signature_list.append('Background ')
            sig_color_list.append(color.r_set2_gray)
        id_txt = ''
        if key_id_list in json_data:
            id_txt = convert.list_to_text(json_data[key_id_list])
        mutations_txt = ''
        if key_mutations in json_data:
            for m in json_data[key_mutations]:
                mutations_txt += '[%d,%d,%f],' % (m[0], m[1], m[2])

        dataset_ref = ''
        for sig in json_data[key_ref]:
            tmp = ''
            for sub in sig:
                tmp += '[' + (',').join(map(str, sub)) + '],'

            dataset_ref += '[' + tmp + '],'

        dataset_alt = ''
        for sig in json_data[key_alt]:
            tmp = ''
            for sub in sig:
                tmp += '[' + (',').join(map(str, sub)) + '],'

            dataset_alt += '[' + tmp + '],'

        dataset_strand = ''
        for sig in json_data[key_strand]:
            dataset_strand += '[' + (',').join(map(str, sig)) + '],'

        keys_di = {'a': '', 'c': '', 'g': '', 't': '', 'ca': '', 'cg': '', 'ct': '', 'ta': '', 'tc': '', 'tg': '', 'plus': '', 'minus': '', 'id': '', 'sig': ''}
        tooltip_refs_txt = ''
        for r in range(len(json_data[key_ref][0])):
            tooltip_refs_txt += js_tooltip_ref_template.format(index=r, tooltip_format=convert.pyformat_to_jstooltip_text(keys_di, config, 'pmsignature', '', 'tooltip_format_ref'))

        mutation_count_txt = ''
        if key_mutation_count != '' and key_mutation_count in json_data.keys():
            for v in json_data[key_mutation_count]:
                mutation_count_txt += '%d,' % v

        sig_num_sift = 0
        if tools.config_getboolean(config, 'result_format_pmsignature', 'background'):
            sig_num_sift = 1
        ellipsis = '%s%d' % (params['ellipsis'], sig_num + sig_num_sift)
        js_file = 'data_%s.js' % ellipsis
        html_file = 'graph_%s.html' % ellipsis
        f = open(params['dir'] + '/' + js_file, 'w')
        f.write(js_header + js_dataset.format(Ids=id_txt, color_A=tools.config_getstr(config, 'pmsignature', 'color_A', '#06B838'), color_C=tools.config_getstr(config, 'pmsignature', 'color_C', '#609CFF'), color_G=tools.config_getstr(config, 'pmsignature', 'color_G', '#B69D02'), color_T=tools.config_getstr(config, 'pmsignature', 'color_T', '#F6766D'), color_plus=tools.config_getstr(config, 'pmsignature', 'color_plus', '#00BEC3'), color_minus=tools.config_getstr(config, 'pmsignature', 'color_minus', '#F263E2'), signatures=convert.list_to_text(signature_list), colors=convert.list_to_text(sig_color_list), mutations=mutations_txt, dataset_ref=dataset_ref, dataset_alt=dataset_alt, dataset_strand=dataset_strand, tooltip_ref=tooltip_refs_txt, tooltip_alt=convert.pyformat_to_jstooltip_text(keys_di, config, 'pmsignature', '', 'tooltip_format_alt'), tooltip_strand=convert.pyformat_to_jstooltip_text(keys_di, config, 'pmsignature', '', 'tooltip_format_strand'), mutation_title=convert.pyformat_to_jstooltip_text(keys_di, config, 'pmsignature', '', 'tooltip_format_mutation_title'), mutation_partial=convert.pyformat_to_jstooltip_text(keys_di, config, 'pmsignature', '', 'tooltip_format_mutation_partial'), mutation_count=mutation_count_txt))
        f_template = open(os.path.dirname(os.path.abspath(__file__)) + '/templates/data_pmsignature.js')
        js_function = f_template.read()
        f_template.close()
        f.write(js_function)
        f.write(js_footer)
        f.close()
        integral = True
        if key_id_list == '' or key_mutations == '' or key_mutation_count == '':
            integral = False
        return {'sig_num': sig_num, 'js': js_file, 
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
    f_template = open(os.path.dirname(os.path.abspath(__file__)) + '/templates/graph_pmsignature.html')
    html_template = f_template.read()
    f_template.close()
    sig_num_sift = 0
    if tools.config_getboolean(config, 'result_format_pmsignature', 'background'):
        sig_num_sift = 1
    f_html = open(params['dir'] + '/' + dataset['html'], 'w')
    f_html.write(html_template.format(project=params['project'], title='%s(#sig %d)' % (params['title'], dataset['sig_num'] + sig_num_sift), data_js=dataset['js'], version=prep.version_text(), date=tools.now_string(), divs=div_text, add_divs=add_text, integral=integral_text, style='../style/%s' % os.path.basename(tools.config_getpath(config, 'style', 'path', 'default.js'))))
    f_html.close()