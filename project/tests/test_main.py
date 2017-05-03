# project/server/tests/test_main.py


import unittest
import yaml

from base import BaseTestCase


class TestMainBlueprint(BaseTestCase):

    def test_index(self):
        # Ensure Flask is setup.
        response = self.client.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Crawlcheck's report", response.data)
        self.assertIn(b'All recorded transactions', response.data)
        self.assertIn(b'All findings', response.data)
        self.assertIn(b'Transactions', response.data)
        self.assertIn(b'Defects', response.data)
        self.assertIn(b'Links', response.data)
        #self.assertIn(b'Register/Login', response.data)

    def test_about(self):
        # Ensure about route behaves correctly.
        response = self.client.get('/about', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'About', response.data)

    def test_404(self):
        # Ensure 404 error is handled.
        response = self.client.get('/404')
        self.assert404(response)
        self.assertTemplateUsed('errors/404.html')

    def test_rest(self):
        response = self.client.delete('/data')
        self.assertEqual(response.status_code, 200)
        payload = dict()
        transaction = dict()
        transaction['id'] = 1
        transaction['method'] = 'GET'
        transaction['responseStatus'] = 200
        transaction['contentType'] = 'text/html'
        transaction['verificationStatusId'] = 0
        transaction['depth'] = 0
        transaction['uri'] = 'http://localhost'
        transaction['parentId'] = 1
        payload['transactions'] = [transaction]
        
        response = self.client.post('/data', data={'payload' : yaml.dump(payload)})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(b'Update data: 1', response.data)

        response = self.client.get('/transaction')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'http://localhost', response.data)
        self.assertIn(b'200', response.data)
        self.assertIn(b'text/html', response.data)




if __name__ == '__main__':
    unittest.main()
