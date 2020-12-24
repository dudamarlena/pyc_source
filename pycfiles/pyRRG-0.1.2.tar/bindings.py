# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\pyrrd\backend\bindings.py
# Compiled at: 2013-08-12 02:05:53
__doc__ = '\nThe following exercises the RRD class with this backend:\n\nCreate an RRD file programmatically::\n\n    >>> import tempfile\n    >>> from pyrrd.rrd import DataSource, RRA, RRD\n    >>> from pyrrd.backend import bindings\n\n    >>> rrdfile = "/tmp/tmprrdfile.rrd"\n    >>> dataSources = []\n    >>> roundRobinArchives = []\n    >>> dataSource = DataSource(\n    ...     dsName=\'speed\', dsType=\'COUNTER\', heartbeat=600)\n    >>> dataSources.append(dataSource)\n    >>> roundRobinArchives.append(RRA(cf=\'AVERAGE\', xff=0.5, steps=1, rows=24))\n    >>> roundRobinArchives.append(RRA(cf=\'AVERAGE\', xff=0.5, steps=6, rows=10))\n\n    >>> myRRD = RRD(rrdfile, ds=dataSources, rra=roundRobinArchives, \n    ...     start=920804400, backend=bindings)\n    >>> myRRD.create()\n\nLet\'s check to see that the file exists::\n\n    >>> import os\n    >>> os.path.isfile(rrdfile)\n    True\n\nLet\'s see how big it is::\n\n    >>> bytes = len(open(rrdfile).read())\n    >>> 800 < bytes < 1200\n    True\n\nIn order to save writes to disk, PyRRD buffers values and then writes the\nvalues to the RRD file at one go::\n\n    >>> myRRD.bufferValue(\'920805600\', \'12363\')\n    >>> myRRD.bufferValue(\'920805900\', \'12363\')\n    >>> myRRD.bufferValue(\'920806200\', \'12373\')\n    >>> myRRD.bufferValue(\'920806500\', \'12383\')\n    >>> myRRD.update()\n\nLet\'s add some more data::\n\n    >>> myRRD.bufferValue(\'920806800\', \'12393\')\n    >>> myRRD.bufferValue(\'920807100\', \'12399\')\n    >>> myRRD.bufferValue(\'920807400\', \'12405\')\n    >>> myRRD.bufferValue(\'920807700\', \'12411\')\n    >>> myRRD.bufferValue(\'920808000\', \'12415\')\n    >>> myRRD.bufferValue(\'920808300\', \'12420\')\n    >>> myRRD.bufferValue(\'920808600\', \'12422\')\n    >>> myRRD.bufferValue(\'920808900\', \'12423\')\n    >>> myRRD.update()\n\nInfo checks when the RRD object is in write mode::\n\n    >>> myRRD.info() # doctest:+ELLIPSIS\n    lastupdate = 920808900\n    rra = [{\'rows\': 24, \'database\': None, \'cf\': \'AVERAGE\', \'cdp_prep\': None, \'beta\': None, \'seasonal_period\': None, \'steps\': 1, \'window_length\': None, \'threshold\': None, \'alpha\': None, \'pdp_per_row\': None, \'xff\': 0.5, \'ds\': [], \'gamma\': None, \'rra_num\': None}, {\'rows\': 10, \'database\': None, \'cf\': \'AVERAGE\', \'cdp_prep\': None, \'beta\': None, \'seasonal_period\': None, \'steps\': 6, \'window_length\': None, \'threshold\': None, \'alpha\': None, \'pdp_per_row\': None, \'xff\': 0.5, \'ds\': [], \'gamma\': None, \'rra_num\': None}]\n    filename = /tmp/...\n    start = 920804400\n    step = 300\n    values = []\n    ds = [{\'name\': \'speed\', \'min\': \'U\', \'max\': \'U\', \'unknown_sec\': None, \'minimal_heartbeat\': 600, \'value\': None, \'rpn\': None, \'type\': \'COUNTER\', \'last_ds\': None}]\n    ds[speed].name = speed\n    ds[speed].min = U\n    ds[speed].max = U\n    ds[speed].minimal_heartbeat = 600\n    ds[speed].type = COUNTER\n    rra[0].rows = 24\n    rra[0].cf = AVERAGE\n    rra[0].steps = 1\n    rra[0].xff = 0.5\n    rra[0].ds = []\n    rra[1].rows = 10\n    rra[1].cf = AVERAGE\n    rra[1].steps = 6\n    rra[1].xff = 0.5\n    rra[1].ds = []\n\nIn order to create a graph, we\'ll need some data definitions. We\'ll also\nthrow in some calculated definitions and variable definitions for good\nmeansure::\n\n    >>> from pyrrd.graph import DEF, CDEF, VDEF, LINE, AREA, GPRINT\n    >>> def1 = DEF(rrdfile=myRRD.filename, vname=\'myspeed\',\n    ...     dsName=dataSource.name)\n    >>> cdef1 = CDEF(vname=\'kmh\', rpn=\'%s,3600,*\' % def1.vname)\n    >>> cdef2 = CDEF(vname=\'fast\', rpn=\'kmh,100,GT,kmh,0,IF\')\n    >>> cdef3 = CDEF(vname=\'good\', rpn=\'kmh,100,GT,0,kmh,IF\')\n    >>> vdef1 = VDEF(vname=\'mymax\', rpn=\'%s,MAXIMUM\' % def1.vname)\n    >>> vdef2 = VDEF(vname=\'myavg\', rpn=\'%s,AVERAGE\' % def1.vname)\n\n    >>> line1 = LINE(value=100, color=\'#990000\', legend=\'Maximum Allowed\')\n    >>> area1 = AREA(defObj=cdef3, color=\'#006600\', legend=\'Good Speed\')\n    >>> area2 = AREA(defObj=cdef2, color=\'#CC6633\', legend=\'Too Fast\')\n    >>> line2 = LINE(defObj=vdef2, color=\'#000099\', legend=\'My Average\', \n    ...     stack=True)\n    >>> gprint1 = GPRINT(vdef2, \'%6.2lf kph\')\n\nColor is the spice of life. Let\'s spice it up a little::\n\n    >>> from pyrrd.graph import ColorAttributes\n    >>> ca = ColorAttributes()\n    >>> ca.back = \'#333333\'\n    >>> ca.canvas = \'#333333\'\n    >>> ca.shadea = \'#000000\'\n    >>> ca.shadeb = \'#111111\'\n    >>> ca.mgrid = \'#CCCCCC\'\n    >>> ca.axis = \'#FFFFFF\'\n    >>> ca.frame = \'#AAAAAA\'\n    >>> ca.font = \'#FFFFFF\'\n    >>> ca.arrow = \'#FFFFFF\'\n\nNow we can create a graph for the data in our RRD file::\n\n    >>> from pyrrd.graph import Graph\n    >>> graphfile = tempfile.NamedTemporaryFile(suffix=".png")\n    >>> g = Graph(graphfile.name, start=920805000, end=920810000,\n    ...     vertical_label=\'km/h\', color=ca, backend=bindings)\n    >>> g.data.extend([def1, cdef1, cdef2, cdef3, vdef1, vdef2, line1, area1,\n    ...     area2, line2, gprint1])\n    >>> g.write()\n\nLet\'s make sure it\'s there::\n\n    >>> os.path.isfile(graphfile.name)\n    True\n\nLet\'s see how big it is::\n\n    >>> bytes = len(open(graphfile.name).read())\n    >>> bytes != 0\n    True\n    >>> 8000 < bytes < 10700\n    True\n\nOpen that up in your favorite image browser and confirm that the appropriate\nRRD graph is generated.\n\n\n    # Cleanup:\n    >>> os.unlink(rrdfile)\n    >>> os.path.exists(rrdfile)\n    False\n'
import rrdtool
from pyrrd.backend import external
from pyrrd.backend.common import buildParameters

def _cmd(command, args, debug=False):
    function = getattr(rrdtool, command)
    args = [ str(x) for x in args ]
    if debug:
        print 'function:', function
        print 'args:', args
    return function(*args)


def create(filename, parameters):
    """
    >>> rrdfile = '/tmp/test.rrd'
    >>> parameters = [
    ...   '--start',
    ...   '920804400',
    ...   'DS:speed:COUNTER:600:U:U',
    ...   'RRA:AVERAGE:0.5:1:24',
    ...   'RRA:AVERAGE:0.5:6:10']
    >>> create(rrdfile, parameters)

    # Check that the file's there:
    >>> import os
    >>> os.path.exists(rrdfile)
    True

    # Cleanup:
    >>> os.unlink(rrdfile)
    >>> os.path.exists(rrdfile)
    False
    """
    parameters.insert(0, filename)
    output = _cmd('create', parameters, debug=True)


def update(filename, parameters, debug=False):
    """
    >>> rrdfile = '/tmp/test.rrd'
    >>> parameters = [
    ...   '--start',
    ...   '920804400',
    ...   'DS:speed:COUNTER:600:U:U',
    ...   'RRA:AVERAGE:0.5:1:24',
    ...   'RRA:AVERAGE:0.5:6:10']
    >>> create(rrdfile, parameters)

    >>> import os
    >>> os.path.exists(rrdfile)
    True

    >>> parameters = ['920804700:12345', '920805000:12357', '920805300:12363']
    >>> update(rrdfile, parameters)
    >>> parameters = ['920805600:12363', '920805900:12363','920806200:12373']
    >>> update(rrdfile, parameters)
    >>> parameters = ['920806500:12383', '920806800:12393','920807100:12399']
    >>> update(rrdfile, parameters)
    >>> parameters = ['920807400:12405', '920807700:12411', '920808000:12415']
    >>> update(rrdfile, parameters)
    >>> parameters = ['920808300:12420', '920808600:12422','920808900:12423']
    >>> update(rrdfile, parameters)

    >>> os.unlink(rrdfile)
    >>> os.path.exists(rrdfile)
    False
    """
    parameters.insert(0, filename)
    if debug:
        _cmd('updatev', parameters)
    else:
        _cmd('update', parameters)


def fetch(filename, parameters, useBindings=False):
    """
    By default, this function does not use the bindings for fetch. The reason
    for this is we want default compatibility with the data output/results from
    the fetch method for both the external and bindings modules.

    If a developer really wants to use the native bindings to get the fetch
    data, they may do so by explicitly setting the useBindings parameter. This
    will return data in the Python Python bindings format, though.

    Do be aware, though, that the PyRRD format is much easier to get data out
    of in a sensible manner (unless you really like the RRDTool approach).

    >>> rrdfile = '/tmp/test.rrd'
    >>> parameters = [
    ...   '--start',
    ...   '920804400',
    ...   'DS:speed:COUNTER:600:U:U',
    ...   'RRA:AVERAGE:0.5:1:24',
    ...   'RRA:AVERAGE:0.5:6:10']
    >>> create(rrdfile, parameters)

    >>> import os
    >>> os.path.exists(rrdfile)
    True

    >>> parameters = ['920804700:12345', '920805000:12357', '920805300:12363']
    >>> update(rrdfile, parameters)
    >>> parameters = ['920805600:12363', '920805900:12363','920806200:12373']
    >>> update(rrdfile, parameters)
    >>> parameters = ['920806500:12383', '920806800:12393','920807100:12399']
    >>> update(rrdfile, parameters)
    >>> parameters = ['920807400:12405', '920807700:12411', '920808000:12415']
    >>> update(rrdfile, parameters)
    >>> parameters = ['920808300:12420', '920808600:12422','920808900:12423']
    >>> update(rrdfile, parameters)

    >>> parameters = ['AVERAGE', '--start', '920804400', '--end', '920809200']
    >>> results = fetch(rrdfile, parameters, useBindings=True)

    >>> results[0]
    (920804400, 920809500, 300)
    >>> results[1]
    ('speed',)
    >>> len(results[2])
    17

    # For more info on the PyRRD data format, see the docstring for
    # pyrrd.external.fetch.
    >>> parameters = ['AVERAGE', '--start', '920804400', '--end', '920809200']
    >>> results = fetch(rrdfile, parameters, useBindings=False)
    >>> sorted(results["ds"].keys())
    ['speed']
    
    >>> os.unlink(rrdfile)
    >>> os.path.exists(rrdfile)
    False
    """
    if useBindings:
        parameters.insert(0, filename)
        return _cmd('fetch', parameters)
    else:
        return external.fetch(filename, external.concat(parameters))


def dump(filename, outfile='', parameters=[]):
    """
    The rrdtool Python bindings don't have support for dump, so we need to use
    the external dump function.

    >>> rrdfile = '/tmp/test.rrd'
    >>> parameters = [
    ...   '--start',
    ...   '920804400',
    ...   'DS:speed:COUNTER:600:U:U',
    ...   'RRA:AVERAGE:0.5:1:24',
    ...   'RRA:AVERAGE:0.5:6:10']
    >>> create(rrdfile, parameters)

    >>> xml = dump(rrdfile)
    >>> xmlBytes = len(xml)
    >>> 3300 < xmlBytes < 4000
    True
    >>> xmlCommentCheck = '<!-- Round Robin Database Dump'
    >>> xmlCommentCheck in xml[0:200]
    True

    >>> xmlfile = '/tmp/test.xml'
    >>> dump(rrdfile, xmlfile)

    >>> import os
    >>> os.path.exists(xmlfile)
    True

    >>> os.unlink(rrdfile)
    >>> os.unlink(xmlfile)
    """
    return external.dump(filename, outfile, parameters)


def load(filename):
    """
    The rrdtool Python bindings don't have support for load, so we need to use
    the external load function.

    >>> rrdfile = '/tmp/test.rrd'
    >>> parameters = [
    ...   '--start',
    ...   '920804400',
    ...   'DS:speed:COUNTER:600:U:U',
    ...   'RRA:AVERAGE:0.5:1:24',
    ...   'RRA:AVERAGE:0.5:6:10']
    >>> create(rrdfile, parameters)

    >>> tree = load(rrdfile)
    >>> [x.tag for x in tree]
    ['version', 'step', 'lastupdate', 'ds', 'rra', 'rra']
    """
    return external.load(filename)


def info(filename, obj=None, useBindings=False, rawData=False, stream=None):
    """
    Similarly to the fetch function, the info function uses
    pyrrd.backend.external by default. This is due to the fact that 1) the
    output of the RRD info module is much more easily legible, and 2) it is
    very similar in form to the output produced by the "rrdtool info" command.
    The output produced by the rrdtool Python bindings is a data structure and
    more difficult to view.

    However, if that output is what you desire, then simply set the useBindings
    parameter to True.
    """
    if useBindings:
        result = _cmd('info', [filename])
        if rawData:
            return result
        from pprint import pprint
        if stream:
            pprint(result, stream=stream)
        else:
            pprint(result)
    else:
        external.info(filename, obj)


def graph(filename, parameters):
    """
    >>> import tempfile
    >>>
    >>> rrdfile = '/tmp/test.rrd'
    >>> parameters = [
    ...   '--start',
    ...   '920804400',
    ...   'DS:speed:COUNTER:600:U:U',
    ...   'RRA:AVERAGE:0.5:1:24',
    ...   'RRA:AVERAGE:0.5:6:10']
    >>> create(rrdfile, parameters)

    >>> import os
    >>> os.path.exists(rrdfile)
    True

    >>> parameters = ['920804700:12345', '920805000:12357', '920805300:12363']
    >>> update(rrdfile, parameters)
    >>> parameters = ['920805600:12363', '920805900:12363','920806200:12373']
    >>> update(rrdfile, parameters)
    >>> parameters = ['920806500:12383', '920806800:12393','920807100:12399']
    >>> update(rrdfile, parameters)
    >>> parameters = ['920807400:12405', '920807700:12411', '920808000:12415']
    >>> update(rrdfile, parameters)
    >>> parameters = ['920808300:12420', '920808600:12422','920808900:12423']
    >>> update(rrdfile, parameters)

    >>> parameters = [
    ...   '--start',
    ...   '920804400', 
    ...   '--end', 
    ...   '920808000',
    ...   '--vertical-label',
    ...   'km/h',
    ...   'DEF:myspeed=%s:speed:AVERAGE' % rrdfile,
    ...   'CDEF:realspeed=myspeed,1000,*',
    ...   'CDEF:kmh=myspeed,3600,*',
    ...   'CDEF:fast=kmh,100,GT,kmh,0,IF',
    ...   'CDEF:good=kmh,100,GT,0,kmh,IF',
    ...   'HRULE:100#0000FF:"Maximum allowed"',
    ...   'AREA:good#00FF00:"Good speed"',
    ...   'AREA:fast#00FFFF:"Too fast"',
    ...   'LINE2:realspeed#FF0000:Unadjusted']
    >>> graphfile = tempfile.NamedTemporaryFile()
    >>> graph(graphfile.name, parameters)

    >>> os.path.exists(graphfile.name)
    True

    """
    parameters.insert(0, filename)
    output = _cmd('graph', parameters)


def prepareObject(function, obj):
    """
    This is a funtion that serves to make interacting with the
    backend as transparent as possible. It"s sole purpose it to
    prepare the attributes and data of the various pyrrd objects
    for use by the functions that call out to rrdtool.

    For all of the rrdtool-methods in this module, we need to split
    the named parameters up into pairs, assebled all the stuff in
    the list obj.data, etc.

    This function will get called by methods in the pyrrd wrapper
    objects. For instance, most of the methods of pyrrd.rrd.RRD
    will call this function. In graph, Pretty much only the method
    pyrrd.graph.Graph.write() will call this function.
    """
    if function == 'create':
        validParams = [
         'start', 'step']
        params = buildParameters(obj, validParams)
        params += [ unicode(x) for x in obj.ds ]
        params += [ unicode(x) for x in obj.rra ]
        return (
         obj.filename, params)
    if function == 'update':
        validParams = [
         'template']
        params = buildParameters(obj, validParams)
        FIRST_VALUE = 0
        DATA = 1
        TIME_OR_DATA = 0
        if obj.values[FIRST_VALUE][DATA]:
            params += [ '%s:%s' % (time, values) for (time, values) in obj.values ]
        else:
            params += [ data for (data, nil) in obj.values ]
        return (obj.filename, params)
    if function == 'fetch':
        validParams = [
         'resolution', 'start', 'end']
        params = buildParameters(obj, validParams)
        return (
         obj.filename, [obj.cf] + params)
    if function == 'info':
        return (obj.filename, obj)
    if function == 'graph':
        validParams = [
         'start', 'end', 'step', 'title',
         'vertical_label', 'width', 'height', 'only_graph',
         'upper_limit', 'lower_limit', 'rigid', 'alt_autoscale',
         'alt_autoscale_max', 'no_gridfit', 'x_grid', 'y_grid',
         'alt_y_grid', 'logarithmic', 'units_exponent', 'zoom',
         'font', 'font_render_mode', 'interlaced', 'no_legend',
         'force_rules_legend', 'tabwidth', 'base', 'color', 'imgformat',
         'slope_mode']
        params = buildParameters(obj, validParams)
        params += [ unicode(x) for x in obj.data ]
        return (
         obj.filename, params)


if __name__ == '__main__':
    import doctest
    doctest.testmod()