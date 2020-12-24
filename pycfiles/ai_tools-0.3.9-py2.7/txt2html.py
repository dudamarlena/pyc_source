# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ai_tools/txt2html.py
# Compiled at: 2018-08-17 05:32:20
import sys

def txt2html(res_file, title_list_str, attach_info):
    TABLE = '<table>'
    TR = '<tr>'
    TD = '<td>'
    C_TABLE = '</table>'
    C_TR = '</tr>'
    C_TD = '</td>'
    title_list = title_list_str.split(',')
    title_length = len(title_list)
    tableContent = '<table border="1"; style="border-collapse:collapse;text-align:left;">'
    tableContent += '<tr bgcolor="#CCCCCC">'
    for title in title_list:
        tableContent += '<td>%s</td>' % title

    tableContent += '</tr>'
    with open(res_file) as (f):
        for line in f:
            items = line.strip().split(' ')
            tableContent += TR
            for item in items:
                tableContent += TD + str(item) + C_TD

            tableContent += C_TR

    tableContent += C_TABLE
    mailContent = '<html>'
    mailContent += '<div style="text-align:center;"><h3> 数据报告 </h3></div>'
    mailContent += '<p></p>'
    mailContent += '<p>%s</p>' % attach_info
    mailContent += tableContent
    mailContent += '</br>'
    mailContent += '</html>'
    print mailContent
    return mailContent


if __name__ == '__main__':
    txt2html(sys.argv[1], sys.argv[2], sys.argv[3])