# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-intel/egg/genonets/genonets_reader.py
# Compiled at: 2017-01-24 10:46:26
"""
    genonets_reader
    ~~~~~~~~~~~~~~~

    Parser for the genonets input file format.

    :author: Fahad Khalid
    :license: MIT, see LICENSE for more details.
"""
import csv
from genonets_exceptions import GenonetsError
from genonets_constants import ErrorCodes
from genonets_constants import SupportedAlphabet

class InReader:

    def __init__(self):
        pass

    COL_HEADERS = [
     'Genotypeset', 'Delta', 'Genotype', 'Score']

    @staticmethod
    def build_data_dicts(in_file_path, tau, alphabet_type):
        data_dict = {}
        delta_dict = {}
        genotypes = []
        genotype_sets = []
        genotype_length = 0
        reader, in_file = InReader.dict_reader_for_file(in_file_path)
        if not InReader.req_hdrs_are_present(reader.fieldnames):
            in_file.close()
            print 'Error: ' + ErrorCodes.getErrDescription(ErrorCodes.INCONSISTENT_HEADER)
            raise GenonetsError(ErrorCodes.INCONSISTENT_HEADER)
        for row in reader:
            if any(row[col] in (None, '') for col in row.keys()):
                in_file.close()
                line_number = str(int(reader.line_num))
                print 'Error: ' + ErrorCodes.getErrDescription(ErrorCodes.MISSING_VALUE) + ': Line No. ' + line_number
                raise GenonetsError(ErrorCodes.MISSING_VALUE, 'Line No. ' + line_number)
            try:
                score = float(row['Score'])
            except:
                in_file.close()
                line_number = str(int(reader.line_num))
                print 'Error: ' + ErrorCodes.getErrDescription(ErrorCodes.BAD_SCORE_FORMAT) + ': Line No. ' + line_number
                raise GenonetsError(ErrorCodes.BAD_SCORE_FORMAT, 'Line No. ' + line_number)

            if score >= tau:
                if row['Genotypeset'] not in data_dict:
                    data_dict[row['Genotypeset']] = {}
                    genotype_sets.append(row['Genotypeset'])
                    try:
                        delta = float(row['Delta'])
                    except:
                        in_file.close()
                        line_number = str(int(reader.line_num))
                        print 'Error: ' + ErrorCodes.getErrDescription(ErrorCodes.BAD_DELTA_FORMAT) + ': Line No. ' + line_number
                        raise GenonetsError(ErrorCodes.BAD_DELTA_FORMAT, 'Line No. ' + line_number)

                    delta_dict[row['Genotypeset']] = delta
                genotype = row['Genotype']
                if genotype_length == 0:
                    genotype_length = len(genotype)
                try:
                    InReader.verify_genotype(genotype, genotype_length, alphabet_type, str(int(reader.line_num)))
                except Exception as e:
                    in_file.close()
                    raise e

                data_dict[row['Genotypeset']][genotype] = score
                if genotype not in genotypes:
                    genotypes.append(genotype)

        in_file.close()
        if not data_dict:
            print 'Error: ' + ErrorCodes.getErrDescription(ErrorCodes.NO_USABLE_SCORES) + ': Tau=' + str(tau)
            raise GenonetsError(ErrorCodes.NO_USABLE_SCORES, 'Tau=' + str(tau))
        genotype_to_set_dict = InReader.build_genotype_to_set_dict(genotypes, data_dict)
        return (
         data_dict, delta_dict, genotype_to_set_dict, genotype_length, genotype_sets)

    @staticmethod
    def build_genotype_to_set_dict(genotypes, data_dict):
        genotype_to_set_dict = {}
        for seq in genotypes:
            genotype_to_set_dict[seq] = []
            for rep in data_dict.keys():
                if seq in data_dict[rep]:
                    genotype_to_set_dict[seq].append(rep)

        return genotype_to_set_dict

    @staticmethod
    def req_hdrs_are_present(col_names):
        cols_in_file = [ col for col in col_names ]
        if any(header not in cols_in_file for header in InReader.COL_HEADERS):
            return False
        return True

    @staticmethod
    def verify_genotype(genotype, genotype_length, alphabet_type, line_number):
        if len(genotype) != genotype_length:
            print 'Error: ' + ErrorCodes.getErrDescription(ErrorCodes.INCONSISTENT_SEQ_LEN) + ': Line No. ' + line_number
            raise GenonetsError(ErrorCodes.INCONSISTENT_SEQ_LEN, 'Line No. ' + line_number)
        alphabet = SupportedAlphabet.getAlphabet(alphabet_type)
        if any(letter not in alphabet for letter in genotype):
            print 'Error: ' + ErrorCodes.getErrDescription(ErrorCodes.ALPHABET_TYPE_MISMATCH) + ': Line No. ' + line_number
            raise GenonetsError(ErrorCodes.ALPHABET_TYPE_MISMATCH, 'Line No. ' + line_number)

    @staticmethod
    def dict_reader_for_file(file_name):
        try:
            data_file = open(file_name, 'rU')
        except Exception as e:
            print 'Error: ' + ErrorCodes.getErrDescription(ErrorCodes.UNKNOWN_PARSING_ERROR)
            raise GenonetsError(ErrorCodes.UNKNOWN_PARSING_ERROR)

        reader = csv.DictReader(data_file, delimiter='\t')
        return (
         reader, data_file)