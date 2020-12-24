# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/kchiba/azurebatchmon/azurebatchmon/task_parser.py
# Compiled at: 2018-03-01 03:14:29
import sys, os, csv
from task import Task
tasks = []

def bind(header_col, value, task):
    key, name = header_col.split(' ')
    if key == '--env':
        task.env[name] = value
    elif key == '--input':
        task.inputs[name] = value
    elif key == '--input-recursive':
        task.input_recursive[name] = value
    elif key == '--output':
        task.outputs[name] = value
    elif key == '--output-recursive':
        task.output_recursive[name] = value


def parseTasksFile(filename):
    tsv_file = file(filename)
    reader = csv.reader(tsv_file, delimiter='\t')
    header = reader.next()
    for idx, row in enumerate(reader):
        task = Task()
        for idx, col in enumerate(row):
            bind(header[idx], col, task)

        tasks.append(task)

    return tasks