# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/formats/_yaml.py
# Compiled at: 2019-05-16 13:41:33
import yaml
from insights.core.evaluators import SingleEvaluator
from insights.formats import EvaluatorFormatterAdapter
from yaml.representer import Representer
from insights.core import ScanMeta
Representer.add_representer(ScanMeta, Representer.represent_name)

class YamlFormat(SingleEvaluator):

    def postprocess(self):
        yaml.dump(self.get_response(), self.stream)


class YamlFormatterAdapter(EvaluatorFormatterAdapter):
    Impl = YamlFormat