# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.5/site-packages/stock/server/main.py
# Compiled at: 2016-06-25 11:05:58
# Size of source mod 2**32: 2657 bytes
from flask import Flask, request, jsonify
from flask import render_template as _render_template
from stock import service
from stock import util
from stock import config as C
app = Flask(__name__)

def render_template(name, **kw):
    kw.update({'C': C, 'service': service})
    return _render_template(name, **kw)


def to_int(key):
    try:
        return int(request.args.get(key))
    except:
        return


@app.route('/', methods=['GET'])
def index():
    field_keys = [
     'ratio_closing1_minus_closing2',
     'ratio_closing_minus_rolling_mean_25',
     'closing_rsi_14',
     'closing_macd_minus_signal',
     'interval_closing_bollinger_band_20',
     'closing_stochastic_d_minus_sd']
    d = {k:to_int(k) for k in field_keys}
    company_list = service.company.get(**d)
    return render_template('index.html', **{'company_list': company_list})


@app.route('/quandl/<string:database_code>/<string:quandl_code>', methods=['GET'])
def get_quandl(database_code, quandl_code):
    code = '%s/%s' % (database_code, quandl_code)
    q = service.quandl.first(code)
    return render_template('quandl_code.html', **{'quandl_code': q})


@app.route('/api/quandl/<string:database_code>/<string:quandl_code>', methods=['GET'])
def api_get_quandl(database_code, quandl_code):
    code = '%s/%s' % (database_code, quandl_code)
    series = service.charts.get_series(code)
    result = service.simulate.RollingMean(series).simulate()
    return jsonify({'series': util.df_to_series(result) + util.df_to_series(series)})


@app.route('/api/quandl/<string:database_code>/<string:quandl_code>/rolling_mean', methods=['GET'])
def rolling_api_get_quandl(database_code, quandl_code):
    code = '%s/%s' % (database_code, quandl_code)
    df = service.charts.get_series(code)
    return jsonify({'series': util.df_to_series(df)})


@app.route('/company/<int:id>', methods=['GET'])
def company(id):
    company = service.company.first(id=id, raise_404=True)
    return render_template('company.html', **{'company': company})


@app.route('/api/<int:company_id>', methods=['GET'])
def api(company_id):
    company = service.company.first(id=company_id, raise_404=True)
    q = service.day_info.get(company_id)
    return jsonify({'company': company.w.to_dict(), 
     'series': q.to_series()})


@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html')