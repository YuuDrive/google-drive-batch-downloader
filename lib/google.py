'''
Credited to 
https://stackoverflow.com/questions/25010369/wget-curl-large-file-from-google-drive
with a little improvised
'''

import requests
from tqdm import tqdm

class GDirect(object):
    GOGOLE_URL = "https://docs.google.com/uc?export=download"
    direct_url = None
    google_response = None

    def __init__(self, **kwargs):
        self.session = requests.Session()
        self.destination = kwargs.get('destination', None)
    
    def __confirm_token(self, response):
        for key, value in response.cookies.items():
            if key.startswith('download_warning'):
                return value
        return None

    def get_direct(self, google_id):
        try:
            self.google_id = google_id
            response = self.session.get(self.GOGOLE_URL, params = { 'id' : google_id }, stream = True)
            token = self.__confirm_token(response)
            if token:
                params = { 'id' : google_id, 'confirm' : token }
                response = self.session.get(self.GOGOLE_URL, params = params, stream = True)
            self.direct_url = response.url
            self.destination = f'./downloads/{google_id}'
            self.google_response = response
            return response
        except Exception as e:
            return None

    def download(self, *args, **kwargs):
        CHUNK_SIZE = 32768
        response = self.google_response
        destination = kwargs.get('destination', self.destination)
        with open(destination, "wb") as f:
            with tqdm(unit='B', unit_scale=True, unit_divisor=1024) as bar:
                for chunk in response.iter_content(CHUNK_SIZE):
                    if chunk:
                        f.write(chunk)
                        bar.update(CHUNK_SIZE)

    @property
    def url(self):
        return self.direct_url