# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/gerardo/Projects/nlp_model_gen/nlp_model_gen/packages/modelManager/model/Model.py
# Compiled at: 2019-06-14 18:07:58
# Size of source mod 2**32: 9823 bytes
from collections import defaultdict, Counter
from nlp_model_gen.utils.objectUtils import transform_dict_key_data_to_int
from nlp_model_gen.packages.logger.Logger import Logger
from nlp_model_gen.packages.errorHandler.ErrorHandler import ErrorHandler
from nlp_model_gen.constants.constants import TEXT_LENGTH_THRESHOLD
from ..analyzerException.AnalyzerException import AnalyzerException
from ..modelLoader.ModelLoader import ModelLoader
from ..token.Token import Token
from ..entity.Entity import Entity
from ..analyzer.Analyzer import Analyzer

class Model:

    def __init__(self, model_id, model_name, description, author, path, analyzer_rules_set, analyzer_exceptions_set):
        self._Model__model_id = model_id
        self._Model__model_name = model_name
        self._Model__description = description
        self._Model__author = author
        self._Model__path = path
        self._Model__analyzer_rules_set = analyzer_rules_set
        self._Model__analyzer_exceptions_set = analyzer_exceptions_set
        self._Model__reference = None
        self._Model__loaded = False

    def get_model_id(self):
        return self._Model__model_id

    def get_model_name(self):
        return self._Model__model_name

    def get_description(self):
        return self._Model__description

    def get_author(self):
        return self._Model__author

    def get_path(self):
        return self._Model__path

    def get_analyser_rules_set(self):
        return self._Model__analyzer_rules_set

    def get_analyzer_exceptions_set(self):
        return self._Model__analyzer_exceptions_set

    def get_reference(self):
        return self._Model__reference

    def set_model_name(self, model_name):
        self._Model__model_name = model_name

    def set_description(self, description):
        self._Model__description = description

    def set_reference(self, reference):
        self._Model__reference = reference

    def is_loaded(self):
        return self._Model__loaded

    def __get_model_ner(self):
        """
        Devuelve el NER del modelo si existe o un NER en blanco en caso que no exista.

        :return: [SpacyNER] - NER del modelo. Si el modelo no estuviese cargado devuelve
        None.
        """
        if not self.is_loaded():
            return
        else:
            return ModelLoader.get_model_ner(self._Model__reference)

    def __build_tokenizer_results(self, tokenizer_dectections, token_count):
        """
        Crea un diccionario con los resultados del procesamiento de los datos obtenidos
        del análisis del tokenizer.

        :tokenizer_detections: [List(Dict)] - Tokens detectados.

        :token_count: [Dict(Counter)] - Conteo de tokens por categoria.

        :return: [Dict] - Resultados procesados.
        """
        token_frequency = dict()
        for key in token_count.keys():
            token_frequency[key] = token_count[key].most_common()

        return {'token_frequency':dict(token_frequency),  'tokenizer_results':tokenizer_dectections}

    def __process_tokenizer_results(self, doc, only_positives=False):
        """
        Procesa los resultados del analisis de un texto almacenados en un doc de spacy en función de los
        resultados del tokenizer.

        :doc: [SpacyDoc] - Documento con los resultado del analisis de spacy.

        :only_positives: [boolean] - Si esta activado, solo se devulven los resultados positivos.

        :return: [Dict] - Diccionario con la lista con los resultados del analisis del tokenizer y 
        el conteo de tokens.
        """
        tokenizer_detections = list([])
        token_count = defaultdict(Counter)
        if doc is None:
            return self._Model__build_tokenizer_results(tokenizer_detections, token_count)
        else:
            token_analyzer = Analyzer(self._Model__analyzer_rules_set, self._Model__analyzer_exceptions_set)
            for sent in doc.sents:
                for token in sent:
                    classified_token = token_analyzer.classify_token(token)
                    token_count[classified_token['type']][classified_token['orth']] += 1
                    generated_token = Token(token.lemma_, token.is_oov, token.pos_, token.sent, token.sentiment, token.tag_, token.text)
                    token_analyzer.analyze_token(generated_token)
                    if not only_positives or generated_token.is_positive():
                        tokenizer_detections.append(generated_token)

            return self._Model__build_tokenizer_results(tokenizer_detections, token_count)

    def __process_ner_results(self, doc):
        """
        Procesa los resultados del analisis de un texto almacenados en un doc de spacy en función de los
        resultados del NER.

        :doc: [SpacyDoc] - Documento con los resultado del analisis de spacy.

        :return: [List(Dict)] - Lista con los resultados del analisis del NER  
        """
        results = list([])
        if doc is None:
            return results
        else:
            for ent in doc.ents:
                results.append(Entity(ent.text, ent.start_char, ent.end_char, ent.label_))

            return results

    def find_exception(self, base_form, token_text):
        """
        Busca una excepción al analizador en la lista de excepciones al analizador del modelo.

        :base_form: [String] - Forma base del token.

        :token_text: [String] - Forma especifica en la que se debe detectar
        el token.

        :return: [AnalyzerException] - Excepción al analizador
        """
        for analyzer_exception in self._Model__analyzer_exceptions_set:
            if analyzer_exception.match_exception(token_text, base_form):
                return analyzer_exception

    def load(self):
        """
        Setea al modelo como cargado.
        """
        Logger.log('L-0056')
        if self.is_loaded():
            return
        model_reference = ModelLoader.load_model(self._Model__path)
        Logger.log('L-0057')
        self._Model__loaded = True
        self._Model__reference = model_reference

    def analyse_text(self, text, only_positives=False):
        """
        Analiza el texto deseado.

        :text: [String] - Texto a analizar

        :only_positives: [Boolean] - Si esta activado solo se devulven los resultados positivos

        :return: [Dict()] - Resultados del análisis.
        """
        Logger.log('L-0059')
        text_length = len(text)
        if text_length >= TEXT_LENGTH_THRESHOLD:
            self._Model__reference.max_length = text_length
        doc = self._Model__reference(text)
        Logger.log('L-0061')
        tokenizer_analysis_results = self._Model__process_tokenizer_results(doc, only_positives)
        results = {'ner_results':self._Model__process_ner_results(doc), 
         'token_frequency':tokenizer_analysis_results['token_frequency'], 
         'tokenizer_results':tokenizer_analysis_results['tokenizer_results']}
        Logger.log('L-0062')
        Logger.log('L-0063')
        return results

    def add_tokenizer_rule_set(self, rule_set):
        """
        Agrega una regla al modelo. El modelo debe estar inicializado.

        :rule_set: [Dict] - Regla agregar al tokenizer del modelo.
        """
        tokenizer = self._Model__reference.tokenizer
        for rule in rule_set:
            token_key = next(iter(rule))
            exception_data = rule[token_key][0]
            exception_dict = transform_dict_key_data_to_int(exception_data)
            tokenizer.add_special_case(token_key, [exception_dict])

    def train_model(self, training_data):
        """
        Aplica los ejemplos de entrenamiento al entrenamiento del modelo.

        :training_data: [List(Dict)] - Lista de ejemplos de entrenamiento.
        """
        if training_data is None:
            ErrorHandler.raise_error('E-0091')
        if not self.is_loaded():
            Logger.log('L-0340')
            self.load()
            Logger.log('L-0342')
        ModelLoader.apply_training_data(self, training_data)

    def to_dict(self):
        """
        Retorna un diccionario con la información del modelo.

        :return: [Dict] - Diccionario con los datos del modelo.
        """
        return dict({'model_id':self._Model__model_id, 
         'model_name':self._Model__model_name, 
         'description':self._Model__description, 
         'author':self._Model__author, 
         'path':self._Model__path, 
         'analyzer_rules_set':self._Model__analyzer_rules_set, 
         'analyzer_exceptions_set':self._Model__analyzer_exceptions_set})

    def __eq__(self, other):
        """
        Sobreescribe metodo equals de la clase.
        """
        if other is None or not isinstance(other, Model):
            return False
        else:
            return self._Model__model_id == other.get_model_id()

    def add_analyzer_exception(self, base_form, token_text, enabled):
        """
        Agrega una nueva excepción para el analizador al modelo.

        :base_form: [String] - Forma base del token.

        :token_text: [String] - Forma especifica en la que se debe detectar
        el token.

        :enabled: [Boolean] - Indicador de si la excepción esta habilitada.
        """
        exception = AnalyzerException(base_form, token_text, enabled)
        self._Model__analyzer_exceptions_set.append(exception)

    def check_exception(self, base_form, token_text):
        """
        Verifica si el modelo cuenta con una excepción al analyzador para la
        combinación de forma base y especifica provista.

        :base_form: [String] - Forma base del token.

        :token_text: [String] - Forma especifica en la que se debe detectar
        el token.

        :return: [Boolean] - True si se ha encontrado, False en caso contrario.
        """
        for exception in self._Model__analyzer_exceptions_set:
            if exception.match_exception(token_text, base_form):
                return True

        return False