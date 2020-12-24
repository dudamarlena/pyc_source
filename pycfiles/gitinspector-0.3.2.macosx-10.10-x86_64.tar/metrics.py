# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/hugo/.virtualenvs/gitinspector/lib/python2.7/site-packages/gitinspector/metrics.py
# Compiled at: 2015-08-05 12:31:15
from __future__ import print_function
from __future__ import unicode_literals
from localization import N_
from outputable import Outputable
from changes import FileDiff
import comment, filtering, interval, re, subprocess
__metric_eloc__ = {b'java': 500, b'c': 500, b'cpp': 500, b'h': 300, b'hpp': 300, b'php': 500, b'py': 500, b'glsl': 1000, b'rb': 500, 
   b'js': 500, b'sql': 1000, b'xml': 1000}
__metric_cc_tokens__ = [
 [
  [
   b'java', b'js', b'c', b'cc', b'cpp'],
  [b'else', b'for\\s+\\(.*\\)', b'if\\s+\\(.*\\)', b'case\\s+\\w+:',
   b'default:', b'while\\s+\\(.*\\)'],
  [
   b'assert', b'break', b'continue', b'return']],
 [
  [
   b'py'], [b'^\\s+elif .*:$', b'^\\s+else:$', b'^\\s+for .*:', b'^\\s+if .*:$', b'^\\s+while .*:$'],
  [
   b'^\\s+assert', b'break', b'continue', b'return']]]
METRIC_CYCLOMATIC_COMPLEXITY_THRESHOLD = 50
METRIC_CYCLOMATIC_COMPLEXITY_DENSITY_THRESHOLD = 0.75

class MetricsLogic:

    def __init__(self):
        self.eloc = {}
        self.cyclomatic_complexity = {}
        self.cyclomatic_complexity_density = {}
        ls_tree_r = subprocess.Popen(b'git ls-tree --name-only -r ' + interval.get_ref(), shell=True, bufsize=1, stdout=subprocess.PIPE).stdout
        for i in ls_tree_r.readlines():
            i = i.strip().decode(b'unicode_escape', b'ignore')
            i = i.encode(b'latin-1', b'replace')
            i = i.decode(b'utf-8', b'replace').strip(b'"').strip(b"'").strip()
            if FileDiff.is_valid_extension(i) and not filtering.set_filtered(FileDiff.get_filename(i)):
                file_r = subprocess.Popen(b'git show ' + interval.get_ref() + (b':"{0}"').format(i.strip()), shell=True, bufsize=1, stdout=subprocess.PIPE).stdout.readlines()
                extension = FileDiff.get_extension(i)
                lines = MetricsLogic.get_eloc(file_r, extension)
                cycc = MetricsLogic.get_cyclomatic_complexity(file_r, extension)
                if __metric_eloc__.get(extension, None) != None and __metric_eloc__[extension] < lines:
                    self.eloc[i.strip()] = lines
                if METRIC_CYCLOMATIC_COMPLEXITY_THRESHOLD < cycc:
                    self.cyclomatic_complexity[i.strip()] = cycc
                if lines > 0 and METRIC_CYCLOMATIC_COMPLEXITY_DENSITY_THRESHOLD < cycc / float(lines):
                    self.cyclomatic_complexity_density[i.strip()] = cycc / float(lines)

        return

    @staticmethod
    def get_cyclomatic_complexity(file_r, extension):
        is_inside_comment = False
        cc_counter = 0
        entry_tokens = None
        exit_tokens = None
        for i in __metric_cc_tokens__:
            if extension in i[0]:
                entry_tokens = i[1]
                exit_tokens = i[2]

        if entry_tokens or exit_tokens:
            for i in file_r:
                i = i.decode(b'utf-8', b'replace')
                _, is_inside_comment = comment.handle_comment_block(is_inside_comment, extension, i)
                if not is_inside_comment and not comment.is_comment(extension, i):
                    for j in entry_tokens:
                        if re.search(j, i, re.DOTALL):
                            cc_counter += 2

                    for j in exit_tokens:
                        if re.search(j, i, re.DOTALL):
                            cc_counter += 1

            return cc_counter
        return -1

    @staticmethod
    def get_eloc(file_r, extension):
        is_inside_comment = False
        eloc_counter = 0
        for i in file_r:
            i = i.decode(b'utf-8', b'replace')
            _, is_inside_comment = comment.handle_comment_block(is_inside_comment, extension, i)
            if not is_inside_comment and not comment.is_comment(extension, i):
                eloc_counter += 1

        return eloc_counter


ELOC_INFO_TEXT = N_(b'The following files are suspiciously big (in order of severity)')
CYCLOMATIC_COMPLEXITY_TEXT = N_(b'The following files have an elevated cyclomatic complexity (in order of severity)')
CYCLOMATIC_COMPLEXITY_DENSITY_TEXT = N_(b'The following files have an elevated cyclomatic complexity density (in order of severity)')
METRICS_MISSING_INFO_TEXT = N_(b'No metrics violations were found in the repository')
METRICS_VIOLATION_SCORES = [
 [
  1.0, b'minimal'], [1.25, b'minor'], [1.5, b'medium'], [2.0, b'bad'], [3.0, b'severe']]

def __get_metrics_score__(ceiling, value):
    for i in reversed(METRICS_VIOLATION_SCORES):
        if value > ceiling * i[0]:
            return i[1]


class Metrics(Outputable):

    def output_text(self):
        metrics_logic = MetricsLogic()
        if not metrics_logic.eloc and not metrics_logic.cyclomatic_complexity and not metrics_logic.cyclomatic_complexity_density:
            print(b'\n' + _(METRICS_MISSING_INFO_TEXT) + b'.')
        if metrics_logic.eloc:
            print(b'\n' + _(ELOC_INFO_TEXT) + b':')
            for i in sorted(set([ (j, i) for i, j in metrics_logic.eloc.items() ]), reverse=True):
                print(_(b'{0} ({1} estimated lines of code)').format(i[1], str(i[0])))

        if metrics_logic.cyclomatic_complexity:
            print(b'\n' + _(CYCLOMATIC_COMPLEXITY_TEXT) + b':')
            for i in sorted(set([ (j, i) for i, j in metrics_logic.cyclomatic_complexity.items() ]), reverse=True):
                print(_(b'{0} ({1} in cyclomatic complexity)').format(i[1], str(i[0])))

        if metrics_logic.cyclomatic_complexity_density:
            print(b'\n' + _(CYCLOMATIC_COMPLEXITY_DENSITY_TEXT) + b':')
            for i in sorted(set([ (j, i) for i, j in metrics_logic.cyclomatic_complexity_density.items() ]), reverse=True):
                print(_(b'{0} ({1:.3f} in cyclomatic complexity density)').format(i[1], i[0]))

    def output_html(self):
        metrics_logic = MetricsLogic()
        metrics_xml = b'<div><div class="box" id="metrics">'
        if not metrics_logic.eloc and not metrics_logic.cyclomatic_complexity and not metrics_logic.cyclomatic_complexity_density:
            metrics_xml += b'<p>' + _(METRICS_MISSING_INFO_TEXT) + b'.</p>'
        if metrics_logic.eloc:
            metrics_xml += b'<div><h4>' + _(ELOC_INFO_TEXT) + b'.</h4>'
            for num, i in enumerate(sorted(set([ (j, i) for i, j in metrics_logic.eloc.items() ]), reverse=True)):
                metrics_xml += b'<div class="' + __get_metrics_score__(__metric_eloc__[FileDiff.get_extension(i[1])], i[0]) + (b' odd">' if num % 2 == 1 else b'">') + _(b'{0} ({1} estimated lines of code)').format(i[1], str(i[0])) + b'</div>'

            metrics_xml += b'</div>'
        if metrics_logic.cyclomatic_complexity:
            metrics_xml += b'<div><h4>' + _(CYCLOMATIC_COMPLEXITY_TEXT) + b'</h4>'
            for num, i in enumerate(sorted(set([ (j, i) for i, j in metrics_logic.cyclomatic_complexity.items() ]), reverse=True)):
                metrics_xml += b'<div class="' + __get_metrics_score__(METRIC_CYCLOMATIC_COMPLEXITY_THRESHOLD, i[0]) + (b' odd">' if num % 2 == 1 else b'">') + _(b'{0} ({1} in cyclomatic complexity)').format(i[1], str(i[0])) + b'</div>'

            metrics_xml += b'</div>'
        if metrics_logic.cyclomatic_complexity_density:
            metrics_xml += b'<div><h4>' + _(CYCLOMATIC_COMPLEXITY_DENSITY_TEXT) + b'</h4>'
            for num, i in enumerate(sorted(set([ (j, i) for i, j in metrics_logic.cyclomatic_complexity_density.items() ]), reverse=True)):
                metrics_xml += b'<div class="' + __get_metrics_score__(METRIC_CYCLOMATIC_COMPLEXITY_DENSITY_THRESHOLD, i[0]) + (b' odd">' if num % 2 == 1 else b'">') + _(b'{0} ({1:.3f} in cyclomatic complexity density)').format(i[1], i[0]) + b'</div>'

            metrics_xml += b'</div>'
        metrics_xml += b'</div></div>'
        print(metrics_xml)

    def output_xml(self):
        metrics_logic = MetricsLogic()
        if not metrics_logic.eloc and not metrics_logic.cyclomatic_complexity and not metrics_logic.cyclomatic_complexity_density:
            print(b'\t<metrics>\n\t\t<message>' + _(METRICS_MISSING_INFO_TEXT) + b'</message>\n\t</metrics>')
        else:
            eloc_xml = b''
            if metrics_logic.eloc:
                for i in sorted(set([ (j, i) for i, j in metrics_logic.eloc.items() ]), reverse=True):
                    eloc_xml += b'\t\t\t<estimated-lines-of-code>\n'
                    eloc_xml += b'\t\t\t\t<file-name>' + i[1] + b'</file-name>\n'
                    eloc_xml += b'\t\t\t\t<value>' + str(i[0]) + b'</value>\n'
                    eloc_xml += b'\t\t\t</estimated-lines-of-code>\n'

            if metrics_logic.cyclomatic_complexity:
                for i in sorted(set([ (j, i) for i, j in metrics_logic.cyclomatic_complexity.items() ]), reverse=True):
                    eloc_xml += b'\t\t\t<cyclomatic-complexity>\n'
                    eloc_xml += b'\t\t\t\t<file-name>' + i[1] + b'</file-name>\n'
                    eloc_xml += b'\t\t\t\t<value>' + str(i[0]) + b'</value>\n'
                    eloc_xml += b'\t\t\t</cyclomatic-complexity>\n'

            if metrics_logic.cyclomatic_complexity_density:
                for i in sorted(set([ (j, i) for i, j in metrics_logic.cyclomatic_complexity_density.items() ]), reverse=True):
                    eloc_xml += b'\t\t\t<cyclomatic-complexity-density>\n'
                    eloc_xml += b'\t\t\t\t<file-name>' + i[1] + b'</file-name>\n'
                    eloc_xml += (b'\t\t\t\t<value>{0:.3f}</value>\n').format(i[0])
                    eloc_xml += b'\t\t\t</cyclomatic-complexity-density>\n'

            print(b'\t<metrics>\n\t\t<violations>\n' + eloc_xml + b'\t\t</violations>\n\t</metrics>')