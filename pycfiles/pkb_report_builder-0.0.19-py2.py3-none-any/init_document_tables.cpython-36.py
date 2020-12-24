# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\Projects\Github\PKBReportBuilder\PKBReportBuilder\modules\table_processing\init_document_tables.py
# Compiled at: 2019-02-04 09:37:03
# Size of source mod 2**32: 54404 bytes
import models.processing_tables.processing_table_models as processing_table_models, logging

def init_existing_contracts_table(root):
    try:
        table_path = [
         'Result', 'Root', 'ExistingContracts', 'Contract']
        table = processing_table_models.ProcessingTable('Действующие договора', root, table_path, hidden_columns_in_groups=[
         'Name', 'SubjectRole',
         'FinancialInstitution'])
        table.init_column('Наименование Заемщика/гаранта/созаемщика', 'Name', [
         [
          [
           'Result', 'Root', 'Header', 'Surname'],
          [
           'Result', 'Root', 'Header', 'Name'],
          [
           'Result', 'Root', 'Header', 'FathersName']],
         [
          [
           'Result', 'Root', 'Header', 'NameNative']]], 'value', processing_table_models.ConditionValue(None, None, None, 'value', None, processing_table_models.ConvertTypesCollection(0), None, None, None, False), processing_table_models.ExtractValueTypesCollection(1), True)
        table.init_column('Роль субъекта', 'SubjectRole', [
         [
          [
           'SubjectRole']]], 'value', processing_table_models.ConditionValue(None, None, None, 'value', None, processing_table_models.ConvertTypesCollection(0), None, None, None, True), processing_table_models.ExtractValueTypesCollection(2), False)
        table.init_column('Наименование Банка', 'FinancialInstitution', [
         [
          [
           'FinancialInstitution']]], 'value', processing_table_models.ConditionValue(None, None, None, 'value', None, processing_table_models.ConvertTypesCollection(0), None, None, None, False), processing_table_models.ExtractValueTypesCollection(2), False)
        table.init_column('Тип КЛ', 'TypeOfFoundingn', [
         [
          [
           'TypeOfFounding']]], 'value', processing_table_models.ConditionValue(None, None, None, 'value', None, processing_table_models.ConvertTypesCollection(0), None, None, None, False), processing_table_models.ExtractValueTypesCollection(2), False)
        table.init_column('Номер договора', 'AgreementNumber', [
         [
          [
           'AgreementNumber']]], 'value', processing_table_models.ConditionValue(None, None, None, 'value', None, processing_table_models.ConvertTypesCollection(0), None, None, None, False), processing_table_models.ExtractValueTypesCollection(2), False)
        table.init_column('Лимит/ Общая сумма кредита (тыс. тенге)', 'TotalAmount', [
         [
          [
           'TotalAmount']]], 'value', processing_table_models.ConditionValue(None, None, None, 'value', None, processing_table_models.ConvertTypesCollection(1), None, None, [
         processing_table_models.OutputValueTypesCollection(1),
         processing_table_models.OutputValueTypesCollection(3),
         processing_table_models.OutputValueTypesCollection(4)], False), processing_table_models.ExtractValueTypesCollection(2), False)
        table.init_column('Наименование Заемщика/гаранта/ созаемщика (тыс. тенге)', 'OutstandingAmount', [
         [
          [
           'OutstandingAmount']]], 'value', processing_table_models.ConditionValue(None, None, None, 'value', None, processing_table_models.ConvertTypesCollection(1), None, None, [
         processing_table_models.OutputValueTypesCollection(1),
         processing_table_models.OutputValueTypesCollection(3),
         processing_table_models.OutputValueTypesCollection(4)], False), processing_table_models.ExtractValueTypesCollection(2), False)
        table.init_column('Сумма ежемесячного платежа, тыс. тенге', 'MonthlyInstalmentAmount', [
         [
          [
           'MonthlyInstalmentAmount']]], 'value', processing_table_models.ConditionValue(None, None, None, 'value', None, processing_table_models.ConvertTypesCollection(1), None, None, [
         processing_table_models.OutputValueTypesCollection(1),
         processing_table_models.OutputValueTypesCollection(3),
         processing_table_models.OutputValueTypesCollection(4)], False), processing_table_models.ExtractValueTypesCollection(0), False)
        table.init_column('Дата открытия кредитной линии, ДД.ММ.ГГГГ', 'DateOfCreditStart', [
         [
          [
           'DateOfCreditStart']]], 'value', processing_table_models.ConditionValue(None, None, None, 'value', None, processing_table_models.ConvertTypesCollection(1), None, None, [
         processing_table_models.OutputValueTypesCollection(2)], False), processing_table_models.ExtractValueTypesCollection(0), False)
        table.init_column('Дата закрытия кредитной линии, ДД.ММ.ГГГГ', 'DateOfCreditEnd', [
         [
          [
           'DateOfCreditEnd']]], 'value', processing_table_models.ConditionValue(None, None, None, 'value', None, processing_table_models.ConvertTypesCollection(1), None, None, [
         processing_table_models.OutputValueTypesCollection(2)], False), processing_table_models.ExtractValueTypesCollection(0), False)
        table.init_column('Период доступности ДД.ММ.ГГГГ', 'AvailableDate', [
         [
          [
           'AvailableDate']]], 'value', processing_table_models.ConditionValue(None, None, None, 'value', None, processing_table_models.ConvertTypesCollection(1), None, None, [
         processing_table_models.OutputValueTypesCollection(2)], False), processing_table_models.ExtractValueTypesCollection(0), False)
        table.init_column('Ставка вознаграждения (при наличии информации) ', 'NominalRate', [
         [
          [
           'NominalRate']]], 'value', processing_table_models.ConditionValue(None, None, None, 'value', None, processing_table_models.ConvertTypesCollection(1), None, None, [
         processing_table_models.OutputValueTypesCollection(1)], False), processing_table_models.ExtractValueTypesCollection(0), False)
        table.init_column('Цель', 'CreditObject/PurposeOfCredit', [
         [
          [
           'CreditObject'],
          [
           'PurposeOfCredit']]], 'value', processing_table_models.ConditionValue(None, None, None, 'value', None, processing_table_models.ConvertTypesCollection(0), None, None, None, True), processing_table_models.ExtractValueTypesCollection(2), False)
        table.init_column('Продолжительность просрочки, дней', 'OverdueAmountMaxCount', [
         [
          [
           'OverdueAmountMaxCount']]], 'value', processing_table_models.ConditionValue(None, None, None, 'value', None, processing_table_models.ConvertTypesCollection(1), None, None, [
         processing_table_models.OutputValueTypesCollection(1)], False), processing_table_models.ExtractValueTypesCollection(2), False)
        table.init_column('Максимальная длина одной просрочки (max)', 'NumberOfOverdueInstalmentsMax', [
         [
          [
           'NumberOfOverdueInstalmentsMax']]], 'value', processing_table_models.ConditionValue(None, None, None, 'value', None, processing_table_models.ConvertTypesCollection(1), None, None, [
         processing_table_models.OutputValueTypesCollection(1)], False), processing_table_models.ExtractValueTypesCollection(2), False)
        table.init_column('Наличие текущей просрочки, в днях', 'NumberOfOverdueInstalments', [
         [
          [
           'NumberOfOverdueInstalments']]], 'value', processing_table_models.ConditionValue(None, None, None, 'value', None, processing_table_models.ConvertTypesCollection(1), None, None, [
         processing_table_models.OutputValueTypesCollection(1)], False), processing_table_models.ExtractValueTypesCollection(2), False)
        table.init_column('Просроченная сумма, тыс. Тенге (макс.)', 'NumberOfOverdueInstalmentsMaxAmount', [
         [
          [
           'NumberOfOverdueInstalmentsMaxAmount']]], 'value', processing_table_models.ConditionValue(None, None, None, 'value', None, processing_table_models.ConvertTypesCollection(1), None, None, [
         processing_table_models.OutputValueTypesCollection(1),
         processing_table_models.OutputValueTypesCollection(3),
         processing_table_models.OutputValueTypesCollection(4)], False), processing_table_models.ExtractValueTypesCollection(2), False)
        table.init_column('Количество месяцев, в которых была зафиксирована просрочка', 'MonthCountInstalments', [
         [
          [
           '-']]], 'value', processing_table_models.ConditionValue(None, None, None, 'value', None, processing_table_models.ConvertTypesCollection(1), None, None, [
         processing_table_models.OutputValueTypesCollection(1),
         processing_table_models.OutputValueTypesCollection(3),
         processing_table_models.OutputValueTypesCollection(4)], False), processing_table_models.ExtractValueTypesCollection(2), False)
        table.init_column('Количество просрочек более 30 дней', 'CountInstalmentsIn30Days', [
         [
          [
           '-']]], 'value', processing_table_models.ConditionValue(None, None, None, 'value', None, processing_table_models.ConvertTypesCollection(1), None, None, [
         processing_table_models.OutputValueTypesCollection(1),
         processing_table_models.OutputValueTypesCollection(3),
         processing_table_models.OutputValueTypesCollection(4)], False), processing_table_models.ExtractValueTypesCollection(2), False)
        table.init_column('Гаранты/созаемщики', 'Garants', [
         [
          [
           '-']]], 'value', processing_table_models.ConditionValue(None, None, None, 'value', None, processing_table_models.ConvertTypesCollection(0), None, None, None, False), processing_table_models.ExtractValueTypesCollection(2), False)
        table.init_column('Вид обеспечения', 'TypeOfGuarantee', [
         [
          [
           'Collateral', 'TypeOfGuarantee']]], 'value', processing_table_models.ConditionValue(None, None, None, 'value', None, processing_table_models.ConvertTypesCollection(0), None, None, None, False), processing_table_models.ExtractValueTypesCollection(2), False)
        table.init_column('Стоимость обеспечения тыс. тенге', 'ValueOfGuarantee', [
         [
          [
           'Collateral', 'ValueOfGuarantee']]], 'value', processing_table_models.ConditionValue(None, None, None, 'value', None, processing_table_models.ConvertTypesCollection(1), None, None, [
         processing_table_models.OutputValueTypesCollection(1),
         processing_table_models.OutputValueTypesCollection(3),
         processing_table_models.OutputValueTypesCollection(4)], False), processing_table_models.ExtractValueTypesCollection(2), False)
        return table
    except Exception as e:
        pass


def init_terminated_contracts_table(root):
    try:
        table_path = ['Result', 'Root', 'TerminatedContracts', 'Contract']
        table = processing_table_models.ProcessingTable('Завершенные договора', root, table_path, hidden_columns_in_groups=[
         'Name', 'SubjectRole',
         'FinancialInstitution'])
        table.init_column('Наименование Заемщика/гаранта/созаемщика', 'Name', [
         [
          [
           'Result', 'Root', 'Header', 'Surname'],
          [
           'Result', 'Root', 'Header', 'Name'],
          [
           'Result', 'Root', 'Header', 'FathersName']],
         [
          [
           'Result', 'Root', 'Header', 'NameNative']]], 'value', processing_table_models.ConditionValue(None, None, None, 'value', None, processing_table_models.ConvertTypesCollection(0), None, None, None, False), processing_table_models.ExtractValueTypesCollection(1), True)
        table.init_column('Роль субъекта', 'SubjectRole', [
         [
          [
           'SubjectRole']]], 'value', processing_table_models.ConditionValue(None, None, None, 'value', None, processing_table_models.ConvertTypesCollection(0), None, None, None, True), processing_table_models.ExtractValueTypesCollection(2), False)
        table.init_column('Наименование Банка', 'FinancialInstitution', [
         [
          [
           'FinancialInstitution']]], 'value', processing_table_models.ConditionValue(None, None, None, 'value', None, processing_table_models.ConvertTypesCollection(0), None, None, None, False), processing_table_models.ExtractValueTypesCollection(2), False)
        table.init_column('Тип КЛ', 'TypeOfFoundingn', [
         [
          [
           'TypeOfFounding']]], 'value', processing_table_models.ConditionValue(None, None, None, 'value', None, processing_table_models.ConvertTypesCollection(0), None, None, None, False), processing_table_models.ExtractValueTypesCollection(2), False)
        table.init_column('Номер договора', 'AgreementNumber', [
         [
          [
           'AgreementNumber']]], 'value', processing_table_models.ConditionValue(None, None, None, 'value', None, processing_table_models.ConvertTypesCollection(0), None, None, None, False), processing_table_models.ExtractValueTypesCollection(2), False)
        table.init_column('Лимит/ Общая сумма кредита (тыс. тенге)', 'TotalAmount', [
         [
          [
           'TotalAmount']]], 'value', processing_table_models.ConditionValue(None, None, None, 'value', None, processing_table_models.ConvertTypesCollection(1), None, None, [
         processing_table_models.OutputValueTypesCollection(1),
         processing_table_models.OutputValueTypesCollection(3),
         processing_table_models.OutputValueTypesCollection(4)], False), processing_table_models.ExtractValueTypesCollection(2), False)
        table.init_column('Дата открытия кредитной линии, ДД.ММ.ГГГГ', 'DateOfCreditStart', [
         [
          [
           'DateOfCreditStart']]], 'value', processing_table_models.ConditionValue(None, None, None, 'value', None, processing_table_models.ConvertTypesCollection(1), None, None, [
         processing_table_models.OutputValueTypesCollection(2)], False), processing_table_models.ExtractValueTypesCollection(0), False)
        table.init_column('Дата закрытия кредитной линии, ДД.ММ.ГГГГ', 'DateOfCreditEnd', [
         [
          [
           'DateOfCreditEnd']]], 'value', processing_table_models.ConditionValue(None, None, None, 'value', None, processing_table_models.ConvertTypesCollection(1), None, None, [
         processing_table_models.OutputValueTypesCollection(2)], False), processing_table_models.ExtractValueTypesCollection(0), False)
        table.init_column('Период доступности ДД.ММ.ГГГГ', 'AvailableDate', [
         [
          [
           'AvailableDate']]], 'value', processing_table_models.ConditionValue(None, None, None, 'value', None, processing_table_models.ConvertTypesCollection(1), None, None, [
         processing_table_models.OutputValueTypesCollection(2)], False), processing_table_models.ExtractValueTypesCollection(0), False)
        table.init_column('Ставка вознаграждения (при наличии информации) ', 'NominalRate', [
         [
          [
           'NominalRate']]], 'value', processing_table_models.ConditionValue(None, None, None, 'value', None, processing_table_models.ConvertTypesCollection(1), None, None, [
         processing_table_models.OutputValueTypesCollection(1)], False), processing_table_models.ExtractValueTypesCollection(0), False)
        table.init_column('Цель', 'CreditObject/PurposeOfCredit', [
         [
          [
           'CreditObject'],
          [
           'PurposeOfCredit']]], 'value', processing_table_models.ConditionValue(None, None, None, 'value', None, processing_table_models.ConvertTypesCollection(0), None, None, None, True), processing_table_models.ExtractValueTypesCollection(2), False)
        table.init_column('Продолжительность просрочки, дней', 'OverdueAmountMaxCount', [
         [
          [
           'OverdueAmountMaxCount']]], 'value', processing_table_models.ConditionValue(None, None, None, 'value', None, processing_table_models.ConvertTypesCollection(1), None, None, [
         processing_table_models.OutputValueTypesCollection(1)], False), processing_table_models.ExtractValueTypesCollection(2), False)
        table.init_column('Максимальная длина одной просрочки (max)', 'NumberOfOverdueInstalmentsMax', [
         [
          [
           'NumberOfOverdueInstalmentsMax']]], 'value', processing_table_models.ConditionValue(None, None, None, 'value', None, processing_table_models.ConvertTypesCollection(1), None, None, [
         processing_table_models.OutputValueTypesCollection(1)], False), processing_table_models.ExtractValueTypesCollection(2), False)
        table.init_column('Просроченная сумма, тыс. Тенге (макс.)', 'NumberOfOverdueInstalmentsMaxAmount', [
         [
          [
           'NumberOfOverdueInstalmentsMaxAmount']]], 'value', processing_table_models.ConditionValue(None, None, None, 'value', None, processing_table_models.ConvertTypesCollection(1), None, None, [
         processing_table_models.OutputValueTypesCollection(1),
         processing_table_models.OutputValueTypesCollection(3),
         processing_table_models.OutputValueTypesCollection(4)], False), processing_table_models.ExtractValueTypesCollection(2), False)
        table.init_column('Количество месяцев, в которых была зафиксирована просрочка', 'MonthCountInstalments', [
         [
          [
           '-']]], 'value', processing_table_models.ConditionValue(None, None, None, 'value', None, processing_table_models.ConvertTypesCollection(1), None, None, [
         processing_table_models.OutputValueTypesCollection(1),
         processing_table_models.OutputValueTypesCollection(3),
         processing_table_models.OutputValueTypesCollection(4)], False), processing_table_models.ExtractValueTypesCollection(2), False)
        table.init_column('Количество просрочек более 30 дней', 'CountInstalmentsIn30Days', [
         [
          [
           '-']]], 'value', processing_table_models.ConditionValue(None, None, None, 'value', None, processing_table_models.ConvertTypesCollection(1), None, None, [
         processing_table_models.OutputValueTypesCollection(1),
         processing_table_models.OutputValueTypesCollection(3),
         processing_table_models.OutputValueTypesCollection(4)], False), processing_table_models.ExtractValueTypesCollection(2), False)
        table.init_column('Гаранты/созаемщики', 'Garants', [
         [
          [
           '-']]], 'value', processing_table_models.ConditionValue(None, None, None, 'value', None, processing_table_models.ConvertTypesCollection(0), None, None, None, False), processing_table_models.ExtractValueTypesCollection(2), False)
        table.init_column('Вид обеспечения', 'TypeOfGuarantee', [
         [
          [
           'Collateral', 'TypeOfGuarantee']]], 'value', processing_table_models.ConditionValue(None, None, None, 'value', None, processing_table_models.ConvertTypesCollection(0), None, None, None, False), processing_table_models.ExtractValueTypesCollection(2), False)
        table.init_column('Стоимость обеспечения тыс. тенге', 'ValueOfGuarantee', [
         [
          [
           'Collateral', 'ValueOfGuarantee']]], 'value', processing_table_models.ConditionValue(None, None, None, 'value', None, processing_table_models.ConvertTypesCollection(1), None, None, [
         processing_table_models.OutputValueTypesCollection(1),
         processing_table_models.OutputValueTypesCollection(3),
         processing_table_models.OutputValueTypesCollection(4)], False), processing_table_models.ExtractValueTypesCollection(2), False)
        return table
    except Exception as e:
        pass


def init_document_tables(root):
    try:
        tables = []
        existing_contracts_table = init_existing_contracts_table(root)
        terminated_contracts_table = init_terminated_contracts_table(root)
        tables.append(existing_contracts_table)
        tables.append(terminated_contracts_table)
        return tables
    except Exception as e:
        logging.error('Error initialization. ' + str(e))