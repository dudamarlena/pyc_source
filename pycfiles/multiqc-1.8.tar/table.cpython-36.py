# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/philewels/GitHub/MultiQC/multiqc/plots/table.py
# Compiled at: 2019-11-13 08:16:50
# Size of source mod 2**32: 16414 bytes
""" MultiQC functions to plot a table """
from collections import defaultdict, OrderedDict
import logging, random
from multiqc.utils import config, report, util_functions, mqc_colour
from multiqc.plots import table_object, beeswarm
logger = logging.getLogger(__name__)
letters = 'abcdefghijklmnopqrstuvwxyz'

def plot(data, headers=None, pconfig=None):
    """ Return HTML for a MultiQC table.
    :param data: 2D dict, first keys as sample names, then x:y data pairs
    :param headers: list of optional dicts with column config in key:value pairs.
    :return: HTML ready to be inserted into the page
    """
    if headers is None:
        headers = []
    else:
        if pconfig is None:
            pconfig = {}
        if 'id' in pconfig:
            if pconfig['id']:
                if pconfig['id'] in config.custom_plot_config:
                    for k, v in config.custom_plot_config[pconfig['id']].items():
                        pconfig[k] = v

    dt = table_object.datatable(data, headers, pconfig)
    s_names = set()
    for d in dt.data:
        for s_name in d.keys():
            s_names.add(s_name)

    if len(s_names) >= config.max_table_rows and pconfig.get('no_beeswarm') is not True:
        logger.debug('Plotting beeswarm instead of table, {} samples'.format(len(s_names)))
        warning = '<p class="text-muted"><span class="glyphicon glyphicon-exclamation-sign" title="A beeswarm plot has been generated instead because of the large number of samples. See http://multiqc.info/docs/#tables--beeswarm-plots" data-toggle="tooltip"></span> Showing {} samples.</p>'.format(len(s_names))
        return warning + beeswarm.make_plot(dt)
    else:
        return make_table(dt)


def make_table(dt):
    """
    Build the HTML needed for a MultiQC table.
    :param data: MultiQC datatable object
    """
    table_id = dt.pconfig.get('id', 'table_{}'.format(''.join(random.sample(letters, 4))))
    table_id = report.save_htmlid(table_id)
    t_headers = OrderedDict()
    t_modal_headers = OrderedDict()
    t_rows = OrderedDict()
    t_rows_empty = OrderedDict()
    dt.raw_vals = defaultdict(lambda : dict())
    empty_cells = dict()
    hidden_cols = 1
    table_title = dt.pconfig.get('table_title')
    if table_title is None:
        table_title = table_id.replace('_', ' ').title()
    for idx, k, header in dt.get_headers_in_order():
        rid = header['rid']
        shared_key = ''
        if header.get('shared_key', None) is not None:
            shared_key = ' data-shared-key={}'.format(header['shared_key'])
        hide = ''
        muted = ''
        checked = ' checked="checked"'
        if header.get('hidden', False) is True:
            hide = 'hidden'
            muted = ' text-muted'
            checked = ''
            hidden_cols += 1
        data_attr = 'data-dmax="{}" data-dmin="{}" data-namespace="{}" {}'.format(header['dmax'], header['dmin'], header['namespace'], shared_key)
        cell_contents = '<span class="mqc_table_tooltip" title="{}: {}">{}</span>'.format(header['namespace'], header['description'], header['title'])
        t_headers[rid] = '<th id="header_{rid}" class="{rid} {h}" {da}>{c}</th>'.format(rid=rid,
          h=hide,
          da=data_attr,
          c=cell_contents)
        empty_cells[rid] = '<td class="data-coloured {rid} {h}"></td>'.format(rid=rid, h=hide)
        t_modal_headers[rid] = '\n        <tr class="{rid}{muted}" style="background-color: rgba({col}, 0.15);">\n          <td class="sorthandle ui-sortable-handle">||</span></td>\n          <td style="text-align:center;">\n            <input class="mqc_table_col_visible" type="checkbox" {checked} value="{rid}" data-target="#{tid}">\n          </td>\n          <td>{name}</td>\n          <td>{title}</td>\n          <td>{desc}</td>\n          <td>{col_id}</td>\n          <td>{sk}</td>\n        </tr>'.format(rid=rid,
          muted=muted,
          checked=checked,
          tid=table_id,
          col=(header['colour']),
          name=(header['namespace']),
          title=(header['title']),
          desc=(header['description']),
          col_id=('<code>{}</code>'.format(k)),
          sk=(header.get('shared_key', '')))
        if header['scale'] == False:
            c_scale = None
        else:
            c_scale = mqc_colour.mqc_colour_scale(header['scale'], header['dmin'], header['dmax'])
        for s_name, samp in dt.data[idx].items():
            if k in samp:
                val = samp[k]
                kname = '{}_{}'.format(header['namespace'], rid)
                dt.raw_vals[s_name][kname] = val
                if 'modify' in header:
                    if callable(header['modify']):
                        val = header['modify'](val)
                try:
                    dmin = header['dmin']
                    dmax = header['dmax']
                    percentage = (float(val) - dmin) / (dmax - dmin) * 100
                    percentage = min(percentage, 100)
                    percentage = max(percentage, 0)
                except (ZeroDivisionError, ValueError):
                    percentage = 0

                try:
                    valstring = str(header['format'].format(val))
                except ValueError:
                    try:
                        valstring = str(header['format'].format(float(val)))
                    except ValueError:
                        valstring = str(val)

                except:
                    valstring = str(val)

                if config.thousandsSep_format is None:
                    config.thousandsSep_format = '<span class="mqc_thousandSep"></span>'
                if config.decimalPoint_format is None:
                    config.decimalPoint_format = '.'
                valstring = valstring.replace('.', 'DECIMAL').replace(',', 'THOUSAND')
                valstring = valstring.replace('DECIMAL', config.decimalPoint_format).replace('THOUSAND', config.thousandsSep_format)
                valstring += header.get('suffix', '')
                cmatches = {cfck:False for cfc in config.table_cond_formatting_colours for cfck in cfc}
                for cfk in ['all_columns', rid]:
                    if cfk in config.table_cond_formatting_rules:
                        for ftype in cmatches.keys():
                            for cmp in config.table_cond_formatting_rules[cfk].get(ftype, []):
                                try:
                                    if 's_eq' in cmp:
                                        if str(cmp['s_eq']).lower() == str(val).lower():
                                            cmatches[ftype] = True
                                        else:
                                            if 's_contains' in cmp:
                                                if str(cmp['s_contains']).lower() in str(val).lower():
                                                    cmatches[ftype] = True
                                                else:
                                                    if 's_ne' in cmp:
                                                        if str(cmp['s_ne']).lower() != str(val).lower():
                                                            cmatches[ftype] = True
                                                    if 'eq' in cmp:
                                                        if float(cmp['eq']) == float(val):
                                                            cmatches[ftype] = True
                                            else:
                                                if 'ne' in cmp:
                                                    if float(cmp['ne']) != float(val):
                                                        cmatches[ftype] = True
                                            if 'gt' in cmp:
                                                if float(cmp['gt']) < float(val):
                                                    cmatches[ftype] = True
                                    else:
                                        if 'lt' in cmp:
                                            if float(cmp['lt']) > float(val):
                                                cmatches[ftype] = True
                                except:
                                    logger.warn("Not able to apply table conditional formatting to '{}' ({})".format(val, cmp))

                bgcol = None
                for cfc in config.table_cond_formatting_colours:
                    for cfck in cfc:
                        if cmatches[cfck]:
                            bgcol = cfc[cfck]

                if bgcol is not None:
                    valstring = '<span class="badge" style="background-color:{}">{}</span>'.format(bgcol, valstring)
                if not header['scale']:
                    if s_name not in t_rows:
                        t_rows[s_name] = dict()
                    t_rows[s_name][rid] = '<td class="{rid} {h}">{v}</td>'.format(rid=rid, h=hide, v=valstring)
                else:
                    if c_scale is not None:
                        col = ' background-color:{};'.format(c_scale.get_colour(val))
                    else:
                        col = ''
                    bar_html = '<span class="bar" style="width:{}%;{}"></span>'.format(percentage, col)
                    val_html = '<span class="val">{}</span>'.format(valstring)
                    wrapper_html = '<div class="wrapper">{}{}</div>'.format(bar_html, val_html)
                    if s_name not in t_rows:
                        t_rows[s_name] = dict()
                    t_rows[s_name][rid] = '<td class="data-coloured {rid} {h}">{c}</td>'.format(rid=rid, h=hide, c=wrapper_html)
                if s_name not in t_rows_empty:
                    t_rows_empty[s_name] = dict()
                t_rows_empty[s_name][rid] = header.get('hidden', False) or str(val).strip() == ''

        if sum([len(rows) for rows in t_rows.values()]) == 0:
            t_headers.pop(rid, None)
            t_modal_headers.pop(rid, None)
            logger.debug('Removing header {} from general stats table, as no data'.format(k))

    html = ''
    if not config.simple_output:
        html += '\n        <button type="button" class="mqc_table_copy_btn btn btn-default btn-sm" data-clipboard-target="#{tid}">\n            <span class="glyphicon glyphicon-copy"></span> Copy table\n        </button>\n        '.format(tid=table_id)
        if len(t_headers) > 1:
            html += '\n            <button type="button" class="mqc_table_configModal_btn btn btn-default btn-sm" data-toggle="modal" data-target="#{tid}_configModal">\n                <span class="glyphicon glyphicon-th"></span> Configure Columns\n            </button>\n            '.format(tid=table_id)
        html += '\n        <button type="button" class="mqc_table_sortHighlight btn btn-default btn-sm" data-target="#{tid}" data-direction="desc" style="display:none;">\n            <span class="glyphicon glyphicon-sort-by-attributes-alt"></span> Sort by highlight\n        </button>\n        '.format(tid=table_id)
        if len(t_headers) > 1:
            html += '\n            <button type="button" class="mqc_table_makeScatter btn btn-default btn-sm" data-toggle="modal" data-target="#tableScatterModal" data-table="#{tid}">\n                <span class="glyphicon glyphicon glyphicon-stats"></span> Plot\n            </button>\n            '.format(tid=table_id)
        row_visibilities = [all(t_rows_empty[s_name].values()) for s_name in t_rows_empty]
        visible_rows = [x for x in row_visibilities if not x]
        html += '\n        <small id="{tid}_numrows_text" class="mqc_table_numrows_text">Showing <sup id="{tid}_numrows" class="mqc_table_numrows">{nvisrows}</sup>/<sub>{nrows}</sub> rows and <sup id="{tid}_numcols" class="mqc_table_numcols">{ncols_vis}</sup>/<sub>{ncols}</sub> columns.</small>\n        '.format(tid=table_id, nvisrows=(len(visible_rows)), nrows=(len(t_rows)), ncols_vis=(len(t_headers) + 1 - hidden_cols), ncols=(len(t_headers)))
    collapse_class = 'mqc-table-collapse' if (len(t_rows) > 10 and config.collapse_tables) else ''
    html += '\n        <div id="{tid}_container" class="mqc_table_container">\n            <div class="table-responsive mqc-table-responsive {cc}">\n                <table id="{tid}" class="table table-condensed mqc_table" data-title="{title}">\n        '.format(tid=table_id, title=table_title, cc=collapse_class)
    col1_header = dt.pconfig.get('col1_header', 'Sample Name')
    html += '<thead><tr><th class="rowheader">{}</th>{}</tr></thead>'.format(col1_header, ''.join(t_headers.values()))
    html += '<tbody>'
    t_row_keys = t_rows.keys()
    if dt.pconfig.get('sortRows') is not False:
        t_row_keys = sorted(t_row_keys)
    for s_name in t_row_keys:
        row_hidden = ' style="display:none"' if all(t_rows_empty[s_name].values()) else ''
        html += '<tr{}>'.format(row_hidden)
        html += '<th class="rowheader" data-original-sn="{sn}">{sn}</th>'.format(sn=s_name)
        for k in t_headers:
            html += t_rows[s_name].get(k, empty_cells[k])

        html += '</tr>'

    html += '</tbody></table></div>'
    if len(t_rows) > 10:
        if config.collapse_tables:
            html += '<div class="mqc-table-expand"><span class="glyphicon glyphicon-chevron-down" aria-hidden="true"></span></div>'
    html += '</div>'
    if not config.simple_output:
        html += '\n    <!-- MultiQC Table Columns Modal -->\n    <div class="modal fade" id="{tid}_configModal" tabindex="-1">\n      <div class="modal-dialog modal-lg">\n        <div class="modal-content">\n          <div class="modal-header">\n            <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>\n            <h4 class="modal-title">{title}: Columns</h4>\n          </div>\n          <div class="modal-body">\n            <p>Uncheck the tick box to hide columns. Click and drag the handle on the left to change order.</p>\n            <p>\n                <button class="btn btn-default btn-sm mqc_configModal_bulkVisible" data-target="#{tid}" data-action="showAll">Show All</button>\n                <button class="btn btn-default btn-sm mqc_configModal_bulkVisible" data-target="#{tid}" data-action="showNone">Show None</button>\n            </p>\n            <table class="table mqc_table mqc_sortable mqc_configModal_table" id="{tid}_configModal_table" data-title="{title}">\n              <thead>\n                <tr>\n                  <th class="sorthandle" style="text-align:center;">Sort</th>\n                  <th style="text-align:center;">Visible</th>\n                  <th>Group</th>\n                  <th>Column</th>\n                  <th>Description</th>\n                  <th>ID</th>\n                  <th>Scale</th>\n                </tr>\n              </thead>\n              <tbody>\n                {trows}\n              </tbody>\n            </table>\n        </div>\n        <div class="modal-footer"> <button type="button" class="btn btn-default" data-dismiss="modal">Close</button> </div>\n    </div> </div> </div>'.format(tid=table_id, title=table_title, trows=(''.join(t_modal_headers.values())))
    if dt.pconfig.get('save_file') is True:
        fn = dt.pconfig.get('raw_data_fn', 'multiqc_{}'.format(table_id))
        util_functions.write_data_file(dt.raw_vals, fn)
        report.saved_raw_data[fn] = dt.raw_vals
    return html