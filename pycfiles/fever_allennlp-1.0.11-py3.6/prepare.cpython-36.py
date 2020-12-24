# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/fever/submission/prepare.py
# Compiled at: 2019-02-21 15:52:13
# Size of source mod 2**32: 1334 bytes
import argparse, json
parser = argparse.ArgumentParser()
parser.add_argument('--predicted_labels', type=str)
parser.add_argument('--predicted_evidence', type=str)
parser.add_argument('--out_file', type=str)
args = parser.parse_args()
predicted_labels = []
predicted_evidence = []
actual = []
with open(args.predicted_labels, 'r') as (predictions_file):
    for line in predictions_file:
        predicted_labels.append(json.loads(line)['predicted_label'])

with open(args.predicted_evidence, 'r') as (predictions_file):
    for line in predictions_file:
        line = json.loads(line)
        if 'predicted_sentences' in line:
            predicted_evidence.append(line['predicted_sentences'])
        else:
            if 'predicted_evidence' in line:
                predicted_evidence.append(line['predicted_evidence'])
            else:
                if 'evidence' in line:
                    all_evidence = []
                    for evidence_group in line['evidence']:
                        all_evidence.extend(evidence_group)

                    predicted_evidence.append(list(set([(evidence[2], evidence[3]) for evidence in all_evidence])))

predictions = []
for ev, label in zip(predicted_evidence, predicted_labels):
    predictions.append({'predicted_evidence':ev,  'predicted_label':label})

with open(args.out_file, 'w+') as (f):
    for line in predictions:
        f.write(json.dumps(line) + '\n')