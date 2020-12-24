# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/generate/application.py
# Compiled at: 2015-04-03 05:42:21
import os, sys, inflection
from app.commons.generate.generate_code_service import GenerateFileService
args = sys.argv
if __name__ == '__main__':
    table_name = args[1]
    table_name = table_name[table_name.find('=') + 1:]
    gen_file = args[2]
    gen_file = gen_file[gen_file.find('=') + 1:]
    gfs = GenerateFileService(table_name=table_name)
    dao_str = gfs.get_dao_string()
    service_str = gfs.get_service_string()
    handler_str = gfs.get_handler_string()
    list_page_str = gfs.get_list_page_string()
    add_edit_page_str = gfs.get_add_edit_page_string()
    detail_page_str = gfs.get_detail_page_string()
    dao_file_path = os.path.join(os.path.dirname(__file__), 'templates')
    current_path = os.path.dirname(__file__)
    app_path = current_path[:current_path.find('commons/')]
    sing_table_name = inflection.singularize(table_name)
    if gen_file == 'dao' or not gen_file or gen_file == 'all':
        dao_file_name = sing_table_name + '_dao.py'
        dao_file_path = os.path.join(app_path, 'daos/' + dao_file_name)
        f = open(dao_file_path, 'w')
        f.write(dao_str)
        print dao_file_path
    if gen_file == 'service' or not gen_file or gen_file == 'all':
        service_file_name = sing_table_name + '_service.py'
        service_file_path = os.path.join(app_path, 'services/' + service_file_name)
        f = open(service_file_path, 'w')
        f.write(service_str)
        print service_file_path
    if gen_file == 'handler' or not gen_file or gen_file == 'all':
        handler_file_name = sing_table_name + '.py'
        handler_file_path = os.path.join(app_path, 'handlers/' + handler_file_name)
        f = open(handler_file_path, 'w')
        f.write(handler_str)
        print handler_file_path
    if not os.path.exists(os.path.join(app_path, 'views/' + sing_table_name)):
        os.mkdir(os.path.join(app_path, 'views/' + sing_table_name))
    if gen_file == 'list' or not gen_file or gen_file == 'all':
        list_page_file_name = table_name + '.html'
        list_page_file_path = os.path.join(app_path, 'views/' + sing_table_name + '/' + list_page_file_name)
        f = open(list_page_file_path, 'w')
        f.write(list_page_str)
        print list_page_file_path
    if gen_file == 'add' or not gen_file or gen_file == 'all':
        add_edit_page_file_name = sing_table_name + '.html'
        add_edit_page_file_path = os.path.join(app_path, 'views/' + sing_table_name + '/' + add_edit_page_file_name)
        f = open(add_edit_page_file_path, 'w')
        f.write(add_edit_page_str)
        print add_edit_page_file_path
    if gen_file == 'detail' or not gen_file or gen_file == 'all':
        detail_page_file_name = sing_table_name + '_detail.html'
        detail_page_file_path = os.path.join(app_path, 'views/' + sing_table_name + '/' + detail_page_file_name)
        f = open(detail_page_file_path, 'w')
        f.write(detail_page_str)
        print detail_page_file_path
    print gfs.get_route_string()