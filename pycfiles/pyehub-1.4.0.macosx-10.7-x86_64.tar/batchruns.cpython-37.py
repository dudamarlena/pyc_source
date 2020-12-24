# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/juancomish/miniconda3/lib/python3.7/site-packages/pyehub/batchruns.py
# Compiled at: 2019-07-03 19:21:52
# Size of source mod 2**32: 2560 bytes
"""
A script for using the run.py module as a subprocess to solve multiple Energy Hubs while changing a given parameter.

This functionality is now also provided by the Besos EvaluatorEH.
"""
import subprocess, openpyxl as op, numpy as np
LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

def main():
    start = 671
    stop = 1
    steps = 11
    in_file = 'Individual_Hubs/test.xlsx'
    sheet_name = 'Storages'
    cell_to_set = 'B4'
    model_out_dir = 'Individual_Hubs/LI_Battery/PV_50/Diesel_27'
    model_inputs = 'Individual_Hubs/temp_inputs.xls'
    sheet_to_read = 'Other'
    cells_to_read = ['B168', 'B170']
    final_output_file = 'Individual_Hubs/LI_Battery/PV_50/Diesel_27/output_LI_PV50_D27.xlsx'
    result_wb = op.Workbook()
    result_sheet = result_wb['Sheet']
    output_cells = ['Input value'] + cells_to_read
    for column, cell in zip(LETTERS, output_cells):
        result_sheet[f"{column}1"].value = cell

    for row, value in enumerate((np.linspace(start, stop, steps)), start=2):
        wb = op.load_workbook(in_file)
        wb[sheet_name][cell_to_set].value = value
        wb.save(model_inputs)
        model_out_file = f"{model_out_dir}/LI_PV50_D27_{int(value)}.xlsx"
        print('starting subprocess')
        subprocess.run(['python', 'run.py', '--output', 'model_out_file'])
        print('file should be there')
        wb = op.load_workbook(model_out_file)
        result_sheet[f"A{row}"].value = value
        for col, cell_to_read in zip(LETTERS[1:], cells_to_read):
            print(f"writing {wb[sheet_to_read][cell_to_read].value} to {col}{row} for {value}")
            result_sheet[f"{col}{row}"].value = wb[sheet_to_read][cell_to_read].value

    result_wb.save(final_output_file)


if __name__ == '__main__':
    main()