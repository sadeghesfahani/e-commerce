from django.views.generic import detail
from h11._abnf import status_code
from rest_framework.exceptions import APIException


class BadRequest(APIException):
    status_code = 400
    default_detail = 'bad data received, check the structure is needed by server to process'
    default_code = "bad request"


class CalculationFailure(APIException):
    message = ""
    detail = ""

    def __init__(self, message_txt=None, detail_txt=None):
        if message_txt is not None:
            CalculationFailure.message = message_txt
        if detail_txt is not None:
            CalculationFailure.detail = detail_txt

    status_code = 400
    default_detail = 'calculation for probability failed'
    default_code = "bad request"
