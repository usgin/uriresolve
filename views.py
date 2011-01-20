from uriresolve.models import *
from uriresolve.utils import HttpResponseSeeOtherRedirect, findMatchingRewriteRule, redirect
from django.http import HttpResponse, Http404
from django.shortcuts import get_list_or_404, render_to_response
from django.template import RequestContext
from django.db.models import Q
from django.core import serializers
import re
    
def resolver(request, given_uri):
    # return HttpResponse('Resolver: ' + given_uri)
    rule = findMatchingRewriteRule(given_uri)
    return redirect(rule, given_uri)
                
def description(request, given_uri=''):
    return HttpResponse('Description: ' + given_uri)
            
def jsonTypesByAuthority(request, authority_name):
    authority = name_authority.objects.get(name=authority_name)
    result = serializers.serialize('json', resource_type.objects.filter(name_authority = authority))
    return HttpResponse(result, mimetype='application/json')
