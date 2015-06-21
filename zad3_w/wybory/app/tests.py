from django.test import TestCase, Client
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
import unittest
from selenium import webdriver
from models import Obwod, Gmina
import json

class InitsTestCase(TestCase):
    def setUp(self):
        g = Gmina.objects.create(nazwa="Jakas")
        Gmina.objects.create(nazwa="Jakas2")
        Obwod.objects.create(adres="Blabla", gmina=g)

    def test_default_values(self):
        ob = Obwod.objects.get(adres="Blabla")
        self.assertEqual(ob.wersja, 0)
        self.assertEqual(ob.uprawnionych, 0)
        self.assertEqual(ob.ileKart, 0)

    def test_gmina_setting(self):
        ob = Obwod.objects.get(adres="Blabla")
        gm = Gmina.objects.get(nazwa="Jakas")
        gm2 = Gmina.objects.get(nazwa="Jakas2")
        self.assertEqual(ob.gmina, gm)
        self.assertNotEqual(ob.gmina, gm2)


class TestClient(unittest.TestCase):
    def setUp(self):
        # Every test needs a client.
        self.client = Client()
        g = Gmina.objects.create(nazwa="Jakas")
        self.o = Obwod.objects.create(adres="Blabla", gmina=g)


    def test_getting_obwod(self):
        response = self.client.post('/obwod/', {'obw_id': self.o.id})

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.content)
        self.assertEqual(self.o.toDict(), data)

    def test_saving_obwod(self):
        response = self.client.post('/save/', {'obw_id': self.o.id, 'ileKart': '3', 'upr': '4', 'wer': '0'})

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.content)

        self.assertEqual(1, data['dict']['wer'])
        self.assertEqual('3', data['dict']['ile'])
        self.assertEqual('4', data['dict']['upr'])
        self.assertEqual(self.o.id, data['dict']['id'])
        self.assertEqual('Blabla', data['dict']['adres'])
        self.assertEqual(False, data['err'])


class SeleniumTestCase(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        # self.browser.maximize_window()
        g = Gmina.objects.create(nazwa="Jakas")
        Obwod.objects.create(adres="Blabla", gmina=g)

    def tearDown(self):
        # Call tearDown to close the web browser
        self.browser.quit()

    def testPageTitle(self):
        self.browser.get('%s' % self.live_server_url)
        edyt = self.browser.find_element_by_class_name("edytuj")
        self.assertTrue(edyt.is_displayed())
        edyt.click()
        self.assertFalse(edyt.is_displayed())

        self.browser.find_element_by_class_name("anuluj").click()
        self.assertTrue(edyt.is_displayed())

if __name__ == '__main__':
    unittest.main(verbosity=2)

