# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/kushalkatta/workspace/Electron/SmartMirror/smart_mirror/smart_mirror/app.py
# Compiled at: 2018-09-21 02:49:10
# Size of source mod 2**32: 22530 bytes
from flask import Flask, render_template, jsonify, request, redirect, url_for
from smart_mirror import app, socketio
from flask_socketio import emit, send
import datetime
from zomato import Zomato
from pywit import RecognizeSpeech
import time

@socketio.on('voice_search')
def s_voice_search(message):
    voice_search()


def voice_search():
    text = RecognizeSpeech('myspeech.wav', 4)
    if 'entities' not in text:
        return
    elif 'intent' in text['entities']:
        if len(text['entities']['intent']) > 0 and 'value' in text['entities']['intent'][0]:
            value = text['entities']['intent'][0]['value']
            if value == 'calendar':
                socketio.emit('calendar', '', broadcast=True, include_self=False)
            else:
                if value == 'home':
                    socketio.emit('home', '', broadcast=True, include_self=False)
                else:
                    if value == 'homepage':
                        socketio.emit('home', '', broadcast=True, include_self=False)
                    else:
                        if value == 'clock':
                            socketio.emit('time', '', broadcast=True, include_self=False)
                        else:
                            if value == 'youtube':
                                socketio.emit('yoututbe', '', broadcast=True, include_self=False)
                            else:
                                if value == 'news':
                                    socketio.emit('news', '', broadcast=True, include_self=False)
                                else:
                                    if value == 'route':
                                        if 'train' in text['entities']:
                                            trainNo = text['entities']['train'][0]['value']
                                            socketio.emit('train_route', ('/' + str(trainNo)), broadcast=True, include_self=False)
                                        else:
                                            socketio.emit('train_route', '/12480', broadcast=True, include_self=False)
                                    else:
                                        if value == 'weather':
                                            if 'location' in text['entities']:
                                                location = text['entities']['location'][0]['value']
                                                socketio.emit('weather', ('/' + str(location)), broadcast=True, include_self=False)
                                            else:
                                                socketio.emit('home', '', broadcast=True, include_self=False)
            if 'Zomato_category' in text['entities']:
                if len(text['entities']['Zomato_category']) > 0:
                    if 'value' in text['entities']['Zomato_category'][0]:
                        value = text['entities']['Zomato_category'][0]['value']
                        category_id = zomato.getCategoryNo(value)
                        if category_id:
                            socketio.emit('zomato', ('/categories/' + str(category_id)), broadcast=True, include_self=False)
        else:
            if 'Zomato_cuisines' in text['entities']:
                if len(text['entities']['Zomato_cuisines']) > 0:
                    if 'value' in text['entities']['Zomato_cuisines'][0]:
                        value = text['entities']['Zomato_cuisines'][0]['value']
                        cuisine_id = zomato.getCuisineNo(value)
                        if cuisine_id:
                            socketio.emit('zomato', ('/cuisines/' + str(cuisine_id)), broadcast=True, include_self=False)
    else:
        if 'Destination' in text['entities']:
            if len(text['entities']['Destination']) > 0:
                if 'value' in text['entities']['Destination'][0]:
                    destination = text['entities']['Destination'][0]['value']
                    if 'Source' in text['entities']:
                        source = text['entities']['Source'][0]['value']
                    else:
                        if 'location' in text['entities']:
                            source = text['entities']['location'][0]['value']
                        else:
                            source = getLocation()
                    socketio.emit('railway', ('?source_station=' + source + '&destination_station=' + destination + '&journey_date=2018-09-21'), broadcast=True, include_self=False)
    if 'Source' in text['entities']:
        print('train enq')
        if len(text['entities']['Source']) > 0:
            if 'value' in text['entities']['Source'][0]:
                source = text['entities']['Source'][0]['value']
                if 'Destination' in text['entities']:
                    destination = text['entities']['Destination'][0]['value']
                else:
                    if 'location' in text['entities']:
                        destination = text['entities']['location'][0]['value']
                    else:
                        destination = getLocation()
                    if 'datetime' in text['entities']:
                        dateTime = text['entities']['datetime'][0]['value']
                        dateTime = dateTime[0:10]
                    else:
                        dateTime = '2018-09-21'
                    print(dateTime)
                    socketio.emit('railway', ('?source_station=' + source + '&destination_station=' + destination + '&journey_date=' + dateTime), broadcast=True, include_self=False)
    if 'intent' in text['entities']:
        if len(text['entities']['intent']) > 0:
            if 'value' in text['entities']['intent'][0]:
                if value == 'ticket':
                    socketio.emit('railway', '', broadcast=True, include_self=False)
                elif value == 'railway':
                    socketio.emit('railway', '', broadcast=True, include_self=False)


@socketio.on('railway')
def s_railway(message):
    emit('railway', '', broadcast=True, include_self=False)


@socketio.on('train_route')
def s_train_route(message):
    emit('train_route', '/12480', broadcast=True, include_self=False)


@socketio.on('home')
def s_home(message):
    emit('home', '', broadcast=True, include_self=False)


@socketio.on('zomato')
def s_zomato(message):
    emit('zomato', '', broadcast=True, include_self=False)


@socketio.on('news')
def s_news(message):
    emit('news', '', broadcast=True, include_self=False)


@socketio.on('youtube')
def s_youtube(message):
    emit('youtube', '', broadcast=True, include_self=False)


@socketio.on('calendar')
def s_calendar(message):
    emit('calendar', '', broadcast=True, include_self=False)


@socketio.on('toggleLED')
def s_toggleLED(message):
    emit('toggleLED', '', broadcast=True, include_self=False)


@socketio.on('time')
def s_time(message):
    emit('time', '', broadcast=True, include_self=False)


@socketio.on('weather')
def s_weather(message):
    emit('weather', '/Pune', broadcast=True, include_self=False)


@app.route('/toggleLED')
def toggleLight():
    socketio.emit('toggleLED', '', broadcast=True)
    return ''


@app.route('/remote')
def remote():
    return render_template('remoteControl.html')


@app.route('/template')
def template():
    return render_template('template.html')


@app.route('/youtube')
def youtube():
    return '\n    <iframe src="https://www.youtube.com/embed/3xokKYrHibc"  style="position:fixed; top:0px; left:0px; bottom:0px; right:0px; width:100%; height:100%; border:none; margin:0; padding:0; overflow:hidden; z-index:999999;" allowfullscreen>\n    </iframe>\n    '


@app.route('/calendar')
def getCalendar():
    return render_template('calendar.html')


@app.route('/news', methods=['GET'])
def getNews():
    from gnewsclient import gnewsclient
    client = gnewsclient()
    country = request.args.get('country')
    if country:
        client.edition = country
    language = request.args.get('language')
    if language:
        client.language = language
    topic = request.args.get('topic')
    if topic:
        client.topic = topic
    query = request.args.get('query')
    if query:
        client.query = query
    return render_template('news.html', articles=(client.get_news()), client=client, country=country, language=language, topic=topic)


@app.route('/railway')
def getRailway():
    source_station = request.args.get('source_station')
    destination_station = request.args.get('destination_station')
    journey_date = request.args.get('journey_date')
    if journey_date:
        journey_date = datetime.datetime.strptime(journey_date, '%Y-%m-%d').strftime('%d-%m-%Y')
    else:
        if source_station and destination_station and journey_date:
            import requests
            url = 'https://api.railwayapi.com/v2/suggest-station/name/' + source_station + '/apikey/ep6m37hkms/'
            response = requests.get(url).json()
            url = validStation(response) or 'https://api.railwayapi.com/v2/code-to-name/code/' + source_station + '/apikey/ep6m37hkms/'
            response = requests.get(url).json()
            if not validStation(response):
                return 'Invalid Source Station Name'
            for station in response['stations']:
                if station['code'].lower() == source_station.lower():
                    source_station = station['code']
                    break

            if not source_station:
                source_station = response['stations'][0]['code']
        else:
            source_station = response['stations'][0]['code']
    url = 'https://api.railwayapi.com/v2/suggest-station/name/' + destination_station + '/apikey/ep6m37hkms/'
    response = requests.get(url).json()
    if not validStation(response):
        url = 'https://api.railwayapi.com/v2/code-to-name/code/' + destination_station + '/apikey/ep6m37hkms/'
        response = requests.get(url).json()
        if not validStation(response):
            return 'Invalid Destination Station Name'
        for station in response['stations']:
            if station['code'].lower() == destination_station.lower():
                destination_station = station['code']
                break

        if not destination_station:
            destination_station = response['stations'][0]['code']
        else:
            destination_station = response['stations'][0]['code']
        return redirect(url_for('getTrainsList', source=source_station, destination=destination_station, journey_date=journey_date))
    else:
        return render_template('railway.html')


def validStation(response):
    if 'stations' not in response:
        return False
    else:
        if not len(response['stations']) > 0:
            return False
        if 'code' not in response['stations'][0]:
            return False
        return True


@app.route('/trains_list/<source>/<destination>/<journey_date>')
def getTrainsList(source, destination, journey_date):
    import requests
    url = 'https://api.railwayapi.com/v2/between/source/' + source + '/dest/' + destination + '/date/' + journey_date + '/apikey/ep6m37hkms/'
    response = requests.get(url).json()
    list = response['trains']
    return render_template('trains_list.html', trains_list=list, source=source, destination=destination, journey_date=journey_date)


@app.route('/train_route/<int:train_no>')
def getTrainRoute(train_no):
    import requests
    url = 'https://api.railwayapi.com/v2/route/train/' + str(train_no) + '/apikey/ep6m37hkms/'
    response = requests.get(url).json()
    train = response['train']
    route = response['route']
    return render_template('train_route.html', train=train, route=route)


@app.route('/time')
def showTime():
    return render_template('snippet_time.html')


@app.route('/weather/<cityName>')
def getWeathe(cityName):
    from weather import Weather, Unit
    weather = Weather(unit=(Unit.CELSIUS))
    location = weather.lookup_by_location(cityName)
    if location:
        weatherDetails = {'City':location.location.city,  'State':location.location.region, 
         'Country':location.location.country, 
         'Sunrise':location.astronomy['sunrise'], 
         'Sunset':location.astronomy['sunset'], 
         'Humidity':location.atmosphere['humidity'], 
         'Temp':location.condition.temp, 
         'Condition':location.condition.text}
        return render_template('snippet_weather.html', weather=weatherDetails, cityName=cityName)
    else:
        return ''


@app.route('/')
def hello():
    return redirect(url_for('getWeather', cityName=(getLocation())))


def getLocation():
    import geocoder
    g = geocoder.ip('me')
    return g.response.json()['city']


@app.route('/home')
def home():
    return render_template('home.html')


from zomato import Zomato
zomato = Zomato()

def setZomatoParameters():
    your_location = request.args.get('your_location')
    if not your_location:
        your_location = getLocation()
        print('Location: ' + str(your_location))
    zomato.setLocation(your_location)
    search_query = request.args.get('search_query')
    zomato.setSearchQuery(search_query)


def getZomato(restaurants=None):
    if not restaurants:
        restaurants = zomato.getBestRestaurants()
    return render_template('zomato.html', your_location=(zomato.getLocation()['title']), search_query=(zomato.getSearchQuery()), categories=(zomato.getCategories()), establishments=(zomato.getEstablishments()), cuisines=(zomato.getCuisines()), collections=(zomato.getCollections()), restaurants=restaurants)


@app.route('/zomato')
def showZomato():
    setZomatoParameters()
    return getZomato()


@app.route('/zomato/categories/<int:category_id>')
def showZomatoCategories(category_id):
    return redirect(url_for('showZomatoCategoriesPageNo', category_id=category_id, pageNo=1))


@app.route('/zomato/categories/<int:category_id>/<int:pageNo>')
def showZomatoCategoriesPageNo(category_id, pageNo):
    setZomatoParameters()
    return getZomato(restaurants=(zomato.getRestaurants_by_category(category_id, pageNo - 1)))


@app.route('/zomato/establishments/<int:establishment_id>')
def showZomatoEstablishments(establishment_id):
    return redirect(url_for('showZomatoEstablishmentsPageNo', establishment_id=establishment_id, pageNo=1))


@app.route('/zomato/establishments/<int:establishment_id>/<int:pageNo>')
def showZomatoEstablishmentsPageNo(establishment_id, pageNo):
    setZomatoParameters()
    return getZomato(restaurants=(zomato.getRestaurants_by_establishment(establishment_id, pageNo - 1)))


@app.route('/zomato/cuisines/<int:cuisine_id>')
def showZomatoCuisines(cuisine_id):
    return redirect(url_for('showZomatoCuisinesPageNo', cuisine_id=cuisine_id, pageNo=1))


@app.route('/zomato/cuisines/<int:cuisine_id>/<int:pageNo>')
def showZomatoCuisinesPageNo(cuisine_id, pageNo):
    setZomatoParameters()
    return getZomato(restaurants=(zomato.getRestaurants_by_cuisine(cuisine_id, pageNo - 1)))


@app.route('/zomato/collections/<int:collection_id>')
def showZomatoCollections(collection_id):
    return redirect(url_for('showZomatoCollectionsPageNo', collection_id=collection_id, pageNo=1))


@app.route('/zomato/collections/<int:collection_id>/<int:pageNo>')
def showZomatoCollectionsPageNo(collection_id, pageNo):
    setZomatoParameters()
    return getZomato(restaurants=(zomato.getRestaurants_by_collection(collection_id, pageNo - 1)))


@app.route('/zomato/all')
def showAllZomato():
    return redirect(url_for('showAllZomatoPageNo', pageNo=1))


@app.route('/zomato/all/<int:pageNo>')
def showAllZomatoPageNo(pageNo):
    setZomatoParameters()
    return getZomato(restaurants=(zomato.getRestaurants(pageNo - 1)))


@app.route('/home/<cityName>')
def getWeather(cityName):
    from weather import Weather, Unit
    weather = Weather(unit=(Unit.CELSIUS))
    location = weather.lookup_by_location(cityName)
    if location:
        weatherDetails = {'City':location.location.city,  'State':location.location.region, 
         'Country':location.location.country, 
         'Sunrise':location.astronomy['sunrise'], 
         'Sunset':location.astronomy['sunset'], 
         'Humidity':location.atmosphere['humidity'], 
         'Temp':location.condition.temp, 
         'Condition':location.condition.text}
        return render_template('home.html', weather=weatherDetails, cityName=cityName)
    else:
        return ''