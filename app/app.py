from flask import Flask, request
from flask_restful import Resource, Api
import config
from scrape import ListApartment,SearchApartment
import os

app = Flask(__name__)
api = Api(app)

app_config = config.read_config()


api.add_resource(SearchApartment, '/api/apartments/')
api.add_resource(ListApartment, '/api/apartments/<int:zipcode>')

app.run(port=app_config['application_port'], host='0.0.0.0',debug=True)