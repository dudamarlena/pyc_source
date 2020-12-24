# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/omkarpathak27/Documents/GITS/py-resume-parser/pyresparser/resume_parser.py
# Compiled at: 2019-11-30 21:44:11
# Size of source mod 2**32: 4503 bytes
import os, multiprocessing as mp, io, spacy, pprint
from spacy.matcher import Matcher
from . import utils

class ResumeParser(object):

    def __init__(self, resume, skills_file=None, custom_regex=None):
        nlp = spacy.load('en_core_web_sm')
        custom_nlp = spacy.load(os.path.dirname(os.path.abspath(__file__)))
        self._ResumeParser__skills_file = skills_file
        self._ResumeParser__custom_regex = custom_regex
        self._ResumeParser__matcher = Matcher(nlp.vocab)
        self._ResumeParser__details = {'name':None, 
         'email':None, 
         'mobile_number':None, 
         'skills':None, 
         'college_name':None, 
         'degree':None, 
         'designation':None, 
         'experience':None, 
         'company_names':None, 
         'no_of_pages':None, 
         'total_experience':None}
        self._ResumeParser__resume = resume
        if not isinstance(self._ResumeParser__resume, io.BytesIO):
            ext = os.path.splitext(self._ResumeParser__resume)[1].split('.')[1]
        else:
            ext = self._ResumeParser__resume.name.split('.')[1]
        self._ResumeParser__text_raw = utils.extract_text(self._ResumeParser__resume, '.' + ext)
        self._ResumeParser__text = ' '.join(self._ResumeParser__text_raw.split())
        self._ResumeParser__nlp = nlp(self._ResumeParser__text)
        self._ResumeParser__custom_nlp = custom_nlp(self._ResumeParser__text_raw)
        self._ResumeParser__noun_chunks = list(self._ResumeParser__nlp.noun_chunks)
        self._ResumeParser__get_basic_details()

    def get_extracted_data(self):
        return self._ResumeParser__details

    def __get_basic_details(self):
        cust_ent = utils.extract_entities_wih_custom_model(self._ResumeParser__custom_nlp)
        name = utils.extract_name((self._ResumeParser__nlp), matcher=(self._ResumeParser__matcher))
        email = utils.extract_email(self._ResumeParser__text)
        mobile = utils.extract_mobile_number(self._ResumeParser__text, self._ResumeParser__custom_regex)
        skills = utils.extract_skills(self._ResumeParser__nlp, self._ResumeParser__noun_chunks, self._ResumeParser__skills_file)
        entities = utils.extract_entity_sections_grad(self._ResumeParser__text_raw)
        try:
            self._ResumeParser__details['name'] = cust_ent['Name'][0]
        except (IndexError, KeyError):
            self._ResumeParser__details['name'] = name

        self._ResumeParser__details['email'] = email
        self._ResumeParser__details['mobile_number'] = mobile
        self._ResumeParser__details['skills'] = skills
        try:
            self._ResumeParser__details['college_name'] = entities['College Name']
        except KeyError:
            pass

        try:
            self._ResumeParser__details['degree'] = cust_ent['Degree']
        except KeyError:
            pass

        try:
            self._ResumeParser__details['designation'] = cust_ent['Designation']
        except KeyError:
            pass

        try:
            self._ResumeParser__details['company_names'] = cust_ent['Companies worked at']
        except KeyError:
            pass

        try:
            self._ResumeParser__details['experience'] = entities['experience']
            try:
                exp = round(utils.get_total_experience(entities['experience']) / 12, 2)
                self._ResumeParser__details['total_experience'] = exp
            except KeyError:
                self._ResumeParser__details['total_experience'] = 0

        except KeyError:
            self._ResumeParser__details['total_experience'] = 0

        self._ResumeParser__details['no_of_pages'] = utils.get_number_of_pages(self._ResumeParser__resume)


def resume_result_wrapper(resume):
    parser = ResumeParser(resume)
    return parser.get_extracted_data()


if __name__ == '__main__':
    pool = mp.Pool(mp.cpu_count())
    resumes = []
    data = []
    for root, directories, filenames in os.walk('resumes'):
        for filename in filenames:
            file = os.path.join(root, filename)
            resumes.append(file)

    results = [pool.apply_async(resume_result_wrapper, args=(x,)) for x in resumes]
    results = [p.get() for p in results]
    pprint.pprint(results)