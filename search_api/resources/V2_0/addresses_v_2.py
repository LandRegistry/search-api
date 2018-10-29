import json
import re

from flask import Blueprint, current_app, g, Response

from search_api import config
from search_api.exceptions import ApplicationError
from search_api.utilities.V2_0 import address_response_mapper_v_2
from flask.globals import request

addresses_V_2 = Blueprint('addresses_V_2', __name__, url_prefix='/v2.0/search/addresses')

body = {
    "datasource": "local_authority",
    "search_type": "",
    "query_value": "",
    "response_srid": "EPSG:27700",
    "max_results": 1000
}
postcode_regex_check = '^([Gg][Ii][Rr] 0[Aa]{2})|((([A-Za-z][0-9]{1,2})|(([A-Za-z][A-Ha-hJ-Yj-y][0-9]{1,2})' \
                       '|(([A-Za-z][0-9][A-Za-z])|([A-Za-z][A-Ha-hJ-Yj-y][0-9]?[A-Za-z])))) [0-9][A-Za-z]{2})$'

uprn_regex_check = '^[0-9]{6,12}$'
usrn_regex_check = '^\d+$'


@addresses_V_2.route('/postcode/<postcode>', methods=['GET'])
def get_addresses_by_postcode(postcode):
    current_app.logger.info("Get address by postcode '%s'", postcode)
    postcode = postcode.strip()
    postcode_is_valid = re.match(postcode_regex_check, postcode)

    if postcode_is_valid is not None:
        body["search_type"] = "postcode"
        body["query_value"] = postcode
        return search_for_addresses(body)
    else:
        raise ApplicationError("Unprocessable Entity: Postcode is not valid", 422, 422)


@addresses_V_2.route('/uprn/<uprn>', methods=['GET'])
def get_addresses_by_uprn(uprn):
    current_app.logger.info("Get address by UPRN '%s'", uprn)
    uprn = uprn.strip()
    uprn_is_valid = re.match(uprn_regex_check, uprn)

    if uprn_is_valid is not None:
        body["search_type"] = "uprn"
        body["query_value"] = int(uprn)
        return search_for_addresses(body)
    else:
        raise ApplicationError("Unprocessable Entity: UPRN is not valid", 422, 422)


@addresses_V_2.route('/usrn/<usrn>', methods=['GET'])
def get_addresses_by_usrn(usrn):
    current_app.logger.info("Get address by USRN '%s'", usrn)
    usrn = usrn.strip()
    usrn_is_valid = re.match(usrn_regex_check, usrn)

    if usrn_is_valid is not None:
        body["search_type"] = "usrn"
        body["query_value"] = int(usrn)
        return search_for_addresses(body)
    else:
        raise ApplicationError("Unprocessable Entity: USRN is not valid", 422, 422)


@addresses_V_2.route('/text/<text>', methods=['GET'])
def get_addresses_by_text(text):
    current_app.logger.info("Get address by text '%s'", text)
    text = text.strip()

    body["search_type"] = "text_search"
    body["query_value"] = text

    return search_for_addresses(body)


def search_for_addresses(request_body):
    current_app.logger.info("Performing address search")
    search_results = g.requests.post(config.ADDRESS_API_URL + '/v2/addresses/search',
                                     data=json.dumps(request_body, sort_keys=True),
                                     headers={"Content-Type": "application/json", "Accept": "application/json"})
    if search_results.status_code == 400:
        raise ApplicationError(search_results.json(), 400, 400)
    if search_results.status_code != 200:
        raise ApplicationError(search_results.json(), 500, 500)
    if not search_results.json():
        current_app.logger.warning("No addresses found for search")
        raise ApplicationError("No addresses found for search.", 404, 404)

    mapped_resp = address_response_mapper_v_2.map_address_response(search_results.json())

    # If index_map argument set to true, get index map for all the addresses
    if request.args.get('index_map') and request.args.get('index_map').lower() == 'true' and config.INDEX_MAP_API_URL:
        for address in mapped_resp:
            if 'uprn' in address and address['uprn']:
                index_map = search_for_index_map(address['uprn'])
                if index_map:
                    address['index_map'] = index_map

    current_app.logger.info("Returning address search result")
    return Response(
        response=json.dumps(mapped_resp),
        status=200,
        mimetype="application/json"
    )


def search_for_index_map(uprn):
    current_app.logger.info("Performing uprn title search")

    title_resp = g.requests.get('{}/v1/uprns/{}'.format(config.INDEX_MAP_API_URL, uprn),
                                headers={"Content-Type": "application/json", "Accept": "application/json"})
    if title_resp.status_code == 200:
        features = []
        for title in title_resp.json():
            current_app.logger.info("Performing index map search")
            index_map_resp = g.requests.get(
                '{}/v1/index_map/{}'.format(config.INDEX_MAP_API_URL, title),
                headers={"Content-Type": "application/json", "Accept": "application/json"})
            if index_map_resp.status_code == 200:
                index_map_json = index_map_resp.json()
                features = features + index_map_json['features']
            elif index_map_resp.status_code != 404:
                raise ApplicationError(index_map_resp.json(), 500, 500)
        if features:
            return {"type": "FeatureCollection",
                    "features": features}
    elif title_resp.status_code != 404:
        raise ApplicationError(title_resp.json(), 500, 500)

    return None
