from django.conf import settings
from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin


class TemplateMiddleware(MiddlewareMixin):
    def __init__(self, get_response=None):
        super().__init__(get_response)

    def process_request(self, request):
        print(request.path)

    def process_response(self, request, response):
        print('bbbb')
        return response
