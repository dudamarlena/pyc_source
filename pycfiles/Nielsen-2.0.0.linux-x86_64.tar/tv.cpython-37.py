# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python3.7/site-packages/nielsen/tv.py
# Compiled at: 2019-11-07 22:38:00
# Size of source mod 2**32: 2814 bytes
"""
Episode title module for Nielsen.
Fetches information from TVmaze.
"""
import logging, requests
from nielsen.config import CONFIG

def select_series(series, results):
    """Return a series from a list of results."""
    if len(results) == 1:
        return results[0]['show']['id']
    print("Search results for '{0}'".format(series))
    for i, result in enumerate(results):
        print('{0}. {1} ({2}) - {3}'.format(i, result['show']['name'], result['show']['premiered'], result['show']['id']))

    print('Other input cancels without selection.')
    try:
        selection = int(input('Select series: '))
        return results[int(selection)]['show']['id']
    except (ValueError, IndexError, EOFError) as e:
        try:
            logging.error('Caught exception: %s', e)
            return
        finally:
            e = None
            del e


def get_series_id(series, interactive=CONFIG.get('Options', 'Interactive')):
    """Return a unique ID for a given series.
        If an ID isn't found in the config, allow the user to select a match from
        search results."""
    series_id = CONFIG.get('IDs', series, fallback=None)
    if not series_id:
        if interactive:
            endpoint = '{0}/search/shows?q={1}'
        else:
            endpoint = '{0}/singlesearch/shows?q={1}'
        endpoint = endpoint.format(CONFIG['Options']['ServiceURI'], series)
        try:
            response = requests.get(endpoint)
        except IOError as e:
            try:
                logging.error('Unable to retrieve series names.')
                logging.debug(e)
                exit()
            finally:
                e = None
                del e

        results = response.json()
        if response.status_code == 200:
            if not interactive:
                series_id = results['id']
            else:
                series_id = select_series(series, results)
    logging.info("Show ID for '%s': %s", series, series_id)
    CONFIG.set('IDs', series, str(series_id))
    return series_id


def get_episode_title(season, episode, series_id=None, series=None):
    """Return the episode title using the series name or ID, season, and
        episode number."""
    if series_id is None:
        if series:
            series_id = get_series_id(series)
    if series_id:
        logging.info('Series ID: %s, Season: %s, Episode: %s', series_id, season, episode)
        try:
            response = requests.get('{0}shows/{1}/episodebynumber?season={2}&number={3}'.format(CONFIG['Options']['ServiceURI'], series_id, season, episode))
            title = response.json()['name']
            logging.info('Title: %s', title)
            return title
        except IOError as e:
            try:
                logging.error('Unable to retrieve episode title.')
                logging.debug(e)
            finally:
                e = None
                del e

    return str()