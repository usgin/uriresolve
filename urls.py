from django.conf.urls.defaults import *
from uriresolve.models import *

urlpatterns = patterns('',
    (r'^$', 'django.views.generic.simple.redirect_to', {'url': 'uri-description/'}),
    (r'^(?P<authority_name>.+)/type/json$', 'uriresolve.views.jsonTypesByAuthority'),
    (r'^(?P<given_uri>.*)uri-description(?:/|\.html)$', 'uriresolve.views.description'),
    (r'^(?P<given_uri>.+)$', 'uriresolve.views.resolver'),
)
