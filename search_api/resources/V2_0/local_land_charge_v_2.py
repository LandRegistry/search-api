import json

from flask import Blueprint, request, current_app
from geoalchemy2 import shape
from shapely.geometry import asShape
from shapely.ops import unary_union
from sqlalchemy import func, or_

from search_api.exceptions import ApplicationError
from search_api.extensions import db
from search_api.models import LocalLandCharge, GeometryFeature
from search_api.utilities import model_mappers

from search_api.resources.local_land_charge import get_local_land_charge, get_local_land_charge_history

local_land_charge_V_2 = Blueprint('local_land_charge_V_2', __name__, url_prefix='/v2.0/search')

SORT_BY_FIELD = 'registration-date'

# Register V1 Endpoints
local_land_charge_V_2.add_url_rule('/local_land_charges/<charge_id>',
                                   view_func=get_local_land_charge,
                                   methods=['GET'])

local_land_charge_V_2.add_url_rule('/local_land_charges/<charge_id>/history',
                                   view_func=get_local_land_charge_history,
                                   methods=['GET'])


@local_land_charge_V_2.route('/local_land_charges', methods=['GET'])
def get_local_land_charges():
    """Get a list of land charges"""
    current_app.logger.info("Get local land charges by filter search")

    further_information_reference = request.args.get('furtherInformationReference')
    authority_charge_id = request.args.get('authority_charge_id')
    migrating_authority = request.args.get('migrating_authority')

    if further_information_reference:
        return get_results_for_further_information_reference(further_information_reference)
    elif (authority_charge_id and migrating_authority):
        return get_results_for_originating_authority_charge(authority_charge_id, migrating_authority)
    else:
        raise ApplicationError("Failed to provide a filter.", 400, 400)


@local_land_charge_V_2.route('/local_land_charges', methods=['POST'])
def post_local_land_charges():
    """Get a list of land charges"""
    current_app.logger.info("Get local land charges by geometry search")

    geo_json_extent = request.get_json()
    charge_filter = request.args.get('filter')
    max_results = (int(request.args.get('maxResults')) if request.args.get('maxResults') else 1000)

    if geo_json_extent:
        return get_results_for_boundary(geo_json_extent, charge_filter, max_results)
    else:
        raise ApplicationError("Failed to provide a search area.", 400, 400)


def get_results_for_boundary(boundary, charge_filter, max_results):
    """Returns the results of land charges contained in a extent

    :param boundary: Extent to search for land charges within
    :param charge_filter: String indicating whether to filter out cancelled charges
    :param max_results: Max number of land charges to be returned.  Defaults to 1000
    :return: Json representation of the results
    """
    try:
        extent_shape = asShape(boundary)
        geo_extent_shape = shape.from_shape(unary_union(extent_shape), srid=27700)

        subquery = db.session.query(GeometryFeature.local_land_charge_id, GeometryFeature.geometry) \
            .distinct(GeometryFeature.local_land_charge_id) \
            .filter(func.ST_DWithin(GeometryFeature.geometry, geo_extent_shape, 0)) \
            .subquery()

        if charge_filter:
            charge_query = LocalLandCharge.query \
                .filter(LocalLandCharge.id == subquery.c.local_land_charge_id) \
                .filter(or_(~func.ST_Touches(subquery.c.geometry, geo_extent_shape),
                            ~LocalLandCharge.llc_item.contains(
                                {'charge-sub-category': 'Conditional planning consent'}))) \
                .filter(LocalLandCharge.cancelled.isnot(True)) \
                .order_by(LocalLandCharge.llc_item[SORT_BY_FIELD].desc())
        else:
            charge_query = LocalLandCharge.query \
                .filter(LocalLandCharge.id == subquery.c.local_land_charge_id) \
                .filter(or_(~func.ST_Touches(subquery.c.geometry, geo_extent_shape),
                            ~LocalLandCharge.llc_item.contains(
                                {'charge-sub-category': 'Conditional planning consent'}))) \
                .order_by(LocalLandCharge.llc_item[SORT_BY_FIELD].desc())

        num_results = charge_query.count()
        if num_results > max_results:
            current_app.logger.info("Search-area: {0}, "
                                    "Number-of-charges: {1}, "
                                    "Normal-limit: {2}, "
                                    "Too many charges returned"
                                    .format(boundary, num_results, max_results))
            raise ApplicationError("Too many charges, search a smaller area", 507, 507)

        llc_result = charge_query.all()

        if llc_result and len(llc_result) > 0:
            current_app.logger.info("Returning local land charges")
            return json.dumps(
                model_mappers.map_llc_result_to_dictionary_list(
                    llc_result)), 200, {'Content-Type': 'application/json'}
        else:
            raise ApplicationError("No land charges found", 404, 404)
    except (ValueError, TypeError) as err:
        raise ApplicationError("Unprocessable Entity. {}".format(err), 422, 422)


def get_results_for_further_information_reference(further_information_reference):
    """Returns the results of land charges which match a given further information reference

    :param further_information_reference: Authority reference to search by
    :return: Json representation of the results
    """
    features = LocalLandCharge.query \
        .filter(
            func.lower(LocalLandCharge.further_information_reference) == func.lower(further_information_reference)
        ).order_by(LocalLandCharge.llc_item[SORT_BY_FIELD].desc()) \
        .all()

    if features and len(features) > 0:
        current_app.logger.info("Returning local land charges")
        return json.dumps(
            model_mappers.map_llc_result_to_dictionary_list(
                features)), 200, {'Content-Type': 'application/json'}
    else:
        raise ApplicationError("No land charges found", 404, 404)


def get_results_for_originating_authority_charge(authority_charge_id, migrating_authority):
    """Returns the results of land charges which match a given originating authority charge identifier

    :param originating_authority_charge_identifier: originating authority charge identifier to search by
    :return: Json representation of the results
    """

    features = LocalLandCharge.query \
        .filter(
            LocalLandCharge.llc_item["originating-authority-charge-identifier"].astext == authority_charge_id,
            LocalLandCharge.llc_item["migrating-authority"].astext == migrating_authority
        ).order_by(LocalLandCharge.llc_item[SORT_BY_FIELD].desc()) \
        .all()

    if features and len(features) > 0:
        current_app.logger.info("Returning local land charges by originating authority & migrating authority")

        return json.dumps(
            model_mappers.map_llc_display_result_to_dictionary_list(
                features)), 200, {'Content-Type': 'application/json'}
    else:
        raise ApplicationError("No land charges found", 404, 404)
