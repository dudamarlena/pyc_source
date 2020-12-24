# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/mdiazmel/code/aramis/clinica/clinica/iotools/converters/adni_to_bids/adni_utils.py
# Compiled at: 2019-11-19 04:22:54
# Size of source mod 2**32: 34867 bytes
__author__ = 'Jorge Samper-Gonzalez and Sabrina Fontanella'
__copyright__ = 'Copyright 2016-2019 The Aramis Lab Team'
__credits__ = ['']
__license__ = 'See LICENSE.txt file'
__version__ = '0.1.0'
__maintainer__ = 'Jorge Samper-Gonzalez'
__email__ = 'jorge.samper-gonzalez@inria.fr'
__status__ = 'Development'

def replace_sequence_chars(sequence_name):
    """
    Replace some special character with the sequence name given in input

    Args:
        sequence_name: sequence to replace

    Returns: the new string

    """
    import re
    return re.sub('[ /;*():]', '_', sequence_name)


def fill_zeros(s, length):
    return '0' * (length - len(str(s))) + str(s)


def days_between(d1, d2):
    """
    Calculate the days between two dates

    Args:
        d1: date 1
        d2: date 2

    Returns: number of days between date 2 and date 1

    """
    from datetime import datetime
    d1 = datetime.strptime(d1, '%Y-%m-%d')
    d2 = datetime.strptime(d2, '%Y-%m-%d')
    return abs((d2 - d1).days)


def viscode_to_session(viscode):
    """
    Replace the session label 'bl' with 'M00' or capitalize the session name passed
    as input

    Args:
        viscode: session name

    Returns: M00 if is the baseline session or the original session name capitalized

    """
    if viscode == 'bl':
        return 'M00'
    else:
        return viscode.capitalize()


def visits_to_timepoints_mrilist(subject, mri_list_subj, adnimerge_subj, modality):
    """

    Args:
        subject:
        mri_list_subj:
        adnimerge_subj:
        modality:

    Returns:

    """
    from datetime import datetime
    from clinica.utils.stream import cprint
    visits = dict()
    unique_visits = list(mri_list_subj.VISIT.unique())
    pending_timepoints = []
    for adni_row in adnimerge_subj.iterrows():
        visit = adni_row[1]
        if visit.ORIGPROT == 'ADNI3':
            if visit.VISCODE == 'bl':
                preferred_visit_name = 'ADNI Screening'
            else:
                year = str(int(visit.VISCODE[1:]) / 12)
                preferred_visit_name = 'ADNI3 Year ' + year + ' Visit'
        elif visit.ORIGPROT == 'ADNI2':
            if visit.VISCODE == 'bl':
                preferred_visit_name = 'ADNI2 Screening MRI-New Pt'
            else:
                if visit.VISCODE == 'm03':
                    preferred_visit_name = 'ADNI2 Month 3 MRI-New Pt'
                else:
                    if visit.VISCODE == 'm06':
                        preferred_visit_name = 'ADNI2 Month 6-New Pt'
                    else:
                        year = str(int(visit.VISCODE[1:]) / 12)
                        preferred_visit_name = 'ADNI2 Year ' + year + ' Visit'
        elif visit.VISCODE == 'bl':
            if visit.ORIGPROT == 'ADNI1':
                preferred_visit_name = 'ADNI Screening'
            else:
                preferred_visit_name = 'ADNIGO Screening MRI'
        else:
            if visit.VISCODE == 'm03':
                preferred_visit_name = 'ADNIGO Month 3 MRI'
            else:
                month = int(visit.VISCODE[1:])
                if month < 54:
                    preferred_visit_name = 'ADNI1/GO Month ' + str(month)
                else:
                    preferred_visit_name = 'ADNIGO Month ' + str(month)
            if preferred_visit_name in unique_visits:
                key_preferred_visit = (
                 visit.VISCODE, visit.COLPROT, visit.ORIGPROT)
                if key_preferred_visit not in visits.keys():
                    visits[key_preferred_visit] = preferred_visit_name
                else:
                    if visits[key_preferred_visit] != preferred_visit_name:
                        cprint('[%s] Subject %s has multiple visits for one timepoint.' % (modality, subject))
                unique_visits.remove(preferred_visit_name)
            else:
                pending_timepoints.append(visit)

    for visit in unique_visits:
        image = mri_list_subj[(mri_list_subj.VISIT == visit)].iloc[0]
        min_db = 100000
        min_db2 = 0
        min_visit = None
        min_visit2 = None
        for timepoint in pending_timepoints:
            db = days_between(image.SCANDATE, timepoint.EXAMDATE)
            if db < min_db:
                min_db2 = min_db
                min_visit2 = min_visit
                min_db = db
                min_visit = timepoint

        if min_visit is None:
            cprint('No corresponding timepoint in ADNIMERGE for subject ' + subject + ' in visit ' + image.VISIT)
            cprint(image)
            continue
        if min_visit2 is not None and min_db > 90:
            cprint('More than 60 days for corresponding timepoint in ADNIMERGE for subject %s in visit %s on %s' % (
             subject, image.VISIT, image.SCANDATE))
            cprint('Timepoint 1: %s - %s on %s (Distance: %s days)' % (
             min_visit.VISCODE, min_visit.ORIGPROT, min_visit.EXAMDATE, min_db))
            cprint('Timepoint 2: %s - %s on %s (Distance: %s days)' % (
             min_visit2.VISCODE, min_visit2.ORIGPROT, min_visit2.EXAMDATE, min_db2))
            if datetime.strptime(min_visit.EXAMDATE, '%Y-%m-%d') > datetime.strptime(image.SCANDATE, '%Y-%m-%d') > datetime.strptime(min_visit2.EXAMDATE, '%Y-%m-%d'):
                dif = days_between(min_visit.EXAMDATE, min_visit2.EXAMDATE)
                if abs(dif / 2.0 - min_db) < 30:
                    min_visit = min_visit2
                cprint('We prefer ' + min_visit.VISCODE)
            else:
                key_min_visit = (
                 min_visit.VISCODE, min_visit.COLPROT, min_visit.ORIGPROT)
                if key_min_visit not in visits.keys():
                    visits[key_min_visit] = image.VISIT
                elif visits[key_min_visit] != image.VISIT:
                    cprint('[%s] Subject %s has multiple visits for one timepoint.' % (modality, subject))

    return visits


def select_image_qc(id_list, mri_qc_subj):
    import numpy as np
    if len(id_list) == 0:
        return
    selected_image = None
    image_ids = ['I' + str(imageuid) for imageuid in id_list]
    int_ids = [int(imageuid) for imageuid in id_list]
    images_qc = mri_qc_subj[mri_qc_subj.loni_image.isin(image_ids)]
    if images_qc.shape[0] < 1:
        return max(int_ids)
    if np.sum(images_qc.series_selected) == 1:
        selected_image = images_qc[(images_qc.series_selected == 1)].iloc[0].loni_image[1:]
    else:
        images_not_rejected = images_qc[(images_qc.series_quality < 4)]
    if images_not_rejected.shape[0] < 1:
        qc_ids = set([int(qc_id[1:]) for qc_id in images_qc.loni_image.unique()])
        no_qc_ids = list(set(int_ids) - qc_ids)
        if len(no_qc_ids) == 0:
            return
        return max(no_qc_ids)
    else:
        series_quality = [q if q > 0 else 4 for q in list(images_not_rejected.series_quality)]
        best_q = np.amin(series_quality)
        if best_q == 4:
            best_q = -1
        images_best_qc = images_not_rejected[(images_not_rejected.series_quality == best_q)]
        if images_best_qc.shape[0] == 1:
            selected_image = images_best_qc.iloc[0].loni_image[1:]
        else:
            best_ids = [int(x[1:]) for x in images_best_qc.loni_image.unique()]
            selected_image = max(best_ids)
        return int(selected_image)


def remove_space_and_symbols(data):
    """
    Remove spaces and  - _ from a list (or a single) of strings

    Args:
        data: list of strings or a single string to clean

    Returns:
         data: list of strings or a string without space and symbols _ and -

    """
    import re
    if type(data) is list:
        for i in range(0, len(data)):
            data[i] = re.sub('[-_ ]', '', data[i])

    else:
        data = re.sub('[-_ ]', '', data)
    return data


def check_two_dcm_folder(dicom_path, bids_folder, image_uid):
    """
    Check if a folder contains more than one DICOM and if yes, copy the DICOM related to image id passed as parameter
    into a temporary folder called tmp_dicom_folder

    Args:
        dicom_path: path to the DICOM folder
        bids_folder: path to the BIDS folder where the dataset will be stored
        image_uid: image id of the fmri

    Returns: the path to the original DICOM folder or the path to a temporary folder called tmp_dicom_folder where only
     the DICOM to convert is copied

    """
    from glob import glob
    from os import path
    from shutil import copy
    import shutil, os
    temp_folder_name = 'tmp_dcm_folder_' + str(image_uid).strip(' ')
    dest_path = path.join(bids_folder, temp_folder_name)
    dicom_list = glob(path.join(dicom_path, '*.dcm'))
    image_list = glob(path.join(dicom_path, '*%s.dcm' % image_uid))
    if len(dicom_list) != len(image_list):
        if os.path.exists(dest_path):
            shutil.rmtree(dest_path)
        os.mkdir(dest_path)
        dmc_to_conv = glob(path.join(dicom_path, '*' + str(image_uid) + '.dcm*'))
        for d in dmc_to_conv:
            copy(d, dest_path)

        return dest_path
    else:
        return dicom_path


def remove_tmp_dmc_folder(bids_dir, image_id):
    """
    Remove the folder tmp_dmc_folder created by the method check_two_dcm_folder (if existing)

    Args:
        bids_dir: path to the BIDS directory
        image_id:

    Returns:

    """
    from os.path import exists, join
    from shutil import rmtree
    tmp_dcm_folder_path = join(bids_dir, 'tmp_dcm_folder_' + str(image_id).strip(' '))
    if exists(tmp_dcm_folder_path):
        rmtree(tmp_dcm_folder_path)


def check_bids_t1(bids_path, container='anat', extension='_T1w.nii.gz', subjects=None):
    import os
    if subjects is None:
        subjects = next(os.walk(bids_path))[1]
    errors = []
    print(len(subjects))
    for subject in subjects:
        sessions = next(os.walk(os.path.join(bids_path, subject)))[1]
        for session in sessions:
            image_name = subject + '_' + session + extension
            image_dir = os.path.join(bids_path, subject, session, container)
            if not os.path.isdir(image_dir):
                print('No directory: ' + image_dir)
            else:
                files = next(os.walk(image_dir))[2]
                if not files:
                    errors.append('Subject ' + subject + ' for session ' + session + ' folder is empty')
                for f in files:
                    if f != image_name:
                        errors.append('Subject ' + subject + ' for session ' + session + ' folder contains: ' + f)

    return errors


def check_bids_dwi(bids_path, container='dwi', extension=('_acq-axial_dwi.bvec', '_acq-axial_dwi.bval', '_acq-axial_dwi.nii.gz'), subjects=None):
    import os
    if subjects is None:
        subjects = next(os.walk(bids_path))[1]
    errors = []
    print(len(subjects))
    for subject in subjects:
        sessions = next(os.walk(os.path.join(bids_path, subject)))[1]
        for session in sessions:
            image_names = [subject + '_' + session + ext for ext in extension]
            image_names.sort()
            image_dir = os.path.join(bids_path, subject, session, container)
            if not os.path.isdir(image_dir):
                print('No directory: ' + image_dir)
            else:
                files = next(os.walk(image_dir))[2]
                files.sort()
                if not files:
                    errors.append('Subject ' + subject + ' for session ' + session + ' folder is empty')
                if image_names != files:
                    errors.append('Subject ' + subject + ' for session ' + session + ' folder contains: \n' + str(files))

    return errors


def is_nan(value):
    """
    Check if a value is nan

    Args:
        value: value that need to be checked

    Returns: true if is nan, false otherwise

    """
    from math import isnan
    import numpy as np
    if type(value) != float:
        if type(value) != np.float64:
            return False
    if isnan(value):
        return True
    else:
        return False


def remove_fields_duplicated(bids_fields):
    seen = set()
    seen_add = seen.add
    return [x for x in bids_fields if not (x in seen or seen_add(x))]


def convert_diagnosis_code(diagnosis_code):
    """
    Convert the numeric field DXCURREN and DXCHANGE contained in DXSUM_PDXCONV_ADNIALL.csv into a code that identify the
    diagnosis

    Args:
        diagnosis_code: a string that represents a number between 1 and 9

    Returns:a code that identify a diagnosis

    """
    diagnosis = {1:'CN', 
     2:'MCI',  3:'AD',  4:'MCI',  5:'AD',  6:'AD',  7:'CN',  8:'MCI',  9:'CN'}
    if is_nan(diagnosis_code):
        return diagnosis_code
    else:
        return diagnosis[int(diagnosis_code)]


def write_adni_sessions_tsv(sessions_dict, fields_bids, bids_subjs_paths):
    """
    Write the result of method create_session_dict into several tsv files

    Args:
        sessions_dict: dictonary coming from the method create_sessions_dict
        fields_bids: fields bids to convert
        bids_subjs_paths: a list with the path to all bids subjects

    Returns:

    """
    from os import path
    import os, pandas as pd, numpy as np
    columns_order = remove_fields_duplicated(fields_bids)
    columns_order.insert(0, 'session_id')
    for sp in bids_subjs_paths:
        if not path.exists(sp):
            os.makedirs(sp)
        bids_id = sp.split(os.sep)[(-1)]
        fields_bids = list(set(fields_bids))
        sessions_df = pd.DataFrame(columns=fields_bids)
        if bids_id in sessions_dict:
            sess_aval = sessions_dict[bids_id].keys()
            for ses in sess_aval:
                sessions_df = sessions_df.append(pd.DataFrame((sessions_dict[bids_id][ses]), index=['i']))

            sessions_df = sessions_df[columns_order]
            sessions_df[['adas_Q1', 'adas_Q2', 'adas_Q3', 'adas_Q4', 'adas_Q5', 'adas_Q6', 'adas_Q7', 'adas_Q8', 'adas_Q9', 'adas_Q10', 'adas_Q11', 'adas_Q12', 'adas_Q13']] = sessions_df[[
             'adas_Q1', 'adas_Q2', 'adas_Q3', 'adas_Q4',
             'adas_Q5', 'adas_Q6', 'adas_Q7', 'adas_Q8',
             'adas_Q9', 'adas_Q10', 'adas_Q11', 'adas_Q12',
             'adas_Q13']].apply(pd.to_numeric)
            sessions_df['adas_memory'] = sessions_df['adas_Q1'] + sessions_df['adas_Q4'] + sessions_df['adas_Q7'] + sessions_df['adas_Q8'] + sessions_df['adas_Q9']
            sessions_df['adas_language'] = sessions_df['adas_Q2'] + sessions_df['adas_Q5'] + sessions_df['adas_Q10'] + sessions_df['adas_Q11'] + sessions_df['adas_Q12']
            sessions_df['adas_praxis'] = sessions_df['adas_Q3'] + sessions_df['adas_Q6']
            sessions_df['adas_concentration'] = sessions_df['adas_Q13']
            list_diagnosis_nan = np.where(pd.isnull(sessions_df['diagnosis']))
            diagnosis_change = {1:'CN',  2:'MCI',  3:'AD'}
            for j in list_diagnosis_nan[0]:
                if not is_nan(sessions_df['adni_diagnosis_change'].iloc[j]) and int(sessions_df['adni_diagnosis_change'].iloc[j]) < 4:
                    sessions_df['diagnosis'].iloc[j] = diagnosis_change[int(sessions_df['adni_diagnosis_change'].iloc[j])]

            sessions_df.to_csv((path.join(sp, bids_id + '_sessions.tsv')), sep='\t', index=False, encoding='utf-8')


def update_sessions_dict--- This code section failed: ---

 L. 512         0  LOAD_FAST                'visit_id'
                2  LOAD_STR                 'sc'
                4  COMPARE_OP               ==
                6  POP_JUMP_IF_TRUE     16  'to 16'
                8  LOAD_FAST                'visit_id'
               10  LOAD_STR                 'uns1'
               12  COMPARE_OP               ==
             14_0  COME_FROM             6  '6'
               14  POP_JUMP_IF_FALSE    20  'to 20'

 L. 513        16  LOAD_FAST                'sessions_dict'
               18  RETURN_END_IF    
             20_0  COME_FROM            14  '14'

 L. 515        20  LOAD_GLOBAL              viscode_to_session
               22  LOAD_FAST                'visit_id'
               24  CALL_FUNCTION_1       1  ''
               26  STORE_FAST               'visit_id'

 L. 517        28  LOAD_FAST                'bids_field_name'
               30  LOAD_STR                 'diagnosis'
               32  COMPARE_OP               ==
               34  POP_JUMP_IF_FALSE    44  'to 44'

 L. 518        36  LOAD_GLOBAL              convert_diagnosis_code
               38  LOAD_FAST                'field_value'
               40  CALL_FUNCTION_1       1  ''
               42  STORE_FAST               'field_value'
             44_0  COME_FROM            34  '34'

 L. 522        44  LOAD_FAST                'subj_bids'
               46  LOAD_FAST                'sessions_dict'
               48  COMPARE_OP               in
               50  POP_JUMP_IF_FALSE   188  'to 188'

 L. 523        52  LOAD_FAST                'sessions_dict'
               54  LOAD_FAST                'subj_bids'
               56  BINARY_SUBSCR    
               58  LOAD_ATTR                keys
               60  CALL_FUNCTION_0       0  ''
               62  STORE_FAST               'sess_available'

 L. 525        64  LOAD_FAST                'visit_id'
               66  LOAD_FAST                'sess_available'
               68  COMPARE_OP               in
               70  POP_JUMP_IF_FALSE   156  'to 156'

 L. 527        72  LOAD_FAST                'bids_field_name'
               74  LOAD_FAST                'sessions_dict'
               76  LOAD_FAST                'subj_bids'
               78  BINARY_SUBSCR    
               80  LOAD_FAST                'visit_id'
               82  BINARY_SUBSCR    
               84  COMPARE_OP               in
               86  POP_JUMP_IF_FALSE   132  'to 132'

 L. 529        88  LOAD_GLOBAL              is_nan
               90  LOAD_FAST                'sessions_dict'
               92  LOAD_FAST                'subj_bids'
               94  BINARY_SUBSCR    
               96  LOAD_FAST                'visit_id'
               98  BINARY_SUBSCR    
              100  LOAD_FAST                'bids_field_name'
              102  BINARY_SUBSCR    
              104  CALL_FUNCTION_1       1  ''
              106  POP_JUMP_IF_FALSE   154  'to 154'

 L. 530       108  LOAD_FAST                'sessions_dict'
              110  LOAD_FAST                'subj_bids'
              112  BINARY_SUBSCR    
              114  LOAD_FAST                'visit_id'
              116  BINARY_SUBSCR    
              118  LOAD_ATTR                update

 L. 531       120  LOAD_FAST                'bids_field_name'
              122  LOAD_FAST                'field_value'
              124  BUILD_MAP_1           1 
              126  CALL_FUNCTION_1       1  ''
              128  POP_TOP          
              130  JUMP_ABSOLUTE       186  'to 186'
              132  ELSE                     '154'

 L. 533       132  LOAD_FAST                'sessions_dict'
              134  LOAD_FAST                'subj_bids'
              136  BINARY_SUBSCR    
              138  LOAD_FAST                'visit_id'
              140  BINARY_SUBSCR    
              142  LOAD_ATTR                update

 L. 534       144  LOAD_FAST                'bids_field_name'
              146  LOAD_FAST                'field_value'
              148  BUILD_MAP_1           1 
              150  CALL_FUNCTION_1       1  ''
              152  POP_TOP          
            154_0  COME_FROM           106  '106'
              154  JUMP_ABSOLUTE       218  'to 218'
              156  ELSE                     '186'

 L. 536       156  LOAD_FAST                'sessions_dict'
              158  LOAD_FAST                'subj_bids'
              160  BINARY_SUBSCR    
              162  LOAD_ATTR                update
              164  LOAD_FAST                'visit_id'
              166  LOAD_STR                 'session_id'
              168  LOAD_STR                 'ses-'
              170  LOAD_FAST                'visit_id'
              172  BINARY_ADD       

 L. 537       174  LOAD_FAST                'bids_field_name'
              176  LOAD_FAST                'field_value'
              178  BUILD_MAP_2           2 
              180  BUILD_MAP_1           1 
              182  CALL_FUNCTION_1       1  ''
              184  POP_TOP          
              186  JUMP_FORWARD        218  'to 218'
              188  ELSE                     '218'

 L. 539       188  LOAD_FAST                'sessions_dict'
              190  LOAD_ATTR                update
              192  LOAD_FAST                'subj_bids'
              194  LOAD_FAST                'visit_id'
              196  LOAD_STR                 'session_id'
              198  LOAD_STR                 'ses-'
              200  LOAD_FAST                'visit_id'
              202  BINARY_ADD       

 L. 540       204  LOAD_FAST                'bids_field_name'
              206  LOAD_FAST                'field_value'
              208  BUILD_MAP_2           2 
              210  BUILD_MAP_1           1 
              212  BUILD_MAP_1           1 
              214  CALL_FUNCTION_1       1  ''
              216  POP_TOP          
            218_0  COME_FROM           186  '186'

 L. 542       218  LOAD_FAST                'sessions_dict'
              220  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `JUMP_ABSOLUTE' instruction at offset 154


def create_adni_sessions_dict(bids_ids, clinic_specs_path, clinical_data_dir, bids_subjs_paths):
    """
    Extract all the data required for the sessions files and organize them in a
    dictionary

    Args: bids_ids: clinic_specs_path: path to the specifications for
    converting the clinical data clinical_data_dir: path to the clinical data
    folder bids_subjs_paths: a list with the path to all the BIDS subjects

    Returns:

    """
    import pandas as pd
    from os import path
    from datetime import datetime
    import clinica.iotools.bids_utils as bids
    from clinica.utils.stream import cprint
    sessions = pd.read_excel(clinic_specs_path, sheetname='sessions.tsv')
    sessions_fields = sessions['ADNI']
    field_location = sessions['ADNI location']
    sessions_fields_bids = sessions['BIDS CLINICA']
    fields_dataset = []
    previous_location = ''
    fields_bids = []
    sessions_dict = {}
    for i in range(0, len(sessions_fields)):
        if not pd.isnull(sessions_fields[i]):
            fields_bids.append(sessions_fields_bids[i])
            fields_dataset.append(sessions_fields[i])

    sessions_df = pd.DataFrame(columns=fields_bids)
    for i in range(0, len(field_location)):
        if not pd.isnull(field_location[i]) and path.exists(path.join(clinical_data_dir, field_location[i].split('/')[0])):
            tmp = field_location[i].split('/')
            location = tmp[0]
            if location != previous_location:
                previous_location = location
                file_to_read_path = path.join(clinical_data_dir, location)
                cprint('\tReading clinical data file : ' + location)
                file_to_read = pd.read_csv(file_to_read_path, dtype=str)
                for r in range(0, len(file_to_read.values)):
                    row = file_to_read.iloc[r]
                    if location == 'ADNIMERGE.csv':
                        id_ref = 'PTID'
                        subj_id = row[id_ref]
                        subj_id = bids.remove_space_and_symbols(subj_id)
                    else:
                        id_ref = 'RID'
                        rid = str(row[id_ref])
                        if 4 - len(rid) > 0:
                            zeros_to_add = 4 - len(rid)
                            subj_id = '0' * zeros_to_add + rid
                        else:
                            subj_id = rid
                    subj_bids = [s for s in bids_ids if subj_id in s]
                    if len(subj_bids) == 0:
                        continue
                    if len(subj_bids) > 1:
                        raise 'Error: multiple subjects found for the same RID'
                    else:
                        subj_bids = subj_bids[0]
                        for j in range(0, len(sessions_fields)):
                            if not pd.isnull(sessions_fields[j]):
                                if location in field_location[i]:
                                    if location == 'ADAS_ADNIGO2.csv' or location == 'DXSUM_PDXCONV_ADNIALL.csv' or location == 'CDR.csv' or location == 'NEUROBAT.csv':
                                        if type(row['VISCODE2']) == float:
                                            pass
                                        else:
                                            visit_id = row['VISCODE2']
                                            if visit_id == 'sc':
                                                visit_id = 'bl'
                                    else:
                                        visit_id = row['VISCODE']
                                try:
                                    field_value = row[sessions_fields[j]]
                                    bids_field_name = sessions_fields_bids[j]
                                    if sessions_fields[j] == 'AGE':
                                        if visit_id != 'bl':
                                            examdate = datetime.strptime(row['EXAMDATE'], '%Y-%m-%d')
                                            examdate_bl = datetime.strptime(row['EXAMDATE_bl'], '%Y-%m-%d')
                                            delta = examdate - examdate_bl
                                            field_value = round(float(field_value) + delta.days / 365.25, 1)
                                    sessions_dict = update_sessions_dict(sessions_dict, subj_bids, visit_id, field_value, bids_field_name)
                                except KeyError:
                                    pass

            continue

    write_adni_sessions_tsv(sessions_dict, fields_bids, bids_subjs_paths)


def create_adni_scans_files(clinic_specs_path, bids_subjs_paths, bids_ids):
    """

    Create scans.tsv files for ADNI

    Args:
        clinic_specs_path: path to the clinical file
        bids_subjs_paths: list of bids subject paths
        bids_ids: list of bids ids

    Returns:

    """
    from glob import glob
    import os, pandas as pd
    from os import path
    from os.path import normpath
    scans_dict = {}
    for bids_id in bids_ids:
        scans_dict.update({bids_id: {'T1/DWI/fMRI':{},  'FDG':{}}})

    scans_specs = pd.read_excel(clinic_specs_path, sheetname='scans.tsv')
    scans_fields_db = scans_specs['ADNI']
    scans_fields_bids = scans_specs['BIDS CLINICA']
    scans_fields_mod = scans_specs['Modalities related']
    fields_bids = ['filename']
    for i in range(0, len(scans_fields_db)):
        if not pd.isnull(scans_fields_db[i]):
            fields_bids.append(scans_fields_bids[i])

    scans_df = pd.DataFrame(columns=fields_bids)
    for bids_subj_path in bids_subjs_paths:
        bids_id = os.path.basename(normpath(bids_subj_path))
        sessions_paths = glob(path.join(bids_subj_path, 'ses-*'))
        for session_path in sessions_paths:
            session_name = session_path.split(os.sep)[(-1)]
            tsv_name = bids_id + '_' + session_name + '_scans.tsv'
            if os.path.exists(path.join(session_path, tsv_name)):
                os.remove(path.join(session_path, tsv_name))
            scans_tsv = open(path.join(session_path, tsv_name), 'a')
            scans_df.to_csv(scans_tsv, sep='\t', index=False, encoding='utf-8')
            mod_available = glob(path.join(session_path, '*'))
            for mod in mod_available:
                mod_name = os.path.basename(mod)
                files = glob(path.join(mod, '*'))
                for file in files:
                    file_name = os.path.basename(file)
                    if mod == 'anat' or mod == 'dwi' or mod == 'func':
                        type_mod = 'T1/DWI/fMRI'
                    else:
                        type_mod = 'FDG'
                    scans_df['filename'] = pd.Series(path.join(mod_name, file_name))
                    scans_df.to_csv(scans_tsv, header=False, sep='\t', index=False, encoding='utf-8')

            scans_df = pd.DataFrame(columns=fields_bids)


def find_image_path(images, source_dir, modality, prefix, id_field):
    from os import path, walk
    import pandas as pd
    from clinica.utils.stream import cprint
    is_dicom = []
    image_folders = []
    for row in images.iterrows():
        image = row[1]
        seq_path = path.join(source_dir, str(image.Subject_ID), image.Sequence)
        image_path = ''
        for dirpath, dirnames, filenames in walk(seq_path):
            found = False
            for d in dirnames:
                if d == prefix + str(image[id_field]):
                    image_path = path.join(dirpath, d)
                    found = True
                    break

            if found:
                break

        dicom = True
        for dirpath, dirnames, filenames in walk(image_path):
            for f in filenames:
                if f.endswith('.nii'):
                    dicom = False
                    image_path = path.join(dirpath, f)
                    break

        is_dicom.append(dicom)
        image_folders.append(image_path)
        if image_path == '':
            cprint('No %s image path found for subject %s in visit %s with image id %s' % (modality, str(image.Subject_ID), str(image.VISCODE), str(image.Image_ID)))

    images.loc[:, 'Is_Dicom'] = pd.Series(is_dicom, index=(images.index))
    images.loc[:, 'Path'] = pd.Series(image_folders, index=(images.index))
    return images


def t1_pet_paths_to_bids(images, bids_dir, modality, mod_to_update=False):
    from multiprocessing import Pool, cpu_count, Value
    from clinica.iotools.converters.adni_to_bids import adni_utils
    from functools import partial
    if modality.lower() not in ('t1', 'fdg', 'pib', 'av45_fbb', 'tau'):
        raise RuntimeError(modality.lower() + ' is not supported for conversion in paths_to_bids')
    counter = None

    def init(args):
        """ store the counter for later use """
        global counter
        counter = args

    counter = Value('i', 0)
    total = images.shape[0]
    images_list = []
    for i in range(total):
        images_list.append(images.iloc[i])

    partial_create_file = partial((adni_utils.create_file), modality=modality,
      total=total,
      bids_dir=bids_dir,
      mod_to_update=mod_to_update)
    poolrunner = Pool((max(cpu_count() - 1, 1)), initializer=init, initargs=(counter,))
    output_file_treated = poolrunner.map(partial_create_file, images_list)
    del counter
    return output_file_treated


def create_file(image, modality, total, bids_dir, mod_to_update):
    import subprocess
    from colorama import Fore
    from clinica.utils.stream import cprint
    from clinica.iotools.converters.adni_to_bids import adni_utils
    from clinica.iotools.utils.data_handling import center_nifti_origin
    from numpy import nan
    import os
    from os import path
    from glob import glob
    modality_specific = {'t1':{'output_path':'anat', 
      'output_filename':'_T1w'}, 
     'fdg':{'output_path':'pet', 
      'output_filename':'_task-rest_acq-fdg_pet'}, 
     'pib':{'output_path':'pet', 
      'output_filename':'_task-rest_acq-pib_pet'}, 
     'av45':{'output_path':'pet', 
      'output_filename':'_task-rest_acq-av45_pet'}, 
     'fbb':{'output_path':'pet', 
      'output_filename':'_task-rest_acq-fbb_pet'}, 
     'tau':{'output_path':'pet', 
      'output_filename':'_task-rest_acq-tau_pet'}}
    with counter.get_lock():
        counter.value += 1
    subject = image.Subject_ID
    if modality == 'av45_fbb':
        modality = image.Tracer.lower()
    if image.Path == '':
        cprint(Fore.RED + '[' + modality.upper() + '] No path specified for ' + image.Subject_ID + ' in session ' + image.VISCODE + ' ' + str(counter.value) + ' / ' + str(total) + Fore.RESET)
        return nan
    else:
        cprint('[' + modality.upper() + '] Processing subject ' + str(subject) + ' - session ' + image.VISCODE + ', ' + str(counter.value) + ' / ' + str(total))
        session = adni_utils.viscode_to_session(image.VISCODE)
        image_path = image.Path
        image_id = image.Image_ID
        if image.Is_Dicom:
            image_path = adni_utils.check_two_dcm_folder(image_path, bids_dir, image_id)
        bids_subj = subject.replace('_', '')
        output_path = path.join(bids_dir, 'sub-ADNI' + bids_subj, 'ses-' + session, modality_specific[modality]['output_path'])
        output_filename = 'sub-ADNI' + bids_subj + '_ses-' + session + modality_specific[modality]['output_filename']
        existing_im = glob(path.join(output_path, output_filename + '*'))
        if mod_to_update:
            if len(existing_im) > 0:
                print('Removing the old image...')
                for im in existing_im:
                    os.remove(im)

        try:
            os.makedirs(output_path)
        except OSError:
            pass

        if image.Is_Dicom:
            command = 'dcm2niix -b n -z n -o ' + output_path + ' -f ' + output_filename + ' ' + image_path
            subprocess.run(command, shell=True,
              stderr=(subprocess.DEVNULL),
              stdout=(subprocess.DEVNULL))
            nifti_file = path.join(output_path, output_filename + '.nii')
            output_image = nifti_file + '.gz'
            if not path.isfile(nifti_file):
                cprint('\tConversion with dcm2niix failed, trying with dcm2nii')
                command = 'dcm2nii -a n -d n -e n -i y -g n -p n -m n -r n -x n -o ' + output_path + ' ' + image_path
                subprocess.run(command, shell=True,
                  stdout=(subprocess.DEVNULL),
                  stderr=(subprocess.DEVNULL))
                nifti_file = path.join(output_path, subject.replace('_', '') + '.nii')
                output_image = path.join(output_path, output_filename + '.nii.gz')
                if not path.isfile(nifti_file):
                    cprint('DICOM to NIFTI conversion error for ' + image_path)
                    return nan
            center_nifti_origin(nifti_file, output_image)
            os.remove(nifti_file)
        else:
            output_image = path.join(output_path, output_filename + '.nii.gz')
            center_nifti_origin(image_path, output_image)
        if output_image is None:
            cprint('Error: For subject %s in session%s an error occurred recentering Nifti image:%s' % (
             subject, session, image_path))
        adni_utils.remove_tmp_dmc_folder(bids_dir, image_id)
        return output_image