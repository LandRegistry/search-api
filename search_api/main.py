# This file is the entry point.
# First we import the app object, which will get initialised as we do it. Then import methods we're about to use.
from search_api.app import app
from search_api.blueprints import register_blueprints
from search_api.exceptions import register_exception_handlers
from search_api.extensions import register_extensions

# Now we register any extensions we use into the app
register_extensions(app)
# Register the exception handlers
register_exception_handlers(app)
# Finally we register our blueprints to get our routes up and running.
register_blueprints(app)
