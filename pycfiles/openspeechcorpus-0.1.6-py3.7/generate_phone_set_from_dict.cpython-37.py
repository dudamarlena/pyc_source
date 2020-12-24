# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/openspeechcorpus_cli/cmu_sphinx/generate_phone_set_from_dict.py
# Compiled at: 2020-01-11 09:24:56
# Size of source mod 2**32: 619 bytes
"""
Crea una lista de fonemas a partir de un diccionario fonetico
"""
import codecs

def execute_script(dict_file, output_file):
    f = codecs.open(dict_file, 'rb', encoding='UTF-8')
    lines = f.readlines()
    all_phones = []
    for line in lines:
        phones = line.split()[1:]
        for phone in phones:
            if phone not in all_phones:
                all_phones.append(phone)

    o_file = codecs.open(output_file, 'w+', encoding='UTF-8')
    for phone in all_phones:
        o_file.write(phone + '\n')

    o_file.write('SIL\n')
    o_file.close()