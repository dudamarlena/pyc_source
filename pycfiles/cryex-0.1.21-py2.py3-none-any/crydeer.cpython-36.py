# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/CryDeer/crydeer.py
# Compiled at: 2017-01-06 22:21:32
# Size of source mod 2**32: 1033 bytes
from sys import argv
import sys, os
from .controller import Controller
import click
controller = Controller()

@click.group(help='包裹查询助手')
def main():
    pass


@main.command('add', help='新增包裹')
@click.argument('number')
@click.option('-d', '--description', help='包裹描述')
def add_package(number, description):
    controller.new_item(number, description)


@main.command('remove', help='新增包裹')
@click.argument('number')
@click.option('-d', '--description', help='包裹描述')
def remove_package(number, description):
    controller.delete_item(number)


@main.command('list', help='显示所有包裹信息')
def list_packages():
    controller.list()


@main.command('detail', help='显示包裹详细信息')
@click.argument('number')
def show_detail(number):
    controller.show_info(number)


@main.command('update', help='更新包裹信息')
def update_packages():
    controller.update_all()


if __name__ == '__main__':
    main()