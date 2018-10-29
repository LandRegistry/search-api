from flask import g
from search_api.main import app
import unittest
import mock
from mock import MagicMock, patch
from search_api.resources.addresses import search_for_addresses
import json


class TestAddresses(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    @patch('search_api.app.validate')
    @mock.patch('search_api.resources.addresses.search_for_addresses')
    def test_get_address_found_with_postcode(self, mock_get_search, mock_validate):
        mock_get_search.return_value = "Test"
        get_response = self.app.get("/search/addresses/postcode/SW1A 1AA", headers={'Content-Type': 'application/json',
                                                                                    'Accept': 'application/json',
                                                                                    'Authorization': 'Fake JWT'})
        self.assertEqual(get_response.status_code, 200)

    @patch('search_api.app.validate')
    @mock.patch('search_api.resources.addresses.search_for_addresses')
    def test_get_address_not_found_with_postcode(self, mock_get_search, mock_validate):
        mock_get_search.return_value = "Test"
        get_response = self.app.get("/search/addresses/postcode/XXXX XXX", headers={'Content-Type': 'application/json',
                                                                                    'Accept': 'application/json',
                                                                                    'Authorization': 'Fake JWT'})
        self.assertEqual(get_response.status_code, 422)

    @patch('search_api.app.validate')
    @mock.patch('search_api.resources.addresses.search_for_addresses')
    def test_get_address_found_with_uprn(self, mock_get_search, mock_validate):
        mock_get_search.return_value = "Test"
        get_response = self.app.get("/search/addresses/uprn/100023346367", headers={'Content-Type': 'application/json',
                                                                                    'Accept': 'application/json',
                                                                                    'Authorization': 'Fake JWT'})
        self.assertEqual(get_response.status_code, 200)

    @patch('search_api.app.validate')
    @mock.patch('search_api.resources.addresses.search_for_addresses')
    def test_get_address_not_found_with_uprn(self, mock_get_search, mock_validate):
        mock_get_search.return_value = "Test"
        get_response = self.app.get("/search/addresses/uprn/11111", headers={'Content-Type': 'application/json',
                                                                             'Accept': 'application/json',
                                                                             'Authorization': 'Fake JWT'})
        self.assertEqual(get_response.status_code, 422)

    @patch('search_api.app.validate')
    @mock.patch('search_api.resources.addresses.search_for_addresses')
    def test_get_address_found_with_text(self, mock_get_search, mock_validate):
        mock_get_search.return_value = "Test"
        get_response = self.app.get("/search/addresses/text/SW1A", headers={'Content-Type': 'application/json',
                                                                            'Accept': 'application/json',
                                                                            'Authorization': 'Fake JWT'})
        self.assertEqual(get_response.status_code, 200)

    @patch('search_api.app.validate')
    @patch('search_api.resources.addresses.g')
    def test_get_address_invalid_postcode_in_valid_format(self, mock_request, mock_validate):
        response = MagicMock()
        response.status_code = 400
        response.json.return_value = "testing"
        mock_request.requests.post.return_value = response

        get_response = self.app.get("/search/addresses/postcode/AB1 2CD", headers={'Content-Type': 'application/json',
                                                                                   'Accept': 'application/json',
                                                                                   'Authorization': 'Fake JWT'})
        self.assertEqual(get_response.status_code, 400)
        self.assertEqual(json.loads(get_response.data.decode())['error_message'], "testing")

    def test_get_address_not_found_with_text(self):
        with app.test_request_context():
            g.requests = MagicMock()
            g.trace_id = '123'
            mock_response = MagicMock()
            mock_response._content = b'[]'
            mock_response.status_code = 200
            g.requests.post.return_value = mock_response

            try:
                search_for_addresses('foo', 'bar')
            except Exception as ex:
                self.assertEqual(ex.http_code, 404)

    def test_get_address_something_went_wrong(self):
        with app.test_request_context():
            g.requests = MagicMock()
            g.trace_id = '123'
            mock_response = MagicMock()
            mock_response.status_code = 500
            g.requests.post.return_value = mock_response

            try:
                search_for_addresses('foo', 'bar')
            except Exception as ex:
                self.assertEqual(ex.http_code, 500)
