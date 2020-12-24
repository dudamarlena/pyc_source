# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.5/site-packages/stock/cli/scrape.py
# Compiled at: 2017-01-14 02:20:11
# Size of source mod 2**32: 1136 bytes
import click
from .main import cli

@cli.group(name='scrape')
def scrape_():
    pass


_decorator = _multiple_decorator([
 click.option('--scraper', default=scrape.YahooJapan),
 click.option('--start'),
 click.option('--end'),
 click.argument('code', type=int)])

@_decorator
@scrape_.command(name='history')
def scrape_history(code, start, end, scraper):
    history = scraper.history(code, start, end)
    for day_info in history:
        click.echo(day_info)


@_decorator
@scrape_.command(name='split')
def split_stock_date(code, start, end, scraper):
    history = scraper.split_stock_date(code, start, end)
    for day_info in history:
        click.echo(day_info)


@click.option('--scraper', default=scrape.YahooJapan)
@click.argument('code', type=int)
@scrape_.command(name='day_info')
def day_info(code, scraper):
    day_info = scraper.day_info(code)
    click.echo(day_info)


@click.option('--scraper', default=scrape.YahooJapan)
@click.argument('code', type=int)
@scrape_.command(name='value')
def current_value(code, scraper):
    value = scraper.current_value(code)
    click.echo(value)