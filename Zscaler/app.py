import json
import time
import requests
import logging
from apps import App, action

logger = logging.getLogger(__name__)

class Zscaler(App):
    def __init__(self, name, device, context):
        App.__init__(self, name, device, context)
        self.api_key = self.device.get_encrypted_field('api_key'))
        self.obfuscated_api_key = self.obfuscate_api_key
        self.api_username = self.device_fields['username'],
        self.api_password = self.device.get_encrypted_field('password'))
        
        self.api_host = self.device_fields['zscaler_instance']
        self.api_base_url = 'https://%s/api/v1/' % (api_host)
        self.api_headers = {
            'Content-Type': 'application/json',
            'Cache-Control': 'no-cache'
        }

    def obfuscate_api_key(self):
        seed = self.api_key
        now = int(time.time() * 1000)
        n = str(now)[-6:]
        r = str(int(n) >> 1).zfill(6)
        key = ''
        for i in range(0, len(str(n)), 1):
            key += seed[int(str(n)[i])]
        for j in range(0, len(str(r)), 1):
            key += seed[int(str(r)[j]) + 2]

        return key

    ### Session
    @action
    def create_session(self):
        url = api_base_url + 'authenticatedSession'
        data = json.dumps({
            'apiKey': self.obfuscated_api_key,
            'username': self.api_username,
            'password': self.api_key,
            'timestamp': int(time.time() * 1000)
        })
        response = requests.post(url, data=data, headers=api_headers)
        return response.cookies['JSESSIONID']
    
    @action
    def delete_session(self):
        headers = api_headersl
        headers['cookie'] = 'JSESSIONID=%s' % (session)
        url = api_base_url + 'authenticatedSession'
        response = requests.delete(url, headers=api_headers)
        return response.cookies['JSESSIONID']

    ### Configuration status
    @action
    def activate_config(self, session):
        headers = api_headers
        headers['cookie'] = 'JSESSIONID=%s' % (session)
        url = api_base_url + 'status/activate'
        response = requests.post(url, headers=headers)
        return response.json()
    

    ### URL Categories
    @action
    def url_categories(self, session, category_id=None):
        headers = api_headers
        headers['cookie'] = 'JSESSIONID=%s' % (session)
        url = api_base_url + 'urlCategories/%s' % (category_id)
        response = requests.get(url, headers=headers)
        return response.json()
    
    @action
    def url_lookup(self, session, domain_list):
        headers = api_headers
        headers['cookie'] = 'JSESSIONID=%s' % (authenticate())
        url = api_base_url + 'urlLookup'
        data = json.dumps(domain_list)
        response = requests.post(url, data=data, headers=headers)
        return response.json()
    
    @action
    def add_to_custom_category(self, session, category_id, domain_list):
        category_info = self.url_categories(session, category_id)
        
        data = {
            'configuredName': category_info['configuredName'],
            'superCategory': category_info['superCategory'],
            'dbCategorizedUrls': blocklist,
            'description': category_info['description']
        }
        headers = api_headers
        headers['cookie'] = 'JSESSIONID=%s' % (session)
        url = api_base_url + 'urlCategories/%s?action=ADD_TO_LIST' % (category_id)
        response = requests.put(url, data=json.dumps(data), headers=headers)
        return response.json()