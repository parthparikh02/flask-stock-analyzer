from flask import jsonify
from typing import Any


def send_json_response(http_status: int, response_status: bool, message_key: str, data: Any = None,
                       error: Any = None) -> tuple:
    """This method used to send JSON response in custom dir structure. Here, status represents boolean value true/false
    and http_status is http response status code."""

    if data is None and error is None:
        return jsonify({'status': response_status, 'message': message_key}), http_status
    if response_status:
        return jsonify({'status': response_status, 'message': message_key, 'data': data}), http_status
    else:
        return jsonify({'status': response_status, 'message': message_key, 'error': error}), http_status
