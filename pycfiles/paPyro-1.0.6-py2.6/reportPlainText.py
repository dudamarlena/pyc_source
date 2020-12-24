# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/papyro/reportPlainText.py
# Compiled at: 2011-07-18 08:31:39
from reportBase import ReportBase
import reports, cStringIO, os.path

class ReportPlainText(ReportBase):

    def __init__(self, report, conector):
        ReportBase.__init__(self, report, conector)
        self.ftext = cStringIO.StringIO()

    def writeReport(self, text_file=None, report_path=None, params=None, debug=False):
        self.debug = debug
        self.base_path = os.path.dirname(report_path or '.')
        self.param_names = [ param[0] for param in self.report.params.params ]
        if params != None:
            for p in params:
                if p[0] in self.param_names:
                    i = self.param_names.index(p[0])
                    self.report.params.params[i] = p

        self.cur_page = self.report.pages[0]
        self.writeReportTitle(self.report.title)
        for page in self.report.pages:
            self.cur_page = page
            self.writeReporPage(page)

        if text_file != None:
            f = file(text_file, 'w')
            try:
                self.ftext.seek(0)
                f.write(self.ftext.read())
            finally:
                f.close()

        self.ftext.seek(0)
        return self.ftext.read()

    def writeReportTitle(self, title):
        self.writeBody(title.body)

    def writeReporPage(self, page):
        if self.debug:
            print 'ReportPage:', unicode(page)
        self.writeBody(page.body)
        if page.page_footer != None:
            self.writePageFooter(page.page_footer)
        return

    def writeBody(self, body, mdata=None, ddata=None):
        if not self.check_condition(body.print_if, mdata, ddata):
            return
        for item in body.items:
            if isinstance(item, reports.Master):
                self.writeMaster(item)
            elif isinstance(item, reports.Detail):
                self.writeDetail(item, mdata)
            elif isinstance(item, reports.Text):
                self.writeText(item, mdata, ddata)
            elif isinstance(item, reports.TextFile):
                self.writeTextFile(item, mdata, ddata)
            elif isinstance(item, reports.Code):
                self.execute_code(item)

    def writeMaster(self, master):
        sql = master.table.query
        master_dict = {}
        for par in self.report.params.params:
            if sql.find(par[0]):
                master_dict[par[0]] = par[1]

        if self.debug:
            print 'master_dict =', master_dict
        if master_dict != {}:
            sql %= master_dict
        if self.debug:
            print sql
        values = [
         None] * len(master.group_headers)
        footers = []
        for gh in master.group_headers:
            footer = None
            for gf in master.group_footers:
                if gf.id == gh.footer_id:
                    footer = gf
                    break

            footers.append(footer)

        data = self.session.execute(sql)
        n = 0
        for mdata in data:
            for i in xrange(len(master.group_headers)):
                if mdata[master.group_headers[i].field] != values[i]:
                    self.writeBody(master.group_headers[i].header, mdata)
                    values[i] = mdata[master.group_headers[i].field]

            self.writeBody(master.body, mdata)
            for detalle in master.details:
                self.writeDetail(detalle, mdata)

            for i in xrange(len(master.group_headers) - 1, -1, -1):
                if len(data) > n + 1:
                    next_value = data[(n + 1)][master.group_headers[i].field]
                else:
                    next_value = None
                if next_value != values[i]:
                    if footers[i] != None:
                        self.writeBody(footers[i].footer, mdata)

            n += 1

        return

    def writeDetail(self, detail, mdata):
        detail_dict = {}
        detail_dict[detail.master_field] = mdata[detail.master_field]
        sql = detail.table.query
        for par in self.report.params.params:
            if sql.find(par[0]):
                detail_dict[par[0]] = par[1]

        sql %= detail_dict
        if self.debug:
            print sql
        data = self.session.execute(sql)
        if detail.header != None:
            if data.rowcount > 0:
                self.writeBody(detail.header.body, mdata)
            elif detail.header.print_if_detail_is_empty:
                self.writeBody(detail.header.body, mdata)
        for ddata in data:
            self.writeBody(detail.body, mdata, ddata)

        return

    def writePageHeader(self, page_header):
        self.writeBody(page_header.body)

    def writePageFooter(self, page_footer):
        pass

    def writeGroupHeader(self, group_header, y, data):
        field_value = None
        for mdata in data:
            if mdata[group_header.field] != field_value:
                self.writeBody(group_header.header, mdata)
                field_value = mdata[group_header.field]
            self.writeBody(group_header.body, mdata)

        return

    def writeGroupFooter(self, group_footer):
        pass

    def writeSubReport(self, subreport):
        if not self.check_condition(subreport.print_if):
            return
        f_xml = file(os.path.join(self.base_path, subreport.name) + '.xml', 'r')
        try:
            informe = reports.Report(xml=f_xml.read())
            parameters = []
            for subparam in subreport.params.params:
                if subparam[1] != '':
                    name = subparam[1]
                else:
                    name = subparam[0]
                i = self.param_names.index(name)
                param = self.report.params.params[i]
                parameters.append((subparam[0], param[1], param[2]))

            subinforme = ReportPlainText(informe, self.session)
            return subinforme.writeReport(params=parameters, debug=self.debug)
        finally:
            f_xml.close()

    def writeText(self, text, mdata=None, ddata=None):
        if not self.check_condition(text.print_if, mdata, ddata):
            return
        out = text.value
        out = self.apply_constants(out)
        out = self.apply_data(out, mdata)
        out = self.apply_data(out, ddata)
        out = self.apply_parameters(out)
        out = self.compile_text(out)
        for subreport in self.report.subreports:
            parameter = '#SUBREPORT %s#' % subreport.id
            out = out.replace(parameter, self.writeSubReport(subreport))

        if self.debug:
            print out
        self.ftext.write(out + '\n')

    def writeTextFile(self, textfile, mdata=None, ddata=None):
        if not self.check_condition(textfile.print_if, mdata, ddata):
            return
        ft = file(os.path.join(self.base_path, textfile.name), 'r')
        try:
            out = ft.read()
        finally:
            ft.close()

        out = self.apply_constants(out)
        out = self.apply_data(out, mdata)
        out = self.apply_data(out, ddata)
        out = self.apply_parameters(out)
        out = self.compile_text(out)
        for subreport in self.report.subreports:
            parameter = '#SUBREPORT %s#' % subreport.id
            out = out.replace(parameter, self.writeSubReport(subreport))

        if self.debug:
            print out
        self.ftext.write(out + '\n')