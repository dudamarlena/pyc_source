# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-intel/egg/onlinelinguisticdatabase/tests/functional/test_morphemelanguagemodels.py
# Compiled at: 2016-09-19 13:27:02
import logging, os, codecs, simplejson as json
from time import sleep
from nose.tools import nottest
from sqlalchemy.sql import desc
from onlinelinguisticdatabase.tests import TestController, url
import onlinelinguisticdatabase.model as model
from onlinelinguisticdatabase.model.meta import Session
from subprocess import call
import onlinelinguisticdatabase.lib.helpers as h
from onlinelinguisticdatabase.model import MorphemeLanguageModel, MorphemeLanguageModelBackup
log = logging.getLogger(__name__)

class TestMorphemelanguagemodelsController(TestController):
    """Tests the morpheme_language_models controller.  WARNING: the tests herein are pretty messy.  The higher 
    ordered tests will fail if the previous tests have not been run.

    TODO: add more tests where we try to create deficient LMs.

    """

    def tearDown(self):
        pass

    def create_form(self, tr, mb, mg, tl, cat):
        params = self.form_create_params.copy()
        params.update({'transcription': tr, 'morpheme_break': mb, 'morpheme_gloss': mg, 'translations': [{'transcription': tl, 'grammaticality': ''}], 'syntactic_category': cat})
        params = json.dumps(params)
        self.app.post(url('forms'), params, self.json_headers, self.extra_environ_admin)

    def human_readable_seconds(self, seconds):
        return '%02dm%02ds' % (seconds / 60, seconds % 60)

    @nottest
    def test_a_create(self):
        """Tests that POST /morphemelanguagemodels creates a new morphology.

        """
        application_settings = h.generate_default_application_settings()
        Session.add(application_settings)
        Session.commit()
        cats = {'N': model.SyntacticCategory(name='N'), 
           'V': model.SyntacticCategory(name='V'), 
           'AGR': model.SyntacticCategory(name='AGR'), 
           'PHI': model.SyntacticCategory(name='PHI'), 
           'S': model.SyntacticCategory(name='S'), 
           'D': model.SyntacticCategory(name='D')}
        Session.add_all(cats.values())
        Session.commit()
        cats = dict([ (k, v.id) for k, v in cats.iteritems() ])
        dataset = (
         (
          'chien', 'chien', 'dog', 'dog', cats['N']),
         (
          'chat', 'chat', 'cat', 'cat', cats['N']),
         (
          'oiseau', 'oiseau', 'bird', 'bird', cats['N']),
         (
          'cheval', 'cheval', 'horse', 'horse', cats['N']),
         (
          'vache', 'vache', 'cow', 'cow', cats['N']),
         (
          'grenouille', 'grenouille', 'frog', 'frog', cats['N']),
         (
          'tortue', 'tortue', 'turtle', 'turtle', cats['N']),
         (
          'fourmi', 'fourmi', 'ant', 'ant', cats['N']),
         (
          'poule!t', 'poule!t', 'chicken', 'chicken', cats['N']),
         (
          'bécasse', 'bécasse', 'woodcock', 'woodcock', cats['N']),
         (
          'parle', 'parle', 'speak', 'speak', cats['V']),
         (
          'grimpe', 'grimpe', 'climb', 'climb', cats['V']),
         (
          'nage', 'nage', 'swim', 'swim', cats['V']),
         (
          'tombe', 'tombe', 'fall', 'fall', cats['V']),
         (
          'le', 'le', 'the', 'the', cats['D']),
         (
          'la', 'la', 'the', 'the', cats['D']),
         (
          's', 's', 'PL', 'plural', cats['PHI']),
         (
          'ait', 'ait', '3SG.IMPV', 'third person singular imperfective', cats['AGR']),
         (
          'aient', 'aient', '3PL.IMPV', 'third person plural imperfective', cats['AGR']),
         (
          'Les chat nageaient.', 'le-s chat-s nage-aient', 'the-PL cat-PL swim-3PL.IMPV', 'The cats were swimming.', cats['S']),
         (
          'La tortue parlait', 'la tortue parle-ait', 'the turtle speak-3SG.IMPV', 'The turtle was speaking.', cats['S']),
         (
          'Les oiseaux parlaient', 'le-s oiseau-s parle-aient', 'the-PL bird-PL speak-3PL.IMPV', 'The birds were speaking.', cats['S']),
         (
          'Le fourmi grimpait', 'le fourmi grimpe-ait', 'the ant climb-3SG.IMPV', 'The ant was climbing.', cats['S']),
         (
          'Les grenouilles nageaient', 'le-s grenouille-s nage-aient', 'the-PL frog-PL swim-3PL.IMPV', 'The frogs were swimming.', cats['S']),
         (
          'Le cheval tombait', 'le cheval tombe-ait', 'the horse fall-3SG.IMPV', 'The horse was falling.', cats['S']))
        for tuple_ in dataset:
            self.create_form(*map(unicode, tuple_))

        restricted_tag = h.generate_restricted_tag()
        Session.add(restricted_tag)
        query = {'filter': ['Form', 'syntactic_category', 'name', '=', 'S']}
        params = self.form_search_create_params.copy()
        params.update({'name': 'Find sentences', 
           'description': 'Returns all sentential forms', 
           'search': query})
        params = json.dumps(params)
        response = self.app.post(url('formsearches'), params, self.json_headers, self.extra_environ_admin)
        sentential_form_search_id = json.loads(response.body)['id']
        params = self.corpus_create_params.copy()
        params.update({'name': 'Corpus of sentences', 
           'form_search': sentential_form_search_id})
        params = json.dumps(params)
        response = self.app.post(url('corpora'), params, self.json_headers, self.extra_environ_admin)
        sentential_corpus_id = json.loads(response.body)['id']
        name = 'Morpheme language model'
        params = self.morpheme_language_model_create_params.copy()
        params.update({'name': name, 
           'corpus': sentential_corpus_id, 
           'toolkit': 'mitlm'})
        params = json.dumps(params)
        response = self.app.post(url('morphemelanguagemodels'), params, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        morpheme_language_model_id = resp['id']
        assert resp['name'] == name
        assert resp['toolkit'] == 'mitlm'
        assert resp['order'] == 3
        assert resp['smoothing'] == ''
        assert resp['restricted'] == False
        response = self.app.put(url(controller='morphemelanguagemodels', action='compute_perplexity', id=morpheme_language_model_id), {}, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        lm_perplexity_attempt = resp['perplexity_attempt']
        requester = lambda : self.app.get(url('morphemelanguagemodel', id=morpheme_language_model_id), headers=self.json_headers, extra_environ=self.extra_environ_admin)
        resp = self.poll(requester, 'perplexity_attempt', lm_perplexity_attempt, log, wait=1, vocal=False)
        perplexity = resp['perplexity']
        log.debug('Perplexity of super toy french (6 sentence corpus, ModKN, n=3): %s' % perplexity)
        response = self.app.get(url(controller='morphemelanguagemodels', action='serve_arpa', id=morpheme_language_model_id), {}, self.json_headers, self.extra_environ_admin, status=404)
        resp = json.loads(response.body)
        assert resp['error'] == 'The ARPA file for morpheme language model %d has not been compiled yet.' % morpheme_language_model_id
        response = self.app.put(url(controller='morphemelanguagemodels', action='generate', id=morpheme_language_model_id), {}, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        lm_generate_attempt = resp['generate_attempt']
        requester = lambda : self.app.get(url('morphemelanguagemodel', id=morpheme_language_model_id), headers=self.json_headers, extra_environ=self.extra_environ_admin)
        resp = self.poll(requester, 'generate_attempt', lm_generate_attempt, log, wait=1, vocal=False)
        assert resp['generate_message'] == 'Language model successfully generated.'
        assert resp['restricted'] == False
        response = self.app.get(url(controller='morphemelanguagemodels', action='serve_arpa', id=morpheme_language_model_id), {}, self.json_headers, self.extra_environ_view)
        assert response.content_type == 'text/plain'
        arpa = unicode(response.body, encoding='utf8')
        assert h.rare_delimiter.join(['parle', 'speak', 'V']) in arpa
        sentence1 = Session.query(model.Form).filter(model.Form.syntactic_category.has(model.SyntacticCategory.name == 'S')).all()[0]
        sentence1.tags.append(restricted_tag)
        Session.commit()
        response = self.app.put(url(controller='morphemelanguagemodels', action='generate', id=morpheme_language_model_id), {}, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        lm_generate_attempt = resp['generate_attempt']
        requester = lambda : self.app.get(url('morphemelanguagemodel', id=morpheme_language_model_id), headers=self.json_headers, extra_environ=self.extra_environ_admin)
        resp = self.poll(requester, 'generate_attempt', lm_generate_attempt, log, wait=1, vocal=False)
        assert resp['generate_message'] == 'Language model successfully generated.'
        assert resp['restricted'] == True
        response = self.app.get(url(controller='morphemelanguagemodels', action='serve_arpa', id=morpheme_language_model_id), {}, self.json_headers, self.extra_environ_view, status=403)
        resp = json.loads(response.body)
        assert response.content_type == 'application/json'
        assert resp == h.unauthorized_msg
        response = self.app.get(url(controller='morphemelanguagemodels', action='serve_arpa', id=morpheme_language_model_id), {}, self.json_headers, self.extra_environ_admin)
        assert response.content_type == 'text/plain'
        arpa = unicode(response.body, encoding='utf8')
        assert h.rare_delimiter.join(['parle', 'speak', 'V']) in arpa
        likely_word = '%s %s' % (
         h.rare_delimiter.join(['chat', 'cat', 'N']),
         h.rare_delimiter.join(['s', 'PL', 'PHI']))
        unlikely_word = '%s %s' % (
         h.rare_delimiter.join(['s', 'PL', 'PHI']),
         h.rare_delimiter.join(['chat', 'cat', 'N']))
        ms_params = json.dumps({'morpheme_sequences': [likely_word, unlikely_word]})
        response = self.app.put(url(controller='morphemelanguagemodels', action='get_probabilities', id=morpheme_language_model_id), ms_params, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        likely_word_log_prob = resp[likely_word]
        unlikely_word_log_prob = resp[unlikely_word]
        assert pow(10, likely_word_log_prob) > pow(10, unlikely_word_log_prob)
        name = 'Morpheme language model FixKN'
        params = self.morpheme_language_model_create_params.copy()
        params.update({'name': name, 
           'corpus': sentential_corpus_id, 
           'toolkit': 'mitlm', 
           'order': 4, 
           'smoothing': 'FixKN'})
        params = json.dumps(params)
        response = self.app.post(url('morphemelanguagemodels'), params, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        morpheme_language_model_id = resp['id']
        assert resp['name'] == name
        assert resp['toolkit'] == 'mitlm'
        assert resp['order'] == 4
        assert resp['smoothing'] == 'FixKN'
        response = self.app.put(url(controller='morphemelanguagemodels', action='generate', id=morpheme_language_model_id), {}, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        lm_generate_attempt = resp['generate_attempt']
        requester = lambda : self.app.get(url('morphemelanguagemodel', id=morpheme_language_model_id), headers=self.json_headers, extra_environ=self.extra_environ_admin)
        resp = self.poll(requester, 'generate_attempt', lm_generate_attempt, log, wait=1, vocal=False)
        response = self.app.put(url(controller='morphemelanguagemodels', action='get_probabilities', id=morpheme_language_model_id), ms_params, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        new_likely_word_log_prob = resp[likely_word]
        new_unlikely_word_log_prob = resp[unlikely_word]
        assert pow(10, new_likely_word_log_prob) > pow(10, new_unlikely_word_log_prob)
        assert new_likely_word_log_prob != likely_word_log_prob
        assert new_unlikely_word_log_prob != unlikely_word_log_prob
        response = self.app.put(url(controller='morphemelanguagemodels', action='compute_perplexity', id=morpheme_language_model_id), {}, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        lm_perplexity_attempt = resp['perplexity_attempt']
        requester = lambda : self.app.get(url('morphemelanguagemodel', id=morpheme_language_model_id), headers=self.json_headers, extra_environ=self.extra_environ_admin)
        resp = self.poll(requester, 'perplexity_attempt', lm_perplexity_attempt, log, wait=1, vocal=False)
        perplexity = resp['perplexity']
        log.debug('Perplexity of super toy french (6 sentence corpus, FixKN, n=4): %s' % perplexity)
        name = 'Morpheme language model with no corpus'
        params = self.morpheme_language_model_create_params.copy()
        params.update({'name': name, 
           'toolkit': 'mitlm_lmlmlm', 
           'order': 7, 
           'smoothing': 'strawberry'})
        params = json.dumps(params)
        response = self.app.post(url('morphemelanguagemodels'), params, self.json_headers, self.extra_environ_admin, status=400)
        resp = json.loads(response.body)
        assert resp['errors']['corpus'] == 'Please enter a value'
        assert resp['errors']['order'] == 'Please enter a number that is 5 or smaller'
        assert 'toolkit' in resp['errors']
        name = 'Morpheme language model with no corpus'
        params = self.morpheme_language_model_create_params.copy()
        params.update({'name': name, 
           'toolkit': 'mitlm', 
           'order': 3, 
           'smoothing': 'strawberry', 
           'corpus': sentential_corpus_id})
        params = json.dumps(params)
        response = self.app.post(url('morphemelanguagemodels'), params, self.json_headers, self.extra_environ_admin, status=400)
        resp = json.loads(response.body)
        assert resp['errors'] == 'The LM toolkit mitlm implements no such smoothing algorithm strawberry.'
        name = 'Category-based mMorpheme language model'
        params = self.morpheme_language_model_create_params.copy()
        params.update({'categorial': True, 
           'name': name, 
           'corpus': sentential_corpus_id, 
           'toolkit': 'mitlm', 
           'order': 4, 
           'smoothing': 'FixKN'})
        params = json.dumps(params)
        response = self.app.post(url('morphemelanguagemodels'), params, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        morpheme_language_model_id = resp['id']
        assert resp['name'] == name
        assert resp['toolkit'] == 'mitlm'
        assert resp['order'] == 4
        assert resp['smoothing'] == 'FixKN'
        assert resp['categorial'] == True
        response = self.app.put(url(controller='morphemelanguagemodels', action='generate', id=morpheme_language_model_id), {}, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        lm_generate_attempt = resp['generate_attempt']
        requester = lambda : self.app.get(url('morphemelanguagemodel', id=morpheme_language_model_id), headers=self.json_headers, extra_environ=self.extra_environ_admin)
        resp = self.poll(requester, 'generate_attempt', lm_generate_attempt, log, wait=1, vocal=True, task_descr='generate categorial MLM')
        response = self.app.get(url(controller='morphemelanguagemodels', action='serve_arpa', id=morpheme_language_model_id), {}, self.json_headers, self.extra_environ_admin)
        assert response.content_type == 'text/plain'
        arpa = unicode(response.body, encoding='utf8')
        assert 'D PHI' in arpa
        assert 'N PHI' in arpa
        assert 'V AGR' in arpa
        assert '<s> V AGR' in arpa
        likely_word = 'N PHI'
        unlikely_word = 'PHI N'
        ms_params = json.dumps({'morpheme_sequences': [likely_word, unlikely_word]})
        response = self.app.put(url(controller='morphemelanguagemodels', action='get_probabilities', id=morpheme_language_model_id), ms_params, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        likely_word_log_prob = resp[likely_word]
        unlikely_word_log_prob = resp[unlikely_word]
        assert likely_word_log_prob > unlikely_word_log_prob
        response = self.app.put(url(controller='morphemelanguagemodels', action='compute_perplexity', id=morpheme_language_model_id), {}, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        lm_perplexity_attempt = resp['perplexity_attempt']
        requester = lambda : self.app.get(url('morphemelanguagemodel', id=morpheme_language_model_id), headers=self.json_headers, extra_environ=self.extra_environ_admin)
        resp = self.poll(requester, 'perplexity_attempt', lm_perplexity_attempt, log, wait=1, vocal=False)
        perplexity = resp['perplexity']
        log.debug('Perplexity of super toy french (6 sentence corpus, category-based, FixKN, n=4): %s' % perplexity)

    @nottest
    def test_b_index(self):
        """Tests that GET /morpheme_language_models returns all morpheme_language_model resources."""
        morpheme_language_models = Session.query(MorphemeLanguageModel).all()
        response = self.app.get(url('morphemelanguagemodels'), headers=self.json_headers, extra_environ=self.extra_environ_view)
        resp = json.loads(response.body)
        assert len(resp) == 3
        paginator = {'items_per_page': 1, 'page': 1}
        response = self.app.get(url('morphemelanguagemodels'), paginator, headers=self.json_headers, extra_environ=self.extra_environ_view)
        resp = json.loads(response.body)
        assert len(resp['items']) == 1
        assert resp['items'][0]['name'] == morpheme_language_models[0].name
        assert response.content_type == 'application/json'
        order_by_params = {'order_by_model': 'MorphemeLanguageModel', 'order_by_attribute': 'id', 'order_by_direction': 'desc'}
        response = self.app.get(url('morphemelanguagemodels'), order_by_params, headers=self.json_headers, extra_environ=self.extra_environ_view)
        resp = json.loads(response.body)
        assert resp[0]['id'] == morpheme_language_models[(-1)].id
        assert response.content_type == 'application/json'
        params = {'order_by_model': 'MorphemeLanguageModel', 'order_by_attribute': 'id', 'order_by_direction': 'desc', 
           'items_per_page': 1, 'page': 3}
        response = self.app.get(url('morphemelanguagemodels'), params, headers=self.json_headers, extra_environ=self.extra_environ_view)
        resp = json.loads(response.body)
        assert morpheme_language_models[0].name == resp['items'][0]['name']
        order_by_params = {'order_by_model': 'MorphemeLanguageModel', 'order_by_attribute': 'name', 'order_by_direction': 'descending'}
        response = self.app.get(url('morphemelanguagemodels'), order_by_params, status=400, headers=self.json_headers, extra_environ=self.extra_environ_view)
        resp = json.loads(response.body)
        assert resp['errors']['order_by_direction'] == "Value must be one of: asc; desc (not u'descending')"
        assert response.content_type == 'application/json'

    @nottest
    def test_d_show(self):
        """Tests that GET /morphemelanguagemodels/id returns the morpheme_language_model with id=id or an appropriate error."""
        morpheme_language_models = Session.query(MorphemeLanguageModel).all()
        id = 100000000000
        response = self.app.get(url('morphemelanguagemodel', id=id), headers=self.json_headers, extra_environ=self.extra_environ_admin, status=404)
        resp = json.loads(response.body)
        assert 'There is no morpheme language model with id %s' % id in json.loads(response.body)['error']
        assert response.content_type == 'application/json'
        response = self.app.get(url('morphemelanguagemodel', id=''), status=404, headers=self.json_headers, extra_environ=self.extra_environ_admin)
        assert json.loads(response.body)['error'] == 'The resource could not be found.'
        assert response.content_type == 'application/json'
        response = self.app.get(url('morphemelanguagemodel', id=morpheme_language_models[0].id), headers=self.json_headers, extra_environ=self.extra_environ_admin)
        resp = json.loads(response.body)
        assert resp['name'] == morpheme_language_models[0].name
        assert resp['description'] == morpheme_language_models[0].description
        assert response.content_type == 'application/json'

    @nottest
    def test_e_new_edit(self):
        """Tests that GET /morphemelanguagemodels/new and GET /morphemelanguagemodels/id/edit return the data needed to create or update a morpheme_language_model.

        """
        morpheme_language_models = Session.query(MorphemeLanguageModel).all()
        corpora = Session.query(model.Corpus).all()
        morphologies = Session.query(model.Morphology).all()
        toolkits = h.language_model_toolkits
        response = self.app.get(url('new_morphemelanguagemodel'), headers=self.json_headers, extra_environ=self.extra_environ_admin)
        resp = json.loads(response.body)
        assert len(resp['corpora']) == len(corpora)
        assert len(resp['morphologies']) == len(morphologies)
        assert len(resp['toolkits'].keys()) == len(toolkits.keys())
        response = self.app.get(url('edit_morphemelanguagemodel', id=morpheme_language_models[0].id), status=401)
        resp = json.loads(response.body)
        assert resp['error'] == 'Authentication is required to access this resource.'
        assert response.content_type == 'application/json'
        id = 9876544
        response = self.app.get(url('edit_morphemelanguagemodel', id=id), headers=self.json_headers, extra_environ=self.extra_environ_admin, status=404)
        assert 'There is no morpheme language model with id %s' % id in json.loads(response.body)['error']
        assert response.content_type == 'application/json'
        response = self.app.get(url('edit_morphemelanguagemodel', id=''), status=404, headers=self.json_headers, extra_environ=self.extra_environ_admin)
        assert json.loads(response.body)['error'] == 'The resource could not be found.'
        assert response.content_type == 'application/json'
        response = self.app.get(url('edit_morphemelanguagemodel', id=morpheme_language_models[0].id), headers=self.json_headers, extra_environ=self.extra_environ_admin)
        resp = json.loads(response.body)
        assert resp['morpheme_language_model']['name'] == morpheme_language_models[0].name
        assert len(resp['data']['corpora']) == len(corpora)
        assert len(resp['data']['morphologies']) == len(morphologies)
        assert len(resp['data']['toolkits'].keys()) == len(toolkits.keys())
        assert response.content_type == 'application/json'

    @nottest
    def test_f_update(self):
        """Tests that PUT /morphemelanguagemodels/id updates the morpheme_language_model with id=id."""
        morpheme_language_models = [ json.loads(json.dumps(m, cls=h.JSONOLDEncoder)) for m in Session.query(MorphemeLanguageModel).all()
                                   ]
        morpheme_language_model_id = morpheme_language_models[0]['id']
        morpheme_language_model_1_name = morpheme_language_models[0]['name']
        morpheme_language_model_1_description = morpheme_language_models[0]['description']
        morpheme_language_model_1_modified = morpheme_language_models[0]['datetime_modified']
        morpheme_language_model_1_corpus_id = morpheme_language_models[0]['corpus']['id']
        morpheme_language_model_1_vocabulary_morphology_id = getattr(morpheme_language_models[0].get('vocabulary_morphology'), 'id', None)
        morpheme_language_model_count = len(morpheme_language_models)
        morpheme_language_model_1_dir = os.path.join(self.morpheme_language_models_path, 'morpheme_language_model_%d' % morpheme_language_model_id)
        morpheme_language_model_1_arpa_path = os.path.join(morpheme_language_model_1_dir, 'morpheme_language_model.lm')
        morpheme_language_model_1_arpa = codecs.open(morpheme_language_model_1_arpa_path, mode='r', encoding='utf8').read()
        original_backup_count = Session.query(MorphemeLanguageModelBackup).count()
        params = self.morpheme_language_model_create_params.copy()
        params.update({'name': morpheme_language_model_1_name, 
           'description': 'New description', 
           'corpus': morpheme_language_model_1_corpus_id, 
           'vocabulary_morphology': morpheme_language_model_1_vocabulary_morphology_id, 
           'toolkit': 'mitlm'})
        params = json.dumps(params)
        response = self.app.put(url('morphemelanguagemodel', id=morpheme_language_model_id), params, self.json_headers, self.extra_environ_admin)
        resp = json.loads(response.body)
        new_backup_count = Session.query(MorphemeLanguageModelBackup).count()
        datetime_modified = resp['datetime_modified']
        new_morpheme_language_model_count = Session.query(MorphemeLanguageModel).count()
        assert morpheme_language_model_count == new_morpheme_language_model_count
        assert datetime_modified != morpheme_language_model_1_modified
        assert resp['description'] == 'New description'
        assert response.content_type == 'application/json'
        assert original_backup_count + 1 == new_backup_count
        backup = Session.query(MorphemeLanguageModelBackup).filter(MorphemeLanguageModelBackup.UUID == unicode(resp['UUID'])).order_by(desc(MorphemeLanguageModelBackup.id)).first()
        assert backup.datetime_modified.isoformat() == morpheme_language_model_1_modified
        assert backup.description == morpheme_language_model_1_description
        assert response.content_type == 'application/json'
        response = self.app.put(url('morphemelanguagemodel', id=morpheme_language_model_id), params, self.json_headers, self.extra_environ_admin, status=400)
        resp = json.loads(response.body)
        morpheme_language_model_count = new_morpheme_language_model_count
        new_morpheme_language_model_count = Session.query(MorphemeLanguageModel).count()
        our_morpheme_language_model_datetime_modified = Session.query(MorphemeLanguageModel).get(morpheme_language_model_id).datetime_modified
        assert our_morpheme_language_model_datetime_modified.isoformat() == datetime_modified
        assert morpheme_language_model_count == new_morpheme_language_model_count
        assert resp['error'] == 'The update request failed because the submitted data were not new.'
        assert response.content_type == 'application/json'
        return

    @nottest
    def test_g_history(self):
        """Tests that GET /morphemelanguagemodels/id/history returns the morpheme_language_model with id=id and its previous incarnations.

        The JSON object returned is of the form
        {'morpheme_language_model': morpheme_language_model, 'previous_versions': [...]}.

        """
        morpheme_language_models = Session.query(MorphemeLanguageModel).all()
        morpheme_language_model_id = morpheme_language_models[0].id
        morpheme_language_model_1_UUID = morpheme_language_models[0].UUID
        morpheme_language_model_1_backup_count = len(Session.query(MorphemeLanguageModelBackup).filter(MorphemeLanguageModelBackup.UUID == morpheme_language_model_1_UUID).all())
        response = self.app.get(url(controller='morphemelanguagemodels', action='history', id=morpheme_language_model_id), headers=self.json_headers, extra_environ=self.extra_environ_view_appset)
        resp = json.loads(response.body)
        assert response.content_type == 'application/json'
        assert 'morpheme_language_model' in resp
        assert 'previous_versions' in resp
        assert len(resp['previous_versions']) == morpheme_language_model_1_backup_count
        response = self.app.get(url(controller='morphemelanguagemodels', action='history', id=morpheme_language_model_1_UUID), headers=self.json_headers, extra_environ=self.extra_environ_view_appset)
        resp = json.loads(response.body)
        assert response.content_type == 'application/json'
        assert 'morpheme_language_model' in resp
        assert 'previous_versions' in resp
        assert len(resp['previous_versions']) == morpheme_language_model_1_backup_count
        response = self.app.get(url(controller='morphemelanguagemodels', action='history', id=123456789), headers=self.json_headers, extra_environ=self.extra_environ_view_appset, status=404)
        resp = json.loads(response.body)
        assert response.content_type == 'application/json'
        assert resp['error'] == 'No morpheme language models or morpheme language model backups match 123456789'

    @nottest
    def test_i_large_datasets(self):
        """Tests that morpheme language model functionality works with large datasets.

        .. note::

            This test only works if MySQL is being used as the RDBMS for the test
            *and* there is a file in 
            ``onlinelinguisticdatabase/onlinelinguisticdatabase/tests/data/datasets/``
            that is a MySQL dump file of a valid OLD database.  The name of this file
            can be configured by setting the ``old_dump_file`` variable.  Note that no
            such dump file is provided with the OLD source since the file used by the
            developer contains data that cannot be publicly shared.

        """
        old_dump_file = 'blaold.sql'
        backup_dump_file = 'old_test_dump.sql'
        old_dump_file_path = os.path.join(self.test_datasets_path, old_dump_file)
        backup_dump_file_path = os.path.join(self.test_datasets_path, backup_dump_file)
        tmp_script_path = os.path.join(self.test_datasets_path, 'tmp.sh')
        if not os.path.isfile(old_dump_file_path):
            return
        config = h.get_config(config_filename='test.ini')
        SQLAlchemyURL = config['sqlalchemy.url']
        if not SQLAlchemyURL.split(':')[0] == 'mysql':
            return
        else:
            rdbms, username, password, db_name = SQLAlchemyURL.split(':')
            username = username[2:]
            password = password.split('@')[0]
            db_name = db_name.split('/')[(-1)]
            with open(tmp_script_path, 'w') as (tmpscript):
                tmpscript.write('#!/bin/sh\nmysqldump -u %s -p%s --single-transaction --no-create-info --result-file=%s %s' % (
                 username, password, backup_dump_file_path, db_name))
            os.chmod(tmp_script_path, 484)
            with open(os.devnull, 'w') as (fnull):
                call([tmp_script_path], stdout=fnull, stderr=fnull)
            with open(tmp_script_path, 'w') as (tmpscript):
                tmpscript.write('#!/bin/sh\nmysql -u %s -p%s %s < %s' % (username, password, db_name, old_dump_file_path))
            with open(os.devnull, 'w') as (fnull):
                call([tmp_script_path], stdout=fnull, stderr=fnull)
            administrator = h.generate_default_administrator()
            contributor = h.generate_default_contributor()
            viewer = h.generate_default_viewer()
            Session.add_all([administrator, contributor, viewer])
            Session.commit()
            query = {'filter': ['and',
                        [
                         ['or',
                          [['Form', 'syntactic_category', 'name', '=', 'sent'],
                           [
                            'Form', 'morpheme_break', 'like', '% %'],
                           [
                            'Form', 'morpheme_break', 'like', '%-%']]],
                         [
                          'Form', 'syntactic_category_string', '!=', None],
                         [
                          'Form', 'grammaticality', '=', '']]]}
            params = self.form_search_create_params.copy()
            params.update({'name': 'Forms containing words', 
               'search': query})
            params = json.dumps(params)
            response = self.app.post(url('formsearches'), params, self.json_headers, self.extra_environ_admin)
            words_form_search_id = json.loads(response.body)['id']
            params = self.corpus_create_params.copy()
            params.update({'name': 'Corpus of forms that contain words', 
               'form_search': words_form_search_id})
            params = json.dumps(params)
            response = self.app.post(url('corpora'), params, self.json_headers, self.extra_environ_admin)
            words_corpus_id = json.loads(response.body)['id']
            name = 'Morpheme language model for Blackfoot'
            params = self.morpheme_language_model_create_params.copy()
            params.update({'name': name, 
               'corpus': words_corpus_id, 
               'toolkit': 'mitlm'})
            params = json.dumps(params)
            response = self.app.post(url('morphemelanguagemodels'), params, self.json_headers, self.extra_environ_admin_appset)
            resp = json.loads(response.body)
            morpheme_language_model_id = resp['id']
            assert resp['name'] == name
            assert resp['toolkit'] == 'mitlm'
            response = self.app.put(url(controller='morphemelanguagemodels', action='generate', id=morpheme_language_model_id), {}, self.json_headers, self.extra_environ_admin)
            resp = json.loads(response.body)
            lm_generate_attempt = resp['generate_attempt']
            requester = lambda : self.app.get(url('morphemelanguagemodel', id=morpheme_language_model_id), headers=self.json_headers, extra_environ=self.extra_environ_admin)
            resp = self.poll(requester, 'generate_attempt', lm_generate_attempt, log)
            assert resp['generate_message'] == 'Language model successfully generated.'
            likely_word = '%s %s' % (
             h.rare_delimiter.join(['nit', '1', 'agra']),
             h.rare_delimiter.join(['ihpiyi', 'dance', 'vai']))
            unlikely_word = '%s %s' % (
             h.rare_delimiter.join(['ihpiyi', 'dance', 'vai']),
             h.rare_delimiter.join(['nit', '1', 'agra']))
            ms_params = json.dumps({'morpheme_sequences': [likely_word, unlikely_word]})
            response = self.app.put(url(controller='morphemelanguagemodels', action='get_probabilities', id=morpheme_language_model_id), ms_params, self.json_headers, self.extra_environ_admin)
            resp = json.loads(response.body)
            likely_word_log_prob = resp[likely_word]
            unlikely_word_log_prob = resp[unlikely_word]
            assert pow(10, likely_word_log_prob) > pow(10, unlikely_word_log_prob)
            response = self.app.put(url(controller='morphemelanguagemodels', action='compute_perplexity', id=morpheme_language_model_id), {}, self.json_headers, self.extra_environ_admin)
            resp = json.loads(response.body)
            lm_perplexity_attempt = resp['perplexity_attempt']
            requester = lambda : self.app.get(url('morphemelanguagemodel', id=morpheme_language_model_id), headers=self.json_headers, extra_environ=self.extra_environ_admin)
            resp = self.poll(requester, 'perplexity_attempt', lm_perplexity_attempt, log)
            perplexity = resp['perplexity']
            lm_corpus_path = os.path.join(self.morpheme_language_models_path, 'morpheme_language_model_%s' % morpheme_language_model_id, 'morpheme_language_model.txt')
            word_count = 0
            with codecs.open(lm_corpus_path, encoding='utf8') as (f):
                for line in f:
                    word_count += 1

            log.debug('Perplexity of Blackfoot LM %s (%s sentence corpus, ModKN, n=3): %s' % (
             morpheme_language_model_id, word_count, perplexity))
            name = 'Category-based morpheme language model for Blackfoot'
            params = self.morpheme_language_model_create_params.copy()
            params.update({'categorial': True, 
               'name': name, 
               'corpus': words_corpus_id, 
               'toolkit': 'mitlm'})
            params = json.dumps(params)
            response = self.app.post(url('morphemelanguagemodels'), params, self.json_headers, self.extra_environ_admin_appset)
            resp = json.loads(response.body)
            morpheme_language_model_id = resp['id']
            assert resp['name'] == name
            assert resp['toolkit'] == 'mitlm'
            response = self.app.put(url(controller='morphemelanguagemodels', action='generate', id=morpheme_language_model_id), {}, self.json_headers, self.extra_environ_admin)
            resp = json.loads(response.body)
            lm_generate_attempt = resp['generate_attempt']
            requester = lambda : self.app.get(url('morphemelanguagemodel', id=morpheme_language_model_id), headers=self.json_headers, extra_environ=self.extra_environ_admin)
            resp = self.poll(requester, 'generate_attempt', lm_generate_attempt, log)
            assert resp['generate_message'] == 'Language model successfully generated.'
            likely_category_word = 'agra vai'
            unlikely_category_word = 'vai agra'
            ms_params = json.dumps({'morpheme_sequences': [likely_category_word, unlikely_category_word]})
            response = self.app.put(url(controller='morphemelanguagemodels', action='get_probabilities', id=morpheme_language_model_id), ms_params, self.json_headers, self.extra_environ_admin)
            resp = json.loads(response.body)
            likely_category_word_log_prob = resp[likely_category_word]
            unlikely_category_word_log_prob = resp[unlikely_category_word]
            assert pow(10, likely_category_word_log_prob) > pow(10, unlikely_category_word_log_prob)
            response = self.app.put(url(controller='morphemelanguagemodels', action='compute_perplexity', id=morpheme_language_model_id), {}, self.json_headers, self.extra_environ_admin)
            resp = json.loads(response.body)
            lm_perplexity_attempt = resp['perplexity_attempt']
            requester = lambda : self.app.get(url('morphemelanguagemodel', id=morpheme_language_model_id), headers=self.json_headers, extra_environ=self.extra_environ_admin)
            resp = self.poll(requester, 'perplexity_attempt', lm_perplexity_attempt, log)
            category_based_perplexity = resp['perplexity']
            lm_corpus_path = os.path.join(self.morpheme_language_models_path, 'morpheme_language_model_%s' % morpheme_language_model_id, 'morpheme_language_model.txt')
            word_count = 0
            with codecs.open(lm_corpus_path, encoding='utf8') as (f):
                for line in f:
                    word_count += 1

            log.debug('Perplexity of Blackfoot category-based LM %s (%s sentence corpus, ModKN, n=3): %s' % (
             morpheme_language_model_id, word_count, category_based_perplexity))
            lexical_category_names = [
             'nan', 'nin', 'nar', 'nir', 'vai', 'vii', 'vta', 'vti', 'vrt', 'adt',
             'drt', 'prev', 'med', 'fin', 'oth', 'o', 'und', 'pro', 'asp', 'ten', 'mod', 'agra', 'agrb', 'thm', 'whq',
             'num', 'stp', 'PN']
            durative_morpheme = 15717
            hkayi_morpheme = 23429
            query = {'filter': ['and',
                        [['Form', 'syntactic_category', 'name', 'in', lexical_category_names],
                         [
                          'not', ['Form', 'morpheme_break', 'regex', '[ -]']],
                         [
                          'not', ['Form', 'id', 'in', [durative_morpheme, hkayi_morpheme]]],
                         [
                          'not', ['Form', 'grammaticality', '=', '*']]]]}
            smaller_query_for_rapid_testing = {'filter': ['and',
                        [['Form', 'id', '<', 1000],
                         [
                          'Form', 'syntactic_category', 'name', 'in', lexical_category_names]]]}
            params = self.form_search_create_params.copy()
            params.update({'name': 'Blackfoot morphemes', 
               'search': query})
            params = json.dumps(params)
            response = self.app.post(url('formsearches'), params, self.json_headers, self.extra_environ_admin)
            lexicon_form_search_id = json.loads(response.body)['id']
            params = self.corpus_create_params.copy()
            params.update({'name': 'Corpus of Blackfoot morphemes', 
               'form_search': lexicon_form_search_id})
            params = json.dumps(params)
            response = self.app.post(url('corpora'), params, self.json_headers, self.extra_environ_admin)
            lexicon_corpus_id = json.loads(response.body)['id']
            query = {'filter': ['and',
                        [
                         ['or',
                          [['Form', 'syntactic_category', 'name', '=', 'sent'],
                           [
                            'Form', 'morpheme_break', 'like', '%-%'],
                           [
                            'Form', 'morpheme_break', 'like', '% %']]],
                         [
                          'Form', 'grammaticality', '=', '']]]}
            params = self.form_search_create_params.copy()
            params.update({'name': 'Find Blackfoot sentences', 
               'description': 'Returns all sentential forms', 
               'search': query})
            params = json.dumps(params)
            response = self.app.post(url('formsearches'), params, self.json_headers, self.extra_environ_admin)
            rules_form_search_id = json.loads(response.body)['id']
            params = self.corpus_create_params.copy()
            params.update({'name': 'Corpus of Blackfoot sentences', 
               'form_search': rules_form_search_id})
            params = json.dumps(params)
            response = self.app.post(url('corpora'), params, self.json_headers, self.extra_environ_admin)
            rules_corpus_id = json.loads(response.body)['id']
            minimum_token_count = 5
            params = {'minimum_token_count': minimum_token_count}
            response = self.app.get(url(controller='corpora', action='get_word_category_sequences', id=rules_corpus_id), params, self.json_headers, self.extra_environ_admin)
            resp = json.loads(response.body)
            word_category_sequences = (' ').join([ word_category_sequence for word_category_sequence, ids in resp ])
            morphology_name = 'Morphology of Blackfoot'
            params = self.morphology_create_params.copy()
            params.update({'name': morphology_name, 
               'lexicon_corpus': lexicon_corpus_id, 
               'rules': word_category_sequences, 
               'script_type': 'lexc', 
               'extract_morphemes_from_rules_corpus': False})
            params = json.dumps(params)
            response = self.app.post(url('morphologies'), params, self.json_headers, self.extra_environ_admin_appset)
            resp = json.loads(response.body)
            morphology_id = resp['id']
            assert resp['name'] == morphology_name
            assert resp['script_type'] == 'lexc'
            response = self.app.put(url(controller='morphologies', action='generate', id=morphology_id), headers=self.json_headers, extra_environ=self.extra_environ_contrib)
            resp = json.loads(response.body)
            generate_attempt = resp['generate_attempt']
            seconds_elapsed = 0
            wait = 2
            while True:
                response = self.app.get(url('morphology', id=morphology_id), headers=self.json_headers, extra_environ=self.extra_environ_contrib)
                resp = json.loads(response.body)
                if generate_attempt != resp['generate_attempt']:
                    log.debug('Generate attempt for morphology %d has terminated.' % morphology_id)
                    break
                else:
                    log.debug("Waiting for morphology %d's script to generate: %s" % (
                     morphology_id, self.human_readable_seconds(seconds_elapsed)))
                sleep(wait)
                seconds_elapsed = seconds_elapsed + wait

            name = 'Morpheme language model for Blackfoot with fixed vocabulary'
            params = self.morpheme_language_model_create_params.copy()
            params.update({'name': name, 
               'corpus': words_corpus_id, 
               'toolkit': 'mitlm', 
               'vocabulary_morphology': morphology_id})
            params = json.dumps(params)
            response = self.app.post(url('morphemelanguagemodels'), params, self.json_headers, self.extra_environ_admin_appset)
            resp = json.loads(response.body)
            morpheme_language_model_id = resp['id']
            assert resp['name'] == name
            assert resp['toolkit'] == 'mitlm'
            assert resp['vocabulary_morphology']['name'] == morphology_name
            response = self.app.put(url(controller='morphemelanguagemodels', action='generate', id=morpheme_language_model_id), {}, self.json_headers, self.extra_environ_admin)
            resp = json.loads(response.body)
            lm_generate_attempt = resp['generate_attempt']
            requester = lambda : self.app.get(url('morphemelanguagemodel', id=morpheme_language_model_id), headers=self.json_headers, extra_environ=self.extra_environ_admin)
            resp = self.poll(requester, 'generate_attempt', lm_generate_attempt, log)
            ms_params = json.dumps({'morpheme_sequences': [likely_word, unlikely_word]})
            response = self.app.put(url(controller='morphemelanguagemodels', action='get_probabilities', id=morpheme_language_model_id), ms_params, self.json_headers, self.extra_environ_admin)
            resp = json.loads(response.body)
            new_likely_word_log_prob = resp[likely_word]
            new_unlikely_word_log_prob = resp[unlikely_word]
            assert pow(10, new_likely_word_log_prob) > pow(10, new_unlikely_word_log_prob)
            assert new_unlikely_word_log_prob != unlikely_word_log_prob
            assert new_likely_word_log_prob != likely_word_log_prob
            response = self.app.put(url(controller='morphemelanguagemodels', action='compute_perplexity', id=morpheme_language_model_id), {}, self.json_headers, self.extra_environ_admin)
            resp = json.loads(response.body)
            lm_perplexity_attempt = resp['perplexity_attempt']
            requester = lambda : self.app.get(url('morphemelanguagemodel', id=morpheme_language_model_id), headers=self.json_headers, extra_environ=self.extra_environ_admin)
            resp = self.poll(requester, 'perplexity_attempt', lm_perplexity_attempt, log, task_descr='GET PERPLEXITY OF LM %s' % morpheme_language_model_id)
            new_perplexity = resp['perplexity']
            log.debug('new_perplexity')
            log.debug(new_perplexity)
            log.debug('perplexity')
            log.debug(perplexity)
            assert new_perplexity < perplexity
            log.debug('Perplexity of Blackfoot LM %s (%s sentence corpus, ModKN, n=3, fixed vocabulary): %s' % (
             morpheme_language_model_id, word_count, new_perplexity))
            name = 'Categorial morpheme language model for Blackfoot with fixed vocabulary'
            params = self.morpheme_language_model_create_params.copy()
            params.update({'name': name, 
               'corpus': words_corpus_id, 
               'toolkit': 'mitlm', 
               'vocabulary_morphology': morphology_id, 
               'categorial': True})
            params = json.dumps(params)
            response = self.app.post(url('morphemelanguagemodels'), params, self.json_headers, self.extra_environ_admin_appset)
            resp = json.loads(response.body)
            morpheme_language_model_id = resp['id']
            assert resp['name'] == name
            assert resp['toolkit'] == 'mitlm'
            assert resp['vocabulary_morphology']['name'] == morphology_name
            response = self.app.put(url(controller='morphemelanguagemodels', action='generate', id=morpheme_language_model_id), {}, self.json_headers, self.extra_environ_admin)
            resp = json.loads(response.body)
            lm_generate_attempt = resp['generate_attempt']
            requester = lambda : self.app.get(url('morphemelanguagemodel', id=morpheme_language_model_id), headers=self.json_headers, extra_environ=self.extra_environ_admin)
            resp = self.poll(requester, 'generate_attempt', lm_generate_attempt, log)
            ms_params = json.dumps({'morpheme_sequences': [likely_category_word, unlikely_category_word]})
            response = self.app.put(url(controller='morphemelanguagemodels', action='get_probabilities', id=morpheme_language_model_id), ms_params, self.json_headers, self.extra_environ_admin)
            resp = json.loads(response.body)
            new_likely_category_word_log_prob = resp[likely_category_word]
            new_unlikely_category_word_log_prob = resp[unlikely_category_word]
            assert pow(10, new_likely_category_word_log_prob) > pow(10, new_unlikely_category_word_log_prob)
            assert new_unlikely_category_word_log_prob != unlikely_category_word_log_prob
            assert new_likely_category_word_log_prob != likely_category_word_log_prob
            response = self.app.put(url(controller='morphemelanguagemodels', action='compute_perplexity', id=morpheme_language_model_id), {}, self.json_headers, self.extra_environ_admin)
            resp = json.loads(response.body)
            lm_perplexity_attempt = resp['perplexity_attempt']
            requester = lambda : self.app.get(url('morphemelanguagemodel', id=morpheme_language_model_id), headers=self.json_headers, extra_environ=self.extra_environ_admin)
            resp = self.poll(requester, 'perplexity_attempt', lm_perplexity_attempt, log, task_descr='GET PERPLEXITY OF LM %s' % morpheme_language_model_id)
            new_category_based_perplexity = resp['perplexity']
            log.debug('Perplexity of Blackfoot LM %s (%s sentence corpus, ModKN, n=3, fixed vocabulary, category-based): %s' % (
             morpheme_language_model_id, word_count, new_category_based_perplexity))
            query = json.dumps({'query': {'filter': ['Form', 'corpora', 'id', '=', words_corpus_id]}})
            response = self.app.post(url('/forms/search'), query, self.json_headers, self.extra_environ_admin)
            resp = json.loads(response.body)
            form_ids = [ f['id'] for f in resp ]
            nit_ihpiyi_ids = [ f['id'] for f in resp if 'nit|1|agra-ihpiyi|dance|vai' in f['break_gloss_category'] ]
            form_ids += nit_ihpiyi_ids * 100
            params = self.corpus_create_params.copy()
            params.update({'name': 'Corpus of forms that contain words with lots of nit-ihpiyi words', 
               'content': (',').join(map(str, form_ids))})
            params = json.dumps(params)
            response = self.app.post(url('corpora'), params, self.json_headers, self.extra_environ_admin)
            nit_ihpiyi_words_corpus_id = json.loads(response.body)['id']
            name = 'Morpheme language model for Blackfoot with fixed vocabulary and weighted towards nit-ihpiyi words'
            params = self.morpheme_language_model_create_params.copy()
            params.update({'name': name, 
               'corpus': nit_ihpiyi_words_corpus_id, 
               'toolkit': 'mitlm', 
               'vocabulary_morphology': morphology_id})
            params = json.dumps(params)
            response = self.app.post(url('morphemelanguagemodels'), params, self.json_headers, self.extra_environ_admin_appset)
            resp = json.loads(response.body)
            morpheme_language_model_id = resp['id']
            assert resp['name'] == name
            assert resp['toolkit'] == 'mitlm'
            assert resp['vocabulary_morphology']['name'] == morphology_name
            response = self.app.put(url(controller='morphemelanguagemodels', action='generate', id=morpheme_language_model_id), {}, self.json_headers, self.extra_environ_admin)
            resp = json.loads(response.body)
            lm_generate_attempt = resp['generate_attempt']
            requester = lambda : self.app.get(url('morphemelanguagemodel', id=morpheme_language_model_id), headers=self.json_headers, extra_environ=self.extra_environ_admin)
            resp = self.poll(requester, 'generate_attempt', lm_generate_attempt, log, task_descr='GET PERPLEXITY OF L %s' % morpheme_language_model_id)
            ms_params = json.dumps({'morpheme_sequences': [likely_word, unlikely_word]})
            response = self.app.put(url(controller='morphemelanguagemodels', action='get_probabilities', id=morpheme_language_model_id), ms_params, self.json_headers, self.extra_environ_admin)
            resp = json.loads(response.body)
            newer_likely_word_log_prob = resp[likely_word]
            newer_unlikely_word_log_prob = resp[unlikely_word]
            assert pow(10, new_likely_word_log_prob) > pow(10, new_unlikely_word_log_prob)
            assert newer_unlikely_word_log_prob != unlikely_word_log_prob
            assert newer_likely_word_log_prob > new_likely_word_log_prob
            response = self.app.put(url(controller='morphemelanguagemodels', action='compute_perplexity', id=morpheme_language_model_id), {}, self.json_headers, self.extra_environ_admin)
            resp = json.loads(response.body)
            lm_perplexity_attempt = resp['perplexity_attempt']
            requester = lambda : self.app.get(url('morphemelanguagemodel', id=morpheme_language_model_id), headers=self.json_headers, extra_environ=self.extra_environ_admin)
            resp = self.poll(requester, 'perplexity_attempt', lm_perplexity_attempt, log, task_descr='GET PERPLEXITY OF LM %s' % morpheme_language_model_id)
            newest_perplexity = resp['perplexity']
            assert newest_perplexity < perplexity
            log.debug('Perplexity of Blackfoot LM %s (%s sentence corpus, ModKN, n=3, fixed vocabulary, corpus weighted towards nit-ihpiyi): %s' % (
             morpheme_language_model_id, word_count, newest_perplexity))
            sleep(1)
            return

    @nottest
    def test_z_cleanup(self):
        """Clean up after the tests."""
        TestController.tearDown(self, clear_all_tables=True, del_global_app_set=True, dirs_to_destroy=[
         'user', 'morpheme_language_model', 'corpus', 'morphological_parser'])