# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/fasttextannotator/__init__.py
# Compiled at: 2018-12-19 17:46:26
import codecs, os, re, sys, prompt

def _is_anything(text):
    stripped = text.strip()
    letters = re.sub('[^a-zA-Z]+', '', stripped)
    return len(letters) > 1


def _run_annotator(corpus_file, output_file, labels):
    last_string = None
    if os.path.exists(output_file):
        with codecs.open(output_file, 'r', encoding='utf8') as (output_handle):
            last_line = ''
            for line in output_handle:
                if len(line.strip()) > 0:
                    last_line = line

            if len(last_line) > 0:
                last_string = last_line.replace(last_line.split()[0] + ' ', '').strip()
    with codecs.open(output_file, 'a+', encoding='utf8') as (output_handle):
        with codecs.open(corpus_file, 'r', encoding='utf8') as (corpus_handle):
            for text in corpus_handle:
                if not _is_anything(text):
                    continue
                if last_string is not None:
                    if text.strip() == last_string:
                        last_string = None
                    continue
                label_idx = 1
                print text
                for label in labels:
                    print '[' + str(label_idx) + ']: ' + label
                    label_idx += 1

                chosen_label_idx = -1
                while chosen_label_idx <= 0 or chosen_label_idx > len(labels):
                    try:
                        chosen_label_idx = prompt.integer(prompt='Enter a number choice:', empty=False)
                    except:
                        continue

                if text[(-1)] != '\n':
                    text.append('\n')
                output_handle.write('__label__' + labels[(chosen_label_idx - 1)] + ' ' + text)

    return


def _main():
    if len(sys.argv) <= 3:
        print 'fasttextannotator [corpus-file] [output-file] labels'
        sys.exit(1)
    corpus_file = sys.argv[1]
    output_file = sys.argv[2]
    _run_annotator(corpus_file, output_file, sys.argv[3:])


if __name__ == '__main__':
    _main()