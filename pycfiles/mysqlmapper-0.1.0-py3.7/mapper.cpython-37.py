# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\mysqlmapper\mysql\generate\mapper.py
# Compiled at: 2020-05-12 03:08:39
# Size of source mod 2**32: 9106 bytes
from jinja2 import Environment
_mapper_xml = '\n<xml>\n    <sql>\n        <key>GetList</key>\n        <value>\n            SELECT\n                {% for column in table.columns %}`{{ column.Name }}`{% if not loop.last %}, {% endif %}{% endfor %}\n            FROM\n                {{table.Name}}\n            WHERE\n    {% for column in table.columns %}\n        {% if column.Name != key %}\n            {% if column.Type|clear_type == "varchar" %}\n                {{ "{"|echo }}% if {{ column.Name }} %{{ "}"|echo }} `{{ column.Name }}` LIKE #{ {{ column.Name }} } AND {{ "{"|echo }}% endif %{{ "}"|echo }}\n            {% endif %}\n            {% if column.Type|clear_type == "text" %}\n                {{ "{"|echo }}% if {{ column.Name }} %{{ "}"|echo }} `{{ column.Name }}` LIKE #{ {{ column.Name }} } AND {{ "{"|echo }}% endif %{{ "}"|echo }}\n            {% endif %}\n            {% if column.Type|clear_type == "longtext" %}\n                {{ "{"|echo }}% if {{ column.Name }} %{{ "}"|echo }} `{{ column.Name }}` LIKE #{ {{ column.Name }} } AND {{ "{"|echo }}% endif %{{ "}"|echo }}\n            {% endif %}\n            {% if column.Type|clear_type == "mediumtext" %}\n                {{ "{"|echo }}% if {{ column.Name }} %{{ "}"|echo }} `{{ column.Name }}` LIKE #{ {{ column.Name }} } AND {{ "{"|echo }}% endif %{{ "}"|echo }}\n            {% endif %}\n            {% if column.Type|clear_type == "int" %}\n                {{ "{"|echo }}% if {{ column.Name }} %{{ "}"|echo }}\n                {{ "{"|echo }}% if {{ column.Name }} != 0 %{{ "}"|echo }} `{{ column.Name }}` = #{ {{ column.Name }} } AND {{ "{"|echo }}% endif %{{ "}"|echo }}\n                {{ "{"|echo }}% endif %{{ "}"|echo }}\n            {% endif %}\n            {% if column.Type|clear_type == "datetime" %}\n                {{ "{"|echo }}% if {{ column.Name }} %{{ "}"|echo }}\n                `{{ column.Name }}` = #{ {{ column.Name }}.strftime("%Y-%m-%d %H:%M:%S") } AND\n                {{ "{"|echo }}% endif %{{ "}"|echo }}\n            {% endif %}\n        {% endif %}\n    {% endfor %}\n            1 = 1\n            {% if key == "id" %}\n                ORDER BY id DESC\n            {% endif %}\n            {{ "{"|echo }}% if (Start | default(-1)) != -1 %{{ "}"|echo }} LIMIT #{ Start },#{ Length | default(10) } {{ "{"|echo }}% endif %{{ "}"|echo }}\n        </value>\n    </sql>\n    <sql>\n        <key>GetCount</key>\n        <value>\n            SELECT\n                COUNT(1)\n            FROM\n                {{table.Name}}\n            WHERE\n    {% for column in table.columns %}\n        {% if column.Name != key %}\n            {% if column.Type|clear_type == "varchar" %}\n                {{ "{"|echo }}% if {{ column.Name }} %{{ "}"|echo }} `{{ column.Name }}` LIKE #{ {{ column.Name }} } AND {{ "{"|echo }}% endif %{{ "}"|echo }}\n            {% endif %}\n            {% if column.Type|clear_type == "text" %}\n                {{ "{"|echo }}% if {{ column.Name }} %{{ "}"|echo }} `{{ column.Name }}` LIKE #{ {{ column.Name }} } AND {{ "{"|echo }}% endif %{{ "}"|echo }}\n            {% endif %}\n            {% if column.Type|clear_type == "longtext" %}\n                {{ "{"|echo }}% if {{ column.Name }} %{{ "}"|echo }} `{{ column.Name }}` LIKE #{ {{ column.Name }} } AND {{ "{"|echo }}% endif %{{ "}"|echo }}\n            {% endif %}\n            {% if column.Type|clear_type == "mediumtext" %}\n                {{ "{"|echo }}% if {{ column.Name }} %{{ "}"|echo }} `{{ column.Name }}` LIKE #{ {{ column.Name }} } AND {{ "{"|echo }}% endif %{{ "}"|echo }}\n            {% endif %}\n            {% if column.Type|clear_type == "int" %}\n                {{ "{"|echo }}% if {{ column.Name }} %{{ "}"|echo }}\n                {{ "{"|echo }}% if {{ column.Name }} != 0 %{{ "}"|echo }} `{{ column.Name }}` = #{ {{ column.Name }} } AND {{ "{"|echo }}% endif %{{ "}"|echo }}\n                {{ "{"|echo }}% endif %{{ "}"|echo }}\n            {% endif %}\n            {% if column.Type|clear_type == "datetime" %}\n                {{ "{"|echo }}% if {{ column.Name }} %{{ "}"|echo }}\n                `{{ column.Name }}` = #{ {{ column.Name }}.strftime("%Y-%m-%d %H:%M:%S") } AND\n                {{ "{"|echo }}% endif %{{ "}"|echo }}\n            {% endif %}\n        {% endif %}\n    {% endfor %}\n            1 = 1\n        </value>\n    </sql>\n    <sql>\n        <key>GetModel</key>\n        <value>\n            SELECT\n                {% for column in table.columns %}`{{ column.Name }}`{% if not loop.last %}, {% endif %}{% endfor %}\n            FROM\n                {{table.Name}}\n            WHERE\n                {{key}} = #{ {{key}} }\n        </value>\n    </sql>\n    <sql>\n        <key>Update</key>\n        <value>\n            UPDATE {{table.Name}} SET\n    {% for column in table.columns %}\n        {% if column.Name != key %}\n            {% if column.Type|clear_type == "varchar" %}\n                {{ "{"|echo }}% if {{ column.Name }} %{{ "}"|echo }} `{{ column.Name }}` = #{ {{ column.Name }} }, {{ "{"|echo }}% endif %{{ "}"|echo }}\n            {% endif %}\n            {% if column.Type|clear_type == "text" %}\n                {{ "{"|echo }}% if {{ column.Name }} %{{ "}"|echo }} `{{ column.Name }}` = #{ {{ column.Name }} }, {{ "{"|echo }}% endif %{{ "}"|echo }}\n            {% endif %}\n            {% if column.Type|clear_type == "longtext" %}\n                {{ "{"|echo }}% if {{ column.Name }} %{{ "}"|echo }} `{{ column.Name }}` = #{ {{ column.Name }} }, {{ "{"|echo }}% endif %{{ "}"|echo }}\n            {% endif %}\n            {% if column.Type|clear_type == "mediumtext" %}\n                {{ "{"|echo }}% if {{ column.Name }} %{{ "}"|echo }} `{{ column.Name }}` = #{ {{ column.Name }} }, {{ "{"|echo }}% endif %{{ "}"|echo }}\n            {% endif %}\n            {% if column.Type|clear_type == "int" %}\n                {{ "{"|echo }}% if {{ column.Name }} %{{ "}"|echo }}\n                {{ "{"|echo }}% if {{ column.Name }} != 0 %{{ "}"|echo }} `{{ column.Name }}` = #{ {{ column.Name }} }, {{ "{"|echo }}% endif %{{ "}"|echo }}\n                {{ "{"|echo }}% endif %{{ "}"|echo }}\n            {% endif %}\n            {% if column.Type|clear_type == "datetime" %}\n                {{ "{"|echo }}% if {{ column.Name }} %{{ "}"|echo }}\n                `{{ column.Name }}` = #{ {{ column.Name }}.strftime("%Y-%m-%d %H:%M:%S") },\n                {{ "{"|echo }}% endif %{{ "}"|echo }}\n            {% endif %}\n        {% endif %}\n    {% endfor %}\n            WHERE {{key}} = #{ {{key}} }\n        </value>\n    </sql>\n    <sql>\n        <key>Insert</key>\n        <value>\n            INSERT INTO {{table.Name}}\n            (\n        {% for column in table.columns %}\n            {% if column.Name != key or table.AutoIncrement == -1 %}\n                `{{ column.Name }}`{% if not loop.last %}, {% endif %}\n            {% endif %}\n        {% endfor %}\n            )\n            VALUES\n            (\n    {% for column in table.columns %}\n        {% if column.Name != key or table.AutoIncrement == -1 %}\n            {% if column.Type|clear_type == "datetime" %}\n                #{ {{column.Name}}.strftime("%Y-%m-%d %H:%M:%S") }\n            {% else %}\n                #{ {{column.Name}} }\n            {% endif %}\n            {% if not loop.last %}, {% endif %}\n        {% endif %}\n    {% endfor %}\n            )\n        </value>\n    </sql>\n    <sql>\n        <key>Delete</key>\n        <value>\n            DELETE FROM {{table.Name}} WHERE {{key}} = #{ {{key}} }\n        </value>\n    </sql>\n</xml>\n'

def get_mapper_xml(database_info, table_name):
    """
    Building XML with database description information
    :param database_info: Database description information
    :param table_name: Table name
    :return: XML document
    """
    env = Environment()

    def echo(value):
        """
        Print a character for secondary rendering
        :param value: Characters to be printed
        :return: Original output
        """
        return value

    def clear_type(value):
        """
        Database type cleanup
        :param value:  Database type
        :return: Cleaning results
        """
        return value.split('(')[0]

    env.filters['echo'] = echo
    env.filters['clear_type'] = clear_type
    template = env.from_string(_mapper_xml)
    data = {'data_base_name': database_info['Name']}
    table = None
    for item in database_info['tables']:
        if item['Name'] == table_name:
            table = item
            break

    if table is None:
        return ''
    data['table'] = table
    key = ''
    for item in table['indexs']:
        if item['Name'] == 'PRIMARY':
            key = item['ColumnName']
            break

    if key is None:
        return ''
    data['key'] = key
    return template.render(data)