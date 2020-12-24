# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/redi/upload.py
# Compiled at: 2018-08-13 08:58:37
"""
Functions related to uploading data to REDCap
"""
import ast, collections, datetime, logging, os
from lxml import etree
from redcap import RedcapError
from utils import throttle
logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

def create_import_data_json(import_data_dict, event_tree):
    """
    Convert data from event_tree to json format.

    @TODO: evaluate performance
    @see the caller {@link #redi.upload.generate_output()}

    :param: import_data_dict: holds the event tree data
    :param: event_tree: holds the event tree data
    :rtype: dict
    :return the json version of the xml data
    """
    root = event_tree
    event_name = root.find('name')
    if event_name is None or not event_name.text:
        raise Exception('Expected non-blank element event/name')
    import_data_dict['redcap_event_name'] = event_name.text
    event_field_value_list = root.xpath('//event/field/name')
    for name in event_field_value_list:
        if name.text is None:
            raise Exception('Expected non-blank element event/field/name')

    event_field_list = root.xpath('field')
    contains_data = False
    for field in event_field_list:
        val = field.findtext('value', '')
        import_data_dict[field.findtext('name')] = val
        if val and not contains_data:
            contains_data = True

    return {'json_data': import_data_dict, 'contains_data': contains_data}


def create_redcap_records(import_data):
    """
    Creates REDCap records from RED-I's form data, AKA import data.

    REDCap API only accepts records for importing. Records are differentiated by
    their unique record ID, unless the REDCap Project is a Longitudinal study.
    In that case, they are differentiated by a combination of record ID and an
    event.

    Since RED-I views the world in terms of forms, we have to project our
    form-centric view into REDCap's record-centric world. This is done by
    combining all form data with the same Subject ID and Event Name into the
    same record.

    :param import_data: iterable of 4-tuples: (study_id_key, form_name,
        event_name, json_data_dict)
    :return: iterable of REDCap records ready for upload
    """
    records_by_subject_and_event = collections.defaultdict(dict)
    for subject_id_key, _, event_name, record in import_data:
        records_by_subject_and_event[(subject_id_key, event_name)].update(record)

    return records_by_subject_and_event.itervalues()


def generate_output(person_tree, redcap_client, rate_limit, sent_events, max_retry_count, skip_blanks=False, bulk_send_blanks=False):
    """
    Note: This function communicates with the redcap application.
    Steps:
        - loop for each person/form/event element
        - generate a csv fragment `using create_eav_output`
        - send csv fragment to REDCap using `send_eav_data_to_redcap`

    @see the caller {@link #redi.redi._run()}

    :rtype:     dictionary
    :return:    the report_data which is passed to the report rendering function
    """
    report_data = {'errors': []}
    subject_details = {}
    form_details = {}
    person_count = 0
    root = person_tree.getroot()
    persons = root.xpath('//person')
    upload_data = throttle.Throttle(redcap_client.send_data_to_redcap, int(rate_limit))
    blanks = []
    for person in persons:
        time_begin = datetime.datetime.now()
        person_count += 1
        study_id = (person.xpath('study_id') or [None])[0]
        if study_id is None:
            raise Exception('Expected a valid value for study_id')
        event_count = 0
        logger.info('Start sending data for study_id: %s' % study_id.text)
        forms = person.xpath('./all_form_events/form')
        for form in forms:
            form_name = form.xpath('name')[0].text
            form_key = 'Total_' + form_name + '_Forms'
            study_id_key = study_id.text
            if study_id_key not in subject_details:
                subject_details[study_id_key] = {}
                subject_details[study_id_key]['lab_id'] = person.get('lab_id')
            if form_key not in subject_details[study_id_key]:
                subject_details[study_id_key][form_key] = 0
            if form_key not in form_details:
                form_details[form_key] = 0
            logger.debug('parsing study_id ' + study_id.text + ' form: ' + form_name)
            for event in form.xpath('event'):
                event_name = event.findtext('name', '')
                assert event_name, 'Missing name for form event'
                try:
                    import_dict = {redcap_client.project.def_field: study_id.text}
                    import_dict = create_import_data_json(import_dict, event)
                    json_data_dict = import_dict['json_data']
                    contains_data = import_dict['contains_data']
                    if sent_events.was_sent(study_id_key, form_name, event_name):
                        logger.debug('Skipping previously sent ' + event_name)
                        if contains_data:
                            subject_details[study_id_key][form_key] += 1
                            form_details[form_key] += 1
                        continue
                    is_blank = not contains_data
                    if is_blank:
                        if skip_blanks:
                            break
                        if bulk_send_blanks:
                            blanks.append((study_id_key, form_name, event_name,
                             json_data_dict))
                            continue
                    event_count += 1
                    if 0 == event_count % 50:
                        logger.info('Requests sent: %s' % event_count)
                    try:
                        upload_data([json_data_dict], max_retry_count, overwrite=True)
                        sent_events.mark_sent(study_id_key, form_name, event_name)
                        logger.debug('Sent ' + event_name)
                        if contains_data:
                            subject_details[study_id_key][form_key] += 1
                            form_details[form_key] += 1
                    except RedcapError as redcap_err:
                        handle_errors_in_redcap_xml_response(study_id, redcap_err, report_data)

                except Exception as e:
                    logger.error(e.message)
                    raise

        time_end = datetime.datetime.now()
        logger.info('Total execution time for study_id %s was %s' % (study_id_key, time_end - time_begin))
        logger.info('Total REDCap requests sent: %s \n' % event_count)

    if blanks:
        logger.info('Sending blank forms in bulk...')
        records = list(create_redcap_records(blanks))
        try:
            response = upload_data(records, overwrite=True)
            for study_id_key, form_name, event_name, record in blanks:
                sent_events.mark_sent(study_id_key, form_name, event_name)

            logger.info(('Sent {} blank form-events.').format(response['count']))
        except RedcapError as redcap_err:
            logger.error('Failed to send blank form-events.')
            handle_errors_in_redcap_xml_response(study_id, redcap_err, report_data)

    report_data.update({'total_subjects': person_count, 
       'form_details': form_details, 
       'subject_details': subject_details, 
       'errors': report_data['errors']})
    logger.debug('report_data ' + repr(report_data))
    return report_data


def handle_errors_in_redcap_xml_response(study_id, redcap_err, report_data):
    """
    Checks for any errors in the redcap response and update
    report data if there are any errors.

    Parameters:
    -----------
    redcap_err: RedcapError object
    report_data: dictionary to which we store error details
    """
    response = ast.literal_eval(str(redcap_err))
    logger.debug('handling response from the REDCap')
    if 'error' not in response:
        logger.warn(("RedcapError does not contain the expected 'error' key: {}").format(response))
        return
    if 'records' in response:
        records = response['records']
        for record in records:
            details = ('(record: {}, field_name: {}, value: {}, message: {})').format(record['record'], record['field_name'], record['value'], record['message'])
            error_string = ('{}: {}').format(response['error'], details)
            report_data['errors'].append(error_string)
            logger.error(('{}').format(error_string))

    elif 'fields' in response:
        fields = response['fields']
        details = ('{}').format(fields)
        error_string = ('{}: {}').format(response['error'], details)
        report_data['errors'].append(error_string)
        logger.error(error_string)
    else:
        err = ('A RedcapError ocured for study_id: {}. It contains an unexpected type of error: {}').format(study_id, response)
        logger.warn(err)