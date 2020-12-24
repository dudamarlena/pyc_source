# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/buzzword/__main__.py
# Compiled at: 2019-08-23 17:50:29
# Size of source mod 2**32: 3434 bytes
"""
buzzword: main file.

Get the needed data from .parts.main, and provide the callback for URL bar.

By calling it __main__.py, we can start the app with `python -m buzzword`
"""
import os, dash_core_components as dcc, dash_html_components as html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from .parts import start, explore
from parts.main import app, server
from parts.main import ROOT, CORPORA, CORPUS_META, CORPORA_CONFIGS
from parts.tabs import _make_tabs
from parts.helpers import _get_corpus, _get_initial_table
for path in {'uploads', 'csv'}:
    if not os.path.isdir(path):
        os.makedirs('csv')

def _get_layout():
    """
    Function for layout. Could be helpful in future to do it this way.
    """
    loc = dcc.Location(id='url', refresh=False)
    search_store = dcc.Store(id='session-search', data=(dict()))
    tables_store = dcc.Store(id='session-tables', data=(dict()))
    click_clear = dcc.Store(id='session-clicks-clear', data=(-1))
    click_table = dcc.Store(id='session-clicks-table', data=(-1))
    configs = dcc.Store(id='session-configs', data=CORPORA_CONFIGS)
    content = html.Div(id='page-content')
    stores = [search_store, tables_store, click_clear, click_table, configs]
    return html.Div([loc] + stores + [content])


app.layout = _get_layout
LAYOUTS = dict()

def _make_explore_layout(slug, conf):
    """
    Simulate globals and generate layout for explore page
    """
    from buzzword.parts.start import CORPORA, INITIAL_TABLES, CORPORA_CONFIGS
    corpus = _get_corpus(slug)
    table = _get_initial_table(slug)
    conf['len'] = conf.get('len', len(corpus))
    conf['slug'] = slug
    return _make_tabs(corpus, table, conf)


def _populate_explore_layouts():
    """
    Can be used to create explore page on startup, save loading time

    broken right now, unused
    """
    for name, meta in CORPUS_META.items():
        slug = meta['slug']
        LAYOUTS[slug] = _make_explore_layout(slug, meta)


def _get_explore_layout(slug, all_configs):
    """
    Get (and maybe generate) the explore layout for this slug
    """
    conf = all_configs.get(slug)
    if not conf:
        return
    if slug in LAYOUTS:
        return LAYOUTS[slug]
    layout = _make_explore_layout(slug, conf)
    LAYOUTS[slug] = layout
    return layout


@app.callback(Output('page-content', 'children'), [Input('url', 'pathname')], [State('session-configs', 'data')])
def _choose_correct_page(pathname, configs):
    """
    When the URL changes, get correct page and populate page-content with it
    """
    if pathname is None:
        raise PreventUpdate
    else:
        pathname = pathname.lstrip('/')
        if pathname.startswith('explore'):
            slug = pathname.rstrip('/').split('/')[(-1)]
            if slug not in CORPORA:
                pathname = ''
            layout = _get_explore_layout(slug, configs)
            if layout:
                return layout
        return pathname or start.layout
    return '404. Page not found: {}'.format(pathname)


if __name__ == '__main__':
    app.run_server(debug=True)