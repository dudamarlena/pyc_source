# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/fever2/scorer.py
# Compiled at: 2019-06-13 16:52:12
from fever.scorer import fever_score

def potency(actual, *all_systems_predictions):
    if len(all_systems_predictions) == 0:
        return 0
    system_scores = map(lambda system_predictions: 1 - fever_score(system_predictions, actual)[0], all_systems_predictions)
    return sum(system_scores) / len(all_systems_predictions)


if __name__ == '__main__':
    import argparse, json, os
    parser = argparse.ArgumentParser()
    parser.add_argument('--actual-file')
    parser.add_argument('--submission-dir')
    args = parser.parse_args()
    all_submissions = []
    actual = []
    for filename in os.listdir(args.submission_dir):
        with open(args.submission_dir + '/' + filename, 'r') as (file):
            file_lines = []
            for line in file:
                file_lines.append(json.loads(line))

            all_submissions.append(file_lines)

    with open(args.actual_file, 'r') as (file):
        for line in file:
            actual.append(json.loads(line))

    print potency(actual, all_submissions)