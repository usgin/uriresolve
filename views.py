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
    if rule == None:
        raise Http404
        
    return redirect(rule, given_uri)
                
def description(request, given_uri=''):
    # Handle the case for the uri-gin/ URI - different template
    if given_uri == '':
        return render_to_response('uriresolve/index.html', {}, context_instance=RequestContext(request))
        
    #return HttpResponse('Description: ' + given_uri)
    
    # Find the matching rule
    rule = findMatchingRewriteRule(given_uri)
    if rule == None:
        raise Http404
        
    # Build Breadcrumbs
    requested = given_uri.split('/')
    noOfParts = len(requested)
    breadcrumb = '/ <a href="/uri-gin/uri-description/">uri-gin</a> / '
    uriPart = ''
    
    for i in range(noOfParts):
        if requested[i] == '':
            continue
        
        uriPart += requested[i] + '/'
        thisRule = findMatchingRewriteRule(uriPart)
        if thisRule == None:
            breadcrumb += requested[i] + ' / '
        else:
            breadcrumb += '<a href="/uri-gin/' + uriPart + 'uri-description/">' + requested[i] + '</a> / '
    # If this is a resource type registry, use a different template
    
    if given_uri[len(given_uri)-5:] == 'type/' and len(given_uri.split('/')) == 3:
        # Find all the resource types that are defined in this guy's name authority
        authorityName = given_uri.split('/')[0]
        authority = name_authority.objects.get(name=authorityName)
        types = resource_type.objects.filter(name_authority=authority)
        
        # Render the registry details page
        return render_to_response('uriresolve/registrydetail.html', { 'given_uri': rule, 'breadcrumbs': breadcrumb, 'resource_types': types })
    else:
        return render_to_response('uriresolve/detail.html', { 'given_uri': rule, 'breadcrumbs': breadcrumb })
    
def jsonTypesByAuthority(request, authority_name):
    authority = name_authority.objects.get(name=authority_name)
    result = serializers.serialize('json', resource_type.objects.filter(name_authority = authority))
    return HttpResponse(result, mimetype='application/json')
