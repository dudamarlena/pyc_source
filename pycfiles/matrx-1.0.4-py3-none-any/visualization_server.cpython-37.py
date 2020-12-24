# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\haijet\PycharmProjects\matrx\matrx_visualizer\visualization_server.py
# Compiled at: 2020-03-26 09:09:11
# Size of source mod 2**32: 4095 bytes
import threading, logging
from flask import Flask, render_template, request, jsonify, send_from_directory
debug = True
port = 3000
app = Flask(__name__, template_folder='templates')
ext_media_folder = ''

@app.route('/human-agent/<id>')
def human_agent_view(id):
    """
    Route for HumanAgentBrain

    Parameters
    ----------
    id
        The human agent ID. Is obtained from the URL.

    Returns
    -------
    str
        The template for this agent's view.

    """
    return render_template('human_agent.html', id=id)


@app.route('/agent/<id>')
def agent_view(id):
    """
    Route for AgentBrain

    Parameters
    ----------
    id
        The agent ID. Is obtained from the URL.

    Returns
    -------
    str
        The template for this agent's view.

    """
    return render_template('agent.html', id=id)


@app.route('/god')
def god_view():
    """
    Route for the 'god' view which contains the ground truth of the world without restrictions.

    Returns
    -------
    str
        The template for this view.

    """
    return render_template('god.html')


@app.route('/')
@app.route('/start')
def start_view():
    """
    Route for the 'start' view which shows information about the current scenario, including links to all agents.

    Returns
    -------
    str
        The template for this view.

    """
    return render_template('start.html')


@app.route('/shutdown_visualizer', methods=['GET', 'POST'])
def shutdown():
    """ Shuts down the visualizer by stopping the Flask thread

    Returns
        True
    -------
    """
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Unable to shutdown visualizer server. Not running with the Werkzeug Server')
    func()
    print('Visualizer server shutting down...')
    return jsonify(True)


@app.route('/fetch_external_media/<path:filename>')
def external_media(filename):
    """ Facilitate the use of images in the visualization outside of the static folder

    Parameters
    ----------
    filename
        path to the image file in the external media folder of the user.

    Returns
    -------
        Returns the url (relative from the website root) to that file
    """
    global ext_media_folder
    return send_from_directory(ext_media_folder, filename, as_attachment=True)


def flask_thread():
    """
    Starts the Flask server on localhost:3000
    """
    global debug
    if not debug:
        log = logging.getLogger('werkzeug')
        log.setLevel(logging.ERROR)
    app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False)


def run_matrx_visualizer(verbose, media_folder):
    """
    Creates a seperate Python thread in which the visualization server (Flask) is started, serving the JS visualization
    :return: MATRX visualization Python thread
    """
    global debug
    global ext_media_folder
    debug = verbose
    ext_media_folder = media_folder
    print('Starting visualization server')
    print('Initialized app:', app)
    vis_thread = threading.Thread(target=flask_thread)
    vis_thread.start()
    return vis_thread


if __name__ == '__main__':
    run_matrx_visualizer()