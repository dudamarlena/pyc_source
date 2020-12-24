# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/formats/simple_html.py
# Compiled at: 2019-11-14 13:57:46
from insights.formats import FormatterAdapter
from insights.formats.html import HtmlFormat

class SimpleHtmlFormat(HtmlFormat):
    """
    This class prints a html summary of rule hits. It should be used
    as a context manager and given an instance of an
    ``insights.core.dr.Broker``. ``dr.run`` should be called within the context
    using the same broker.

    Args:
        broker (Broker): the broker to watch and provide a summary about.
        stream (file-like): Output is written to stream. Defaults to sys.stdout.
    """
    TEMPLATE = ('\n<!doctype html>\n<html lang="en">\n  <head>\n    <!-- Required meta tags -->\n    <meta charset="utf-8">\n    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">\n\n    <title>{{root}}</title>\n    <style>\n    a.pass {\n      color: green;\n    }\n    a.fail {\n      color: red;\n    }\n    a.source {\n      color: orange;\n    }\n    .main {\n      margin-top: 100px;\n      margin-bottom: 100px;\n      margin-right: 150px;\n      margin-left: 80px;\n    }\n    </style>\n  </head>\n  <body>\n  <div class="main">\n  <h2 align="center">Analysis of {{root}}</h2>\n  <h4 align="center">Performed at {{start_time}} UTC</h4>\n    <section>\n      <h2>System Information</h2>\n        <pre>\n        {%- for rule in rules.make_info %}\n{{rule.body}}\n        {%- endfor %}\n        </pre>\n    </section>\n    <h2>Rule Results</h2>\n    <nav>\n      <ul>\n        {%- for response_type, rule_group in rules.items() %}\n        {%- if response_type != "make_info" %}\n        {%- for rule in rule_group %}\n        <ul>\n          <a id="{{rule.id}}_top"\n             class="{% if response_type !=\'make_pass\' %}fail{% else %}pass{% endif %}"\n             href="#{{rule.id}}">\n          {{rule.name}}\n          </a>\n        </ul>\n        {%- endfor %}\n        {%- endif %}\n        {%- endfor %}\n      </ul>\n    </nav>\n    <section>\n    <h2>Rule Result Details</h2>\n        {%- for response_type, rule_group in rules.items() %}\n        {%- if response_type != "make_info" %}\n        {%- for rule in rule_group %}\n        <article>\n          <header>\n          <a id="{{rule.id}}"\n             class="{% if response_type !=\'make_pass\' %}fail{% else %}pass{% endif %}"\n             href="#{{rule.id}}_top">\n          {{rule.name}}\n          </a>\n          </header>\n          <p>\n          <pre>\n{{rule.body}}\n          </pre>\n          </p>\n\n          <hr />\n          <p>\nContributing Data:\n          <ol>\n          {%- for d in rule.datasources %}\n          <li>{{d}}</li>\n          {%- endfor %}\n          </ol>\n          </p>\n\n          <hr />\n          Links:\n          <ul>\n          {% for cat, links in rule.links.items() %}\n            <li>{{cat}}\n            <ul>\n            {% for link in links %}\n            <li><a class="source" href="{{link}}">{{link}}</a></li>\n            {% endfor %}\n            </ul>\n            </li>\n          {%- endfor %}\n          </ul>\n\n          <hr />\n          <p> Rule Source: <a class="source" href="file://{{rule.source_path}}">{{rule.source_path}}</a></p>\n\n          <hr />\n          <div>\n          <p>\n          Documentation:\n          <div>\n          <pre>\n{{rule.mod_doc}}\n{{rule.rule_doc}}\n          </pre>\n          </div>\n          </p>\n          </div>\n          <hr />\n        </article>\n        {%- endfor %}\n        {%- endif %}\n        {%- endfor %}\n    </section>\n  </div>\n  </body>\n</html>\n    ').strip()


class SimpleHtmlFormatterAdapter(FormatterAdapter):
    """ Displays results in a simple html format. """

    def preprocess(self, broker):
        self.formatter = SimpleHtmlFormat(broker)
        self.formatter.preprocess()

    def postprocess(self, broker):
        self.formatter.postprocess()