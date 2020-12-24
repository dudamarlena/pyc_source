# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/hydrosql/main.py
# Compiled at: 2016-07-10 00:44:43
import click, jinja2, sqlalchemy as sql
from bottle import request, post, redirect, route, run
DATABASE_URL = None

def get_conn(database_name=None):
    global DATABASE_URL
    url = DATABASE_URL
    if database_name:
        url += '/' + database_name
    engine = sql.create_engine(url, **{'encoding': 'utf-8', 'echo': True})
    conn = engine.connect()
    return conn


def build_select(table_name):
    where = build_where()
    return ('select * from {table_name} {where};').format(**locals())


def build_delete(table_name):
    where = build_where()
    return ('delete from {table_name} {where};').format(**locals())


def build_where():
    where = ''
    if request.params:
        where = 'where ' + (' or ').join("`%s`='%s'" % (k, v) for k, v in request.params.allitems())
    return where


TEMPLATE_TABLE = '\n<script type="text/javascript" src="//code.jquery.com/jquery-2.2.0.min.js"></script>\n<script type="text/javascript">$(function(){\nvar f=$("form[method=get]");\n$("input").on("click", function(evt){ var i=$(this); var input=$("<input>").val(i.val()).attr("name", i.attr("name")); f.append(input)});\n})</script>\n<a href="/">/</a><br/>\n<a href="/{{ database_name }}">{{ database_name }}</a><br/>\n<a href="{{ request.path }}">{{ request.path }}</a><br/>\n{{ query }}</br>\n{{ delete }}</br>\n<form method="post" action="{{ request.path + \'/delete?\' + request.query_string }}"><input type="submit" value="delete"\n      onsubmit="return confirm(\'Do you really want to delete this ?\');" ></form>\n<form method="get" action="{{ request.path }}"><input type="submit" value="filter"></form>\n<table>\n<tr>{% for k in keys %}<td>{{ k }}</td>{% endfor %}</tr>\n{% for row in rows %}\n<tr>\n  {% for r in row %}\n    {% if r is none %}{% set r = \'\' %}{% endif %}\n    <td><input type="text" name=\'{{ keys[loop.index0] }}\' value=\'{{ r }}\' /></td>\n  {% endfor %}\n</tr>\n{% endfor %}\n</table>\n'

@route('/')
def index():
    rows = get_conn().execute('show databases;')
    return jinja2.Template('\n<ul>\n  {% for (db, ) in rows %}\n    <li><a href="/{{ db }}">{{ db }}</a></li>\n  {% endfor %}\n</ul>\n    ').render(rows=rows)


@route('/<database_name>')
def database(database_name):
    rows = get_conn(database_name).execute('show tables;')
    return jinja2.Template('\n<ul>\n  {% for (db, ) in rows %}\n    <li><a href="/{{ database_name }}/{{ db }}">{{ db }}</a></li>\n  {% endfor %}\n</ul>\n    ').render(rows=rows, database_name=database_name)


@post('/<database_name>/<table_name>/delete')
def delete_rows(database_name, table_name):
    if request.params:
        get_conn(database_name).execute(build_delete(table_name))
    redirect('/%s/%s' % (database_name, table_name))


@route('/<database_name>/<table_name>')
def table(database_name, table_name):
    query = build_select(table_name)
    e = get_conn(database_name).execute(query)
    keys = e.keys()
    rows = e.fetchall()
    return jinja2.Template(TEMPLATE_TABLE).render(database_name=database_name, rows=rows, keys=keys, query=query, delete=build_delete(table_name), request=request)


@click.group()
def cli():
    pass


@cli.command()
@click.argument('url')
@click.option('-p', '--port', default=5001)
def start(url, port):
    global DATABASE_URL
    DATABASE_URL = url
    run(host='0.0.0.0', debug=True, port=port)


if __name__ == '__main__':
    cli()