import json
import os

from flask import Flask, request, make_response
from flask_cors import cross_origin
from pyowm import OWM

app = Flask(__name__)
owmapikey='c8537154778558a3c9e30c03f18a1672'
owm = OWM(owmapikey)


# geting and sending response to dialogflow
@app.route('/webhook', methods=['POST'])
@cross_origin()
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req))

    res = processRequest(req)

    res = json.dumps(res)
    print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


# processing the request from dialogflowOWM
def processRequest(req):
    result = req.get("queryResult")
    parameters = result.get("parameters")
    city = parameters.get("city")

    mgr = owm.weather_manager()
    observation = mgr.weather_at_place(str(city))
    w = observation.weather

    Weather_DetailedStatus =  w.detailed_status  # 'clouds'
    Weather_Wind = w.wind()  # {'speed': 4.6, 'deg': 330}
    Weather_Temperature = w.temperature('celsius')  # {'temp_max': 10.5, 'temp': 9.7, 'temp_min': 9.0}
    Weather_Rain = w.rain  # {}
    Weather_HeatIndex = w.heat_index  # None
    Weather_Could = w.clouds  # 75

    wind = w.wind()
    wind_speed = wind.get('speed')

    humidity = w.humidity

    speech = "Today's the weather in " + str(city) + " is \n Humidity :" + str(humidity) + ".\n Wind Speed :" + str(wind_speed) + ".\n Weather_DetailedStatus :" + str(Weather_DetailedStatus) + ".\n Weather_Wind  :" + str(Weather_Wind)+ ".\n Weather_Temperature :" + str(Weather_Temperature)+ ".\n Weather_Rain :" + str(Weather_Rain)+ ".\n Weather_HeatIndex  :" + str(Weather_HeatIndex)+ ".\n Weather_Could  :" + str(Weather_Could)

    return {
        "fulfillmentText": speech,
        "displayText": speech,
        # "Humidity": humidity,
        # "Wind Speed":wind_speed
    }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    print("Starting app on port %d" % port)
    app.run(debug=True)
