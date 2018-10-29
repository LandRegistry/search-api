import string


def map_address_response(address_response):
    list_of_address_results = list()

    if address_response["result-type"] == "property":
        # Search results will either be a list of properties or streets
        address_list = address_response["search-result"]
        for address in address_list:
            address_result = {
                "address_type": "property",
                "address": get_display_address_title_case(address['formatted_address']),
                "geometry": address['geom'],
                "postcode": address['postcode_locator'],
                "uprn": address['uprn'],
                "line_1": string.capwords(address['address_line_1']),
                "line_2": string.capwords(address['address_line_2']),
                "line_3": string.capwords(address['address_line_3']),
                "line_4": string.capwords(address['address_line_4']),
                "line_5": string.capwords(address['address_line_5']),
                "line_6": string.capwords(address['address_line_6']),
                "street": string.capwords(address['street_description']),
                "town": string.capwords(address['town_name'])
            }
            list_of_address_results.append(address_result)

    elif address_response["result-type"] == "street":
        street_list = address_response["search-result"]
        for street in street_list:
            address_result = {
                "address_type": "street",
                "address": get_display_address_title_case(street['street_text']),
                "usrn": street["usrn"],
                "geometry": street['geom'],
                "postcode": street['partial_postcode']
            }
            list_of_address_results.append(address_result)

    return list_of_address_results


def get_display_address_title_case(display_address):
    return string.capwords(display_address.rsplit(',', 1)[0]) + display_address.rsplit(',', 1)[1]
