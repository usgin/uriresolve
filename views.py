from uriresolve.models import *
from uriresolve.utils import HttpResponseSeeOtherRedirect
from django.http import HttpResponse, Http404
from django.shortcuts import get_list_or_404, render_to_response
from django.template import RequestContext
from django.db.models import Q
from django.core import serializers
import re

def index(request):
    # Show a listing of URIs available on this server
    listing = rewrite_rule.objects.all()
    return render_to_response(
        'uriresolve/index.html',
        { 'redirection_list': listing, }, 
        context_instance=RequestContext(request)
    )
    
def resolver(request, given_uri):
    # return HttpResponse(given_uri)
    
    # Get the set of rewrite_rules
    rules = rewrite_rule.objects.all()
    for rule in rules:
        if  re.match(rule.uri_expression, given_uri) != None:
            # Got a match
            match = re.match(rule.uri_expression, given_uri)
            
            if match.lastindex == None:
                # This occurs if there is a direct match and no replacements. The regular expression had no capture blocks in it.
                return HttpResponseSeeOtherRedirect(rule.url_string)
            else:
                # There were capture groups to take into account.
                redirection = rule.url_string
                
                # Loop through each captured group and adjust the rule's URL String, replacing appropriately
                for i in range(match.lastindex):
                    redirection = re.sub('\$' + str(i + 1), match.group(i + 1), redirection)
                return HttpResponseSeeOtherRedirect(redirection)
    
    # No matches were found.
    raise Http404
                
def detail(request, given_uri=''):
    
    raise Http404
            
def jsonTypesByAuthority(request, authority_name):
    authority = name_authority.objects.get(name=authority_name)
    result = serializers.serialize('json', resource_type.objects.filter(name_authority = authority))
    return HttpResponse(result, mimetype='application/json')
    # return HttpResponse(nameAuthorityId)
    