# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/mdiazmel/code/aramis/clinica/clinica/iotools/converters/adni_to_bids/adni_modalities/adni_t1.py
# Compiled at: 2019-10-10 04:46:11
# Size of source mod 2**32: 23875 bytes
__doc__ = '\n Module for converting T1 of ADNI\n'
__author__ = 'Jorge Samper-Gonzalez'
__copyright__ = 'Copyright 2016-2019 The Aramis Lab Team'
__credits__ = ['Sabrina Fontanella']
__license__ = 'See LICENSE.txt file'
__version__ = '0.1.0'
__maintainer__ = 'Jorge Samper-Gonzalez'
__email__ = 'jorge.samper-gonzalez@inria.fr'
__status__ = 'Development'

def convert_adni_t1(source_dir, csv_dir, dest_dir, subjs_list=None):
    """
    Convert T1 MR images of ADNI into BIDS format

    Args:
        source_dir: path to the ADNI directory
        csv_dir: path to the clinical data directory
        dest_dir: path to the destination BIDS directory
        subjs_list: subjects list

    """
    from os import path
    from pandas.io import parsers
    from colorama import Fore
    from clinica.utils.stream import cprint
    from clinica.iotools.converters.adni_to_bids.adni_utils import t1_pet_paths_to_bids
    if subjs_list is None:
        adni_merge_path = path.join(csv_dir, 'ADNIMERGE.csv')
        adni_merge = parsers.read_csv(adni_merge_path, sep=',', low_memory=False)
        subjs_list = list(adni_merge.PTID.unique())
    cprint('Calculating paths of T1 images. Output will be stored in ' + path.join(dest_dir, 'conversion_info') + '.')
    images = compute_t1_paths(source_dir, csv_dir, dest_dir, subjs_list)
    cprint('Paths of T1 images found. Exporting images into BIDS ...')
    t1_pet_paths_to_bids(images, dest_dir, 't1')
    cprint(Fore.GREEN + 'T1 conversion done.' + Fore.RESET)


def compute_t1_paths(source_dir, csv_dir, dest_dir, subjs_list):
    """
    Compute the paths to T1 MR images and store them in a tsv file

    Args:
        source_dir: path to the ADNI directory
        csv_dir: path to the clinical data directory
        dest_dir: path to the destination BIDS directory
        subjs_list: subjects list

    Returns:
        images: a dataframe with all the paths to the T1 MR images that will be converted into BIDS

    """
    import operator
    from functools import reduce
    from os import path, makedirs
    import pandas as pd
    from clinica.utils.stream import cprint
    from clinica.iotools.converters.adni_to_bids.adni_utils import find_image_path
    t1_col_df = [
     'Subject_ID', 'VISCODE', 'Visit', 'Sequence', 'Scan_Date',
     'Study_ID', 'Field_Strength', 'Series_ID', 'Image_ID', 'Original']
    t1_df = pd.DataFrame(columns=t1_col_df)
    adni_merge = pd.read_csv((path.join(csv_dir, 'ADNIMERGE.csv')), sep=',', low_memory=False)
    mprage_meta = pd.read_csv((path.join(csv_dir, 'MPRAGEMETA.csv')), sep=',', low_memory=False)
    mri_quality = pd.read_csv((path.join(csv_dir, 'MRIQUALITY.csv')), sep=',', low_memory=False)
    mayo_mri_qc = pd.read_csv((path.join(csv_dir, 'MAYOADIRL_MRI_IMAGEQC_12_08_15.csv')), sep=',', low_memory=False)
    mayo_mri_qc = mayo_mri_qc[(mayo_mri_qc.series_type == 'T1')]
    for subj in subjs_list:
        adnimerge_subj = adni_merge[(adni_merge.PTID == subj)]
        adnimerge_subj = adnimerge_subj.sort_values('EXAMDATE')
        mprage_meta_subj = mprage_meta[(mprage_meta.SubjectID == subj)]
        mprage_meta_subj = mprage_meta_subj.sort_values('ScanDate')
        mri_quality_subj = mri_quality[(mri_quality.RID == int(subj[-4:]))]
        mayo_mri_qc_subj = mayo_mri_qc[(mayo_mri_qc.RID == int(subj[-4:]))]
        visits = visits_to_timepoints_t1(subj, mprage_meta_subj, adnimerge_subj)
        for visit_info in visits.keys():
            cohort = visit_info[1]
            timepoint = visit_info[0]
            visit_str = visits[visit_info]
            image_dict = None
            if cohort in ('ADNI1', 'ADNIGO', 'ADNI2'):
                image_dict = adni1GO2_image(subj, timepoint, visit_str, mprage_meta_subj, mri_quality_subj, mayo_mri_qc_subj,
                  preferred_field_strength=(1.5 if cohort == 'ADNI1' else 3.0))
            else:
                if cohort == 'ADNI3':
                    image_dict = adni3_image(subj, timepoint, visit_str, mprage_meta_subj, mayo_mri_qc_subj)
                else:
                    cprint('Subject %s visit %s belongs to an unknown cohort: %s' % (subj, visit_str, cohort))
            if image_dict is None:
                image_dict = {'Subject_ID':subj, 
                 'VISCODE':visit_info[0], 
                 'Visit':visits[visit_info], 
                 'Sequence':'', 
                 'Scan_Date':'', 
                 'Study_ID':'', 
                 'Series_ID':'', 
                 'Image_ID':'', 
                 'Field_Strength':'', 
                 'Original':True}
            row_to_append = pd.DataFrame(image_dict, index=['i'])
            t1_df = t1_df.append(row_to_append, ignore_index=True)

    conversion_errors = [
     ('031_S_0830', 'm48'),
     ('100_S_0995', 'm18'),
     ('031_S_0867', 'm48'),
     ('100_S_0892', 'm18'),
     ('029_S_0845', 'm24'),
     ('094_S_1267', 'm24'),
     ('029_S_0843', 'm24'),
     ('027_S_0307', 'm48'),
     ('057_S_1269', 'm24'),
     ('036_S_4899', 'm03'),
     ('033_S_1016', 'm120'),
     ('130_S_4984', 'm12'),
     ('027_S_4802', 'm06'),
     ('131_S_0409', 'bl'),
     ('082_S_4224', 'm24'),
     ('006_S_4960', 'bl'),
     ('006_S_4960', 'm03'),
     ('006_S_4960', 'm06'),
     ('006_S_4960', 'm12'),
     ('006_S_4960', 'm24'),
     ('006_S_4960', 'm36'),
     ('006_S_4960', 'm72'),
     ('022_S_5004', 'bl'),
     ('022_S_5004', 'm03'),
     ('006_S_4485', 'm84')]
    error_indices = []
    for conv_error in conversion_errors:
        error_indices.append((t1_df.Subject_ID == conv_error[0]) & (t1_df.VISCODE == conv_error[1]))

    if error_indices:
        indices_to_remove = t1_df.index[reduce(operator.or_, error_indices, False)]
        t1_df.drop(indices_to_remove, inplace=True)
    images = find_image_path(t1_df, source_dir, 'T1', 'S', 'Series_ID')
    t1_tsv_path = path.join(dest_dir, 'conversion_info')
    if not path.exists(t1_tsv_path):
        makedirs(t1_tsv_path)
    images.to_csv((path.join(t1_tsv_path, 't1_paths.tsv')), sep='\t', index=False)
    return images


def adni1GO2_image(subject_id, timepoint, visit_str, mprage_meta_subj, mri_quality_subj, mayo_mri_qc_subj, preferred_field_strength=3.0):
    from clinica.iotools.converters.adni_to_bids.adni_utils import replace_sequence_chars
    filtered_mprage = mprage_meta_subj[((mprage_meta_subj['Orig/Proc'] == 'Processed') & (mprage_meta_subj.Visit == visit_str) & mprage_meta_subj.Sequence.map(lambda x: x.endswith('Scaled')))]
    if filtered_mprage.shape[0] < 1:
        filtered_mprage = mprage_meta_subj[((mprage_meta_subj['Orig/Proc'] == 'Processed') & (mprage_meta_subj.Visit == visit_str) & mprage_meta_subj.Sequence.map(lambda x: x.endswith('N3m')))]
        if filtered_mprage.shape[0] < 1:
            return original_image(subject_id, timepoint, visit_str, mprage_meta_subj, mayo_mri_qc_subj, preferred_field_strength)
        if len(filtered_mprage.MagStrength.unique()) > 1:
            filtered_mprage = filtered_mprage[(filtered_mprage.MagStrength == preferred_field_strength)]
        filtered_mprage = filtered_mprage.sort_values('SeriesID')
        scan = filtered_mprage.iloc[0]
        return check_qc(scan, subject_id, visit_str, mprage_meta_subj, mri_quality_subj) or None
    else:
        n3 = scan.Sequence.find('N3')
        sequence = scan.Sequence[:n3 + 2 + int(scan.Sequence[(n3 + 2)] == 'm')]
        sequence = replace_sequence_chars(sequence)
        return {'Subject_ID':subject_id, 
         'VISCODE':timepoint, 
         'Visit':visit_str, 
         'Sequence':sequence, 
         'Scan_Date':scan.ScanDate, 
         'Study_ID':str(scan.StudyID), 
         'Series_ID':str(scan.SeriesID), 
         'Image_ID':str(scan.ImageUID), 
         'Field_Strength':scan.MagStrength, 
         'Original':False}


def original_image(subject_id, timepoint, visit_str, mprage_meta_subj, mayo_mri_qc_subj, preferred_field_strength=3.0):
    from clinica.iotools.converters.adni_to_bids.adni_utils import replace_sequence_chars
    from clinica.utils.stream import cprint
    mprage_meta_subj_orig = mprage_meta_subj[(mprage_meta_subj['Orig/Proc'] == 'Original')]
    cond_mprage = (mprage_meta_subj_orig.Visit == visit_str) & mprage_meta_subj_orig.Sequence.map(lambda x: ((x.lower().find('mprage') > -1) | (x.lower().find('mp-rage') > -1) | (x.lower().find('mp rage') > -1)) & (x.find('2') < 0))
    cond_spgr = (mprage_meta_subj_orig.Visit == visit_str) & mprage_meta_subj_orig.Sequence.map(lambda x: (x.lower().find('spgr') > -1) & (x.lower().find('acc') < 0))
    filtered_scan = mprage_meta_subj_orig[(cond_mprage | cond_spgr)]
    if filtered_scan.shape[0] < 1:
        cprint('NO MPRAGE Meta: ' + subject_id + ' for visit ' + timepoint + ' - ' + visit_str)
        return
    else:
        scan = select_scan_qc_adni2(filtered_scan, mayo_mri_qc_subj, preferred_field_strength)
        sequence = replace_sequence_chars(scan.Sequence)
        return {'Subject_ID':subject_id, 
         'VISCODE':timepoint, 
         'Visit':visit_str, 
         'Sequence':sequence, 
         'Scan_Date':scan.ScanDate, 
         'Study_ID':str(scan.StudyID), 
         'Series_ID':str(scan.SeriesID), 
         'Image_ID':str(scan.ImageUID), 
         'Field_Strength':scan.MagStrength, 
         'Original':True}


def adni3_image(subject_id, timepoint, visit_str, mprage_meta_subj, mayo_mri_qc_subj):
    from clinica.iotools.converters.adni_to_bids.adni_utils import replace_sequence_chars
    from clinica.utils.stream import cprint
    filtered_scan = mprage_meta_subj[((mprage_meta_subj['Orig/Proc'] == 'Original') & (mprage_meta_subj.Visit == visit_str) & mprage_meta_subj.Sequence.map(lambda x: (x.lower().find('accel') > -1) & ~x.lower().endswith('_ND')))]
    if filtered_scan.shape[0] < 1:
        cprint('NO MPRAGE Meta for ADNI3: ' + subject_id + ' for visit ' + timepoint + ' - ' + visit_str)
        return
    else:
        scan = select_scan_qc_adni2(filtered_scan, mayo_mri_qc_subj, preferred_field_strength=3.0)
        sequence = replace_sequence_chars(scan.Sequence)
        return {'Subject_ID':subject_id, 
         'VISCODE':timepoint, 
         'Visit':visit_str, 
         'Sequence':sequence, 
         'Scan_Date':scan.ScanDate, 
         'Study_ID':str(scan.StudyID), 
         'Series_ID':str(scan.SeriesID), 
         'Image_ID':str(scan.ImageUID), 
         'Field_Strength':scan.MagStrength, 
         'Original':True}


def check_qc(scan, subject_id, visit_str, mprage_meta_subj, mri_quality_subj):
    from clinica.utils.stream import cprint
    series_id = scan.SeriesID
    qc_passed = True
    qc = mri_quality_subj[(mri_quality_subj.LONIUID == 'S' + str(scan.SeriesID))]
    if qc.shape[0] > 0:
        if qc.iloc[0].PASS != 1:
            cprint('QC found but NOT passed')
            cprint('Subject ' + subject_id + ' - Series: ' + str(scan.SeriesID) + ' - Study: ' + str(scan.StudyID))
            mprage_meta_subj_alt = mprage_meta_subj[((mprage_meta_subj['Orig/Proc'] == 'Original') & (mprage_meta_subj.Visit == visit_str) & (mprage_meta_subj.SeriesID != series_id))]
            qc_prev_sequence = scan.Sequence
            scan = mprage_meta_subj_alt.iloc[0]
            series_id = scan.SeriesID
            qc_passed = False
    if not qc_passed:
        if scan.Sequence == 'MP-RAGE':
            original_img_seq = 'MPR'
        else:
            original_img_seq = 'MPR-R'
        processing_seq = qc_prev_sequence[qc_prev_sequence.find(';'):qc_prev_sequence.find('Scaled') - 2]
        sequence = original_img_seq + processing_seq
    qc = mri_quality_subj[(mri_quality_subj.LONIUID == 'S' + str(scan.SeriesID))]
    if qc.shape[0] > 0 and qc.iloc[0].PASS != 1:
        cprint('QC found but NOT passed')
        cprint('Subject ' + subject_id + ' - Series: ' + str(scan.SeriesID) + ' - Study: ' + str(scan.StudyID))
        return False
    else:
        return True


def visits_to_timepoints_t1(subject, mprage_meta_subj_orig, adnimerge_subj):
    from datetime import datetime
    from clinica.iotools.converters.adni_to_bids.adni_utils import days_between
    from clinica.utils.stream import cprint
    mprage_meta_subj_orig = mprage_meta_subj_orig[(mprage_meta_subj_orig['Visit'] != 'ADNI Baseline')]
    visits = dict()
    unique_visits = list(mprage_meta_subj_orig.Visit.unique())
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
                        cprint('[T1] Subject ' + subject + ' has multiple visits for one timepoint. ')
                unique_visits.remove(preferred_visit_name)
            else:
                pending_timepoints.append(visit)

    for visit in unique_visits:
        image = mprage_meta_subj_orig[(mprage_meta_subj_orig.Visit == visit)].iloc[0]
        min_db = 100000
        min_db2 = 0
        min_visit = None
        min_visit2 = None
        for timepoint in pending_timepoints:
            db = days_between(image.ScanDate, timepoint.EXAMDATE)
            if db < min_db:
                min_db2 = min_db
                min_visit2 = min_visit
                min_db = db
                min_visit = timepoint

        if min_visit is None:
            cprint('No corresponding timepoint in ADNIMERGE for subject ' + subject + ' in visit ' + image.Visit)
            cprint(image)
            continue
        if min_visit2 is not None and min_db > 90:
            cprint('More than 60 days for corresponding timepoint in ADNIMERGE for subject ' + subject + ' in visit ' + image.Visit + ' on ' + image.ScanDate)
            cprint('Timepoint 1: ' + min_visit.VISCODE + ' - ' + min_visit.ORIGPROT + ' on ' + min_visit.EXAMDATE + ' (Distance: ' + str(min_db) + ' days)')
            cprint('Timepoint 2: ' + min_visit2.VISCODE + ' - ' + min_visit2.ORIGPROT + ' on ' + min_visit2.EXAMDATE + ' (Distance: ' + str(min_db2) + ' days)')
            if datetime.strptime(min_visit.EXAMDATE, '%Y-%m-%d') > datetime.strptime(image.ScanDate, '%Y-%m-%d') > datetime.strptime(min_visit2.EXAMDATE, '%Y-%m-%d'):
                dif = days_between(min_visit.EXAMDATE, min_visit2.EXAMDATE)
                if abs(dif / 2.0 - min_db) < 30:
                    min_visit = min_visit2
                cprint('We prefer ' + min_visit.VISCODE)
            else:
                key_min_visit = (
                 min_visit.VISCODE, min_visit.COLPROT, min_visit.ORIGPROT)
                if key_min_visit not in visits.keys():
                    visits[key_min_visit] = image.Visit
                elif visits[key_min_visit] != image.Visit:
                    cprint('[T1] Subject ' + subject + ' has multiple visits for one timepoint.')

    return visits


def select_scan_no_qc(scans_meta):
    selected_scan = scans_meta[scans_meta.Sequence.map(lambda x: x.lower().find('repeat') < 0)]
    if selected_scan.shape[0] < 1:
        selected_scan = scans_meta
    scan = selected_scan.iloc[0]
    return scan


def select_scan_qc_adni2(scans_meta, mayo_mri_qc_subj, preferred_field_strength):
    import numpy as np
    multiple_mag_strength = False
    if len(scans_meta.MagStrength.unique()) > 1:
        multiple_mag_strength = True
        not_preferred_scan = scans_meta[(scans_meta.MagStrength != preferred_field_strength)]
        scans_meta = scans_meta[(scans_meta.MagStrength == preferred_field_strength)]
    if scans_meta.MagStrength.unique()[0] == 3.0:
        id_list = scans_meta.ImageUID.unique()
        image_ids = ['I' + str(imageuid) for imageuid in id_list]
        int_ids = [int(imageuid) for imageuid in id_list]
        images_qc = mayo_mri_qc_subj[mayo_mri_qc_subj.loni_image.isin(image_ids)]
        if images_qc.shape[0] > 0:
            selected_image = None
            if np.sum(images_qc.series_selected) == 1:
                selected_image = images_qc[(images_qc.series_selected == 1)].iloc[0].loni_image[1:]
            else:
                images_not_rejected = images_qc[(images_qc.series_quality < 4)]
            if images_not_rejected.shape[0] < 1:
                qc_ids = set([int(qc_id[1:]) for qc_id in images_qc.loni_image.unique()])
                no_qc_ids = list(set(int_ids) - qc_ids)
                if len(no_qc_ids) > 0:
                    no_qc_scans_meta = scans_meta[scans_meta.ImageUID.isin(no_qc_ids)]
                    return select_scan_no_qc(no_qc_scans_meta)
            else:
                series_quality = [q if q > 0 else 4 for q in list(images_not_rejected.series_quality)]
                best_q = np.amin(series_quality)
                if best_q == 4:
                    best_q = -1
                else:
                    images_best_qc = images_not_rejected[(images_not_rejected.series_quality == best_q)]
                    if images_best_qc.shape[0] == 1:
                        selected_image = images_best_qc.iloc[0].loni_image[1:]
                    else:
                        best_ids = [int(x[1:]) for x in images_best_qc.loni_image.unique()]
                        best_qc_meta = scans_meta[scans_meta.ImageUID.isin(best_ids)]
                        return select_scan_no_qc(best_qc_meta)
                    if selected_image is None and multiple_mag_strength:
                        scans_meta = not_preferred_scan
                    else:
                        scan = scans_meta[(scans_meta.ImageUID == int(selected_image))].iloc[0]
                        return scan
    return select_scan_no_qc(scans_meta)


def check_exceptions(bids_dir):
    from os import path
    import pandas as pd
    from glob import glob
    t1_paths = pd.read_csv((path.join(bids_dir, 'conversion_info', 't1_paths.tsv')), sep='\t')
    t1_paths = t1_paths[t1_paths.Path.notnull()]
    t1_paths['BIDS_SubjID'] = ['sub-ADNI' + s.replace('_', '') for s in t1_paths.Subject_ID.to_list()]
    t1_paths['BIDS_Session'] = ['ses-' + s.replace('bl', 'm00').upper() for s in t1_paths.VISCODE.to_list()]
    count = 0
    for r in t1_paths.iterrows():
        image = r[1]
        image_dir = path.join(bids_dir, image.BIDS_SubjID, image.BIDS_Session, 'anat')
        image_pattern = path.join(image_dir, '*')
        files_list = glob(image_pattern)
        if not files_list:
            print('No images for subject %s in session %s' % (image.BIDS_SubjID, image.BIDS_Session))
            count += 1
        else:
            if len(files_list) > 1:
                print('Too many images for subject %s in session %s' % (image.BIDS_SubjID, image.BIDS_Session))
                print(files_list)

    print(count)