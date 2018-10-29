# Import every blueprint file
from search_api.resources import addresses
from search_api.resources import general
from search_api.resources import local_land_charge
from search_api.resources.V2_0 import local_land_charge_v_2
from search_api.resources.V2_0 import addresses_v_2


def register_blueprints(app):
    """Adds all blueprint objects into the app."""
    app.register_blueprint(general.general)
    app.register_blueprint(local_land_charge.local_land_charge)
    app.register_blueprint(local_land_charge_v_2.local_land_charge_V_2)
    app.register_blueprint(addresses.addresses)
    app.register_blueprint(addresses_v_2.addresses_V_2)

    # All done!
    app.logger.info("Blueprints registered")
