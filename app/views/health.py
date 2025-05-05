from app.utils.common import send_json_response
from app.utils.constants import HttpStatusCode


def health_check():
    """
        Health Check
        ---
        tags:
          - Utility
        summary: Check if the service is running
        responses:
          200:
            description: Service is up and running
            schema:
              type: object
              properties:
                status:
                  type: boolean
                  example: true
                message:
                  type: string
                  example: "Details Fetched Successfully"
        """
    return send_json_response(response_status=True, message_key="Details Fetched Successfully",
                              http_status=HttpStatusCode.OK.value)
