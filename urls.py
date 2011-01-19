from django.conf.urls.defaults import *
from uriresolve.models import *

urlpatterns = patterns('',
    (r'^$', 'django.views.generic.simple.redirect_to', {'url': '/uri-gin/description/'}),
    (r'^description(?:/|\.html)$', 'uriresolve.views.index'),
    (r'^(?P<authority_name>.+)/type/json$', 'uriresolve.views.jsonTypesByAuthority'),
    # (r'^(?P<given_uri>.+)/description(?:/|\.html)$', 'uriresolve.views.detail'),
    (r'^(?P<given_uri>.+)$', 'uriresolve.views.resolver'),
    
)
