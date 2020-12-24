# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/drqascripts/retriever/interactive.py
# Compiled at: 2019-08-29 06:03:42
# Size of source mod 2**32: 1453 bytes
"""Interactive mode for the tfidf DrQA retriever module."""
import argparse, code, prettytable, logging
from drqa import retriever
logger = logging.getLogger()
logger.setLevel(logging.INFO)
fmt = logging.Formatter('%(asctime)s: [ %(message)s ]', '%m/%d/%Y %I:%M:%S %p')
console = logging.StreamHandler()
console.setFormatter(fmt)
logger.addHandler(console)
parser = argparse.ArgumentParser()
parser.add_argument('--model', type=str, default=None)
args = parser.parse_args()
logger.info('Initializing ranker...')
ranker = retriever.get_class('tfidf')(tfidf_path=(args.model))

def process(query, k=1):
    doc_names, doc_scores = ranker.closest_docs(query, k)
    table = prettytable.PrettyTable([
     'Rank', 'Doc Id', 'Doc Score'])
    for i in range(len(doc_names)):
        table.add_row([i + 1, doc_names[i], '%.5g' % doc_scores[i]])

    print(table)


banner = '\nInteractive TF-IDF DrQA Retriever\n>> process(question, k=1)\n>> usage()\n'

def usage():
    print(banner)


code.interact(banner=banner, local=(locals()))