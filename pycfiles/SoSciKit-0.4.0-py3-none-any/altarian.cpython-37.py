# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\scars\Desktop\marradi_app\soscikit\plotting\altarian.py
# Compiled at: 2019-10-20 16:55:29
# Size of source mod 2**32: 3386 bytes
import altair as alt, pandas as pd, numpy as np

def altair_monovariate(data, options_tipo_var, lista_ordinale):
    datatest = data
    if options_tipo_var == 'cardinale':
        bars = alt.Chart(datatest).mark_bar().encode(x='X:N',
          y='Frequency').encode(tooltip=[
         'X', 'Frequency'])
        text = bars.mark_text(align='left',
          baseline='middle',
          color='blue',
          fontSize=20,
          dx=0,
          dy=(-7)).encode(text='Frequency:Q',
          tooltip=[
         'X', 'Frequency'])
        chart = (bars + text).properties(width=800, height=400).interactive()
    else:
        if options_tipo_var == 'categoriale':
            bars = alt.Chart(datatest).mark_bar().encode(x=alt.X('X:N', sort=alt.EncodingSortField(field='frequency',
              order='descending')),
              y=(alt.Y('Frequency'))).encode(tooltip=[
             'X', 'Frequency'])
            text = bars.mark_text(align='left',
              baseline='middle',
              color='blue',
              fontSize=20,
              dx=0,
              dy=(-7)).encode(text='Frequency:Q',
              tooltip=[
             'X', 'Frequency'])
            chart = (bars + text).properties(width=800, height=400).interactive()
        else:
            if lista_ordinale == True:
                bars = alt.Chart(datatest).mark_bar().encode(x=alt.X('X:N', sort=lista_ordinale),
                  y=(alt.Y('Frequency'))).encode(tooltip=[
                 'X', 'Frequency'])
                text = bars.mark_text(align='left',
                  baseline='middle',
                  color='blue',
                  fontSize=20,
                  dx=0,
                  dy=(-7)).encode(text='Frequency:Q',
                  tooltip=[
                 'X', 'Frequency'])
                chart = (bars + text).properties(width=800, height=400).interactive()
            return chart


def altair_bivariate(dataset, g_x, g_y):
    dataset = dataset.dropna(subset=[g_x, g_y])
    datatest = pd.DataFrame({'X':dataset[g_x],  'Y':dataset[g_y]})
    degree_list = [
     1, 3, 5]
    poly_data = pd.DataFrame({'xfit': np.linspace(datatest['X'].min(), datatest['X'].max(), 500)})
    for degree in degree_list:
        poly_data[str(degree)] = np.poly1d(np.polyfit(datatest['X'], datatest['Y'], degree))(poly_data['xfit'])

    points = alt.Chart(datatest).mark_point().encode(x='X',
      y='Y').encode(tooltip=[
     'X', 'Y'])
    polynomial_fit = alt.Chart(poly_data).transform_fold([
     '1', '3', '5'],
      as_=[
     'degree', 'yfit']).mark_line().encode(x='xfit:Q',
      y='yfit:Q',
      color='degree:N')
    chart = (points + polynomial_fit).properties(width=800, height=400).interactive()
    return chart