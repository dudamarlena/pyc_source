# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/_vendor/nvd3/ipynb.py
# Compiled at: 2019-09-11 02:44:38
# Size of source mod 2**32: 4491 bytes
__doc__ = '\nipython compatability module for nvd3-python\nThis adds simple ipython compatibility to the nvd3-python package, without making any\nmajor modifications to how the main package is structured.  It utilizes the IPython\ndisplay-formatter functionality, as described at:\nhttp://nbviewer.ipython.org/github/ipython/ipython/blob/master/examples/notebooks/Custom%20Display%20Logic.ipynb\nFor additional examples, see:\nhttps://github.com/sympy/sympy/blob/master/sympy/interactive/printing.py\n'
try:
    _ip = get_ipython()
except:
    _ip = None

if _ip:
    if _ip.__module__.lower().startswith('ipy'):
        _js_initialized = False

        def _print_html(chart):
            """Function to return the HTML code for the div container plus the javascript
        to generate the chart.  This function is bound to the ipython formatter so that
        charts are displayed inline."""
            global _js_initialized
            if not _js_initialized:
                print('js not initialized - pausing to allow time for it to load...')
                initialize_javascript()
                import time
                time.sleep(5)
            chart.buildhtml()
            return chart.htmlcontent


        def _setup_ipython_formatter(ip):
            """ Set up the ipython formatter to display HTML formatted output inline"""
            from IPython import __version__ as IPython_version
            from nvd3 import __all__ as nvd3_all
            if IPython_version >= '0.11':
                html_formatter = ip.display_formatter.formatters['text/html']
                for chart_type in nvd3_all:
                    html_formatter.for_type_by_name('nvd3.' + chart_type, chart_type, _print_html)


        def initialize_javascript(d3_js_url='https://cdnjs.cloudflare.com/ajax/libs/d3/3.5.5/d3.min.js', nvd3_js_url='https://cdnjs.cloudflare.com/ajax/libs/nvd3/1.7.0/nv.d3.min.js', nvd3_css_url='https://cdnjs.cloudflare.com/ajax/libs/nvd3/1.7.0/nv.d3.min.css', use_remote=False):
            """Initialize the ipython notebook to be able to display nvd3 results.
        by instructing IPython to load the nvd3 JS and css files, and the d3 JS file.

        by default, it looks for the files in your IPython Notebook working directory.

        Takes the following options:

        use_remote: use remote hosts for d3.js, nvd3.js, and nv.d3.css (default False)
        * Note:  the following options are ignored if use_remote is False:
        nvd3_css_url: location of nvd3 css file (default https://cdnjs.cloudflare.com/ajax/libs/nvd3/1.7.0/nv.d3.min.css)
        nvd3_js_url: location of nvd3 javascript file (default  https://cdnjs.cloudflare.com/ajax/libs/nvd3/1.7.0/nv.d3.min.css)
        d3_js_url: location of d3 javascript file (default https://cdnjs.cloudflare.com/ajax/libs/d3/3.5.5/d3.min.js)
        """
            global _js_initialized
            from IPython.display import display, Javascript, HTML
            if not use_remote:
                d3_js_url = 'files/d3.v3.js'
                nvd3_js_url = 'files/nv.d3.js'
                nvd3_css_url = 'files/nv.d3.css'
            display(HTML('<link media="all" href="%s" type="text/css"\n                        rel="stylesheet"/>' % nvd3_css_url))
            display(Javascript('$.getScript("%s")' % nvd3_js_url))
            display(Javascript('$.getScript("%s", function() {\n                              $.getScript("%s", function() {})});' % (d3_js_url, nvd3_js_url)))
            display(HTML('<script src="%s"></script>' % d3_js_url))
            display(HTML('<script src="%s"></script>' % nvd3_js_url))
            _js_initialized = True


        print('loaded nvd3 IPython extension\nrun nvd3.ipynb.initialize_javascript() to set up the notebook\nhelp(nvd3.ipynb.initialize_javascript) for options')
        _setup_ipython_formatter(_ip)