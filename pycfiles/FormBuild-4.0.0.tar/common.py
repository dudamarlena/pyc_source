# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/james/Documents/Work/OKFN/examples/env/src/formbuild/example/common.py
# Compiled at: 2011-02-07 07:31:39
interest_choices = [
 ('sitting', 'Sitting'),
 ('running', 'Running'),
 ('walking', 'Walking')]
invalid_sample_data = {'census_name': 'my census', 'census_email': 'bobodwls.com', 
   'census_date': '2011-01-01', 
   'census_type': 'type2', 
   'people': [
            {'name': 'Bob', 'interests': [
                           'shitting', 'running']}]}
valid_sample_data = {'census_name': 'my census', 'census_email': 'bob@owls.com', 
   'census_date': '2011-01-01', 
   'census_type': 'type2', 
   'people': [
            {'name': 'Bob', 'interests': [
                           'sitting', 'running']}]}