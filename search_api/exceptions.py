from flask import current_app, Response
import json


class ApplicationError(Exception):
    """This class is raised when the application identifies there's been a problem and the client should be informed.

    Example: raise ApplicationError("Title number invalid", "E102", 400)
    The handler method will then create the response body in a standard structure so clients
    will always know what to parse.

    """

    def __init__(self, message, code, http_code=500):
        Exception.__init__(self)
        self.message = message
        self.http_code = http_code
        self.code = code

    # For ApplicationErrors raised in this API we will submit a response
    # appropriate for our API
    def response(self):
        return Response(
            response=json.dumps(
                {"error_message": self.message, "error_code": self.code}),
            status=self.http_code,
            mimetype='application/json'
        )


def unhandled_exception(e):
    current_app.logger.exception('Unhandled Exception: %s', repr(e))
    return ApplicationError("Internal Server Error", 500, 500).response()


def application_error(e):
    current_app.logger.warning(
        'Application Exception: %s', repr(e), exc_info=True)
    return e.response()


def register_exception_handlers(app):
    app.register_error_handler(ApplicationError, application_error)
    app.register_error_handler(Exception, unhandled_exception)

    app.logger.info("Exception handlers registered")
