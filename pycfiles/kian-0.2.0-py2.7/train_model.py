# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/scripts/train_model.py
# Compiled at: 2015-11-03 05:43:43
import argparse
if __name__ == '__main__' and __package__ is None:
    from os import sys, path
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from kian import ModelWithData
import kian
parser = argparse.ArgumentParser(description='Train a model.')
parser.add_argument('--name', '-n', nargs='?', required=True, help='name of the model to train')
parser.add_argument('--reload-wikidata', '-rwd', action='store_true', help='Reload data from Wikidata')
parser.add_argument('--reload-wikipedia', '-rwp', action='store_true', help='Reload data from Wikipedia')
args = parser.parse_args()
model = ModelWithData.from_file(args.name)
print 'Loading data'
model.load_data(reload_wiki=args.reload_wikipedia, reload_wikidata=args.reload_wikidata)
model.retrieve_data(reload_wiki=args.reload_wikipedia, reload_wikidata=args.reload_wikidata)
print 'Building the training set'
model.label_categories()
print 'Training the model'
bot = kian.Kian(model)
bot.run()