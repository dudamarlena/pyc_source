# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/redi/utils/redcap_records.py
# Compiled at: 2018-08-13 08:58:37
import sys, argparse, json
from redcap import Project, RedcapError

def main():
    parser = argparse.ArgumentParser(description='Read some data from a REDCap Project')
    parser.add_argument('--token', dest='token', default='', required=True, help='Specify the authentication/authorization token that will provide access to the REDCap project')
    parser.add_argument('--url', dest='url', default='', required=True, help='Specify the url of the REDCap server to connect with')
    parser.add_argument('--verify_ssl', dest='verify_ssl', default=True, help='Specify whether the SSL cert of the REDCap server should be checked')
    parser.add_argument('-i', '--import_data', dest='import_data', default='', help='Specify the input data file to load into REDCap')
    parser.add_argument('-f', '--forms', dest='forms', default='', help='Specify a list of forms, separated by spaces, for which data should be returned.')
    parser.add_argument('-t', '--type', choices=[
     'json', 'csv', 'xml'], dest='data_type', default='csv', help='Specify the file type used as input or output. Valid types: json, csv, xml')
    parser.add_argument('--fields', dest='fields', default='', help='Specify a list of fields, separated by spaces, for which data should be returned.')
    parser.add_argument('-e', '--events', dest='events', default='', help='Specify a list of events, separated by spaces, for which data should be returned.')
    parser.add_argument('-r', '--records', dest='records', default='', help='Specify a list of records, separated by spaces, for which data should be returned.')
    args = vars(parser.parse_args())
    data_type = args['data_type']
    if args['verify_ssl'] == 'y':
        args['verify_ssl'] = True
    else:
        args['verify_ssl'] = False
    try:
        project = Project(args['url'], args['token'], '', args['verify_ssl'])
    except:
        print 'Cannot connect to project at ' + args['url'] + ' with token ' + args['token']
        quit()

    if args['import_data'] == '':
        my_forms = args['forms'].split()
        my_fields = args['fields'].split()
        my_events = args['events'].split()
        my_records = args['records'].split()
        data = project.export_records(forms=my_forms, format=data_type, fields=my_fields, events=my_events, records=my_records, event_name='unique')
        if 'json' == data_type:
            print json.dumps(data, ensure_ascii=False)
        else:
            print str(data)
    else:
        file = args['import_data']
        try:
            input = open(file, 'r')
        except IOError:
            print 'Cannot open file ' + file
            quit()

        if 'json' == data_type:
            json_data = json.load(input)
            response = project.import_records(json_data)
        else:
            response = project.import_records(input.read(), format=data_type)
        print response


if __name__ == '__main__':
    main()