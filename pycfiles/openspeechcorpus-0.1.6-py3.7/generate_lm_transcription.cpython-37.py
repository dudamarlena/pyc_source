# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/openspeechcorpus_cli/cmu_sphinx/generate_lm_transcription.py
# Compiled at: 2020-01-11 08:44:43
# Size of source mod 2**32: 791 bytes
import codecs
NAME = 'ops_generic_test'
train_transcription = NAME + '/' + NAME + '_etc/' + NAME + '_train.transcription'
test_transcription = NAME + '/' + NAME + '_etc/' + NAME + '_test.transcription'
output = NAME + '/' + NAME + '_etc/' + NAME + '.transcription'
train_transcription_file = codecs.open(train_transcription, encoding='UTF-8')
test_transcription_file = codecs.open(test_transcription, encoding='UTF-8')
output_file = codecs.open(output, 'w+', encoding='UTF-8')
train_content = train_transcription_file.readlines()
for line in train_content:
    output_file.write(' '.join(line.split()[:-1]) + '\n')

test_content = train_transcription_file.readlines()
for line in test_content:
    output_file.write(' '.join(line.split()[:-1]) + '\n')

output_file.close()