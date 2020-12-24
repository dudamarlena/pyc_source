# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/openspeechcorpus_cli/cmu_sphinx/generate_filler.py
# Compiled at: 2020-01-11 09:24:56
# Size of source mod 2**32: 388 bytes
"""
Genera un archivo con los silencios necesarios para el entrenamiento
"""
import codecs

def execute_script(filler_file):
    default_silences = [
     '<s>', '<sil>', '</s>']
    f = codecs.open(filler_file, 'w+', encoding='UTF-8')
    for default_silence in default_silences:
        f.write(default_silence + '\t' + 'SIL\n')

    f.close()