from typing import Dict,Tuple
import requests

from django.contrib.sites.models import Site

from suds.client import Client

ZARINPAL_WEBSERVICE:str = "https://www.zarinpal.com/pg/services/WebGate/wsdl"
ZARINPAL_PAYMENT_URL:str = "https://www.zarinpal.com/pg/StartPay/"

class ZarinaPalPayment:
    def __init__(self,merchant_id:str,amount:int,**moreinfo:str) -> None:
        self.__merchant_id :str = merchant_id
        self.__amount:int = amount
        self.__moreinfo:Dict[str,str] = moreinfo
        self.__domain_name:str = Site.objects.get_current().domain or moreinfo.get("domain_name")

    def pay(self) -> None:
        """this method do payment job and uses data that has taken in __init__ (Constructor) method

        Raises:
            Exception: if mission being failed , a error raise
        """
        client = Client(ZARINPAL_WEBSERVICE)
        result = client.service.PaymentRequest(self.__merchant_id,
                                           self.__amount,
                                           self.__moreinfo.get("desciption",""),
                                           self.__moreinfo.get("email",""),
                                           self.__moreinfo.get("mobile",""),
                                           self.__domain_name + "/verify/")
        if result.Status == 100:
            requests.get(ZARINPAL_PAYMENT_URL + result.Authority)
        else:
            raise Exception("Failed in mission")

    def verify(self,request) -> Tuple[bool,str]:
        client = Client(ZARINPAL_WEBSERVICE)
        if request.GET.get("Status") == "OK":
            result = client.service.PaymentVerification(self.__merchant_id,
                                                    request.GET.get['Authority'],
                                                    self.__amount)
            if result.Status == 100:
                return True,"Transaction Success"
            elif result.Status == 101:
                return True,"Transaction Submited"
            else:
                return False,"Transaction Failed"
        else:
            return False,"Transaction failed or canceled by user"