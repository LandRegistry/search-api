from search_api import main
from flask_testing import TestCase
from flask import url_for
from mock import patch
from unittest.mock import MagicMock
import json

CHARGE_ID = 'LLC-6521'
INVALID_CHARGE_ID = 'some_invalid_charge_id'

GET_LOCAL_LAND_CHARGES_ROUTE = 'local_land_charge_V_2.get_local_land_charges'
POST_LOCAL_LAND_CHARGES_ROUTE = 'local_land_charge_V_2.post_local_land_charges'

BASE64_GEO = "eyJjb29yZGluYXRlcyI6WzQ0ODY4MS41Mzc1MDAwMDAwMywyNzk2NTkuMTEyNV0sInR5cGUiOiJQb2ludCJ9"

BOUNDARY_DATA = '{"coordinates":[448681.53750000003,279659.1125],"type":"Point"}'
MULTIPLE_EXTENTS_DATA = '{"type": "geometrycollection", "geometries": \
    [{"coordinates": [ \
        [[290000, 910000], [290100, 910000], [290100, 910100], [290000, 910100], [290000, 910000]] \
    ], "type": "Polygon", "crs": {"properties": {"name": "EPSG:27700"}, "type": "name"}}, \
    {"coordinates": [ \
        [[290001, 910001], [290101, 910001], [290101, 910101], [290001, 910101], [290001, 910001]] \
    ], "type": "Polygon", "crs": {"properties": {"name": "EPSG:27700"}, "type": "name"}}]}'


class TestLocalLandCharge(TestCase):
    def create_app(self):
        main.app.testing = True
        return main.app

    @patch('search_api.app.validate')
    @patch('search_api.resources.V2_0.local_land_charge_v_2.db')
    @patch('search_api.resources.V2_0.local_land_charge_v_2.model_mappers')
    @patch('search_api.resources.V2_0.local_land_charge_v_2.LocalLandCharge')
    @patch('search_api.resources.V2_0.local_land_charge_v_2.func')
    @patch('search_api.resources.V2_0.local_land_charge_v_2.or_')
    def test_get_land_charges_geo_results(self,
                                          mock_or,
                                          mock_funk,
                                          mock_local_land_charge,
                                          model_mappers_mock,
                                          mock_db,
                                          mock_validate):
        """Should return a 200 status and response should contain charge ids returned by query"""
        mock_charge = MagicMock()
        mock_charge.local_land_charge.display_id = CHARGE_ID
        mock_charge.local_land_charge.llc_item = {
            'registration-date': '2017-01-01'
        }

        mock_local_land_charge.query \
            .filter.return_value \
            .filter.return_value \
            .order_by.return_value \
            .count.return_value = 1

        mock_local_land_charge.query \
            .filter.return_value \
            .filter.return_value \
            .order_by.return_value \
            .all.return_value = [mock_charge]

        model_mappers_mock.map_llc_result_to_dictionary_list.return_value = [{"woo": CHARGE_ID}]
        response = self.client.post(url_for(POST_LOCAL_LAND_CHARGES_ROUTE), data=BOUNDARY_DATA,
                                    headers={'Authorization': 'Fake JWT', 'Content-Type': 'application/json'})

        model_mappers_mock.map_llc_result_to_dictionary_list.assert_called_with([mock_charge])

        self.assertIn(CHARGE_ID, response.data.decode())
        self.assertStatus(response, 200)

    @patch('search_api.app.validate')
    @patch('search_api.resources.V2_0.local_land_charge_v_2.db')
    @patch('search_api.resources.V2_0.local_land_charge_v_2.model_mappers')
    @patch('search_api.resources.V2_0.local_land_charge_v_2.LocalLandCharge')
    @patch('search_api.resources.V2_0.local_land_charge_v_2.func')
    @patch('search_api.resources.V2_0.local_land_charge_v_2.or_')
    def test_get_land_charges_geo_results_multiple_extents(self,
                                                           mock_or,
                                                           mock_funk,
                                                           mock_local_land_charge,
                                                           model_mappers_mock,
                                                           mock_db,
                                                           mock_validate):
        """Should return a 200 status and response should contain charge ids returned by query"""
        mock_charge = MagicMock()
        mock_charge.local_land_charge.display_id = CHARGE_ID
        mock_charge.local_land_charge.llc_item = {
            'registration-date': '2017-01-01'
        }

        mock_local_land_charge.query \
            .filter.return_value \
            .filter.return_value \
            .order_by.return_value \
            .count.return_value = 1

        mock_local_land_charge.query \
            .filter.return_value \
            .filter.return_value \
            .order_by.return_value \
            .all.return_value = [mock_charge]

        model_mappers_mock.map_llc_result_to_dictionary_list.return_value = [{"woo": CHARGE_ID}]
        response = self.client.post(url_for(POST_LOCAL_LAND_CHARGES_ROUTE), data=MULTIPLE_EXTENTS_DATA,
                                    headers={'Authorization': 'Fake JWT', 'Content-Type': 'application/json'})

        model_mappers_mock.map_llc_result_to_dictionary_list.assert_called_with([mock_charge])

        self.assertIn(CHARGE_ID, response.data.decode())
        self.assertStatus(response, 200)

    @patch('search_api.app.validate')
    def test_get_land_charges_no_bounding_box(self, mock_validate):
        """Should return a 400 status when request does not contain a bounding box"""
        response = self.client.post(url_for(POST_LOCAL_LAND_CHARGES_ROUTE), headers={'Authorization': 'Fake JWT'})
        self.assertIn('Failed to provide a search area.', response.data.decode())
        self.assertStatus(response, 400)

    @patch('search_api.app.validate')
    @patch('search_api.resources.V2_0.local_land_charge_v_2.db')
    @patch('search_api.resources.V2_0.local_land_charge_v_2.current_app')
    @patch('search_api.resources.V2_0.local_land_charge_v_2.LocalLandCharge')
    @patch('search_api.resources.V2_0.local_land_charge_v_2.func')
    @patch('search_api.resources.V2_0.local_land_charge_v_2.or_')
    def test_get_land_charges_in_geo_too_many_results_exception(self,
                                                                mock_or,
                                                                mock_funk,
                                                                mock_local_land_charge,
                                                                mock_app,
                                                                mock_db, mock_validate):
        """Should throw an ApplicationError returning a 507 status if more than 1000 results found"""
        mock_main_query = MagicMock()

        mock_local_land_charge.query \
            .filter.return_value \
            .filter.return_value \
            .filter.return_value \
            .order_by.return_value = mock_main_query

        mock_main_query.count.return_value = 1500

        response = self.client.post(url_for(POST_LOCAL_LAND_CHARGES_ROUTE), data=BOUNDARY_DATA,
                                    query_string={'filter': 'cancelled'},
                                    headers={'Authorization': 'Fake JWT', 'Content-Type': 'application/json'})

        self.assertIn('Too many charges, search a smaller area', response.data.decode())
        self.assertStatus(response, 507)

        expected_string = "Search-area: {0}, Number-of-charges: {1}, Normal-limit: {2}, Too many charges returned"\
            .format(json.loads(BOUNDARY_DATA), 1500, 1000)
        mock_app.logger.info.assert_called_with(expected_string)

    @patch('search_api.app.validate')
    @patch('search_api.resources.V2_0.local_land_charge_v_2.db')
    @patch('search_api.resources.V2_0.local_land_charge_v_2.LocalLandCharge')
    @patch('search_api.resources.V2_0.local_land_charge_v_2.func')
    @patch('search_api.resources.V2_0.local_land_charge_v_2.or_')
    def test_get_land_charges_in_geo_too_many_results_when_max_defined_exception(self,
                                                                                 mock_or,
                                                                                 mock_funk,
                                                                                 mock_local_land_charge,
                                                                                 mock_db, mock_validate):
        """Should throw an ApplicationError returning a 507 status if more than 200 results found"""
        mock_main_query = MagicMock()

        mock_local_land_charge.query \
            .filter.return_value \
            .filter.return_value \
            .filter.return_value \
            .order_by.return_value = mock_main_query

        mock_main_query.count.return_value = 201

        response = self.client.post(url_for(POST_LOCAL_LAND_CHARGES_ROUTE), data=BOUNDARY_DATA,
                                    query_string={'filter': 'cancelled',
                                                  'maxResults': '200'},
                                    headers={'Authorization': 'Fake JWT', 'Content-Type': 'application/json'})

        self.assertIn('Too many charges, search a smaller area', response.data.decode())
        self.assertStatus(response, 507)

    @patch('search_api.app.validate')
    @patch('search_api.resources.V2_0.local_land_charge_v_2.db')
    @patch('search_api.resources.V2_0.local_land_charge_v_2.LocalLandCharge')
    @patch('search_api.resources.V2_0.local_land_charge_v_2.func')
    @patch('search_api.resources.V2_0.local_land_charge_v_2.or_')
    def test_get_land_charges_in_geo_no_results_exception(self,
                                                          mock_or,
                                                          mock_funk,
                                                          mock_local_land_charge,
                                                          mock_db,
                                                          mock_validate):
        """Should throw an ApplicationError returning a 404 status if no charge ids where found"""
        mock_main_query = MagicMock()

        mock_local_land_charge.query \
            .filter.return_value \
            .filter.return_value \
            .order_by.return_value = mock_main_query

        mock_main_query.count.return_value = 0
        mock_main_query.limit.return_value \
            .offset.return_value \
            .all.return_value = []

        response = self.client.post(url_for(POST_LOCAL_LAND_CHARGES_ROUTE), data=BOUNDARY_DATA,
                                    headers={'Authorization': 'Fake JWT', 'Content-Type': 'application/json'})

        self.assertIn('No land charges found', response.data.decode())
        self.assertStatus(response, 404)

    @patch('search_api.app.validate')
    @patch('search_api.resources.V2_0.local_land_charge_v_2.model_mappers')
    @patch('search_api.resources.V2_0.local_land_charge_v_2.LocalLandCharge')
    def test_get_land_charges_by_further_info_ref(self, mock_llc_query, model_mappers_mock, mock_validate):
        """Should return a 200 status and response should contain charge ids returned by query"""
        mock_charge = MagicMock()
        mock_charge.display_id = CHARGE_ID
        mock_charge.llc_item = {
            'registration-date': '2017-01-01'
        }

        mock_llc_query.query.filter.return_value.order_by.return_value.all.return_value = [mock_charge]

        model_mappers_mock.map_llc_result_to_dictionary_list.return_value = [{"woo": CHARGE_ID}]

        response = self.client.get(url_for(GET_LOCAL_LAND_CHARGES_ROUTE, furtherInformationReference="KD-1337"),
                                   headers={'Authorization': 'Fake JWT'})

        model_mappers_mock.map_llc_result_to_dictionary_list.assert_called_with([mock_charge])

        self.assertIn(CHARGE_ID, response.data.decode())
        self.assertStatus(response, 200)

    @patch('search_api.app.validate')
    @patch('search_api.resources.V2_0.local_land_charge_v_2.LocalLandCharge')
    def test_get_land_charges_by_further_info_ref_no_results(self, mock_llc_query, mock_validate):
        """Should return a 200 status and response should contain charge ids returned by query"""
        mock_llc_query.query.filter.return_value.order_by.return_value.all.return_value = []

        response = self.client.get(url_for(GET_LOCAL_LAND_CHARGES_ROUTE, furtherInformationReference="KD-1337"),
                                   headers={'Authorization': 'Fake JWT'})

        self.assertIn('No land charges found', response.data.decode())
        self.assertStatus(response, 404)
