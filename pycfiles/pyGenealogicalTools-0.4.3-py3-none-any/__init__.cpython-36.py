# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\Val\Documents\GitHub\GeniTools\build\lib\pyGeni\__init__.py
# Compiled at: 2019-08-07 12:21:32
# Size of source mod 2**32: 2646 bytes
__all__ = [
 'profile', 'data_models', 'immediate_family', 'geniapi_common', 'union', 'geni2gedcom', 'interface_geni_database']
import requests, logging, re
from messages.pygeni_messages import ERROR_REQUESTS
GENI_ADDRESS = 'https://www.geni.com'
GENI_FAMILY = '/immediate-family'
GENI_INITIATE_PARAMETER = '?'
GENI_ADD_PARAMETER = '&'
GENI_TOKEN = 'access_token='
GENI_SINGLE_TOKEN = GENI_INITIATE_PARAMETER + GENI_TOKEN
GENI_PARAM_TOKEN = GENI_ADD_PARAMETER + GENI_TOKEN
GENI_ADD_CHILD = '/add-child'
GENI_DELETE = '/delete'
GENI_ADD_PARTNER = '/add-partner'
GENI_UPDATE = '/update'
GENI_ADD_PARENT = '/add-parent'
GENI_VALIDATE_TOKEN = GENI_ADDRESS + '/platform/oauth/validate_token' + GENI_SINGLE_TOKEN
GENI_API = GENI_ADDRESS + '/api/'
GENI_PEOPLE = GENI_ADDRESS + '/people/'
GENI_PROFILE = GENI_API + 'profile-'
GENI_CALLED_UNIONS = {}
TOKEN = None

def get_token():
    """
    Function to get the token value
    """
    global TOKEN
    return TOKEN


def set_token(token_value):
    """
    Function to set-up the token
    """
    global TOKEN
    TOKEN = token_value


def update_geni_address(new_geni_address):
    """
    This function will update the values of geni variables to be able to use
    in testing mode
    """
    global GENI_ADDRESS
    global GENI_API
    global GENI_PEOPLE
    global GENI_PROFILE
    global GENI_SINGLE_TOKEN
    global GENI_VALIDATE_TOKEN
    GENI_ADDRESS = new_geni_address
    GENI_VALIDATE_TOKEN = GENI_ADDRESS + '/platform/oauth/validate_token' + GENI_SINGLE_TOKEN
    GENI_API = GENI_ADDRESS + '/api/'
    GENI_PEOPLE = GENI_ADDRESS + '/people/'
    GENI_PROFILE = GENI_API + 'profile-'


def geni_request_get(url):
    """
    Function to perform get calls.
    """
    data = requests.get(url)
    if 'error' in data.json().keys():
        logging.error(ERROR_REQUESTS + str(data.json()))
    return data


def geni_request_post(url, data_input=None):
    """
    Function to perform post calls.
    """
    if data_input == None:
        data_input = {}
    data = requests.post(url, json=data_input)
    if 'error' in data.json().keys():
        logging.error(ERROR_REQUESTS + str(data.json()))
    return data


def get_profile_id_from_address(prof_url):
    """
    Function to extract the profile from the address
    """
    return re.sub('.*profile', 'profile', prof_url)