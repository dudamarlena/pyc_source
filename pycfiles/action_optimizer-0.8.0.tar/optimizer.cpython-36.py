# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/chris/git/action-optimizer/action_optimizer/optimizer.py
# Compiled at: 2019-04-09 16:01:17
# Size of source mod 2**32: 28636 bytes
from __future__ import print_function
import os, sys, traceback, copy, csv, random, math
from datetime import date, timedelta
from pprint import pprint
from decimal import Decimal
from collections import defaultdict
from dateutil.parser import parse
import numpy as np
from pyexcel_ods import get_data
from weka.arff import ArffFile, Nom, Num, Str, Date, MISSING
from weka.classifiers import EnsembleClassifier

class SkipRow(Exception):
    pass


BASE_DIR = os.path.split(os.path.realpath(__file__))[0]
NUMERIC = 'numeric'
DATE = 'date'
MN = 'mn_'
NO = 'no_'
EV = 'ev_'
MONTHLY = '_monthly'
OTHERS = 'others'
NA_CHANGE = ''
RELATIVE_CHANGE = 'rel'
ABSOLUTE_CHANGE = 'abs'
CHANGE_TYPES = (NA_CHANGE, RELATIVE_CHANGE, ABSOLUTE_CHANGE)
MIN_DAYS = 30
HEADER_ROW_INDEX = 0
TYPE_ROW_INDEX = 1
RANGE_ROW_INDEX = 2
LEARN_ROW_INDEX = 3
PREDICT_ROW_INDEX = 4
CHANGE_ROW_INDEX = 5
DATA_ROW_INDEX = 6
TOLERANCE = 1.0
CLASS_ATTR_NAME = 'score_next'
DEFAULT_SCORE_FIELD_NAME = 'score'
DEFAULT_CLASSIFIER_FN = '/tmp/%s-last-classifier.pkl.gz'
DEFAULT_RELATION = '%s-training'

def attempt_cast_str_to_numeric(value):
    try:
        return float(value)
    except ValueError:
        return value


class Optimizer(object):

    def __init__(self, fn, **kwargs):
        if not fn.startswith('/'):
            fn = os.path.join(BASE_DIR, fn)
        elif not os.path.isfile(fn):
            raise AssertionError('File %s does not exist.' % fn)
        self.fn = fn
        self.fqfn_base = os.path.splitext(os.path.abspath(fn))[0]
        self.fn_base = os.path.splitext(os.path.split(fn)[0])[0]
        self.__dict__.update(kwargs)
        self.score_field_name = self.__dict__.get('score_field_name') or DEFAULT_SCORE_FIELD_NAME
        self.only_attribute = self.__dict__.get('only_attribute')
        self.stop_on_error = self.__dict__.get('stop_on_error') or False
        self.no_train = self.__dict__.get('no_train') or False
        self.all_classifiers = self.__dict__.get('all_classifiers') or False
        self.calculate_pcc = self.__dict__.get('calculate_pcc') or False
        self.yes = self.__dict__.get('yes', None)
        self.classifier_fn = self.__dict__.get('classifier_fn', DEFAULT_CLASSIFIER_FN) % self.fn_base
        self.relation = self.__dict__.get('relation', DEFAULT_RELATION) % self.fn_base

    def analyze(self, save=True):
        self.score_field_name = self.score_field_name or DEFAULT_SCORE_FIELD_NAME
        print('Retrieving data...')
        sys.stdout.flush()
        data = get_data(self.fn)['data']
        field_to_day_count = {}
        column_names = data[HEADER_ROW_INDEX]
        column_types = data[TYPE_ROW_INDEX]
        column_types_dict = dict(zip(column_names, column_types))
        column_ranges = dict(zip(column_names, data[RANGE_ROW_INDEX]))
        for _name in column_ranges.keys():
            if _name not in 'date' and column_ranges[_name]:
                column_ranges[_name] = list(map(float, column_ranges[_name].split(',')))
            else:
                column_ranges[_name] = None

        column_nominals = self.column_nominals = {}
        if not len(column_names) == len(column_types):
            raise AssertionError
        else:
            for column_name, ct in zip(column_names, column_types):
                assert ct in (DATE, NUMERIC) or ct[0] == '{' and ct[(-1)] == '}', 'Invalid type: %s' % ct
                if ct[0] == '{':
                    column_nominals[column_name] = set(ct[1:-1].split(','))

            column_learnables = self.column_learnables = {}
            for _a, _b in zip(column_names, data[LEARN_ROW_INDEX]):
                if _a == DATE:
                    column_learnables[_a] = 0
                    continue
                try:
                    column_learnables[_a] = int(_b)
                except Exception as exc:
                    raise Exception('Error checking controllable for column %s: %s' % (_a, exc))

            print('column_learnables:', column_learnables)
            column_predictables = self.column_predictables = {}
            for _a, _b in zip(column_names, data[PREDICT_ROW_INDEX]):
                if _a == DATE:
                    column_predictables[_a] = 0
                    continue
                try:
                    column_predictables[_a] = int(_b)
                except Exception as exc:
                    raise Exception('Error checking predictable for column %s: %s' % (_a, exc))

            print('column_predictables:', column_predictables)
            column_changeables = self.column_changeables = {}
            for _a, _b in zip(column_names, data[CHANGE_ROW_INDEX]):
                if _a == DATE:
                    column_changeables[_a] = NA_CHANGE
                    continue
                try:
                    assert _b in CHANGE_TYPES, 'Invalid change type for column %s: %s' % (_a, _b)
                    column_changeables[_a] = _b
                except Exception as exc:
                    raise Exception('Error checking changeable for column %s: %s' % (_a, exc))

            print('column_changeables:', column_changeables)
            row_errors = {}
            data = data[DATA_ROW_INDEX:]
            arff = ArffFile(relation=(self.relation))
            arff.class_attr_name = CLASS_ATTR_NAME
            arff.relation = self.relation
            row_count = 0
            best_day = (float('-inf'), None)
            best_date = (float('-inf'), None)
            last_full_day = (date.min, None)
            date_to_score = {}
            column_values = defaultdict(set)
            new_rows = []
            for row in data:
                row_count += 1
                try:
                    if not row:
                        continue
                    else:
                        if not len(row) == len(column_names):
                            raise AssertionError('Row %i has length %i but there are %i column headers.' % (row_count, len(row), len(column_names)))
                        elif not len(row) == len(column_types):
                            raise AssertionError
                        old_row = dict(zip(column_names, row))
                        new_row = {}
                        for row_value, column_name, ct in zip(row, column_names, column_types):
                            if column_name.startswith('next_day') or column_name.startswith('subscore'):
                                if row_value == '':
                                    raise SkipRow
                                    continue
                            if ct == DATE:
                                if row_count == 1:
                                    if not isinstance(row_value, date):
                                        print(('Warning: Invalid date "%s" on row %s.' % (row_value, row_count)), file=(sys.stderr))
                                        raise SkipRow
                                    if isinstance(row_value, str):
                                        _row_value = parse(row_value)
                                        if _row_value:
                                            row_value = _row_value.date()
                                            old_row[column_name] = row_value
                                        if not isinstance(row_value, date):
                                            raise AssertionError('Invalid date "%s" on row %s.' % (row_value, row_count))
                                            continue
                                    else:
                                        if ct == NUMERIC:
                                            if row_value != '':
                                                row_value = attempt_cast_str_to_numeric(row_value)
                                                assert isinstance(row_value, (int, bool, float)), 'Invalid numeric value "%s" of type "%s" in column "%s" of row %i.' % (
                                                 row_value, type(row_value), column_name, row_count)
                                                new_row[column_name] = Num(row_value)
                                        else:
                                            continue
                                else:
                                    if ct[0] == '{':
                                        if row_value != '':
                                            assert str(row_value) in column_nominals[column_name], 'Invalid nominal value "%s" for column "%s". Legal values: %s' % (
                                             row_value, column_name, ', '.join(sorted(map(str, column_nominals[column_name]))))
                                            new_row[column_name] = Nom(str(row_value))
                                        else:
                                            continue
                                    else:
                                        raise NotImplementedError('Unknown type/column: %s/%s' % (ct, column_name))
                                    column_values[column_name].add(new_row[column_name])
                                    field_to_day_count.setdefault(column_name, 0)
                                    field_to_day_count[column_name] += new_row[column_name] != '' and new_row[column_name] != None

                        new_row['date'] = old_row['date']
                        assert isinstance(old_row['date'], date)
                    date_to_score[old_row['date']] = new_row[self.score_field_name]
                    print("new_row:'%s':value: %s" % (self.score_field_name, new_row[self.score_field_name].value))
                    best_day = max(best_day, (new_row[self.score_field_name].value, new_row), key=(lambda o: o[0]))
                    best_date = max(best_date, (new_row[self.score_field_name].value, old_row['date']), key=(lambda o: o[0]))
                    last_full_day = max(last_full_day, (old_row['date'], new_row), key=(lambda o: o[0]))
                    new_rows.append(new_row)
                except SkipRow:
                    pass
                except Exception as exc:
                    traceback.print_exc()
                    row_errors[row_count] = traceback.format_exc()
                    if self.stop_on_error:
                        raise

            assert new_rows, 'No data!'
        modified_rows = []
        for new_row in new_rows:
            current_date = new_row['date']
            current_score = new_row[self.score_field_name]
            next_date = current_date + timedelta(days=1)
            assert isinstance(next_date, date)
            if next_date in date_to_score:
                next_score = date_to_score[next_date]
                print('current_date:', current_date)
                print('current_score.value:', current_score.value)
                print('next_date:', next_date)
                print('next_score.value:', next_score.value)
                assert current_date < next_date
                new_row[CLASS_ATTR_NAME] = next_score
                for _column, _controllable in column_learnables.items():
                    if not _controllable and _column in new_row:
                        del new_row[_column]

                print('new_row:', new_row)
                sys.stdout.flush()
                modified_rows.append(new_row)
                arff.append(new_row)

        if self.calculate_pcc:
            pcc_rows = []
            with open('pcc.csv', 'w') as (fout):
                fieldnames = [
                 'name', 'samples', 'pcc', 'utility']
                writer = csv.DictWriter(fout, fieldnames=fieldnames)
                writer.writerow(dict(zip(fieldnames, fieldnames)))
                for target_attr in column_names:
                    if not column_types_dict[target_attr] != NUMERIC:
                        if not not column_predictables.get(target_attr):
                            if target_attr == CLASS_ATTR_NAME:
                                continue
                            _x = []
                            _y = []
                            for new_row in modified_rows:
                                try:
                                    xv = float(new_row[CLASS_ATTR_NAME].value)
                                    yv = float(new_row[target_attr].value)
                                    _x.append(xv)
                                    _y.append(yv)
                                except (KeyError, AttributeError):
                                    continue

                            x = np.array(_x).astype(np.float32)
                            y = np.array(_y).astype(np.float32)
                            pcc = np.corrcoef(x, y)[(0, 1)]
                            print('Pearson correlation for %s: %s' % (target_attr, pcc))
                            samples = len(_x)
                            if math.isnan(pcc):
                                continue
                            pcc_rows.append(dict(name=target_attr, pcc=pcc, samples=samples, utility=(samples * pcc)))

                pcc_rows.sort(key=(lambda o: o['utility']))
                for pcc_row in pcc_rows:
                    writer.writerow(pcc_row)

            return
        else:
            print('attributes:', sorted(arff.attributes))
            arff.alphabetize_attributes()
            assert len(arff), 'Empty arff!'
            if row_errors:
                print('=' * 80)
                print('Row Errors: %s' % len(row_errors))
                for row_count in sorted(row_errors):
                    print('Row %i:' % row_count)
                    print(row_errors[row_count])

                print('=' * 80)
            else:
                print('No row errors.')
            for name in column_nominals:
                if name in arff.attribute_data:
                    arff.attribute_data[name].update(column_nominals[name])

            training_fn = os.path.join(BASE_DIR, self.fqfn_base + '.arff')
            print('training_fn:', training_fn)
            print('Writing arff...')
            with open(training_fn, 'w') as (fout):
                arff.write(fout)
            print('Arff written!')
            if self.all_classifiers:
                classes = None
            else:
                classes = [
                 'weka.classifiers.lazy.IBk',
                 'weka.classifiers.lazy.KStar',
                 'weka.classifiers.functions.MultilayerPerceptron']
            if self.no_train:
                assert os.path.isfile(self.classifier_fn), 'If training is disabled, then a classifier file must exist to re-use, but %s does not exist.' % self.classifier_fn
                print('Loading classifier from file %s...' % self.classifier_fn)
                classifier = EnsembleClassifier.load(self.classifier_fn)
                print('Classifier loaded.')
            else:
                classifier = EnsembleClassifier(classes=classes)
                classifier.train(training_data=training_fn, verbose=(self.all_classifiers))
            print('=' * 80)
            print('best:')
            classifier.get_training_best()
            print('=' * 80)
            print('coverage: %.02f%%' % (classifier.get_training_coverage() * 100))
            if self.all_classifiers:
                print('Aborting query with all classifiers.')
                sys.exit(0)
            print('=' * 80)
            best_day_score, best_day_data = best_day
            print('best_day_score:', best_day_score)
            print('best_day_data:')
            pprint(best_day_data, indent=4)
            print('best date:', best_date)
            print('last full day:', last_full_day)
            last_full_day_date = last_full_day[0]
            if self.yes is None:
                if abs((last_full_day_date - date.today()).days) > 1:
                    if input('Last full day is %s, which is over 1 day ago. Continue? [yn]:' % last_full_day_date).lower()[0] != 'y':
                        sys.exit(1)
            print('=' * 80)
            print('ranges:')
            for _name, _range in sorted((column_ranges.items()), key=(lambda o: o[0])):
                print(_name, _range)

            _, best_data = last_full_day
            queries = []
            query_name_list = sorted(column_values)
            if self.only_attribute:
                query_name_list = [
                 self.only_attribute]
            for name in query_name_list:
                if name == CLASS_ATTR_NAME:
                    pass
                else:
                    if name in column_predictables:
                        if not column_predictables[name]:
                            continue
                        print('Query attribute name:', name)
                        if isinstance(list(column_values[name])[0], Nom):
                            print('Nominal attribute.')
                            for direction in column_nominals[name]:
                                query_value = direction = Nom(direction)
                                new_query = copy.deepcopy(best_data)
                                new_query[name] = direction
                                best_value = best_data.get(name, sorted(column_nominals[name])[0])
                                if best_value != query_value:
                                    description = '%s: change from %s -> %s' % (name, best_value, query_value)
                                    print('\t%s' % description)
                                    queries.append((name, description, new_query))

                        else:
                            print('Numeric attribute.')
                            column_ranges.get(name) or print('Has no column ranges. Skipping.')
                    else:
                        _min, _max, _step = column_ranges[name]
                        assert _min < _max, 'Invalid min/max!'
                        if self.only_attribute or name in 'bed':
                            _value = _min
                            while _value <= _max:
                                print('Checking query %s=%s.' % (name, _value))
                                new_query = copy.deepcopy(best_data)
                                _mean = None
                                if name not in new_query:
                                    new_query[name] = sum(column_values[name], Num(0.0)) / len(column_values[name])
                                    _mean = copy.deepcopy(new_query[name])
                                if _value == best_data.get(name, _mean):
                                    print('Hold case. Skipping.')
                                    continue
                                new_query[name].value = _value
                                if best_data.get(name, _mean) != new_query[name]:
                                    print('\tallowable range min/max/step:', _min, _max, _step)
                                    description = '%s: change from %s -> %s' % (name, best_data.get(name, _mean), new_query[name].value)
                                    print('\t%s' % description)
                                    assert _min <= new_query[name].value <= _max
                                    queries.append((name, description, new_query))
                                _value += _step

                        else:
                            for direction in (-1, 1):
                                new_query = copy.deepcopy(best_data)
                                _mean = None
                                if name not in new_query:
                                    new_query[name] = sum(column_values[name], Num(0.0)) / len(column_values[name])
                                    _mean = copy.deepcopy(new_query[name])
                                new_query[name].value += direction * _step
                                new_query[name].value = min(new_query[name].value, _max)
                                new_query[name].value = max(new_query[name].value, _min)
                                if best_data.get(name, _mean) != new_query[name]:
                                    print('\tallowable range min/max/step:', _min, _max, _step)
                                    description = '%s: change from %s -> %s' % (name, best_data.get(name, _mean), new_query[name])
                                    print('\t%s' % description)
                                    queries.append((name, description, new_query))

                        new_query = copy.deepcopy(best_data)
                        description = '%s: hold at %s' % (name, best_data.get(name, _mean))
                        queries.append((name, description, new_query))

            if save:
                print('Saving classifier...')
                classifier.save(self.classifier_fn)
                print('Classifier saved to %s.' % self.classifier_fn)
            print('=' * 80)
            total = len(queries)
            i = 0
            final_recommendations = []
            final_scores = {}
            for name, description, query_data in queries:
                i += 1
                print('Running query %i of %i...' % (i, total))
                new_arff = arff.copy(schema_only=True)
                new_arff.relation = 'optimizer-query'
                query_data[CLASS_ATTR_NAME] = MISSING
                for _column, _controllable in column_learnables.items():
                    if not _controllable and _column in query_data:
                        del query_data[_column]

                print('query_data:', sorted(query_data))
                new_arff.append(query_data)
                print('$' * 80)
                print('predicting...')
                predictions = list(classifier.predict(new_arff, tolerance=TOLERANCE, verbose=1, cleanup=0))
                print('\tdesc:', description)
                print('\tpredictions:', predictions)
                score_change = predictions[0].predicted
                print('\tscore change: %.02f' % score_change)
                final_recommendations.append((score_change, 0, 0, description, name))
                final_scores.setdefault(name, (float('-inf'), None))
                final_scores[name] = max(final_scores[name], (score_change, description))

            print('=' * 80)
            print('best predictors:')
            best_names = classifier.get_best_predictors(tolerance=TOLERANCE, verbose=True)
            print(best_names)
            seed_date = last_full_day[0]
            print('=' * 80)
            print('recommendations by attribute based on date: %s' % seed_date)
            final_recommendations.sort(key=(lambda o: (o[4], o[0])))
            i = 0
            digits = len(str(len(final_recommendations)))
            for change, _old_score, _new_score, description, name in final_recommendations:
                i += 1
                best_score_change, best_description = final_scores[name]
                if description != best_description:
                    pass
                else:
                    print(('\t%0' + str(digits) + 'i %s => %.06f') % (i, description, change))

            final_recommendations.sort()
            print('=' * 80)
            print('Evening recommendations by change based on date: %s' % seed_date)
            print_recommendation(final_recommendations, final_scores, typ=EV)
            print('=' * 80)
            print('Morning recommendations by change based on date: %s' % seed_date)
            print_recommendation(final_recommendations, final_scores, typ=MN)
            print('=' * 80)
            print('Other recommendations by change based on date: %s' % seed_date)
            print_recommendation(final_recommendations, final_scores, typ=OTHERS)
            return (
             final_recommendations, final_scores)


def print_recommendation(recs, scores, typ=None):
    i = len(recs) + 1
    digits = len(str(len(recs)))
    for change, _old_score, _new_score, description, name in recs:
        i -= 1
        if typ:
            if typ == EV:
                if EV not in name:
                    continue
            if typ == MN:
                if MN not in name:
                    continue
                elif typ == OTHERS:
                    if not EV in name:
                        if MN in name:
                            continue
            best_score_change, best_description = scores[name]
            if description != best_description:
                pass
            else:
                print(('\t%0' + str(digits) + 'i %s => %.06f') % (i, description, change))


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Analyzes daily routine features to optimize your routine.')
    parser.add_argument('fn', help='Filename of ODS file containing data.')
    parser.add_argument('--only-attribute', default=None, help='If given, only predicts the effect of this one attribute. Otherwise looks at all attributes.')
    parser.add_argument('--stop-on-error', action='store_true', default=False, help='If given, halts at first error. Otherwise shows a warning and continues.')
    parser.add_argument('--no-train', action='store_true', default=False, help='If given, skips training and re-uses last trained classifier.')
    parser.add_argument('--score-field-name', default=None, help=('The name of the field containing the score to maximize. Default is "%s".' % DEFAULT_SCORE_FIELD_NAME))
    parser.add_argument('--all-classifiers', action='store_true', default=False, help='If given, trains all classifiers, even the crappy ones. Otherwise, only uses the known best.')
    parser.add_argument('--calculate-pcc', action='store_true', default=False, help='If given, calculates the Pearson correlation coefficient for all attributes.')
    parser.add_argument('--yes', default=None, action='store_true', help='Enables non-interactive mode and assumes yes for any interactive yes/no prompts.')
    args = parser.parse_args()
    o = Optimizer(**args.__dict__)
    o.analyze()