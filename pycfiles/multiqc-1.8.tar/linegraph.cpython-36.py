# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
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
    print('##### ERROR! MatPlotLib library could not be loaded!    #####', file=(sys.stderr))
    print('##### Flat plots will instead be plotted as interactive #####', file=(sys.stderr))
    print(e)

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

            else:
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
                                else:
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
                            else:
                                pairs.append([k, d[s][k]])
                                try:
                                    maxval = max(maxval, d[s][k])
                                except TypeError:
                                    pass

                    if maxval > 0 or series_config.get('hide_empty') is not True:
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
            if config.plots_force_flat or not config.plots_force_interactive and len(plotdata[0]) > config.plots_flat_numseries:
                try:
                    return matplotlib_linegraph(plotdata, pconfig)
                except Exception as e:
                    logger.error('############### Error making MatPlotLib figure! Falling back to HighCharts.')
                    logger.debug(e, exc_info=True)
                    return highcharts_linegraph(plotdata, pconfig)

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
    else:
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


def matplotlib_linegraph(plotdata, pconfig=None):
    """
    Plot a line graph with Matplot lib and return a HTML string. Either embeds a base64
    encoded image within HTML or writes the plot and links to it. Should be called by
    plot_bargraph, which properly formats the input data.
    """
    if pconfig is None:
        pconfig = {}
    else:
        if pconfig.get('id') is None:
            pconfig['id'] = 'mqc_mplplot_' + ''.join(random.sample(letters, 10))
        pconfig['id'] = report.save_htmlid(pconfig['id'])
        pids = []
        for k in range(len(plotdata)):
            try:
                name = pconfig['data_labels'][k]['name']
            except:
                name = k + 1

            pid = 'mqc_{}_{}'.format(pconfig['id'], name)
            pid = report.save_htmlid(pid, skiplint=True)
            pids.append(pid)

        html = '<p class="text-info"><small><span class="glyphicon glyphicon-picture" aria-hidden="true"></span> ' + 'Flat image plot. Toolbox functions such as highlighting / hiding samples will not work ' + '(see the <a href="http://multiqc.info/docs/#flat--interactive-plots" target="_blank">docs</a>).</small></p>'
        html += '<div class="mqc_mplplot_plotgroup" id="{}">'.format(pconfig['id'])
        default_colors = [
         '#7cb5ec', '#434348', '#90ed7d', '#f7a35c', '#8085e9',
         '#f15c80', '#e4d354', '#2b908f', '#f45b5b', '#91e8e1']
        if len(plotdata) > 1 and not config.simple_output:
            html += '<div class="btn-group mpl_switch_group mqc_mplplot_bargraph_switchds">\n'
            for k, p in enumerate(plotdata):
                pid = pids[k]
                active = 'active' if k == 0 else ''
                try:
                    name = pconfig['data_labels'][k]['name']
                except:
                    name = k + 1

                html += '<button class="btn btn-default btn-sm {a}" data-target="#{pid}">{n}</button>\n'.format(a=active, pid=pid, n=name)

            html += '</div>\n\n'
    for pidx, pdata in enumerate(plotdata):
        pid = pids[pidx]
        fdata = OrderedDict()
        lastcats = None
        sharedcats = True
        for d in pdata:
            fdata[d['name']] = OrderedDict()
            for i, x in enumerate(d['data']):
                if type(x) is list:
                    fdata[d['name']][str(x[0])] = x[1]
                    if lastcats is None:
                        lastcats = [x[0] for x in d['data']]
                    elif lastcats != [x[0] for x in d['data']]:
                        pass
                    sharedcats = False
                else:
                    try:
                        fdata[d['name']][pconfig['categories'][i]] = x
                    except (KeyError, IndexError):
                        fdata[d['name']][str(i)] = x

        if not sharedcats:
            if config.data_format == 'tsv':
                fout = ''
                for d in pdata:
                    fout += '\t' + '\t'.join([str(x[0]) for x in d['data']])
                    fout += '\n{}\t'.format(d['name'])
                    fout += '\t'.join([str(x[1]) for x in d['data']])
                    fout += '\n'

                with io.open((os.path.join(config.data_dir, '{}.txt'.format(pid))), 'w', encoding='utf-8') as (f):
                    print((fout.encode('utf-8', 'ignore').decode('utf-8')), file=f)
        else:
            util_functions.write_data_file(fdata, pid)
        fig = plt.figure(figsize=(14, 6), frameon=False)
        axes = fig.add_subplot(111)
        for idx, d in enumerate(pdata):
            cidx = idx
            while cidx >= len(default_colors):
                cidx -= len(default_colors)

            linestyle = 'solid'
            if d.get('dashStyle', None) == 'Dash':
                linestyle = 'dashed'
            try:
                axes.plot([x[0] for x in d['data']], [x[1] for x in d['data']], label=(d['name']), color=(d.get('color', default_colors[cidx])), linestyle=linestyle, linewidth=1, marker=None)
            except TypeError:
                axes.plot((d['data']), label=(d['name']), color=(d.get('color', default_colors[cidx])), linewidth=1, marker=None)

        axes.tick_params(labelsize=8, direction='out', left=False, right=False, top=False, bottom=False)
        axes.set_xlabel(pconfig.get('xlab', ''))
        axes.set_ylabel(pconfig.get('ylab', ''))
        try:
            axes.set_ylabel(pconfig['data_labels'][pidx]['ylab'])
        except:
            pass

        default_ylimits = axes.get_ylim()
        ymin = default_ylimits[0]
        if 'ymin' in pconfig:
            ymin = pconfig['ymin']
        elif 'yFloor' in pconfig:
            ymin = max(pconfig['yFloor'], default_ylimits[0])
        else:
            ymax = default_ylimits[1]
            if 'ymax' in pconfig:
                ymax = pconfig['ymax']
            else:
                if 'yCeiling' in pconfig:
                    ymax = min(pconfig['yCeiling'], default_ylimits[1])
            if ymax - ymin < pconfig.get('yMinRange', 0):
                ymax = ymin + pconfig['yMinRange']
            axes.set_ylim((ymin, ymax))
            try:
                axes.set_ylim((ymin, pconfig['data_labels'][pidx]['ymax']))
            except:
                pass

        default_xlimits = axes.get_xlim()
        xmin = default_xlimits[0]
        if 'xmin' in pconfig:
            xmin = pconfig['xmin']
        else:
            if 'xFloor' in pconfig:
                xmin = max(pconfig['xFloor'], default_xlimits[0])
            else:
                xmax = default_xlimits[1]
                if 'xmax' in pconfig:
                    xmax = pconfig['xmax']
                else:
                    if 'xCeiling' in pconfig:
                        xmax = min(pconfig['xCeiling'], default_xlimits[1])
                    else:
                        if xmax - xmin < pconfig.get('xMinRange', 0):
                            xmax = xmin + pconfig['xMinRange']
                        else:
                            axes.set_xlim((xmin, xmax))
                            if 'title' in pconfig:
                                plt.text(0.5, 1.05, (pconfig['title']), horizontalalignment='center', fontsize=16, transform=(axes.transAxes))
                            axes.grid(True, zorder=10, which='both', axis='y', linestyle='-', color='#dedede', linewidth=1)
                            if 'categories' in pconfig:
                                axes.set_xticks([i for i, v in enumerate(pconfig['categories'])])
                                axes.set_xticklabels(pconfig['categories'])
                            xlim = axes.get_xlim()
                            axes.plot([xlim[0], xlim[1]], [0, 0], linestyle='-', color='#dedede', linewidth=2)
                            axes.set_axisbelow(True)
                            axes.spines['right'].set_visible(False)
                            axes.spines['top'].set_visible(False)
                            axes.spines['bottom'].set_visible(False)
                            axes.spines['left'].set_visible(False)
                            if 'yPlotBands' in pconfig:
                                xlim = axes.get_xlim()
                                for pb in pconfig['yPlotBands']:
                                    axes.barh((pb['from']), (xlim[1]), height=(pb['to'] - pb['from']), left=(xlim[0]), color=(pb['color']), linewidth=0, zorder=0, align='edge')

                        if 'xPlotBands' in pconfig:
                            ylim = axes.get_ylim()
                            for pb in pconfig['xPlotBands']:
                                axes.bar((pb['from']), (ylim[1]), width=(pb['to'] - pb['from']), bottom=(ylim[0]), color=(pb['color']), linewidth=0, zorder=0, align='edge')

                    if len(pdata) <= 15:
                        axes.legend(loc='lower center', bbox_to_anchor=(0, -0.22, 1,
                                                                        0.102), ncol=5, mode='expand', fontsize=8, frameon=False)
                        plt.tight_layout(rect=[0, 0.08, 1, 0.92])
                    else:
                        plt.tight_layout(rect=[0, 0, 1, 0.92])
                hidediv = ''
                if pidx > 0:
                    hidediv = ' style="display:none;"'
                if config.export_plots:
                    for fformat in config.export_plot_formats:
                        plot_dir = os.path.join(config.plots_dir, fformat)
                        if not os.path.exists(plot_dir):
                            os.makedirs(plot_dir)
                        plot_fn = os.path.join(plot_dir, '{}.{}'.format(pid, fformat))
                        fig.savefig(plot_fn, format=fformat, bbox_inches='tight')

            if getattr(get_template_mod(), 'base64_plots', True) is True:
                img_buffer = io.BytesIO()
                fig.savefig(img_buffer, format='png', bbox_inches='tight')
                b64_img = base64.b64encode(img_buffer.getvalue()).decode('utf8')
                img_buffer.close()
                html += '<div class="mqc_mplplot" id="{}"{}><img src="data:image/png;base64,{}" /></div>'.format(pid, hidediv, b64_img)
            else:
                plot_relpath = os.path.join(config.plots_dir_name, 'png', '{}.png'.format(pid))
                html += '<div class="mqc_mplplot" id="{}"{}><img src="{}" /></div>'.format(pid, hidediv, plot_relpath)
        plt.close(fig)

    html += '</div>'
    report.num_mpl_plots += 1
    return html


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
        if len(d) <= numpoints or len(d) == 0:
            smoothed_data[s_name] = d
        else:
            binsize = (len(d) - 1) / (numpoints - 1)
            first_element_indices = [round(binsize * i) for i in range(numpoints)]
            smoothed_d = OrderedDict(xy for i, xy in enumerate(d.items()) if i in first_element_indices)
            smoothed_data[s_name] = smoothed_d

    return smoothed_data