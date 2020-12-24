# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyredatam/cpv2010arg.py
# Compiled at: 2015-09-21 12:56:27
"""
cpv2010arg.py

Make a query to 2010 Argentina's Census REDATAM database.
"""
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import with_statement
import os
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pyvirtualdisplay import Display
import pandas as pd
from bs4 import BeautifulSoup
import requests
from collections import OrderedDict
import json, time
from utils import get_data_dir
BASE_URL = b'http://200.51.91.245/argbin/RpWebEngine.exe/PortalAction?BASE=CPV2010B'
URL_DICTIONARY = b'http://200.51.91.245/argbin/RpWebEngine.exe/Dictionary?&BASE=CPV2010B&ITEM=DICALL&MAIN=WebServerMain.inl'
URL_CATEGORIES = b'http://200.51.91.245/argbin/RpWebEngine.exe/Dictionary'

def make_arealist_query(query):
    """Query ARG REDATAM 2010 Census for an Area List.

    A Firefox visible instance will be opened to make the query simulating user
    input. If Xephyr, Xvfb or Xvnc backends are installed, the instance will be
    hidden. You MUST have Firefox installed to use this method.

    Args:
        query (str): REDATAM Area List query.

    Returns:
        pandas.DataFrame: Data result from query.
    """
    return parse_arealist_to_dataframe(make_query(query))


def parse_arealist_to_dataframe(html):
    """Parse an html result of a query to REDATAM, into a DataFrame.

    Args:
        html (str): Result of a REDATAM query.

    Returns:
        pandas.DataFrame: Data result from query.
    """
    bs = BeautifulSoup(html, b'html5lib')
    rows = bs.find_all(b'tr')
    df = pd.DataFrame(columns=[ td.get_text() for td in rows[1].find_all(b'td') ])
    for row in rows[2:-1]:
        text_values = [ td.get_text() for td in row.find_all(b'td') ]
        area_code = text_values[0]
        values = [ int(text.replace(b'.', b'')) for text in text_values[1:] ]
        values.insert(0, area_code)
        df.loc[len(df)] = values

    return df


def make_query(query, url=BASE_URL):
    """Query ARG REDATAM 2010 Census.

    A Firefox visible instance will be opened to make the query simulating user
    input. If Xephyr, Xvfb or Xvnc backends are installed, the instance will be
    hidden. You MUST have Firefox installed to use this method.

    Args:
        query (str): REDATAM query.

    Returns:
        str: Data result from query in html format.
    """
    with Display(visible=False):
        driver = webdriver.Firefox()
        driver.get(url)
        driver.switch_to.frame(b'Index')
        info_gral = _get_clickable_by_id(driver, b'ui-accordion-root-header-4')
        info_gral.click()
        id_progr_redatam = b'ui-accordion-ui-accordion-root-panel-4-header-1'
        progr_redatam = _get_clickable_by_id(driver, id_progr_redatam)
        progr_redatam.click()
        id_redatam_panel = b'ui-accordion-ui-accordion-root-panel-4-panel-1'
        progr_redatam_panel = _get_clickable_by_id(driver, id_redatam_panel)
        procesador = progr_redatam_panel.find_element_by_tag_name(b'a')
        procesador.click()
        driver.switch_to.default_content()
        _switch_to_loaded_frame(driver, b'Output')
        query_input = driver.find_element_by_tag_name(b'textarea')
        query_input.send_keys(query.decode(b'utf-8', b'ignore'))
        submit = driver.find_element_by_name(b'SUBMIT')
        submit.click()
        driver.switch_to.default_content()
        _switch_to_loaded_frame(driver, b'Output')
        _switch_to_loaded_frame(driver, b'grid')
        _wait_until_text(driver, b'body > p > a:nth-child(1)', b'Descargar en formato Excel')
        html = driver.page_source
        driver.close()
    return html


def get_dictionary(dict_filename=b'cpv2010arg_diccionario.json'):
    with open(os.path.join(get_data_dir(), dict_filename), b'r') as (f):
        return json.load(f)


def get_ids(ids_filename=b'cpv2010arg_ids.json'):
    with open(os.path.join(get_data_dir(), ids_filename), b'r') as (f):
        return json.load(f)


def scrape_dictionary(url_dictionary=URL_DICTIONARY, url_categories=URL_CATEGORIES):
    """Build an entities and variables dictionary of ARG 2010 Census.

    Args:
        url_dictionary (str): Url where dictionary is.
        url_categories (str): Request url to get the categories of variables.

    Returns:
        (dict, list, list): A dictionary of entities and variables, a list of
            entities used as geographical divisions and a list of entities with
            data (not used as geographical divisions).
    """
    df = pd.read_html(url_dictionary, flavor=b'html5lib', header=0, skiprows=[1, 72, 73])[1]
    dictionary, geo_entities, data_entities = _parse_df_to_dict(df)
    variables = [ data_entity + b'.' + variable for data_entity in data_entities for variable in dictionary[data_entity].keys()
                ]
    data = {b'MAIN': b'WebServerMain.inl', 
       b'BASE': b'CPV2010B', 
       b'CODIGO': b'xxUsuarioxx', 
       b'ITEM': b'DICCATVIV', 
       b'MODE': b'LISTVAR', 
       b'DICTIONARY': b'HTML', 
       b'VARIABLE': variables, 
       b'SUBMIT': b'Ejecutar'}
    r = requests.post(url_categories, data=data)
    bs = BeautifulSoup(r.content, b'html5lib')
    text = bs.select(b'#redInput')[0].get_text()
    _parse_categories(dictionary, text)
    return (
     dictionary, geo_entities, data_entities)


def _get_clickable_by_id(driver, element_id):
    return WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, element_id)))


def _switch_to_loaded_frame(driver, frame_id):
    return WebDriverWait(driver, 20).until(EC.frame_to_be_available_and_switch_to_it((By.NAME, frame_id)))


def _wait_until_text(driver, css_selector, text):
    WebDriverWait(driver, 20).until(EC.text_to_be_present_in_element((
     By.CSS_SELECTOR, css_selector), text))


def _parse_df_to_dict(df):
    """Create entities and variables dictionary from a DataFrame."""
    dictionary = OrderedDict()
    geo_entities, data_entities = [], []
    last_entity = b'0'
    entity_name = b''
    for row in df.iterrows():
        entity, variable = unicode(row[1][b'#']).split(b'.')
        if entity != last_entity:
            if entity_name not in geo_entities and len(entity_name) > 0:
                data_entities.append(entity_name)
            entity_name = row[1][b'Nombre de la entidad']
            dictionary[entity_name] = {}
            last_entity = entity
        else:
            dictionary[entity_name][row[1][b'Nombre de la variable']] = []
            if row[1][b'Tipo'].strip() == b'C' and entity_name not in geo_entities:
                geo_entities.append(entity_name)

    data_entities.append(entity_name)
    return (
     dictionary, geo_entities, data_entities)


def _parse_categories(dictionary, text):
    """Parse variable's categories from text.

    Args:
        dictionary (dict): Entities and variables dictionary.
        text (str): Text with the categories of each variable.

    Side effects:
        Populate lists of categories in each variable in the dictionary.
    """
    variable = b''
    entity = b''
    for line in text.splitlines():
        if b':' in line:
            field, value = line.split(b':')
            if field.strip() == b'Nombre':
                variable = value.strip()
            elif field.strip() == b'Entidad':
                entity = value.strip()
        elif b'.' in line:
            id_category, category = line.split(b'.', 1)
            dictionary[entity][variable].append((
             id_category.strip(), category.strip()))