# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/scripts/human_review_add.py
# Compiled at: 2015-11-03 05:22:30
import argparse, pywikibot, sys, codecs, os
if __name__ == '__main__' and __package__ is None:
    from os import sys, path
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
import kian.fitness
from kian import TrainedModel
from kian import Kian
site = pywikibot.Site('wikidata', fam='wikidata')

def main():
    args = sys.argv[1:]
    parser = argparse.ArgumentParser(description='Parse and add statements based on trained model')
    parser.add_argument('--name', '-n', nargs='?', required=True, help='name of the model to train')
    parsed_args = parser.parse_known_args(args)[0]
    model = TrainedModel.from_file(parsed_args.name)
    print 'Loading the model'
    model.load_data()
    model.load()
    file_path = os.path.join(model.data_directory, 'res2.dat')
    if not os.path.isfile(file_path):
        raise ValueError('You should train the model first')
    with codecs.open(file_path, 'r', 'utf-8') as (f):
        cv_set = eval(f.read())
    first_thrashhold = kian.fitness.optimum_thrashhold(cv_set, 1)[0]
    second_thrashhold = kian.fitness.optimum_thrashhold(cv_set, 0.125)[0]
    print 'Finding possible adds to human review'
    print (first_thrashhold, second_thrashhold)
    pros = model.wikidata_data_w | model.wikidata_data_wo
    print len(pros)
    name = None
    a = []
    with model.wiki_data_file as (f):
        for line in f:
            line = line.replace('\n', '')
            if '\t' not in line:
                continue
            if name and name != line.split('\t')[0]:
                if name in pros:
                    a = []
                    name = line.split('\t')[0]
                    continue
                features = model.label_case(a)
                res = Kian.kian(model.theta, features)[0]
                if res > first_thrashhold and res < second_thrashhold:
                    print '%s: %s' % (name, res)
                a = []
            name = line.split('\t')[0]
            a.append(line.split('\t')[1])

    return


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        sys.exit()