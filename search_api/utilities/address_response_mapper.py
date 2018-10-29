import string


def map_address_response(address_response, search_type):
    list_of_address_results = list()

    for address in address_response:
        address_result = {
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
            "town": string.capwords(address['town_name']),
        }
        list_of_address_results.append(address_result)
    return list_of_address_results


def is_street_search(address_response):
    streets_list = list()
    town_list = list()
    for addresses in address_response:
        current_street = addresses["street_description"]
        current_town = addresses['town_name']
        if current_street not in streets_list:
            streets_list.append(current_street)
        if current_town not in town_list:
            town_list.append(current_town)
    return len(streets_list) == 1 and len(town_list) == 1


def get_display_address_title_case(display_address):
    return string.capwords(display_address.rsplit(',', 1)[0]) + display_address.rsplit(',', 1)[1]
