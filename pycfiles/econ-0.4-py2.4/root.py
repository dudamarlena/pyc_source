# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.darwin-8.8.0-Power_Macintosh/egg/econ/www/controllers/root.py
# Compiled at: 2007-04-18 06:57:54
import os, urllib, StringIO
from econ.www.lib.base import *
import econ
cfg = econ.conf

class RootController(BaseController):
    __module__ = __name__

    def index(self):
        return render_response('index')

    def current_value(self):
        try:
            year = int(request.params.get('year', 2001))
            currentValue = get_current_value(year)
            c.year = (year,)
            c.ownPath = '/current_value/'
            c.value = currentValue
            return render_response('current_value')
        except Exception, inst:
            return Response('<p><strong>There was an error: ' + str(inst) + '</strong></p>')

    def store(self):
        import econ.store
        index = econ.store.index.items()

        def get_title(_dict):
            if _dict.has_key('title'):
                return _dict['title']
            else:
                return 'No title available'

        storeIndex = [ (ii[0], ii[1].metadata.get('title', 'No title available'), ii[1].data_path) for ii in index ]
        c.store_index = storeIndex
        return render_response('store_index')

    def view(self):
        data_url = request.params.get('data_url', None)
        format = request.params.get('format', 'raw')
        limit = request.params.get('limit', '[:]')
        if not data_url.endswith('.csv'):
            self.response('At present only the viewing of csv format files is supported.')
        fileobj = None
        try:
            fileobj = StringIO.StringIO(urllib.urlopen(data_url).read())
            fileobj = limit_fileobj(fileobj, limit)
        except Exception, inst:
            msg = 'Error: Unable to open and process the data file at %s because %s' % (data_url, inst)
            return Response(msg)

        if format == 'raw':
            result = fileobj.read()
            return Response(result, mimetype='text/plain')
        elif format == 'html':
            import genshi
            c.html_table = genshi.XML(get_html_table(fileobj))
            return render_response('view_html', strip_whitespace=False)
        else:
            msg = 'The format requested, [%s], is unsupported' % format
            return Response('msg')
        return


def get_html_table(fileobj):
    import econ.data.tabular
    reader = econ.data.tabular.ReaderCsv()
    writer = econ.data.tabular.WriterHtml({'id': 'table_1'})
    tabdata = reader.read(fileobj)
    html = writer.write(tabdata)
    return html


def get_current_value(startYear, endYear=2002):
    import econ.data, econ.store, econ.DiscountRate
    databundle = econ.store.index['uk_price_index_1850-2002_annual']
    filePath = databundle.data_path
    ts1 = econ.data.getTimeSeriesFromCsv(file(filePath))
    discounter = econ.DiscountRate.DiscountRateHistorical(ts1)
    return discounter.getReturn(startYear, endYear)


def parse_limit(instr):
    default = (None, None)
    if not (instr.startswith('[') and instr.endswith(']')):
        return default
    newstr = instr[1:-1]
    try:
        (first, second) = newstr.split(':')
    except:
        return default

    if first == '':
        first = None
    else:
        first = int(first)
    if second == '':
        second = None
    else:
        second = int(second)
    return (
     first, second)


def limit_fileobj(fo, limit_str):
    (start, end) = parse_limit(limit_str)
    lines = fo.readlines()
    outlines = lines[start:end]
    outstr = ('').join(outlines)
    outfo = StringIO.StringIO(outstr)
    return outfo