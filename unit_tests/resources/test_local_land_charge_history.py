from search_api import main
from flask_testing import TestCase
from flask import url_for
from mock import patch

CHARGE_ID = 'LLC-6521'
INVALID_CHARGE_ID = 'some_invalid_charge_id'
LOCAL_LAND_CHARGES_HISTORY_ROUTE = 'local_land_charge.get_local_land_charge_history'


class TestLocalLandChargeHistory(TestCase):

    def create_app(self):
        main.app.testing = True
        return main.app

    @patch('search_api.app.validate')
    @patch('search_api.resources.local_land_charge.model_mappers')
    @patch('search_api.resources.local_land_charge.is_valid_charge_id')
    @patch('search_api.resources.local_land_charge.decode_charge_id')
    @patch('search_api.resources.local_land_charge.LocalLandChargeHistory')
    def test_get_land_charge_history_with_valid_charge_id(
            self, llc_query_mock, decode_charge_id_mock, is_valid_charge_id_mock, model_mappers_mock, mock_validate):
        """Valid ID test

        Should pass the given charge id to the charge id service to decode it, then use it to query the charge ids,
        and pass the charge ids to the mapper.
        """
        is_valid_charge_id_mock.return_value = True
        decode_charge_id_mock.return_value = CHARGE_ID
        llc_query_mock.query.filter.return_value.order_by.return_value.all.return_value = CHARGE_ID
        model_mappers_mock.map_llc_history_result_to_dictionary_list.return_value = CHARGE_ID

        response = self.client.get(url_for(LOCAL_LAND_CHARGES_HISTORY_ROUTE,
                                           charge_id=CHARGE_ID), headers={'Authorization': 'Fake JWT'})

        decode_charge_id_mock.assert_called_with(CHARGE_ID)
        llc_query_mock.query.filter.assert_called()
        model_mappers_mock.map_llc_history_result_to_dictionary_list.assert_called_with(CHARGE_ID)

        self.assertIn(CHARGE_ID, response.data.decode())
        self.assertStatus(response, 200)

    @patch('search_api.app.validate')
    @patch('search_api.resources.local_land_charge.is_valid_charge_id')
    def test_get_land_charge_history_with_invalid_charge_id(self, is_valid_charge_id_mock, mock_validate):
        """Should throw an ApplicationError returning a status of 422 if the given charge id is invalid"""
        is_valid_charge_id_mock.return_value = False
        response = self.client.get(url_for(LOCAL_LAND_CHARGES_HISTORY_ROUTE,
                                           charge_id=INVALID_CHARGE_ID), headers={'Authorization': 'Fake JWT'})

        self.assertIn('Invalid Land Charge Number', response.data.decode())
        self.assertStatus(response, 422)

    @patch('search_api.app.validate')
    @patch('search_api.resources.local_land_charge.is_valid_charge_id')
    @patch('search_api.resources.local_land_charge.LocalLandChargeHistory')
    def test_get_land_charge_history_with_no_results_returned(self, llc_query_mock, is_valid_charge_id_mock,
                                                              mock_validate):
        """Should throw an ApplicationError returning a status of 404 if no charges with the given id where found"""
        is_valid_charge_id_mock.return_value = True
        llc_query_mock.query.filter.return_value.order_by.return_value.all.return_value = None

        response = self.client.get(url_for(LOCAL_LAND_CHARGES_HISTORY_ROUTE,
                                           charge_id=CHARGE_ID), headers={'Authorization': 'Fake JWT'})
        self.assertIn('No land charge history found.', response.data.decode())
        self.assertStatus(response, 404)
