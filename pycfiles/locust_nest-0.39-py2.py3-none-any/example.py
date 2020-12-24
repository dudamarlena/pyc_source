# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./example.py
# Compiled at: 2018-06-11 06:09:40
from locust import TaskSet, task, HttpLocust

class ExampleModel(TaskSet):
    weight = 0
    auth_endpoint = ''
    auth_header = {'Authorization': 'Bearer {}'}
    username = None
    password = None

    def login(self, username, password, auth_endpoint):
        payload = {'userName': username, 
           'password': password}
        headers = {'Content-Type': 'application/json'}
        r = self.client.post(auth_endpoint, headers=headers, json=payload)
        if r.ok:
            jr = r.json()
            self.token = jr.get('token')
            return True
        else:
            print r.content
            r.raise_for_status()
            return False

    def on_start(self):
        """Set up before running tasks.

        For example:
        * Log in & save token
        * Retrieve bulk information needed for other tasks

        """
        return self.login(self.username, self.password, self.auth_endpoint)

    def on_stop(self):
        """Teardown: unclaim resources e.g. claimed user/resource.

        """
        pass

    @task(5)
    def model_action(self):
        """Codified behaviour of a particular action this model may perform
        e.g. viewing user details

        """
        self.client.get('/')


class ExampleModelLocust(HttpLocust):
    host = 'http://127.0.0.1:8089'
    task_set = ExampleModel