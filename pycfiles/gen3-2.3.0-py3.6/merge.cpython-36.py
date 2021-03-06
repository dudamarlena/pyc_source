# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/gen3/tools/merge.py
# Compiled at: 2020-04-23 10:30:11
# Size of source mod 2**32: 8177 bytes
import os, csv
from collections import OrderedDict
from pathlib import Path
import sys, copy, time, base64
from datetime import datetime
import logging

def _get_guids_for_manifest_row(row, data_from_indexing_manifest, config, **kwargs):
    """
    Given a row from the manifest, return the guids that match it.

    Example:
        row = {"submitted_sample_id": "123", "foo": "bar", "fizz": "buzz"}
        data_from_indexing_manifest = {
            "123": [{"guid": "aefdf8f2-9e96-4601-a8b9-c3f661b27bc8"}],
            "456": [{"guid": "56e908b2-12df-434e-be9b-023edf66814b"}]
        }

    Returns:
        List: guids
    """
    guid_column_name = config.get('guid_column_name', 'guid')
    row_key = config.get('row_column_name')
    key_id_from_row = row.get(row_key, '').strip()
    return [row.get(guid_column_name) for row in data_from_indexing_manifest.get(key_id_from_row, []) if row.get(guid_column_name)]


def get_guids_for_manifest_row_partial_match(row, data_from_indexing_manifest, config, **kwargs):
    """
    Given a row from the manifest, return the guid to use for the metadata object by
    partially matching against the keys.

    WARNING: This iterates over the entire data_from_indexing_manifest dict EVERY TIME
             IT'S CALLED. So this is O(n2).

    ANOTHER WARNING: This does not support GUIDs matching multiple rows
                     of metadata, it only supports metadata matching multiple
                     GUIDs.

    Example:
        row = {"submitted_sample_id": "123", "foo": "bar", "fizz": "buzz"}
        data_from_indexing_manifest = {
            "123": {"guid": "aefdf8f2-9e96-4601-a8b9-c3f661b27bc8"},
            "456": {"guid": "56e908b2-12df-434e-be9b-023edf66814b"}
        }

    Returns:
        List: guids
    """
    guid_column_name = config.get('guid_column_name')
    row_key = config.get('row_column_name')
    key_from_row = row.get(row_key).strip()
    matching_guids = []
    matching_keys = []
    logging.info(f"{len(data_from_indexing_manifest)} unmatched records remaining in indexing manifest file.")
    for key, matching_rows in data_from_indexing_manifest.items():
        if key_from_row in key and matching_rows:
            matching_keys.append(key)
            matching_guids.extend([row.get(guid_column_name) for row in matching_rows if row.get(guid_column_name)])

    for key in matching_keys:
        del data_from_indexing_manifest[key]

    return matching_guids


def _get_data_from_indexing_manifest(manifest_file, config, delimiter='\t', **kwargs):
    """
    Create an OrderedDictionary mapping some key to a list of matching records with some
    field to use as a GUID.

    Args:
        manifest_file (string)
        delimiter (string): delimiter used to separate entries in the file. for a tsv,
            this is     

    Returns:
        column_to_matching_rows (dict): maps a key to a list and appends data from rows
            with matching columns
    """
    key_column_name = config.get('indexing_manifest_column_name')
    value_column_names = [config.get('guid_column_name')]
    column_to_matching_rows = {}
    with open(manifest_file, 'rt') as (csvfile):
        csvReader = csv.DictReader(csvfile, delimiter=delimiter)
        for row in csvReader:
            key = str(row[key_column_name]).strip()
            column_to_matching_rows.setdefault(key, []).append({item:row.get(item) for item in value_column_names})

    logging.debug(f"sample data from indexing manifest file: {str(column_to_matching_rows)[:250]}")
    return column_to_matching_rows


manifest_row_parsers = {'guids_for_manifest_row':_get_guids_for_manifest_row, 
 'get_data_from_indexing_manifest':_get_data_from_indexing_manifest}
manifests_mapping_config = {'guid_column_name':'guid', 
 'row_column_name':'submitted_sample_id', 
 'indexing_manifest_column_name':'sample_id'}

def merge_guids_into_metadata(indexing_manifest, metadata_manifest, indexing_manifest_file_delimiter=None, metadata_manifest_file_delimiter=None, manifest_row_parsers=manifest_row_parsers, manifests_mapping_config=manifests_mapping_config, output_filename='merged-metadata-manifest.tsv'):
    start_time = time.perf_counter()
    logging.info(f"start time: {start_time}")
    if not indexing_manifest_file_delimiter:
        indexing_manifest_file_delimiter = _get_delimiter_from_extension(indexing_manifest)
    if not metadata_manifest_file_delimiter:
        metadata_manifest_file_delimiter = _get_delimiter_from_extension(metadata_manifest)
    logging.debug(f"Getting data from {indexing_manifest} and loading into dict.")
    data_from_indexing_manifest = manifest_row_parsers['get_data_from_indexing_manifest'](indexing_manifest,
      config=manifests_mapping_config,
      delimiter=indexing_manifest_file_delimiter)
    logging.debug(f"Iterating over {metadata_manifest} and finding guid using dict created from {indexing_manifest}.")
    with open(metadata_manifest, 'rt') as (file):
        reader = csv.DictReader(file, delimiter=metadata_manifest_file_delimiter)
        headers = ['guid']
        headers.extend(reader.fieldnames)
        logging.debug(f"writing headers to {output_filename}: {headers}")
        write_header_to_file(filename=output_filename,
          fieldnames=headers,
          delimiter='\t')
        logging.debug(f"beginning iteration over rows in {metadata_manifest}")
        for row in reader:
            guids = manifest_row_parsers['guids_for_manifest_row'](row,
              data_from_indexing_manifest, config=manifests_mapping_config)
            if not guids:
                logging.warning(f"could not find matching guid for row: {row}")
            else:
                logging.debug(f"found guids {guids} matching row: {row}")
            for guid in guids:
                row.update({'guid': guid})
                append_row_to_file(filename=output_filename,
                  row=row,
                  fieldnames=headers,
                  delimiter='\t')

    end_time = time.perf_counter()
    logging.info(f"end time: {end_time}")
    logging.info(f"run time: {end_time - start_time}")
    logging.info(f"output file:\n{os.path.abspath(output_filename)}")


def _get_delimiter_from_extension(filename):
    file_ext = os.path.splitext(filename)
    if file_ext[(-1)].lower() == '.tsv':
        file_delimiter = '\t'
    else:
        file_delimiter = ','
    return file_delimiter


def write_header_to_file(filename, fieldnames, delimiter='\t'):
    """
    Writes to a file in TSV format.

    Returns:
        None
    """
    with open(filename, mode='w+') as (outfile):
        writer = csv.DictWriter(outfile,
          delimiter=delimiter, fieldnames=fieldnames, extrasaction='ignore')
        writer.writeheader()


def append_row_to_file(filename, row, fieldnames, delimiter='\t'):
    """
    Appends to a file in TSV format.

    Returns:
        None
    """
    with open(filename, mode='a') as (outfile):
        writer = csv.DictWriter(outfile,
          delimiter=delimiter, fieldnames=fieldnames, extrasaction='ignore')
        writer.writerow(row)