import unittest
import sqlite3
import pikepdf
from flask import Flask
import requests

class MetadataTestCase(unittest.TestCase):
    URL = "http://127.0.0.1:5000"
    def setUp(self):
        self.app = Flask(__name__)
        self.pdf = pikepdf.Pdf.open("Rapport.pdf")
        self.pdf_info = self.pdf.docinfo
        self.filemetadata = {}
        for key, value in self.pdf_info.items():
            formatted_key = key.replace("/", "")
            self.filemetadata[formatted_key] = value

    def test_index(self):
        with self.app.test_client() as client:
            response = client.get('/')
            self.assertEqual(response.status_code, 200)
            self.assertTrue(b'Index Page' in response.data)

    def test_con(self):
            response = requests.get(self.URL)
            self.assertEqual(response.status_code, 200)

    def test_metadata(self):
        with self.app.test_client() as client:
            response = client.post('/metadata', data={'file': 'sample.pdf'}, content_type='multipart/form-data')
            self.assertEqual(response.status_code, 200)
            self.assertTrue(b'Metadata Page' in response.data)

    def test_addtodb(self):
        with self.app.test_client() as client:
            client.post('/metadata', data={'file': 'sample.pdf'}, content_type='multipart/form-data')
            response = client.post('/addtobdd', follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertTrue(b'Index Page' in response.data)

    def test_display_table(self):
        with self.app.test_client() as client:
            client.post('/metadata', data={'file': 'sample.pdf'}, content_type='multipart/form-data')
            client.post('/addtobdd', follow_redirects=True)
            response = client.get('/list')
            self.assertEqual(response.status_code, 200)
            self.assertTrue(b'List Page' in response.data)

    def test_search(self):
        with self.app.test_client() as client:
            client.post('/metadata', data={'file': 'sample.pdf'}, content_type='multipart/form-data')
            client.post('/addtobdd', follow_redirects=True)
            response = client.post('/search', data={'id': 1})
            self.assertEqual(response.status_code, 200)
            self.assertTrue(b'Search Page' in response.data)
    def test_one(self) : 
         with self.app.test_client() as client:
            self.assertEqual(1,1)

if __name__ == '__main__':
    unittest.main()
