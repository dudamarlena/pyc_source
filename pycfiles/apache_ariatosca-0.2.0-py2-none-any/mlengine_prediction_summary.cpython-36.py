# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/utils/mlengine_prediction_summary.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 7019 bytes
__doc__ = 'A template called by DataFlowPythonOperator to summarize BatchPrediction.\n\nIt accepts a user function to calculate the metric(s) per instance in\nthe prediction results, then aggregates to output as a summary.\n\nArgs:\n  --prediction_path:\n      The GCS folder that contains BatchPrediction results, containing\n      prediction.results-NNNNN-of-NNNNN files in the json format.\n      Output will be also stored in this folder, as \'prediction.summary.json\'.\n\n  --metric_fn_encoded:\n      An encoded function that calculates and returns a tuple of metric(s)\n      for a given instance (as a dictionary). It should be encoded\n      via base64.b64encode(dill.dumps(fn, recurse=True)).\n\n  --metric_keys:\n      A comma-separated key(s) of the aggregated metric(s) in the summary\n      output. The order and the size of the keys must match to the output\n      of metric_fn.\n      The summary will have an additional key, \'count\', to represent the\n      total number of instances, so the keys shouldn\'t include \'count\'.\n\n# Usage example:\ndef get_metric_fn():\n    import math  # all imports must be outside of the function to be passed.\n    def metric_fn(inst):\n        label = float(inst["input_label"])\n        classes = float(inst["classes"])\n        prediction = float(inst["scores"][1])\n        log_loss = math.log(1 + math.exp(\n            -(label * 2 - 1) * math.log(prediction / (1 - prediction))))\n        squared_err = (classes-label)**2\n        return (log_loss, squared_err)\n    return metric_fn\nmetric_fn_encoded = base64.b64encode(dill.dumps(get_metric_fn(), recurse=True))\n\nairflow.contrib.operators.DataFlowPythonOperator(\n    task_id="summary-prediction",\n    py_options=["-m"],\n    py_file="airflow.contrib.operators.mlengine_prediction_summary",\n    options={\n        "prediction_path": prediction_path,\n        "metric_fn_encoded": metric_fn_encoded,\n        "metric_keys": "log_loss,mse"\n    },\n    dataflow_default_options={\n        "project": "xxx", "region": "us-east1",\n        "staging_location": "gs://yy", "temp_location": "gs://zz",\n    })\n    >> dag\n\n# When the input file is like the following:\n{"inputs": "1,x,y,z", "classes": 1, "scores": [0.1, 0.9]}\n{"inputs": "0,o,m,g", "classes": 0, "scores": [0.7, 0.3]}\n{"inputs": "1,o,m,w", "classes": 0, "scores": [0.6, 0.4]}\n{"inputs": "1,b,r,b", "classes": 1, "scores": [0.2, 0.8]}\n\n# The output file will be:\n{"log_loss": 0.43890510565304547, "count": 4, "mse": 0.25}\n\n# To test outside of the dag:\nsubprocess.check_call(["python",\n                       "-m",\n                       "airflow.contrib.operators.mlengine_prediction_summary",\n                       "--prediction_path=gs://...",\n                       "--metric_fn_encoded=" + metric_fn_encoded,\n                       "--metric_keys=log_loss,mse",\n                       "--runner=DataflowRunner",\n                       "--staging_location=gs://...",\n                       "--temp_location=gs://...",\n                       ])\n\n'
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import argparse, base64, json, os, apache_beam as beam, dill

class JsonCoder(object):

    @staticmethod
    def encode(x):
        return json.dumps(x)

    @staticmethod
    def decode(x):
        return json.loads(x)


@beam.ptransform_fn
def MakeSummary(pcoll, metric_fn, metric_keys):
    return pcoll | 'ApplyMetricFnPerInstance' >> beam.Map(metric_fn) | 'PairWith1' >> beam.Map(lambda tup: tup + (1, )) | 'SumTuple' >> beam.CombineGlobally((beam.combiners.TupleCombineFn)(*[sum] * (len(metric_keys) + 1))) | 'AverageAndMakeDict' >> beam.Map(lambda tup: dict([(name, tup[i] / tup[(-1)]) for i, name in enumerate(metric_keys)] + [
     (
      'count', tup[(-1)])]))


def run(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('--prediction_path',
      required=True, help="The GCS folder that contains BatchPrediction results, containing prediction.results-NNNNN-of-NNNNN files in the json format. Output will be also stored in this folder, as a file'prediction.summary.json'.")
    parser.add_argument('--metric_fn_encoded',
      required=True, help='An encoded function that calculates and returns a tuple of metric(s) for a given instance (as a dictionary). It should be encoded via base64.b64encode(dill.dumps(fn, recurse=True)).')
    parser.add_argument('--metric_keys',
      required=True, help="A comma-separated keys of the aggregated metric(s) in the summary output. The order and the size of the keys must match to the output of metric_fn. The summary will have an additional key, 'count', to represent the total number of instances, so this flag shouldn't include 'count'.")
    known_args, pipeline_args = parser.parse_known_args(argv)
    metric_fn = dill.loads(base64.b64decode(known_args.metric_fn_encoded))
    if not callable(metric_fn):
        raise ValueError('--metric_fn_encoded must be an encoded callable.')
    metric_keys = known_args.metric_keys.split(',')
    with beam.Pipeline(options=(beam.pipeline.PipelineOptions(pipeline_args))) as (p):
        _ = p | 'ReadPredictionResult' >> beam.io.ReadFromText((os.path.join(known_args.prediction_path, 'prediction.results-*-of-*')), coder=(JsonCoder())) | 'Summary' >> MakeSummary(metric_fn, metric_keys) | 'Write' >> beam.io.WriteToText((os.path.join(known_args.prediction_path, 'prediction.summary.json')),
          shard_name_template='',
          coder=(JsonCoder()))


if __name__ == '__main__':
    run()