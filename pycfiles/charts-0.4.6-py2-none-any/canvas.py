# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/redhat/cuemacro/chartpy/chartpy/canvas.py
# Compiled at: 2019-02-13 09:27:16
from __future__ import division
__author__ = 'saeedamen'
from chartpy.chart import Chart
try:
    import pdfkit
except:
    pass

class Canvas(object):

    def __init__(self, elements_to_render):
        self.elements_to_render = elements_to_render

    def generate_canvas(self, page_title='chartpy dashboard', jupyter_notebook=False, silent_display=True, output_filename=None, canvas_plotter='plain', render_pdf=False, return_html_binary=False, return_pdf_binary=False, extra_head_code=''):
        if canvas_plotter == 'plain':
            canvas_plotter = CanvasPlotterPlain()
        elif canvas_plotter == 'keen':
            canvas_plotter = CanvasPlotterKeen()
        return canvas_plotter.render_canvas(self.elements_to_render, page_title=page_title, jupyter_notebook=jupyter_notebook, silent_display=silent_display, output_filename=output_filename, render_pdf=render_pdf, return_html_binary=return_html_binary, return_pdf_binary=return_pdf_binary, extra_head_code=extra_head_code)


import abc
ABC = abc.ABCMeta('ABC', (object,), {'__slots__': ()})
import pandas

class CanvasPlotterTemplate(ABC):

    @abc.abstractmethod
    def render_canvas(self, elements_to_render, jupyter_notebook=False, silent_display=True, output_filename=None, canvas_plotter=None, page_title='chartpy dashboard', render_pdf=False, return_html_binary=False, return_pdf_binary=False):
        pass

    def output_page(self, html, jupyter_notebook, output_filename, silent_display, render_pdf, return_html_binary, return_pdf_binary):
        if output_filename is None:
            import datetime
            html_filename = str(datetime.datetime.now()).replace(':', '-').replace(' ', '-').replace('.', '-') + '-canvas.html'
        else:
            html_filename = output_filename
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html, 'html.parser')
        html = soup.prettify()
        if not return_html_binary:
            html_file = open(html_filename, 'w')
            html_file.write(html)
            html_file.close()
            if not silent_display:
                import webbrowser
                webbrowser.open(html_filename)
        if jupyter_notebook:
            from IPython.display import IFrame, display, HTML
            html = IFrame(html_filename, width=900, height=350, onload="this.style.height=this.contentDocument.body.scrollHeight +'px'")
            display(html)
        pdf_binary = None
        if render_pdf:
            pdf_filename = html_filename.replace('html', 'pdf')
            pdf_filename = pdf_filename.replace('htm', 'pdf')
            if return_pdf_binary:
                pdf_binary = pdfkit.from_string(html, False)
            else:
                pdfkit.from_string(html, pdf_filename)
        return (
         html, pdf_binary)


class CanvasPlotterPlain(CanvasPlotterTemplate):

    def render_canvas(self, elements_to_render, jupyter_notebook=False, silent_display=True, output_filename=None, page_title='chartpy dashboard', render_pdf=False, return_html_binary=False, return_pdf_binary=False, extra_head_code=''):
        html = []
        html.append('<head><title>' + page_title + '</title>')
        html.append(plain_css)
        html.append(extra_head_code)
        html.append('</head>')
        html.append('<h1>' + page_title + '</h1>')
        html.append('<table cellpadding="0">')
        if not isinstance(elements_to_render, list):
            elements_to_render = [
             elements_to_render]
        for i in range(0, len(elements_to_render)):
            row = elements_to_render[i]
            if not isinstance(row, list):
                row = [
                 row]
            if row != []:
                if row is not None:
                    html.append('<tr>\n')
                    for j in range(0, len(row)):
                        html.append('<td>')
                        object = row[j]
                        if isinstance(object, Chart):
                            chart = object
                            padding = 40
                            old_margin = chart.style.thin_margin
                            old_silent_display = chart.style.silent_display
                            chart.style.silent_display = True
                            chart.style.thin_margin = True
                            chart.plot()
                            chart.style.thin_margin = old_margin
                            chart.style.silent_display = old_silent_display
                            if chart.engine == 'matplotlib':
                                source_file = chart.style.file_output
                            else:
                                source_file = chart.style.html_file_output
                            try:
                                width = chart.style.width * abs(chart.style.scale_factor) + padding
                                height = chart.style.height * abs(chart.style.scale_factor) + padding
                                html.append('<iframe src="' + source_file + '" width="' + str(width) + '" height="' + str(height) + '" frameborder="0" scrolling="no"></iframe>')
                            except:
                                pass

                        elif isinstance(object, pandas.DataFrame):
                            old_width = pandas.get_option('display.max_colwidth')
                            pandas.set_option('display.max_colwidth', -1)
                            html_table = object.to_html(escape=False).replace('border="1"', 'border="0"')
                            html_table = html_table.replace('text-align: right;', 'text-align: center; vertical-align: text-top;')
                            html.append(html_table)
                            pandas.set_option('display.max_colwidth', old_width)
                        else:
                            html.append(object)
                        html.append('</td>\n')

                    html.append('</tr>\n')

        html.append('</table>\n')
        html = ('\n').join(html)
        return self.output_page(html, jupyter_notebook, output_filename, silent_display, render_pdf, return_html_binary, return_pdf_binary)


class CanvasPlotterKeen(CanvasPlotterTemplate):

    def render_canvas(self, elements_to_render, jupyter_notebook=False, silent_display=True, output_filename=None, page_title='chartpy dashboard', render_pdf=False, return_html_binary=False, return_pdf_binary=False, extra_head_code=''):
        html = []
        html.append('\n                <!DOCTYPE html>\n                <html>\n                <head>\n                  <title>')
        html.append(page_title)
        html.append('</title>\n                  <link rel="shortcut icon" href="logo.png" />\n                  <link rel="stylesheet" type="text/css" href="static/css/bootstrap.min.css" />\n                  <link rel="stylesheet" type="text/css" href="static/css/keen-dashboards.css" />\n                  <!-- For slider -->\n                  <link rel="stylesheet" type="text/css" href="static/css/iThing.css" />')
        html.append(extra_head_code)
        html.append('</head>\n                <body class="application">\n\n                <div class="navbar navbar-inverse navbar-fixed-top" role="navigation">\n                    <div class="container-fluid">\n                      <div class="navbar-header">\n                        <button type="button" class="navbar-toggle" data-toggle="collapse" data-target=".navbar-collapse">\n                          <span class="sr-only">Toggle navigation</span>\n                          <span class="icon-bar"></span>\n                          <span class="icon-bar"></span>\n                          <span class="icon-bar"></span>\n                        </button>\n                        <a class="navbar-brand">\n                          <!-- <img src="logo.png" alt="Smiley face" height="23" width="23"> -->\n                          <span class="glyphicon glyphicon-chevron-left"></span>\n                        </a>\n                        <a class="navbar-brand" href="http://www.cuemacro.com">chartpy dashboard </a>\n                      </div>\n                    </div>\n                </div>\n                ')
        html.append('<div class="container-fluid">')
        if not isinstance(elements_to_render, list):
            elements_to_render = [
             elements_to_render]
        for i in range(0, len(elements_to_render)):
            row = elements_to_render[i]
            if row != []:
                if row is not None:
                    if not isinstance(row, list):
                        row = [
                         row]
                    html.append('<div class="row">')
                    for j in range(0, len(row)):
                        object = row[j]
                        if isinstance(object, Chart):
                            chart = object
                            padding = 20
                            html.append('<div style="display:inline-block; width: ' + str(chart.style.width * abs(chart.style.scale_factor) + padding) + 'px">')
                            html.append('<div class="chart-wrapper">')
                            html.append('<div class="chart-title">' + chart.style.title + '</div>')
                            old_scale_factor = chart.style.scale_factor
                            old_silent_display = chart.style.silent_display
                            old_margin = chart.style.thin_margin
                            old_title = chart.style.title
                            old_source = chart.style.source
                            chart.style.silent_display = True
                            chart.style.title = None
                            chart.style.source = None
                            chart.style.thin_margin = True
                            if chart.engine == 'bokeh':
                                chart.style.scale_factor = 0.9 * chart.style.scale_factor
                            chart.plot()
                            chart.style.silent_display = old_silent_display
                            chart.style.scale_factor = old_scale_factor
                            chart.style.thin_margin = old_margin
                            chart.style.title = old_title
                            chart.style.source = old_source
                            if chart.engine == 'matplotlib':
                                if chart.style.file_output is None:
                                    import time
                                    chart.style.file_output = str(time.time()) + 'matplotlib.png'
                                source_file = chart.style.file_output
                            else:
                                source_file = chart.style.html_file_output
                            try:
                                html.append('<div style="display:inline-block; height: ' + str(chart.style.height * abs(chart.style.scale_factor) + padding) + 'px; vertical-align: center" class="chart-stage">')
                                html.append('<iframe src="' + source_file + '" width="' + str(chart.style.width * abs(chart.style.scale_factor) + padding) + '" height="' + str(chart.style.height * abs(chart.style.scale_factor) + padding) + '" frameborder="0" scrolling="no" align="middle"></iframe>')
                                html.append('</div>')
                                html.append('<div class="chart-notes">' + old_source + '</div>')
                            except:
                                pass

                            html.append('</div>')
                        elif isinstance(object, pandas.DataFrame):
                            html.append('<div style="display:inline-block;>')
                            html.append(object.to_html())
                            html.append('</div>')
                        else:
                            html.append('<div style="display:inline-block;>')
                            html.append(object)
                            html.append('</div>')
                        html.append('</div>')

                    html.append('</div>')

        html.append('</div>')
        html = ('\n').join(html)
        return self.output_page(html, jupyter_notebook, output_filename, silent_display, render_pdf, return_html_binary, return_pdf_binary)


plain_css = '\n<style>\na, a:focus, a:hover, a:active {\n  color: #00afd7;\n}\n\np, tr {\n  font-family: "Open Sans Light", "Raleway", "Helvetica Neue", Helvetica, Arial, sans-serif;\n}\n\nh1, h2, h3 {\n  font-family: "Open Sans Light", "Raleway", "Helvetica Neue", Helvetica, Arial, sans-serif;\n  margin: 12px 0;\n}\nh1 {\n  font-size: 32px;\n  font-weight: 100;\n  letter-spacing: .02em;\n  line-height: 48px;\n  margin: 12px 0;\n}\nh2 {\n  color: #2a333c;\n  font-weight: 200;\n  font-size: 21px;\n}\nh3 {\n  color: rgb(84, 102, 120);\n  font-size: 21px;\n  font-weight: 500;\n  letter-spacing: -0.28px;\n  line-height: 29.39px;\n}\n\n.btn {\n  background: transparent;\n  border: 1px solid white;\n}\n\n.keen-logo {\n  height: 38px;\n  margin: 0 15px 0 0;\n  width: 150px;\n}\n\n.navbar-toggle {\n  background-color: rgba(255,255,255,.25);\n}\n.navbar-toggle .icon-bar {\n  background: #fff;\n}\n\n\n.navbar-nav {\n  margin: 5px 0 0;\n}\n.navbar-nav > li > a {\n  font-size: 15px;\n  font-weight: 200;\n  letter-spacing: 0.03em;\n  padding-top: 19px;\n  text-shadow: 0 0 2px rgba(0,0,0,.1);\n}\n.navbar-nav > li > a:focus,\n.navbar-nav > li > a:hover {\n  background: transparent none;\n}\n\n.navbar-nav > li > a.navbar-btn {\n  background-color: rgba(255,255,255,.25);\n  border: medium none;\n  padding: 10px 15px;\n}\n.navbar-nav > li > a.navbar-btn:focus,\n.navbar-nav > li > a.navbar-btn:hover {\n  background-color: rgba(255,255,255,.35);\n}\n.navbar-collapse {\n  box-shadow: none;\n}\n\n.masthead {\n  background-color: #00afd7;\n  background-image: url("../img/bg-bars.png");\n  background-position: 0 -290px;\n  background-repeat: repeat-x;\n  color: #fff;\n  margin: 0 0 24px;\n  padding: 20px 0;\n}\n.masthead h1 {\n  margin: 0;\n}\n.masthead small,\n.masthead a,\n.masthead a:focus,\n.masthead a:hover,\n.masthead a:active {\n  color: #fff;\n}\n.masthead p {\n  color: #b3e7f3;\n  font-weight: 100;\n  letter-spacing: .05em;\n}\n\n.hero {\n  background-position: 50% 100%;\n  min-height: 450px;\n  text-align: center;\n}\n.hero h1 {\n  font-size: 48px;\n  margin: 120px 0 0;\n}\n.hero .lead {\n  margin-bottom: 32px;\n}\n.hero a.hero-btn {\n  border: 2px solid #fff;\n  display: block;\n  font-family: "Raleway", "Helvetica Neue", Helvetica, Arial, sans-serif;\n  font-size: 24px;\n  font-weight: 200;\n  margin: 0 auto 12px;\n  padding: 12px 0 6px;\n  width: 320px;\n}\n.hero a.hero-btn:focus,\n.hero a.hero-btn:hover {\n  border-color: transparent;\n  background-color: #fff;\n  color: #00afd7;\n}\n\n.sample-item {\n  margin-bottom: 24px;\n}\n\n.signup {\n  float: left;\n  display: inline-block;\n  vertical-align: middle;\n  margin-top: -6px;\n  margin-right: 10px;\n}\n\n.love {\n  border-top: 1px solid #d7d7d7;\n  color: #546678;\n  margin: 24px 0 0;\n  padding: 15px 0;\n  text-align: center;\n}\n\n.love p {\n  margin-bottom: 0;\n}\n\ntd {\n    text-align: center;\n    vertical-align: text-top;\n    font-size: 12px\n}\n\ntr {\n    text-align: center;\n    vertical-align: text-top;\n    font-size: 12px\n}\n\n</style>\n'