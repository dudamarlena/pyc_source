# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/profpy/web/cli/files/cli.main.py
# Compiled at: 2020-01-09 13:18:17
# Size of source mod 2**32: 437 bytes
from profpy.web import SecureFlaskApp
from profpy.db import get_sql_alchemy_oracle_engine
from flask import render_template
{
 asset_import}
engine = get_sql_alchemy_oracle_engine()
tables = {tables}
app = SecureFlaskApp(__name__, '{app_name}', engine, tables)
{
 asset_config}

@app.route('/index')
@app.secured()
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True, port=8080)