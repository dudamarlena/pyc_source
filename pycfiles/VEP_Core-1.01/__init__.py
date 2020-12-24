# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\LocalUsers\ealexand\VEP_Core\vep_core\Serendip\__init__.py
# Compiled at: 2014-10-17 12:17:08
import os, json
from flask import Flask, url_for, redirect, send_from_directory
import CorpusViewer, TextViewer, Utilities, Ity
from Support.flask_util_js.flask_util_js import FlaskUtilJs
app = Flask(__name__)
app.jinja_options = dict(extensions=[
 'jinja2.ext.do',
 'jinja2.ext.autoescape'])
app.config.from_object('config.DevelopmentConfig')
fujs = FlaskUtilJs(app)

def get_colors():
    colors_str_prefix = 'app_colors = '
    colors_path = os.path.join(app.static_folder, 'js', 'app_colors.json')
    colors_file = open(colors_path, 'rU')
    colors_str = colors_file.read()
    colors_file.close()
    if colors_str.startswith(colors_str_prefix):
        colors_str = colors_str[len(colors_str_prefix):]
    colors = json.loads(colors_str)
    return colors


app.config.update(COLORS=get_colors())

@app.context_processor
def inject_colors():
    return dict(colors=app.config['COLORS'])


@app.route('/css/HTMLFormatter.css')
def get_html_formatter_css():
    return send_from_directory(os.path.join(Ity.root, 'Formatters', 'HTMLFormatter', 'templates'), 'styles.css')


@app.route('/css/LineGraphFormatter.css')
def get_line_graph_formatter_css():
    return send_from_directory(os.path.join(Ity.root, 'Formatters', 'LineGraphFormatter', 'templates'), 'styles.css')


@app.route('/')
def index():
    return redirect(url_for('corpus_view_by_name', corpus_name=app.config['DEFAULT_CORPUS_NAME']))


@app.route('/corpus:<path:corpus_name>/')
def redirect_corpus_view(corpus_name):
    return redirect(url_for('corpus_view_by_name', corpus_name=corpus_name))


app.add_url_rule('/corpus:<path:corpus_name>/matrix', 'corpus_view_by_name', CorpusViewer.view_by_name)
app.add_url_rule('/corpus:<path:corpus_name>/meso', 'corpus_mesoview', CorpusViewer.mesoview)
app.add_url_rule('/corpus:<path:corpus_name>/_getMetadata', 'corpus_get_metadata', CorpusViewer.get_metadata)
app.add_url_rule('/corpus:<path:corpus_name>/_getTheta', 'corpus_get_theta', CorpusViewer.get_theta)
app.add_url_rule('/_getCorpora', 'get_corpora', Utilities.get_corpora)
app.add_url_rule('/corpus:<path:corpus_name>/_get_word_rankings/<rankingType>/<words>', 'get_word_rankings_json', Utilities.get_word_rankings_json)
app.add_url_rule('/corpus:<path:corpus_name>/wordRankings/<rankingType>/<wordColorPairs>', 'wordRankings', Utilities.wordRankings)
app.add_url_rule('/corpus:<path:corpus_name>/wordRankings/', 'wordRankingsDefault', Utilities.wordRankingsDefault)
app.add_url_rule('/corpus:<corpus_name>/get_word_ranking/<rankingType>/<word>', 'get_word_ranking', Utilities.get_word_ranking)
app.add_url_rule('/corpus:<path:corpus_name>/_setGroupName/<group_file>/<group_name>/<group>', 'corpus_set_group_name', CorpusViewer.set_group_name)
app.add_url_rule('/corpus:<path:corpus_name>/_getGroups/<group_file>', 'corpus_get_groups', CorpusViewer.get_groups)
app.add_url_rule('/corpus:<path:corpus_name>/_getAnovaOrder/<fieldName>', 'corpus_get_anova_order', CorpusViewer.getAnovaOrder)
app.add_url_rule('/corpus:<path:corpus_name>/_getContrastOrder/<fieldName>/<group1>/<group2>', 'corpus_get_contrast_order', CorpusViewer.getContrastOrder)
app.add_url_rule('/corpus:<path:corpus_name>/_getTopic/<topic_num>/<num_words>/<ranking_type>', 'corpus_get_topic', CorpusViewer.get_topic)
app.add_url_rule('/corpus:<path:corpus_name>/_getTopicNames/', 'corpus_get_topic_names', CorpusViewer.get_topic_names)
app.add_url_rule('/corpus:<path:corpus_name>/_setTopicName/<topic_num>/<topic_name>/<num_topics>', 'corpus_set_topic_name', CorpusViewer.set_topic_name)
app.add_url_rule('/corpus:<path:corpus_name>/malletText:<text_name>/', 'text_mallet_view_by_name', TextViewer.mallet_view_by_name)
app.add_url_rule('/corpus:<path:corpus_name>/malletText:<text_name>/lineGraph/<ranking_type>', 'text_get_mallet_line_graph', TextViewer.get_mallet_line_graph)

@app.route('/corpus:<path:corpus_name>/text:<text_name>/topic_model_html_partial.json/')
def text_get_html_partial(corpus_name, text_name):
    return redirect(url_for('text_get_html_partial_for_tag_maps', corpus_name=corpus_name, text_name=text_name, start_index=1, end_index=app.config['TEXTVIEWER_DEFAULT_NUM_TAG_MAPS']))


@app.route('/corpus:<path:corpus_name>/text:<text_name>/topic_model_html_partial.json/tag_maps:<int:start_index>')
def text_get_html_partial_for_tag_maps_start_only(corpus_name, text_name, start_index):
    return redirect(url_for('text_get_html_partial_for_tag_maps', corpus_name=corpus_name, text_name=text_name, start_index=start_index, end_index=start_index))


@app.route('/corpus:<path:corpus_name>/text:<text_name>/topic_model_html_partial.json/tag_maps:<int:start_index>:<int:num_tag_maps>')
def text_get_html_partial_for_tag_maps_start_and_count(corpus_name, text_name, start_index, num_tag_maps):
    return redirect(url_for('text_get_html_partial_for_tag_maps', corpus_name=corpus_name, text_name=text_name, start_index=start_index, end_index=start_index + num_tag_maps - 1))


if __name__ == '__main__':
    app.run()