# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/formats/html.py
# Compiled at: 2019-11-14 13:57:46
from __future__ import print_function
from collections import OrderedDict
from itertools import groupby
from operator import itemgetter
from insights import make_info, make_fail, make_response, make_pass
from insights.formats import FormatterAdapter
from insights.formats.template import TemplateFormat

class HtmlFormat(TemplateFormat):
    """
    This class prints a html summary of rule hits. It should be used
    as a context manager and given an instance of an
    ``insights.core.dr.Broker``. ``dr.run`` should be called within the context
    using the same broker.

    Args:
        broker (Broker): the broker to watch and provide a summary about.
        stream (file-like): Output is written to stream. Defaults to sys.stdout.
    """
    TEMPLATE = ('\n<!doctype html>\n<html lang="en">\n  <head>\n    <!-- Required meta tags -->\n    <meta charset="utf-8">\n    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">\n\n    <!-- Bootstrap CSS -->\n    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css" integrity="sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO" crossorigin="anonymous">\n\n    <title>{{root}}</title>\n  </head>\n  <body>\n    <div class="container">\n      <p>\n        <h2>Analysis of {{root}}</h2>\n        <h4>Performed at {{start_time}} UTC</h4>\n      </p>\n      <div class="card">\n        <div class="card-header">System Information</div>\n        <div class="card-body">\n        <pre>\n{% for rule in rules.make_info %}\n{{-rule.body}}\n{% endfor -%}\n        </pre>\n        </div>\n      </div>\n      <div class="card">\n        <div class="card-header">Rule Results</div>\n        <div class="card-body">\n          <div class="accordion" id="ruleAccordion">\n          {%- for group, results in rules.items() %}\n          {%- if group != "make_info" %}\n          {%- for rule in results %}\n            <div class="card">\n              <div class="card-header bg-{% if group == "make_pass" %}success{% else %}danger{% endif %}" id="heading_{{rule.id}}">\n                <h2 class="mb-0">\n                  <button class="btn btn-{% if group == "make_pass" %}success{% else %}danger{% endif %} text-white" type="button" data-toggle="collapse" data-target="#{{rule.id}}" aria-expanded="true" aria-controls="{{rule.id}}">\n                  {{rule.name}}\n                  </button>\n                </h2>\n              </div>\n              <div id="{{rule.id}}" class="collapse" aria-labelledby="heading_{{rule.id}}" data-parent="#ruleAccordion">\n                <div class="card-body">\n                <pre>\n{{rule.body}}\n                </pre>\n                <hr />\n                Contributing data:\n                <ol>\n                {% for d in rule.datasources %}\n                  <li>\n                  {{d}}\n                  </li>\n                {%- endfor %}\n                </ol>\n                <hr />\n                Links:\n                <ul>\n                {% for cat, links in rule.links.items() %}\n                  <li>{{cat}}\n                  <ul>\n                  {% for link in links %}\n                  <li><a href="{{link}}">{{link}}</a></li>\n                  {% endfor %}\n                  </ul>\n                  </li>\n                {%- endfor %}\n                </ul>\n                <hr />\n                Rule source: {{rule.source_path}}\n                <hr />\n          Documentation:\n                <pre>\n{{rule.mod_doc}}\n{{rule.rule_doc}}\n                </pre>\n                </div>\n              </div>\n            </div>\n          {%- endfor %}\n          {% endif %}\n          {% endfor %}\n          </div>\n        </div>\n      </div>\n    </div>\n    <!-- Optional JavaScript -->\n    <!-- jQuery first, then Popper.js, then Bootstrap JS -->\n    <script\n        src="http://code.jquery.com/jquery-3.4.1.slim.min.js"\n        integrity="sha256-pasqAKBDmFT4eHoN2ndd6lN370kFiGUFyTiUHWhU7k8="\n        crossorigin="anonymous"></script>\n    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.3/umd/popper.min.js" integrity="sha384-ZMP7rVo3mIykV+2+9J3UJ46jBk0WLaUAdn689aCwoqbBJiSnjAK/l8WvCWPIPm49" crossorigin="anonymous"></script>\n    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/js/bootstrap.min.js" integrity="sha384-ChfqqxuZUCnJSK3+MXmPNIyE6ZbWh2IMqE241rYiqJxyMiZ6OW/JmZQ5stwEULTy" crossorigin="anonymous"></script>\n  </body>\n</html>\n    ').strip()

    def create_template_context(self):
        ctx = {'root': self.find_root() or 'Unknown', 
           'start_time': self.start_time}
        sorted_rules = {}
        response_type_getter = itemgetter('response_type')
        self.rules = sorted(self.rules, key=response_type_getter)
        for response_type, rules in groupby(self.rules, response_type_getter):
            rules = sorted(rules, key=itemgetter('name'))
            sorted_rules[response_type] = rules

        ctx['rules'] = OrderedDict()
        for key in (make_info, make_fail, make_response, make_pass):
            name = key.__name__
            if name in sorted_rules:
                ctx['rules'][name] = sorted_rules[name]

        return ctx


class HtmlFormatterAdapter(FormatterAdapter):
    """ Displays results in html format. """

    def preprocess(self, broker):
        self.formatter = HtmlFormat(broker)
        self.formatter.preprocess()

    def postprocess(self, broker):
        self.formatter.postprocess()