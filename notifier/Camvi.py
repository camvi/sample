import requests
import json
import zmq
import base64
import urllib
from config import camvi_options


class Camvi:
    def __init__(self, timeout=1):
        self.ip = camvi_options['ip']
        self.port = camvi_options['port']
        self.listen_on = 'tcp://{}:2687'.format(self.ip)
        self.username = camvi_options['username']
        self.password = camvi_options['password']
        self.timeout = timeout

    def listen(self):
        self.sock = zmq.Context().socket(zmq.SUB)
        self.sock.setsockopt(zmq.SUBSCRIBE, b"")
        self.sock.connect(self.listen_on)
        print('listening on {}'.format(self.listen_on))

    def event(self):
        return json.loads(self.sock.recv().decode())

    def get_group(self, person_id, tok):
        base_url = "http://{}:{}/service/api/person/query?person-id={}".format(self.ip, self.port, str(person_id))
        resp = requests.get(base_url, headers={'Authorization': tok}, timeout=self.timeout).json()

        # if unknown return dict of group_name = unknwon:
        resp_code = resp.get('code')
        if resp_code is not None and resp_code == 1001:
            group = [{'id': 0, 'name': 'unknown'}]
            return group
        else:
            return resp['groups']

    def retrieve_auth_token(self):
        base_url = "http://{}:{}/service/api/user/login?".format(self.ip, self.port)
        parameters = {
            "username": self.username,
            "password": base64.b64encode(self.password.encode('utf-8'))
        }
        full_url = base_url + urllib.parse.urlencode(parameters)
        tok = requests.post(full_url, timeout=self.timeout).json()
        return tok

    def get_log_image(self, log_id, tok):
        base_url = "http://{}:{}/service/api/log/image/{}.jpeg".format(self.ip, self.port, log_id)
        log_image = requests.get(base_url, headers={'Authorization': tok}, timeout=self.timeout).content
        return log_image
