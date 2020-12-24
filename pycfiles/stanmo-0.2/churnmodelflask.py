# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\qduan\Stanmo\git\bitbucket\src\stanmo_proj\stanmo\spec\churn\churnmodelflask.py
# Compiled at: 2015-12-22 12:08:42
from flask import Flask, jsonify
from flask import render_template
import os, simplejson
from flask import abort
from flask import request

class ChurnModelFlask:

    def __init__(self, port=None, to_execute=None, the_model=None):
        self.port = port
        self.to_execute = to_execute
        self.the_model = the_model

    def run(self):
        SPEC_INSTALL_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), 'web'))
        app = Flask(__name__, template_folder=os.path.join(SPEC_INSTALL_PATH, 'templates'), static_folder=os.path.join(SPEC_INSTALL_PATH, 'static'))

        @app.route('/')
        def index():
            return render_template('index.html')

        @app.route('/get_input_attribute_names')
        def get_input_attribute_names():
            attr_list = [
             '_state_code', '_tenure_days', '_customer_id']
            return simplejson.dumps(attr_list)

        @app.route('/get_churners')
        def get_churners():
            with open('C:\\qduan\\Stanmo\\flask\\flask\\churn_dashboard\\static\\json\\churners1.json') as (f):
                json_projects = simplejson.load(f)
            return simplejson.dumps(json_projects)

        @app.route('/get_cumulative_gain_data')
        def get_cumulative_gain_data():
            chart_data = self.the_model.get_roc_curve_all(model_name=self.the_model.model_name)
            return simplejson.dumps(chart_data)

        @app.route('/get_prediction_history')
        def get_prediction_history():
            pred_df1 = self.the_model.get_daily_prediction_count(model_name=self.the_model.model_name)
            pred_df = pred_df1.astype(float)
            print 'prediciton begin.'
            adata = {'labels': pred_df.index.tolist(), 
               'datasets': [
                          {'label': 'My Second dataset', 
                             'fillColor': 'rgba(151,187,205,0)', 
                             'strokeColor': 'rgba(151,187,205,1)', 
                             'pointColor': 'rgba(151,187,205,1)', 
                             'pointStrokeColor': '#fff', 
                             'pointHighlightFill': '#fff', 
                             'pointHighlightStroke': 'rgba(151,187,205,1)', 
                             'data': pred_df.tolist()}]}
            return simplejson.dumps(adata)

        @app.route('/get_overall_statistics')
        def get_overall_statistics():
            print 'get for model : ' + self.the_model.model_name
            overall_stat = self.the_model.get_overall_statistics(model_name=self.the_model.model_name)
            adata = {'model_storage_path': self.the_model.stanmoapp.get_model_spec_path(self.the_model.model_name), 
               'number_of_model_instances': len(self.the_model.model_instances), 
               'number_of_predictions': overall_stat['total_prediction_count'], 
               'number_of_feedbacks': overall_stat['total_feedback_count'], 
               'input_attributes': [
                                  'column1', 'column2', 'column 3', 'col3', 'col5'], 
               'output_attributes': [
                                   'column11', 'column12', 'column1 3', 'col13', 'co1l5', 'column11', 'column12', 'column1 3', 'col13', 'co1l5'], 
               'overall_precision': overall_stat['total_precision']}
            print simplejson.dumps(adata)
            return simplejson.dumps(adata)

        @app.route('/set_feedback_json', methods=['POST'])
        def set_feedback_json():
            if not request.json:
                abort(400)
            feedback_json = request.json
            predict_result = self.the_model.set_feedback_json(model_name=self.the_model.model_name, feedback_json=feedback_json)
            return simplejson.dumps({'status': 'ok'})

        @app.route('/predict_json', methods=['POST'])
        def predict_json():
            if not request.json:
                abort(400)
            json_customers = request.json
            new_json_customers = []
            for customer in json_customers:
                new_customer = self.the_model.create_default_record()
                for customer_attr in customer.keys():
                    new_customer[customer_attr] = customer[customer_attr]

                new_json_customers.append(new_customer)

            predict_result = self.the_model.predict_json(new_json_customers)
            return predict_result

        if self.to_execute:
            app.run(host='0.0.0.0', port=self.port, debug=False, threaded=True)
        else:
            return app


if __name__ == '__main__':
    port = 5010
    the_flask = ChurnModelFlask(port, True)
    the_flask.run()