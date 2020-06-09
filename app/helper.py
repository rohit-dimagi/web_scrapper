import json
import config
import requests

#SOME HELPER FUNCTION TO GET DETAILS OF CITY WITH ZIPCODE
class Helper:
    def __init__(self, config_file):
        self.config_file = config_file

    def check_valid_pincode(self, zipcode):
        valid_zipcode = config.read_config()['zipcode']
        if zipcode in valid_zipcode:
            return True
        else:
            return False
        
    def get_cityname(self, zipcode):
        url = config.read_config()['zipcode_url']+"/"+str(zipcode)
        resp = requests.get(url)
        if resp.status_code == 200:
            json_data = json.loads(resp.text)
            full_city_name = "{0}-{1}".format(json_data['city'], json_data['state'])
            return full_city_name
        else:
            return None 
