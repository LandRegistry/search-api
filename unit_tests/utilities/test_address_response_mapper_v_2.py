import json
import unittest

from search_api.main import app
from search_api.utilities.V2_0 import address_response_mapper_v_2
from unit_tests.data import mapper_v_2_in, mapper_v_2_out


class TestAddressResponseMapper(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_mapper_property(self):
        filtered_result = json.dumps(address_response_mapper_v_2.map_address_response
                                     (mapper_v_2_in.property_data), sort_keys=True)
        mapper_v_2_out_json = json.dumps(mapper_v_2_out.property_data, sort_keys=True)
        self.assertEqual(filtered_result, mapper_v_2_out_json)

    def test_mapper_street(self):
        filtered_result = json.dumps(address_response_mapper_v_2.map_address_response
                                     (mapper_v_2_in.street_data), sort_keys=True)
        mapper_v_2_out_json = json.dumps(mapper_v_2_out.street_data, sort_keys=True)
        self.assertEqual(filtered_result, mapper_v_2_out_json)
