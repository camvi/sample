# requires Python3.6 +

import requests
import urllib
import json
import base64

class Camvi:
    def __init__(self):
        # camvi connection credentials
        # replace 12.34.56.78 with your IP
        self.engine_ip = '12.34.56.78'
        self.engine_ip = 'localhost'
        self.username = 'admin'
        self.password = 'Camvi2017'
        self.auth_tok = ''

    def retrieve_auth_token(self):
        # retrieve auth token
        base_url = "http://"+self.engine_ip+":8080/service/api/user/login?"
        parameters = {
            "username": self.username,
            "password": base64.b64encode(self.password.encode('utf-8'))
        }
        self.auth_tok = requests.post(base_url + urllib.parse.urlencode(parameters)).json()
        return self.auth_tok

    def image_to_base64(self, img):
        # convert face img to base64
        prependInfo = 'data:image/jpeg;base64,'
        encodedString = base64.b64encode(img).decode("utf-8")
        fullString = str(prependInfo) + encodedString
        return str(fullString)

    def retrieve_person_name(self, img):
        base_url = "http://"+self.engine_ip+":8080/service/api/recognize?"
        # base_url = "http://{self.engine_ip}:8080/service/api/recognize?"
        parameters = {
            "group-id": '0'
        }
        data = {
            "image-data": self.image_to_base64(img)
        }
        r = requests.post(base_url + urllib.parse.urlencode(parameters),headers={'Authorization': self.auth_tok}, data=data).json()
        return r


camvi = Camvi()
camvi.retrieve_auth_token()

with open('/path/to/your/image', "rb") as img:
    person_name = camvi.retrieve_person_name(img.read())
    print (person_name)

