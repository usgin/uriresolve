from uriresolve.models import *
from uriresolve.utils import HttpResponseSeeOtherRedirect
from django.http import HttpResponse, Http404
from django.shortcuts import get_list_or_404, render_to_response
from django.template import RequestContext
from django.db.models import Q
from django.core import serializers

def index(request):
    # Show a listing of URIs available on this server
    listing = redirection.objects.all()
    return render_to_response(
        'uriresolve/index.html',
        { 'redirection_list': listing, }, 
        context_instance=RequestContext(request)
    )
    
def resolver(request, given_uri):
    
    raise Http404
                
def detail(request, given_uri=''):
    
    raise Http404
            
def jsonTypesByAuthority(request, authority_name):
    authority = name_authority.objects.get(name=authority_name)
    result = serializers.serialize('json', resource_type.objects.filter(name_authority = authority))
    return HttpResponse(result, mimetype='application/json')
    # return HttpResponse(nameAuthorityId)
    