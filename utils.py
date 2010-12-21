from django.http import HttpResponse
from django.utils.encoding import iri_to_uri

class HttpResponseSeeOtherRedirect(HttpResponse):
    status_code = 303

    def __init__(self, redirect_to):
        HttpResponse.__init__(self)
        self['Location'] = iri_to_uri(redirect_to)