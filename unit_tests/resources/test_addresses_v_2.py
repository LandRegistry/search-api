from flask import g
from search_api.main import app
import unittest
import mock
from mock import MagicMock, patch
from search_api.resources.V2_0.addresses_v_2 import search_for_addresses
import json


class TestAddressesV2(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    @patch('search_api.app.validate')
    @mock.patch('search_api.resources.V2_0.addresses_v_2.search_for_addresses')
    def test_get_address_found_with_postcode(self, mock_get_search, mock_validate):
        mock_get_search.return_value = "Test"
        get_response = self.app.get("/v2.0/search/addresses/postcode/SW1A 1AA",
                                    headers={'Content-Type': 'application/json',
                                             'Accept': 'application/json',
                                             'Authorization': 'Fake JWT'})
        self.assertEqual(get_response.status_code, 200)

    @patch('search_api.app.validate')
    @mock.patch('search_api.resources.V2_0.addresses_v_2.search_for_addresses')
    def test_get_address_not_found_with_postcode(self, mock_get_search, mock_validate):
        mock_get_search.return_value = "Test"
        get_response = self.app.get("/v2.0/search/addresses/postcode/XXXX XXX",
                                    headers={'Content-Type': 'application/json',
                                             'Accept': 'application/json',
                                             'Authorization': 'Fake JWT'})
        self.assertEqual(get_response.status_code, 422)

    @patch('search_api.app.validate')
    @mock.patch('search_api.resources.V2_0.addresses_v_2.search_for_addresses')
    def test_get_address_found_with_uprn(self, mock_get_search, mock_validate):
        mock_get_search.return_value = "Test"
        get_response = self.app.get("/v2.0/search/addresses/uprn/100023346367",
                                    headers={'Content-Type': 'application/json',
                                             'Accept': 'application/json',
                                             'Authorization': 'Fake JWT'})
        self.assertEqual(get_response.status_code, 200)

    @patch('search_api.app.validate')
    @mock.patch('search_api.resources.V2_0.addresses_v_2.search_for_addresses')
    def test_get_address_not_found_with_uprn(self, mock_get_search, mock_validate):
        mock_get_search.return_value = "Test"
        get_response = self.app.get("/v2.0/search/addresses/uprn/11111",
                                    headers={'Content-Type': 'application/json',
                                             'Accept': 'application/json',
                                             'Authorization': 'Fake JWT'})
        self.assertEqual(get_response.status_code, 422)

    @patch('search_api.app.validate')
    @mock.patch('search_api.resources.V2_0.addresses_v_2.search_for_addresses')
    def test_get_address_found_with_usrn(self, mock_get_search, mock_validate):
        mock_get_search.return_value = "Test"
        get_response = self.app.get("/v2.0/search/addresses/usrn/100023346367",
                                    headers={'Content-Type': 'application/json',
                                             'Accept': 'application/json',
                                             'Authorization': 'Fake JWT'})
        self.assertEqual(get_response.status_code, 200)

    @patch('search_api.app.validate')
    @mock.patch('search_api.resources.V2_0.addresses_v_2.search_for_addresses')
    def test_get_address_not_found_with_usrn(self, mock_get_search, mock_validate):
        mock_get_search.return_value = "Test"
        get_response = self.app.get("/v2.0/search/addresses/usrn/badusrn",
                                    headers={'Content-Type': 'application/json',
                                             'Accept': 'application/json',
                                             'Authorization': 'Fake JWT'})
        self.assertEqual(get_response.status_code, 422)

    @patch('search_api.app.validate')
    @mock.patch('search_api.resources.V2_0.addresses_v_2.search_for_addresses')
    def test_get_address_found_with_text(self, mock_get_search, mock_validate):
        mock_get_search.return_value = "Test"
        get_response = self.app.get("/v2.0/search/addresses/text/SW1A",
                                    headers={'Content-Type': 'application/json',
                                             'Accept': 'application/json',
                                             'Authorization': 'Fake JWT'})
        self.assertEqual(get_response.status_code, 200)

    @patch('search_api.app.validate')
    @patch('search_api.resources.V2_0.addresses_v_2.g')
    def test_get_address_invalid_postcode_in_valid_format(self, mock_request, mock_validate):
        response = MagicMock()
        response.status_code = 400
        response.json.return_value = "testing"
        mock_request.requests.post.return_value = response

        get_response = self.app.get("/v2.0/search/addresses/postcode/AB1 2CD", headers={
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': 'Fake JWT'})
        self.assertEqual(get_response.status_code, 400)
        self.assertEqual(json.loads(get_response.data.decode())['error_message'], "testing")

    @patch('search_api.app.validate')
    @patch('search_api.resources.V2_0.addresses_v_2.g')
    @patch('search_api.utilities.V2_0.address_response_mapper_v_2.map_address_response')
    def test_get_address_index_map(self, mock_mapper, mock_request, mock_validate):
        response_addr = MagicMock()
        response_addr.status_code = 200
        response_addr.json.return_value = [{"uprn": 1234}]
        mock_request.requests.post.return_value = response_addr

        response_index_uprn = MagicMock()
        response_index_uprn.status_code = 200
        response_index_uprn.json.return_value = ["ATITLE"]

        response_index_title = MagicMock()
        response_index_title.status_code = 200
        response_index_title.json.return_value = {"features": [{"not": "arealfeature"}]}

        mock_request.requests.get.side_effect = [response_index_uprn, response_index_title]

        mock_mapper.return_value = [{"uprn": 1234}]

        get_response = self.app.get("/v2.0/search/addresses/postcode/AB1 2CD?index_map=true", headers={
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': 'Fake JWT'})
        self.assertEqual(get_response.status_code, 200)
        self.assertEqual(json.loads(get_response.data.decode()), [
                         {"uprn": 1234, "index_map": {'type': 'FeatureCollection',
                                                      'features': [{'not': 'arealfeature'}]}}])

    @patch('search_api.app.validate')
    @patch('search_api.resources.V2_0.addresses_v_2.g')
    @patch('search_api.utilities.V2_0.address_response_mapper_v_2.map_address_response')
    def test_get_address_index_map_uprn_fail(self, mock_mapper, mock_request, mock_validate):
        response_addr = MagicMock()
        response_addr.status_code = 200
        response_addr.json.return_value = [{"uprn": 1234}]
        mock_request.requests.post.return_value = response_addr

        response_index_uprn = MagicMock()
        response_index_uprn.status_code = 500
        response_index_uprn.json.return_value = {"a": "fail"}

        mock_request.requests.get.side_effect = [response_index_uprn]

        mock_mapper.return_value = [{"uprn": 1234}]

        get_response = self.app.get("/v2.0/search/addresses/postcode/AB1 2CD?index_map=true", headers={
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': 'Fake JWT'})
        self.assertEqual(get_response.status_code, 500)
        self.assertEqual(json.loads(get_response.data.decode()), {'error_message': {'a': 'fail'}, 'error_code': 500})

    @patch('search_api.app.validate')
    @patch('search_api.resources.V2_0.addresses_v_2.g')
    @patch('search_api.utilities.V2_0.address_response_mapper_v_2.map_address_response')
    def test_get_address_index_map_uprn_notfound(self, mock_mapper, mock_request, mock_validate):
        response_addr = MagicMock()
        response_addr.status_code = 200
        response_addr.json.return_value = [{"uprn": 1234}]
        mock_request.requests.post.return_value = response_addr

        response_index_uprn = MagicMock()
        response_index_uprn.status_code = 404

        mock_request.requests.get.side_effect = [response_index_uprn]

        mock_mapper.return_value = [{"uprn": 1234}]

        get_response = self.app.get("/v2.0/search/addresses/postcode/AB1 2CD?index_map=true", headers={
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': 'Fake JWT'})
        self.assertEqual(get_response.status_code, 200)
        self.assertEqual(json.loads(get_response.data.decode()), [{'uprn': 1234}])

    @patch('search_api.app.validate')
    @patch('search_api.resources.V2_0.addresses_v_2.g')
    @patch('search_api.utilities.V2_0.address_response_mapper_v_2.map_address_response')
    def test_get_address_index_map_title_fail(self, mock_mapper, mock_request, mock_validate):
        response_addr = MagicMock()
        response_addr.status_code = 200
        response_addr.json.return_value = [{"uprn": 1234}]
        mock_request.requests.post.return_value = response_addr

        response_index_uprn = MagicMock()
        response_index_uprn.status_code = 200
        response_index_uprn.json.return_value = ["ATITLE"]

        response_index_title = MagicMock()
        response_index_title.status_code = 500
        response_index_title.json.return_value = {"a": "fail"}

        mock_request.requests.get.side_effect = [response_index_uprn, response_index_title]

        mock_mapper.return_value = [{"uprn": 1234}]

        get_response = self.app.get("/v2.0/search/addresses/postcode/AB1 2CD?index_map=true", headers={
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': 'Fake JWT'})
        self.assertEqual(get_response.status_code, 500)
        self.assertEqual(json.loads(get_response.data.decode()), {'error_message': {'a': 'fail'}, 'error_code': 500})

    def test_get_address_not_found_with_text(self):
        with app.test_request_context():
            g.requests = MagicMock()
            g.trace_id = '123'
            mock_response = MagicMock()
            mock_response._content = b'[]'
            mock_response.status_code = 200
            g.requests.post.return_value = mock_response

            try:
                search_for_addresses('foo')
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
                search_for_addresses('foo')
            except Exception as ex:
                self.assertEqual(ex.http_code, 500)
