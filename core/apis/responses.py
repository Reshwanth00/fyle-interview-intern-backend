from flask import Response, jsonify, make_response

class APIResponse(Response):
    @classmethod
    def respond(cls, data, status=200):
        """Respond with JSON data and a status code."""
        response_data = {"data": data}
        return make_response(jsonify(response_data), status)

    @classmethod
    def respond_error(cls, message, status):
        """Respond with an error message and a status code."""
        response_data = {"error": message}
        return make_response(jsonify(response_data), status)
    
    @classmethod
    def submit_respond_error(cls, message, status):
        """Respond with an error message and a status code."""
        response_data = {'error': 'FyleError',
                         "message":message}
        return make_response(jsonify(response_data), status)
