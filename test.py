import unittest
from flask import Flask
import pikepdf
from run import app
import os
class MetadataTest(unittest.TestCase):
    
    def test_index(self) :
        tester = app.test_client(self)
        response = tester.get("/")
        stat = response.status_code
        self.assertEqual(stat,200)

    def test_addtodb(self):
        tester = app.test_client(self)
        with open(os.path.join(os.path.dirname(__file__), 'Rapport.pdf'), 'rb') as fp:
            response = tester.post('/metadata', data={'file': (fp, 'Rapport.pdf')})
        self.assertEqual(response.status_code,200)
        self.assertIn(b'Producer', response.data)
        self.assertIn(b'Rapport', response.data)
    
    def test_display_table(self):
        tester = app.test_client(self)
        response = tester.get('/list')
        self.assertEqual(response.status_code,200)
        
        

if __name__ == '__main__':
    unittest.main()
