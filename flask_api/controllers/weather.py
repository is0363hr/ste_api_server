from flask import Blueprint, jsonify, make_response, request, abort
from flask.wrappers import Response
from modules.meteorological_img import MeteImg, strToDate, image_file_to_base64
from apscheduler_img import Map_update


isDebug = True
weather_api = Blueprint("weather_api", __name__)

@weather_api.route("/weather", methods=['GET', 'POST'])
def get_weather():
    data = {}
    params = ['imgYear', 'imgMonth', 'imgDay', 'imgHour', 'imgMinute', 'lon', 'lat', 'zoom']
    try:
        if request.method == 'GET':
            print('GET')
            for param in params:
                data.update({
                    param: request.args.get(param, '')
                })

            date_data = strToDate(
                data['imgYear'],
                data['imgMonth'],
                data['imgDay'],
                data['imgHour'],
                data['imgMinute'],
            )
            mimg = MeteImg(
                date_data,
                data['lon'],
                data['lat'],
                int(data['zoom']),
            )
            img_path = mimg.cloud_create(True)
            print(img_path)
            img_bytes = image_file_to_base64(img_path)

            map_update = Map_update()
            map_update.request_insert_img(date_data, int(data['zoom']), img_path)

            response = make_response(img_bytes)
            response.headers.set('Content-Type', 'text/plain')
            return response
        elif request.method == 'POST':
            print('POST')
            # print(request.form['query'])
            # return request.form['query']
            response = {}
            response.headers.set('Content-Type', 'application/json')
            return make_response(jsonify(response))
        else:
            return abort(400)
    except Exception as e:
        return str(e)