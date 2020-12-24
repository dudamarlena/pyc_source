# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/ProDaMa/services/setup_script.py
# Compiled at: 2009-09-24 03:11:06
import os, inspect

def configuration():
    file_position = str(__file__)
    os.chdir(file_position[:file_position.rfind('/') + 1])
    text_file = open('setup_script.txt', 'r')
    print ('').join(text_file.readlines())
    text_file.close()
    configuration_data = {}
    configuration_data['DB_NAME'] = raw_input('Database name:   ')
    configuration_data['DB_USER'] = raw_input('Database user:   ')
    configuration_data['DB_PASSWORD'] = raw_input('Database password:   ')
    configuration_data['DB_HOST'] = raw_input('Database url [localhost]:   ') or 'localhost'
    configuration_data['DB_PORT'] = raw_input('Database port [3306]:   ') or '3306'
    print ''
    configuration_data['EMAIL'] = raw_input('Email address (used by PSIBlast):   ')
    configuration_data['PSIBLAST'] = raw_input('PSIBlast path:   ')
    configuration_data['PISCES'] = raw_input('PISCES path:   ')
    configuration_data['DATA'] = raw_input('Temporary data directory path:   ')
    if '' in configuration_data.values():
        print 'Some of the required fields are empty. Please repeat the configuration.'
        exit()
    config_file = open('config.py', 'r')
    config_file_lines = config_file.readlines()
    config_file.close()
    config_file = open('config.py', 'w')
    for line in config_file_lines:
        if line.find('=') != -1:
            quotes_start = line.find('"')
            quotes_end = line.rfind('"')
            line_field = line.split('=')[0].strip()
            if line_field != 'DB_ENGINE':
                line = line[:quotes_start + 1] + configuration_data[line_field] + line[quotes_end:]
        config_file.write(line)

    os.remove('config.pyc')


if __name__ == '__main__':
    configuration()