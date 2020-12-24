# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mafju/current/icm/removing_madis_from_code/avroknife/avroknife/test/tools.py
# Compiled at: 2015-09-04 08:27:04
import string

class Tools:

    @staticmethod
    def replace(text, prefix, replace_function):
        """Replace substring from text marked with a given prefix using
        replace_function. 
        
        Args:
            text: analyzed text
            prefix: prefix that defines a special substring to be replaced
            replace_function: function that accepts found substring and returns
                new value that should replace the substring
        """
        new = []
        while len(text) > 0:
            chunk_index = string.find(text, prefix)
            if chunk_index == -1:
                new.append(text)
                break
            key_start_index = chunk_index + len(prefix)
            key_end_index = string.find(text, ' ', key_start_index)
            if key_end_index == -1:
                key = text[key_start_index:]
            else:
                key = text[key_start_index:key_end_index]
            value = replace_function(key)
            new.append(text[:chunk_index])
            new.append(value)
            if key_end_index == -1:
                text = ''
            else:
                text = text[key_end_index:]

        return ('').join(new)