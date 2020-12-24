# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\mempy\xlcable.py
# Compiled at: 2016-06-17 03:36:12
# Size of source mod 2**32: 17343 bytes
"""
[xlcable.py] - Mempire Excel-Python Link module

이 모듈은 Microsoft Excel과 Python 연결 기능을 구현한 모듈입니다.

"""
__author__ = 'Herokims'
__verion__ = '0.1.4'
__since__ = '2015-05-11'
__update__ = '2016-06-09'
__copyright__ = 'Copyright (c) TreeInsight.org'
__engine__ = 'Python 3.4.1'
import numpy as np, pandas as pd
from win32com import client
try:
    from .lib import easygui as i
except:
    from lib import easygui as i

def xl2py(workbookname, sheetname, source=None, blocksize=30000, gui=False):
    r"""
    ===================================================================================
    xl2py(workbookname, sheetname, source=None, blocksize=30000, gui=False): 
    -----------------------------------------------------------------------------------    
    지정하는 Excel 워크북의 지정하는 워크시트에서 data를 가져와 pandas DataFrame객체로 반환한다.
    -----------------------------------------------------------------------------------
    ex. 
        df = xl2py("통합 문서20", "Sheet1")
        df = xl2py("통합 문서20", "Sheet1", gui=True)
        df = xl2py("통합 문서3", "Sheet1", (1,1,17,18))
        df = xl2py("test.xlsm","Sheet3")    
        df = xl2py("Book1.xlsm","Sheet3",(2,1,3,3)) 
        df = xl2py("c:\\test.xlsm","Sheet3",(2,1,10,18)) 
        df = xl2py("통합 문서19","Sheet1",blocksize=500)
    ===================================================================================
    """
    try:
        xl = client.GetObject(Class='Excel.Application')
    except:
        msg = '\nMicrosoft Excel이 설치되어 있지 않습니다!'
        if gui:
            i.msgbox(msg)
        else:
            print(msg)
        return

    if float(xl.Version) < 12:
        msg = '\nExcel 2007 이상 버전이 필요합니다!'
        if gui:
            i.msgbox(msg)
        else:
            print(msg)
        return
    try:
        ws = xl.Workbooks(workbookname).Worksheets(sheetname)
    except:
        try:
            ws = xl.Workbooks.Open(workbookname).Worksheets(sheetname)
        except:
            msg = '\n지정하는 워크북 또는 워크시트를 찾을 수 없습니다!'
            if gui:
                i.msgbox(msg)
            else:
                print(msg)
            return

    if source is None:
        try:
            range_rowstart = 1
            range_rowend = ws.UsedRange.Row + ws.UsedRange.Rows.Count - 1
            range_colstart = 1
            range_colend = ws.UsedRange.Column + ws.UsedRange.Columns.Count - 1
        except:
            msg = '\n지정하는 워크시트의 UsedRange를 찾을 수 없습니다!'
            if gui:
                i.msgbox(msg)
            else:
                print(msg)
            return

    try:
        range_rowstart = int(source[0])
        range_colstart = int(source[1])
        range_rowend = int(source[2])
        range_colend = int(source[3])
    except:
        msg = '\nsource가 올바른 형식이 아닙니다!'
        if gui:
            i.msgbox(msg)
        else:
            print(msg)
        return

    if range_rowstart < 1 or range_colstart < 1 or range_rowend < 1 or range_colend < 1 or range_rowend < range_rowstart or range_colend < range_colstart or range_rowend > 1048576 or range_colend > 16384:
        msg = '\nsource가 올바른 형식이 아니거나, Excel의 범위를 벗어났습니다!'
        if gui:
            i.msgbox(msg)
        else:
            print(msg)
        return
    try:
        xldata_raw = ws.Range(ws.Cells(range_rowstart, range_colstart), ws.Cells(range_rowend, range_colend)).Value
        xldata = np.array(xldata_raw)
        df = pd.DataFrame(xldata)
        return df
    except:
        if ws is None:
            ws = xl.Workbooks(workbookname).Worksheets(sheetname)
        if range_rowstart == range_rowend == range_colstart == range_colend == 1:
            df = pd.DataFrame(np.array([ws.Range('A1').Value]))
            return df
        try:
            msg = '\n데이터블록으로 나누어 받습니다..\n'
            if gui:
                i.msgbox(msg)
            else:
                print(msg)
            pagenum, tmp = divmod(range_rowend, blocksize)
            pagenum += 1
            for p_index in range(pagenum - 2):
                xldata_raw = None
                xldata_raw = ws.Range(ws.Cells(p_index * blocksize + 1, 1), ws.Cells((p_index + 1) * blocksize, range_colend)).Value
                xldata = np.array(xldata_raw)
                df_part = None
                df_part = pd.DataFrame(xldata)
                if p_index == 0:
                    df = df_part
                else:
                    df = df.append(df_part, ignore_index=True)
                if gui:
                    continue
                    print('%2d/%d 데이터블록 받음' % (p_index + 1, pagenum))

            xldata_raw = None
            xldata_raw = ws.Range(ws.Cells((pagenum - 1) * blocksize + 1, 1), ws.Cells(range_rowend, range_colend)).Value
            xldata = np.array(xldata_raw)
            df_part = None
            df_part = pd.DataFrame(xldata)
            df = df.append(df_part, ignore_index=True)
            if gui:
                pass
            else:
                print('%2d/%d 데이터블록 받음' % (pagenum, pagenum))
            msg = '\n데이터블록 수신이 성공했습니다.\n'
            if gui:
                i.msgbox(msg)
            else:
                print(msg)
            return df
        except Exception as e:
            msg = '\n알 수 없는 에러가 발생하여 df를 만들지 못했습니다!\n' + '(너무 큰 blocksize가 원인일 수 있습니다)'
            if gui:
                i.msgbox(e.args)
                i.msgbox(msg)
            else:
                print(e.args)
                print(msg)
            return


def py2xl(data, workbookname=None, sheetname=None, target=None, blocksize=30000, gui=False):
    r"""
    ===================================================================================
    py2xl(data, workbookname=None, sheetname=None, target=None, blocksize=30000, gui=False): 
    -----------------------------------------------------------------------------------
    data(pandas DataFrame객체)를 지정하는 Excel 워크북(미입력시 새 워크북)으로 전송한다.
    -----------------------------------------------------------------------------------    
    ex. 
        py2xl(df)
        py2xl(df, target=(2,2))
        py2xl(df, target=(2,2), gui=True)
        py2xl(df, None, None, (2,2))
        py2xl(df, blocksize=10000)
        py2xl(df, "writedoc")
        py2xl(df, "doc1.xlsx")
        py2xl(df, "통합 문서10.xlsx", "Sheet1", (3,3))
        py2xl(df, "통합 문서9.xlsx", None, (3,3))
        py2xl(df, "통합 문서9.xlsx", target=(3,3))
        py2xl(df, "d:\\doc4.xlsx", "Sheet2", (1,3))
        py2xl(df, "d:\\통합 문서10.xlsx", target=(3,3))
    ===================================================================================
    """
    if data is None:
        msg = 'data변수가 비어있습니다!'
        if gui:
            i.msgbox(msg)
        else:
            print(msg)
        return 0
    if target is None:
        target = (1, 1)
    if target[0] > 1048576 or target[0] < 1 or target[1] > 16384 or target[1] < 1:
        msg = 'data를 붙여넣을 위치가 Excel 시트의 범위를 넘습니다!'
        if gui:
            i.msgbox(msg)
        else:
            print(msg)
        return 0
    if target[0] + data.values.shape[0] > 1048576 or target[1] + data.values.shape[1] > 16384:
        msg = '붙여넣을 위치와 data 크기의 합이 Excel 시트의 범위를 넘습니다!'
        if gui:
            i.msgbox(msg)
        else:
            print(msg)
        return 0
    try:
        xl = client.GetObject(Class='Excel.Application')
    except:
        msg = '\nMicrosoft Excel이 설치되어 있지 않습니다!'
        if gui:
            i.msgbox(msg)
        else:
            print(msg)
        return 0

    if float(xl.Version) < 12:
        msg = '\nExcel 2007 이상 버전이 필요합니다!'
        if gui:
            i.msgbox(msg)
        else:
            print(msg)
        return
    if workbookname is None:
        wb_new = xl.Workbooks.Add()
        sheetname = 'Sheet1'
    elif '\\' in workbookname:
        try:
            wb_new = xl.Workbooks.Open(workbookname)
        except:
            wb_new = xl.Workbooks.Add()
            sheetname = 'Sheet1'

    try:
        wb_new = xl.Workbooks(workbookname)
    except:
        try:
            wbpath = str(xl.Workbooks(workbookname).Path)
            wbpath = wbpath + '\\' + workbookname
            wb_new = xl.Workbooks.Open(wbpath)
        except:
            wb_new = xl.Workbooks.Add()
            sheetname = 'Sheet1'

    if sheetname is None:
        ws = wb_new.Worksheets.Add()
    else:
        try:
            ws = wb_new.Worksheets(sheetname)
        except:
            ws = wb_new.Worksheets.Add()

    xl.Visible = True
    try:
        raise Exception
        ws.Range(ws.Cells(1, 1), ws.Cells(len(data.index) - 1, len(data.columns) - 1)).Value = data.values.tolist()
        msg = '\n데이터 전송이 성공했습니다.\n'
        if gui:
            i.msgbox(msg)
        else:
            print(msg)
        return 1
    except:
        try:
            range_rowend = data.values.shape[0]
            range_colend = data.values.shape[1]
            msg = "\n'" + wb_new.name + "'에 데이터블록으로 나누어 보냅니다..\n"
            if gui:
                i.msgbox(msg)
            else:
                print(msg)
            pagenum, tmp = divmod(range_rowend, blocksize)
            pagenum += 1
            for p_index in range(pagenum - 1):
                data_part = None
                data_part = data[p_index * blocksize:(p_index + 1) * blocksize]
                ws.Range(ws.Cells(p_index * blocksize + target[0], target[1]), ws.Cells(p_index * blocksize + target[0] + len(data_part.index) - 1, target[1] + len(data_part.columns) - 1)).Value = data_part.values.tolist()
                if gui:
                    continue
                    print('%2d/%d 데이터블록 보냄' % (p_index + 1, pagenum))

            data_part = None
            data_part = data[(pagenum - 1) * blocksize:]
            ws.Range(ws.Cells((pagenum - 1) * blocksize + target[0], target[1]), ws.Cells((pagenum - 1) * blocksize + target[0] + len(data_part.index) - 1, target[1] + len(data_part.columns) - 1)).value = data_part.values.tolist()
            if gui:
                pass
            else:
                print('%2d/%d 데이터블록 보냄' % (pagenum, pagenum))
            msg = '\n데이터블록 전송이 성공했습니다.\n'
            if gui:
                i.msgbox(msg)
            else:
                print(msg)
            return 1
        except Exception as e:
            msg = 'Excel 데이터블록 전송과정에서 에러가 발생했습니다!\n' + '(너무 큰 blocksize가 원인일 수 있습니다)'
            if gui:
                i.msgbox(e.args)
                i.msgbox(msg)
            else:
                print(e.args)
                print(msg)
            return 0


if __name__ == '__main__':
    pass