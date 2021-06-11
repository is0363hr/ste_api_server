from interceptors.errorHandler import *
from interceptors.Auth import *
from application import app
from controllers.index import index_page
from controllers.weather import weather_api

from flask_debugtoolbar import DebugToolbarExtension

toolbar = DebugToolbarExtension(app)


app.register_blueprint(index_page, url_prefix="/")
app.register_blueprint(weather_api, url_prefix="/api")