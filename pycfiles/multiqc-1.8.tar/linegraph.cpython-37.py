# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/philewels/GitHub/MultiQC/multiqc/plots/linegraph.py
# Compiled at: 2019-11-20 06:36:42
# Size of source mod 2**32: 20079 bytes
""" MultiQC functions to plot a linegraph """
from __future__ import print_function, division
from collections import OrderedDict
import base64, io, logging, os, random, sys
from multiqc.utils import config, report, util_functions
logger = logging.getLogger(__name__)
try:
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    logger.debug('Using matplotlib version {}'.format(matplotlib.__version__))
except Exception as e:
    try:
        print('##### ERROR! MatPlotLib library could not be loaded!    #####', file=(sys.stderr))
        print('##### Flat plots will instead be plotted as interactive #####', file=(sys.stderr))
        print(e)
    finally:
        e = None
        del e

letters = 'abcdefghijklmnopqrstuvwxyz'
_template_mod = None

def get_template_mod():
    global _template_mod
    if not _template_mod:
        _template_mod = config.avail_templates[config.template].load()
    return _template_mod


def plot(data, pconfig=None):
    """ Plot a line graph with X,Y data.
    :param data: 2D dict, first keys as sample names, then x:y data pairs
    :param pconfig: optional dict with config key:value pairs. See CONTRIBUTING.md
    :return: HTML and JS, ready to be inserted into the page
    """
    if pconfig is None:
        pconfig = {}
    else:
        if 'id' in pconfig:
            if pconfig['id']:
                if pconfig['id'] in config.custom_plot_config:
                    for k, v in config.custom_plot_config[pconfig['id']].items():
                        pconfig[k] = v

            elif type(data) is not list:
                data = [
                 data]
            else:
                if pconfig.get('smooth_points', None) is not None:
                    sumcounts = pconfig.get('smooth_points_sumcounts', True)
                    for i, d in enumerate(data):
                        if type(sumcounts) is list:
                            sumc = sumcounts[i]
                        else:
                            sumc = sumcounts
                        data[i] = smooth_line_data(d, pconfig['smooth_points'], sumc)

                for idx, yp in enumerate(pconfig.get('yPlotLines', [])):
                    pconfig['yPlotLines'][idx]['width'] = pconfig['yPlotLines'][idx].get('width', 2)

                if pconfig.get('ylab') is None:
                    try:
                        pconfig['ylab'] = pconfig['data_labels'][0]['ylab']
                    except (KeyError, IndexError):
                        pass

            if pconfig.get('xlab') is None:
                try:
                    pconfig['xlab'] = pconfig['data_labels'][0]['xlab']
                except (KeyError, IndexError):
                    pass

        else:
            plotdata = list()
            for data_index, d in enumerate(data):
                thisplotdata = list()
                for s in sorted(d.keys()):
                    series_config = pconfig.copy()
                    if 'data_labels' in pconfig:
                        if type(pconfig['data_labels'][data_index]) is dict:
                            series_config.update(pconfig['data_labels'][data_index])
                    else:
                        pairs = list()
                        maxval = 0
                        if 'categories' in series_config:
                            pconfig['categories'] = list()
                            for k in d[s].keys():
                                pconfig['categories'].append(k)
                                pairs.append(d[s][k])
                                maxval = max(maxval, d[s][k])

                        else:
                            for k in sorted(d[s].keys()):
                                if k is not None:
                                    if 'xmax' in series_config:
                                        if float(k) > float(series_config['xmax']):
                                            continue
                                    if 'xmin' in series_config:
                                        if float(k) < float(series_config['xmin']):
                                            continue
                                if d[s][k] is not None:
                                    if 'ymax' in series_config:
                                        if float(d[s][k]) > float(series_config['ymax']):
                                            continue
                                    if 'ymin' in series_config:
                                        if float(d[s][k]) < float(series_config['ymin']):
                                            continue
                                pairs.append([k, d[s][k]])
                                try:
                                    maxval = max(maxval, d[s][k])
                                except TypeError:
                                    pass

                    if not maxval > 0:
                        if series_config.get('hide_empty') is not True:
                            this_series = {'name':s, 
                             'data':pairs}
                            try:
                                this_series['color'] = series_config['colors'][s]
                            except:
                                pass

                        thisplotdata.append(this_series)

                plotdata.append(thisplotdata)

            try:
                if pconfig.get('extra_series'):
                    extra_series = pconfig['extra_series']
                    if type(pconfig['extra_series']) == dict:
                        extra_series = [
                         [
                          pconfig['extra_series']]]
                    else:
                        if type(pconfig['extra_series']) == list:
                            if type(pconfig['extra_series'][0]) == dict:
                                extra_series = [
                                 pconfig['extra_series']]
                        for i, es in enumerate(extra_series):
                            for s in es:
                                plotdata[i].append(s)

            except (KeyError, IndexError):
                pass

        try:
            return get_template_mod().linegraph(plotdata, pconfig)
        except (AttributeError, TypeError):
            if config.plots_force_flat or (config.plots_force_interactive or len(plotdata[0])) > config.plots_flat_numseries:
                try:
                    return matplotlib_linegraph(plotdata, pconfig)
                except Exception as e:
                    try:
                        logger.error('############### Error making MatPlotLib figure! Falling back to HighCharts.')
                        logger.debug(e, exc_info=True)
                        return highcharts_linegraph(plotdata, pconfig)
                    finally:
                        e = None
                        del e

            else:
                if config.export_plots:
                    matplotlib_linegraph(plotdata, pconfig)
                return highcharts_linegraph(plotdata, pconfig)


def highcharts_linegraph(plotdata, pconfig=None):
    """
    Build the HTML needed for a HighCharts line graph. Should be
    called by linegraph.plot(), which properly formats input data.
    """
    if pconfig is None:
        pconfig = {}
    if pconfig.get('id') is None:
        pconfig['id'] = 'mqc_hcplot_' + ''.join(random.sample(letters, 10))
    pconfig['id'] = report.save_htmlid(pconfig['id'])
    html = '<div class="mqc_hcplot_plotgroup">'
    if len(plotdata) > 1:
        html += '<div class="btn-group hc_switch_group">\n'
        for k, p in enumerate(plotdata):
            active = 'active' if k == 0 else ''
            try:
                name = pconfig['data_labels'][k]['name']
            except:
                name = k + 1

            try:
                ylab = 'data-ylab="{}"'.format(pconfig['data_labels'][k]['ylab'])
            except:
                ylab = 'data-ylab="{}"'.format(name) if name != k + 1 else ''

            try:
                ymax = 'data-ymax="{}"'.format(pconfig['data_labels'][k]['ymax'])
            except:
                ymax = ''

            try:
                xlab = 'data-xlab="{}"'.format(pconfig['data_labels'][k]['xlab'])
            except:
                xlab = ''

            html += '<button class="btn btn-default btn-sm {a}" data-action="set_data" {y} {ym} {x} data-newdata="{k}" data-target="{id}">{n}</button>\n'.format(a=active, id=(pconfig['id']), n=name, y=ylab, ym=ymax, x=xlab, k=k)

        html += '</div>\n\n'
    html += '<div class="hc-plot-wrapper"><div id="{id}" class="hc-plot not_rendered hc-line-plot"><small>loading..</small></div></div></div> \n'.format(id=(pconfig['id']))
    report.num_hc_plots += 1
    report.plot_data[pconfig['id']] = {'plot_type':'xy_line', 
     'datasets':plotdata, 
     'config':pconfig}
    return html


def matplotlib_linegraph--- This code section failed: ---

 L. 229         0  LOAD_FAST                'pconfig'
                2  LOAD_CONST               None
                4  COMPARE_OP               is
                6  POP_JUMP_IF_FALSE    12  'to 12'

 L. 230         8  BUILD_MAP_0           0 
               10  STORE_FAST               'pconfig'
             12_0  COME_FROM             6  '6'

 L. 233        12  LOAD_FAST                'pconfig'
               14  LOAD_METHOD              get
               16  LOAD_STR                 'id'
               18  CALL_METHOD_1         1  '1 positional argument'
               20  LOAD_CONST               None
               22  COMPARE_OP               is
               24  POP_JUMP_IF_FALSE    52  'to 52'

 L. 234        26  LOAD_STR                 'mqc_mplplot_'
               28  LOAD_STR                 ''
               30  LOAD_METHOD              join
               32  LOAD_GLOBAL              random
               34  LOAD_METHOD              sample
               36  LOAD_GLOBAL              letters
               38  LOAD_CONST               10
               40  CALL_METHOD_2         2  '2 positional arguments'
               42  CALL_METHOD_1         1  '1 positional argument'
               44  BINARY_ADD       
               46  LOAD_FAST                'pconfig'
               48  LOAD_STR                 'id'
               50  STORE_SUBSCR     
             52_0  COME_FROM            24  '24'

 L. 237        52  LOAD_GLOBAL              report
               54  LOAD_METHOD              save_htmlid
               56  LOAD_FAST                'pconfig'
               58  LOAD_STR                 'id'
               60  BINARY_SUBSCR    
               62  CALL_METHOD_1         1  '1 positional argument'
               64  LOAD_FAST                'pconfig'
               66  LOAD_STR                 'id'
               68  STORE_SUBSCR     

 L. 240        70  BUILD_LIST_0          0 
               72  STORE_FAST               'pids'

 L. 241        74  SETUP_LOOP          178  'to 178'
               76  LOAD_GLOBAL              range
               78  LOAD_GLOBAL              len
               80  LOAD_FAST                'plotdata'
               82  CALL_FUNCTION_1       1  '1 positional argument'
               84  CALL_FUNCTION_1       1  '1 positional argument'
               86  GET_ITER         
               88  FOR_ITER            176  'to 176'
               90  STORE_FAST               'k'

 L. 242        92  SETUP_EXCEPT        114  'to 114'

 L. 243        94  LOAD_FAST                'pconfig'
               96  LOAD_STR                 'data_labels'
               98  BINARY_SUBSCR    
              100  LOAD_FAST                'k'
              102  BINARY_SUBSCR    
              104  LOAD_STR                 'name'
              106  BINARY_SUBSCR    
              108  STORE_FAST               'name'
              110  POP_BLOCK        
              112  JUMP_FORWARD        134  'to 134'
            114_0  COME_FROM_EXCEPT     92  '92'

 L. 244       114  POP_TOP          
              116  POP_TOP          
              118  POP_TOP          

 L. 245       120  LOAD_FAST                'k'
              122  LOAD_CONST               1
              124  BINARY_ADD       
              126  STORE_FAST               'name'
              128  POP_EXCEPT       
              130  JUMP_FORWARD        134  'to 134'
              132  END_FINALLY      
            134_0  COME_FROM           130  '130'
            134_1  COME_FROM           112  '112'

 L. 246       134  LOAD_STR                 'mqc_{}_{}'
              136  LOAD_METHOD              format
              138  LOAD_FAST                'pconfig'
              140  LOAD_STR                 'id'
              142  BINARY_SUBSCR    
              144  LOAD_FAST                'name'
              146  CALL_METHOD_2         2  '2 positional arguments'
              148  STORE_FAST               'pid'

 L. 247       150  LOAD_GLOBAL              report
              152  LOAD_ATTR                save_htmlid
              154  LOAD_FAST                'pid'
              156  LOAD_CONST               True
              158  LOAD_CONST               ('skiplint',)
              160  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              162  STORE_FAST               'pid'

 L. 248       164  LOAD_FAST                'pids'
              166  LOAD_METHOD              append
              168  LOAD_FAST                'pid'
              170  CALL_METHOD_1         1  '1 positional argument'
              172  POP_TOP          
              174  JUMP_BACK            88  'to 88'
              176  POP_BLOCK        
            178_0  COME_FROM_LOOP       74  '74'

 L. 251       178  LOAD_STR                 '<p class="text-info"><small><span class="glyphicon glyphicon-picture" aria-hidden="true"></span> Flat image plot. Toolbox functions such as highlighting / hiding samples will not work (see the <a href="http://multiqc.info/docs/#flat--interactive-plots" target="_blank">docs</a>).</small></p>'
              180  STORE_FAST               'html'

 L. 253       182  LOAD_FAST                'html'
              184  LOAD_STR                 '<div class="mqc_mplplot_plotgroup" id="{}">'
              186  LOAD_METHOD              format
              188  LOAD_FAST                'pconfig'
              190  LOAD_STR                 'id'
              192  BINARY_SUBSCR    
              194  CALL_METHOD_1         1  '1 positional argument'
              196  INPLACE_ADD      
              198  STORE_FAST               'html'

 L. 256       200  LOAD_STR                 '#7cb5ec'
              202  LOAD_STR                 '#434348'
              204  LOAD_STR                 '#90ed7d'
              206  LOAD_STR                 '#f7a35c'
              208  LOAD_STR                 '#8085e9'

 L. 257       210  LOAD_STR                 '#f15c80'
              212  LOAD_STR                 '#e4d354'
              214  LOAD_STR                 '#2b908f'
              216  LOAD_STR                 '#f45b5b'
              218  LOAD_STR                 '#91e8e1'
              220  BUILD_LIST_10        10 
              222  STORE_FAST               'default_colors'

 L. 260       224  LOAD_GLOBAL              len
              226  LOAD_FAST                'plotdata'
              228  CALL_FUNCTION_1       1  '1 positional argument'
              230  LOAD_CONST               1
              232  COMPARE_OP               >
          234_236  POP_JUMP_IF_FALSE   374  'to 374'
              238  LOAD_GLOBAL              config
              240  LOAD_ATTR                simple_output
          242_244  POP_JUMP_IF_TRUE    374  'to 374'

 L. 261       246  LOAD_FAST                'html'
              248  LOAD_STR                 '<div class="btn-group mpl_switch_group mqc_mplplot_bargraph_switchds">\n'
              250  INPLACE_ADD      
              252  STORE_FAST               'html'

 L. 262       254  SETUP_LOOP          366  'to 366'
              256  LOAD_GLOBAL              enumerate
              258  LOAD_FAST                'plotdata'
              260  CALL_FUNCTION_1       1  '1 positional argument'
              262  GET_ITER         
              264  FOR_ITER            364  'to 364'
              266  UNPACK_SEQUENCE_2     2 
              268  STORE_FAST               'k'
              270  STORE_FAST               'p'

 L. 263       272  LOAD_FAST                'pids'
              274  LOAD_FAST                'k'
              276  BINARY_SUBSCR    
              278  STORE_FAST               'pid'

 L. 264       280  LOAD_FAST                'k'
              282  LOAD_CONST               0
              284  COMPARE_OP               ==
          286_288  POP_JUMP_IF_FALSE   294  'to 294'
              290  LOAD_STR                 'active'
              292  JUMP_FORWARD        296  'to 296'
            294_0  COME_FROM           286  '286'
              294  LOAD_STR                 ''
            296_0  COME_FROM           292  '292'
              296  STORE_FAST               'active'

 L. 265       298  SETUP_EXCEPT        320  'to 320'

 L. 266       300  LOAD_FAST                'pconfig'
              302  LOAD_STR                 'data_labels'
              304  BINARY_SUBSCR    
              306  LOAD_FAST                'k'
              308  BINARY_SUBSCR    
              310  LOAD_STR                 'name'
              312  BINARY_SUBSCR    
              314  STORE_FAST               'name'
              316  POP_BLOCK        
              318  JUMP_FORWARD        340  'to 340'
            320_0  COME_FROM_EXCEPT    298  '298'

 L. 267       320  POP_TOP          
              322  POP_TOP          
              324  POP_TOP          

 L. 268       326  LOAD_FAST                'k'
              328  LOAD_CONST               1
              330  BINARY_ADD       
              332  STORE_FAST               'name'
              334  POP_EXCEPT       
              336  JUMP_FORWARD        340  'to 340'
              338  END_FINALLY      
            340_0  COME_FROM           336  '336'
            340_1  COME_FROM           318  '318'

 L. 269       340  LOAD_FAST                'html'
              342  LOAD_STR                 '<button class="btn btn-default btn-sm {a}" data-target="#{pid}">{n}</button>\n'
              344  LOAD_ATTR                format
              346  LOAD_FAST                'active'
              348  LOAD_FAST                'pid'
              350  LOAD_FAST                'name'
              352  LOAD_CONST               ('a', 'pid', 'n')
              354  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              356  INPLACE_ADD      
              358  STORE_FAST               'html'
          360_362  JUMP_BACK           264  'to 264'
              364  POP_BLOCK        
            366_0  COME_FROM_LOOP      254  '254'

 L. 270       366  LOAD_FAST                'html'
              368  LOAD_STR                 '</div>\n\n'
              370  INPLACE_ADD      
              372  STORE_FAST               'html'
            374_0  COME_FROM           242  '242'
            374_1  COME_FROM           234  '234'

 L. 273   374_376  SETUP_LOOP         2356  'to 2356'
              378  LOAD_GLOBAL              enumerate
              380  LOAD_FAST                'plotdata'
              382  CALL_FUNCTION_1       1  '1 positional argument'
              384  GET_ITER         
          386_388  FOR_ITER           2354  'to 2354'
              390  UNPACK_SEQUENCE_2     2 
              392  STORE_FAST               'pidx'
              394  STORE_FAST               'pdata'

 L. 276       396  LOAD_FAST                'pids'
              398  LOAD_FAST                'pidx'
              400  BINARY_SUBSCR    
              402  STORE_FAST               'pid'

 L. 279       404  LOAD_GLOBAL              OrderedDict
              406  CALL_FUNCTION_0       0  '0 positional arguments'
              408  STORE_FAST               'fdata'

 L. 280       410  LOAD_CONST               None
              412  STORE_FAST               'lastcats'

 L. 281       414  LOAD_CONST               True
              416  STORE_FAST               'sharedcats'

 L. 282       418  SETUP_LOOP          654  'to 654'
              420  LOAD_FAST                'pdata'
              422  GET_ITER         
              424  FOR_ITER            652  'to 652'
              426  STORE_FAST               'd'

 L. 283       428  LOAD_GLOBAL              OrderedDict
              430  CALL_FUNCTION_0       0  '0 positional arguments'
              432  LOAD_FAST                'fdata'
              434  LOAD_FAST                'd'
              436  LOAD_STR                 'name'
              438  BINARY_SUBSCR    
              440  STORE_SUBSCR     

 L. 284       442  SETUP_LOOP          648  'to 648'
              444  LOAD_GLOBAL              enumerate
              446  LOAD_FAST                'd'
              448  LOAD_STR                 'data'
              450  BINARY_SUBSCR    
              452  CALL_FUNCTION_1       1  '1 positional argument'
              454  GET_ITER         
              456  FOR_ITER            646  'to 646'
              458  UNPACK_SEQUENCE_2     2 
              460  STORE_FAST               'i'
              462  STORE_FAST               'x'

 L. 285       464  LOAD_GLOBAL              type
              466  LOAD_FAST                'x'
              468  CALL_FUNCTION_1       1  '1 positional argument'
              470  LOAD_GLOBAL              list
              472  COMPARE_OP               is
          474_476  POP_JUMP_IF_FALSE   566  'to 566'

 L. 286       478  LOAD_FAST                'x'
              480  LOAD_CONST               1
              482  BINARY_SUBSCR    
              484  LOAD_FAST                'fdata'
              486  LOAD_FAST                'd'
              488  LOAD_STR                 'name'
              490  BINARY_SUBSCR    
              492  BINARY_SUBSCR    
              494  LOAD_GLOBAL              str
              496  LOAD_FAST                'x'
              498  LOAD_CONST               0
              500  BINARY_SUBSCR    
              502  CALL_FUNCTION_1       1  '1 positional argument'
              504  STORE_SUBSCR     

 L. 288       506  LOAD_FAST                'lastcats'
              508  LOAD_CONST               None
              510  COMPARE_OP               is
          512_514  POP_JUMP_IF_FALSE   536  'to 536'

 L. 289       516  LOAD_LISTCOMP            '<code_object <listcomp>>'
              518  LOAD_STR                 'matplotlib_linegraph.<locals>.<listcomp>'
              520  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              522  LOAD_FAST                'd'
              524  LOAD_STR                 'data'
              526  BINARY_SUBSCR    
              528  GET_ITER         
              530  CALL_FUNCTION_1       1  '1 positional argument'
              532  STORE_FAST               'lastcats'
              534  JUMP_FORWARD        564  'to 564'
            536_0  COME_FROM           512  '512'

 L. 290       536  LOAD_FAST                'lastcats'
              538  LOAD_LISTCOMP            '<code_object <listcomp>>'
              540  LOAD_STR                 'matplotlib_linegraph.<locals>.<listcomp>'
              542  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              544  LOAD_FAST                'd'
              546  LOAD_STR                 'data'
              548  BINARY_SUBSCR    
              550  GET_ITER         
              552  CALL_FUNCTION_1       1  '1 positional argument'
              554  COMPARE_OP               !=
          556_558  POP_JUMP_IF_FALSE   642  'to 642'

 L. 291       560  LOAD_CONST               False
              562  STORE_FAST               'sharedcats'
            564_0  COME_FROM           534  '534'
              564  JUMP_BACK           456  'to 456'
            566_0  COME_FROM           474  '474'

 L. 293       566  SETUP_EXCEPT        596  'to 596'

 L. 294       568  LOAD_FAST                'x'
              570  LOAD_FAST                'fdata'
              572  LOAD_FAST                'd'
              574  LOAD_STR                 'name'
              576  BINARY_SUBSCR    
              578  BINARY_SUBSCR    
              580  LOAD_FAST                'pconfig'
              582  LOAD_STR                 'categories'
              584  BINARY_SUBSCR    
              586  LOAD_FAST                'i'
              588  BINARY_SUBSCR    
              590  STORE_SUBSCR     
              592  POP_BLOCK        
              594  JUMP_BACK           456  'to 456'
            596_0  COME_FROM_EXCEPT    566  '566'

 L. 295       596  DUP_TOP          
              598  LOAD_GLOBAL              KeyError
              600  LOAD_GLOBAL              IndexError
              602  BUILD_TUPLE_2         2 
              604  COMPARE_OP               exception-match
          606_608  POP_JUMP_IF_FALSE   640  'to 640'
              610  POP_TOP          
              612  POP_TOP          
              614  POP_TOP          

 L. 296       616  LOAD_FAST                'x'
              618  LOAD_FAST                'fdata'
              620  LOAD_FAST                'd'
              622  LOAD_STR                 'name'
              624  BINARY_SUBSCR    
              626  BINARY_SUBSCR    
              628  LOAD_GLOBAL              str
              630  LOAD_FAST                'i'
              632  CALL_FUNCTION_1       1  '1 positional argument'
              634  STORE_SUBSCR     
              636  POP_EXCEPT       
              638  JUMP_BACK           456  'to 456'
            640_0  COME_FROM           606  '606'
              640  END_FINALLY      
            642_0  COME_FROM           556  '556'
          642_644  JUMP_BACK           456  'to 456'
              646  POP_BLOCK        
            648_0  COME_FROM_LOOP      442  '442'
          648_650  JUMP_BACK           424  'to 424'
              652  POP_BLOCK        
            654_0  COME_FROM_LOOP      418  '418'

 L. 299       654  LOAD_FAST                'sharedcats'
          656_658  POP_JUMP_IF_TRUE    852  'to 852'
              660  LOAD_GLOBAL              config
              662  LOAD_ATTR                data_format
              664  LOAD_STR                 'tsv'
              666  COMPARE_OP               ==
          668_670  POP_JUMP_IF_FALSE   852  'to 852'

 L. 300       672  LOAD_STR                 ''
              674  STORE_FAST               'fout'

 L. 301       676  SETUP_LOOP          778  'to 778'
              678  LOAD_FAST                'pdata'
              680  GET_ITER         
              682  FOR_ITER            776  'to 776'
              684  STORE_FAST               'd'

 L. 302       686  LOAD_FAST                'fout'
              688  LOAD_STR                 '\t'
              690  LOAD_STR                 '\t'
              692  LOAD_METHOD              join
              694  LOAD_LISTCOMP            '<code_object <listcomp>>'
              696  LOAD_STR                 'matplotlib_linegraph.<locals>.<listcomp>'
              698  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              700  LOAD_FAST                'd'
              702  LOAD_STR                 'data'
              704  BINARY_SUBSCR    
              706  GET_ITER         
              708  CALL_FUNCTION_1       1  '1 positional argument'
              710  CALL_METHOD_1         1  '1 positional argument'
              712  BINARY_ADD       
              714  INPLACE_ADD      
              716  STORE_FAST               'fout'

 L. 303       718  LOAD_FAST                'fout'
              720  LOAD_STR                 '\n{}\t'
              722  LOAD_METHOD              format
              724  LOAD_FAST                'd'
              726  LOAD_STR                 'name'
              728  BINARY_SUBSCR    
              730  CALL_METHOD_1         1  '1 positional argument'
              732  INPLACE_ADD      
              734  STORE_FAST               'fout'

 L. 304       736  LOAD_FAST                'fout'
              738  LOAD_STR                 '\t'
              740  LOAD_METHOD              join
              742  LOAD_LISTCOMP            '<code_object <listcomp>>'
              744  LOAD_STR                 'matplotlib_linegraph.<locals>.<listcomp>'
              746  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              748  LOAD_FAST                'd'
              750  LOAD_STR                 'data'
              752  BINARY_SUBSCR    
              754  GET_ITER         
              756  CALL_FUNCTION_1       1  '1 positional argument'
              758  CALL_METHOD_1         1  '1 positional argument'
              760  INPLACE_ADD      
              762  STORE_FAST               'fout'

 L. 305       764  LOAD_FAST                'fout'
              766  LOAD_STR                 '\n'
              768  INPLACE_ADD      
              770  STORE_FAST               'fout'
          772_774  JUMP_BACK           682  'to 682'
              776  POP_BLOCK        
            778_0  COME_FROM_LOOP      676  '676'

 L. 306       778  LOAD_GLOBAL              io
              780  LOAD_ATTR                open
              782  LOAD_GLOBAL              os
              784  LOAD_ATTR                path
              786  LOAD_METHOD              join
              788  LOAD_GLOBAL              config
              790  LOAD_ATTR                data_dir
              792  LOAD_STR                 '{}.txt'
              794  LOAD_METHOD              format
              796  LOAD_FAST                'pid'
              798  CALL_METHOD_1         1  '1 positional argument'
              800  CALL_METHOD_2         2  '2 positional arguments'
              802  LOAD_STR                 'w'
              804  LOAD_STR                 'utf-8'
              806  LOAD_CONST               ('encoding',)
              808  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              810  SETUP_WITH          844  'to 844'
              812  STORE_FAST               'f'

 L. 307       814  LOAD_GLOBAL              print
              816  LOAD_FAST                'fout'
              818  LOAD_METHOD              encode
              820  LOAD_STR                 'utf-8'
              822  LOAD_STR                 'ignore'
              824  CALL_METHOD_2         2  '2 positional arguments'
              826  LOAD_METHOD              decode
              828  LOAD_STR                 'utf-8'
              830  CALL_METHOD_1         1  '1 positional argument'
              832  LOAD_FAST                'f'
              834  LOAD_CONST               ('file',)
              836  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              838  POP_TOP          
              840  POP_BLOCK        
              842  LOAD_CONST               None
            844_0  COME_FROM_WITH      810  '810'
              844  WITH_CLEANUP_START
              846  WITH_CLEANUP_FINISH
              848  END_FINALLY      
              850  JUMP_FORWARD        864  'to 864'
            852_0  COME_FROM           668  '668'
            852_1  COME_FROM           656  '656'

 L. 309       852  LOAD_GLOBAL              util_functions
              854  LOAD_METHOD              write_data_file
              856  LOAD_FAST                'fdata'
              858  LOAD_FAST                'pid'
              860  CALL_METHOD_2         2  '2 positional arguments'
              862  POP_TOP          
            864_0  COME_FROM           850  '850'

 L. 312       864  LOAD_GLOBAL              plt
              866  LOAD_ATTR                figure
              868  LOAD_CONST               (14, 6)
              870  LOAD_CONST               False
              872  LOAD_CONST               ('figsize', 'frameon')
              874  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              876  STORE_FAST               'fig'

 L. 313       878  LOAD_FAST                'fig'
              880  LOAD_METHOD              add_subplot
              882  LOAD_CONST               111
              884  CALL_METHOD_1         1  '1 positional argument'
              886  STORE_FAST               'axes'

 L. 316       888  SETUP_LOOP         1112  'to 1112'
              890  LOAD_GLOBAL              enumerate
              892  LOAD_FAST                'pdata'
              894  CALL_FUNCTION_1       1  '1 positional argument'
              896  GET_ITER         
              898  FOR_ITER           1110  'to 1110'
              900  UNPACK_SEQUENCE_2     2 
              902  STORE_FAST               'idx'
              904  STORE_FAST               'd'

 L. 319       906  LOAD_FAST                'idx'
              908  STORE_FAST               'cidx'

 L. 320       910  SETUP_LOOP          944  'to 944'
              912  LOAD_FAST                'cidx'
              914  LOAD_GLOBAL              len
              916  LOAD_FAST                'default_colors'
              918  CALL_FUNCTION_1       1  '1 positional argument'
              920  COMPARE_OP               >=
          922_924  POP_JUMP_IF_FALSE   942  'to 942'

 L. 321       926  LOAD_FAST                'cidx'
              928  LOAD_GLOBAL              len
              930  LOAD_FAST                'default_colors'
              932  CALL_FUNCTION_1       1  '1 positional argument'
              934  INPLACE_SUBTRACT 
              936  STORE_FAST               'cidx'
          938_940  JUMP_BACK           912  'to 912'
            942_0  COME_FROM           922  '922'
              942  POP_BLOCK        
            944_0  COME_FROM_LOOP      910  '910'

 L. 324       944  LOAD_STR                 'solid'
              946  STORE_FAST               'linestyle'

 L. 325       948  LOAD_FAST                'd'
              950  LOAD_METHOD              get
              952  LOAD_STR                 'dashStyle'
              954  LOAD_CONST               None
              956  CALL_METHOD_2         2  '2 positional arguments'
              958  LOAD_STR                 'Dash'
              960  COMPARE_OP               ==
          962_964  POP_JUMP_IF_FALSE   970  'to 970'

 L. 326       966  LOAD_STR                 'dashed'
              968  STORE_FAST               'linestyle'
            970_0  COME_FROM           962  '962'

 L. 329       970  SETUP_EXCEPT       1044  'to 1044'

 L. 330       972  LOAD_FAST                'axes'
              974  LOAD_ATTR                plot
              976  LOAD_LISTCOMP            '<code_object <listcomp>>'
              978  LOAD_STR                 'matplotlib_linegraph.<locals>.<listcomp>'
              980  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              982  LOAD_FAST                'd'
              984  LOAD_STR                 'data'
              986  BINARY_SUBSCR    
              988  GET_ITER         
              990  CALL_FUNCTION_1       1  '1 positional argument'
              992  LOAD_LISTCOMP            '<code_object <listcomp>>'
              994  LOAD_STR                 'matplotlib_linegraph.<locals>.<listcomp>'
              996  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              998  LOAD_FAST                'd'
             1000  LOAD_STR                 'data'
             1002  BINARY_SUBSCR    
             1004  GET_ITER         
             1006  CALL_FUNCTION_1       1  '1 positional argument'
             1008  LOAD_FAST                'd'
             1010  LOAD_STR                 'name'
             1012  BINARY_SUBSCR    
             1014  LOAD_FAST                'd'
             1016  LOAD_METHOD              get
             1018  LOAD_STR                 'color'
             1020  LOAD_FAST                'default_colors'
             1022  LOAD_FAST                'cidx'
             1024  BINARY_SUBSCR    
             1026  CALL_METHOD_2         2  '2 positional arguments'
             1028  LOAD_FAST                'linestyle'
             1030  LOAD_CONST               1
             1032  LOAD_CONST               None
             1034  LOAD_CONST               ('label', 'color', 'linestyle', 'linewidth', 'marker')
             1036  CALL_FUNCTION_KW_7     7  '7 total positional and keyword args'
             1038  POP_TOP          
             1040  POP_BLOCK        
             1042  JUMP_BACK           898  'to 898'
           1044_0  COME_FROM_EXCEPT    970  '970'

 L. 331      1044  DUP_TOP          
             1046  LOAD_GLOBAL              TypeError
             1048  COMPARE_OP               exception-match
         1050_1052  POP_JUMP_IF_FALSE  1104  'to 1104'
             1054  POP_TOP          
             1056  POP_TOP          
             1058  POP_TOP          

 L. 333      1060  LOAD_FAST                'axes'
             1062  LOAD_ATTR                plot
             1064  LOAD_FAST                'd'
             1066  LOAD_STR                 'data'
             1068  BINARY_SUBSCR    
             1070  LOAD_FAST                'd'
             1072  LOAD_STR                 'name'
             1074  BINARY_SUBSCR    
             1076  LOAD_FAST                'd'
             1078  LOAD_METHOD              get
             1080  LOAD_STR                 'color'
             1082  LOAD_FAST                'default_colors'
             1084  LOAD_FAST                'cidx'
             1086  BINARY_SUBSCR    
             1088  CALL_METHOD_2         2  '2 positional arguments'
             1090  LOAD_CONST               1
             1092  LOAD_CONST               None
             1094  LOAD_CONST               ('label', 'color', 'linewidth', 'marker')
             1096  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
             1098  POP_TOP          
             1100  POP_EXCEPT       
             1102  JUMP_BACK           898  'to 898'
           1104_0  COME_FROM          1050  '1050'
             1104  END_FINALLY      
         1106_1108  JUMP_BACK           898  'to 898'
             1110  POP_BLOCK        
           1112_0  COME_FROM_LOOP      888  '888'

 L. 336      1112  LOAD_FAST                'axes'
             1114  LOAD_ATTR                tick_params
             1116  LOAD_CONST               8
             1118  LOAD_STR                 'out'
             1120  LOAD_CONST               False
             1122  LOAD_CONST               False
             1124  LOAD_CONST               False
             1126  LOAD_CONST               False
             1128  LOAD_CONST               ('labelsize', 'direction', 'left', 'right', 'top', 'bottom')
             1130  CALL_FUNCTION_KW_6     6  '6 total positional and keyword args'
             1132  POP_TOP          

 L. 337      1134  LOAD_FAST                'axes'
             1136  LOAD_METHOD              set_xlabel
             1138  LOAD_FAST                'pconfig'
             1140  LOAD_METHOD              get
             1142  LOAD_STR                 'xlab'
             1144  LOAD_STR                 ''
             1146  CALL_METHOD_2         2  '2 positional arguments'
             1148  CALL_METHOD_1         1  '1 positional argument'
             1150  POP_TOP          

 L. 338      1152  LOAD_FAST                'axes'
             1154  LOAD_METHOD              set_ylabel
             1156  LOAD_FAST                'pconfig'
             1158  LOAD_METHOD              get
             1160  LOAD_STR                 'ylab'
             1162  LOAD_STR                 ''
             1164  CALL_METHOD_2         2  '2 positional arguments'
             1166  CALL_METHOD_1         1  '1 positional argument'
             1168  POP_TOP          

 L. 341      1170  SETUP_EXCEPT       1198  'to 1198'

 L. 342      1172  LOAD_FAST                'axes'
             1174  LOAD_METHOD              set_ylabel
             1176  LOAD_FAST                'pconfig'
             1178  LOAD_STR                 'data_labels'
             1180  BINARY_SUBSCR    
             1182  LOAD_FAST                'pidx'
             1184  BINARY_SUBSCR    
             1186  LOAD_STR                 'ylab'
             1188  BINARY_SUBSCR    
             1190  CALL_METHOD_1         1  '1 positional argument'
             1192  POP_TOP          
             1194  POP_BLOCK        
             1196  JUMP_FORWARD       1210  'to 1210'
           1198_0  COME_FROM_EXCEPT   1170  '1170'

 L. 343      1198  POP_TOP          
             1200  POP_TOP          
             1202  POP_TOP          

 L. 344      1204  POP_EXCEPT       
             1206  JUMP_FORWARD       1210  'to 1210'
             1208  END_FINALLY      
           1210_0  COME_FROM          1206  '1206'
           1210_1  COME_FROM          1196  '1196'

 L. 347      1210  LOAD_FAST                'axes'
             1212  LOAD_METHOD              get_ylim
             1214  CALL_METHOD_0         0  '0 positional arguments'
             1216  STORE_FAST               'default_ylimits'

 L. 348      1218  LOAD_FAST                'default_ylimits'
             1220  LOAD_CONST               0
             1222  BINARY_SUBSCR    
             1224  STORE_FAST               'ymin'

 L. 349      1226  LOAD_STR                 'ymin'
             1228  LOAD_FAST                'pconfig'
             1230  COMPARE_OP               in
         1232_1234  POP_JUMP_IF_FALSE  1246  'to 1246'

 L. 350      1236  LOAD_FAST                'pconfig'
             1238  LOAD_STR                 'ymin'
             1240  BINARY_SUBSCR    
             1242  STORE_FAST               'ymin'
             1244  JUMP_FORWARD       1274  'to 1274'
           1246_0  COME_FROM          1232  '1232'

 L. 351      1246  LOAD_STR                 'yFloor'
             1248  LOAD_FAST                'pconfig'
             1250  COMPARE_OP               in
         1252_1254  POP_JUMP_IF_FALSE  1274  'to 1274'

 L. 352      1256  LOAD_GLOBAL              max
             1258  LOAD_FAST                'pconfig'
             1260  LOAD_STR                 'yFloor'
             1262  BINARY_SUBSCR    
             1264  LOAD_FAST                'default_ylimits'
             1266  LOAD_CONST               0
             1268  BINARY_SUBSCR    
             1270  CALL_FUNCTION_2       2  '2 positional arguments'
             1272  STORE_FAST               'ymin'
           1274_0  COME_FROM          1252  '1252'
           1274_1  COME_FROM          1244  '1244'

 L. 353      1274  LOAD_FAST                'default_ylimits'
             1276  LOAD_CONST               1
             1278  BINARY_SUBSCR    
             1280  STORE_FAST               'ymax'

 L. 354      1282  LOAD_STR                 'ymax'
             1284  LOAD_FAST                'pconfig'
             1286  COMPARE_OP               in
         1288_1290  POP_JUMP_IF_FALSE  1302  'to 1302'

 L. 355      1292  LOAD_FAST                'pconfig'
             1294  LOAD_STR                 'ymax'
             1296  BINARY_SUBSCR    
             1298  STORE_FAST               'ymax'
             1300  JUMP_FORWARD       1330  'to 1330'
           1302_0  COME_FROM          1288  '1288'

 L. 356      1302  LOAD_STR                 'yCeiling'
             1304  LOAD_FAST                'pconfig'
             1306  COMPARE_OP               in
         1308_1310  POP_JUMP_IF_FALSE  1330  'to 1330'

 L. 357      1312  LOAD_GLOBAL              min
             1314  LOAD_FAST                'pconfig'
             1316  LOAD_STR                 'yCeiling'
             1318  BINARY_SUBSCR    
             1320  LOAD_FAST                'default_ylimits'
             1322  LOAD_CONST               1
             1324  BINARY_SUBSCR    
             1326  CALL_FUNCTION_2       2  '2 positional arguments'
             1328  STORE_FAST               'ymax'
           1330_0  COME_FROM          1308  '1308'
           1330_1  COME_FROM          1300  '1300'

 L. 358      1330  LOAD_FAST                'ymax'
             1332  LOAD_FAST                'ymin'
             1334  BINARY_SUBTRACT  
             1336  LOAD_FAST                'pconfig'
             1338  LOAD_METHOD              get
             1340  LOAD_STR                 'yMinRange'
             1342  LOAD_CONST               0
             1344  CALL_METHOD_2         2  '2 positional arguments'
             1346  COMPARE_OP               <
         1348_1350  POP_JUMP_IF_FALSE  1364  'to 1364'

 L. 359      1352  LOAD_FAST                'ymin'
             1354  LOAD_FAST                'pconfig'
             1356  LOAD_STR                 'yMinRange'
             1358  BINARY_SUBSCR    
             1360  BINARY_ADD       
             1362  STORE_FAST               'ymax'
           1364_0  COME_FROM          1348  '1348'

 L. 360      1364  LOAD_FAST                'axes'
             1366  LOAD_METHOD              set_ylim
             1368  LOAD_FAST                'ymin'
             1370  LOAD_FAST                'ymax'
             1372  BUILD_TUPLE_2         2 
             1374  CALL_METHOD_1         1  '1 positional argument'
             1376  POP_TOP          

 L. 363      1378  SETUP_EXCEPT       1410  'to 1410'

 L. 364      1380  LOAD_FAST                'axes'
             1382  LOAD_METHOD              set_ylim
             1384  LOAD_FAST                'ymin'
             1386  LOAD_FAST                'pconfig'
             1388  LOAD_STR                 'data_labels'
             1390  BINARY_SUBSCR    
             1392  LOAD_FAST                'pidx'
             1394  BINARY_SUBSCR    
             1396  LOAD_STR                 'ymax'
             1398  BINARY_SUBSCR    
             1400  BUILD_TUPLE_2         2 
             1402  CALL_METHOD_1         1  '1 positional argument'
             1404  POP_TOP          
             1406  POP_BLOCK        
             1408  JUMP_FORWARD       1422  'to 1422'
           1410_0  COME_FROM_EXCEPT   1378  '1378'

 L. 365      1410  POP_TOP          
             1412  POP_TOP          
             1414  POP_TOP          

 L. 366      1416  POP_EXCEPT       
             1418  JUMP_FORWARD       1422  'to 1422'
             1420  END_FINALLY      
           1422_0  COME_FROM          1418  '1418'
           1422_1  COME_FROM          1408  '1408'

 L. 368      1422  LOAD_FAST                'axes'
             1424  LOAD_METHOD              get_xlim
             1426  CALL_METHOD_0         0  '0 positional arguments'
             1428  STORE_FAST               'default_xlimits'

 L. 369      1430  LOAD_FAST                'default_xlimits'
             1432  LOAD_CONST               0
             1434  BINARY_SUBSCR    
             1436  STORE_FAST               'xmin'

 L. 370      1438  LOAD_STR                 'xmin'
             1440  LOAD_FAST                'pconfig'
             1442  COMPARE_OP               in
         1444_1446  POP_JUMP_IF_FALSE  1458  'to 1458'

 L. 371      1448  LOAD_FAST                'pconfig'
             1450  LOAD_STR                 'xmin'
             1452  BINARY_SUBSCR    
             1454  STORE_FAST               'xmin'
             1456  JUMP_FORWARD       1486  'to 1486'
           1458_0  COME_FROM          1444  '1444'

 L. 372      1458  LOAD_STR                 'xFloor'
             1460  LOAD_FAST                'pconfig'
             1462  COMPARE_OP               in
         1464_1466  POP_JUMP_IF_FALSE  1486  'to 1486'

 L. 373      1468  LOAD_GLOBAL              max
             1470  LOAD_FAST                'pconfig'
             1472  LOAD_STR                 'xFloor'
             1474  BINARY_SUBSCR    
             1476  LOAD_FAST                'default_xlimits'
             1478  LOAD_CONST               0
             1480  BINARY_SUBSCR    
             1482  CALL_FUNCTION_2       2  '2 positional arguments'
             1484  STORE_FAST               'xmin'
           1486_0  COME_FROM          1464  '1464'
           1486_1  COME_FROM          1456  '1456'

 L. 374      1486  LOAD_FAST                'default_xlimits'
             1488  LOAD_CONST               1
             1490  BINARY_SUBSCR    
             1492  STORE_FAST               'xmax'

 L. 375      1494  LOAD_STR                 'xmax'
             1496  LOAD_FAST                'pconfig'
             1498  COMPARE_OP               in
         1500_1502  POP_JUMP_IF_FALSE  1514  'to 1514'

 L. 376      1504  LOAD_FAST                'pconfig'
             1506  LOAD_STR                 'xmax'
             1508  BINARY_SUBSCR    
             1510  STORE_FAST               'xmax'
             1512  JUMP_FORWARD       1542  'to 1542'
           1514_0  COME_FROM          1500  '1500'

 L. 377      1514  LOAD_STR                 'xCeiling'
             1516  LOAD_FAST                'pconfig'
             1518  COMPARE_OP               in
         1520_1522  POP_JUMP_IF_FALSE  1542  'to 1542'

 L. 378      1524  LOAD_GLOBAL              min
             1526  LOAD_FAST                'pconfig'
             1528  LOAD_STR                 'xCeiling'
             1530  BINARY_SUBSCR    
             1532  LOAD_FAST                'default_xlimits'
             1534  LOAD_CONST               1
             1536  BINARY_SUBSCR    
             1538  CALL_FUNCTION_2       2  '2 positional arguments'
             1540  STORE_FAST               'xmax'
           1542_0  COME_FROM          1520  '1520'
           1542_1  COME_FROM          1512  '1512'

 L. 379      1542  LOAD_FAST                'xmax'
             1544  LOAD_FAST                'xmin'
             1546  BINARY_SUBTRACT  
             1548  LOAD_FAST                'pconfig'
             1550  LOAD_METHOD              get
             1552  LOAD_STR                 'xMinRange'
             1554  LOAD_CONST               0
             1556  CALL_METHOD_2         2  '2 positional arguments'
             1558  COMPARE_OP               <
         1560_1562  POP_JUMP_IF_FALSE  1576  'to 1576'

 L. 380      1564  LOAD_FAST                'xmin'
             1566  LOAD_FAST                'pconfig'
             1568  LOAD_STR                 'xMinRange'
             1570  BINARY_SUBSCR    
             1572  BINARY_ADD       
             1574  STORE_FAST               'xmax'
           1576_0  COME_FROM          1560  '1560'

 L. 381      1576  LOAD_FAST                'axes'
             1578  LOAD_METHOD              set_xlim
             1580  LOAD_FAST                'xmin'
             1582  LOAD_FAST                'xmax'
             1584  BUILD_TUPLE_2         2 
             1586  CALL_METHOD_1         1  '1 positional argument'
             1588  POP_TOP          

 L. 384      1590  LOAD_STR                 'title'
             1592  LOAD_FAST                'pconfig'
             1594  COMPARE_OP               in
         1596_1598  POP_JUMP_IF_FALSE  1628  'to 1628'

 L. 385      1600  LOAD_GLOBAL              plt
             1602  LOAD_ATTR                text
             1604  LOAD_CONST               0.5
             1606  LOAD_CONST               1.05
             1608  LOAD_FAST                'pconfig'
             1610  LOAD_STR                 'title'
             1612  BINARY_SUBSCR    
             1614  LOAD_STR                 'center'
             1616  LOAD_CONST               16
             1618  LOAD_FAST                'axes'
             1620  LOAD_ATTR                transAxes
             1622  LOAD_CONST               ('horizontalalignment', 'fontsize', 'transform')
             1624  CALL_FUNCTION_KW_6     6  '6 total positional and keyword args'
             1626  POP_TOP          
           1628_0  COME_FROM          1596  '1596'

 L. 386      1628  LOAD_FAST                'axes'
             1630  LOAD_ATTR                grid
             1632  LOAD_CONST               True
             1634  LOAD_CONST               10
             1636  LOAD_STR                 'both'
             1638  LOAD_STR                 'y'
             1640  LOAD_STR                 '-'
             1642  LOAD_STR                 '#dedede'
             1644  LOAD_CONST               1
             1646  LOAD_CONST               ('zorder', 'which', 'axis', 'linestyle', 'color', 'linewidth')
             1648  CALL_FUNCTION_KW_7     7  '7 total positional and keyword args'
             1650  POP_TOP          

 L. 389      1652  LOAD_STR                 'categories'
             1654  LOAD_FAST                'pconfig'
             1656  COMPARE_OP               in
         1658_1660  POP_JUMP_IF_FALSE  1704  'to 1704'

 L. 390      1662  LOAD_FAST                'axes'
             1664  LOAD_METHOD              set_xticks
             1666  LOAD_LISTCOMP            '<code_object <listcomp>>'
             1668  LOAD_STR                 'matplotlib_linegraph.<locals>.<listcomp>'
             1670  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
             1672  LOAD_GLOBAL              enumerate
             1674  LOAD_FAST                'pconfig'
             1676  LOAD_STR                 'categories'
             1678  BINARY_SUBSCR    
             1680  CALL_FUNCTION_1       1  '1 positional argument'
             1682  GET_ITER         
             1684  CALL_FUNCTION_1       1  '1 positional argument'
             1686  CALL_METHOD_1         1  '1 positional argument'
             1688  POP_TOP          

 L. 391      1690  LOAD_FAST                'axes'
             1692  LOAD_METHOD              set_xticklabels
             1694  LOAD_FAST                'pconfig'
             1696  LOAD_STR                 'categories'
             1698  BINARY_SUBSCR    
             1700  CALL_METHOD_1         1  '1 positional argument'
             1702  POP_TOP          
           1704_0  COME_FROM          1658  '1658'

 L. 394      1704  LOAD_FAST                'axes'
             1706  LOAD_METHOD              get_xlim
             1708  CALL_METHOD_0         0  '0 positional arguments'
             1710  STORE_FAST               'xlim'

 L. 395      1712  LOAD_FAST                'axes'
             1714  LOAD_ATTR                plot
             1716  LOAD_FAST                'xlim'
             1718  LOAD_CONST               0
             1720  BINARY_SUBSCR    
             1722  LOAD_FAST                'xlim'
             1724  LOAD_CONST               1
             1726  BINARY_SUBSCR    
             1728  BUILD_LIST_2          2 
             1730  LOAD_CONST               0
             1732  LOAD_CONST               0
             1734  BUILD_LIST_2          2 
             1736  LOAD_STR                 '-'
             1738  LOAD_STR                 '#dedede'
             1740  LOAD_CONST               2
             1742  LOAD_CONST               ('linestyle', 'color', 'linewidth')
             1744  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
             1746  POP_TOP          

 L. 396      1748  LOAD_FAST                'axes'
             1750  LOAD_METHOD              set_axisbelow
             1752  LOAD_CONST               True
             1754  CALL_METHOD_1         1  '1 positional argument'
             1756  POP_TOP          

 L. 397      1758  LOAD_FAST                'axes'
             1760  LOAD_ATTR                spines
             1762  LOAD_STR                 'right'
             1764  BINARY_SUBSCR    
             1766  LOAD_METHOD              set_visible
             1768  LOAD_CONST               False
             1770  CALL_METHOD_1         1  '1 positional argument'
             1772  POP_TOP          

 L. 398      1774  LOAD_FAST                'axes'
             1776  LOAD_ATTR                spines
             1778  LOAD_STR                 'top'
             1780  BINARY_SUBSCR    
             1782  LOAD_METHOD              set_visible
             1784  LOAD_CONST               False
             1786  CALL_METHOD_1         1  '1 positional argument'
             1788  POP_TOP          

 L. 399      1790  LOAD_FAST                'axes'
             1792  LOAD_ATTR                spines
             1794  LOAD_STR                 'bottom'
             1796  BINARY_SUBSCR    
             1798  LOAD_METHOD              set_visible
             1800  LOAD_CONST               False
             1802  CALL_METHOD_1         1  '1 positional argument'
             1804  POP_TOP          

 L. 400      1806  LOAD_FAST                'axes'
             1808  LOAD_ATTR                spines
             1810  LOAD_STR                 'left'
             1812  BINARY_SUBSCR    
             1814  LOAD_METHOD              set_visible
             1816  LOAD_CONST               False
             1818  CALL_METHOD_1         1  '1 positional argument'
             1820  POP_TOP          

 L. 403      1822  LOAD_STR                 'yPlotBands'
             1824  LOAD_FAST                'pconfig'
             1826  COMPARE_OP               in
         1828_1830  POP_JUMP_IF_FALSE  1914  'to 1914'

 L. 404      1832  LOAD_FAST                'axes'
             1834  LOAD_METHOD              get_xlim
             1836  CALL_METHOD_0         0  '0 positional arguments'
             1838  STORE_FAST               'xlim'

 L. 405      1840  SETUP_LOOP         1914  'to 1914'
             1842  LOAD_FAST                'pconfig'
             1844  LOAD_STR                 'yPlotBands'
             1846  BINARY_SUBSCR    
             1848  GET_ITER         
             1850  FOR_ITER           1912  'to 1912'
             1852  STORE_FAST               'pb'

 L. 406      1854  LOAD_FAST                'axes'
             1856  LOAD_ATTR                barh
             1858  LOAD_FAST                'pb'
             1860  LOAD_STR                 'from'
             1862  BINARY_SUBSCR    
             1864  LOAD_FAST                'xlim'
             1866  LOAD_CONST               1
             1868  BINARY_SUBSCR    
             1870  LOAD_FAST                'pb'
             1872  LOAD_STR                 'to'
             1874  BINARY_SUBSCR    
             1876  LOAD_FAST                'pb'
             1878  LOAD_STR                 'from'
             1880  BINARY_SUBSCR    
             1882  BINARY_SUBTRACT  
             1884  LOAD_FAST                'xlim'
             1886  LOAD_CONST               0
             1888  BINARY_SUBSCR    
             1890  LOAD_FAST                'pb'
             1892  LOAD_STR                 'color'
             1894  BINARY_SUBSCR    
             1896  LOAD_CONST               0
             1898  LOAD_CONST               0
             1900  LOAD_STR                 'edge'
             1902  LOAD_CONST               ('height', 'left', 'color', 'linewidth', 'zorder', 'align')
             1904  CALL_FUNCTION_KW_8     8  '8 total positional and keyword args'
             1906  POP_TOP          
         1908_1910  JUMP_BACK          1850  'to 1850'
             1912  POP_BLOCK        
           1914_0  COME_FROM_LOOP     1840  '1840'
           1914_1  COME_FROM          1828  '1828'

 L. 407      1914  LOAD_STR                 'xPlotBands'
             1916  LOAD_FAST                'pconfig'
             1918  COMPARE_OP               in
         1920_1922  POP_JUMP_IF_FALSE  2006  'to 2006'

 L. 408      1924  LOAD_FAST                'axes'
             1926  LOAD_METHOD              get_ylim
             1928  CALL_METHOD_0         0  '0 positional arguments'
             1930  STORE_FAST               'ylim'

 L. 409      1932  SETUP_LOOP         2006  'to 2006'
             1934  LOAD_FAST                'pconfig'
             1936  LOAD_STR                 'xPlotBands'
             1938  BINARY_SUBSCR    
             1940  GET_ITER         
             1942  FOR_ITER           2004  'to 2004'
             1944  STORE_FAST               'pb'

 L. 410      1946  LOAD_FAST                'axes'
             1948  LOAD_ATTR                bar
             1950  LOAD_FAST                'pb'
             1952  LOAD_STR                 'from'
             1954  BINARY_SUBSCR    
             1956  LOAD_FAST                'ylim'
             1958  LOAD_CONST               1
             1960  BINARY_SUBSCR    
             1962  LOAD_FAST                'pb'
             1964  LOAD_STR                 'to'
             1966  BINARY_SUBSCR    
             1968  LOAD_FAST                'pb'
             1970  LOAD_STR                 'from'
             1972  BINARY_SUBSCR    
             1974  BINARY_SUBTRACT  
             1976  LOAD_FAST                'ylim'
             1978  LOAD_CONST               0
             1980  BINARY_SUBSCR    
             1982  LOAD_FAST                'pb'
             1984  LOAD_STR                 'color'
             1986  BINARY_SUBSCR    
             1988  LOAD_CONST               0
             1990  LOAD_CONST               0
             1992  LOAD_STR                 'edge'
             1994  LOAD_CONST               ('width', 'bottom', 'color', 'linewidth', 'zorder', 'align')
             1996  CALL_FUNCTION_KW_8     8  '8 total positional and keyword args'
             1998  POP_TOP          
         2000_2002  JUMP_BACK          1942  'to 1942'
             2004  POP_BLOCK        
           2006_0  COME_FROM_LOOP     1932  '1932'
           2006_1  COME_FROM          1920  '1920'

 L. 413      2006  LOAD_GLOBAL              len
             2008  LOAD_FAST                'pdata'
             2010  CALL_FUNCTION_1       1  '1 positional argument'
             2012  LOAD_CONST               15
             2014  COMPARE_OP               <=
         2016_2018  POP_JUMP_IF_FALSE  2064  'to 2064'

 L. 414      2020  LOAD_FAST                'axes'
             2022  LOAD_ATTR                legend
             2024  LOAD_STR                 'lower center'
             2026  LOAD_CONST               (0, -0.22, 1, 0.102)
             2028  LOAD_CONST               5
             2030  LOAD_STR                 'expand'
             2032  LOAD_CONST               8
             2034  LOAD_CONST               False
             2036  LOAD_CONST               ('loc', 'bbox_to_anchor', 'ncol', 'mode', 'fontsize', 'frameon')
             2038  CALL_FUNCTION_KW_6     6  '6 total positional and keyword args'
             2040  POP_TOP          

 L. 415      2042  LOAD_GLOBAL              plt
             2044  LOAD_ATTR                tight_layout
             2046  LOAD_CONST               0
             2048  LOAD_CONST               0.08
             2050  LOAD_CONST               1
             2052  LOAD_CONST               0.92
             2054  BUILD_LIST_4          4 
             2056  LOAD_CONST               ('rect',)
             2058  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
             2060  POP_TOP          
             2062  JUMP_FORWARD       2084  'to 2084'
           2064_0  COME_FROM          2016  '2016'

 L. 417      2064  LOAD_GLOBAL              plt
             2066  LOAD_ATTR                tight_layout
             2068  LOAD_CONST               0
             2070  LOAD_CONST               0
             2072  LOAD_CONST               1
             2074  LOAD_CONST               0.92
             2076  BUILD_LIST_4          4 
             2078  LOAD_CONST               ('rect',)
             2080  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
             2082  POP_TOP          
           2084_0  COME_FROM          2062  '2062'

 L. 420      2084  LOAD_STR                 ''
             2086  STORE_FAST               'hidediv'

 L. 421      2088  LOAD_FAST                'pidx'
             2090  LOAD_CONST               0
             2092  COMPARE_OP               >
         2094_2096  POP_JUMP_IF_FALSE  2102  'to 2102'

 L. 422      2098  LOAD_STR                 ' style="display:none;"'
             2100  STORE_FAST               'hidediv'
           2102_0  COME_FROM          2094  '2094'

 L. 425      2102  LOAD_GLOBAL              config
             2104  LOAD_ATTR                export_plots
         2106_2108  POP_JUMP_IF_FALSE  2206  'to 2206'

 L. 426      2110  SETUP_LOOP         2206  'to 2206'
             2112  LOAD_GLOBAL              config
             2114  LOAD_ATTR                export_plot_formats
             2116  GET_ITER         
             2118  FOR_ITER           2204  'to 2204'
             2120  STORE_FAST               'fformat'

 L. 428      2122  LOAD_GLOBAL              os
             2124  LOAD_ATTR                path
             2126  LOAD_METHOD              join
             2128  LOAD_GLOBAL              config
             2130  LOAD_ATTR                plots_dir
             2132  LOAD_FAST                'fformat'
             2134  CALL_METHOD_2         2  '2 positional arguments'
             2136  STORE_FAST               'plot_dir'

 L. 429      2138  LOAD_GLOBAL              os
             2140  LOAD_ATTR                path
             2142  LOAD_METHOD              exists
             2144  LOAD_FAST                'plot_dir'
             2146  CALL_METHOD_1         1  '1 positional argument'
         2148_2150  POP_JUMP_IF_TRUE   2162  'to 2162'

 L. 430      2152  LOAD_GLOBAL              os
             2154  LOAD_METHOD              makedirs
             2156  LOAD_FAST                'plot_dir'
             2158  CALL_METHOD_1         1  '1 positional argument'
             2160  POP_TOP          
           2162_0  COME_FROM          2148  '2148'

 L. 432      2162  LOAD_GLOBAL              os
             2164  LOAD_ATTR                path
             2166  LOAD_METHOD              join
             2168  LOAD_FAST                'plot_dir'
             2170  LOAD_STR                 '{}.{}'
             2172  LOAD_METHOD              format
             2174  LOAD_FAST                'pid'
             2176  LOAD_FAST                'fformat'
             2178  CALL_METHOD_2         2  '2 positional arguments'
             2180  CALL_METHOD_2         2  '2 positional arguments'
             2182  STORE_FAST               'plot_fn'

 L. 433      2184  LOAD_FAST                'fig'
             2186  LOAD_ATTR                savefig
             2188  LOAD_FAST                'plot_fn'
             2190  LOAD_FAST                'fformat'
             2192  LOAD_STR                 'tight'
             2194  LOAD_CONST               ('format', 'bbox_inches')
             2196  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
             2198  POP_TOP          
         2200_2202  JUMP_BACK          2118  'to 2118'
             2204  POP_BLOCK        
           2206_0  COME_FROM_LOOP     2110  '2110'
           2206_1  COME_FROM          2106  '2106'

 L. 436      2206  LOAD_GLOBAL              getattr
             2208  LOAD_GLOBAL              get_template_mod
             2210  CALL_FUNCTION_0       0  '0 positional arguments'
             2212  LOAD_STR                 'base64_plots'
             2214  LOAD_CONST               True
             2216  CALL_FUNCTION_3       3  '3 positional arguments'
             2218  LOAD_CONST               True
             2220  COMPARE_OP               is
         2222_2224  POP_JUMP_IF_FALSE  2298  'to 2298'

 L. 437      2226  LOAD_GLOBAL              io
             2228  LOAD_METHOD              BytesIO
             2230  CALL_METHOD_0         0  '0 positional arguments'
             2232  STORE_FAST               'img_buffer'

 L. 438      2234  LOAD_FAST                'fig'
             2236  LOAD_ATTR                savefig
             2238  LOAD_FAST                'img_buffer'
             2240  LOAD_STR                 'png'
             2242  LOAD_STR                 'tight'
             2244  LOAD_CONST               ('format', 'bbox_inches')
             2246  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
             2248  POP_TOP          

 L. 439      2250  LOAD_GLOBAL              base64
             2252  LOAD_METHOD              b64encode
             2254  LOAD_FAST                'img_buffer'
             2256  LOAD_METHOD              getvalue
             2258  CALL_METHOD_0         0  '0 positional arguments'
             2260  CALL_METHOD_1         1  '1 positional argument'
             2262  LOAD_METHOD              decode
             2264  LOAD_STR                 'utf8'
             2266  CALL_METHOD_1         1  '1 positional argument'
             2268  STORE_FAST               'b64_img'

 L. 440      2270  LOAD_FAST                'img_buffer'
             2272  LOAD_METHOD              close
             2274  CALL_METHOD_0         0  '0 positional arguments'
             2276  POP_TOP          

 L. 441      2278  LOAD_FAST                'html'
             2280  LOAD_STR                 '<div class="mqc_mplplot" id="{}"{}><img src="data:image/png;base64,{}" /></div>'
             2282  LOAD_METHOD              format
             2284  LOAD_FAST                'pid'
             2286  LOAD_FAST                'hidediv'
             2288  LOAD_FAST                'b64_img'
             2290  CALL_METHOD_3         3  '3 positional arguments'
             2292  INPLACE_ADD      
             2294  STORE_FAST               'html'
             2296  JUMP_FORWARD       2340  'to 2340'
           2298_0  COME_FROM          2222  '2222'

 L. 445      2298  LOAD_GLOBAL              os
             2300  LOAD_ATTR                path
             2302  LOAD_METHOD              join
             2304  LOAD_GLOBAL              config
             2306  LOAD_ATTR                plots_dir_name
             2308  LOAD_STR                 'png'
             2310  LOAD_STR                 '{}.png'
             2312  LOAD_METHOD              format
             2314  LOAD_FAST                'pid'
             2316  CALL_METHOD_1         1  '1 positional argument'
             2318  CALL_METHOD_3         3  '3 positional arguments'
             2320  STORE_FAST               'plot_relpath'

 L. 446      2322  LOAD_FAST                'html'
             2324  LOAD_STR                 '<div class="mqc_mplplot" id="{}"{}><img src="{}" /></div>'
             2326  LOAD_METHOD              format
             2328  LOAD_FAST                'pid'
             2330  LOAD_FAST                'hidediv'
             2332  LOAD_FAST                'plot_relpath'
             2334  CALL_METHOD_3         3  '3 positional arguments'
             2336  INPLACE_ADD      
             2338  STORE_FAST               'html'
           2340_0  COME_FROM          2296  '2296'

 L. 448      2340  LOAD_GLOBAL              plt
             2342  LOAD_METHOD              close
             2344  LOAD_FAST                'fig'
             2346  CALL_METHOD_1         1  '1 positional argument'
             2348  POP_TOP          
         2350_2352  JUMP_BACK           386  'to 386'
             2354  POP_BLOCK        
           2356_0  COME_FROM_LOOP      374  '374'

 L. 452      2356  LOAD_FAST                'html'
             2358  LOAD_STR                 '</div>'
             2360  INPLACE_ADD      
             2362  STORE_FAST               'html'

 L. 454      2364  LOAD_GLOBAL              report
             2366  DUP_TOP          
             2368  LOAD_ATTR                num_mpl_plots
             2370  LOAD_CONST               1
             2372  INPLACE_ADD      
             2374  ROT_TWO          
             2376  STORE_ATTR               num_mpl_plots

 L. 456      2378  LOAD_FAST                'html'
             2380  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `JUMP_BACK' instruction at offset 642_644


def smooth_line_data(data, numpoints, sumcounts=True):
    """
    Function to take an x-y dataset and use binning to smooth to a maximum number of datapoints.
    Each datapoint in a smoothed dataset corresponds to the first point in a bin.

    Examples to show the idea:

    d=[0 1 2 3 4 5 6 7 8 9], numpoints=6
    we want to keep the first and the last element, thus excluding the last element from the binning:
    binsize = len([0 1 2 3 4 5 6 7 8]))/(numpoints-1) = 9/5 = 1.8
    taking points in indices rounded from multiples of 1.8: [0, 1.8, 3.6, 5.4, 7.2, 9],
    ...which evaluates to first_element_in_bin_indices=[0, 2, 4, 5, 7, 9]
    picking up the elements: [0 _ 2 _ 4 5 _ 7 _ 9]

    d=[0 1 2 3 4 5 6 7 8 9], numpoints=9
    binsize = 9/8 = 1.125
    indices: [0.0, 1.125, 2.25, 3.375, 4.5, 5.625, 6.75, 7.875, 9] -> [0, 1, 2, 3, 5, 6, 7, 8, 9]
    picking up the elements: [0 1 2 3 _ 5 6 7 8 9]

    d=[0 1 2 3 4 5 6 7 8 9], numpoints=3
    binsize = len(d)/numpoints = 9/2 = 4.5
    incides: [0.0, 4.5, 9] -> [0, 5, 9]
    picking up the elements: [0 _ _ _ _ 5 _ _ _ 9]
    """
    smoothed_data = dict()
    for s_name, d in data.items():
        if not len(d) <= numpoints:
            if len(d) == 0:
                smoothed_data[s_name] = d
                continue
            binsize = (len(d) - 1) / (numpoints - 1)
            first_element_indices = [round(binsize * i) for i in range(numpoints)]
            smoothed_d = OrderedDict((xy for i, xy in enumerate(d.items()) if i in first_element_indices))
            smoothed_data[s_name] = smoothed_d

    return smoothed_data