# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pg_python2/pg_table.py
# Compiled at: 2018-08-03 06:01:13
# Size of source mod 2**32: 3781 bytes
"""
Program's aim is to get tables from a given html
Pure functional.
"""
from BeautifulSoup import BeautifulSoup
import urlparse

def _get_soup(html, elem):
    """
    Soup html element
    :param html:
    :param elem:
    :return:
    """
    soup = BeautifulSoup(html)
    tables = soup.findAll(elem)
    return tables


def _get_fixed_soup(html):
    """
    Fix the soup
    :param html:
    :return:
    """
    tables = _get_soup(html, 'table')
    if tables is not None:
        if len(tables) > 0:
            return tables
    trs = _get_soup(html, 'tr')
    if trs is not None:
        return _get_soup('<table>' + html + '</table>', 'table')


def _get_header_cells(soup):
    all_th = []
    th = soup('th')
    for i in th:
        all_th.append(i.text)

    return all_th


def _get_caption_cells(soup):
    all_th = []
    th = soup('caption')
    for i in th:
        all_th.append(i.text)

    return all_th


def get_table(html):
    """
    :param html: html of a page.
    :return: (number of tables found, {'header' : top_row, 'data' : other_rows})
    """
    all_tables = []
    soup = _get_fixed_soup(html)
    if not soup:
        return (0, None)
    else:
        count = 0
        if type(soup) == list:
            for s in soup:
                rows = [[cell.text for cell in row('td')] for row in s('tr')]
                count = count + 1
                first_row = _get_header_cells(s)
                caption = _get_caption_cells(s)
                all_tables.append({'header':first_row,  'data':rows,  'title':caption})

        else:
            rows = [[cell.text for cell in row('td')] for row in soup('tr')]
            count = count + 1
            first_row = _get_header_cells(soup)
            caption = _get_caption_cells(soup)
            all_tables.append({'header':first_row,  'data':rows,  'title':caption})
        return (
         count, all_tables)


def get_table_with_links(html, base_url):
    """
    Fetch all tables in the html that contain links,
    returns a list of dictionaries with {header : [], data : [[]], num_links : 4}
    :param html:
    :return:
    """
    all_tables = []
    soup = _get_fixed_soup(html)
    if not soup:
        return (0, None)
    else:
        count = 0
        if type(soup) == list:
            for s in soup:
                rows = [[cell.text for cell in row('td')] for row in s('tr')]
                links = [[_fix_url(cell, base_url) for cell in row('td')] for row in s('tr')]
                count = count + 1
                first_row = _get_header_cells(s)
                caption = _get_caption_cells(s)
                all_tables.append({'header':first_row,  'data':rows,  'title':caption,  'links':links})

        else:
            rows = [[cell.text for cell in row('td')] for row in soup('tr')]
            links = [[cell.findAll('a') for cell in row('td')] for row in soup('tr')]
            count = count + 1
            first_row = _get_header_cells(soup)
            caption = _get_caption_cells(soup)
            all_tables.append({'header':first_row,  'data':rows,  'title':caption,  'links':links})
        return (
         count, all_tables)


def _fix_url(soup, base_url):
    aa = soup.findAll('a')
    a_href = None
    for a in aa:
        try:
            a_href_rel = a['href']
            a_href = urlparse.urljoin(base_url, a_href_rel)
        except Exception as e:
            continue

    return a_href


if __name__ == '__main__':
    import requests
    base_url = 'http://www.jreda.com/tenders/tenders.htm'
    r = requests.get(base_url)
    num, tables = get_table_with_links(r.content, base_url)
    print(num)
    for table in tables:
        for link in table['links']:
            print(link)