from rest_framework.exceptions import APIException


class BadRequest(APIException):
    status_code = 400
    default_detail = 'bad data received, check the structure is needed by server to process'
    default_code = "bad request"



