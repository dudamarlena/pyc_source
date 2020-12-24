# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/user/PycharmProjects/simple_NER/simple_NER/annotators/medacy_ner.py
# Compiled at: 2019-12-12 21:17:29
# Size of source mod 2**32: 1053 bytes
from simple_NER.annotators import NERWrapper
from simple_NER import Entity
try:
    from medacy.ner.model import Model
except ImportError:
    print('you need to install medacy and download the model')
    print('pip install git+https://github.com/NLPatVCU/medaCy.git')
    print('pip install git+https://github.com/NLPatVCU/medaCy_model_clinical_notes.git')
    raise

class MedacyNER(NERWrapper):

    def __init__(self, model='medacy_model_clinical_notes'):
        super().__init__()
        self.add_detector(self.annotate)
        self.model = Model.load_external(model)

    def annotate(self, text):
        annotation = self.model.predict(text).__dict__['annotations']
        for entity in annotation['entities']:
            label, start, end, text = annotation['entities'][entity]
            yield Entity(text, label, source_text=text)


if __name__ == '__main__':
    ner = MedacyNER()
    text = 'The patient was prescribed 1 capsule of Advil for 5 days.'
    for e in ner.extract_entities(text):
        print(e.value, e.entity_type)