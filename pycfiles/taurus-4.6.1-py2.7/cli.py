# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/taurus/qt/qtgui/qwt5/cli.py
# Compiled at: 2019-08-19 15:09:30
import click
from .taurustrend import TaurusTrend

@click.group('qwt5')
def qwt5():
    """Qwt5 related commands"""
    pass


@qwt5.command('plot')
@click.argument('models', nargs=-1)
@click.option('--config', 'config_file', type=click.File('rb'), help='configuration file for initialization')
@click.option('-x', '--x-axis-mode', 'x_axis_mode', type=click.Choice(['t', 'n']), default='n', show_default=True, help='X axis mode. "t" implies using a Date axis' + '"n" uses the regular axis')
@click.option('--demo', is_flag=True, help='show a demo of the widget')
@click.option('--window-name', 'window_name', default='TaurusPlot (qwt5)', help='Name of the window')
def plot_cmd(models, config_file, x_axis_mode, demo, window_name):
    """Shows a plot for the given models"""
    from .taurusplot import plot_main
    return plot_main(models=models, config_file=config_file, x_axis_mode=x_axis_mode, demo=demo, window_name=window_name)


@qwt5.command('trend')
@click.argument('models', nargs=-1)
@click.option('-x', '--x-axis-mode', 'x_axis_mode', type=click.Choice(['t', 'n']), default='n', show_default=True, help='X axis mode. "t" implies using a Date axis' + '"n" uses the regular axis')
@click.option('-a', '--use-archiving', 'use_archiving', is_flag=True, default=False, help='enable automatic archiving queries')
@click.option('-b', '--buffer', 'max_buffer_size', type=int, default=TaurusTrend.DEFAULT_MAX_BUFFER_SIZE, show_default=True, help='maximum number of values per curve to be plotted')
@click.option('-r', '--forced-read', 'forced_read_period', type=int, default=-1, metavar='MILLISECONDS', help='force re-reading of the attributes every MILLISECONDS ms')
@click.option('--config', 'config_file', type=click.File('rb'), help='configuration file for initialization')
@click.option('--demo', is_flag=True, help='show a demo of the widget')
@click.option('--window-name', 'window_name', default='TaurusPlot (qwt5)', help='Name of the window')
def trend_cmd(models, x_axis_mode, use_archiving, max_buffer_size, forced_read_period, config_file, demo, window_name):
    """Shows a trend for the given models"""
    from .taurustrend import trend_main
    return trend_main(models=models, config_file=config_file, x_axis_mode=x_axis_mode, use_archiving=use_archiving, max_buffer_size=max_buffer_size, forced_read_period=forced_read_period, demo=demo, window_name=window_name)


if __name__ == '__main__':
    qwt5()