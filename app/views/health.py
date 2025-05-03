from app.utils.common import send_json_response
from app.utils.constants import HttpStatusCode


def health_check():
    return send_json_response(response_status=True, message_key="Details Fetched Successfully",
                              http_status=HttpStatusCode.OK.value)
