# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/philewels/GitHub/MultiQC/multiqc/modules/custom_content/custom_content.py
# Compiled at: 2019-11-20 10:26:16
""" Core MultiQC module to parse output from custom script output """
from __future__ import print_function
import base64
from collections import defaultdict, OrderedDict
import logging, json, os, yaml
from multiqc import config
from multiqc.utils import report
from multiqc.modules.base_module import BaseMultiqcModule
from multiqc.plots import table, bargraph, linegraph, scatter, heatmap, beeswarm
log = logging.getLogger(__name__)

def yaml_ordered_load(stream):

    class OrderedLoader(yaml.SafeLoader):
        pass

    def construct_mapping(loader, node):
        loader.flatten_mapping(node)
        return OrderedDict(loader.construct_pairs(node))

    OrderedLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, construct_mapping)
    return yaml.load(stream, OrderedLoader)


def custom_module_classes():
    """
    MultiQC Custom Content class. This module does a lot of different
    things depending on the input and is as flexible as possible.

    NB: THIS IS TOTALLY DIFFERENT TO ALL OTHER MODULES
    """
    cust_mods = defaultdict(lambda : defaultdict(lambda : OrderedDict()))
    search_patterns = [
     'custom_content']
    config_data = getattr(config, 'custom_data', {})
    for k, f in config_data.items():
        if type(f) != dict:
            log.debug(('config.custom_data row was not a dictionary: {}').format(k))
            continue
        c_id = f.get('id', k)
        if 'data' in f:
            cust_mods[c_id]['data'].update(f['data'])
            cust_mods[c_id]['config'].update({k:v for k, v in f.items() if k is not 'data' if k is not 'data'})
            cust_mods[c_id]['config']['id'] = cust_mods[c_id]['config'].get('id', c_id)
            continue
        if c_id in report.files:
            cust_mods[c_id]['config'] = f
            cust_mods[c_id]['config']['id'] = cust_mods[c_id]['config'].get('id', c_id)
            search_patterns.append(c_id)
            continue
        log.warn(("Found section '{}' in config for under custom_data, but no data or search patterns.").format(c_id))

    bm = BaseMultiqcModule()
    for k in search_patterns:
        num_sp_found_files = 0
        for f in bm.find_log_files(k):
            num_sp_found_files += 1
            try:
                f_extension = os.path.splitext(f['fn'])[1]
                parsed_data = None
                if f_extension == '.yaml' or f_extension == '.yml':
                    try:
                        parsed_data = yaml_ordered_load(f['f'])
                    except Exception as e:
                        log.warning(("Error parsing YAML file '{}' (probably invalid YAML)").format(f['fn']))
                        log.debug(('YAML error: {}').format(e), exc_info=True)
                        break

                else:
                    if f_extension == '.json':
                        try:
                            parsed_data = json.loads(f['f'], object_pairs_hook=OrderedDict)
                        except Exception as e:
                            log.warning(("Error parsing JSON file '{}' (probably invalid JSON)").format(f['fn']))
                            log.warning(('JSON error: {}').format(e))
                            break

                    elif f_extension == '.png' or f_extension == '.jpeg' or f_extension == '.jpg':
                        image_string = base64.b64encode(f['f'].read()).decode('utf-8')
                        image_format = 'png' if f_extension == '.png' else 'jpg'
                        img_html = ('<div class="mqc-custom-content-image"><img src="data:image/{};base64,{}" /></div>').format(image_format, image_string)
                        parsed_data = {'id': f['s_name'], 
                           'plot_type': 'image', 
                           'section_name': f['s_name'].replace('_', ' ').replace('-', ' ').replace('.', ' '), 
                           'description': ('Embedded image <code>{}</code>').format(f['fn']), 
                           'data': img_html}
                    if parsed_data is not None:
                        c_id = parsed_data.get('id', k)
                        if len(parsed_data.get('data', {})) > 0:
                            if type(parsed_data['data']) == str:
                                cust_mods[c_id]['data'] = parsed_data['data']
                            else:
                                cust_mods[c_id]['data'].update(parsed_data['data'])
                            cust_mods[c_id]['config'].update({j:k for j, k in parsed_data.items() if j != 'data' if j != 'data'})
                        else:
                            log.warning(('No data found in {}').format(f['fn']))
                    else:
                        m_config = _find_file_header(f)
                        s_name = None
                        if m_config is not None:
                            c_id = m_config.get('id', k)
                            b_config = cust_mods.get(c_id, {}).get('config', {})
                            b_config.update(m_config)
                            m_config = dict(b_config)
                            s_name = m_config.get('sample_name')
                        else:
                            c_id = k
                            m_config = cust_mods.get(c_id, {}).get('config', {})
                        if s_name is None:
                            s_name = bm.clean_s_name(f['s_name'], f['root'])
                        if k == 'custom_content':
                            c_id = s_name
                        if 'files' not in m_config:
                            m_config['files'] = dict()
                        m_config['files'].update({s_name: {'fn': f['fn'], 'root': f['root']}})
                        if m_config.get('file_format') is None:
                            m_config['file_format'] = _guess_file_format(f)
                        try:
                            parsed_data, conf = _parse_txt(f, m_config)
                            if parsed_data is None or len(parsed_data) == 0:
                                log.warning(('Not able to parse custom data in {}').format(f['fn']))
                            else:
                                if conf.get('id') is not None:
                                    c_id = conf.get('id')
                                if type(parsed_data) == list:
                                    cust_mods[c_id]['data'] = parsed_data
                                elif conf.get('plot_type') == 'html':
                                    cust_mods[c_id]['data'] = parsed_data
                                else:
                                    cust_mods[c_id]['data'].update(parsed_data)
                                cust_mods[c_id]['config'].update(conf)
                        except (IndexError, AttributeError, TypeError):
                            log.error(('Unexpected parsing error for {}').format(f['fn']), exc_info=True)
                            raise

            except Exception as e:
                log.error(("Uncaught exception raised for file '{}'").format(f['fn']))
                log.exception(e)

        if num_sp_found_files == 0 and k != 'custom_content':
            log.debug(('No samples found: custom content ({})').format(k))

    for k in cust_mods:
        cust_mods[k]['data'] = bm.ignore_samples(cust_mods[k]['data'])

    remove_cids = [ k for k in cust_mods if len(cust_mods[k]['data']) == 0 ]
    for k in remove_cids:
        del cust_mods[k]

    if len(cust_mods) == 0:
        raise UserWarning
    parsed_modules = list()
    for module_id, mod in cust_mods.items():
        if mod['config'].get('plot_type') == 'generalstats':
            gsheaders = mod['config'].get('pconfig')
            if gsheaders is None:
                headers = set()
                for d in mod['data'].values():
                    headers.update(d.keys())

                headers = list(headers)
                headers.sort()
                gsheaders = OrderedDict()
                for h in headers:
                    gsheaders[h] = dict()

            if type(gsheaders) == list:
                gsheaders_dict = OrderedDict()
                for gsheader in gsheaders:
                    for col_id, col_data in gsheader.items():
                        gsheaders_dict[col_id] = col_data

                gsheaders = gsheaders_dict
            for m_id in gsheaders:
                if 'namespace' not in gsheaders[m_id]:
                    gsheaders[m_id]['namespace'] = mod['config'].get('namespace', module_id)

            bm.general_stats_addcols(mod['data'], gsheaders)
        else:
            parsed_modules.append(MultiqcModule(module_id, mod))
            if mod['config'].get('plot_type') == 'html':
                log.info(('{}: Found 1 sample (html)').format(module_id))
            if mod['config'].get('plot_type') == 'image':
                log.info(('{}: Found 1 sample (image)').format(module_id))
            else:
                log.info(('{}: Found {} samples ({})').format(module_id, len(mod['data']), mod['config'].get('plot_type')))

    mod_order = getattr(config, 'custom_content', {}).get('order', [])
    sorted_modules = [ parsed_mod for parsed_mod in parsed_modules if parsed_mod.anchor not in mod_order ]
    sorted_modules.extend([ parsed_mod for mod_id in mod_order for parsed_mod in parsed_modules if parsed_mod.anchor == mod_id ])
    if len(sorted_modules) == 0:
        raise UserWarning
    return sorted_modules


class MultiqcModule(BaseMultiqcModule):
    """ Module class, used for each custom content type """

    def __init__(self, c_id, mod):
        modname = mod['config'].get('section_name', c_id.replace('_', ' ').title())
        if modname == '' or modname is None:
            modname = 'Custom Content'
        super(MultiqcModule, self).__init__(name=modname, anchor=mod['config'].get('section_anchor', c_id), href=mod['config'].get('section_href'), info=mod['config'].get('description'))
        pconfig = mod['config'].get('pconfig', {})
        if pconfig.get('title') is None:
            pconfig['title'] = modname
        if mod['config'].get('plot_type') == 'table':
            pconfig['sortRows'] = pconfig.get('sortRows', False)
            headers = mod['config'].get('headers')
            self.add_section(plot=table.plot(mod['data'], headers, pconfig))
            self.write_data_file(mod['data'], ('multiqc_{}').format(modname.lower().replace(' ', '_')))
        elif mod['config'].get('plot_type') == 'bargraph':
            self.add_section(plot=bargraph.plot(mod['data'], mod['config'].get('categories'), pconfig))
        elif mod['config'].get('plot_type') == 'linegraph':
            self.add_section(plot=linegraph.plot(mod['data'], pconfig))
        elif mod['config'].get('plot_type') == 'scatter':
            self.add_section(plot=scatter.plot(mod['data'], pconfig))
        elif mod['config'].get('plot_type') == 'heatmap':
            self.add_section(plot=heatmap.plot(mod['data'], mod['config'].get('xcats'), mod['config'].get('ycats'), pconfig))
        elif mod['config'].get('plot_type') == 'beeswarm':
            self.add_section(plot=beeswarm.plot(mod['data'], pconfig))
        elif mod['config'].get('plot_type') == 'html':
            self.add_section(content=mod['data'])
        elif mod['config'].get('plot_type') == 'image':
            self.add_section(content=mod['data'])
        elif mod['config'].get('plot_type') == None:
            log.warning(("Plot type not found for content ID '{}'").format(c_id))
        else:
            log.warning(("Error - custom content plot type '{}' not recognised for content ID {}").format(mod['config'].get('plot_type'), c_id))
        return


def _find_file_header(f):
    hlines = []
    for l in f['f'].splitlines():
        if l.startswith('#'):
            hlines.append(l[1:])

    if len(hlines) == 0:
        return
    else:
        hconfig = None
        try:
            hconfig = yaml.safe_load(('\n').join(hlines))
            assert isinstance(hconfig, dict)
        except yaml.YAMLError as e:
            log.warn(('Could not parse comment file header for MultiQC custom content: {}').format(f['fn']))
            log.debug(e)
        except AssertionError:
            log.debug(('Custom Content comment file header looked wrong: {}').format(hconfig))
        else:
            return hconfig

        return


def _guess_file_format(f):
    """
    Tries to guess file format, first based on file extension (csv / tsv),
    then by looking for common column separators in the first 10 non-commented lines.
    Splits by tab / comma / space and counts resulting number of columns. Finds the most
    common column count, then comparsed how many lines had this number.
    eg. if tab, all 10 lines should have x columns when split by tab.
    Returns: csv | tsv | spaces   (spaces by default if all else fails)
    """
    filename, file_extension = os.path.splitext(f['fn'])
    tabs = []
    commas = []
    spaces = []
    j = 0
    for l in f['f'].splitlines():
        if not l.startswith('#'):
            j += 1
            tabs.append(len(l.split('\t')))
            commas.append(len(l.split(',')))
            spaces.append(len(l.split()))
        if j == 10:
            break

    tab_mode = max(set(tabs), key=tabs.count)
    commas_mode = max(set(commas), key=commas.count)
    spaces_mode = max(set(spaces), key=spaces.count)
    tab_lc = tabs.count(tab_mode) if tab_mode > 1 else 0
    commas_lc = commas.count(commas_mode) if commas_mode > 1 else 0
    spaces_lc = spaces.count(spaces_mode) if spaces_mode > 1 else 0
    if tab_lc == j:
        return 'tsv'
    if commas_lc == j:
        return 'csv'
    if tab_lc > commas_lc and tab_lc > spaces_lc:
        return 'tsv'
    if commas_lc > tab_lc and commas_lc > spaces_lc:
        return 'csv'
    if spaces_lc > tab_lc and spaces_lc > commas_lc:
        return 'spaces'
    if tab_mode == commas_lc and tab_mode > spaces_lc:
        if tab_mode > commas_mode:
            return 'tsv'
        else:
            return 'csv'

    return 'spaces'


def _parse_txt(f, conf):
    sep = None
    if conf['file_format'] == 'csv':
        sep = ','
    if conf['file_format'] == 'tsv':
        sep = '\t'
    lines = f['f'].splitlines()
    d = []
    if conf.get('plot_type') == 'html':
        for l in lines:
            if l and not l.startswith('#'):
                d.append(l)

        return (
         ('\n').join(d), conf)
    ncols = None
    for l in lines:
        if l and not l.startswith('#'):
            sections = l.split(sep)
            d.append(sections)
            if ncols is None:
                ncols = len(sections)
            elif ncols != len(sections):
                log.warn(('Inconsistent number of columns found in {}! Skipping..').format(f['fn']))
                return (
                 None, conf)

    first_row_str = 0
    for i, l in enumerate(d):
        for j, v in enumerate(l):
            try:
                d[i][j] = float(v)
            except ValueError:
                if v.startswith('"') and v.endswith('"') or v.startswith("'") and v.endswith("'"):
                    v = v[1:-1]
                d[i][j] = v
                if i == 0:
                    first_row_str += 1

    all_numeric = all([ type(l) == float for l in d[i][1:] for i in range(1, len(d)) ])
    if conf.get('plot_type') == 'generalstats' and len(d) >= 2 and ncols >= 2:
        data = defaultdict(dict)
        for i, l in enumerate(d[1:], 1):
            for j, v in enumerate(l[1:], 1):
                data[l[0]][d[0][j]] = v

        return (
         data, conf)
    else:
        if conf.get('plot_type') is None and first_row_str == len(lines) and all_numeric:
            conf['plot_type'] = 'heatmap'
        if conf.get('plot_type') == 'heatmap':
            conf['xcats'] = d[0][1:]
            conf['ycats'] = [ s[0] for s in d[1:] ]
            data = [ s[1:] for s in d[1:] ]
            return (
             data, conf)
        if first_row_str == len(d[0]) or conf.get('plot_type') == 'table':
            data = OrderedDict()
            for s in d[1:]:
                data[s[0]] = OrderedDict()
                for i, v in enumerate(s[1:]):
                    cat = str(d[0][(i + 1)])
                    data[s[0]][cat] = v

            if conf.get('plot_type') is None:
                allfloats = True
                for r in d[1:]:
                    for v in r[1:]:
                        allfloats = allfloats and type(v) == float

                if allfloats:
                    conf['plot_type'] = 'bargraph'
                else:
                    conf['plot_type'] = 'table'
            if conf.get('plot_type') == 'table' and d[0][0].strip() != '':
                conf['pconfig'] = conf.get('pconfig', {})
                if not conf['pconfig'].get('col1_header'):
                    conf['pconfig']['col1_header'] = d[0][0].strip()
            if conf.get('plot_type') == 'bargraph' or conf.get('plot_type') == 'table':
                return (data, conf)
            data = OrderedDict()
        if conf.get('plot_type') is None and len(d[0]) == 3 and type(d[0][0]) != float and type(d[0][1]) == float and type(d[0][2]) == float:
            conf['plot_type'] = 'scatter'
        if conf.get('plot_type') == 'scatter':
            data = dict()
            for s in d:
                try:
                    data[s[0]] = {'x': float(s[1]), 
                       'y': float(s[2])}
                except (IndexError, ValueError):
                    pass

            return (data, conf)
        if len(d[0]) == 2:
            if conf.get('plot_type') is None and type(d[0][0]) == float and type(d[0][1]) == float:
                conf['plot_type'] = 'linegraph'
            if conf.get('plot_type') is None and type(d[0][0]) != float and type(d[0][1]) == float:
                conf['plot_type'] = 'bargraph'
            if conf.get('plot_type') == 'linegraph' or conf.get('plot_type') == 'bargraph':
                if conf.get('id') is None:
                    conf['id'] = os.path.basename(f['root'])
                data = OrderedDict()
                for s in d:
                    data[s[0]] = s[1]

                return ({f['s_name']: data}, conf)
        if conf.get('plot_type') is None and len(d[0]) > 4 and all_numeric:
            conf['plot_type'] = 'linegraph'
        if conf.get('plot_type') == 'linegraph':
            data = dict()
            for s in d:
                data[s[0]] = dict()
                for i, v in enumerate(s[1:]):
                    j = i + 1
                    data[s[0]][i + 1] = v

            return (
             data, conf)
        log.debug(("Not able to figure out a plot type for '{}' ").format(f['fn']) + ('plot type = {}, all numeric = {}, first row str = {}').format(conf.get('plot_type'), all_numeric, first_row_str))
        return (None, conf)