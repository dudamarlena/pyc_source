# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/jlopes/PycharmProjects/mcg/core/TestsGenerator.py
# Compiled at: 2017-01-24 01:10:58
# Size of source mod 2**32: 3160 bytes
from faker import Factory

class TestsGenerator:

    def fetch_type(self, file, field):
        fake = Factory.create()
        if field['specific_type'] == 'simple_string':
            file.write("'" + fake.word() + "'")
        else:
            if field['specific_type'] == 'sentence_string':
                file.write("'" + fake.sentence(variable_nb_words=True) + "'")
            else:
                if field['specific_type'] == 'text_string':
                    file.write("'" + fake.text() + "'")
                else:
                    if field['specific_type'] == 'id':
                        file.write("'" + fake.md5(raw_output=False) + "'")
                    else:
                        if field['specific_type'] == 'name':
                            file.write("'" + fake.name() + "'")
                        else:
                            if field['specific_type'] == 'phone_number':
                                file.write("'" + fake.phone_number() + "'")
                            else:
                                if field['specific_type'] == 'user_agent':
                                    file.write("'" + fake.user_agent() + "'")
                                else:
                                    if field['specific_type'] == 'job':
                                        file.write("'" + fake.job() + "'")
                                    else:
                                        if field['specific_type'] == 'url':
                                            file.write("'" + fake.url() + "'")
                                        else:
                                            if field['specific_type'] == 'email':
                                                file.write("'" + fake.email() + "'")
                                            else:
                                                if field['specific_type'] == 'ipv4':
                                                    file.write("'" + fake.ipv4(network=False) + "'")
                                                else:
                                                    if field['specific_type'] == 'mac_address':
                                                        file.write("'" + fake.mac_address() + "'")
                                                    else:
                                                        if field['specific_type'] == 'file_name':
                                                            file.write("'" + fake.file_name(category=None, extension=None) + "'")
                                                        else:
                                                            if field['specific_type'] == 'datetime':
                                                                file.write("'" + fake.iso8601(tzinfo=None) + "'")
                                                            else:
                                                                if field['specific_type'] == 'hex_color':
                                                                    file.write("'" + fake.hex_color() + "'")
                                                                else:
                                                                    if field['specific_type'] == 'rgb_color':
                                                                        file.write("'" + fake.rgb_color() + "'")
                                                                    else:
                                                                        if field['specific_type'] == 'address':
                                                                            file.write("'" + fake.address() + "'")
                                                                        else:
                                                                            if field['specific_type'] == 'postcode':
                                                                                file.write("'" + fake.postcode() + "'")
                                                                            else:
                                                                                if field['specific_type'] == 'state':
                                                                                    file.write("'" + fake.state() + "'")
                                                                                else:
                                                                                    if field['specific_type'] == 'city':
                                                                                        file.write("'" + fake.city() + "'")
                                                                                    else:
                                                                                        if field['specific_type'] == 'address_number':
                                                                                            file.write(fake.random_number(digits=None, fix_len=False))
                                                                                        else:
                                                                                            if field['specific_type'] == 'street_address':
                                                                                                file.write("'" + fake.street_address() + "'")
                                                                                            else:
                                                                                                if field['specific_type'] == 'state_abbr':
                                                                                                    file.write("'" + fake.state_abbr() + "'")
                                                                                                else:
                                                                                                    if field['specific_type'] == 'country':
                                                                                                        file.write("'" + fake.country() + "'")
                                                                                                    else:
                                                                                                        if field['specific_type'] == 'country_code':
                                                                                                            file.write("'" + fake.country_code() + "'")
                                                                                                        else:
                                                                                                            if field['specific_type'] == 'boolean':
                                                                                                                file.write(fake.pybool())
                                                                                                            else:
                                                                                                                if field['specific_type'] == 'int':
                                                                                                                    file.write(fake.pyint())
                                                                                                                else:
                                                                                                                    if field['specific_type'] == 'float':
                                                                                                                        file.write(fake.pyfloat(left_digits=None, right_digits=None, positive=False))
                                                                                                                    else:
                                                                                                                        file.write('Unknown')