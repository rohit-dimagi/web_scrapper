from flask import request
from flask_restful import Resource, reqparse
from helper import Helper
import webcrawl

class ListApartment(Resource):
    def get(self,zipcode):
        if Helper.check_valid_pincode(self,zipcode):
            city_name = Helper.get_cityname(self,zipcode)
            if city_name:
                data = webcrawl.calculate_response(city_name)
                if data:
                    return {"data": data}
                else: 
                    return {'status': 500, 'message': 'internal sever error, please retry'}
            else:
                return {'status': 500, 'message': 'Internal server error, please retry'}
        else:
            return {'status': 400, 'message': 'zip code is not allowed', 'extra': 'allowed values are --'}

class SearchApartment(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('bathroom', type=int,required=True)
        parser.add_argument('bedroom', type=int,required=True)
        parser.add_argument('zipcode', type=int,required=True)
        args = parser.parse_args()

        if Helper.check_valid_pincode(self,args['zipcode']):
            city_name = Helper.get_cityname(self,args['zipcode'])
            if city_name:
                data = webcrawl.calculate_response(city_name,bathroom=args['bathroom'],bedroom=args['bedroom'])
                if data:
                    return {"data": data}
                else: 
                    return {'status': 500, 'message': 'internal sever error, please retry'}
            else:
                return {'status': 500, 'message': 'Internal server error, please retry'}
        else:
            return {'status': 400, 'message': 'zip code is not allowed', 'extra': 'allowed values are --'}        