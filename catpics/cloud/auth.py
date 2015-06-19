import json
from requests import Session
import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()

from catpics.libs.utils import get_entry

class CloudApi(object):
    def __init__(self, cloud):
        self.username = cloud.username
        self.apikey = cloud.apikey
        self.identity = cloud.identity
        self.region = cloud.region
        self.session = Session()
        self._auth()

    def _auth(self):
        self.session.headers['Content-Type'] = 'application/json'
        payload = {
            "auth": {
                "RAX-KSKEY:apiKeyCredentials":{
                    "username": self.username,
                    "apiKey": self.apikey,
                }
            }
        }
        self.ident = self.session.post(self.identity, data=json.dumps(payload)).json()
        self.token = self.ident['access']['token']['id']
        self.catalog = self.ident['access']['serviceCatalog']
        self._load()

    def _load(self):
        pass
