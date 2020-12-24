# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nwinter/PycharmProjects/photon_projects/photon_core/photonai/investigator/app/main/controller/hyperpipe.py
# Compiled at: 2019-09-11 10:06:06
# Size of source mod 2**32: 8148 bytes
from flask import render_template
from ..main import application
from photonai.processing.results_structure import MDBHyperpipe
from photonai.processing.results_handler import ResultsHandler
from pymodm.errors import ValidationError, ConnectionError
from ..model.Metric import Metric
from ..model.BestConfigTrace import BestConfigTrace
from ..model.BestConfigPlot import BestConfigPlot
from ..model.PlotlyTrace import PlotlyTrace
from ..model.PlotlyPlot import PlotlyPlot
from .helper import load_pipe, load_available_pipes
from ..model.Figures import plotly_optimizer_history, plot_scatter, plotly_confusion_matrix

@application.route('/pipeline/<storage>')
def index_pipeline(storage):
    try:
        available_pipes = load_available_pipes()
        pipeline_list = list(MDBHyperpipe.objects.all())
        return render_template('pipeline/index.html', s=storage, pipelines=pipeline_list, available_pipes=available_pipes)
    except ValidationError as exc:
        return exc.message
    except ConnectionError as exc:
        return exc.message


@application.route('/error')
def show_error(msg):
    return render_template('default/error.html', error_msg=msg)


@application.route('/pipeline/<storage>/<name>')
def show_pipeline(storage, name):
    try:
        available_pipes = load_available_pipes()
        pipe = load_pipe(storage, name)
        handler = ResultsHandler(pipe)
        config_evaluations = handler.get_config_evaluations()
        min_config_evaluations = handler.get_minimum_config_evaluations()
        optimizer_history = plotly_optimizer_history('optimizer_history', config_evaluations, min_config_evaluations, pipe.hyperpipe_info.best_config_metric)
        data_info = pipe.hyperpipe_info.data
        optimizer_info = pipe.hyperpipe_info.optimization
        cross_validation_info = pipe.hyperpipe_info.cross_validation
        best_config_plot_list = list()
        overview_plot_train = PlotlyPlot('overview_plot_training', 'Training Performance', show_legend=False)
        overview_plot_test = PlotlyPlot('overview_plot_test', 'Test Performance', show_legend=False)
        true_and_pred_val = list()
        true_and_pred_train = list()
        for fold in pipe.outer_folds:
            true_and_pred_val.append([fold.best_config.best_config_score.validation.y_true,
             fold.best_config.best_config_score.validation.y_pred])
            true_and_pred_train.append([fold.best_config.best_config_score.training.y_true,
             fold.best_config.best_config_score.training.y_pred])

        if pipe.hyperpipe_info.estimation_type == 'regressor':
            predictions_plot_train = plot_scatter(true_and_pred_train, 'predictions_plot_train', 'True/Pred Training')
            predictions_plot_test = plot_scatter(true_and_pred_val, 'predictions_plot_test', 'True/Pred Test')
        else:
            predictions_plot_train = plotly_confusion_matrix('predictions_plot_train', 'Confusion Matrix Training', true_and_pred_train)
            predictions_plot_test = plotly_confusion_matrix('predictions_plot_test', 'Confusion Matrix Test', true_and_pred_val)
        for fold in pipe.outer_folds:
            overview_plot_training_trace = PlotlyTrace(('fold_' + str(fold.fold_nr) + '_training'), trace_color='rgb(91, 91, 91)')
            overview_plot_test_trace = PlotlyTrace(('fold_' + str(fold.fold_nr) + '_test'), trace_color='rgb(91, 91, 91)')
            if fold.best_config:
                metric_training_list = list()
                metric_validation_list = list()
                for key, value in fold.best_config.best_config_score.training.metrics.items():
                    overview_plot_training_trace.add_x(key)
                    overview_plot_training_trace.add_y(value)
                    metric = Metric(key, value)
                    metric_training_list.append(metric)

                for key, value in fold.best_config.best_config_score.validation.metrics.items():
                    overview_plot_test_trace.add_x(key)
                    overview_plot_test_trace.add_y(value)
                    metric = Metric(key, value)
                    metric_validation_list.append(metric)

            overview_plot_train.add_trace(overview_plot_training_trace)
            overview_plot_test.add_trace(overview_plot_test_trace)
            metric_training_trace = BestConfigTrace('training', metric_training_list, '', 'bar')
            metric_test_trace = BestConfigTrace('test', metric_validation_list, '', 'bar')
            best_config_plot = BestConfigPlot('outer_fold_' + str(fold.fold_nr) + '_best_config_overview', 'Best Performance Outer Fold ' + str(fold.fold_nr), metric_training_trace, metric_test_trace)
            best_config_plot_list.append(best_config_plot)

        training_mean_trace = PlotlyTrace('mean', trace_size=8, trace_color='rgb(31, 119, 180)')
        test_mean_trace = PlotlyTrace('mean', trace_size=8, trace_color='rgb(214, 123, 25)')
        for metric in pipe.metrics_train:
            if metric.operation == 'FoldOperations.MEAN':
                training_mean_trace.add_x(metric.metric_name)
                training_mean_trace.add_y(metric.value)

        for metric in pipe.metrics_test:
            if metric.operation == 'FoldOperations.MEAN':
                test_mean_trace.add_x(metric.metric_name)
                test_mean_trace.add_y(metric.value)

        overview_plot_train.add_trace(training_mean_trace)
        overview_plot_test.add_trace(test_mean_trace)
        return render_template('outer_folds/index.html', pipe=pipe, best_config_plot_list=best_config_plot_list, overview_plot_train=overview_plot_train,
          overview_plot_test=overview_plot_test,
          predictions_plot_train=predictions_plot_train,
          predictions_plot_test=predictions_plot_test,
          optimizer_history=optimizer_history,
          s=storage,
          available_pipes=available_pipes,
          cross_validation_info=cross_validation_info,
          data_info=data_info,
          optimizer_info=optimizer_info)
    except ValidationError as exc:
        return exc.message
    except ConnectionError as exc:
        return exc.message