# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.8/site-packages/MetaStalk/modules/PieChart.py
# Compiled at: 2020-05-08 18:09:31
# Size of source mod 2**32: 1754 bytes
"""Module that makes a pie chart."""
import logging
import plotly.graph_objects as go
log = logging.getLogger('MetaStalk')

def create_chart(table: list, pielabel: str) -> go.Figure():
    """Create_chart

    Creates the pie chart by frequency of items in a dictionary.

    Arguments:
        table {list} -- [description]
        pielabel {str} -- The label of the pie chart.

    Returns
        go.Figure -- A plotly PieChart

    """
    freq = {}
    for item in table:
        if item in freq:
            freq[item] += 1
        else:
            freq[item] = 1
    else:
        labels, values = [], []
        for key, value in freq.items():
            if pielabel == 'EXIF FocalLength':
                labels.append('Length: {}'.format(key))
            else:
                labels.append(key)
            values.append(value)
        else:
            fig = go.Figure(data=[
             go.Pie(labels=labels, values=values)])
            fig.update_layout(title=f"{pielabel} Information", title_x=0.5)
            return fig


def pie_chart(photos: list, pietype: str) -> go.Figure():
    """PieChart

    Parses information and returns a pie chart

    Arguments:
        photos {list} -- A list of dictionaries with phot information.
        pietype {str} -- The type of metadata for the pie chart

    Returns:
        go.Figure -- A plotly PieChart

    """
    log.info('Staring %s Chart', pietype)
    table = []
    for each in photos:
        try:
            table.append(str(each[pietype]))
            log.debug('%s has %s data', each['item'], pietype)
        except KeyError:
            log.info('%s has no %s data', each['item'], pietype)

    else:
        return create_chart(table, pietype)