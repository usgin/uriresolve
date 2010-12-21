from django.conf.urls.defaults import *
from uriresolve.models import *

urlpatterns = patterns('',
    (r'^uridetail\.html$', 'uriresolve.views.base_detail'),
    (r'^(?P<given_uri>.+)/uridetail\.html$', 'uriresolve.views.detail'),
    (r'^(?P<given_uri>.+)$', 'uriresolve.views.resolver'),    
)
