# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\eatlint\lint.py
# Compiled at: 2009-04-02 14:22:50
__docformat__ = 'restructuredtext en'
from trac.core import *
from trac.web.chrome import Chrome
from trac.web.clearsilver import HDFWrapper
from bitten.api import IReportChartGenerator, IReportSummarizer
from trac.web.chrome import ITemplateProvider
import pkg_resources

class PyLintChartGenerator(Component):
    implements(IReportChartGenerator)

    def get_supported_categories(self):
        return [
         'lint']

    def generate_chart_data(self, req, config, category):
        assert category == 'lint'
        db = self.env.get_db_cnx()
        cursor = db.cursor()
        query = "\nselect build.rev, \n (select count(*) from bitten_report_item as item\n  where item.report = report.id and item.name='category' and item.value='convention'),\n (select count(*) from bitten_report_item as item\n  where item.report = report.id and item.name='category' and item.value='error'),\n (select count(*) from bitten_report_item as item\n  where item.report = report.id and item.name='category' and item.value='refactor'),\n (select count(*) from bitten_report_item as item\n  where item.report = report.id and item.name='category' and item.value='warning')\nfrom bitten_report as report\n left outer join bitten_build as build ON (report.build=build.id)\nwhere build.config='%s' and report.category='lint'\ngroup by build.rev_time, build.rev, build.platform\norder by build.rev_time;" % (config.name,)
        cursor.execute(query)
        lint = []
        prev_rev = None
        for (rev, conv, err, ref, warn) in cursor:
            if rev != prev_rev:
                total = conv + err + ref + warn
                lint.append([rev, total, conv, err, ref, warn])
            prev_rev = rev

        req.hdf['chart.title'] = 'Lint Problems by Type'
        req.hdf['chart.data'] = [
         [
          'Revision'] + [ '[%s]' % item[0] for item in lint ],
         [
          'Total Problems'] + [ item[1] for item in lint ],
         [
          'Convention'] + [ item[2] for item in lint ],
         [
          'Error'] + [ item[3] for item in lint ],
         [
          'Refactor'] + [ item[4] for item in lint ],
         [
          'Warning'] + [ item[5] for item in lint ]]
        return 'bitten_chart_lint.cs'


class PyLintSummarizer(Component):
    implements(IReportSummarizer)

    def get_supported_categories(self):
        return [
         'lint']

    def render_summary(self, req, config, build, step, category):
        assert category == 'lint'
        db = self.env.get_db_cnx()
        cursor = db.cursor()
        cursor.execute("\nSELECT item_type.value AS type, item_file.value AS file,\n    item_line.value as line, item_category.value as category,\n    report.category as report_category\nFROM bitten_report AS report\n LEFT OUTER JOIN bitten_report_item AS item_type\n  ON (item_type.report=report.id AND item_type.name='type')\n LEFT OUTER JOIN bitten_report_item AS item_file\n  ON (item_file.report=report.id AND\n    item_file.item=item_type.item AND\n    item_file.name='file')\n LEFT OUTER JOIN bitten_report_item AS item_line\n  ON (item_line.report=report.id AND\n    item_line.item=item_type.item AND\n    item_line.name='lines')\n LEFT OUTER JOIN bitten_report_item AS item_category\n  ON (item_category.report=report.id AND\n    item_category.item=item_type.item AND\n    item_category.name='category')\nWHERE report.category='lint' AND build=%s AND step=%s\nORDER BY item_type.value", (build.id, step.name))
        file_data = {}
        type_total = {}
        category_total = {}
        line_total = 0
        file_total = 0
        seen_files = {}
        for (type, file, line, category, report_category) in cursor:
            if not file_data.has_key(file):
                file_data[file] = {'file': file, 'type': {}, 'lines': 0, 'category': {}}
            d = file_data[file]
            if not d['type'].has_key(type):
                d['type'][type] = 0
            d['type'][type] += 1
            d['lines'] += 1
            line_total += 1
            if not d['category'].has_key(category):
                d['category'][category] = 0
            d['category'][category] += 1
            if file:
                d['href'] = req.href.browser(config.path, file)
            if not type_total.has_key(type):
                type_total[type] = 0
            type_total[type] += 1
            if not category_total.has_key(category):
                category_total[category] = 0
            category_total[category] += 1
            if not seen_files.has_key(file):
                seen_files[file] = 0
                file_total += 1

        data = []
        for d in file_data.values():
            d['catnames'] = d['category'].keys()
            data.append(d)

        hdf = HDFWrapper(loadpaths=Chrome(self.env).get_all_templates_dirs())
        hdf['data'] = data
        hdf['totals'] = {'type': type_total, 'category': category_total, 'files': file_total, 'lines': line_total}
        return hdf.render('bitten_summary_lint.cs')


class EatLintChrome(Component):
    implements(ITemplateProvider)

    def get_htdocs_dirs(self):
        """Return the directories containing static resources."""
        return [
         (
          'eatlint', pkg_resources.resource_filename(__name__, 'htdocs'))]

    def get_templates_dirs(self):
        """Return the directories containing templates."""
        return [
         pkg_resources.resource_filename(__name__, 'templates')]