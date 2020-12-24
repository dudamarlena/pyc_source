# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/qoaladep/gcp/ml_engine/train_model.py
# Compiled at: 2020-03-10 06:22:57
# Size of source mod 2**32: 3560 bytes
from googleapiclient import discovery

def deploy(project_id, model_name, engine_type, package_url, python_module, region, output_url, runtime_version, python_version, running_time, engine_type_spec=None):
    """[Function for model training to ml engine]
    
    Arguments:
        project_id {[string]} -- [Project ID of model]
        model_name {[string]} -- [Model name : must be unique within the AI Platform Prediction model.]
        engine_type {[string]} -- [Type of engine for training the model , ref: https://cloud.google.com/ai-platform/training/docs/machine-types]
        package_url {[string]} -- [A packaged training application that is staged in a Cloud Storage location, ref for creating package : https://cloud.google.com/ai-platform/training/docs/packaging-trainer]
        python_module {[string]} -- [The name of the main module in your package]
        region {[string]} -- [The Compute Engine region where you want your job to run]
        output_url {[string]} -- [The path to a Cloud Storage location to use for job output]
        runtime_version {[string]} -- [The AI Platform Training runtime version to use for the job, ref: https://cloud.google.com/ai-platform/training/docs/runtime-version-list]
        python_version {[string]} -- [The Python version to use for the job]
        running_time {[string]} -- [A maximum duration in seconds with the suffix s (for example, 7200s) for your training job]
        engine_type_spec {[dict]} -- [Detail specification of engine type] Default : None

    Arguments:
        model_path {str} -- model path, example: gs://ml_models/recommendation/a1/
        new_version_name {str} -- the new version name
        model_name {str} -- the model name
    """
    status = True
    try:
        training_inputs = {}
        if engine_type == 'CUSTOM':
            training_inputs['scaleTier'] = engine_type
            training_inputs['masterType'] = engine_type_spec['masterType']
            training_inputs['workerType'] = engine_type_spec['workerType']
            training_inputs['parameterServerType'] = engine_type_spec['parameterServerType']
            training_inputs['workerCount'] = engine_type_spec['workerCount']
            training_inputs['parameterServerCount'] = engine_type_spec['parameterServerCount']
        else:
            if engine_type == 'BASIC':
                training_inputs['scaleTier'] = engine_type
            else:
                if engine_type == 'STANDARD_1':
                    training_inputs['scaleTier'] = engine_type
                else:
                    if engine_type == 'PREMIUM_1':
                        training_inputs['scaleTier'] = engine_type
                    else:
                        if engine_type == 'BASIC_GPU':
                            training_inputs['scaleTier'] = engine_type
                        else:
                            if engine_type == 'BASIC_TPU':
                                training_inputs['scaleTier'] = engine_type
        training_inputs = {'packageUris':[
          package_url], 
         'pythonModule':python_module, 
         'region':region, 
         'jobDir':output_url, 
         'runtimeVersion':runtime_version, 
         'pythonVersion':python_version, 
         'scheduling':{'maxRunningTime': running_time}}
        job_spec = {'jobId':str(model_name), 
         'trainingInput':training_inputs}
        project_id = 'projects/{}'.format(project_id)
        cloudml = discovery.build('ml', 'v1')
        request = cloudml.projects().jobs().create(body=job_spec, parent=project_id)
        response = request.execute()
    except errors.HttpError as err:
        try:
            status = False
            response = str(err._get_reason())
        finally:
            err = None
            del err

    return (
     response, status)