# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/olek/Wszystkie_aggrescamy_swiata/aggrescan3d/a3d_gui/server_plot.py
# Compiled at: 2018-12-13 09:14:35
from bokeh.plotting import figure, output_file, ColumnDataSource, save, show
from bokeh.models import HoverTool, FactorRange, Legend
from bokeh.models.glyphs import Line
from bokeh.resources import INLINE
from bokeh.util.string import encode_utf8
import bokeh.palettes
from bokeh.embed import components
from os.path import join
aa_dict_F = {'A': 'alanine', 'R': 'arginine', 'N': 'asparagine', 'D': 'aspartic acid', 
   'C': 'cysteine', 'E': 'glutamic acid', 'Q': 'glutamine', 
   'G': 'glycine', 'H': 'histidine', 'I': 'isoleucine', 
   'L': 'leucine', 'K': 'lysine', 'M': 'methionine', 
   'F': 'phenylalanine', 'P': 'proline', 'S': 'serine', 
   'T': 'threonine', 'W': 'tryptophan', 'Y': 'tyrosine', 
   'V': 'valine', 'X': 'unknown'}

def create_mut_plot(data_dir, save_plot=False):
    mutants = [
     '']
    max_mutants, counter = (12, 0)
    p = []
    with open(join(data_dir, 'Mutations_summary.csv'), 'r') as (f):
        f.readline()
        for line in f:
            mutants.append(line.split(',')[0])
            counter += 1
            if counter >= max_mutants:
                break

    counter = 0
    colors = bokeh.palettes.Category10[10]
    colors.append('#1E1717')
    colors.append('#f3ff00')
    colors.append('#ce6778')
    legend_items = []
    for mutant in mutants:
        x, y, chain, name, index, status = ([], [], [], [], [], [])
        mutant = mutant if mutant else 'A3D'
        with open(join(data_dir, mutant + '.csv'), 'r') as (f):
            if mutant == 'A3D':
                mutant = 'Wild type'
            f.readline()
            for line in f:
                a = line.strip().split(',')
                x.append(('Chain %s' % a[1], a[2] + a[1]))
                y.append(float(a[(-1)]))
                name.append(aa_dict_F[a[(-2)]])
                index.append(a[2])
                chain.append(a[1])
                status.append('Soluble' if float(a[(-1)]) <= 0 else 'Aggregation prone')

        if not p:
            p = figure(plot_width=1150, plot_height=600, tools=['box_zoom,pan,reset,save'], title='Score breakdown for mutants. Click on the legend to hide/show the line. Mouse over a point to see details.', x_range=FactorRange(*x), toolbar_location='below')
            p.xaxis.major_tick_line_color = None
            p.xaxis.minor_tick_line_color = None
            p.yaxis.minor_tick_line_color = None
            p.xaxis.major_label_text_font_size = '0pt'
            p.xgrid.grid_line_color = None
            p.ygrid.grid_line_color = None
        mut_names = [ mutant for i in range(len(x)) ]
        source = ColumnDataSource(data=dict(x=x, y=y, line_y=[ 0 for i in range(len(x)) ], name=name, index=index, status=status, chain=chain, mut_name=mut_names))
        hover = HoverTool(tooltips=[
         ('Chain', '@chain'),
         ('Residue name', '@name'),
         ('Residue index', '@index'),
         ('Prediction', '@status'),
         ('Mutant', '@mut_name')], mode='vline', names=[
         mutant])
        the_line = p.line('x', 'y', source=source, name=mutant, color=colors[counter], line_width=2.5, line_alpha=1.0)
        legend_items.append((mutant, [the_line]))
        if counter not in (0, 1):
            the_line.visible = False
        p.add_tools(hover)
        counter += 1

    legend = Legend(items=legend_items, click_policy='hide')
    p.add_layout(legend, 'left')
    script, div = components(p)
    if save_plot:
        save(p, filename='Automated_mutations', title='Mutation analysis')
    else:
        return (
         script, div)
    return


def create_plot(csv_address, model):
    x, y, chain, name, index, status = ([], [], [], [], [], [])
    with open(csv_address, 'r') as (f):
        f.readline()
        for line in f:
            a = line.strip().split(',')
            x.append(('Chain %s' % a[1], a[2] + a[1]))
            y.append(float(a[(-1)]))
            name.append(aa_dict_F[a[(-2)]])
            index.append(a[2])
            chain.append(a[1])
            status.append('Soluble' if float(a[(-1)]) <= 0 else 'Aggregation prone')

    source = ColumnDataSource(data=dict(x=x, y=y, line_y=[ 0 for i in range(len(x)) ], name=name, index=index, status=status, chain=chain))
    hover = HoverTool(tooltips=[
     ('Chain', '@chain'),
     ('Residue name', '@name'),
     ('Residue index', '@index'),
     ('Prediction', '@status')], mode='vline', names=[
     'line'])
    p = figure(plot_width=1150, plot_height=600, tools=[hover, 'box_zoom,pan,reset,save'], title="Aggrescan3D score based on residue for %s. Mouse over the plot to see residue's details" % model, x_range=FactorRange(*x), toolbar_location='below')
    p.xaxis.major_tick_line_color = None
    p.xaxis.minor_tick_line_color = None
    p.yaxis.minor_tick_line_color = None
    p.xaxis.major_label_text_font_size = '0pt'
    p.xgrid.grid_line_color = None
    p.ygrid.grid_line_color = None
    p.line('x', 'y', source=source, name='line')
    glyph = Line(x='x', y='line_y', line_color='#f46d43', line_width=2, line_alpha=0.3)
    p.add_glyph(source, glyph)
    script, div = components(p)
    return (
     script, div)