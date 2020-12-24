# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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