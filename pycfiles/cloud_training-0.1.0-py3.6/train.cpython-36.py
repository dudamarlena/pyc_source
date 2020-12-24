# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\cloud_training\commands\train.py
# Compiled at: 2017-10-30 16:56:13
# Size of source mod 2**32: 6070 bytes
import base64, os, time
from datetime import datetime
from cloud_training import utils
from cloud_training.project_command import ProjectCommand

class TrainCommand(ProjectCommand):

    def run(self):
        train_script_path = os.path.join(self._project_dir, self._project_config['package_name'], 'models', self._model, 'train.py')
        if not os.path.exists(train_script_path):
            self._print('The train script "%s" was not found.' % train_script_path)
            return False
        instance_type = self._args.instance_type if self._args.instance_type else self._settings['instance_type']
        prices = self._aws.spot_price(instance_type)
        if not prices:
            self._print("Can't get spot instance prices")
            return False
        min_price = float(min(prices.values()))
        max_price = min_price * 1.25
        self._print('Spot instance price for "%s" is %.03f' % (instance_type, min_price))
        user_price = input('Set your max price [default: %.03f]: ' % max_price)
        if user_price:
            max_price = float(user_price)
        self._print('Compressing files in the data directory...')
        data_dir = os.path.join(self._project_dir, 'data')
        utils.zip_dir(data_dir)
        session_id = self._args.session
        if not session_id:
            session_id = datetime.today().strftime('%y%m%d_%H%M')
        self._print('Syncing the project with S3...')
        exclude = [os.path.join(self._project_dir, '*')]
        include = [os.path.join(data_dir, '*.zip'),
         os.path.join(self._project_dir, self._project_config['package_name'], '*'),
         os.path.join(self._project_dir, 'training', self._model, session_id, '*')]
        self._aws.s3_sync(self._project_dir, self._s3_project_dir, exclude, include)
        with open(utils.data_dir('user_data.sh')) as (f):
            user_data = f.read()
        with open(utils.data_dir('unzip.py')) as (f):
            unzip_script_base64 = base64.b64encode(f.read().encode()).decode()
        user_data_replacements = {'aws_access_key_id':self._settings['aws_access_key_id'], 
         'aws_secret_access_key':self._settings['aws_secret_access_key'], 
         'aws_region':self._settings['region'], 
         'project_name':self._project_config['project_name'], 
         'package_name':self._project_config['package_name'], 
         's3_project_dir':self._s3_project_dir, 
         'model_name':self._model, 
         'session_id':session_id, 
         'conda_env':self._args.conda_env if self._args.conda_env else '', 
         'unzip_script_base64':unzip_script_base64}
        for key in user_data_replacements:
            user_data = user_data.replace('{{' + key + '}}', user_data_replacements[key])

        request = self._aws.create_spot_request(instance_type, self._settings['image_id'], self._settings['root_snapshot_id'], int(self._settings['root_volume_size']), int(self._settings['training_volume_size']), user_data, self._settings['key_name'], max_price)
        if not request:
            self._print("Can't create a spot instance request")
            return False
        request_id = request['SpotInstanceRequestId']
        request_status = request['Status']['Code']
        if request_status != 'pending-evaluation':
            self._print('Request is failed (status=%s). Message: %s' % (request_status, request['Status']['Message']))
            self._cancel_request(request_id)
            return False
        else:
            self._print('Waiting for the "active" status for the request...')
            waiting_statuses = {
             'pending-evaluation', 'pending-fulfillment'}
            while request_status in waiting_statuses:
                request = self._aws.get_spot_request(request_id)
                request_status = request['Status']['Code']
                time.sleep(3)

            if request_status != 'fulfilled':
                self._print('Request is failed (status=%s). Message: %s' % (request_status, request['Status']['Message']))
                self._cancel_request(request_id)
                return False
            self._aws.create_tag([request['InstanceId'], request_id], 'model', '%s-%s' % (self._project_config['project_name'], self._model))
            instance = self._aws.get_instance_by_id(request['InstanceId'])
            self._print('IP address of the instance: ' + instance['PublicIpAddress'])
            self._print('Use "cloud-training --model %s sync-session --session %s" command to get the trained model' % (
             self._model, session_id))
            return True

    def _cancel_request(self, request_id):
        """Cancel the spot request if it was failed for some reason.

        For example, if the requested price is lower than the minimum required price,
        instance will not be run, but the request will be still open. If the minimum required
        price will become lower than the requested one, the instance will be run, but
        you may not notice it.
        """
        cancelled = self._aws.cancel_spot_request(request_id)
        if not cancelled:
            self._print('[WARNING] Request "%s" can\'t be cancelled! Please make sure that it was closed.' % request_id)