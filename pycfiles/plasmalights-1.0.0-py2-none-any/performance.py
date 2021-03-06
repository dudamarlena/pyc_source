# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/plasma/utils/performance.py
# Compiled at: 2017-02-17 21:50:27
import matplotlib.pyplot as plt, os
from pprint import pprint
import numpy as np
from plasma.preprocessor.normalize import VarNormalizer as Normalizer
from plasma.conf import conf

class PerformanceAnalyzer:

    def __init__(self, results_dir=None, shots_dir=None, i=0, T_min_warn=0, T_max_warn=1000, verbose=False, pred_ttd=False, conf=None):
        self.T_min_warn = T_min_warn
        self.T_max_warn = T_max_warn
        self.verbose = verbose
        self.results_dir = results_dir
        self.shots_dir = shots_dir
        self.i = i
        self.pred_ttd = pred_ttd
        self.conf = conf
        self.pred_train = None
        self.truth_train = None
        self.disruptive_train = None
        self.shot_list_train = None
        self.pred_test = None
        self.truth_test = None
        self.disruptive_test = None
        self.shot_list_test = None
        self.normalizer = None
        return

    def get_metrics_vs_p_thresh(self, mode):
        if mode == 'train':
            all_preds = self.pred_train
            all_truths = self.truth_train
            all_disruptive = self.disruptive_train
        elif mode == 'test':
            all_preds = self.pred_test
            all_truths = self.truth_test
            all_disruptive = self.disruptive_test
        return self.get_metrics_vs_p_thresh_custom(all_preds, all_truths, all_disruptive)

    def get_p_thresh_range(self):
        return self.conf['data']['target'].threshold_range(self.conf['data']['T_warning'])

    def get_metrics_vs_p_thresh_custom(self, all_preds, all_truths, all_disruptive):
        P_thresh_range = self.get_p_thresh_range()
        correct_range = np.zeros_like(P_thresh_range)
        accuracy_range = np.zeros_like(P_thresh_range)
        fp_range = np.zeros_like(P_thresh_range)
        missed_range = np.zeros_like(P_thresh_range)
        early_alarm_range = np.zeros_like(P_thresh_range)
        for i, P_thresh in enumerate(P_thresh_range):
            correct, accuracy, fp_rate, missed, early_alarm_rate = self.summarize_shot_prediction_stats(P_thresh, all_preds, all_truths, all_disruptive)
            correct_range[i] = correct
            accuracy_range[i] = accuracy
            fp_range[i] = fp_rate
            missed_range[i] = missed
            early_alarm_range[i] = early_alarm_rate

        return (
         correct_range, accuracy_range, fp_range, missed_range, early_alarm_range)

    def summarize_shot_prediction_stats_by_mode(self, P_thresh, mode, verbose=False):
        if mode == 'train':
            all_preds = self.pred_train
            all_truths = self.truth_train
            all_disruptive = self.disruptive_train
        elif mode == 'test':
            all_preds = self.pred_test
            all_truths = self.truth_test
            all_disruptive = self.disruptive_test
        return self.summarize_shot_prediction_stats(P_thresh, all_preds, all_truths, all_disruptive, verbose)

    def summarize_shot_prediction_stats(self, P_thresh, all_preds, all_truths, all_disruptive, verbose=False):
        TPs, FPs, FNs, TNs, earlies, lates = (0, 0, 0, 0, 0, 0)
        for i in range(len(all_preds)):
            preds = all_preds[i]
            truth = all_truths[i]
            is_disruptive = all_disruptive[i]
            TP, FP, FN, TN, early, late = self.get_shot_prediction_stats(P_thresh, preds, truth, is_disruptive)
            TPs += TP
            FPs += FP
            FNs += FN
            TNs += TN
            earlies += early
            lates += late

        disr = earlies + lates + TPs + FNs
        nondisr = FPs + TNs
        if verbose:
            print ('total: {}, tp: {} fp: {} fn: {} tn: {} early: {} late: {} disr: {} nondisr: {}').format(len(all_preds), TPs, FPs, FNs, TNs, earlies, lates, disr, nondisr)
        return self.get_accuracy_and_fp_rate_from_stats(TPs, FPs, FNs, TNs, earlies, lates, verbose)

    def get_shot_prediction_stats(self, P_thresh, pred, truth, is_disruptive):
        if self.pred_ttd:
            predictions = pred < P_thresh
        else:
            predictions = pred > P_thresh
        predictions = np.reshape(predictions, (len(predictions),))
        max_acceptable = self.create_acceptable_region(truth, 'max')
        min_acceptable = self.create_acceptable_region(truth, 'min')
        early = late = TP = TN = FN = FP = 0
        positives = self.get_positives(predictions)
        if len(positives) == 0:
            if is_disruptive:
                FN = 1
            else:
                TN = 1
        elif is_disruptive:
            first_pred_idx = positives[0]
            if max_acceptable[first_pred_idx] and ~min_acceptable[first_pred_idx]:
                TP = 1
            elif min_acceptable[first_pred_idx]:
                late = 1
            elif ~max_acceptable[first_pred_idx]:
                early = 1
        else:
            FP = 1
        return (TP, FP, FN, TN, early, late)

    def get_positives(self, predictions):
        indices = np.arange(len(predictions))
        return np.where(np.logical_and(predictions, indices >= 100))[0]

    def create_acceptable_region(self, truth, mode):
        if mode == 'min':
            acceptable_timesteps = self.T_min_warn
        elif mode == 'max':
            acceptable_timesteps = self.T_max_warn
        else:
            print 'Error Invalid Mode for acceptable region'
            exit(1)
        acceptable = np.zeros_like(truth, dtype=bool)
        if acceptable_timesteps > 0:
            acceptable[(-acceptable_timesteps):] = True
        return acceptable

    def get_accuracy_and_fp_rate_from_stats(self, tp, fp, fn, tn, early, late, verbose=False):
        total = tp + fp + fn + tn + early + late
        disr = early + late + tp + fn
        nondisr = fp + tn
        if disr == 0:
            early_alarm_rate = 0
            missed = 0
            accuracy = 0
        else:
            early_alarm_rate = 1.0 * early / disr
            missed = 1.0 * (late + fn) / disr
            accuracy = 1.0 * tp / disr
        if nondisr == 0:
            fp_rate = 0
        else:
            fp_rate = 1.0 * fp / nondisr
        correct = 1.0 * (tp + tn) / total
        if verbose:
            print ('accuracy: {}').format(accuracy)
            print ('missed: {}').format(missed)
            print ('early alarms: {}').format(early_alarm_rate)
            print ('false positive rate: {}').format(fp_rate)
            print ('correct: {}').format(correct)
        return (
         correct, accuracy, fp_rate, missed, early_alarm_rate)

    def load_ith_file(self):
        results_files = os.listdir(self.results_dir)
        print results_files
        dat = np.load(self.results_dir + results_files[self.i])
        if self.verbose:
            print ('configuration: {} ').format(dat['conf'])
        self.pred_train = dat['y_prime_train']
        self.truth_train = dat['y_gold_train']
        self.disruptive_train = dat['disruptive_train']
        self.pred_test = dat['y_prime_test']
        self.truth_test = dat['y_gold_test']
        self.disruptive_test = dat['disruptive_test']
        self.shot_list_test = dat['shot_list_test'][()]
        self.shot_list_train = dat['shot_list_train'][()]
        self.conf = dat['conf'][()]
        for mode in ['test', 'train']:
            print ('{}: loaded {} shot ({}) disruptive').format(mode, self.get_num_shots(mode), self.get_num_disruptive_shots(mode))

        self.print_conf()

    def print_conf(self):
        pprint(self.conf)

    def get_num_shots(self, mode):
        if mode == 'test':
            return len(self.disruptive_test)
        if mode == 'train':
            return len(self.disruptive_train)

    def get_num_disruptive_shots(self, mode):
        if mode == 'test':
            return sum(self.disruptive_test)
        if mode == 'train':
            return sum(self.disruptive_train)

    def hist_alarms(self, alarms, title_str='alarms', save_figure=False):
        T_min_warn = self.T_min_warn
        T_max_warn = self.T_max_warn
        if len(alarms) > 0:
            alarms = alarms / 1000.0
            alarms = np.sort(alarms)
            T_min_warn /= 1000.0
            T_max_warn /= 1000.0
            plt.figure()
            alarms += 0.0001
            bins = np.logspace(np.log10(min(alarms)), np.log10(max(alarms)), 40)
            plt.step(np.concatenate((alarms[::-1], alarms[[0]])), 1.0 * np.arange(alarms.size + 1) / alarms.size)
            plt.gca().set_xscale('log')
            plt.axvline(T_min_warn, color='r')
            plt.axvline(T_max_warn, color='r')
            plt.xlabel('TTD [s]')
            plt.ylabel('Accumulated fraction of detected disruptions')
            plt.xlim([0.0001, max(alarms) * 10])
            plt.ylim([0, 1])
            plt.grid()
            plt.title(title_str)
            plt.show()
        if save_figure:
            plt.savefig('accum_disruptions.png', bbox_inches='tight')
        else:
            print title_str + ': No alarms!'

    def gather_first_alarms(self, P_thresh, mode):
        if mode == 'train':
            pred_list = self.pred_train
            disruptive_list = self.disruptive_train
        else:
            if mode == 'test':
                pred_list = self.pred_test
                disruptive_list = self.disruptive_test
            alarms = []
            disr_alarms = []
            nondisr_alarms = []
            for i in range(len(pred_list)):
                pred = pred_list[i]
                if self.pred_ttd:
                    predictions = pred < P_thresh
                else:
                    predictions = pred > P_thresh
                predictions = np.reshape(predictions, (len(predictions),))
                positives = self.get_positives(predictions)
                if len(positives) > 0:
                    alarm_ttd = len(pred) - 1.0 - positives[0]
                    alarms.append(alarm_ttd)
                    if disruptive_list[i]:
                        disr_alarms.append(alarm_ttd)
                    else:
                        nondisr_alarms.append(alarm_ttd)
                elif disruptive_list[i]:
                    disr_alarms.append(-1)

        return (
         np.array(alarms), np.array(disr_alarms), np.array(nondisr_alarms))

    def compute_tradeoffs_and_print(self, mode):
        P_thresh_range = self.get_p_thresh_range()
        correct_range, accuracy_range, fp_range, missed_range, early_alarm_range = self.get_metrics_vs_p_thresh(mode)
        fp_threshs = [0.01, 0.05, 0.1]
        missed_threshs = [0.01, 0.05, 0.0]
        for fp_thresh in fp_threshs:
            print ('============= FP RATE < {} =============').format(fp_thresh)
            if any(fp_range < fp_thresh):
                idx = np.where(fp_range <= fp_thresh)[0][0]
                P_thresh_opt = P_thresh_range[idx]
                self.summarize_shot_prediction_stats_by_mode(P_thresh_opt, mode, verbose=True)
                print ('============= AT P_THRESH = {} =============').format(P_thresh_opt)
            else:
                print 'No such P_thresh found'
            print ''

        for missed_thresh in missed_threshs:
            print ('============= MISSED RATE < {} =============').format(missed_thresh)
            if any(missed_range < missed_thresh):
                idx = np.where(missed_range <= missed_thresh)[0][(-1)]
                P_thresh_opt = P_thresh_range[idx]
                self.summarize_shot_prediction_stats_by_mode(P_thresh_opt, mode, verbose=True)
                print ('============= AT P_THRESH = {} =============').format(P_thresh_opt)
            else:
                print 'No such P_thresh found'
            print ''

        print '============== Crossing Point: =============='
        print '============= TEST PERFORMANCE: ============='
        idx = np.where(missed_range <= fp_range)[0][(-1)]
        P_thresh_opt = P_thresh_range[idx]
        self.summarize_shot_prediction_stats_by_mode(P_thresh_opt, mode, verbose=True)
        P_thresh_ret = P_thresh_opt
        return P_thresh_ret

    def compute_tradeoffs_and_print_from_training(self):
        P_thresh_range = self.get_p_thresh_range()
        correct_range, accuracy_range, fp_range, missed_range, early_alarm_range = self.get_metrics_vs_p_thresh('train')
        fp_threshs = [
         0.01, 0.05, 0.1]
        missed_threshs = [0.01, 0.05, 0.0]
        P_thresh_default = 0.03
        P_thresh_ret = P_thresh_default
        first_idx = 0 if not self.pred_ttd else -1
        last_idx = -1 if not self.pred_ttd else 0
        for fp_thresh in fp_threshs:
            print ('============= TRAINING FP RATE < {} =============').format(fp_thresh)
            print '============= TEST PERFORMANCE: ============='
            if any(fp_range < fp_thresh):
                idx = np.where(fp_range <= fp_thresh)[0][first_idx]
                P_thresh_opt = P_thresh_range[idx]
                self.summarize_shot_prediction_stats_by_mode(P_thresh_opt, 'test', verbose=True)
                print ('============= AT P_THRESH = {} =============').format(P_thresh_opt)
            else:
                print 'No such P_thresh found'
            P_thresh_opt = P_thresh_default
            print ''

        for missed_thresh in missed_threshs:
            print ('============= TRAINING MISSED RATE < {} =============').format(missed_thresh)
            print '============= TEST PERFORMANCE: ============='
            if any(missed_range < missed_thresh):
                idx = np.where(missed_range <= missed_thresh)[0][last_idx]
                P_thresh_opt = P_thresh_range[idx]
                self.summarize_shot_prediction_stats_by_mode(P_thresh_opt, 'test', verbose=True)
                if missed_thresh == 0.05:
                    P_thresh_ret = P_thresh_opt
                print ('============= AT P_THRESH = {} =============').format(P_thresh_opt)
            else:
                print 'No such P_thresh found'
            P_thresh_opt = P_thresh_default
            print ''

        print '============== Crossing Point: =============='
        print '============= TEST PERFORMANCE: ============='
        if any(missed_range <= fp_range):
            idx = np.where(missed_range <= fp_range)[0][last_idx]
            P_thresh_opt = P_thresh_range[idx]
            self.summarize_shot_prediction_stats_by_mode(P_thresh_opt, 'test', verbose=True)
            P_thresh_ret = P_thresh_opt
            print ('============= AT P_THRESH = {} =============').format(P_thresh_opt)
        else:
            print 'No such P_thresh found'
        return P_thresh_ret

    def compute_tradeoffs_and_plot(self, mode, save_figure=True, plot_string=''):
        correct_range, accuracy_range, fp_range, missed_range, early_alarm_range = self.get_metrics_vs_p_thresh(mode)
        self.tradeoff_plot(accuracy_range, missed_range, fp_range, early_alarm_range, save_figure=save_figure, plot_string=plot_string)

    def get_prediction_type(self, TP, FP, FN, TN, early, late):
        if TP:
            return 'TP'
        if FP:
            return 'FP'
        if FN:
            return 'FN'
        if TN:
            return 'TN'
        if early:
            return 'early'
        if late:
            return 'late'

    def example_plots(self, P_thresh_opt, mode='test', types_to_plot=['FP'], max_plot=5, normalize=True, plot_signals=True):
        if mode == 'test':
            pred = self.pred_test
            truth = self.truth_test
            is_disruptive = self.disruptive_test
            shot_list = self.shot_list_test
        else:
            pred = self.pred_train
            truth = self.truth_train
            is_disruptive = self.disruptive_train
            shot_list = self.shot_list_train
        plotted = 0
        iterate_arr = np.arange(len(truth))
        np.random.shuffle(iterate_arr)
        for i in iterate_arr:
            t = truth[i]
            p = pred[i]
            is_disr = is_disruptive[i]
            shot = shot_list.shots[i]
            TP, FP, FN, TN, early, late = self.get_shot_prediction_stats(P_thresh_opt, p, t, is_disr)
            prediction_type = self.get_prediction_type(TP, FP, FN, TN, early, late)
            if not all(_ in set(['FP', 'TP', 'FN', 'TN', 'late', 'early', 'any']) for _ in types_to_plot):
                print 'warning, unkown types_to_plot'
                return
            if ('any' in types_to_plot or prediction_type in types_to_plot) and plotted < max_plot:
                if plot_signals:
                    self.plot_shot(shot, True, normalize, t, p, P_thresh_opt, prediction_type)
                else:
                    plt.figure()
                    plt.semilogy((t + 0.001)[::-1], label='ground truth')
                    plt.plot(p[::-1], 'g', label='neural net prediction')
                    plt.axvline(self.T_min_warn, color='r', label='max warning time')
                    plt.axvline(self.T_max_warn, color='r', label='min warning time')
                    plt.axhline(P_thresh_opt, color='k', label='trigger threshold')
                    plt.xlabel('TTD [ms]')
                    plt.legend(loc=(1.0, 0.6))
                    plt.ylim([1e-07, 1.1])
                    plt.grid()
                    plt.savefig(('fig_{}.png').format(shot.number), bbox_inches='tight')
                plotted += 1

    def plot_shot(self, shot, save_fig=True, normalize=True, truth=None, prediction=None, P_thresh_opt=None, prediction_type=''):
        if self.normalizer is None and normalize:
            nn = Normalizer(self.conf)
            nn.train()
            self.normalizer = nn
        if shot.previously_saved(self.shots_dir):
            shot.restore(self.shots_dir)
            t_disrupt = shot.t_disrupt
            is_disruptive = shot.is_disruptive
            if normalize:
                self.normalizer.apply(shot)
            signals = np.empty((len(shot.signals), 0))
            labels = []
            signals_index = 0
            signals_masks = conf['paths']['signals_masks']
            plot_masks = conf['plots']['plot_masks']
            group_labels = conf['plots']['group_labels']
            for i, group in enumerate(conf['paths']['signals_dirs']):
                for j, signal_name in enumerate(group):
                    if signals_masks[i][j]:
                        if plot_masks[i][j]:
                            labels += group_labels[i]
                            signals = np.column_stack((signals, shot.signals.T[signals_index]))
                        signals_index += 1

            if is_disruptive:
                print 'disruptive'
            else:
                print 'non disruptive'
            f, axarr = subplots(len(signals.T) + 1, 1, sharex=True, figsize=(13, 13))
            title(prediction_type)
            for i, sig in enumerate(signals.T):
                ax = axarr[i]
                ax.plot(sig[::-1], label=labels[i])
                ax.legend(loc='best', fontsize=8)
                setp(ax.get_xticklabels(), visible=False)
                setp(ax.get_yticklabels(), fontsize=7)
                f.subplots_adjust(hspace=0)
                print ('min: {}, max: {}').format(min(sig), max(sig))

            ax = axarr[(-1)]
            if self.pred_ttd:
                ax.semilogy((-truth + 0.0001)[::-1], label='ground truth')
                ax.plot(-prediction[::-1] + 0.0001, 'g', label='neural net prediction')
                ax.axhline(-P_thresh_opt, color='k', label='trigger threshold')
            else:
                ax.plot((truth + 0.001)[::-1], label='ground truth')
                ax.plot(prediction[::-1], 'g', label='neural net prediction')
                ax.axhline(P_thresh_opt, color='k', label='trigger threshold')
            ax.set_ylim([-2, 2])
            ax.axvline(self.T_min_warn, color='r', label='max warning time')
            ax.axvline(self.T_max_warn, color='r', label='min warning time')
            ax.set_xlabel('TTD [ms]')
            ax.legend(loc='best', fontsize=10)
            plt.setp(ax.get_yticklabels(), fontsize=7)
            if save_fig:
                plt.savefig(('sig_fig_{}.png').format(shot.number), bbox_inches='tight')
        else:
            print "Shot hasn't been processed"
        return

    def tradeoff_plot(self, accuracy_range, missed_range, fp_range, early_alarm_range, save_figure=False, plot_string=''):
        plt.figure()
        P_thresh_range = self.get_p_thresh_range()
        if self.pred_ttd:
            plt.semilogx(abs(P_thresh_range[::-1]), missed_range, 'r', label='missed')
            plt.plot(abs(P_thresh_range[::-1]), fp_range, 'k', label='false positives')
        else:
            plt.plot(P_thresh_range, missed_range, 'r', label='missed')
            plt.plot(P_thresh_range, fp_range, 'k', label='false positives')
        plt.legend(loc=(1.0, 0.6))
        plt.xlabel('Alarm threshold')
        plt.grid()
        title_str = ('metrics{}').format(plot_string)
        plt.title(title_str)
        if save_figure:
            plt.savefig(title_str + '.png', bbox_inches='tight')
        plt.close('all')
        plt.plot(fp_range, 1 - missed_range, 'o-b')
        ax = plt.gca()
        plt.xlabel('FP rate')
        plt.ylabel('TP rate')
        major_ticks = np.arange(0, 1.01, 0.2)
        minor_ticks = np.arange(0, 1.01, 0.05)
        ax.set_xticks(major_ticks)
        ax.set_yticks(major_ticks)
        ax.set_xticks(minor_ticks, minor=True)
        ax.set_yticks(minor_ticks, minor=True)
        ax.grid(which='both')
        ax.grid(which='major', alpha=0.5)
        ax.grid(which='minor', alpha=0.3)
        plt.xlim([0, 1])
        plt.ylim([0, 1])
        if save_figure:
            plt.savefig(title_str + '_roc.png', bbox_inches='tight')
        print ('ROC area ({}) is {}').format(plot_string, self.roc_from_missed_fp(missed_range, fp_range))

    def get_roc_area(self, all_preds, all_truths, all_disruptive):
        correct_range, accuracy_range, fp_range, missed_range, early_alarm_range = self.get_metrics_vs_p_thresh_custom(all_preds, all_truths, all_disruptive)
        return self.roc_from_missed_fp(missed_range, fp_range)

    def roc_from_missed_fp(self, missed_range, fp_range):
        return -np.trapz(1 - missed_range, x=fp_range)