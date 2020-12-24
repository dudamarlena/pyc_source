# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\Projects\Github\PKBReportBuilder\PKBReportBuilder\models\export_models\export_document.py
# Compiled at: 2019-01-28 08:09:08
# Size of source mod 2**32: 10908 bytes
import logging, models.export_models.export_document_elements as export_document_models, models.tree_models.xml_navigator as xml_navigator, models.export_models.export_styles as styles

class ExportDocument:

    def __init__(self):
        try:
            self.export_elements = []
            self.xml_document_tables = []
            self.group_rows = []
        except Exception as e:
            logging.error('Error initialization. ' + str(e))

    def add_export_element(self, params):
        try:
            type = params[0]
            name = params[1]
            navigate_params = params[2]
            element = export_document_models.ExportDocumentElement(type, name)
            if type == 0:
                element.init_element_row(navigate_params)
            else:
                if type == 1:
                    element.init_element_table(navigate_params)
            self.export_elements.append(element)
        except Exception as e:
            logging.error('Error initialization. ' + str(e))

    def init_document_field_elements(self):
        try:
            params = [
             [
              0, 'MvdCriminalInvestigations',
              [
               xml_navigator.XmlNavigator([
                [
                 'Result', 'Root', 'PublicSources', 'MvdCriminalInvestigations']], 'title', [
                0], styles.row_title_style),
               xml_navigator.XmlNavigator([
                'Result', 'Root', 'PublicSources', 'MvdCriminalInvestigations', 'Status'], 'value', [
                0], styles.row_value_style)]],
             [
              0, 'MvdMissingInvestigations',
              [
               xml_navigator.XmlNavigator([
                [
                 'Result', 'Root', 'PublicSources', 'MvdMissingInvestigations']], 'title', [
                0], styles.row_title_style),
               xml_navigator.XmlNavigator([
                [
                 'Result', 'Root', 'PublicSources', 'MvdMissingInvestigations', 'Status']], 'value', [
                0], styles.row_value_style)]],
             [
              0, 'TerrorList',
              [
               xml_navigator.XmlNavigator([
                [
                 'Result', 'Root', 'PublicSources', 'TerrorList']], 'title', [
                0], styles.row_title_style),
               xml_navigator.XmlNavigator([
                [
                 'Result', 'Root', 'PublicSources', 'TerrorList', 'Status']], 'value', [
                0], styles.row_value_style)]],
             [
              0, 'Areears',
              [
               xml_navigator.XmlNavigator([
                [
                 'Result', 'Root', 'PublicSources', 'Areears']], 'title', [
                0], styles.row_title_style),
               xml_navigator.XmlNavigator([
                [
                 'Result', 'Root', 'PublicSources', 'Areears', 'Status']], 'value', [
                0], styles.row_value_style)]],
             [
              0, 'FalseBusi',
              [
               xml_navigator.XmlNavigator([
                [
                 'Result', 'Root', 'PublicSources', 'FalseBusi']], 'title', [
                0], styles.row_title_style),
               xml_navigator.XmlNavigator([
                [
                 'Result', 'Root', 'PublicSources', 'FalseBusi', 'Status']], 'value', [
                0], styles.row_value_style)]],
             [
              0, 'Bankruptcy',
              [
               xml_navigator.XmlNavigator([
                [
                 'Result', 'Root', 'PublicSources', 'Bankruptcy']], 'title', [
                0], styles.row_title_style),
               xml_navigator.XmlNavigator([
                [
                 'Result', 'Root', 'PublicSources', 'Bankruptcy', 'Status']], 'value', [
                0], styles.row_value_style)]],
             [
              0, 'RNUGosZakup',
              [
               xml_navigator.XmlNavigator([
                [
                 'Result', 'Root', 'PublicSources', 'RNUGosZakup']], 'title', [
                0], styles.row_title_style),
               xml_navigator.XmlNavigator([
                [
                 'Result', 'Root', 'PublicSources', 'RNUGosZakup', 'Status']], 'value', [
                0], styles.row_value_style)]],
             [
              0, 'QamqorList',
              [
               xml_navigator.XmlNavigator([
                [
                 'Result', 'Root', 'PublicSources', 'QamqorList']], 'title', [
                0], styles.row_title_style),
               xml_navigator.XmlNavigator([
                [
                 'Result', 'Root', 'PublicSources', 'QamqorList', 'Status']], 'value', [
                0], styles.row_value_style)]],
             [
              0, 'QamqorAlimony',
              [
               xml_navigator.XmlNavigator([
                [
                 'Result', 'Root', 'PublicSources', 'QamqorAlimony']], 'title', [
                0], styles.row_title_style),
               xml_navigator.XmlNavigator([
                [
                 'Result', 'Root', 'PublicSources', 'QamqorAlimony', 'Status']], 'value', [
                0], styles.row_value_style)]],
             [
              0, 'KgdWanted',
              [
               xml_navigator.XmlNavigator([
                [
                 'Result', 'Root', 'PublicSources', 'KgdWanted']], 'title', [
                0], styles.row_title_style),
               xml_navigator.XmlNavigator([
                [
                 'Result', 'Root', 'PublicSources', 'KgdWanted', 'Status']], 'value', [
                0], styles.row_value_style)]]]
            return params
        except Exception as e:
            logging.error('Error initialization. ' + str(e))

    def init_document_table_elements(self):
        try:
            params = [
             [
              1, 'ExistingContracts',
              [
               xml_navigator.XmlNavigator([
                [
                 'Result', 'Root', 'ExistingContracts', 'Contract']], 'title', [
                0], styles.row_title_style),
               xml_navigator.XmlNavigator([
                [
                 'Result', 'Root', 'PublicSources', 'KgdWanted', 'Status']], 'value', [
                0], styles.row_title_style)]]]
        except Exception as e:
            logging.error('Error initialization. ' + str(e))

    def init_document_elements(self):
        try:
            field_element_params = self.init_document_field_elements()
            for param in field_element_params:
                self.add_export_element(param)

        except Exception as e:
            logging.error('Error initialization. ' + str(e))