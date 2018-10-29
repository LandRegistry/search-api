import base64
import json

from flask import Blueprint, request, current_app
from geoalchemy2 import shape
from shapely.geometry import asShape
from sqlalchemy import func

from search_api.exceptions import ApplicationError
from search_api.extensions import db
from search_api.models import LocalLandCharge, LocalLandChargeHistory, GeometryFeature
from search_api.utilities import model_mappers
from search_api.utilities.charge_id import is_valid_charge_id, decode_charge_id

local_land_charge = Blueprint('local_land_charge', __name__, url_prefix='/search')


@local_land_charge.route('/local_land_charges/<charge_id>', methods=['GET'])
def get_local_land_charge(charge_id):
    """Get local land charge

    Returns local land charge with specified charge_id
    """
    current_app.logger.info("Get local land charge by ID '%s'", charge_id)
    charge_id_param = charge_id.upper()

    if is_valid_charge_id(charge_id_param):
        charge_id_base_10 = decode_charge_id(charge_id_param)
        llc_result = LocalLandCharge.query.get(charge_id_base_10)
    else:
        raise ApplicationError("Invalid Land Charge Number", 422, 422)

    if not llc_result:
        raise ApplicationError("No land charges found.", 404, 404)

    current_app.logger.info("Returning local land charge '%s'", charge_id)
    return json.dumps(model_mappers.map_llc_result_to_dictionary_list(llc_result)), \
        200, {'Content-Type': 'application/json'}


@local_land_charge.route('/local_land_charges/', methods=['GET'])
def get_local_land_charges():
    """Get a list of land charges

    Returns all if no parameter is required, otherwise it will return
    those contained in bounding box.
    """
    current_app.logger.info("Get local land charges by geometry search")
    geo_json_extent = request.args.get('boundingBox')
    if geo_json_extent:
        try:
            json_extent = json.loads(base64.b64decode(geo_json_extent).decode())
            extent_shape = asShape(json_extent)

            features = GeometryFeature.query.filter(
                func.ST_Intersects(
                    GeometryFeature.geometry, shape.from_shape(extent_shape, srid=27700)
                )).options(db.joinedload(GeometryFeature.local_land_charge)).all()
            res_set = set()
            for feature in features:
                res_set.add(feature.local_land_charge)
            llc_result = list(res_set)

        except (ValueError, TypeError) as err:
            raise ApplicationError("Unprocessable Entity. {}".format(err), 422, 422)
    else:
        current_app.logger.warning("No bounding box supplied - returning all local land charges")
        llc_result = LocalLandCharge.query.all()

    if not llc_result or len(llc_result) == 0:
        raise ApplicationError("No land charges found", 404, 404)

    current_app.logger.info("Returning local land charges")
    return json.dumps(model_mappers.map_llc_result_to_dictionary_list(llc_result)), \
        200, {'Content-Type': 'application/json'}


@local_land_charge.route('/local_land_charges/<charge_id>/history', methods=['GET'])
def get_local_land_charge_history(charge_id):
    """Get history of land charge.

    Returns all history for local land charge with charge_id
    """
    current_app.logger.info("Get local land charge history by ID '%s'", charge_id)
    charge_id_param = charge_id.upper()

    if is_valid_charge_id(charge_id_param):
        charge_id_base_10 = decode_charge_id(charge_id_param)

        llc_result = LocalLandChargeHistory.query.filter(LocalLandChargeHistory.id == charge_id_base_10)\
            .order_by(LocalLandChargeHistory.entry_timestamp).all()
    else:
        raise ApplicationError("Invalid Land Charge Number", 422, 422)

    if not llc_result:
        raise ApplicationError("No land charge history found.", 404, 404)

    current_app.logger.info("Returning local land charge history")
    return json.dumps(model_mappers.map_llc_history_result_to_dictionary_list(llc_result)), \
        200, {'Content-Type': 'application/json'}
