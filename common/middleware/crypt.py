from django.conf import settings
from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin
from common.utils.encryptutil import encrypt, decrypt
from common.utils.jsonutil import loads


class EncryptMiddleware(MiddlewareMixin):
    def __init__(self, get_response=None):
        super().__init__(get_response)

    def process_request(self, request):
        if settings.SECRET_MODE and request.method == 'POST':
            body = loads(request.body).get('body')
            request._body = decrypt(body)

    def process_response(self, request, response):
        if settings.SECRET_MODE and request.method == 'POST':
            return HttpResponse(encrypt(response.content.decode()))
        return response
